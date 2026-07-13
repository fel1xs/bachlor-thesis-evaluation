# agent.md — Handbuch für Coding-Agents

Dieses Dokument beschreibt das Evaluation-Tool in `eval/`: Ziel, Architektur, Dateien, Guardrails und typische Arbeitsabläufe. Sprache der Evaluationsinhalte (Fragen, Antworten, Musterlösungen, Judge): **Deutsch**. Code und Kommentare: beliebig.

---

## 1. Ziel des Projekts

Vergleich der Antwortqualität von **drei Architekturen** auf denselben realen Hochschulverwaltungs-Anfragen der Wirtschaftswissenschaftlichen Fakultät (Uni Leipzig), bewertet durch einen **LLM-as-a-Judge** gegen offizielle Musterlösungen.

**Ein Generierungsmodell für alle drei Configs:** `openai/gpt-5.2` (über OpenRouter bzw. n8n).  
**Einzige Variable:** die Architektur.

| ID | Konfiguration | Aufruf | Besonderheit |
| --- | --- | --- | --- |
| **A** | Agentisches System | n8n-Webhook, synchron (GET) | PageIndex-Navigation, mehrstufig, Tools |
| **B** | Klassisches Vektor-RAG | lokal (LlamaIndex) | dieselben Dokumente wie A, Single-Shot Top-k |
| **C+** | Generisch + Websuche | OpenRouter API | native Websuche, kein fakultätsspezifisches Wissen |

**Datenumfang:** 61 Fragen × 3 Configs = **183 Antworten** → Judge → Aggregation.

---

## 2. Architektur: drei strikt getrennte Stages

Jede Stage ist ein **eigenes Script**, schreibt **inkrementell auf Platte** (append) und ist **resume-fähig**. Teure Agent-Calls dürfen nicht neu laufen, wenn nur Judge oder Aggregation geändert wird.

```
Stage 1  stage1_generate.py   →  out/raw_responses.jsonl
Stage 2  stage2_judge.py      →  out/judged_results.jsonl
Stage 3  stage3_aggregate.py  →  out/summary.md, summary.csv, manual_sample.csv, manual_key.csv
```

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│ questions   │────▶│ Stage 1      │────▶│ raw_responses   │
│ .csv        │     │ clients A/B/C+│     │ .jsonl          │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                     ┌──────────────┐               │
                     │ Stage 2      │◀──────────────┘
                     │ Judge (blind)│
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐     ┌─────────────────┐
                     │ judged_      │────▶│ Stage 3         │
                     │ results.jsonl│     │ Aggregation     │
                     └──────────────┘     └─────────────────┘
```

**Regel für Agents:** Stages nicht zusammenlegen. Kein „All-in-one“-Script bauen, außer der Nutzer verlangt es ausdrücklich.

---

## 3. Dateistruktur

```
eval/
  .env                     # Secrets (NICHT committen)
  .env.example             # Vorlage ohne echte Keys
  config.py                # zentrale Konfiguration
  requirements.txt         # gepinnte Versionen
  README.md                # Kurzanleitung für Menschen
  data/
    questions.csv          # id, frage, antwort (Musterlösung)
  docs/                    # Rohdokumente für Config B (wie Agent A)
  rag_index/               # Docstore/Metadaten (generiert, gitignored)
  rag_chroma/              # Chroma-Vektoren (generiert, gitignored; ersetzt riesige vector_store.json)
  stage1_generate.py
  stage2_judge.py
  stage3_aggregate.py
  lib/
    clients.py             # Aufrufe A / B / C+ / Judge
    io_utils.py            # JSONL, Resume, CSV
  out/                     # Laufzeit-Artefakte (gitignored)
    raw_responses.jsonl
    judged_results.jsonl
    errors.log
    summary.md
    summary.csv
    manual_sample.csv
    manual_key.csv
