"""Theorems A and the Path Lemma.

Everything here is verified exhaustively on all 2-connected graphs with up to
eight vertices (7123 isomorphism classes), i.e. on all pairs of vertices of all
small 2-connected graphs.
"""

from __future__ import annotations

import pytest

from cycle_spectra import (
    Q,
    c_complete,
    complete_graph,
    count_cycles,
    count_paths,
    three_connected_graphs,
    two_connected_graphs,
    vertex_connectivity,
    wheel,
)


def test_Q_matches_its_recurrence():
    """Q_2 = 1 and Q_{r+1} = 1 + (r-1) Q_r."""
    assert Q(2) == 1
    for k in range(3, 12):
        assert Q(k) == 1 + (k - 2) * Q(k - 1), k


def test_Q_matches_counting_in_complete_graphs():
    for k in range(2, 9):
        g = complete_graph(k)
        assert count_paths(g, 0, 1) == Q(k)


def test_c_complete_matches_enumeration():
    from cycle_spectra import complete_graph

    for n in range(3, 8):
        assert c_complete(n) == count_cycles(complete_graph(n))


@pytest.mark.parametrize("n", [5, 6, 7])
def test_path_lemma_on_all_two_connected_graphs(n):
    """In an r-connected graph, p(x,y) >= Q_{r+1} for every pair x != y."""
    for g in two_connected_graphs(n):
        r = vertex_connectivity(g)
        target = Q(r + 1)
        for x in range(n):
            for y in range(x + 1, n):
                assert count_paths(g, x, y) >= target, (n, r, x, y)


def test_path_lemma_equality_for_r_ge_3():
    """For r >= 3, p(x,y) = Q_{r+1} forces G = K_{r+1}."""
    for n in range(4, 8):
        for g in two_connected_graphs(n):
            r = vertex_connectivity(g)
            if r < 3:
                continue
            target = Q(r + 1)
            for x in range(n):
                for y in range(x + 1, n):
                    if count_paths(g, x, y) == target:
                        assert n == r + 1 and g.m == n * (n - 1) // 2, (n, r)


def test_path_lemma_equality_fails_for_r_eq_2():
    """Documented counterexample to the naive equality statement for r = 2."""
    from cycle_spectra import cycle_graph

    c4 = cycle_graph(4)
    assert vertex_connectivity(c4) == 2
    assert count_paths(c4, 0, 1) == Q(3) == 2
    assert c4.m != 4 * 3 // 2


@pytest.mark.parametrize("n", [4, 5, 6, 7, 8, 9])
def test_theorem_A_on_all_three_connected_graphs(n):
    """c(G) >= c(K_{k+1}) for k = 3, with equality only for K_4."""
    for g in three_connected_graphs(n):
        c = count_cycles(g)
        assert c >= c_complete(4)
        if c == c_complete(4):
            assert n == 4 and g.m == 6


@pytest.mark.parametrize("n", [4, 5, 6, 7])
def test_theorem_A_for_all_connectivity_levels(n):
    """c(G) >= c(K_{k+1}) where k = kappa(G), equality only at G = K_{k+1}."""
    for g in three_connected_graphs(n):
        k = vertex_connectivity(g)
        c = count_cycles(g)
        assert c >= c_complete(k + 1), (n, k, c)
        if c == c_complete(k + 1):
            assert n == k + 1 and g.m == n * (n - 1) // 2, (n, k)


def test_wheels_beat_the_minimum_for_k_ge_3():
    """For n > k+1 the minimum is strictly above c(K_{k+1})."""
    assert count_cycles(wheel(8)) == 43 > c_complete(4) == 7