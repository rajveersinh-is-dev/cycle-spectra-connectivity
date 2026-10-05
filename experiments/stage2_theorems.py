"""Stage 2: the Path Lemma and Theorem A.

Questions answered
------------------
1.  Does ``p(x,y) >= Q_{r+1}`` hold in every ``r``-connected graph, for every
    pair of vertices?  (Checked on *all* 2-connected graphs up to order
    ``max_n``.)
2.  Is the minimum number of cycles of a ``k``-connected graph exactly
    ``c(K_{k+1})``, as Theorem A claims, and is the extremiser ``K_{k+1}``?
"""

from __future__ import annotations

from common import Timer, dump
from cycle_spectra import (
    Q,
    c_complete,
    count_cycles,
    count_paths,
    three_connected_graphs,
    two_connected_graphs,
    vertex_connectivity,
)


def q_by_recurrence(k: int) -> int:
    """Q via the recurrence Q_2 = 1, Q_{r+1} = 1 + (r-1) Q_r."""
    if k == 2:
        return 1
    return 1 + (k - 2) * q_by_recurrence(k - 1)


def stage2_path_lemma(max_n: int = 8) -> dict:
    print("stage 2a: Path Lemma")
    q_table = {k: Q(k) for k in range(2, 10)}
    rec_ok = all(Q(k) == q_by_recurrence(k) for k in q_table)
    print("  Q_k = p_{K_k}(x,y) for k=2..9: " + str(q_table))
    print(f"  recurrence Q_(r+1) = 1 + (r-1) Q_r verified: {rec_ok}")

    violations = []
    observed: dict[str, int] = {}
    checked_pairs = 0
    for n in range(3, max_n + 1):
        t0 = Timer()
        with t0:
            graphs = two_connected_graphs(n)
        for g in graphs:
            r = vertex_connectivity(g)
            target = Q(r + 1)
            key = str(r)
            for x in range(n):
                for y in range(x + 1, n):
                    p = count_paths(g, x, y)
                    checked_pairs += 1
                    if p < target:
                        violations.append(
                            {"n": n, "kappa": r, "x": x, "y": y, "p": p, "target": target}
                        )
                    if key not in observed or p < observed[key]:
                        observed[key] = p
        print(
            f"  n={n}: {len(graphs):>6} classes, {t0.seconds:6.1f}s; "
            f"min p(x,y) by connectivity: "
            + ", ".join(
                f"r={r}: {observed[str(r)]} (>= Q_{r+1}={Q(r+1)})"
                for r in range(2, n)
                if str(r) in observed
            )
        )
    print(f"  pairs checked: {checked_pairs}, violations: {len(violations)}")
    return {
        "Q_table": q_table,
        "recurrence_verified": rec_ok,
        "pairs_checked": checked_pairs,
        "violations": violations,
        "min_path_count_by_connectivity": observed,
    }


def stage2_theorem_a(max_n: int = 9) -> dict:
    print("stage 2b: Theorem A")
    best: dict[int, dict] = {}
    per_order: dict[str, dict] = {}
    for n in range(4, max_n + 1):
        row = {}
        for g in three_connected_graphs(n):
            k = vertex_connectivity(g)
            c = count_cycles(g)
            row.setdefault(k, []).append(c)
            if k not in best or c < best[k]["min_cycles"]:
                best[k] = {
                    "min_cycles": c,
                    "order": n,
                    "edges": g.m,
                    "degree_sequence": sorted(g.degrees(), reverse=True),
                    "edges_list": [list(e) for e in g.edge_list()],
                }
        per_order[str(n)] = {
            "kappa_min_cycles": {str(k): min(v) for k, v in sorted(row.items())},
            "c_complete": c_complete(n),
            "classes": len(three_connected_graphs(n)),
        }
        summary = ", ".join(f"k={k}:{min(v)}" for k, v in sorted(row.items(), reverse=True))
        print(f"  n={n}: min c by connectivity -> {summary}")
    print()
    ok = True
    for k in sorted(best):
        target = c_complete(k + 1)
        good = best[k]["min_cycles"] == target
        ok &= good
        print(
            f"  k={k}: min c = {best[k]['min_cycles']}  c(K_{k+1}) = {target}  "
            f"{'OK' if good else 'MISMATCH'}  (extremiser: n={best[k]['order']}, "
            f"degseq={best[k]['degree_sequence']})"
        )
    return {
        "minimum_over_k_connected": {str(k): best[k] for k in sorted(best)},
        "c_complete": {str(k + 1): c_complete(k + 1) for k in sorted(best)},
        "per_order": per_order,
        "theorem_a_verified": ok,
    }


def stage2_two_connected_lemma(max_n: int = 8) -> dict:
    """Lemma (paths in 2-connected graphs).

    In a 2-connected graph ``H`` and for ``a != b``: ``p_H(a,b) >= 2``, and
    ``p_H(a,b) == 2`` if and only if ``H`` is a cycle.  This is the statement the
    Path Lemma's ``r = 3`` equality case rests on, so it is checked on the same
    family as the Path Lemma itself.
    """
    print("stage 2a': paths in 2-connected graphs")
    violations: list[dict] = []
    checked_pairs = 0
    cycles_seen = 0
    for n in range(3, max_n + 1):
        for g in two_connected_graphs(n):
            # H is a cycle iff it is 2-regular with |E| = |V| and connected;
            # 2-connected already gives connected and n >= 3.
            is_cycle = g.m == n and g.min_degree == 2 and count_cycles(g) == 1
            cycles_seen += int(is_cycle)
            for x in range(n):
                for y in range(x + 1, n):
                    p = count_paths(g, x, y)
                    checked_pairs += 1
                    if p < 2 or (p == 2) != is_cycle:
                        violations.append(
                            {"n": n, "x": x, "y": y, "p": p, "is_cycle": is_cycle}
                        )
    print(
        f"  pairs checked: {checked_pairs} ({cycles_seen} cycles), "
        f"violations: {len(violations)}"
    )
    return {
        "pairs_checked": checked_pairs,
        "cycles_seen": cycles_seen,
        "violations": violations,
        "lemma_verified": not violations,
    }


def main(max_n: int = 8) -> dict:
    path = stage2_path_lemma(max_n=min(max_n, 8))
    two = stage2_two_connected_lemma(max_n=min(max_n, 8))
    thm = stage2_theorem_a(max_n=max_n)
    dump(
        "path_lemma_and_theorem_a",
        {"path_lemma": path, "two_connected_lemma": two, "theorem_a": thm},
    )
    return {"path_lemma": path, "two_connected_lemma": two, "theorem_a": thm}


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)