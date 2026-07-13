"""Stage 3: Ergebnisse aggregieren, Stichprobe exportieren, Judge vs. Mensch."""

from __future__ import annotations

import argparse
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from lib.io_utils import (
    load_jsonl,
    load_questions,
    read_csv,
    write_csv,
)
from lib.summary_plots import build_charts_markdown, render_summary_charts


def _pct(count: int, total: int) -> float:
    return round(100.0 * count / total, 1) if total else 0.0


def _mean_score(values: list[str], mapping: dict[str, float]) -> float:
    scores = [mapping.get(v) for v in values if v in mapping]
    return round(statistics.mean(scores), 3) if scores else 0.0


def _median_latency(latencies: list[int]) -> float:
    return round(statistics.median(latencies), 1) if latencies else 0.0


def aggregate(judged: list[dict[str, Any]], raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raw_by_key = {
        (row.get("question_id"), row.get("config_id")): row for row in raw
    }

    rows: list[dict[str, Any]] = []
    for config_id in config.CONFIG_IDS:
        subset = [r for r in judged if r.get("config_id") == config_id]
        n = len(subset)
        if n == 0:
            continue

        korrektheit_counts = Counter(r.get("korrektheit") for r in subset)
        voll_counts = Counter(r.get("vollstaendigkeit") for r in subset)

        # passend-Rate (Headline-Metrik): Antwort trifft eine Aussage zur Sache,
        # ist korrekt UND vollständig (wahr ∧ vollstaendig). Bestraft — anders als
        # der Wahr-Score — auch Enthaltung und Lücken.
        passend_n = sum(
            1
            for r in subset
            if r.get("korrektheit") == "wahr"
            and r.get("vollstaendigkeit") == "vollstaendig"
        )
        # Abdeckung (Diagnose): Anteil echter Aussagen (nicht enthaltung)
        abdeckung_n = korrektheit_counts.get("wahr", 0) + korrektheit_counts.get("falsch", 0)

        latencies = [
            raw_by_key[(r.get("question_id"), config_id)].get("latency_ms", 0)
            for r in subset
            if (r.get("question_id"), config_id) in raw_by_key
        ]

        row = {
            "config_id": config_id,
            "n": n,
            "passend_n": passend_n,
            "passend_pct": _pct(passend_n, n),
            "abdeckung_n": abdeckung_n,
            "abdeckung_pct": _pct(abdeckung_n, n),
            "wahr_n": korrektheit_counts.get("wahr", 0),
            "wahr_pct": _pct(korrektheit_counts.get("wahr", 0), n),
            "falsch_n": korrektheit_counts.get("falsch", 0),
            "falsch_pct": _pct(korrektheit_counts.get("falsch", 0), n),
            "enthaltung_n": korrektheit_counts.get("enthaltung", 0),
            "enthaltung_pct": _pct(korrektheit_counts.get("enthaltung", 0), n),
            # Score nur über wahr/falsch (enthaltung ist keine Wahrheitsaussage)
            "korrektheit_score": _mean_score(
                [r.get("korrektheit", "") for r in subset], config.KORREKTHEIT_SCORES
            ),
            "vollstaendig_n": voll_counts.get("vollstaendig", 0),
            "vollstaendig_pct": _pct(voll_counts.get("vollstaendig", 0), n),
            "unvollstaendig_n": voll_counts.get("unvollstaendig", 0),
            "unvollstaendig_pct": _pct(voll_counts.get("unvollstaendig", 0), n),
            "vollstaendigkeit_score": _mean_score(
                [r.get("vollstaendigkeit", "") for r in subset], config.VOLLSTAENDIGKEIT_SCORES
            ),
            "latency_median_ms": _median_latency([int(x) for x in latencies if x is not None]),
        }
        rows.append(row)
    return rows


def _float_field(row: dict[str, Any], key: str) -> float:
    value = row.get(key)
    if value in (None, ""):
        return 0.0
    return float(value)


def _int_field(row: dict[str, Any], key: str) -> int:
    value = row.get(key)
    if value in (None, ""):
        return 0
    return int(float(value))


def load_agg_rows_from_csv() -> list[dict[str, Any]]:
    if not config.SUMMARY_CSV.exists():
        return []
    rows: list[dict[str, Any]] = []
    for row in read_csv(config.SUMMARY_CSV):
        rows.append(
            {
                "config_id": row.get("config_id", ""),
                "n": _int_field(row, "n"),
                "passend_n": _int_field(row, "passend_n"),
                "passend_pct": _float_field(row, "passend_pct"),
                "abdeckung_n": _int_field(row, "abdeckung_n"),
                "abdeckung_pct": _float_field(row, "abdeckung_pct"),
                "wahr_n": _int_field(row, "wahr_n"),
                "wahr_pct": _float_field(row, "wahr_pct"),
                "falsch_n": _int_field(row, "falsch_n"),
                "falsch_pct": _float_field(row, "falsch_pct"),
                "enthaltung_n": _int_field(row, "enthaltung_n"),
                "enthaltung_pct": _float_field(row, "enthaltung_pct"),
                "korrektheit_score": _float_field(row, "korrektheit_score"),
                "vollstaendig_n": _int_field(row, "vollstaendig_n"),
                "vollstaendig_pct": _float_field(row, "vollstaendig_pct"),
                "unvollstaendig_n": _int_field(row, "unvollstaendig_n"),
                "unvollstaendig_pct": _float_field(row, "unvollstaendig_pct"),
                "vollstaendigkeit_score": _float_field(row, "vollstaendigkeit_score"),
                "latency_median_ms": _float_field(row, "latency_median_ms"),
            }
        )
    return rows


def write_summary_charts(agg_rows: list[dict[str, Any]]) -> str | None:
    if not agg_rows:
        return None
    chart_path = render_summary_charts(agg_rows, config.CHARTS_DIR)
    return build_charts_markdown(chart_path, config.SUMMARY_MD)


def build_summary_md(
    agg_rows: list[dict[str, Any]],
    human_section: str | None = None,
    charts_section: str | None = None,
) -> str:
    lines = [
        "# Evaluations-Zusammenfassung",
        "",
        f"Generierungsmodell: `{config.GENERATION_MODEL}`",
        f"Judge-Modell: `{config.JUDGE_MODEL}`",
        "",
        "## Vergleich nach Konfiguration",
        "",
        "| Config | n | **Passend %** | Abdeckung % | Wahr % | Falsch % | Enthaltung % | Wahr-Score | Vollst. % | Unvollst. % | V-Score | Median Latenz (ms) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in agg_rows:
        lines.append(
            f"| {row['config_id']} | {row['n']} | **{row.get('passend_pct', 0.0)}** | "
            f"{row.get('abdeckung_pct', 0.0)} | {row['wahr_pct']} | "
            f"{row['falsch_pct']} | {row['enthaltung_pct']} | "
            f"{row['korrektheit_score']} | {row['vollstaendig_pct']} | "
            f"{row['unvollstaendig_pct']} | "
            f"{row['vollstaendigkeit_score']} | {row['latency_median_ms']} |"
        )

    lines.extend(
        [
            "",
            "## Hinweise",
            "",
            "- **Passend-Rate (Headline-Metrik):** Anteil der Antworten, die eine Aussage zur "
            "Sache treffen (nicht `enthaltung`), `korrektheit = wahr` UND "
            "`vollstaendigkeit = vollstaendig` sind — bezogen auf alle n. Bestraft (anders als "
            "der Wahr-Score) auch Schweigen und Lücken.",
            "- **Abdeckung (Diagnose):** Anteil echter Aussagen = (wahr + falsch) / n; zeigt die "
            "Antwortfreude. Diagnose-Trio = Abdeckung + Wahr-Score + Vollständigkeit.",
            "- **Korrektheit** ist 3-kategorial: `wahr` / `falsch` / `enthaltung`. `falsch` = "
            "unsicheres Scheitern (Widerspruch/Halluzination), `enthaltung` = sicheres Scheitern "
            "(kein Sachurteil und nichts Falsches: Unwissen ODER bloßer Verweis). Der **Wahr-Score** "
            "ist der Anteil wahrer Antworten NUR unter den echten Aussagen (wahr + falsch); "
            "`enthaltung` bleibt ausgeschlossen und wird als eigene Quote ausgewiesen.",
            "- **Vollständigkeit** ist binär (`vollstaendig`/`unvollstaendig`); optionale "
            "Musterlösungs-Punkte zählen nicht.",
            "- **A (Agent):** Determinismus wird innerhalb von n8n gesteuert, nicht von außen setzbar.",
            "- **B (RAG):** Neutrales Default-Chunking (~512 Token, Overlap), "
            f"`text-embedding-3-large`, top_k={config.RAG_SIMILARITY_TOP_K}.",
            "- **C+ (Websuche):** Inhärent nicht-deterministisch; `run_ts` pro Antwort loggen.",
            "- Judge ist blind (keine config_id, kein Generierungsmodell).",
        ]
    )

    if human_section:
        lines.extend(["", human_section])

    if charts_section:
        lines.extend(["", charts_section.rstrip()])

    return "\n".join(lines) + "\n"


def _stratified_sample(
    pool: list[dict[str, Any]],
    k: int,
    key_fn,
    rng: random.Random,
) -> list[dict[str, Any]]:
    """Ziehe k Elemente aus pool, moeglichst gleichmaessig ueber die Kategorien
    key_fn(row) verteilt (Round-Robin, durch Verfuegbarkeit begrenzt), deterministisch."""
    if k >= len(pool):
        return list(pool)
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in pool:
        groups[key_fn(row)].append(row)
    cats = sorted(groups)  # stabile Reihenfolge (falsch < enthaltung < wahr)
    alloc = {c: 0 for c in cats}
    remaining = k
    # Round-Robin: pro Runde jeder Kategorie mit Restkapazitaet ein Slot
    while remaining > 0 and any(len(groups[c]) > alloc[c] for c in cats):
        for c in cats:
            if remaining == 0:
                break
            if alloc[c] < len(groups[c]):
                alloc[c] += 1
                remaining -= 1
    chosen: list[dict[str, Any]] = []
    for c in cats:
        chosen.extend(rng.sample(groups[c], alloc[c]))
    rng.shuffle(chosen)
    return chosen


def export_manual_sample(
    judged: list[dict[str, Any]],
    raw: list[dict[str, Any]],
    questions_by_id: dict[str, dict[str, str]],
) -> None:
    by_config: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in judged:
        cid = row.get("config_id")
        if cid in config.CONFIG_IDS:
            by_config[cid].append(row)

    rng = random.Random(config.MANUAL_SAMPLE_SEED)
    selected: list[dict[str, Any]] = []
    for config_id in config.CONFIG_IDS:
        pool = by_config.get(config_id, [])
        k = min(config.MANUAL_SAMPLE_PER_CONFIG, len(pool))
        # Stratifiziert nach Korrektheits-Kategorie (wahr/falsch/enthaltung), damit die
        # strittigen Minderheitsklassen (falsch, enthaltung) in der Judge-Validierung
        # vertreten sind und Cohen's kappa nicht von der wahr-Mehrheit dominiert wird.
        selected.extend(
            _stratified_sample(pool, k, lambda r: r.get("korrektheit", ""), rng)
        )

    raw_by_key = {
        (row.get("question_id"), row.get("config_id")): row for row in raw
    }

    sample_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    for idx, judged_row in enumerate(selected, start=1):
        qid = judged_row["question_id"]
        cid = judged_row["config_id"]
        question = questions_by_id[qid]
        raw_row = raw_by_key.get((qid, cid), {})
        sample_id = f"S{idx:02d}"

        sample_rows.append(
            {
                "sample_id": sample_id,
                "question_id": qid,
                "frage": question["frage"],
                "musterloesung": question["musterloesung"],
                "answer": raw_row.get("answer", ""),
                "human_korrektheit": "",
                "human_vollstaendigkeit": "",
            }
        )
        key_rows.append(
            {
                "sample_id": sample_id,
                "question_id": qid,
                "config_id": cid,
                "judge_korrektheit": judged_row.get("korrektheit", ""),
                "judge_vollstaendigkeit": judged_row.get("vollstaendigkeit", ""),
            }
        )

    write_csv(
        config.MANUAL_SAMPLE_CSV,
        [
            "sample_id",
            "question_id",
            "frage",
            "musterloesung",
            "answer",
            "human_korrektheit",
            "human_vollstaendigkeit",
        ],
        sample_rows,
    )
    write_csv(
        config.MANUAL_KEY_CSV,
        [
            "sample_id",
            "question_id",
            "config_id",
            "judge_korrektheit",
            "judge_vollstaendigkeit",
        ],
        key_rows,
    )


def cohens_kappa(labels_a: list[str], labels_b: list[str]) -> float | None:
    if len(labels_a) != len(labels_b) or not labels_a:
        return None
    categories = sorted(set(labels_a) | set(labels_b))
    n = len(labels_a)
    if n == 0:
        return None

    observed = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n
    dist_a = Counter(labels_a)
    dist_b = Counter(labels_b)
    expected = sum((dist_a[c] / n) * (dist_b[c] / n) for c in categories)
    if expected >= 1.0:
        return None
    return round((observed - expected) / (1 - expected), 3)


def compare_human_judge() -> str | None:
    if not config.MANUAL_SAMPLE_CSV.exists() or not config.MANUAL_KEY_CSV.exists():
        return None

    sample = read_csv(config.MANUAL_SAMPLE_CSV)
    key = {row["sample_id"]: row for row in read_csv(config.MANUAL_KEY_CSV)}

    paired_k: list[tuple[str, str]] = []
    paired_v: list[tuple[str, str]] = []
    for row in sample:
        sid = row.get("sample_id", "")
        human_k = (row.get("human_korrektheit") or "").strip().lower()
        human_v = (row.get("human_vollstaendigkeit") or "").strip().lower()
        if not human_k or not human_v:
            continue
        judge_row = key.get(sid)
        if not judge_row:
            continue
        paired_k.append((human_k, judge_row.get("judge_korrektheit", "").strip().lower()))
        paired_v.append((human_v, judge_row.get("judge_vollstaendigkeit", "").strip().lower()))

    if not paired_k:
        return (
            "## Manuelle Validierung\n\n"
            "_Noch keine ausgefüllten human_korrektheit/human_vollstaendigkeit "
            "in manual_sample.csv._"
        )

    agree_k = sum(1 for h, j in paired_k if h == j) / len(paired_k)
    agree_v = sum(1 for h, j in paired_v if h == j) / len(paired_v)
    kappa_k = cohens_kappa([h for h, _ in paired_k], [j for _, j in paired_k])
    kappa_v = cohens_kappa([h for h, _ in paired_v], [j for _, j in paired_v])

    lines = [
        "## Manuelle Validierung (Judge vs. Mensch)",
        "",
        f"- Stichprobe: {len(paired_k)} ausgefüllte Fälle",
        f"- Übereinstimmung Korrektheit: {round(agree_k * 100, 1)}%",
        f"- Übereinstimmung Vollständigkeit: {round(agree_v * 100, 1)}%",
    ]
    if kappa_k is not None:
        lines.append(f"- Cohen's κ Korrektheit: {kappa_k}")
    if kappa_v is not None:
        lines.append(f"- Cohen's κ Vollständigkeit: {kappa_v}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage 3: Aggregation und Stichprobe")
    parser.add_argument(
        "--compare-human",
        action="store_true",
        help="Nur Judge-vs.-Mensch-Vergleich in summary.md ergänzen",
    )
    parser.add_argument(
        "--skip-sample",
        action="store_true",
        help="Manuelle Stichprobe nicht neu erzeugen",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config.OUT_DIR.mkdir(parents=True, exist_ok=True)

    judged = load_jsonl(config.JUDGED_RESULTS_JSONL)
    raw = load_jsonl(config.RAW_RESPONSES_JSONL)
    questions_by_id = {q["question_id"]: q for q in load_questions()}

    if args.compare_human:
        agg_rows = load_agg_rows_from_csv()
        human_section = compare_human_judge()
        charts_section = write_summary_charts(agg_rows)
        if not agg_rows:
            existing = (
                config.SUMMARY_MD.read_text(encoding="utf-8")
                if config.SUMMARY_MD.exists()
                else ""
            )
            if human_section and "## Manuelle Validierung" in existing:
                prefix = existing.split("## Manuelle Validierung", 1)[0].rstrip()
                suffix = ""
                if "## Visualisierung" in existing:
                    suffix = (
                        "\n\n## Visualisierung\n\n"
                        + existing.split("## Visualisierung", 1)[1].lstrip()
                    )
                config.SUMMARY_MD.write_text(
                    prefix + "\n\n" + human_section + suffix + "\n",
                    encoding="utf-8",
                )
            elif human_section:
                config.SUMMARY_MD.write_text(
                    existing.rstrip() + "\n\n" + human_section + "\n",
                    encoding="utf-8",
                )
        else:
            config.SUMMARY_MD.write_text(
                build_summary_md(agg_rows, human_section, charts_section),
                encoding="utf-8",
            )
        print("Human-Vergleich in summary.md aktualisiert.")
        return

    agg_rows = aggregate(judged, raw)
    if not agg_rows:
        print("Keine judged_results — nichts zu aggregieren.")
        return

    write_csv(config.SUMMARY_CSV, list(agg_rows[0].keys()), agg_rows)
    human_section = compare_human_judge()
    charts_section = write_summary_charts(agg_rows)
    config.SUMMARY_MD.write_text(
        build_summary_md(agg_rows, human_section, charts_section),
        encoding="utf-8",
    )

    if not args.skip_sample:
        export_manual_sample(judged, raw, questions_by_id)

    print(f"Geschrieben: {config.SUMMARY_CSV}, {config.SUMMARY_MD}")
    if charts_section:
        print(f"Diagramm: {config.SUMMARY_CHART_OVERVIEW}")
    if not args.skip_sample:
        print(f"Stichprobe: {config.MANUAL_SAMPLE_CSV}, Mapping: {config.MANUAL_KEY_CSV}")


if __name__ == "__main__":
    main()
