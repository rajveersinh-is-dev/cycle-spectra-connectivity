"""Stage 5: the cone theorem (Theorem B).

Question answered: *among 2-connected base graphs of a fixed order, which cone
has the fewest cycles, and is the minimum attained only by the cycle?*
"""

from __future__ import annotations

from common import Timer, dump
from cycle_spectra import (
    Graph,
    cone_cycles,
    count_cycles,
    count_paths,
    two_connected_graphs,
    total_paths,
)


def cone(base: Graph) -> Graph:
    """The cone ``K_1 v base``."""
    n = base.n
    hub = 1 << n
    adj = [base.adj[v] | hub for v in range(n)] + [hub - 1]
    return Graph(n + 1, adj)


def main(max_n: int = 8) -> dict:
    print("stage 5: cone theorem")
    rows = []
    identity_ok = True
    for n in range(3, max_n + 1):
        with Timer() as t:
            graphs = two_connected_graphs(n)
        vals = [cone_cycles(g) for g in graphs]
        mn = min(vals)
        argmin = [g for g, v in zip(graphs, vals) if v == mn]
        expected = n * (n - 1) + 1
        is_cycle = all(sorted(g.degrees()) == [2] * n for g in argmin)
        for g in graphs:
            if cone_cycles(g) != count_cycles(cone(g)) or cone_cycles(g) != count_cycles(g) + total_paths(g):
                identity_ok = False
        rows.append(
            {
                "base_order": n,
                "classes": len(graphs),
                "min_cone_cycles": mn,
                "predicted_min": expected,
                "minimiser_is_the_cycle": is_cycle,
                "num_minimisers": len(argmin),
                "max_cone_cycles": max(vals),
                "seconds": round(t.seconds, 2),
            }
        )
        print(
            f"  n={n}: min c(K_1 v F) = {mn} (predicted n(n-1)+1 = {expected}), "
            f"minimiser is the cycle: {is_cycle}, spread "
            f"[{mn}, {max(vals)}] over {len(graphs)} classes"
        )
    payload = {
        "rows": rows,
        "identity_c_K1vF_verified": identity_ok,
        "theorem_b_verified": all(
            r["min_cone_cycles"] == r["predicted_min"] and r["minimiser_is_the_cycle"]
            for r in rows
        ),
        "statement": (
            "For every 2-connected graph F on m >= 3 vertices, c(K_1 v F) >= m(m-1)+1, "
            "with equality iff F is a cycle."
        ),
    }
    dump("cone_theorem", payload)
    return payload


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)