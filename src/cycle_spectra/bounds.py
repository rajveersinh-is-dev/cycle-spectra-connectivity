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

``B_dominating``    ``c(G) >= 1 + (k-1) * C(n-1, 2)``  if ``G`` has a dominating
                    vertex.  Equality analysis is in the paper.

``B_order``        If ``G`` is ``k``-connected (``k >= 3``) and ``c(G) <= K``
                    then ``|V(G)| <= floor(2(K-1)/(k-2))``.
"""

from __future__ import annotations

from math import comb

from .connectivity import vertex_connectivity
from .graph import Graph

__all__ = [
    "B_fundamental",
    "B_star",
    "B_dominating",
    "B_order",
    "lower_bound",
]


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
    """Best of the elementary bounds proved in the paper (max of B_fundamental,
    B_star, B_dominating)."""
    return max(B_fundamental(g), B_star(g, k=k), B_dominating(g, k=k))