"""Bereinigung von Generierungsantworten (v. a. Config C+ / Websuche).

Manche Modelle mischen Tool-Aufrufe, JSON-Queries und interne Kommentare in
message.content. Dieses Modul entfernt solche Artefakte vor der Speicherung.
"""

from __future__ import annotations

import re
from typing import Any

_TOOL_QUERY_JSON = re.compile(
    r'\{["\']query["\']\s*:\s*(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')[^}]*\}',
    re.IGNORECASE,
)

_COMMENTARY_TAG = re.compile(
    r"<commentary\b[^>]*>.*?</commentary>",
    re.IGNORECASE | re.DOTALL,
)

_TOOL_TARGET_FRAGMENT = re.compile(
    r"[^\s]{0,40}to=functions\.openrouter_web_search[^\.\n]*\.?",
    re.IGNORECASE,
)

_LEAK_PHRASES: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"Oops can'?t call without function\.?",
        r"Let'?s do web search\.?",
        r"Let'?s search PDF\.?",
        r"Use web search\.?",
        r"Maybe use function openrouter_web_search\.?",
        r"Let'?s call properly\.?",
        r"Wait tool call must be valid\.?",
        r"Ich suche kurz[^\.{]*(?:\{[^}]*\})?[^\.]*\.?",
    )
)

_ANSWER_START = re.compile(
    r"(?:"
    r"(?:^|[\.\n]\s*)"
    r"(?:"
    r"Ja[,\s–—\-]|Nein[,\s–—\-]|"
    r"Die |Du |Sie |Für |Um |Wenn |Auf |Ob |"
    r"Grundsätzlich |"
    r"## "
    r")"
    r")",
    re.IGNORECASE | re.MULTILINE,
)


def normalize_message_content(content: Any) -> str:
    """OpenRouter content kann String oder Liste von Text-Blöcken sein."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    if content is None:
        return ""
    return str(content)


def sanitize_c_plus_answer(text: str) -> tuple[str, bool]:
    """Entfernt Tool-Leaks aus C+-Antworten. Gibt (bereinigt, geändert) zurück."""
    original = text
    cleaned = text

    cleaned = _COMMENTARY_TAG.sub("", cleaned)
    cleaned = _TOOL_QUERY_JSON.sub("", cleaned)
    cleaned = _TOOL_TARGET_FRAGMENT.sub("", cleaned)
    for pattern in _LEAK_PHRASES:
        cleaned = pattern.sub("", cleaned)

    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    if _looks_like_tool_leak_prefix(cleaned):
        match = _ANSWER_START.search(cleaned)
        if match:
            cleaned = cleaned[match.start() :].lstrip(".\n ")

    cleaned = cleaned.strip()
    return cleaned, cleaned != original.strip()


def _looks_like_tool_leak_prefix(text: str) -> bool:
    """Heuristik: Beginnt der Text noch mit Tool-/Meta-Artefakten?"""
    if not text:
        return False
    head = text[:200].lower()
    markers = (
        '{"query"',
        "openrouter_web_search",
        "use web search",
        "let's search",
        "oops can't",
        "<commentary",
        "to=functions.",
    )
    return any(m in head for m in markers)
