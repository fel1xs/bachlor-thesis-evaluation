"""API-Clients für Config A (Agent), B (RAG), C+ (Websuche) und Judge."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import quote

import requests
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

import config
from lib.http_ssl import make_httpx_client, requests_verify
from lib.io_utils import log_error
from lib.openrouter_params import openrouter_generation_extra
from lib.prompts import C_PLUS_SYSTEM_PROMPT
from lib.response_sanitize import normalize_message_content, sanitize_c_plus_answer


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, requests.HTTPError):
        status = exc.response.status_code if exc.response is not None else 0
        return status in (429, 500, 502, 503, 504)
    return isinstance(exc, (requests.Timeout, requests.ConnectionError))


def _retryable_call(func, *args, **kwargs):
    @retry(
        retry=retry_if_exception(_is_retryable),
        stop=stop_after_attempt(config.MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        reraise=True,
    )
    def _wrapped():
        return func(*args, **kwargs)

    return _wrapped()


def _extract_web_citations(message: dict[str, Any]) -> list[str]:
    citations: list[str] = []
    for annotation in message.get("annotations") or []:
        if not isinstance(annotation, dict):
            continue
        if annotation.get("type") == "url_citation":
            url = annotation.get("url")
            if url:
                citations.append(url)
            continue
        url_citation = annotation.get("url_citation")
        if isinstance(url_citation, dict):
            url = url_citation.get("url")
            if url:
                citations.append(url)
    # Dedupe, Reihenfolge behalten
    seen: set[str] = set()
    unique: list[str] = []
    for url in citations:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def call_config_a(frage: str) -> tuple[str, dict[str, Any]]:
    """Config A: synchroner n8n-Webhook (GET)."""
    if not config.AGENT_WEBHOOK_URL:
        raise ValueError("AGENT_WEBHOOK_URL ist nicht gesetzt")

    # n8n erwartet JSON-encodierten String als Query-Parameter (siehe Spec-Beispiel)
    encoded_input = quote(json.dumps(frage, ensure_ascii=False))
    url = f"{config.AGENT_WEBHOOK_URL}?{config.AGENT_REQUEST_FIELD}={encoded_input}"

    def _request() -> requests.Response:
        resp = requests.get(
            url,
            timeout=config.AGENT_TIMEOUT_S,
            verify=requests_verify(),
        )
        if resp.status_code in (429, 500, 502, 503, 504):
            resp.raise_for_status()
        resp.raise_for_status()
        return resp

    response = _retryable_call(_request)
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError(f"Unerwartete Agent-Antwort (kein JSON-Objekt): {payload!r}")

    answer = payload.get(config.AGENT_RESPONSE_FIELD)
    if answer is None:
        raise ValueError(
            f"Feld '{config.AGENT_RESPONSE_FIELD}' fehlt in Agent-Antwort: {payload!r}"
        )

    meta: dict[str, Any] = {"web_citations": [], "error": None, "raw_keys": list(payload.keys())}
    return str(answer), meta


def call_config_b(frage: str) -> tuple[str, dict[str, Any]]:
    """Config B: klassisches Vektor-RAG (LlamaIndex, neutrale Defaults)."""
    from lib.rag_setup import query_rag

    answer = query_rag(frage)
    meta: dict[str, Any] = {
        "web_citations": [],
        "error": None,
        "rag_top_k": config.RAG_SIMILARITY_TOP_K,
        "embedding_model": config.EMBEDDING_MODEL,
        "reasoning_effort": config.OPENROUTER_REASONING_EFFORT,
        "reasoning_exclude": config.OPENROUTER_REASONING_EXCLUDE,
    }
    return answer, meta


def call_config_c_plus(frage: str) -> tuple[str, dict[str, Any]]:
    """Config C+: generisches Modell mit nativer Websuche über OpenRouter."""
    if not config.OPENAI_API_KEY_C:
        raise ValueError("OPENAI_API_KEY_C ist nicht gesetzt (Config C+)")

    payload = {
        "model": config.GENERATION_MODEL,
        "messages": [
            {"role": "system", "content": C_PLUS_SYSTEM_PROMPT},
            {"role": "user", "content": frage},
        ],
        "tools": [
            {
                "type": "openrouter:web_search",
                "parameters": {
                    "engine": config.WEB_SEARCH_ENGINE,
                    "search_context_size": config.WEB_SEARCH_CONTEXT_SIZE,
                },
            }
        ],
        "temperature": config.GENERATION_TEMPERATURE,
        **openrouter_generation_extra(),
    }

    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY_C}",
        "Content-Type": "application/json",
    }

    def _request() -> dict[str, Any]:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=180,
            verify=requests_verify(),
        )
        if resp.status_code in (429, 500, 502, 503, 504):
            resp.raise_for_status()
        resp.raise_for_status()
        return resp.json()

    data = _retryable_call(_request)
    choices = data.get("choices") or []
    if not choices:
        raise ValueError(f"OpenRouter-Antwort ohne choices: {data!r}")

    message = choices[0].get("message") or {}
    content = normalize_message_content(message.get("content"))
    if not content.strip():
        raise ValueError(f"OpenRouter-Antwort ohne message.content: {data!r}")

    cleaned, sanitized = sanitize_c_plus_answer(content)
    if not cleaned.strip():
        raise ValueError(
            f"C+-Antwort nach Bereinigung leer (Rohlänge {len(content)}): {content[:500]!r}"
        )

    citations = _extract_web_citations(message)
    meta: dict[str, Any] = {
        "web_citations": citations,
        "error": None,
        "web_search_engine": config.WEB_SEARCH_ENGINE,
        "web_search_requests": (data.get("usage") or {}).get("server_tool_use", {}).get(
            "web_search_requests"
        ),
        "content_sanitized": sanitized,
        "reasoning_effort": config.OPENROUTER_REASONING_EFFORT,
        "reasoning_exclude": config.OPENROUTER_REASONING_EXCLUDE,
    }
    return cleaned, meta


JUDGE_SYSTEM_PROMPT = """Du bist ein strenger, neutraler Prüfer. Du bewertest die Antwort eines Systems auf eine
Anfrage an die Hochschulverwaltung ausschließlich anhand einer offiziellen Musterlösung.

