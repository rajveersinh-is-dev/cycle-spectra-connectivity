# Cycle Counts of $k$-Connected Graphs

How many cycles must a highly connected graph have?  This repository answers
that question sharply, proves that the cycle-count spectrum of every
connectivity class is computable, and computes the extremal function and the
spectrum for 3-connected graphs exactly up to order 9.

**Author: Rajveersinh Pardeshi.**  *Paper:* [`paper/main.tex`](paper/main.tex)
(compiled PDF: [`paper/main.pdf`](paper/main.pdf)) · *Headline result:* Theorem A
below.

---

## Research Question

For which positive integers $m$ does there exist a $k$-vertex-connected graph
with **exactly $m$ cycles**, and how sparse can the cycle structure of a highly
connected graph be?

Writing $c(G)$ for the number of cycles of $G$ (each cycle a 2-regular
connected spanning subgraph, counted once) and
$$S_k=\{c(G): G \text{ is } k\text{-connected}\},$$
we study the decreasing chain $S_1\supseteq S_2\supseteq S_3\supseteq\cdots$,
the extremal function $m_k(n)=\min\{c(G): G\ k\text{-connected},\ |V(G)|=n\}$,
and the order in which data about $c$ forces cycles to exist.

## Main Result

> **Theorem A (sharp minimum).**  For every $k\ge 3$ and every $k$-connected
> graph $G$,
> $$c(G)\ \ge\ c(K_{k+1})\ =\ \tfrac12\sum_{j=3}^{k+1}\binom{k+1}{j}(j-1)!,$$
> with equality **iff** $G\cong K_{k+1}$.  For $k=2$ the minimum is $c(K_3)=1$,
> attained exactly by the cycles.

Complete graphs are the sparsest highly connected graphs.  For $k=3$ this
recovers "no 3-connected graph has fewer than $7$ cycles", the sharp general
statement being $7,37,197,1172,8018,62814$ for $k=3,\dots,8$.

The key tool is a sharp path-counting lemma.  With
$Q_k=$ the number of paths between two vertices of $K_k$ and
$Q_{k}=Q_2=1,\;Q_{r+1}=1+(r-1)Q_r$:

> **Lemma (path lemma).**  If $F$ is $r$-connected and $x\ne y\in V(F)$ then
> $p_F(x,y)\ge Q_{r+1}$; for $r\ge3$ equality forces $F\cong K_{r+1}$.

## Why This Is Interesting

* **It is a clean dichotomy.**  Everything about the *minimum* number of cycles
  in a connectivity class is decided by the order: the smallest possible graph
  wins.  Nothing is left to optimise.
* **The constant is factorial.**  $Q_k$ grows like $k!$, so the number of
  cycles in a $k$-connected graph is at least factorial in $k$ — a far stronger
  statement than the linear or quadratic bounds obtainable from degree
  arguments.
* **It explains the cone.**  Every $k$-connected graph becomes $(k+1)$-connected
  by adding a universal vertex, so wheels are "the 3-connected analogues of
  cycles" (Carmesin–Kurkofka).  Theorem B below makes that quantitative.
* **It makes the spectra computable.**  Theorem C turns "$m\in S_k$?" into a
  finite search for every $k\ge3$ — a statement that is *false* for $k\le2$,
  where infinitely many $2$-connected graphs share the cycle count 1.

## Mathematical Contribution

