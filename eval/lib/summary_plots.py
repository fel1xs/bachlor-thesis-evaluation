"""Diagramme für die Evaluations-Zusammenfassung (Stage 3)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CONFIG_COLORS = {
    "A": "#2563eb",
    "B": "#7c3aed",
    "C+": "#059669",
}

KORREKTHEIT_COLORS = {
    "wahr": "#16a34a",
    "falsch": "#dc2626",
    "enthaltung": "#9ca3af",
}

VOLLSTAENDIGKEIT_COLORS = {
    "vollstaendig": "#16a34a",
    "unvollstaendig": "#dc2626",
}


def _configs(agg_rows: list[dict[str, Any]]) -> list[str]:
    return [str(row["config_id"]) for row in agg_rows]


def _pct(row: dict[str, Any], key: str) -> float:
    return float(row.get(key) or 0)


def render_summary_charts(agg_rows: list[dict[str, Any]], out_dir: Path) -> Path:
    """Erzeugt ein 2×2-Übersichtsdiagramm. Gibt den PNG-Pfad zurück."""
    if not agg_rows:
        raise ValueError("Keine Aggregationsdaten für Diagramme")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "summary_overview.png"

    configs = _configs(agg_rows)
    x = range(len(configs))

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    fig.suptitle("Evaluationsvergleich nach Konfiguration", fontsize=14, fontweight="bold")

    _plot_stacked_percent(
        axes[0, 0],
        configs,
        x,
        [
            [_pct(row, "wahr_pct") for row in agg_rows],
            [_pct(row, "falsch_pct") for row in agg_rows],
            [_pct(row, "enthaltung_pct") for row in agg_rows],
        ],
        ["Wahr", "Falsch", "Enthaltung"],
        [
            KORREKTHEIT_COLORS["wahr"],
            KORREKTHEIT_COLORS["falsch"],
            KORREKTHEIT_COLORS["enthaltung"],
        ],
        "Korrektheit (%)",
    )

    _plot_stacked_percent(
        axes[0, 1],
        configs,
        x,
        [
            [_pct(row, "vollstaendig_pct") for row in agg_rows],
            [_pct(row, "unvollstaendig_pct") for row in agg_rows],
        ],
        ["Vollständig", "Unvollständig"],
        [
            VOLLSTAENDIGKEIT_COLORS["vollstaendig"],
            VOLLSTAENDIGKEIT_COLORS["unvollstaendig"],
        ],
        "Vollständigkeit (%)",
    )

    _plot_scores(axes[1, 0], configs, x, agg_rows)
    _plot_latency(axes[1, 1], configs, x, agg_rows)

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def _plot_stacked_percent(
    ax: plt.Axes,
    configs: list[str],
    x: range,
    series: list[list[float]],
    labels: list[str],
    colors: list[str],
    title: str,
) -> None:
    bottom = [0.0] * len(configs)
    for values, label, color in zip(series, labels, colors):
        ax.bar(x, values, bottom=bottom, label=label, color=color, width=0.55)
        bottom = [b + v for b, v in zip(bottom, values)]

    ax.set_title(title)
    ax.set_xticks(list(x))
    ax.set_xticklabels(configs)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Anteil (%)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)


def _plot_scores(
    ax: plt.Axes,
    configs: list[str],
    x: range,
    agg_rows: list[dict[str, Any]],
) -> None:
    width = 0.35
    x_list = list(x)
    k_scores = [float(row.get("korrektheit_score") or 0) for row in agg_rows]
    v_scores = [float(row.get("vollstaendigkeit_score") or 0) for row in agg_rows]

    ax.bar(
        [i - width / 2 for i in x_list],
        k_scores,
        width=width,
        label="Wahr-Score",
        color="#3b82f6",
    )
    ax.bar(
        [i + width / 2 for i in x_list],
        v_scores,
        width=width,
        label="V-Score",
        color="#8b5cf6",
    )
    ax.set_title("Mittlere Scores (0–1)")
    ax.set_xticks(x_list)
    ax.set_xticklabels(configs)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)


def _plot_latency(
    ax: plt.Axes,
    configs: list[str],
    x: range,
    agg_rows: list[dict[str, Any]],
) -> None:
    latencies = [float(row.get("latency_median_ms") or 0) for row in agg_rows]
    colors = [CONFIG_COLORS.get(cfg, "#64748b") for cfg in configs]
    bars = ax.bar(list(x), latencies, color=colors, width=0.55)
    ax.set_title("Median-Latenz")
    ax.set_xticks(list(x))
    ax.set_xticklabels(configs)
    ax.set_ylabel("Millisekunden")
    ax.grid(axis="y", alpha=0.25)

    for bar, value in zip(bars, latencies):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,.0f}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=8,
        )


def build_charts_markdown(chart_path: Path, summary_md: Path) -> str:
    """Relativer Markdown-Link von summary.md zum Diagramm."""
    rel = chart_path.relative_to(summary_md.parent).as_posix()
    return (
        "## Visualisierung\n\n"
        f"![Übersicht der Evaluationsmetriken]({rel})\n"
    )
