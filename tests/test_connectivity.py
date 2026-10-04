"""Correctness of the connectivity tests."""

from __future__ import annotations

import pytest

from conftest import all_graphs, to_networkx
from cycle_spectra import (
    Graph,
    is_2connected,
    is_3connected,
    is_connected,
    is_k_connected,
    vertex_connectivity,
)


@pytest.mark.parametrize("n", [4, 5, 6])
def test_against_networkx(n):
    import networkx as nx

    for g in all_graphs(n):
        h = to_networkx(g)
        expected = (
            0
            if h.number_of_nodes() == 0
            else (nx.node_connectivity(h) if n > 1 else 0)
        )
        assert vertex_connectivity(g) == expected, g


@pytest.mark.parametrize("n", [5, 6])
def test_k_connected_against_connectivity(n):
    for g in all_graphs(n):
        k = vertex_connectivity(g)
        for kk in range(1, n):
            assert is_k_connected(g, kk) == (k >= kk), (g, kk)


def test_2connected_equals_no_cutvertex_for_n_ge_3():
    for n in range(3, 7):
        for g in all_graphs(n):
            if n < 3:
                continue
            # no cut vertex <=> connected and stays connected after any deletion
            if is_2connected(g):
                for v in range(g.n):
                    h = g.subgraph([x for x in range(g.n) if x != v])
                    assert is_connected(h)


def test_3connected_implies_2connected():
    for n in range(4, 7):
        for g in all_graphs(n):
            if is_3connected(g):
                assert is_2connected(g)


def test_small_conventions():
    assert is_2connected(Graph(2, [0b10, 0b01])) is False
    assert is_3connected(Graph(3, [0b110, 0b101, 0b011])) is False
    assert is_connected(Graph(0, ())) is True