| # | Result | Statement | Status |
|---|--------|-----------|--------|
| A | Sharp minimum | $\min\{c(G): G\ k\text{-conn}\}=c(K_{k+1})$, equality only at $K_{k+1}$ ($k\ge3$) | **theorem, proved** |
| A′ | Recurrence | $Q_{k}=1,\;Q_{r+1}=1+(r-1)Q_r$ | **theorem, proved** |
| B | Cone minimum | $c(K_1\vee F)\ge m(m-1)+1$ for 2-connected $F$ on $m$ vertices, equality iff $F\cong C_m$ | **theorem, proved** |
| B′ | Dominating vertex | $c(G)\ge 1+(k-1)\binom{n-1}{2}$, equality only for $k=3$, $G=W_n$ | **theorem, proved** |
| C | Finiteness | 3-connected $G$ with $c(G)\le K$ has $|V(G)|\le\lfloor 2(K-1)/(k-2)\rfloor$ | **theorem, proved** |
| C′ | Decidability | each $S_k$ ($k\ge3$) is computable; $\min S_k=c(K_{k+1})$; $\kappa(m)=O(m^{1/3})$ | **corollary** |
| D | Extremal function | $m_3(4..9)=7,13,14,24,26,42$ with minimisers | **exact computation** |
| D′ | Spectra | $S_2$ misses $\{2,4,5,8,9,16\}$; $S_3$ misses exactly the 21 integers conjectured by McCulloch et al. below 51 | **exact computation** |
| — | Sharp order bound | $c(G)\ge\binom{n-1}{2}$ for 3-connected $G$ on $n\ge4$ | **conjecture**, verified $n\le9$ |

### The counting identity everything rests on

For any vertex $v$ of $G$ with $F=G-v$,
$$c(G)=c(F)+\!\!\sum_{\{x,y\}\in\binom{N(v)}{2}}\!\!\! p_F(x,y)\,,$$
because a cycle through $v$ is exactly a pair of neighbours of $v$ together
with a path between them avoiding $v$.  Theorem B follows from
$p_F(x,y)\ge2$ (Menger) and Theorem A from $p_F(x,y)\ge Q_k$ (path lemma).

## Computational Verification

Everything is exact integer arithmetic; **no experiment uses randomness or
floating point**.

