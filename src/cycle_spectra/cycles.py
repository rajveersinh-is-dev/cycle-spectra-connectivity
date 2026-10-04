"""Exact counting of cycles and paths in small simple graphs.

Every routine here is *exact* (integer arithmetic only) and works with the
bitmask representation of :mod:`cycle_spectra.graph`.

Conventions
-----------
A *cycle* is a subgraph that is 2-regular and connected, i.e. it is counted
once, not twice by direction, and rotations are identified.  A *path* has two
distinct endpoints, a length of at least 1, and is likewise counted once.
"""

from __future__ import annotations

from .graph import Graph, bits

__all__ = [
    "count_cycles",
    "count_cycles_by_length",
    "count_paths",
    "total_paths",
    "cone_cycles",
    "girth",
]


def count_cycles(g: Graph) -> int:
    """Return the number of cycles of ``g``.

    Each cycle is counted exactly once.  The algorithm fixes the *smallest
    vertex* of the cycle and then enumerates simple paths from that vertex to
    a neighbour of it, restricted to larger vertex labels; each cycle is found
    twice (once per direction of traversal) and the result is divided by two.

    Complexity: ``O(#paths of G)`` bitmask operations, which is comfortably
    fast for ``n <= 12`` and adequate for ``n <= 16``.
    """
    n, adj = g.n, g.adj
    full = (1 << n) - 1
    total = 0
    for s in range(n):
        higher = full & ~((1 << (s + 1)) - 1)
        start_nbrs = adj[s] & higher
        if not start_nbrs:
            continue
        adj_s = adj[s]

        def extend(cur: int, used: int) -> int:
            cand = adj[cur] & higher & ~used
            if not cand:
                return 0
            # (a) close the cycle: a fresh neighbour of cur that sees s
            cnt = (cand & adj_s).bit_count()
            # (b) extend the path
            while cand:
                b = cand & -cand
                cand ^= b
                cnt += extend(b.bit_length() - 1, used | b)
            return cnt

        sub = 0
        while start_nbrs:
            b = start_nbrs & -start_nbrs
            start_nbrs ^= b
            sub += extend(b.bit_length() - 1, b)
        total += sub >> 1
    return total


def count_cycles_by_length(g: Graph) -> dict[int, int]:
    """Return ``{length: number of cycles of that length}``."""
    n, adj = g.n, g.adj
    full = (1 << n) - 1
    out: dict[int, int] = {}
    for s in range(n):
        higher = full & ~((1 << (s + 1)) - 1)
        start_nbrs = adj[s] & higher
        adj_s = adj[s]

        stack = [(b.bit_length() - 1, b, 1) for b in _lowbits(start_nbrs)]
        while stack:
            cur, used, depth = stack.pop()
            cand = adj[cur] & higher & ~used
            closed = cand & adj_s
            while closed:
                cb = closed & -closed
                closed ^= cb
                out[depth + 2] = out.get(depth + 2, 0) + 1
            while cand:
                b = cand & -cand
                cand ^= b
                stack.append((b.bit_length() - 1, used | b, depth + 1))
    # each cycle counted once per orientation
    return {k: v // 2 for k, v in out.items()}


def _lowbits(mask: int):
    while mask:
        b = mask & -mask
        mask ^= b
        yield b


def count_paths(g: Graph, x: int, y: int) -> int:
    """Number of simple ``x``-``y`` paths in ``g`` (requires ``x != y``).

    The path consisting of the single edge ``xy`` is included.
    """
    n, adj = g.n, g.adj
    if x == y:
        raise ValueError("endpoints must differ")
    full = (1 << n) - 1
    rest = full & ~((1 << x) | (1 << y))
    adj_y = adj[y]

    def extend(cur: int, used: int) -> int:
        # close the path at cur if cur sees y
        cnt = (adj_y >> cur) & 1
        cand = adj[cur] & rest & ~used
        while cand:
            b = cand & -cand
            cand ^= b
            cnt += extend(b.bit_length() - 1, used | b)
        return cnt

    total = (adj[y] >> x) & 1
    nbrs = adj[x] & rest
    while nbrs:
        b = nbrs & -nbrs
        nbrs ^= b
        total += extend(b.bit_length() - 1, b)
    return total


def total_paths(g: Graph) -> int:
    """Number of paths of ``g`` with two distinct endpoints.

    Equivalently ``sum_{x<y} p(x,y)`` where ``p(x,y)`` is the number of
    simple ``x``-``y`` paths.
    """
    return sum(count_paths(g, x, y) for x in range(g.n) for y in range(x + 1, g.n))


def cone_cycles(base: Graph) -> int:
    """Return ``c(K_1 v base)``, the cycle count of the cone over ``base``.

    This uses the counting identity

        c(K_1 v G) = c(G) + sum_{ {x,y} in E_pairs(G) } p_G(x,y),

    proved in the paper: the cycles of the cone that avoid the apex are the
    cycles of ``G``, and a cycle through the apex is determined by a pair of
    vertices of ``G`` together with a path between them in ``G``.
    """
    return count_cycles(base) + total_paths(base)


def girth(g: Graph) -> int:
    """Length of a shortest cycle, or ``0`` if ``g`` is acyclic."""
    by_len = count_cycles_by_length(g)
    return min(by_len) if by_len else 0