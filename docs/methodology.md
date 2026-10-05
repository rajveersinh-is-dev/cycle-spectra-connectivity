# Methodology

How the experiments are designed, and why each design decision was made.  The
point of this file is that a reader should be able to see where a number in the
paper comes from and how hard one could try to break it.

## Principles

1. **Exactness only.**  Every quantity is computed in integer arithmetic.  There
   is no sampling, no floating point in the mathematics, no randomised hashing,
   and no probabilistic isomorphism test.  Every result file records
   `"randomness_used": false`.
2. **Completeness before speed.**  The generators use classical *complete*
   descriptions (ears; Menger) rather than heuristics, so the enumeration is
   provably exhaustive.
3. **Validate the primitive, then trust it.**  Each primitive is checked against
   an independent implementation on *all* small instances before being used at
   scale.
4. **Distinguish theorem, computation, conjecture** everywhere: in the code
   (module docstrings restate the argument), in `results/`, and in the paper.

## The primitives

### Cycle counting

Fix the smallest vertex `s` of a cycle as a pivot; enumerate simple paths from
`s` using only vertices `> s`; close the cycle whenever the path reaches a
neighbour of `s`.  Each cycle is found twice (once per direction of traversal)
and the total is halved.  Bitmask arithmetic on Python ints makes the inner
loops cheap.

*Cost:* `O(#paths of G)` bitmask operations, `O(n)` bits of working memory.
`#paths` is at most `Σ_{j≤n} C(n,j)(j-1)! = O((n-1)!)`, so the worst case is
factorial; in practice `n = 12` takes milliseconds.

*Validation.*  (i) against `networkx.simple_cycles` on **all** graphs with
`n <= 5`; (ii) against an independent brute force that enumerates
`2`-regular connected edge subsets, on all graphs with `n <= 6`; (iii) the
length profile is checked to sum to `c(G)`.

### Path counting

Same technique, with the endpoint `y` excluded from the search space and the
final edge to `y` handled by a closure test at the current endpoint.  Validated
against `networkx.all_simple_paths` on all graphs with `n <= 5`.

### Connectivity

`k`-connectivity is decided by exhaustive deletion of all sets of size `< k` with
a bitmask BFS for each; `κ(G)` searches increasing cut sizes with
`min-degree` as an upper bound.  Validated against
`networkx.node_connectivity` on all graphs with `n <= 6`.

*Pitfall found by the tests:* the first version returned `n-1` for
disconnected graphs because the cut search had no `j = 0` case; fixed by an
explicit connectivity pre-check.  Regression-tested.

### Isomorphism

Exact canonical labelling via **bliss** (through `igraph`), not colour
refinement.  This matters: 1-WL is *not* enough to certify that two graphs are
non-isomorphic, so a hash-based dedupe would silently merge or split classes.

## The generators

### 2-connected graphs

By the ear theorem (Whitney 1932, as cited by McCulloch et al.), every
2-connected graph is

* a cycle, or
* obtained from a 2-connected graph on fewer vertices by adding an ear with at
  least one fresh internal vertex, or
* obtained from a 2-connected graph on the **same** order by adding a single
  edge (which preserves 2-connectivity).

The generator implements (1) and (2) directly and then takes the closure under
(3).  *This was a real bug found by cross-validation:* the first implementation
omitted (3) and produced 2 classes of 2-connected graphs on 4 vertices instead of
3 — it was missing `K_4` altogether, because for `K_4` every ear is a single
edge.  Cardinality check against the published sequence caught it.

### 3-connected graphs

If `G` is 3-connected then `G - v` is 2-connected for every `v`, so every
3-connected graph is a 2-connected graph plus one vertex joined to a set `S` of
at least three vertices.  Two exact prunings:

* every degree-2 vertex of the parent must lie in `S` (because `δ(G) >= 3`);
  this is what makes the enumeration feasible;
* the candidate is then tested for 3-connectivity directly.

## The validation protocol

Cardinality agreement is necessary but not sufficient, so we compare **sets of
canonical labels**:

```python
brute = {canonical_form(G) for G in all_graphs(n) if is_3connected(G)}
mine  = {canonical_form(G) for G in three_connected_graphs(n)}
assert brute == mine
```

for `n <= 7` (`scripts/validate_generators.py`; `n <= 6` inside the test
suite).  The induced cycle-count spectra are compared as well, so a generator
that produced the right number of wrong classes would still fail.

## Falsification attempts

The project has a deliberate falsification layer; here is what was actually
tried and what happened.

| attempt | outcome |
|---|---|
| Does a 2-connected graph ever have exactly 2, 4, 5 cycles? | No — and the exception list `{2,4,5,8,9,16}` is proved by McCulloch et al.; our enumeration reproduces it. |
| Can `c(G) = c(K_{k+1})` happen for a non-complete `k`-connected graph? | No for all `3`-connected graphs with `n <= 9` and all connectivity levels `k = 3..8` (Theorem A, equality case). |
| Does the path lemma's *equality* statement hold for `r = 2`? | **No** — `C_4` has `p(x,y) = 2 = Q_3` for adjacent `x,y`.  Our first proof of Theorem A wrongly used the equality statement at `r = 2`; the released proof handles `k = 3` separately using `δ(G) >= 3`, and the counterexample is kept as a regression test. |
| Is the wheel the minimiser of `m_3(n)`? | **No** for `n >= 6`: the triangular prism beats `W_6` (14 vs 21), and a cubic graph beats `W_8` (26 vs 43).  Recorded in Table 2; this is why Theorem A cannot be extended order-by-order trivially. |
| Does $c(G) \ge \binom{n-1}{2}$ fail for some small 3-connected graph? | No for `n <= 9` (80 890 classes); the ratio `m_3(n)/C(n-1,2)` grows towards 2, so the conjecture is loose but not falsified. |
| Can `S_3` contain something outside the conjectured exception list below 51? | No — our independent enumeration returns exactly the conjectured list. |
| Does a 3-connected graph on 10 vertices have fewer cycles than $m_3(9) = 42$? | **Unknown**: the generator did not terminate in 50 minutes, so no value is reported. |
| Is the "witness" for `S_1` cheap to verify? | First attempt used a **chain** of triangles; it is correct but a simple path can traverse every triangle, so the path count is exponential and `count_cycles` on 25 triangles took 54 s. Replaced by a **bouquet** (all triangles sharing one vertex): a simple path then uses at most two triangles, and the same count takes 0.6 ms at 200 triangles. Caught by the test suite timing out. |

## Reproducibility

* Every result file carries a provenance block: Python version, platform,
  `numpy`/`networkx`/`igraph`/`matplotlib` versions, git commit, UTC timestamp,
  `seed: 0`, `randomness_used: false`.
* `experiments/run_all.py --max-n N` is the single entry point; the summary
  table in `results/summary.md` is generated, not transcribed.
* The tests do not depend on the experiments and the experiments do not depend
  on the figures, so any stage can be re-run in isolation.
* We verified the pipeline by deleting `results/` and `figures/` and re-running
  from a clean checkout.  Every mathematical field reproduced **bit for bit**;
  the only field that differed between the two runs was
  `timings_seconds` in `results/cardinalities.json`, which is a wall-clock
  measurement and is flagged as such inside that file.  A side-by-side diff of
  the two runs is the check we recommend repeating after any change.