Die Musterlösung ist eine Checkliste aus Stichpunkten (jeweils eine Zeile mit "- "):
- Normale Punkte sind PFLICHTPUNKTE. Sie müssen inhaltlich abgedeckt sein.
- Mit "(optional)" markierte Punkte sind ZUSATZINFO. Ihr Fehlen ist KEIN Mangel; ihr korrektes
  Vorhandensein ist KEIN Fehler. Nur ein WIDERSPRUCH zu einem optionalen Punkt zählt gegen die Korrektheit.

Dir wird der ITEM-TYP der Frage genannt:
- "beantwortbar": Die Frage lässt sich inhaltlich beantworten; die korrekte Antwort ist eine Sachaussage.
- "verweis": Die korrekte Antwort besteht darin, an die zuständige Stelle zu verweisen (die Musterlösung
  IST selbst ein solcher Verweis). Hier ist ein korrekter Verweis die richtige Antwort.

Bewerte zwei unabhängige Kriterien.

KORREKTHEIT — genau EINE von DREI Kategorien. Prüfe in dieser Reihenfolge:
1. "falsch" (unsicheres Scheitern): Die Antwort widerspricht der Musterlösung in mindestens einem Punkt
   oder erfindet Fakten. Eine einzige Falschaussage macht die GESAMTE Antwort "falsch" — auch wenn andere
   Teile stimmen. Bei Item-Typ "verweis": ein Verweis an die FALSCHE Stelle oder ein erfundener Sachablauf
   statt des korrekten Verweises ist "falsch".
2. "wahr": Die Antwort trifft eine inhaltliche Aussage, die (mindestens teilweise) mit der Musterlösung
   übereinstimmt, und widerspricht ihr nirgends. Auch eine unvollständige Antwort ist "wahr", solange
   nichts Falsches gesagt wird. Bei Item-Typ "verweis": ein Verweis an die RICHTIGE, in der Musterlösung
   genannte Stelle ist "wahr".
