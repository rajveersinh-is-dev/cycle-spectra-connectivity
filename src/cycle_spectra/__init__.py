"""Cycle-count spectra of graphs of prescribed connectivity.

A small, exact computational laboratory for the mathematics in
``paper/main.tex``.  Nothing in this package uses randomness, floating point
arithmetic, or heuristics: all quantities are computed exactly and all
enumerations are proved complete by cross-validation (``scripts/validate_generators.py``).

Main objects
------------
``Graph``                 compact bitmask graph type
``count_cycles``          number of cycles of a graph
``cone_cycles``           cycle count of a cone, via the counting identity
``is_k_connected``        exact k-connectivity tests
``two_connected_graphs``  all unlabeled 2-connected graphs on n vertices
``three_connected_graphs`` all unlabeled 3-connected graphs on n vertices
``B_fundamental`` etc.    provable lower bounds on ``c(G)``
``cycle_spectrum``        group graphs by their cycle count
"""

from .graph import (
    Graph,
    complete_graph,
    cube_graph,
    cycle_graph,
    prism_graph,
    theta_graph,
    wheel,
)
from .cycles import (
    cone_cycles,
    count_cycles,
    count_cycles_by_length,
    count_paths,
    girth,
    total_paths,
)
from .connectivity import (
    is_2connected,
    is_3connected,
    is_connected,
    is_k_connected,
    vertex_connectivity,
)
from .generation import (
    canonical_form,
    canonical_vertex_order,
    connected_graphs,
    three_connected_graphs,
    two_connected_graphs,
)
from .bounds import (
    B_dominating,
    B_fundamental,
    B_order,
    B_star,
    lower_bound,
)
from .spectra import (
    Witness,
    cycle_spectrum,
    extremal_function,
    max_connectivity_realising,
    min_order_realising,
    missing_below,
    spectrum_below,
)
from .handfacts import exhaustive_two_connected_cycle_counts, is_2connected_minimal_graph

__all__ = [
    "Graph",
    "complete_graph",
    "cycle_graph",
    "wheel",
    "theta_graph",
    "prism_graph",
    "cube_graph",
    "count_cycles",
    "count_cycles_by_length",
    "count_paths",
    "total_paths",
    "cone_cycles",
    "girth",
    "is_connected",
    "is_2connected",
    "is_3connected",
    "is_k_connected",
    "vertex_connectivity",
    "canonical_form",
    "canonical_vertex_order",
    "connected_graphs",
    "two_connected_graphs",
    "three_connected_graphs",
    "B_fundamental",
    "B_star",
    "B_dominating",
    "B_order",
    "lower_bound",
    "Witness",
    "cycle_spectrum",
    "spectrum_below",
    "missing_below",
    "extremal_function",
    "min_order_realising",
    "max_connectivity_realising",
    "exhaustive_two_connected_cycle_counts",
    "is_2connected_minimal_graph",
]

__version__ = "1.0.0"