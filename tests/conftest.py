"""Shared fixtures and helpers for the test suite."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cycle_spectra import Graph  # noqa: E402
from cycle_spectra.generation import canonical_form  # noqa: E402


def to_networkx(g: Graph):
    import networkx as nx

    h = nx.Graph()
    h.add_nodes_from(range(g.n))
    h.add_edges_from(g.edge_list())
    return h


def all_graphs(n: int):
    """Every graph on ``n`` vertices, as :class:`Graph` objects."""
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(pairs)):
        adj = [0] * n
        for i, (u, v) in enumerate(pairs):
            if (mask >> i) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        yield Graph(n, adj)


def isoclasses(graphs, predicate=None):
    """Deduplicate by canonical form, optionally filtering first."""
    seen: set[int] = set()
    out = []
    for g in graphs:
        if predicate is not None and not predicate(g):
            continue
        k = canonical_form(g)
        if k not in seen:
            seen.add(k)
            out.append(g)
    return out


@pytest.fixture(scope="session")
def graphs_upto_6():
    return list(all_graphs(6))