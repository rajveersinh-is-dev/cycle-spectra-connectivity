"""Compute the extremal function m_3(n) and identify the minimising graphs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cycle_spectra import count_cycles, three_connected_graphs, wheel  # noqa: E402
from cycle_spectra.graph import cycle_graph  # noqa: E402


def describe(g) -> str:
    d = sorted(g.degrees(), reverse=True)
    return f"n={g.n} m={g.m} c={count_cycles(g)} degseq={d} edges={g.edge_list()}"


def main(max_n: int = 9):
    print(f"{'n':>3} {'m_3(n)':>8} {'#min':>6} {'binom':>7} {'c(W_n)':>8}  minimiser(s)")
    all_values = {}
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
        all_values[n] = sorted({count_cycles(g) for g in thc})
        print(
            f"{n:>3} {best:>8} {len(mins):>6} {(n-1)*(n-2)//2:>7} {count_cycles(wheel(n)):>8}  "
            + " | ".join(describe(g) for g in mins[:3])
        )
        # sanity: is the conjectured lower bound respected?
        assert best >= (n - 1) * (n - 2) // 2, f"bound violated at n={n}"
    print()
    # cumulative spectrum
    cum = set()
    for n in range(4, max_n + 1):
        cum |= set(all_values[n])
    print(f"cumulative 3-connected spectrum up to n={max_n}: |S|={len(cum)}, max={max(cum)}")
    print(f"values in [1,50] present: {sorted(m for m in cum if m <= 50)}")
    print(f"missing in [1,50]: {[m for m in range(1, 51) if m not in cum]}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)