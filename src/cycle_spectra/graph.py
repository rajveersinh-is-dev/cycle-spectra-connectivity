"""A compact graph type based on adjacency bitmasks.

All algorithms in this package work with simple graphs on the vertex set
``{0, 1, ..., n-1}``.  A graph is represented by an ``n x n`` adjacency
relationship given by a tuple of ``n`` Python integers, each of which is the
bitmask of the neighbourhood of the corresponding vertex.  This makes the hot
loops (cycle enumeration, connectivity tests) pure integer arithmetic.
"""

from __future__ import annotations

from typing import Iterable, Sequence

__all__ = [
    "Graph",
    "complete_graph",
    "wheel",
    "cycle_graph",
    "theta_graph",
    "prism_graph",
    "cube_graph",
]


class Graph:
    """An immutable simple graph stored as adjacency bitmasks.

    Attributes
    ----------
    n:
        number of vertices; the vertex set is ``range(n)``.
    adj:
        tuple of ``n`` integers; ``adj[v]`` is the bitmask of ``N(v)``.
    """

    __slots__ = ("n", "adj")

    def __init__(self, n: int, adj: Sequence[int]):
        if n < 0:
            raise ValueError("n must be non-negative")
        adj = tuple(int(a) for a in adj)
        if len(adj) != n:
            raise ValueError("adj must have length n")
        full = (1 << n) - 1
        for v, a in enumerate(adj):
            if a < 0 or a > full:
                raise ValueError("adjacency out of range")
            if (a >> v) & 1:
                raise ValueError("loops are not allowed")
            # symmetry
            for u in range(n):
                if (a >> u) & 1 and not ((adj[u] >> v) & 1):
                    raise ValueError("adjacency is not symmetric")
        object.__setattr__(self, "n", n)
        object.__setattr__(self, "adj", adj)

    # -- basic accessors -------------------------------------------------
    def neighbours(self, v: int) -> list[int]:
        return bits(self.adj[v])

    def degree(self, v: int) -> int:
        return self.adj[v].bit_count()

    def degrees(self) -> list[int]:
        return [a.bit_count() for a in self.adj]

    @property
    def m(self) -> int:
        """Number of edges."""
        return sum(self.degrees()) // 2

    @property
    def max_degree(self) -> int:
        return max((a.bit_count() for a in self.adj), default=0)

    @property
    def min_degree(self) -> int:
        return min((a.bit_count() for a in self.adj), default=0)

    def edge_count_between(self, nbrs: int) -> int:
        """Number of edges inside the vertex set given by bitmask ``nbrs``."""
        cnt = 0
        for v in bits(nbrs):
            cnt += (self.adj[v] & nbrs).bit_count()
        return cnt // 2

    def is_adjacent(self, u: int, v: int) -> bool:
        return bool((self.adj[u] >> v) & 1)

    def edge_list(self) -> list[tuple[int, int]]:
        out = []
        for u in range(self.n):
            for v in bits(self.adj[u]):
                if u < v:
                    out.append((u, v))
        return out

    def subgraph(self, verts: Iterable[int]) -> "Graph":
        """Induced subgraph on ``verts`` (relabelled to ``range(len(verts))``)."""
        idx = list(verts)
        pos = {v: i for i, v in enumerate(idx)}
        adj = []
        for v in idx:
            mask = 0
            for w in bits(self.adj[v]):
                if w in pos:
                    mask |= 1 << pos[w]
            adj.append(mask)
        return Graph(len(idx), adj)

    def with_vertex(self, nbrs: int) -> "Graph":
        """Add a new (last) vertex whose neighbourhood is given by ``nbrs``."""
        if nbrs >> self.n:
            raise ValueError("nbrs out of range")
        return Graph(self.n + 1, self.adj + (nbrs,))

    # -- dunder ----------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"Graph(n={self.n}, m={self.m}, adj={list(self.adj)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph):
            return NotImplemented
        return self.n == other.n and self.adj == other.adj

    def __hash__(self) -> int:
        return hash((self.n, self.adj))


def bits(mask: int) -> list[int]:
    """Indices of the set bits of ``mask``, in increasing order."""
    out = []
    while mask:
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out


# ---------------------------------------------------------------- factories
def complete_graph(n: int) -> Graph:
    """The complete graph ``K_n``."""
    full = (1 << n) - 1
    return Graph(n, [full & ~(1 << v) for v in range(n)])


def cycle_graph(n: int) -> Graph:
    """The cycle ``C_n`` (``n >= 3``)."""
    if n < 3:
        raise ValueError("cycles need n >= 3")
    adj = [0] * n
    for v in range(n):
        adj[v] = (1 << ((v - 1) % n)) | (1 << ((v + 1) % n))
    return Graph(n, adj)


def wheel(n: int) -> Graph:
    """The wheel on ``n`` vertices: a cycle ``C_{n-1}`` plus a hub (``n >= 4``)."""
    if n < 4:
        raise ValueError("wheels need n >= 4")
    rim = cycle_graph(n - 1)
    hub = 1 << (n - 1)
    adj = list(rim.adj) + [hub - 1]
    for v in range(n - 1):
        adj[v] |= hub
    return Graph(n, adj)


def theta_graph(paths: Sequence[int]) -> Graph:
    """The multigraph theta with internally disjoint ``u``-``v`` paths of the
    given lengths.  Vertex 0 is ``u``, vertex 1 is ``v``.

    Simple graphs are obtained iff no two lengths are 1 and at most one length
    equals 1 (paths of length 1 create parallel edges).
    """
    if len(paths) < 2:
        raise ValueError("need at least two paths")
    adj: list[int] = [0, 0]
    for L in paths:
        prev = 0
        for _ in range(L - 1):
            adj.append(0)
            nxt = len(adj) - 1
            adj[prev] |= 1 << nxt
            adj[nxt] |= 1 << prev
            prev = nxt
        adj[prev] |= 1 << 1
        adj[1] |= 1 << prev
    return Graph(len(adj), adj)


def prism_graph(k: int) -> Graph:
    """The ``k``-prism ``C_k x K_2`` (``k >= 3``)."""
    if k < 3:
        raise ValueError("prisms need k >= 3")
    n = 2 * k
    adj = [0] * n
    for i in range(k):
        adj[i] |= (1 << ((i + 1) % k)) | (1 << ((i - 1) % k)) | (1 << (i + k))
        adj[i + k] |= (1 << (((i + 1) % k) + k)) | (1 << (((i - 1) % k) + k)) | (1 << i)
    return Graph(n, adj)


def cube_graph() -> Graph:
    """The cube graph ``Q_3``."""
    return prism_graph(4)