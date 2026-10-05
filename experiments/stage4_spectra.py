"""Stage 4: cycle-count spectra for connectivity levels k = 1, 2, 3 (and 4, 5).

Questions answered
------------------
*   ``S_1`` (connected graphs): which integers occur?  (all of them)
*   ``S_2`` (2-connected): which integers below 50 are missing, and does that
    agree with the proved exception list of McCulloch--McKay--Salahshoori--
    Zaslavsky?
*   ``S_3`` (3-connected): which integers below 51 are missing, and does that
    agree with *their conjecture*?
*   What are the least order ``mu(m)`` and greatest connectivity ``kap(m)`` that
    realise a given cycle count?
"""

from __future__ import annotations

from common import (
    THREE_CONN_CONJECTURED_EXCEPTIONS,
    TWO_CONN_KNOWN_EXCEPTIONS,
    Timer,
    dump,
)
from cycle_spectra import (
    count_cycles,
    is_connected,
    min_order_realising,
    missing_below,
    flower,
    three_connected_graphs,
    two_connected_graphs,
    vertex_connectivity,
)

BOUND = 50


def main(max_n: int = 9) -> dict:
    print("stage 4: spectra")
    # ---- S_1 -------------------------------------------------------------
    # A bouquet of t triangles is connected and has exactly t cycles, so S_1 is
    # all positive integers.  We *verify* the construction rather than assert it.
    s1 = set()
    bouquet_ok = True
    for t in range(1, 401):
        g = flower(t)
        if not is_connected(g):
            bouquet_ok = False
        s1.add(count_cycles(g))
    s1_missing = missing_below(s1, BOUND)
    print(f"  k=1 (connected): bouquets 1..400 verified ({'ok' if bouquet_ok else 'FAILED'}), "
          f"missing in [1,{BOUND}]: {s1_missing}")

    # ---- S_2 and S_3 -----------------------------------------------------
    s2: set[int] = set()
    s3: set[int] = set()
    per_order: dict[str, dict[str, int]] = {"2-connected": {}, "3-connected": {}}
    for n in range(3, max_n + 1):
        with Timer() as t:
            vals = {count_cycles(g) for g in two_connected_graphs(n)}
        s2 |= vals
        per_order["2-connected"][str(n)] = len(vals)
    for n in range(4, max_n + 1):
        vals = {count_cycles(g) for g in three_connected_graphs(n)}
        s3 |= vals
        per_order["3-connected"][str(n)] = len(vals)

    miss2 = missing_below(s2, BOUND)
    miss3 = missing_below(s3, BOUND)
    print(f"  k=2 (2-connected): |S_2|={len(s2)}, missing in [1,{BOUND}] = {miss2}")
    print(f"      agrees with the proved exception list {TWO_CONN_KNOWN_EXCEPTIONS}: "
          f"{set(miss2) <= set(TWO_CONN_KNOWN_EXCEPTIONS)}")
    print(f"  k=3 (3-connected): |S_3|={len(s3)}, missing in [1,{BOUND}] = {miss3}")
    print(f"      agrees with the conjectured exception list "
          f"{THREE_CONN_CONJECTURED_EXCEPTIONS}: "
          f"{miss3 == THREE_CONN_CONJECTURED_EXCEPTIONS}")

    # ---- S_4, S_5 restricted to small orders -----------------------------
    small3 = [g for n in range(4, min(max_n, 7) + 1) for g in three_connected_graphs(n)]
    kappa_hist: dict[int, int] = {}
    for g in small3:
        k = vertex_connectivity(g)
        kappa_hist[k] = kappa_hist.get(k, 0) + 1
    s4 = {count_cycles(g) for g in small3 if vertex_connectivity(g) >= 4}
    s5 = {count_cycles(g) for g in small3 if vertex_connectivity(g) >= 5}
    print(f"  k=4: |S_4| (orders <= {min(max_n, 7)}) = {len(s4)}, "
          f"min = {min(s4)}")
    print(f"  k=5: |S_5| (orders <= {min(max_n, 7)}) = {len(s5)}, "
          f"min = {min(s5)}")
    print(f"  connectivity histogram over those classes: {dict(sorted(kappa_hist.items()))}")

    # ---- mu and kap tables ----------------------------------------------
    all3 = [g for n in range(4, max_n + 1) for g in three_connected_graphs(n)]
    spec: dict[int, list] = {}
    for g in all3:
        spec.setdefault(count_cycles(g), []).append(g)
    mu = min_order_realising(spec)
    kap = {
        v: max((vertex_connectivity(g) for g in gs), default=0) for v, gs in spec.items()
    }
    print(f"  mu(m) = least order realising m, for m <= 12: "
          f"{ {m: mu[m].n for m in sorted(mu) if m <= 12} }")

    payload = {
        "max_order_examined": max_n,
        "S_1": "all positive integers (verified for 1..400 via the bouquet construction)",
        "S_1_bouquets_verified": bouquet_ok,
        "S_1_missing_below": s1_missing,
        "S_2_missing_below_bound": miss2,
        "S_2_bound": BOUND,
        "S_2_agrees_with_published": set(miss2) <= set(TWO_CONN_KNOWN_EXCEPTIONS),
        "S_2_published_exceptions": TWO_CONN_KNOWN_EXCEPTIONS,
        "S_3_missing_below_bound": miss3,
        "S_3_bound": BOUND,
        "S_3_agrees_with_conjecture": miss3 == THREE_CONN_CONJECTURED_EXCEPTIONS,
        "S_3_conjectured_exceptions": THREE_CONN_CONJECTURED_EXCEPTIONS,
        "S_2_size": len(s2),
        "S_3_size": len(s3),
        "distinct_counts_per_order": per_order,
        "S_4_size_small_orders": len(s4),
        "S_5_size_small_orders": len(s5),
        "connectivity_histogram": {str(k): v for k, v in sorted(kappa_hist.items())},
        "mu_small": {str(m): mu[m].n for m in sorted(mu) if m <= 20},
        "kappa_small": {str(m): kap[m] for m in sorted(kap) if m <= 20},
    }
    dump("spectra", payload)
    return payload


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)
