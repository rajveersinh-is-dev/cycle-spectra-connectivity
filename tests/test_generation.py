"""The generators must be complete and must not invent isomorphism classes.

The counts below are the published cardinalities of the unlabeled 2-connected
and 3-connected graphs (sequences A002218 and the 3-connected analogue).  The
stronger claim -- that the generators produce exactly the right *sets* -- is
checked against exhaustive brute force for n <= 7 by
``scripts/validate_generators.py`` and, for n <= 6, by the test below.
"""

from __future__ import annotations

import pytest

from conftest import all_graphs, isoclasses
from cycle_spectra import (
    count_cycles,
    is_2connected,
    is_3connected,
    three_connected_graphs,
    two_connected_graphs,
)
from cycle_spectra.generation import canonical_form

TWO_CONN_COUNTS = {3: 1, 4: 3, 5: 10, 6: 56, 7: 468}
THREE_CONN_COUNTS = {4: 1, 5: 3, 6: 17, 7: 136}


@pytest.mark.parametrize("n,expected", sorted(TWO_CONN_COUNTS.items()))
def test_two_connected_cardinality(n, expected):
    assert len(two_connected_graphs(n)) == expected


@pytest.mark.parametrize("n,expected", sorted(THREE_CONN_COUNTS.items()))
def test_three_connected_cardinality(n, expected):
    assert len(three_connected_graphs(n)) == expected


@pytest.mark.parametrize("n", [4, 5, 6])
def test_two_connected_matches_brute_force(n):
    brute = isoclasses(all_graphs(n), is_2connected)
    gen = two_connected_graphs(n)
    assert {canonical_form(g) for g in brute} == {canonical_form(g) for g in gen}


@pytest.mark.parametrize("n", [4, 5, 6])
def test_three_connected_matches_brute_force(n):
    brute = isoclasses(all_graphs(n), is_3connected)
    gen = three_connected_graphs(n)
    assert {canonical_form(g) for g in brute} == {canonical_form(g) for g in gen}


@pytest.mark.parametrize("n", [4, 5, 6])
def test_spectra_match_brute_force(n):
    for pred, gen in ((is_2connected, two_connected_graphs), (is_3connected, three_connected_graphs)):
        b = {count_cycles(g) for g in isoclasses(all_graphs(n), pred)}
        s = {count_cycles(g) for g in gen(n)}
        assert b == s


def test_generated_graphs_have_the_advertised_connectivity():
    for n in range(4, 8):
        for g in three_connected_graphs(n):
            assert is_3connected(g)
    for n in range(3, 8):
        for g in two_connected_graphs(n):
            assert is_2connected(g)