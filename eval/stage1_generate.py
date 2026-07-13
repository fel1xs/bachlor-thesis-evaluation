"""Stage 1: Antworten für alle (Frage × Konfiguration) erzeugen."""

from __future__ import annotations

import argparse
import sys
import threading
from pathlib import Path
from typing import Any

# eval/ als Import-Root
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from lib.clients import generate_answer, measure_latency_ms
from lib.io_utils import append_jsonl, load_completed_keys, load_questions, log_error, utc_now_iso
from lib.parallel import run_bounded_parallel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage 1: Rohantworten generieren")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Nur die ersten N Fragen verarbeiten (für Testläufe)",
    )
    parser.add_argument(
        "--configs",
        nargs="+",
        default=list(config.CONFIG_IDS),
        choices=list(config.CONFIG_IDS),
        help="Welche Konfigurationen laufen sollen",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    questions = load_questions()
    if args.limit is not None:
        questions = questions[: args.limit]

    completed = load_completed_keys(config.RAW_RESPONSES_JSONL)
    total = len(questions) * len(args.configs)
    skipped = sum(
        1
        for q in questions
        for cid in args.configs
        if (q["question_id"], cid) in completed
    )

    print(
        f"Stage 1: {len(questions)} Fragen × {len(args.configs)} Configs "
        f"= {total} geplante Antworten"
    )
    workers = ", ".join(f"{c}={config.GENERATION_WORKERS[c]}" for c in args.configs)
    print(f"Parallelität: {workers}")

    if "B" in args.configs:
        from lib.rag_setup import ensure_rag_index

        try:
            ensure_rag_index()
        except Exception as exc:  # noqa: BLE001
            msg = f"Stage1 RAG-Index: {type(exc).__name__}: {exc}"
            log_error(msg)
            print(f"FEHLER beim RAG-Index: {exc}")
            print("Config B wird für diesen Lauf übersprungen.")
            args.configs = [c for c in args.configs if c != "B"]
            total = len(questions) * len(args.configs)
            skipped = sum(
                1
                for q in questions
                for cid in args.configs
                if (q["question_id"], cid) in completed
            )

    pending: list[tuple[dict[str, str], str]] = []
    for question in questions:
        qid = question["question_id"]
        for config_id in args.configs:
            if (qid, config_id) not in completed:
                pending.append((question, config_id))

    print_lock = threading.Lock()
    completed_lock = threading.Lock()

    def worker(item: tuple[dict[str, str], str]) -> dict[str, Any]:
        question, config_id = item
        qid = question["question_id"]
        frage = question["frage"]
        try:
            (answer, meta), latency_ms = measure_latency_ms(generate_answer, config_id, frage)
            record = {
                "question_id": qid,
                "config_id": config_id,
                "answer": answer,
                "latency_ms": latency_ms,
                "model": config.GENERATION_MODEL,
                "run_ts": utc_now_iso(),
                "meta": meta,
            }
            append_jsonl(config.RAW_RESPONSES_JSONL, record)
            with print_lock:
                print(f"OK  {qid} / {config_id} ({latency_ms} ms)")
            return record
        except Exception as exc:  # noqa: BLE001
            msg = f"Stage1 {qid}/{config_id}: {type(exc).__name__}: {exc}"
            log_error(msg)
            record = {
                "question_id": qid,
                "config_id": config_id,
                "answer": "",
                "latency_ms": 0,
                "model": config.GENERATION_MODEL,
                "run_ts": utc_now_iso(),
                "meta": {"web_citations": [], "error": str(exc)},
            }
            append_jsonl(config.RAW_RESPONSES_JSONL, record)
            with print_lock:
                print(f"ERR {qid} / {config_id}: {exc}")
            raise

    def on_success(item: tuple[dict[str, str], str], _record: dict[str, Any]) -> None:
        qid, cid = item[0]["question_id"], item[1]
        with completed_lock:
            completed.add((qid, cid))

    def on_error(item: tuple[dict[str, str], str], _exc: Exception) -> None:
        qid, cid = item[0]["question_id"], item[1]
        with completed_lock:
            completed.add((qid, cid))

    limits = {cid: config.GENERATION_WORKERS[cid] for cid in args.configs}
    created, errors = run_bounded_parallel(
        pending,
        worker,
        limit_key=lambda item: item[1],
        limits=limits,
        pause_s=config.REQUEST_PAUSE_S,
        on_success=on_success,
        on_error=on_error,
    )

    print(
        f"\nFertig: {created + skipped}/{total} vorhanden "
        f"({created} neu, {skipped} übersprungen, {errors} Fehler)"
    )


if __name__ == "__main__":
    main()
