# Evaluation-Tool: Agent vs. RAG vs. Websuche

Vergleich von drei Architekturen auf denselben Hochschulverwaltungs-Anfragen, bewertet durch einen blinden LLM-Judge gegen offizielle Musterlösungen.

| Config | Beschreibung |
| --- | --- |
| **A** | Agentisches System (n8n-Webhook, synchron) |
| **B** | Klassisches Vektor-RAG (LlamaIndex, neutrale Defaults) |
| **C+** | Generisches Modell + native Websuche (OpenRouter) |

Generierungsmodell für A/B/C+: `openai/gpt-5.2` · Judge: separates Modell (≠ GPT-5.2)

## Setup

```bash
cd eval
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # Keys eintragen
```

1. `data/questions.csv` — 61 Fragen mit Musterlösungen (bereits kopiert aus `../data/input.csv`)
2. `docs/` — dieselben Rohdokumente wie für Config A ablegen (siehe `docs/README.md`)

## Drei Stages (strikt getrennt, jeweils resume-fähig)

```bash
# Stage 1: Rohantworten (Test mit 3 Fragen)
python stage1_generate.py --limit 3

# Stage 2: Judge
python stage2_judge.py --limit 9

# Stage 3: Aggregation + blinde Stichprobe
python stage3_aggregate.py
```

Volllauf (61 Fragen × 3 Configs = 183 Antworten):

```bash
python stage1_generate.py
python stage2_judge.py
python stage3_aggregate.py
```

Einzelne Configs testen:

```bash
python stage1_generate.py --limit 2 --configs C+
```

## Ausgaben (`out/`)

| Datei | Inhalt |
| --- | --- |
| `raw_responses.jsonl` | Rohantworten inkl. Latenz, Modell, `run_ts` |
| `judged_results.jsonl` | Judge-Bewertungen (blind) |
| `summary.md` / `summary.csv` | Aggregierte Kennzahlen |
| `charts/summary_overview.png` | Visualisierung der Kennzahlen |
| `manual_sample.csv` | 18 zufällige Fälle (6 je Config, blind) |
| `manual_key.csv` | Mapping sample_id → config_id |
| `errors.log` | Fehlerprotokoll |

Nach manuellem Ausfüllen von `human_korrektheit` / `human_vollstaendigkeit` in `manual_sample.csv`:

```bash
python stage3_aggregate.py --compare-human
```

## Hinweise

- **Config C+** nutzt das aktuelle OpenRouter Server Tool `openrouter:web_search` (Nachfolger des deprecated `plugins: [{id: "web"}]`); Engine `native` entspricht der Spec-Absicht.
- **Config B** Embeddings direkt über OpenAI; kein NLTK nötig (`TokenTextSplitter`); Index: `python build_rag_index.py --rebuild` (Vektoren in `rag_chroma/`, nicht mehr als riesige JSON)
- **Config A** Timeout 180 s; bei SSL-Fehler: `AGENT_VERIFY_SSL=false` in `.env`
- Alle Stages schreiben inkrementell (append) — Abbrüche sind resume-fähig
- **Parallelität:** Stage 1/2 laufen Aufgaben parallel (ThreadPool).
  Limits pro Config: `GEN_WORKERS_A=2` (n8n), `GEN_WORKERS_B=2` (RAG, max. 2), `GEN_WORKERS_CPLUS=6`,
  `JUDGE_WORKERS=6` — in `.env` anpassbar.
