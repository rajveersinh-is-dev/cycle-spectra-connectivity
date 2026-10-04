"""Generation of the unlabeled 2-connected and 3-connected graphs of small order.

Why these particular constructions
----------------------------------
*   **2-connected graphs.**  By the classical ear theorem, every 2-connected
    graph is a cycle, or is obtained from a 2-connected graph on fewer vertices
    by adding an *ear* (a path whose endpoints lie in the old graph and whose
    internal vertices are new), or from a 2-connected graph on the same number
    of vertices by adding a single edge.  The last case is handled by closing
    the set under adding edges, which is legitimate because adding an edge to a
    2-connected graph leaves it 2-connected.  The generator is therefore
    *complete*.

*   **3-connected graphs.**  If ``G`` is 3-connected then ``G - v`` is
    2-connected for every vertex ``v`` (Menger).  Hence every 3-connected graph
    is obtained by adding one vertex to a 2-connected graph on one vertex
    fewer, joined to some set ``S`` of at least three vertices.  Moreover
    ``S`` must contain every degree-2 vertex of the parent (since
    ``delta(G) >= 3``), which is used as a cheap and exact pruning rule.
    Again the generator is complete.

Isomorphism is decided with an exact canonical labelling (``igraph``/bliss);
nothing here relies on heuristics such as colour refinement, which would not be
sufficient for correctness.
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

from .graph import Graph, cycle_graph

__all__ = [
    "canonical_form",
    "canonical_vertex_order",
    "connected_graphs",
    "two_connected_graphs",
    "three_connected_graphs",
]

_TWO_CACHE: dict[int, list[Graph]] = {}
_THREE_CACHE: dict[int, list[Graph]] = {}
_CONN_CACHE: dict[int, list[Graph]] = {}


def _igraph(g: Graph):
    import igraph as ig

    return ig.Graph(g.n, g.edge_list())


def canonical_vertex_order(g: Graph) -> tuple[int, ...]:
    """A vertex order putting ``g`` into a canonical form (isomorphism invariant)."""
    perm = _igraph(g).canonical_permutation()
    return tuple(int(x) for x in perm)


def canonical_form(g: Graph) -> int:
    """An isomorphism-invariant integer key for ``g``."""
    perm = canonical_vertex_order(g)
    pos = [0] * g.n
    for i, v in enumerate(perm):
        pos[v] = i
    key = 0
    for u, v in g.edge_list():
        a, b = pos[u], pos[v]
        if a > b:
            a, b = b, a
        key |= 1 << (a * g.n + b)
    return key


def _dedupe(cands: Iterable[Graph]) -> list[Graph]:
    seen: set[int] = set()
    out: list[Graph] = []
    for g in cands:
        k = canonical_form(g)
        if k not in seen:
            seen.add(k)
            out.append(g)
    out.sort(key=canonical_form)
    return out


# ---------------------------------------------------------------- 2-connected
def _add_ear(h: Graph, u: int, v: int, k: int) -> Graph:
    """Extend ``h`` by an ear ``u - x_1 - ... - x_k - v`` (``k`` fresh vertices)."""
    adj = list(h.adj)
    prev = u
    for _ in range(k):
        adj.append(0)
        nxt = len(adj) - 1
        adj[prev] |= 1 << nxt
        adj[nxt] |= 1 << prev
        prev = nxt
    adj[prev] |= 1 << v
    adj[v] |= 1 << prev
    return Graph(len(adj), adj)


def two_connected_graphs(n: int) -> list[Graph]:
    """All unlabeled 2-connected graphs on ``n`` vertices (isomorphism classes).

    Known cardinalities (OEIS A002218 shifted): 1, 3, 10, 56, 468, 7123, 194066
    for ``n = 3, 4, ..., 9``.
    """
    if n in _TWO_CACHE:
        return _TWO_CACHE[n]
    if n < 3:
        _TWO_CACHE[n] = []
        return _TWO_CACHE[n]

    # stage 1: cycles, and ears with at least one fresh vertex
    cands: list[Graph] = [cycle_graph(n)]
    for j in range(3, n):
        for h in two_connected_graphs(j):
            k = n - j
            for u in range(h.n):
                for v in range(u + 1, h.n):
                    cands.append(_add_ear(h, u, v, k))
    base = _dedupe(cands)

    # stage 2: close under adding a single edge
    store: dict[int, Graph] = {canonical_form(g): g for g in base}
    frontier = list(base)
    while frontier:
        nxt: list[Graph] = []
        for g in frontier:
            have = 0
            for u, v in g.edge_list():
                have |= 1 << (u * g.n + v)
            all_pairs = 0
            for u in range(g.n):
                for v in range(u + 1, g.n):
                    all_pairs |= 1 << (u * g.n + v)
            missing = all_pairs & ~have
            while missing:
                b = missing & -missing
                missing ^= b
                i, j = divmod(b.bit_length() - 1, g.n)
                adj = list(g.adj)
                adj[i] |= 1 << j
                adj[j] |= 1 << i
                h = Graph(g.n, adj)
                k = canonical_form(h)
                if k not in store:
                    store[k] = h
                    nxt.append(h)
        frontier = nxt
    res = sorted(store.values(), key=canonical_form)
    _TWO_CACHE[n] = res
    return res


# --------------------------------------------------------------- 3-connected
def _is_3connected(h: Graph, s: int) -> bool:
    """Is ``h`` plus a fresh vertex adjacent to ``s`` 3-connected?"""
    n = h.n + 1
    newbit = 1 << h.n
    adj = [(h.adj[v] | newbit) if (s >> v) & 1 else h.adj[v] for v in range(h.n)] + [s]
    full = (1 << n) - 1

    def connected(deleted: int) -> bool:
        alive = full & ~deleted
        start = alive & -alive
        seen = start
        frontier = start
        while frontier:
            nxt = 0
            f = frontier
            while f:
                b = f & -f
                f ^= b
                u = b.bit_length() - 1
                nxt |= adj[u]
            frontier = nxt & alive & ~seen
            seen |= frontier
        return seen == alive

    for x in range(n):
        if not connected(1 << x):
            return False
    for x in range(n):
        for y in range(x + 1, n):
            if not connected((1 << x) | (1 << y)):
                return False
    return True


def three_connected_graphs(n: int) -> list[Graph]:
    """All unlabeled 3-connected graphs on ``n`` vertices (isomorphism classes).

    Known cardinalities for ``n = 4, 5, 6, 7, 8, 9``: 1, 3, 19, 136, 1555, 21887.
    """
    if n in _THREE_CACHE:
        return _THREE_CACHE[n]
    if n < 4:
        _THREE_CACHE[n] = []
        return _THREE_CACHE[n]
    cands: list[Graph] = []
    for h in two_connected_graphs(n - 1):
        forced = 0
        for x in range(h.n):
            if h.degree(x) == 2:
                forced |= 1 << x
        free = [x for x in range(h.n) if not ((forced >> x) & 1)]
        for extra in range(0, len(free) + 1):
            for comb in combinations(free, extra):
                mask = forced
                for x in comb:
                    mask |= 1 << x
                if bin(mask).count("1") < 3:
                    continue
                if _is_3connected(h, mask):
                    newbit = 1 << h.n
                    adj = [
                        (h.adj[v] | newbit) if (mask >> v) & 1 else h.adj[v]
                        for v in range(h.n)
                    ] + [mask]
                    cands.append(Graph(n, adj))
    res = _dedupe(cands)
    _THREE_CACHE[n] = res
    return res


# ----------------------------------------------------------------- connected
def connected_graphs(n: int) -> list[Graph]:
    """All unlabeled connected graphs on ``n`` vertices."""
    if n in _CONN_CACHE:
        return _CONN_CACHE[n]
    if n == 0:
        _CONN_CACHE[n] = [Graph(0, ())]
        return _CONN_CACHE[n]
    cands: list[Graph] = []
    for j in range(n - 1, 0, -1):
        for h in connected_graphs(j):
            for s in range(1, j + 1):
                for comb in combinations(range(j), s):
                    mask = sum(1 << v for v in comb)
                    cands.append(h.with_vertex(mask))
    res = _dedupe(cands)
    _CONN_CACHE[n] = res
    return res