"""Hand-provable facts about graphs with very few cycles.

These are the statements that can be established without any computer
assistance; the proofs are given in full in the paper (Section 4).

*   ``cycle_count_is_never_two``   -- no graph has exactly 2 cycles unless ...
*   ``two_connected_minimal``     -- a 2-connected graph has 1 cycle iff it is a
    cycle, and 3 cycles iff it is a theta graph.
*   therefore no 2-connected graph has 2, 4 or 5 cycles.

The computational counterpart (which needs the ear analysis of
McCulloch--McKay--Salahshoori--Zaslavsky for 8, 9, 16) is checked in
``tests/test_spectra.py``.
"""

from __future__ import annotations

from itertools import combinations

from .cycles import count_cycles
from .graph import Graph, cycle_graph

__all__ = [
    "is_2connected_minimal_graph",
    "exhaustive_two_connected_cycle_counts",
]


def is_2connected_minimal_graph(g: Graph, value: int) -> bool:
    """Structural certificate for small cycle counts.

    ``value == 1``: ``g`` is a cycle (so 2-connected iff ``|V| >= 3``).
    ``value == 3``: ``g`` is a theta graph, i.e. it consists of three internally
    disjoint paths with common end points.
    """
    if value == 1:
        return all(g.degree(v) == 2 for v in range(g.n)) and g.m == g.n
    if value == 3:
        return sorted(g.degrees(), reverse=True) == [3, 3] + [2] * (g.n - 2)
    return False


def exhaustive_two_connected_cycle_counts(max_n: int = 9) -> dict[int, int]:
    """Cycle counts of 2-connected graphs up to ``max_n``: value -> how many classes."""
    from .generation import two_connected_graphs

    out: dict[int, int] = {}
    for n in range(3, max_n + 1):
        for g in two_connected_graphs(n):
            c = count_cycles(g)
            out[c] = out.get(c, 0) + 1
    return dict(sorted(out.items()))