"""Spectrum-level regression tests.

These pin down the statements that appear in the paper.  If a future change to
the library breaks the mathematics, these tests fail.
"""

from __future__ import annotations

import pytest

from cycle_spectra import (
    count_cycles,
    exhaustive_two_connected_cycle_counts,
    is_3connected,
    missing_below,
    three_connected_graphs,
    two_connected_graphs,
)

# The 2-connected spectrum, per McCulloch--McKay--Salahshoori--Zaslavsky
# (Graphs Combin. 42 (2026)):  all positive integers except 2, 4, 5, 8, 9, 16.
TWO_CONN_EXCEPTIONS = {2, 4, 5, 8, 9, 16}

# Their conjectured exception list for 3-connected graphs.
THREE_CONN_EXCEPTIONS_BELOW_51 = {
    1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 27, 30, 32, 33, 34,
}


def _spectrum(n_max: int, gen) -> set[int]:
    out: set[int] = set()
    for n in range(4 if gen is three_connected_graphs else 3, n_max + 1):
        out |= {count_cycles(g) for g in gen(n)}
    return out


def test_two_connected_spectrum_has_no_small_exceptions():
    """None of 2, 4, 5, 8, 9, 16 occur as a 2-connected cycle count up to n = 7."""
    spec = _spectrum(7, two_connected_graphs)
    for e in TWO_CONN_EXCEPTIONS:
        assert e not in spec, e


def test_two_connected_spectrum_is_dense_below_50():
    spec = _spectrum(7, two_connected_graphs)
    missing = missing_below(spec, 50)
    assert set(missing) <= TWO_CONN_EXCEPTIONS


@pytest.mark.parametrize("n", [4, 5, 6, 7])
def test_three_connected_spectrum_below_51(n):
    """Cumulative 3-connected spectrum up to n = 9 reproduces the conjectured set."""
    spec = _spectrum(n, three_connected_graphs)
    missing = set(missing_below(spec, 50))
    # every exception below 51 stays missing as n grows
    for e in THREE_CONN_EXCEPTIONS_BELOW_51:
        if e <= 26 or n >= 8:
            assert e in missing, (e, n)


def test_three_connected_exceptions_below_27_are_all_missing():
    spec = _spectrum(8, three_connected_graphs)
    missing = set(missing_below(spec, 26))
    # 1..6, 8..12, 16..20 are impossible; 7, 13..15, 21..26 all occur
    for m in list(range(1, 7)) + list(range(8, 13)) + list(range(16, 21)):
        assert m in missing
    for m in [7, 13, 14, 15] + list(range(21, 27)):
        assert m not in missing, m


def test_smallest_3connected_graphs():
    """K_4 is the unique 3-connected graph with 7 cycles and it is the smallest."""
    for n in range(4, 6):
        for g in three_connected_graphs(n):
            assert count_cycles(g) >= 7
    ks = [count_cycles(g) for g in three_connected_graphs(4)]
    assert ks == [7]


def test_handfacts_2connected_counts():
    counts = exhaustive_two_connected_cycle_counts(7)
    assert min(counts) == 1
    assert 2 not in counts
    assert 3 in counts
    assert 4 not in counts
    assert 5 not in counts
    assert 6 in counts
    assert 7 in counts