"""Ad-hoc exploratory script (kept out of the package; used to sanity check).

Run from the repository root::

    python -m scripts.explore
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cycle_spectra import (  # noqa: E402
    Graph,
    count_cycles,
    count_cycles_by_length,
    complete_graph,
    cycle_graph,
    is_2connected,
    is_3connected,
    prism_graph,
    three_connected_graphs,
    total_paths,
    two_connected_graphs,
    wheel,
)
from cycle_spectra.graph import bits  # noqa: E402


def show_basic():
    print("== sanity checks ==")
    for name, g in [
        ("C_3", cycle_graph(3)),
        ("C_4", cycle_graph(4)),
        ("K_4", Graph(4, [0b1110, 0b1101, 0b1011, 0b0111])),
        ("K_5", complete_graph(5)),
        ("W_6", wheel(6)),
        ("prism(3)", prism_graph(3)),
        ("cube", prism_graph(4)),
    ]:
        print(f"{name:10s} n={g.n} m={g.m} c={count_cycles(g)} 2conn={is_2connected(g)} 3conn={is_3connected(g)}")
    print("K_5 cycle length profile:", count_cycles_by_length(complete_graph(5)))


def show_spectra(max_n: int = 8):
    print()
    print(f"== spectra up to n = {max_n} ==")
    for n in range(3, max_n + 1):
        tc = two_connected_graphs(n)
        thc = three_connected_graphs(n)
        c2 = {count_cycles(g) for g in tc}
        c3 = {count_cycles(g) for g in thc}
        s3 = f"min={min(c3)}" if c3 else "min=n/a"
        print(f"n={n}: |2conn|={len(tc):6d} |3conn|={len(thc):6d}  min c(2conn)={min(c2)}  {s3}")
        print(f"      S3(<={n}) = {sorted(c3)[:40]}")


def show_m3(max_n: int = 8):
    print()
    print("== m_3(n): min cycle count of 3-connected graphs ==")
    from cycle_spectra.graph import cycle_graph

    for n in range(4, max_n + 1):
        thc = three_connected_graphs(n)
        best = None
        mins = []
        for g in thc:
            c = count_cycles(g)
            if best is None or c < best:
                best, mins = c, [g]
            elif c == best:
                mins.append(g)
        w = wheel(n)
        print(
            f"n={n}: m_3(n)={best}  (number of minimisers={len(mins)}), "
            f"c(W_n)={count_cycles(w)}, binom(n-1,2)={(n-1)*(n-2)//2}"
        )


if __name__ == "__main__":
    show_basic()
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    show_spectra(n_max)
    show_m3(n_max)
