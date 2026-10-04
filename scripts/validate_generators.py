"""Cross-validation of the generators against exhaustive brute force.

For ``n <= 7`` we enumerate *all* ``2^(n choose 2)`` graphs on ``n`` vertices,
filter the ``k``-connected ones and deduplicate with exact canonical labels.
This gives an independent check that the incremental generators in
``cycle_spectra.generation`` neither miss nor invent isomorphism classes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cycle_spectra import count_cycles, is_2connected, is_3connected  # noqa: E402
from cycle_spectra.generation import (  # noqa: E402
    canonical_form,
    three_connected_graphs,
    two_connected_graphs,
)
from cycle_spectra.graph import Graph  # noqa: E402


def all_graphs(n: int):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(pairs)):
        adj = [0] * n
        for i, (u, v) in enumerate(pairs):
            if (mask >> i) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        yield Graph(n, adj)


def classes(graphs, pred):
    seen: set[int] = set()
    out = []
    for g in graphs:
        if pred(g):
            k = canonical_form(g)
            if k not in seen:
                seen.add(k)
                out.append(g)
    return out


def main(max_n: int = 7):
    print("n | brute 2conn | gen 2conn | brute 3conn | gen 3conn")
    for n in range(3, max_n + 1):
        graphs = list(all_graphs(n))
        b2 = classes(graphs, is_2connected)
        b3 = classes(graphs, is_3connected)
        g2 = two_connected_graphs(n)
        g3 = three_connected_graphs(n)
        print(f"{n} | {len(b2):8d} | {len(g2):7d} | {len(b3):10d} | {len(g3):7d}")
        assert len(b2) == len(g2), f"2-connected count mismatch at n={n}"
        assert len(b3) == len(g3), f"3-connected count mismatch at n={n}"
        # cross-check cycle-count spectra agree
        s_b2 = {count_cycles(g) for g in b2}
        s_g2 = {count_cycles(g) for g in g2}
        assert s_b2 == s_g2, f"2-connected spectrum mismatch at n={n}"
        s_b3 = {count_cycles(g) for g in b3}
        s_g3 = {count_cycles(g) for g in g3}
        assert s_b3 == s_g3, f"3-connected spectrum mismatch at n={n}"
    print("all cross-validation checks passed")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)