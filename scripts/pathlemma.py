"""Test the lemma:  in an r-connected graph, p(x,y) >= p_{K_{r+1}}(x,y).

If true, an induction gives  min{ c(G) : G k-connected } = c(K_{k+1}).
"""

from __future__ import annotations

import sys
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cycle_spectra import (  # noqa: E402
    count_paths,
    two_connected_graphs,
    vertex_connectivity,
)


def Q(k: int) -> int:
    """p_{K_k}(x,y): number of simple x-y paths in the complete graph K_k."""
    return sum(comb(k - 2, j) * factorial(j) for j in range(0, k - 1))


def Q_by_recurrence(k: int) -> int:
    """The same number via Q_2 = 1 and Q_{r+1} = 1 + (r-1) Q_r."""
    if k == 2:
        return 1
    return 1 + (k - 2) * Q_by_recurrence(k - 1)


def main(max_n: int = 8):
    print("Q(k) = p_{K_k}(x,y) for k = 2..9 :", {k: Q(k) for k in range(2, 10)})
    print("via recurrence             :", {k: Q_by_recurrence(k) for k in range(2, 10)})
    for k in range(2, 10):
        assert Q(k) == Q_by_recurrence(k), k
    print("recurrence identity verified for k = 2..9")
    print()
    for n in range(3, max_n + 1):
        graphs = two_connected_graphs(n)
        bad = []
        minima = {}
        for g in graphs:
            k = vertex_connectivity(g)
            for x in range(n):
                for y in range(x + 1, n):
                    p = count_paths(g, x, y)
                    key = (k, g.n)
                    if key not in minima or p < minima[key][0]:
                        minima[key] = (p, g)
                    if p < Q(k + 1):
                        bad.append((g.n, g.m, k, x, y, p, Q(k + 1)))
        if bad:
            print(f"n={n}: LEMMA VIOLATED in {len(bad)} cases, e.g. {bad[0]}")
        else:
            summary = {
                k: (minima[(k, n)][0], Q(k + 1)) for k in sorted({key[0] for key in minima})
            }
            print(
                f"n={n}: lemma holds. (min p(x,y), Q(k+1)) by connectivity: {summary}"
            )


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)