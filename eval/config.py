"""Zentrale Konfiguration für das Evaluation-Tool."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

EVAL_ROOT = Path(__file__).resolve().parent
load_dotenv(EVAL_ROOT / ".env", override=True)


def _env_bool(val: str | None, default: bool = True) -> bool:
    if val is None:
        return default
    lowered = val.lower()
    if lowered in ("0", "false", "no", "off"):
        return False
    if lowered in ("1", "true", "yes", "on"):
        return True
    return default


# TLS-Verifikation für alle ausgehenden HTTPS-Calls (requests, httpx/OpenAI, …)
# AGENT_VERIFY_SSL ist Legacy-Alias, falls HTTP_VERIFY_SSL nicht gesetzt ist.
_http_verify_raw = os.getenv("HTTP_VERIFY_SSL")
if _http_verify_raw is None:
    _http_verify_raw = os.getenv("AGENT_VERIFY_SSL")
HTTP_VERIFY_SSL = _env_bool(_http_verify_raw, True) if _http_verify_raw is not None else True

from lib.http_ssl import apply_ssl_env  # noqa: E402

apply_ssl_env()

# Pfade
DATA_DIR = EVAL_ROOT / "data"
DOCS_DIR = EVAL_ROOT / "docs"
RAG_INDEX_DIR = EVAL_ROOT / "rag_index"
RAG_CHROMA_DIR = EVAL_ROOT / "rag_chroma"
OUT_DIR = EVAL_ROOT / "out"

QUESTIONS_CSV = DATA_DIR / "questions.csv"
RAW_RESPONSES_JSONL = OUT_DIR / "raw_responses.jsonl"
JUDGED_RESULTS_JSONL = OUT_DIR / "judged_results.jsonl"
ERRORS_LOG = OUT_DIR / "errors.log"
SUMMARY_MD = OUT_DIR / "summary.md"
SUMMARY_CSV = OUT_DIR / "summary.csv"
CHARTS_DIR = OUT_DIR / "charts"
SUMMARY_CHART_OVERVIEW = CHARTS_DIR / "summary_overview.png"
MANUAL_SAMPLE_CSV = OUT_DIR / "manual_sample.csv"
MANUAL_KEY_CSV = OUT_DIR / "manual_key.csv"

# API-Keys & Endpoints (OpenRouter getrennt pro Config für Verbrauchstracking)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")  # Judge
OPENROUTER_API_KEY_B = os.getenv("OPENROUTER_API_KEY_B", "")  # Config B: RAG-LLM
OPENROUTER_API_KEY_C = os.getenv("OPENROUTER_API_KEY_C", "")  # Config C+: Websuche
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Config B: Embeddings (direkt OpenAI)
AGENT_WEBHOOK_URL = os.getenv(
    "AGENT_WEBHOOK_URL", "https://n8n-1.salzer-siegel.de/webhook/wifassist"
)
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "anthropic/claude-sonnet-5")

# Modelle
GENERATION_MODEL = "openai/gpt-5.2"
# OpenRouter: Reasoning für gpt-5.x explizit aus (none) — siehe lib/openrouter_params.py
OPENROUTER_REASONING_EFFORT = os.getenv("OPENROUTER_REASONING_EFFORT", "none")
OPENROUTER_REASONING_EXCLUDE = _env_bool(os.getenv("OPENROUTER_REASONING_EXCLUDE", "true"), True)

# Konfigurationen
CONFIG_IDS = ("A", "B", "C+")

# Config A — n8n-Agent (GET-Webhook)
AGENT_REQUEST_FIELD = os.getenv("AGENT_REQUEST_FIELD", "input")
AGENT_RESPONSE_FIELD = os.getenv("AGENT_RESPONSE_FIELD", "output")
AGENT_TIMEOUT_S = int(os.getenv("AGENT_TIMEOUT_S", "180"))
AGENT_VERIFY_SSL = HTTP_VERIFY_SSL

# Config B — RAG (LlamaIndex, neutrale Defaults)
RAG_SIMILARITY_TOP_K = int(os.getenv("RAG_SIMILARITY_TOP_K", "5"))
RAG_RESPONSE_MODE = os.getenv("RAG_RESPONSE_MODE", "compact")
RAG_QUERY_TIMEOUT_S = int(os.getenv("RAG_QUERY_TIMEOUT_S", "180"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")

# Config C+ — Websuche (OpenRouter Server Tool, native Engine ≈ Spec-Plugin)
WEB_SEARCH_ENGINE = os.getenv("WEB_SEARCH_ENGINE", "native")
WEB_SEARCH_CONTEXT_SIZE = os.getenv("WEB_SEARCH_CONTEXT_SIZE", "medium")

# Laufzeit
GENERATION_TEMPERATURE = 0.0
JUDGE_TEMPERATURE = 0.0
REQUEST_PAUSE_S = float(os.getenv("REQUEST_PAUSE_S", "1.0"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

# Parallele Ausführung (ThreadPool, I/O-bound). Limits gelten pro Config bzw. Judge.
GENERATION_WORKERS: dict[str, int] = {
    "A": int(os.getenv("GEN_WORKERS_A", "2")),       # n8n-Webhook
    "B": min(2, int(os.getenv("GEN_WORKERS_B", "2"))),  # RAG: max. 2 parallel
    "C+": int(os.getenv("GEN_WORKERS_CPLUS", "6")),  # OpenRouter + Websuche
}
JUDGE_WORKERS = int(os.getenv("JUDGE_WORKERS", "6"))

# CSV-Spalten (questions.csv)
CSV_COL_ID = "id"
CSV_COL_FRAGE = "frage"
CSV_COL_MUSTERLOESUNG = "antwort"
CSV_COL_ITEM_TYP = "item_typ"

# Manuelle Stichprobe
MANUAL_SAMPLE_SIZE = 18
MANUAL_SAMPLE_PER_CONFIG = 6
MANUAL_SAMPLE_SEED = 42

# Score-Mapping für Aggregation
# Korrektheit hat vier Kategorien: wahr/falsch liegen auf der Wahrheitsachse und gehen in
# den korrektheit_score ein; keine_aussage/eskalation sind KEINE Wahr/Falsch-Aussage und
# werden aus dem Score ausgeschlossen (separat als Quote ausgewiesen).
KORREKTHEIT_SCORES = {"wahr": 1.0, "falsch": 0.0}
KORREKTHEIT_KATEGORIEN = ("wahr", "falsch", "enthaltung")
# Vollständigkeit ist binär: alle Pflichtpunkte abgedeckt -> vollstaendig, sonst unvollstaendig.
VOLLSTAENDIGKEIT_SCORES = {
    "vollstaendig": 1.0,
    "unvollstaendig": 0.0,
}
