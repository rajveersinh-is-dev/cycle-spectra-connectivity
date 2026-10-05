# Changelog

All notable changes to this project are documented here.  The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-04

First public release.  No prior public version, no claim of peer review.

### Mathematics

- **Theorem A (sharp minimum).**  For `k >= 3`, every `k`-connected graph `G`
  satisfies `c(G) >= c(K_{k+1})`, with equality iff `G = K_{k+1}`.  Corollary:
  for `k = 2` the minimum is `c(K_3) = 1`, attained exactly by the cycles.
- **Lemma (path lemma).**  In an `r`-connected graph, `p(x,y) >= Q_{r+1}`,
  where `Q_k` is the number of paths between two vertices of `K_k`; equality for
  `r >= 3` forces `F = K_{r+1}`.  Verified on 210 233 vertex pairs with no
  violation.
- **Lemma (recurrence).**  `Q_2 = 1` and `Q_{r+1} = 1 + (r-1) Q_r`.
- **Lemma (cone identity).**  `c(G) = c(G - v) + sum over pairs in N(v) of
  p_{G-v}(x,y)`.
- **Theorem B (cone minimum).**  For 2-connected `F` on `m >= 3` vertices,
  `c(K_1 v F) >= m(m-1) + 1`, equality iff `F = C_m`; and
  `c(G) >= 1 + (k-1) C(n-1, 2)` for `k`-connected graphs with a dominating
  vertex, equality only for `k = 3` and `G = W_n`.
- **Theorem C (finiteness).**  A `k`-connected graph (`k >= 3`) with
  `c(G) <= K` has at most `floor(2(K-1)/(k-2))` vertices; hence each spectrum
  `S_k` is a computable set, with `min S_k = c(K_{k+1})` and
  `kappa(m) = O(m^{1/3})`.
- **Conjecture C (open).**  `c(G) >= C(n-1, 2)` for 3-connected `G` on
  `n >= 4` vertices; verified exhaustively for `n <= 9`.

### Computation

- Exact cycle counting, cycle-length profiles, path counting, cone counts and
  `k`-connectivity for graphs on small orders.
- Provably complete generators for unlabeled 2- and 3-connected graphs, up to
  order 9, cross-validated against exhaustive brute force for `n <= 7`.
- Exact determination of the extremal function `m_3(n)` for `4 <= n <= 9`:
  `7, 13, 14, 24, 26, 42`, with minimisers.
- Exact spectra `S_2` and `S_3` below 51; `S_3`'s exception list agrees exactly
  with the conjecture of McCulloch, McKay, Salahshoori & Zaslavsky (2026).
- Six figures, each answering one mathematical question.

### Infrastructure

- 92 tests covering primitives, generators, bounds, spectra and the stated
  theorems; the suite runs in about three minutes.
- `experiments/run_all.py` writes JSON results with a provenance block
  (versions, git commit, timestamp, `randomness_used: false`).
- Paper `paper/main.tex` compiles standalone; no BibTeX required.

[1.0.0]: https://github.com/daveaddams91-dev/cycle-spectra-connectivity/releases/tag/v1.0.0