```

**Repo-Root:**

```
data/input.csv             # Quelle der Fragen (Kopie liegt in eval/data/questions.csv)
agent.md                   # dieses Dokument
README.md                  # Verweis auf eval/
```

---

## 4. Environment (`.env`)

Pflichtvariablen in `eval/.env`:

| Variable | Zweck |
| --- | --- |
| `OPENROUTER_API_KEY` | Generierung B/C+, Judge, LLM für B |
| `OPENAI_API_KEY` | **Nur Embeddings** für Config B (`text-embedding-3-large`) |
| `AGENT_WEBHOOK_URL` | n8n-Webhook für Config A |
| `JUDGE_MODEL` | z. B. `anthropic/claude-sonnet-5` (≠ GPT-5.2) |

Optionale Overrides: `AGENT_REQUEST_FIELD`, `AGENT_RESPONSE_FIELD`, `AGENT_TIMEOUT_S`, `REQUEST_PAUSE_S`, `RAG_SIMILARITY_TOP_K`, `WEB_SEARCH_ENGINE`, `WEB_SEARCH_CONTEXT_SIZE`.

**Niemals** `.env` oder API-Keys committen.

---

## 5. Konfigurations-Details (Implementierung in `lib/clients.py`)

### Config A — Agent (n8n)

- **GET** an `AGENT_WEBHOOK_URL`
- Query-Parameter `input` = JSON-encodierter String der Frage (z. B. `?input=%22hi%22`)
- Antwortfeld: `output` (konfigurierbar via `AGENT_RESPONSE_FIELD`)
- Timeout: 180 s
- Latenz: Wall-Clock um den Request
- Determinismus wird **in n8n** gesteuert, nicht von außen

### Config B — Vektor-RAG (LlamaIndex + Chroma)

- LLM: `OpenAILike` → OpenRouter, Modell `openai/gpt-5.2`, `temperature=0`
- Embeddings: `OpenAIEmbedding` → **direkt OpenAI** (OpenRouter proxyt Embeddings i.d.R. nicht)
- Index: Vektoren in `rag_chroma/`, Metadaten in `rag_index/` (kein riesiges `default__vector_store.json`)
- Rebuild: `python build_rag_index.py --rebuild`
- Query Engine: `similarity_top_k=5`, `response_mode="compact"` — neutrale Defaults
- **System-Prompt:** Spiegel von Config A (`lib/prompts.py`) — gleiche Rolle, Quellenpflicht, Ton; statt Tools nur `{context_str}` aus RAG

### Config C+ — Websuche (OpenRouter)

- Chat Completions mit Server Tool `openrouter:web_search`
- **System-Prompt:** generisch wie ChatGPT (`lib/prompts.py`) — kein Fakultätswissen, keine Quellenpflicht
- Parameter: `engine=native`, `search_context_size=medium`

### Judge

- OpenRouter, `temperature=0`, `response_format: json_object`
- **Blind:** keine `config_id`, kein Generierungsmodell im Prompt
- Nur Frage, Musterlösung, zu bewertende Antwort
- Anti-Bias: Länge, Ton, Selbstsicherheit ignorieren

---

## 6. Datenschemas

### Input: `eval/data/questions.csv`

| Spalte | Verwendung |
| --- | --- |
| `id` | `question_id` (z. B. F01) |
| `frage` | Anfrage an alle Configs |
| `antwort` | Musterlösung für Judge (Stichpunkt-Checkliste) |

Die Musterlösung (`antwort`) ist eine knappe Stichpunktliste (je Zeile `- `):

- Normale Punkte = **Pflichtpunkte**; sie müssen abgedeckt sein und zählen für die Vollständigkeit.
- Mit `- (optional) ` markierte Punkte = korrekte, aber nicht erfragte **Zusatzinfo**; ihr Fehlen senkt die Vollständigkeit nicht, ihr korrektes Vorhandensein ist kein Fehler (nur ein Widerspruch zählt gegen die Korrektheit).

Aufbau/Herkunft: `data/build_stichpunkte.py` erzeugt `antwort` faktentreu aus dem Original-Backup; Begründungen je Zeile in `data/input_stichpunkte_changelog.md`.

Encoding: **UTF-8 mit BOM** (`utf-8-sig` beim Lesen).

### `out/raw_responses.jsonl` (eine Zeile pro Antwort)

```json
{
  "question_id": "F01",
  "config_id": "A",
  "answer": "Text der Antwort ...",
  "latency_ms": 4213,
  "model": "openai/gpt-5.2",
  "run_ts": "2026-07-03T14:22:01Z",
  "meta": {"web_citations": [], "error": null}
}
```

Bei Fehlern: `answer` leer, `meta.error` gesetzt; Stage 1 crasht **nicht**.

### `out/judged_results.jsonl`

```json
{
  "question_id": "F01",
  "config_id": "A",
  "korrektheit": "wahr",
  "vollstaendigkeit": "vollstaendig",
  "begruendung": "Deckt Frist und Verfahren korrekt ab.",
  "judge_model": "anthropic/claude-sonnet-5",
  "judge_ts": "2026-07-03T15:01:44Z"
}
```

**Korrektheit** (4-kategorial):

- `wahr`: trifft eine Aussage, die (mind. teilweise) der Musterlösung entspricht und ihr nicht widerspricht.
- `falsch`: widerspricht der Musterlösung oder erfindet Fakten (eine Falschaussage genügt).
- `eskalation`: beantwortet die Frage nicht, sondern verweist nur an eine zuständige Stelle (außer die Musterlösung ist selbst ein solcher Verweis → dann `wahr`).
- `keine_aussage`: trifft keine Aussage / drückt Unwissen aus ("weiß ich nicht", "finde nichts dazu").

**Vollständigkeit:** `vollstaendig` | `unvollstaendig` (binär: alle Pflichtpunkte abgedeckt oder nicht; optionale Punkte zählen nicht)

---

## 7. Stage-Skripte und CLI

Alle Scripts aus `eval/` mit aktiviertem venv ausführen:

```bash
cd eval
.venv\Scripts\activate    # Windows
```

### Stage 1 — `stage1_generate.py`

```bash
python stage1_generate.py                    # Volllauf
python stage1_generate.py --limit 3          # Kostentest
python stage1_generate.py --configs C+ A    # nur bestimmte Configs
```

- Resume: `(question_id, config_id)` bereits in `raw_responses.jsonl` → überspringen
- Retries: tenacity, exponential backoff, 429/5xx
- Pause zwischen Calls: `REQUEST_PAUSE_S` (default 1 s)

### Stage 2 — `stage2_judge.py`

```bash
python stage2_judge.py
python stage2_judge.py --limit 9
```

- Resume analog Stage 1
- Parse-Fehler: 1 Retry, sonst `errors.log`
- Generierungsfehler (`meta.error`): automatisch als falsch/unvollständig bewertet

> **Re-Judge nach Änderung der Musterlösung.** Stage 1 (`raw_responses.jsonl`) bleibt
> gültig — die Modellantworten hängen nicht von der Musterlösung ab. Für neue Scores muss
> aber `out/judged_results.jsonl` **geleert** werden (Stage 2 überspringt sonst per Resume
> alle vorhandenen `(question_id, config_id)`-Paare), danach Stage 2 + Stage 3 neu laufen.
> Das verursacht Judge-API-Kosten und wird **nicht** automatisch gestartet.
>
> ```bash
> del out\judged_results.jsonl   # Windows (bzw. rm unter Unix)
> python stage2_judge.py
> python stage3_aggregate.py
> ```

### Stage 3 — `stage3_aggregate.py`

```bash
python stage3_aggregate.py                   # Aggregation + Stichprobe
python stage3_aggregate.py --skip-sample     # ohne neue Stichprobe
python stage3_aggregate.py --compare-human   # nach manuellem Ausfüllen
```

**Headline-Scores** (in `summary.csv`):

- Korrektheit → **Wahr-Score** = Anteil `wahr` unter den echten Aussagen (`wahr`+`falsch`); `keine_aussage`/`eskalation` sind ausgeschlossen und werden als eigene Quoten ausgewiesen
- Vollständigkeit (binär): vollstaendig=1, unvollstaendig=0
- Median-Latenz je Config aus `raw_responses.jsonl`

**Manuelle Stichprobe:** 18 Fälle, 6 je Config, seed=42.  
`manual_sample.csv` ist **blind** (keine `config_id`). Mapping in `manual_key.csv`.
Die Spalten `human_korrektheit` / `human_vollstaendigkeit` werden manuell in der CSV ausgefüllt.

---

## 8. Guardrails (nicht verhandelbar)

| Regel | Begründung |
| --- | --- |
| Kein externer Vektor-DB-Server | LlamaIndex `VectorStoreIndex` + Persist reicht |
| RAG nicht absichtlich schwächen | Solides Embedding, neutrales Chunking |
| Judge blind | Keine `config_id`, kein Modellname an Judge |
| Judge-Modell ≠ GPT-5.2 | Self-Enhancement-Bias vermeiden |
| Inkrementell schreiben (append) | Abbrüche dürfen Fortschritt nicht vernichten |
| Resume überall | `(question_id, config_id)` als Schlüssel |
| `temperature: 0` für B und Judge | Reproduzierbarkeit |
| Modellversionen + Timestamps loggen | BA-Anhang / Nachvollziehbarkeit |
| `requirements.txt` gepinnt | Reproduzierbare Läufe |

**Config C+** ist wegen Websuche nicht voll deterministisch — dokumentieren, nicht „fixen“.

---

## 9. Typische Aufgaben für Agents

### Neuer Volllauf

1. `eval/docs/` mit Wissensbasis füllen (falls B noch nicht gelaufen)
2. Optional: `eval/out/` leeren (nur wenn bewusst neu starten)
3. `stage1_generate.py` → `stage2_judge.py` → `stage3_aggregate.py`

### Judge-Prompt ändern

- Nur `JUDGE_SYSTEM_PROMPT` in `lib/clients.py` und/oder Stage-2-Logik anpassen
- `judged_results.jsonl` löschen oder gezielt Zeilen entfernen
- **Nicht** Stage 1 neu laufen lassen

### Nur eine Config nachholen

```bash
python stage1_generate.py --configs B
```

Resume überspringt bereits vorhandene Paare.

### RAG-Index neu bauen

```bash
cd eval
python build_rag_index.py --rebuild
```

Dauert bei ~730 Docs ca. 10–15 Min (Embeddings über OpenAI).

### Kostenprobe vor Volllauf

```bash
python stage1_generate.py --limit 3
python stage2_judge.py --limit 9
```

---

## 10. Bekannte Limitationen

- **Config A:** Determinismus nur in n8n; Timeout bis 180 s pro Anfrage
- **Config A SSL:** `HTTP_VERIFY_SSL=false` in `.env` bei Zertifikatsproblemen (gilt auch für OpenAI-Embeddings und OpenRouter)
- **Config B:** Braucht identische Dokumente wie Agent A in `eval/docs/`; Embeddings kosten OpenAI-Credits
- **Config B Chunking:** `TokenTextSplitter` (512/20) statt NLTK-SentenceSplitter — kein NLTK-Download nötig
- **Config C+:** Websuche variiert; Zitate in `meta.web_citations` können leer sein
- **Fragenanzahl:** 61 (ein Item je Basisfrage 1–60, Frage 2 als 2a/2b); Stand 2026-07-11, siehe data/input_finalset_changelog_2026-07-11.md

## 11. Fehlerbehebung

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `Resource 'stopwords' not found` (NLTK) | Alter LlamaIndex-Default | Behoben via `TokenTextSplitter` in `lib/rag_setup.py`; ggf. `rag_index/` löschen und neu bauen |
| `SSL: CERTIFICATE_VERIFY_FAILED` (n8n/OpenAI/OpenRouter) | Fehlende CA / self-signed | `HTTP_VERIFY_SSL=false` in `eval/.env` (gilt für alle HTTPS-Calls) |
| RAG-Index baut bei jeder Frage neu | Index fehlte | `python build_rag_index.py` einmal vor Stage 1; Stage 1 baut jetzt auch upfront |
| `F01/B` in `raw_responses.jsonl` mit `meta.error` | Fehlgeschlagener Lauf | Zeile löschen oder Datei leeren, dann erneut `--configs B` |
| Config B hängt / keine B-Antworten | Alter `default__vector_store.json` (~2 GB) blockiert beim Laden | `python build_rag_index.py --rebuild`, dann nur Config B generieren |

---

## 12. Was Agents vermeiden sollen

- Secrets in Code oder Commits
- Stages zu einem Script fusionieren
- Judge mit `config_id` oder Generierungsmodell füttern
- RAG absichtlich mit schlechten Parametern konfigurieren
- `out/` oder `rag_index/` committen
- Volllauf ohne vorherigen `--limit`-Test starten (Kosten)

---

## 13. Abhängigkeiten

Siehe `eval/requirements.txt`. Virtuelle Umgebung liegt in `eval/.venv/` (gitignored).

Hauptpakete: `python-dotenv`, `requests`, `tenacity`, `llama-index`, `llama-index-llms-openai-like`, `llama-index-embeddings-openai`.

---

## 14. Verweise

- Menschliche Kurzanleitung: `eval/README.md`
- Wissensbasis-Hinweis: `eval/docs/README.md`
- Zentrale Konfiguration: `eval/config.py`
- API-Clients: `eval/lib/clients.py`
