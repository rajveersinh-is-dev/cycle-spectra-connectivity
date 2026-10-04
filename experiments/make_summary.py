"""Regenerate ``results/summary.md`` from the JSON files already on disk.

This lets the summary be refreshed without re-running the (expensive)
computations, e.g. after editing the formatting.  All numbers are read from
``results/*.json``; nothing is recomputed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
from run_all import summarise  # noqa: E402

FILES = {
    "cardinalities": "cardinalities",
    "theorems": "path_lemma_and_theorem_a",
    "extremal": "extremal_m3",
    "spectra": "spectra",
    "cone": "cone_theorem",
}


def main() -> None:
    results = {}
    for key, name in FILES.items():
        results[key] = json.loads((common.RESULTS / f"{name}.json").read_text(encoding="utf-8"))
    summarise(results)
    print("summary regenerated from results/*.json")


if __name__ == "__main__":
    main()