* **Validation of the enumerators.**  We generate *all* unlabeled 2- and
  3-connected graphs by provably complete methods (ear extension; vertex
  extension with Menger's condition), deduplicate by exact canonical labelling
  (bliss), and cross-check against exhaustive brute force over all
  $2^{\binom n2}$ graphs for $n\le 7$ — comparing **sets of canonical labels**,
  not just counts.  Class counts match the published cardinalities
  (`1, 3, 10, 56, 468, 7123, 194066` for 2-connected on $n=3..9$;
  `1, 3, 17, 136, 2388, 80890` for 3-connected on $n=4..9$).
* **Primitive-level validation.**  Cycle counting and path counting are checked
  against `networkx` and against an independent brute-force search over
  2-regular connected edge subsets; vertex connectivity is checked against
  `networkx` on all graphs with $n\le 6$.
* **Path lemma.**  Verified on every pair of vertices of every 2-connected graph
  with $n\le 8$: **210 233 pairs checked, 0 violations**.  The observed minima of
  $p(x,y)$ by connectivity are exactly $Q_3,\dots,Q_8$, so the constant is
  sharp.
* **Theorem A.**  Verified on all $80890$ 3-connected classes with $n\le 9$:
  the minimum at each level $k=3..8$ equals $c(K_{k+1})$, attained by $K_{k+1}$
  alone.
* **92 tests** run in about 3 minutes (`python -m pytest tests -q`).

## Repository Structure

```
paper/           main.tex, references.bib  (the paper)
src/cycle_spectra/
    graph.py           bitmask graph type, factories
    cycles.py          exact cycle and path counting, cone identity
    connectivity.py    exact k-connectivity
    generation.py      complete generators for 2-/3-connected classes
    bounds.py          proved lower bounds (B_fundamental, B_star, ...)
    spectra.py         spectra, extremal function, mu(m) and kappa(m)
    handfacts.py       hand-provable small facts
tests/          92 tests, incl. brute-force cross-validation
experiments/    the pipeline: stages 1-6, run_all.py
scripts/        standalone probes and the brute-force validator
results/        machine-generated JSON + summary.md (provenance block)
figures/        figures used by the paper (generated, not hand-drawn)
docs/           literature review, novelty audit, methodology, notes
```

## Reproducing Results

```bash
pip install -r requirements.txt          # numpy, networkx, igraph, matplotlib, pytest

python -m pytest tests -q                # ~3 min: 92 tests
python experiments/run_all.py            # ~12 min: all results and figures
python experiments/run_all.py --max-n 7  # ~1 min smoke run
python scripts/validate_generators.py 7  # brute-force validation of the generators
```

`experiments/run_all.py` writes `results/*.json` (each with a provenance block
recording Python, library versions, git commit, timestamp and
`"randomness_used": false`) plus `results/summary.md` and the six figures.
Re-running from a clean clone reproduces the values quoted in the paper
bit-for-bit.

**Paper.**  `paper/main.tex` compiles standalone with any LaTeX distribution;
no BibTeX is required, and `references.bib` is provided for users who prefer it.
The compiled PDF (`paper/main.pdf`) is tracked and figures are referenced as
`../figures/*.png`, so compile from inside `paper/`.

## Examples

```python
from cycle_spectra import *

wheel(8)                       # the 6-vertex wheel
count_cycles(wheel(8))         # 43  =  (n-1)(n-2)+1, Theorem B
count_cycles(complete_graph(5))  # 37  =  c(K_5), the minimum for 4-connected graphs

len(three_connected_graphs(8))  # 2388  isomorphism classes, all 3-connected
m, minimisers = extremal_function(three_connected_graphs(8))
m                                # 26 ; the minimiser is a cubic graph

Q(6)                            # 65 = 5*4*3*2*1 + 4! + 3! + 2! + 1  (paths in K_6)
lower_bound(wheel(8))          # 43, attained: wheels are extremal
```

## Limitations

* **Conjecture C is open.**  $c(G)\ge\binom{n-1}{2}$ for 3-connected $G$ is
  verified for $n\le 9$ and proved only for graphs with a dominating vertex.
  Without it, our order bound $2(K-1)$ is far too weak to settle the
  nonexistence direction of McCulloch et al.'s Conjecture 6(a) in general.
* **$m_3(10)$ is not reported.**  The 3-connected generator on 10 vertices did
  not terminate in 50 minutes, so we omit the value rather than extrapolate.
* **$S_k$ for $k\ge4$ is sampled, not determined.**  We report $|S_4|=30$ and
  $|S_5|=5$ on orders $\le7$; the minima are known by Theorem A, the exception
  sets are not.
* **We do not attack the existence direction.**  Showing every $m\ge35$ is a
  3-connected cycle count is a construction problem we leave open.
* **Enumeration is the ceiling, not the mathematics.**  Nothing in the proofs
  depends on computation; the computations merely confirm and measure.

## Related Work

* McCulloch, McKay, Salahshoori & Zaslavsky, *The cycle counts of graphs*,
  Graphs Combin. **42** (2026) — determines $S_2$ and conjectures the
  exception lists for $3$-connected and cubic classes.  We reproduce their
  3-connected exception list below 51 by an independent route.
* Aldred & Thomassen, *On the number of cycles in 3-connected cubic graphs*,
  JCTB **71** (1997) — the closest existing work on "few cycles in highly
  connected graphs", but for *cubic* graphs, a different extremal function.
* Whitney, *Non-separable and planar graphs*, Trans. AMS **34** (1932) —
  ear decomposition of graphs without a cut vertex.
* Carmesin & Kurkofka, *Canonical decompositions of 3-connected graphs*,
  Adv. Combin. **2025:7** — wheels as the elementary 3-connected structures.
* Volkmann, *Estimations for the number of cycles in a graph* (1996);
  Dvořák (2021) — bounds on $c$ from minimum degree and degree sequences.

See [`docs/literature_review.md`](docs/literature_review.md) for the search
strategy and [`docs/novelty_audit.md`](docs/novelty_audit.md) for a
claim-by-claim assessment of what is new.

## Citation

```bibtex
@misc{cycle-spectra,
  author = {Pardeshi, Rajveersinh},
  title  = {Cycle Counts of k-Connected Graphs: A Sharp Minimum, a Decidability
            Theorem, and the 3-Connected Spectrum},
  note   = {Preprint v1.0.0, \url{https://github.com/daveaddams91-dev/cycle-spectra-connectivity}},
  year   = {2026}
}
```

## License

MIT — see [LICENSE](LICENSE).  No claim of peer review or publication is made.
