"""Shared configuration and IO helpers for the experiment pipeline."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

#: No experiment in this repository uses randomness.  The seed is recorded
#: anyway so that the provenance block of every result file is complete.
SEED = 0

#: Published cardinalities used as an external cross-check.
PUBLISHED_TWO_CONN = {3: 1, 4: 3, 5: 10, 6: 56, 7: 468, 8: 7123, 9: 194066}
PUBLISHED_THREE_CONN = {4: 1, 5: 3, 6: 17, 7: 136, 8: 2388}

#: The exception list conjectured by McCulloch--McKay--Salahshoori--Zaslavsky for
#: 3-connected graphs (Graphs Combin. 42 (2026), Conjecture 6(a)).
THREE_CONN_CONJECTURED_EXCEPTIONS = [
    1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 27, 30, 32, 33, 34,
]

#: Their proved exception list for 2-connected graphs.
TWO_CONN_KNOWN_EXCEPTIONS = [2, 4, 5, 8, 9, 16]


def environment() -> dict[str, Any]:
    """Provenance block written into every result file."""
    import matplotlib
    import networkx
    import numpy
    import igraph

    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
    except Exception:  # pragma: no cover
        commit = "unknown"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": numpy.__version__,
        "networkx": networkx.__version__,
        "igraph": igraph.__version__,
        "matplotlib": matplotlib.__version__,
        "git_commit": commit,
        "seed": SEED,
        "randomness_used": False,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class Timer:
    """Context manager writing ``{'seconds': ..., 'started': ...}``."""

    def __init__(self) -> None:
        self.t0 = time.time()

    def __enter__(self) -> "Timer":
        return self

    def __exit__(self, *exc: object) -> None:
        self.seconds = time.time() - self.t0


def dump(name: str, payload: dict[str, Any]) -> Path:
    """Write ``payload`` to ``results/<name>.json`` with provenance attached."""
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    data = {"_environment": environment(), **payload}
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")
    return path


def setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 140,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "figure.autolayout": False,
        }
    )
    return plt