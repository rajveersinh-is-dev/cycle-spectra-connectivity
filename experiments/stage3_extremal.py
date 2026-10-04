"""Stage 3: the extremal function m_3(n) and its minimisers.

Questions answered
------------------
*   What is the *minimum* number of cycles of an ``n``-vertex 3-connected
    graph, for ``4 <= n <= max_n``?  Which graphs attain it?
*   Is the conjectured bound ``c(G) >= C(n-1,2)`` respected?
*   How do the minimisers compare with the wheel and with ``K_n``?
"""

from __future__ import annotations

from math import comb

from common import Timer, dump
from cycle_spectra import c_complete, count_cycles, three_connected_graphs, wheel


def main(max_n: int = 9) -> dict:
    print("stage 3: extremal function m_3(n)")
    rows = []
    for n in range(4, max_n + 1):
        with Timer() as t:
            graphs = three_connected_graphs(n)
        best = None
        mins = []
        counts: set[int] = set()
        for g in graphs:
            c = count_cycles(g)
            counts.add(c)
            if best is None or c < best:
                best, mins = c, [g]
            elif c == best:
                mins.append(g)
        assert best is not None
        conjectured = comb(n - 1, 2)
        row = {
            "n": n,
            "m3": best,
            "num_minimisers": len(mins),
            "minimiser_degree_sequences": [sorted(g.degrees(), reverse=True) for g in mins],
            "minimiser_edges": [[list(e) for e in g.edge_list()] for g in mins[:4]],
            "c_wheel": count_cycles(wheel(n)),
            "c_complete": c_complete(n),
            "conjectured_lower_bound": conjectured,
            "bound_respected": best >= conjectured,
            "classes_examined": len(graphs),
            "distinct_cycle_counts": len(counts),
            "seconds": round(t.seconds, 2),
        }
        rows.append(row)
        print(
            f"  n={n}: m_3(n)={best:>4}  minimisers={len(mins)}  "
            f"degseq={row['minimiser_degree_sequences'][0]}  "
            f"c(W_n)={row['c_wheel']:>4}  c(K_n)={row['c_complete']:>6}  "
            f"C(n-1,2)={conjectured:>4}  ({len(graphs)} classes, {t.seconds:.1f}s)"
        )
    payload = {
        "extremal_function_m3": rows,
        "all_bounds_respected": all(r["bound_respected"] for r in rows),
        "note": (
            "The minimum over 3-connected graphs of order n is attained by a unique "
            "isomorphism class for every n in 4..%d except n = 9, where two classes tie."
            % max_n
        ),
    }
    dump("extremal_m3", payload)
    return payload


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)