3. "enthaltung" (sicheres Scheitern): Die Antwort trifft keine belastbare Sachaussage zur Frage UND sagt
   zugleich nichts Falsches. Das umfasst zwei Spielarten, die NICHT unterschieden werden:
   (a) sie drückt Unwissen aus ("das weiß ich nicht", "dazu finde ich nichts"), oder
   (b) sie beantwortet die Frage nicht selbst, sondern verweist nur an eine zuständige Stelle
       (z. B. "bitte wenden Sie sich an das Studienbüro").
   WICHTIG:
   - Bei Item-Typ "verweis" ist ein Verweis an die richtige Stelle KEINE Enthaltung, sondern "wahr".
   - Ein bloßes Zusatz-Angebot am Ende einer sonst inhaltlichen, richtigen Antwort ("ich kann deine Frage
     bei Bedarf ans Studienbüro weiterleiten") macht die Antwort NICHT zur Enthaltung; entscheidend ist,
     ob die eigentliche Frage inhaltlich beantwortet wurde.

Beispiele (Item-Typ "beantwortbar", Frage "Wie gebe ich die Bachelorarbeit ab?", Musterlösung "online über AlmaWeb"):
"online über AlmaWeb" -> wahr; "per Post" -> falsch; "Das weiß ich nicht" -> enthaltung;
"Bitte wenden Sie sich an das Studienbüro" -> enthaltung.
Beispiel (Item-Typ "verweis", Musterlösung "an das Studierendensekretariat wenden"):
"Wenden Sie sich an das Studierendensekretariat" -> wahr; "Das erledigt das Studienbüro der Fakultät" -> falsch;
"Das weiß ich nicht" -> enthaltung.

VOLLSTAENDIGKEIT — binär, misst NUR die Abdeckung der PFLICHTPUNKTE:
- "vollstaendig": ALLE Pflichtpunkte der Musterlösung sind sinngemäß (grob) genannt.
- "unvollstaendig": Mindestens ein Pflichtpunkt fehlt.
- Optionale Punkte werden für die Vollständigkeit NIE herangezogen (weder positiv noch negativ).

Regeln:
- Bewerte NUR den Inhalt im Abgleich mit der Musterlösung, sinngemäß (nicht wortwörtlich).
- Ignoriere Länge, Ton, Formulierung, Höflichkeit, Selbstsicherheit.
- Zusätzliche korrekte Informationen sind kein Fehler; zusätzliche FALSCHE Informationen machen "falsch".
- Korrektheit und Vollständigkeit sind unabhängig: Eine "wahre" Antwort kann unvollständig sein.
  "enthaltung" ist praktisch immer "unvollstaendig".

Antworte AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown, im Format:
{"korrektheit": "wahr|falsch|enthaltung", "vollstaendigkeit": "vollstaendig|unvollstaendig", "begruendung": "<1-2 Sätze>"}"""


def call_judge(frage: str, musterloesung: str, answer: str, item_typ: str = "beantwortbar") -> dict[str, str]:
    """Blind-Judge über OpenRouter (keine config_id / kein Generierungsmodell)."""
    if not config.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY ist nicht gesetzt")

    user_prompt = (
        f"ITEM-TYP: {item_typ}\n\n"
        f"ANFRAGE:\n{frage}\n\n"
        f"OFFIZIELLE MUSTERLÖSUNG:\n{musterloesung}\n\n"
        f"ZU BEWERTENDE ANTWORT:\n{answer}"
    )

    payload = {
        "model": config.JUDGE_MODEL,
        "messages": [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": config.JUDGE_TEMPERATURE,
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    def _request() -> dict[str, Any]:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
            verify=requests_verify(),
        )
        if resp.status_code in (429, 500, 502, 503, 504):
            resp.raise_for_status()
        resp.raise_for_status()
        return resp.json()

    data = _retryable_call(_request)
    content = ((data.get("choices") or [{}])[0].get("message") or {}).get("content")
    if not content:
        raise ValueError(f"Judge-Antwort ohne content: {data!r}")

    parsed = json.loads(content)
    for field in ("korrektheit", "vollstaendigkeit", "begruendung"):
        if field not in parsed:
            raise ValueError(f"Judge-JSON fehlt Feld '{field}': {parsed!r}")

    return {
        "korrektheit": str(parsed["korrektheit"]),
        "vollstaendigkeit": str(parsed["vollstaendigkeit"]),
        "begruendung": str(parsed["begruendung"]),
    }


def generate_answer(config_id: str, frage: str) -> tuple[str, dict[str, Any]]:
    if config_id == "A":
        return call_config_a(frage)
    if config_id == "B":
        return call_config_b(frage)
    if config_id == "C+":
        return call_config_c_plus(frage)
    raise ValueError(f"Unbekannte config_id: {config_id}")


def measure_latency_ms(func, *args, **kwargs) -> tuple[Any, int]:
    start = time.perf_counter()
    result = func(*args, **kwargs)
    latency_ms = int((time.perf_counter() - start) * 1000)
    return result, latency_ms
