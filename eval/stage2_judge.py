"""Stage 2: LLM-as-a-Judge (blind) über Rohantworten."""

from __future__ import annotations

import argparse
import sys
import threading
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from lib.clients import call_judge
from lib.io_utils import (
    append_jsonl,
    load_completed_keys,
    load_jsonl,
    load_questions,
    log_error,
    utc_now_iso,
)
from lib.parallel import run_bounded_parallel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage 2: Antworten bewerten")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Nur die ersten N Rohantworten bewerten",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    questions_by_id = {q["question_id"]: q for q in load_questions()}
    raw_rows = load_jsonl(config.RAW_RESPONSES_JSONL)
    if args.limit is not None:
        raw_rows = raw_rows[: args.limit]

    completed = load_completed_keys(config.JUDGED_RESULTS_JSONL)
    total = len(raw_rows)
    skipped = sum(
        1
        for row in raw_rows
        if (row.get("question_id"), row.get("config_id")) in completed
    )

    print(f"Stage 2: {total} Rohantworten zu bewerten (Judge: {config.JUDGE_MODEL})")
    print(f"Parallelität: judge={config.JUDGE_WORKERS}")

    pending = [
        row
        for row in raw_rows
        if (row.get("question_id"), row.get("config_id")) not in completed
    ]

    print_lock = threading.Lock()
    completed_lock = threading.Lock()

    def worker(row: dict[str, Any]) -> dict[str, Any]:
        qid = row.get("question_id")
        config_id = row.get("config_id")
        question = questions_by_id.get(qid)
        if question is None:
            log_error(f"Stage2: Unbekannte question_id {qid!r}")
            raise ValueError(f"unbekannte question_id {qid!r}")

        answer = row.get("answer") or ""
        meta_error = (row.get("meta") or {}).get("error")
        if meta_error:
            log_error(f"Stage2 {qid}/{config_id}: überspringe wegen Generierungsfehler")
            record = {
                "question_id": qid,
                "config_id": config_id,
                "korrektheit": "enthaltung",
                "vollstaendigkeit": "unvollstaendig",
                "begruendung": f"Keine gültige Antwort (Generierungsfehler: {meta_error})",
                "judge_model": config.JUDGE_MODEL,
                "judge_ts": utc_now_iso(),
            }
            append_jsonl(config.JUDGED_RESULTS_JSONL, record)
            with print_lock:
                print(f"SKIP {qid} / {config_id} (Generierungsfehler)")
            return record

        try:
            result = call_judge(question["frage"], question["musterloesung"], answer, question.get("item_typ", "beantwortbar"))
        except Exception as first_exc:  # noqa: BLE001
            try:
                result = call_judge(question["frage"], question["musterloesung"], answer, question.get("item_typ", "beantwortbar"))
            except Exception as second_exc:  # noqa: BLE001
                msg = (
                    f"Stage2 {qid}/{config_id}: Judge fehlgeschlagen — "
                    f"{type(first_exc).__name__}: {first_exc}; "
                    f"Retry {type(second_exc).__name__}: {second_exc}"
                )
                log_error(msg)
                with print_lock:
                    print(f"ERR {qid} / {config_id}")
                raise

        record = {
            "question_id": qid,
            "config_id": config_id,
            "korrektheit": result["korrektheit"],
            "vollstaendigkeit": result["vollstaendigkeit"],
            "begruendung": result["begruendung"],
            "judge_model": config.JUDGE_MODEL,
            "judge_ts": utc_now_iso(),
        }
        append_jsonl(config.JUDGED_RESULTS_JSONL, record)
        with print_lock:
            print(f"OK  {qid} / {config_id}: {result['korrektheit']}, {result['vollstaendigkeit']}")
        return record

    def on_success(row: dict[str, Any], _record: dict[str, Any]) -> None:
        with completed_lock:
            completed.add((row.get("question_id"), row.get("config_id")))

    def on_error(_row: dict[str, Any], _exc: Exception) -> None:
        pass

    judged, errors = run_bounded_parallel(
        pending,
        worker,
        limit_key=lambda _row: "judge",
        limits={"judge": config.JUDGE_WORKERS},
        pause_s=config.REQUEST_PAUSE_S,
        on_success=on_success,
        on_error=on_error,
    )

    print(
        f"\nFertig: {judged + skipped}/{total} bewertet "
        f"({judged} neu, {skipped} übersprungen, {errors} Fehler)"
    )


if __name__ == "__main__":
    main()
