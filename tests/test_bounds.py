"""The provable lower bounds, checked on every small 3-connected graph."""

from __future__ import annotations

import pytest

from cycle_spectra import (
    B_dominating,
    B_fundamental,
    B_order,
    B_star,
    count_cycles,
    is_3connected,
    lower_bound,
    three_connected_graphs,
    vertex_connectivity,
    wheel,
)


def test_theorem1_wheel_is_sharp():
    """c(W_n) = (n-1)(n-2)+1 = B_dominating(W_n) for every n >= 4."""
    for n in range(4, 15):
        w = wheel(n)
        assert B_dominating(w) == count_cycles(w) == (n - 1) * (n - 2) + 1


def test_bounds_hold_on_all_small_3connected_graphs():
    """All 3-connected graphs up to n = 7: every proved bound holds."""
    for n in range(4, 8):
        for g in three_connected_graphs(n):
            c = count_cycles(g)
            assert B_fundamental(g) <= c
            assert B_star(g, k=3) <= c
            assert B_dominating(g, k=3) <= c
            assert lower_bound(g, k=3) <= c


def test_B_star_is_attained_for_wheels():
    for n in range(4, 12):
        w = wheel(n)
        assert B_star(w) == count_cycles(w)


def test_order_bound_consistent_with_computation():
    """Every graph with <= K cycles satisfies the proved order bound."""
    for K in (10, 20, 30, 40, 50):
        bound = B_order(K, 3)
        for n in range(4, 9):
            for g in three_connected_graphs(n):
                if count_cycles(g) <= K:
                    assert n <= bound


def test_B_order_is_a_valid_necessary_condition():
    """A 3-connected graph on n vertices always has more than n/2 cycles."""
    import math

    for n in range(4, 9):
        for g in three_connected_graphs(n):
            # if c(G) <= K then n <= 2(K-1); contrapositive:
            K = count_cycles(g)
            assert not (n > 2 * (K - 1)), (n, K)


def test_conjectured_bound_holds_on_all_small_3connected_graphs():
    """Conjecture C: c(G) >= C(n-1, 2).  Verified here for n <= 7."""
    for n in range(4, 8):
        bound = (n - 1) * (n - 2) // 2
        for g in three_connected_graphs(n):
            assert count_cycles(g) >= bound, (n, g.n)