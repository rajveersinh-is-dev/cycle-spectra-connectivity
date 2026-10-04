"""Provable lower bounds on the number of cycles.

Everything in this module is accompanied by a proof in the paper; the docstrings
state the argument so that the code and the mathematics cannot drift apart.

Summary of the bounds
---------------------
``B_fundamental``   ``c(G) >= |E(G)| - |V(G)| + 1``
                    (fundamental cycles of a spanning tree are pairwise distinct).

``B_star``         ``c(G) >= c(G - v) + (k-1) * C(d(v), 2)``  for ``k``-connected
                    ``G`` with ``|V(G)| >= k+1`` and ``d(v) >= 2``.
                    (Menger: ``G - v`` is ``(k-1)``-connected, so every pair of
                    vertices of ``N(v)`` is joined by at least ``k-1`` paths in
                    ``G - v``, and each such path closes one cycle through ``v``;
                    cycles not through ``v`` number ``c(G-v) >= 1``.)

``B_star_paths``   ``c(G) >= c(K_k) + C(d(v),2) * Q_k`` where ``Q_k`` is the
                    number of paths between two vertices of ``K_k``.  Together
                    with ``d(v) >= k`` this gives Theorem A:
                    ``c(G) >= c(K_{k+1})`` for every ``k``-connected ``G``.

``B_dominating``    ``c(G) >= 1 + (k-1) * C(n-1, 2)``  if ``G`` has a dominating
                    vertex.  Equality analysis is in the paper.

``B_order``        If ``G`` is ``k``-connected (``k >= 3``) and ``c(G) <= K``
                    then ``|V(G)| <= floor(2(K-1)/(k-2))``.
"""

from __future__ import annotations

from math import comb, factorial

from .connectivity import vertex_connectivity
from .graph import Graph

__all__ = [
    "Q",
    "c_complete",
    "B_fundamental",
    "B_star",
    "B_star_paths",
    "B_dominating",
    "B_min_k_connected",
    "B_order",
    "lower_bound",
]


def Q(k: int) -> int:
    """The number ``Q_k`` of simple ``x``-``y`` paths in ``K_k`` (``x != y``).

    ``Q_k = sum_{j=0}^{k-2} C(k-2, j) j!``, and it satisfies the recurrence
    ``Q_2 = 1``, ``Q_{r+1} = 1 + (r-1) Q_r`` (verified in the tests).  ``Q_k``
    is the constant in the Path Lemma: every ``r``-connected graph has at least
    ``Q_{r+1}`` paths between any two vertices.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    return sum(comb(k - 2, j) * factorial(j) for j in range(0, k - 1))


def c_complete(n: int) -> int:
    """The number of cycles of ``K_n``: ``sum_{j>=3} C(n,j) (j-1)! / 2``."""
    return sum(comb(n, j) * factorial(j - 1) // 2 for j in range(3, n + 1))


def B_min_k_connected(k: int) -> int:
    """``min { c(G) : G is k-connected } = c(K_{k+1})`` (Theorem A)."""
    return c_complete(k + 1)


def B_fundamental(g: Graph) -> int:
    """``c(G) >= |E| - |V| + 1``: one distinct fundamental cycle per cotree edge."""
    return g.m - g.n + 1 if g.n else 0


def B_star(g: Graph, v: int | None = None, k: int | None = None) -> int:
    """``c(G) >= c(G-v) + (k-1) C(d(v),2)``; use ``v = argmax degree`` by default.

    The bound is clipped at 0 (it is vacuous for small graphs).
    """
    from .cycles import count_cycles

    n = g.n
    if v is None:
        if n == 0:
            return 0
        v = max(range(n), key=lambda x: g.degree(x))
    d = g.degree(v)
    if k is None:
        k = vertex_connectivity(g)
    rest = count_cycles(g.subgraph([x for x in range(n) if x != v]))
    val = rest + max(0, k - 1) * comb(d, 2)
    return max(val, 0)


def B_star_paths(g: Graph, v: int | None = None, k: int | None = None) -> int:
    """``c(G) >= c(K_k) + C(d(v),2) * Q_k`` for a ``k``-connected graph ``G``.

    Uses the Path Lemma (``p_{G-v}(x,y) >= Q_k`` for every pair of neighbours of
    ``v``) together with the induction hypothesis ``c(G-v) >= c(K_k)``.  With
    ``d(v) >= k`` this immediately yields ``c(G) >= c(K_{k+1})``.
    """
    from .cycles import count_cycles  # noqa: F401  (documents the recursion used)

    n = g.n
    if n < 3:
        return 0
    if v is None:
        v = max(range(n), key=lambda x: g.degree(x))
    d = g.degree(v)
    if k is None:
        k = vertex_connectivity(g)
    if k < 2:
        return 0
    return c_complete(k) + comb(d, 2) * Q(k)


def B_dominating(g: Graph, k: int | None = None) -> int:
    """``c(G) >= 1 + (k-1) C(n-1, 2)`` when ``G`` has a dominating vertex, else 0."""
    n = g.n
    if n < 3:
        return 0
    if max(g.degrees(), default=0) != n - 1:
        return 0
    if k is None:
        k = vertex_connectivity(g)
    return 1 + max(0, k - 1) * comb(n - 1, 2)


def B_order(K: int, k: int) -> int:
    """Max order of a ``k``-connected graph (``k >= 3``) having at most ``K`` cycles."""
    if k < 3 or K < 1:
        raise ValueError("need k >= 3 and K >= 1")
    return (2 * (K - 1)) // (k - 2)


def lower_bound(g: Graph, k: int | None = None) -> int:
    """Best of the elementary bounds proved in the paper."""
    return max(B_fundamental(g), B_star(g, k=k), B_dominating(g, k=k), B_star_paths(g, k=k))