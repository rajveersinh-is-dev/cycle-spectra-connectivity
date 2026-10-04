"""Stage 1: cardinalities of the isomorphism classes, with published cross-checks.

Question answered: *do our generators produce exactly the published number of
unlabeled 2-connected and 3-connected graphs of each order?*
"""

from __future__ import annotations

from common import PUBLISHED_THREE_CONN, PUBLISHED_TWO_CONN, Timer, dump
from cycle_spectra import three_connected_graphs, two_connected_graphs


def main(max_n: int = 9) -> dict:
    two = {}
    three = {}
    timings = {"two_connected": {}, "three_connected": {}}
    print("stage 1: cardinalities")
    for n in range(3, max_n + 1):
        with Timer() as t:
            two[n] = len(two_connected_graphs(n))
        timings["two_connected"][n] = round(t.seconds, 2)
        ok = PUBLISHED_TWO_CONN.get(n)
        print(f"  2-connected n={n}: {two[n]:>7}   published {ok}   {'OK' if ok == two[n] or ok is None else 'MISMATCH'}")
    for n in range(4, max_n + 1):
        with Timer() as t:
            three[n] = len(three_connected_graphs(n))
        timings["three_connected"][n] = round(t.seconds, 2)
        ok = PUBLISHED_THREE_CONN.get(n)
        print(f"  3-connected n={n}: {three[n]:>7}   published {ok}   {'OK' if ok == three[n] or ok is None else 'MISMATCH'}")
    payload = {
        "two_connected_counts": two,
        "three_connected_counts": three,
        "published_two_connected": PUBLISHED_TWO_CONN,
        "published_three_connected": PUBLISHED_THREE_CONN,
        "timings_seconds": timings,
        "_note": (
            "'timings_seconds' is a wall-clock measurement and is the ONLY field "
            "in any results file that is expected to differ between runs on "
            "different machines; every other field reproduces exactly."
        ),
        "agreement": all(PUBLISHED_TWO_CONN.get(n, two[n]) == two[n] for n in two)
        and all(PUBLISHED_THREE_CONN.get(n, three[n]) == three[n] for n in three),
    }
    dump("cardinalities", payload)
    return payload


if __name__ == "__main__":
    import sys

    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)