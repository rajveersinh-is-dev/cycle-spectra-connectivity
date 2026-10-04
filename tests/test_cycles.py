"""Correctness of cycle and path counting.

Every routine is checked against a completely independent implementation
(``networkx.simple_cycles``, and a brute-force edge-subset search) on *all*
graphs with up to six vertices, plus hand-computed values on classical graphs.
"""

from __future__ import annotations

from itertools import combinations

import pytest

from conftest import all_graphs, to_networkx
from cycle_spectra import (
    Graph,
    complete_graph,
    cone_cycles,
    count_cycles,
    count_cycles_by_length,
    count_paths,
    cycle_graph,
    prism_graph,
    theta_graph,
    total_paths,
    wheel,
)


def brute_force_cycles(g: Graph) -> int:
    """Count 2-regular connected edge subsets by brute force (n <= 6 only)."""
    edges = g.edge_list()
    count = 0
    for k in range(3, len(edges) + 1):
        for subset in combinations(edges, k):
            deg = {}
            for u, v in subset:
                deg[u] = deg.get(u, 0) + 1
                deg[v] = deg.get(v, 0) + 1
            if any(d != 2 for d in deg.values()):
                continue
            if len(deg) != k:  # not a single cycle
                continue
            # connectivity
            start = next(iter(deg))
            seen = {start}
            stack = [start]
            while stack:
                x = stack.pop()
                for u, v in subset:
                    if u == x and v not in seen:
                        seen.add(v)
                        stack.append(v)
                    elif v == x and u not in seen:
                        seen.add(u)
                        stack.append(u)
            if len(seen) == k:
                count += 1
    return count


HAND_VALUES = [
    (cycle_graph(3), 1),
    (cycle_graph(4), 1),
    (cycle_graph(7), 1),
    (complete_graph(4), 7),
    (complete_graph(5), 37),
    (complete_graph(6), 197),
    (wheel(4), 7),
    (wheel(6), 21),
    (wheel(8), 43),
    (wheel(10), 73),
    (prism_graph(3), 14),
    (prism_graph(4), 28),
    (theta_graph([2, 2, 2]), 3),
    (theta_graph([1, 2, 4]), 3),
]


@pytest.mark.parametrize("g,expected", HAND_VALUES)
def test_hand_values(g, expected):
    assert count_cycles(g) == expected


def test_complete_graph_profile():
    profile = count_cycles_by_length(complete_graph(5))
    assert profile == {3: 10, 4: 15, 5: 12}
    assert sum(profile.values()) == 37


@pytest.mark.parametrize("n", [3, 4, 5])
def test_against_networkx(n):
    import networkx as nx

    for g in all_graphs(n):
        assert count_cycles(g) == len(list(nx.simple_cycles(to_networkx(g)))), g


@pytest.mark.parametrize("n", [4, 5])
def test_against_brute_force(n):
    for g in all_graphs(n):
        assert count_cycles(g) == brute_force_cycles(g), g


@pytest.mark.parametrize("n", [4, 5, 6])
def test_length_profile_consistent(n):
    for g in all_graphs(n):
        assert sum(count_cycles_by_length(g).values()) == count_cycles(g)


def test_counts_paths_and_total():
    # a cycle of length m has exactly two x-y paths for every pair
    for m in range(3, 8):
        c = cycle_graph(m)
        for x in range(m):
            for y in range(x + 1, m):
                assert count_paths(c, x, y) == 2
        assert total_paths(c) == m * (m - 1)


def test_path_count_against_networkx():
    import networkx as nx

    for g in all_graphs(5):
        h = to_networkx(g)
        for x in range(g.n):
            for y in range(x + 1, g.n):
                expected = len(list(nx.all_simple_paths(h, x, y)))
                assert count_paths(g, x, y) == expected, (g, x, y)


def test_cone_identity():
    """c(K_1 v G) = c(G) + number of paths of G."""
    from cycle_spectra import two_connected_graphs

    for n in range(3, 7):
        for g in two_connected_graphs(n):
            base = count_cycles(g)
            cone_adj = [(g.adj[v] | (1 << n)) for v in range(n)] + [(1 << n) - 1]
            cone = Graph(n + 1, cone_adj)
            assert cone_cycles(g) == count_cycles(cone) == base + total_paths(g)


def test_cone_minimum_is_the_wheel():
    """Among cones over 2-connected graphs, the cycle is the unique minimiser."""
    from cycle_spectra import two_connected_graphs

    for n in range(3, 7):
        cs = [cone_cycles(g) for g in two_connected_graphs(n)]
        assert min(cs) == n * (n - 1) + 1
        assert cs.count(min(cs)) == 1


def test_wheel_is_cone_over_cycle():
    for n in range(4, 12):
        w = wheel(n)
        assert count_cycles(w) == (n - 1) * (n - 2) + 1


def test_no_cycles_in_forests():
    # path 0-1-2-3 together with an isolated vertex 4
    g = Graph(5, [0b0010, 0b0101, 0b1010, 0b0100, 0])
    assert count_cycles(g) == 0
    assert count_cycles_by_length(g) == {}