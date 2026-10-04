"""Explore the minimum number of cycles in a k-connected graph.

Question: is min{ c(G) : G k-connected } equal to c(K_{k+1})?
We enumerate every unlabeled 3-connected graph up to order 8 and partition by
vertex connectivity.
"""

from __future__ import annotations

import sys
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cycle_spectra import (  # noqa: E402
    count_cycles,
    three_connected_graphs,
    vertex_connectivity,
)


def c_complete(n: int) -> int:
    """Number of cycles of K_n."""
    return sum(comb(n, j) * factorial(j - 1) // 2 for j in range(3, n + 1))


def main(max_n: int = 8):
    print("c(K_n):", {n: c_complete(n) for n in range(3, max_n + 2)})
    print()
    best = {}
    for n in range(4, max_n + 1):
        graphs = three_connected_graphs(n)
        by_k = {}
        for g in graphs:
            k = vertex_connectivity(g)
            c = count_cycles(g)
            if k not in by_k or c < by_k[k][0]:
                by_k[k] = (c, g)
        line = f"n={n}: "
        for k in sorted(by_k, reverse=True):
            c, g = by_k[k]
            line += f"[k={k}: min={c} degseq={sorted(g.degrees(), reverse=True)}] "
            if k not in best or c < best[k][0]:
                best[k] = (c, n, g)
        print(line)
    print()
    for k in sorted(best):
        c, n, g = best[k]
        print(
            f"k={k}: min cycle count over all enumerated = {c} "
            f"(attained at n={n}); c(K_{k+1}) = {c_complete(k + 1)}"
        )


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)