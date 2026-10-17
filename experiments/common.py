'''Shared configuration and IO helpers for the experiment pipeline.

This module provides a small set of utilities used throughout the
experiment code base:

* Path constants (ROOT, SRC, RESULTS, FIGURES)
* A deterministic random seed (SEED)
* Published reference data for 2‑ and 3‑connected graphs
* Functions for provenance collection, timing, JSON dumping and a
  Matplotlib configuration helper.

All public objects are exported via ``__all__`` to make the intended API
explicit.  Type hints and thorough docstrings are added to aid static
analysis and improve maintainability.
'''  # noqa: D400, D401

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict

# ---------------------------------------------------------------------------
# Path constants – resolved once at import time for efficiency.
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

# Ensure the source directory is on ``sys.path`` so that ``import`` works when
# the repository is executed from the top‑level directory.
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# ---------------------------------------------------------------------------
# Global configuration values.
# ---------------------------------------------------------------------------
#: No experiment in this repository uses randomness. The seed is recorded
#: anyway so that the provenance block of every result file is complete.
SEED: int = 0

#: Published cardinalities used as an external cross‑check.
PUBLISHED_TWO_CONN: Dict[int, int] = {
    3: 1,
    4: 3,
    5: 10,
    6: 56,
    7: 468,
    8: 7123,
    9: 194066,
}
PUBLISHED_THREE_CONN: Dict[int, int] = {
    4: 1,
    5: 3,
    6: 17,
    7: 136,
    8: 2388,
}

#: The exception list conjectured by McCulloch–McKay–Salahshoori–Zaslavsky for
#: 3‑connected graphs (Graphs Combin. 42 (2026), Conjecture 6(a)).
THREE_CONN_CONJECTURED_EXCEPTIONS = [
    1,
    2,
    3,
    4,
    5,
    6,
    8,
    9,
    10,
    11,
    12,
    16,
    17,
    18,
    19,
    20,
    27,
    30,
    32,
    33,
    34,
]

#: Their proved exception list for 2‑connected graphs.
TWO_CONN_KNOWN_EXCEPTIONS = [2, 4, 5, 8, 9, 16]

__all__ = [
    "ROOT",
    "SRC",
    "RESULTS",
    "FIGURES",
    "SEED",
    "PUBLISHED_TWO_CONN",
    "PUBLISHED_THREE_CONN",
    "THREE_CONN_CONJECTURED_EXCEPTIONS",
    "TWO_CONN_KNOWN_EXCEPTIONS",
    "environment",
    "Timer",
    "dump",
    "setup_matplotlib",
]


def environment() -> Dict[str, Any]:
    """Collect a provenance dictionary for result files.

    The function lazily imports heavy optional dependencies (``matplotlib``,
    ``networkx``, ``numpy`` and ``igraph``) only when required, keeping import
    time low for scripts that do not need provenance information.

    Returns
    -------
    dict
        Mapping containing version information, the current Git commit (if
        available), the deterministic seed, and a UTC timestamp.
    """
    import matplotlib
    import networkx
    import numpy
    import igraph

    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:  # pragma: no cover – Git may be unavailable in CI.
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
    """Simple context manager for measuring elapsed wall‑clock time.

    Example
    -------
    >>> with Timer() as t:
    ...     heavy_computation()
    >>> print(t.seconds)  # doctest: +SKIP
    """

    def __init__(self) -> None:
        self._start: float | None = None
        self.seconds: float | None = None

    def __enter__(self) -> "Timer":
        self._start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Record elapsed time even if an exception propagates.
        if self._start is not None:
            self.seconds = time.time() - self._start
        # Returning ``False`` (or ``None``) tells Python to re‑raise any exception.
        return False

    def __repr__(self) -> str:  # pragma: no cover – trivial representation.
        elapsed = f"{self.seconds:.6f}s" if self.seconds is not None else "not finished"
        return f"<Timer elapsed={elapsed}>"


def dump(name: str, payload: Dict[str, Any]) -> Path:
    """Write ``payload`` to ``results/<name>.json`` with provenance attached.

    Parameters
    ----------
    name:
        Base filename without extension.  The function creates the ``results``
        directory if it does not exist.
    payload:
        Arbitrary JSON‑serialisable data that will be merged with the provenance
        block under the ``"_environment"`` key.

    Returns
    -------
    pathlib.Path
        Path to the written JSON file.
    """
    # Defensive programming – ensure the target directory exists.
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    data = {"_environment": environment(), **payload}
    # ``json.dumps`` raises ``TypeError`` for non‑serialisable objects; we let the
    # exception propagate so that callers are aware of malformed payloads.
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")
    return path


def setup_matplotlib():
    """Configure Matplotlib for non‑interactive, reproducible figure generation.

    The function switches the backend to ``Agg`` (suitable for headless CI
    environments) and applies a compact style that matches the figures used in
    the associated paper.

    Returns
    -------
    matplotlib.pyplot.ModuleType
        The ``pyplot`` module after configuration, allowing callers to use the
        familiar ``plt`` alias directly.
    """
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
