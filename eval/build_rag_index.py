"""RAG-Index manuell bauen (optional, vor Stage 1)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.rag_setup import ensure_rag_index


def main() -> None:
    parser = argparse.ArgumentParser(description="LlamaIndex-Vektorstore bauen oder neu bauen")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Vorhandenen rag_index/ + rag_chroma/ löschen und neu erstellen",
    )
    args = parser.parse_args()
    ensure_rag_index(force_rebuild=args.rebuild)
    print("Fertig.")


if __name__ == "__main__":
    main()
