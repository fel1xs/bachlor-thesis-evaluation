"""JSONL-I/O, Resume-Logik und CSV-Hilfen."""

from __future__ import annotations

import csv
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import config

_jsonl_append_lock = threading.Lock()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    ensure_parent(path)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with _jsonl_append_lock:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                log_error(f"Ungültige JSONL-Zeile in {path} (Zeile {line_no}): {exc}")
    return rows


def load_completed_keys(
    path: Path,
    key_fields: tuple[str, ...] = ("question_id", "config_id"),
) -> set[tuple[Any, ...]]:
    return {tuple(row.get(field) for field in key_fields) for row in load_jsonl(path)}


def log_error(message: str) -> None:
    ensure_parent(config.ERRORS_LOG)
    ts = utc_now_iso()
    with config.ERRORS_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{ts}] {message}\n")
    print(f"ERROR: {message}")


def load_questions(csv_path: Path | None = None) -> list[dict[str, str]]:
    path = csv_path or config.QUESTIONS_CSV
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        questions: list[dict[str, str]] = []
        for row in reader:
            question_id = (row.get(config.CSV_COL_ID) or "").strip()
            frage = (row.get(config.CSV_COL_FRAGE) or "").strip()
            musterloesung = (row.get(config.CSV_COL_MUSTERLOESUNG) or "").strip()
            item_typ = (row.get(config.CSV_COL_ITEM_TYP) or "beantwortbar").strip() or "beantwortbar"
            if not question_id or not frage:
                continue
            questions.append(
                {
                    "question_id": question_id,
                    "frage": frage,
                    "musterloesung": musterloesung,
                    "item_typ": item_typ,
                }
            )
        return questions


def write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    ensure_parent(path)
    fields = list(fieldnames)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))
