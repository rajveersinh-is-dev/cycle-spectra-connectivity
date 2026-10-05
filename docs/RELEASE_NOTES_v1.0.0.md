# v1.0.0 — Cycle Counts of $k$-Connected Graphs

A sharp answer to "how many cycles must a highly connected graph have?", a
decidability theorem for cycle-count spectra, and an exact computation of the
3-connected spectrum up to order 9.

---

## Research question

For which positive integers $m$ does there exist a $k$-vertex-connected graph
with exactly $m$ cycles?  Writing $c(G)$ for the number of cycles and
$S_k=\{c(G): G\ k\text{-connected}\}$, we study the decreasing chain
$S_1\supseteq S_2\supseteq S_3\supseteq\cdots$, the extremal function
$m_3(n)=\min\{c(G): G\ 3\text{-connected},\ |V(G)|=n\}$, and what makes these
spectra computable.

## Main theorem

> **Theorem A.**  For every $k\ge 3$ and every $k$-connected graph $G$,
> $$c(G)\ \ge\ c(K_{k+1})=\tfrac12\sum_{j=3}^{k+1}\binom{k+1}{j}(j-1)!,$$
> with equality **iff** $G\cong K_{k+1}$.  For $k=2$ the minimum is $c(K_3)=1$,
> attained exactly by the cycles.

Complete graphs are the sparsest highly connected graphs; the bound is factorial
in $k$ ($7,37,197,1172,8018,62814$ for $k=3,\dots,8$).

**Tool (Path Lemma).**  In an $r$-connected graph, $p_F(x,y)\ge Q_{r+1}$ for all
$x\ne y$, where $Q_k$ = the number of paths between two vertices of $K_k$ and
$Q_2=1$, $Q_{r+1}=1+(r-1)Q_r$.  For $r\ge3$ equality forces $F=K_{r+1}$.

## Also proved

| | result |
|---|---|
| **Counting identity** | $c(G)=c(G-v)+\sum_{\{x,y\}\in\binom{N(v)}{2}}p_{G-v}(x,y)$ |
| **Theorem B** | For 2-connected $F$ on $m\ge3$ vertices, $c(K_1\vee F)\ge m(m-1)+1$, equality iff $F=C_m$.  Equivalently $c(W_n)=(n-1)(n-2)+1$ and the wheel is the unique $n$-vertex 3-connected graph with a dominating vertex minimising $c$; generally $c(G)\ge 1+(k-1)\binom{n-1}{2}$, equality only for $k=3$ |
| **Theorem C** | A $k$-connected graph ($k\ge3$) with $c(G)\le K$ has at most $\lfloor 2(K-1)/(k-2)\rfloor$ vertices, so each $S_k$ is a **computable** set, with $\min S_k=c(K_{k+1})$ and $\kappa(m)=O(m^{1/3})$ |

## Computational contribution

* Provably **complete** generators for unlabeled 2- and 3-connected graphs,
  cross-validated against exhaustive brute force for $n\le 7$ by comparing
  **sets of canonical labels** (bliss), not just counts.  Class counts match the
  published cardinalities: `1, 3, 10, 56, 468, 7123, 194066` and
  `1, 3, 17, 136, 2388, 80890`.
* **Path Lemma** verified on all 210 233 vertex pairs of all 2-connected graphs
  with $n\le8$: **0 violations**, minima equal $Q_3,\dots,Q_8$ exactly.
* **Theorem A** verified on all 80 890 3-connected classes with $n\le9$.
* **Extremal function:** $m_3(4..9)=7,13,14,24,26,42$, minimisers identified.
  From $n=6$ onwards wheels are *not* extremal (the triangular prism beats $W_6$:
  14 vs 21).
* **Spectra:** $S_1=\mathbb{Z}_{>0}$ (every $m$ is realised by a bouquet of $m$
  triangles; verified for $m\le400$).  $S_2$ misses exactly
  $\{2,4,5,8,9,16\}$ below 51 — the list proved by McCulloch, McKay,
  Salahshoori & Zaslavsky (2026) — and $S_3$ misses exactly the 21 integers
  **conjectured** in that paper,
  $\{1,\dots,6,\,8,\dots,12,\,16,\dots,20,\,27,\,30,\,32,\,33,\,34\}$.  This is
  an independent confirmation of their Conjecture 6(a) in this range, obtained
  with a different generator; it is **not** a proof of that conjecture.
* 92 tests in ~3 minutes; six generated figures; every number reproducible
  bit-for-bit from a clean clone.

## Reproducing

```bash
pip install -r requirements.txt
python -m pytest tests -q                 # 90 tests, ~3 min
python experiments/run_all.py             # full pipeline, orders <= 9, ~12 min
python experiments/run_all.py --max-n 7   # smoke run, ~1 min
python scripts/validate_generators.py 7   # brute-force generator validation
```

Everything is exact integer arithmetic; no experiment uses randomness or
floating point.  Each file in `results/` carries a provenance block (library
versions, git commit, timestamp, `randomness_used: false`).

The paper is `paper/main.tex`; it compiles standalone with any LaTeX
distribution (`cd paper && pdflatex main.tex`).

## Known limitations

* **Conjecture C is open:** $c(G)\ge\binom{n-1}{2}$ for 3-connected $G$ is
  verified for $n\le9$ and proved only for graphs with a dominating vertex.
  It is exactly the missing ingredient for turning the low part of the
  3-connected spectrum into a finite computation in general.
* $m_3(10)$ is **not reported** — the generator on 10 vertices did not terminate
  in 50 minutes, so the value is omitted rather than extrapolated.
* $S_k$ for $k\ge4$ is sampled, not determined (minima are known exactly by
  Theorem A; exception sets are not).
* The **existence** direction of McCulloch et al.'s Conjecture 6(a) (constructing
  3-connected graphs for every $m\ge35$) is not attempted.
* We could not access MathSciNet/zbMATH, so novelty claims are stated as "we did
  not find a prior result establishing", never as "first".  See
  `docs/novelty_audit.md` for a claim-by-claim audit, including the parts we
  label as folklore.

## Citation

`ibtex
@misc{cycle-spectra,
  author = {Pardeshi, Rajveersinh},
  title  = {Cycle Counts of k-Connected Graphs: A Sharp Minimum, a Decidability
            Theorem, and the 3-Connected Spectrum},
  note   = {Preprint v1.0.0, \url{https://github.com/rajveersinh-is-dev/cycle-spectra-connectivity}},
  year   = {2026}
}
```

MIT licensed.  **No claim of peer review or journal publication is made.**