"""Cycle-count spectra: which integers occur, and with which witnesses.

Definitions used throughout
---------------------------
For a finite simple graph ``G`` let ``c(G)`` be the number of cycles of ``G``
(2-regular connected subgraphs, each counted once).  For ``k >= 1`` put

    ``S_k``   = { c(G) : G is a finite simple k-connected graph }

and call ``S_k`` the *cycle-count spectrum of k-connected graphs*.  Note that
``S_2 superset S_3 superset S_4 ...``, since higher connectivity is a stronger
requirement.  Two derived functions are of independent interest:

    ``mu(m) = min { |V(G)| : c(G) = m }``      least order realising a cycle count
    ``kap(m) = max { kappa(G) : c(G) = m }``    greatest connectivity realising it
"""

from __future__ import annotations

from dataclasses import dataclass

from .connectivity import vertex_connectivity
from .cycles import count_cycles
from .graph import Graph

__all__ = [
    "Witness",
    "cycle_spectrum",
    "spectrum_below",
    "missing_below",
    "extremal_function",
    "min_order_realising",
    "max_connectivity_realising",
]


@dataclass(frozen=True)
class Witness:
    """A graph realising a given cycle count, with its connectivity."""

    value: int
    graph: Graph
    connectivity: int

    @property
    def n(self) -> int:
        return self.graph.n

    @property
    def degree_sequence(self) -> tuple[int, ...]:
        return tuple(sorted(self.graph.degrees(), reverse=True))

    def to_json(self) -> dict:
        return {
            "cycles": self.value,
            "order": self.n,
            "edges": self.graph.m,
            "connectivity": self.connectivity,
            "degree_sequence": list(self.degree_sequence),
            "edges_list": [list(e) for e in self.graph.edge_list()],
        }


def cycle_spectrum(graphs: list[Graph]) -> dict[int, list[Graph]]:
    """Group ``graphs`` by cycle count."""
    out: dict[int, list[Graph]] = {}
    for g in graphs:
        out.setdefault(count_cycles(g), []).append(g)
    return dict(sorted(out.items()))


def spectrum_below(spec: dict[int, list[Graph]], bound: int) -> set[int]:
    """The values of ``spec`` that are at most ``bound``."""
    return {v for v in spec if v <= bound}


def missing_below(values: set[int], bound: int) -> list[int]:
    """Integers in ``[1, bound]`` that are *not* in ``values``."""
    return [m for m in range(1, bound + 1) if m not in values]


def extremal_function(graphs: list[Graph]) -> tuple[int, list[Graph]]:
    """``(m, minimisers)`` for the given family of graphs."""
    best: int | None = None
    mins: list[Graph] = []
    for g in graphs:
        c = count_cycles(g)
        if best is None or c < best:
            best, mins = c, [g]
        elif c == best:
            mins.append(g)
    assert best is not None
    return best, mins


def min_order_realising(spec: dict[int, list[Graph]]) -> dict[int, Witness]:
    """``mu``: for each realised cycle count, a witness of minimum order."""
    out: dict[int, Witness] = {}
    for value, gs in spec.items():
        g = min(gs, key=lambda x: x.n)
        out[value] = Witness(value, g, vertex_connectivity(g))
    return out


def max_connectivity_realising(spec: dict[int, list[Graph]]) -> dict[int, Witness]:
    """``kap``: for each realised cycle count, a witness of maximum connectivity."""
    out: dict[int, Witness] = {}
    for value, gs in spec.items():
        g = max(gs, key=vertex_connectivity)
        out[value] = Witness(value, g, vertex_connectivity(g))
    return out