"""Vertex connectivity tests for small graphs.

A graph is ``k``-connected (``|V| > k``) if deleting any set of fewer than ``k``
vertices leaves a connected graph.  The tests below are brute force but exact;
for the graph sizes of interest (n <= 12) this is both fast and completely
transparent, which matters more here than asymptotics.
"""

from __future__ import annotations

from itertools import combinations

from .graph import Graph, bits

__all__ = [
    "is_connected",
    "is_2connected",
    "is_3connected",
    "is_k_connected",
    "vertex_connectivity",
]


def _connected_after_deletion(g: Graph, deleted: int, must_be_nonempty: bool) -> bool:
    """Is ``g - deleted`` connected?  ``deleted`` is a vertex bitmask."""
    n = g.n
    alive = ((1 << n) - 1) & ~deleted
    if not alive:
        return not must_be_nonempty
    start = alive & -alive
    seen = start
    frontier = start
    while frontier:
        nxt = 0
        f = frontier
        while f:
            b = f & -f
            f ^= b
            nxt |= g.adj[b.bit_length() - 1]
        frontier = nxt & alive & ~seen
        seen |= frontier
    return seen == alive


def is_connected(g: Graph) -> bool:
    """Connectivity of ``g`` (the graph ``K_1`` and the empty graph are
    connected by convention)."""
    if g.n == 0:
        return True
    return _connected_after_deletion(g, 0, must_be_nonempty=True)


def is_k_connected(g: Graph, k: int) -> bool:
    """``k``-connectivity in the standard sense (``|V| > k`` required)."""
    if g.n <= k:
        return False
    n = g.n
    for j in range(k):
        for S in combinations(range(n), j):
            if not _connected_after_deletion(g, sum(1 << v for v in S), must_be_nonempty=True):
                return False
    return True


def is_2connected(g: Graph) -> bool:
    """2-connectivity.  For loop-free graphs with more than two vertices this
    is equivalent to having no cut vertex (Whitney's 'non-separable')."""
    if g.n < 3:
        return False
    return is_k_connected(g, 2)


def is_3connected(g: Graph) -> bool:
    """3-connectivity."""
    if g.n < 4:
        return False
    return is_k_connected(g, 3)


def vertex_connectivity(g: Graph) -> int:
    """Exact vertex connectivity ``kappa(G)`` of a simple graph.

    ``kappa(K_n) = n-1`` by convention; otherwise ``kappa`` is the size of a
    smallest vertex cut, computed here by exhaustive search.
    """
    n = g.n
    if n == 0:
        return 0
    if n == 1:
        return 0
    if g.m == n * (n - 1) // 2:
        return n - 1
    if not is_connected(g):
        return 0
    # upper bound: minimum degree
    ub = min(g.min_degree, n - 1)
    for j in range(1, ub + 1):
        for S in combinations(range(n), j):
            if not _connected_after_deletion(g, sum(1 << v for v in S), must_be_nonempty=True):
                return j
    return n - 1