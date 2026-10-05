# Changelog

All notable changes to this project are documented here.  The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-10-05

Patch release.  No change to any theorem statement, numerical result or figure;
one proof gap in `v1.0.0` is closed and the disclosure is retained in the paper.

### Fixed

- **Proof gap in the Path Lemma's `r = 3` equality case** (`paper/main.tex`,
  `docs/novelty_audit.md` §E).  The `v1.0.0` proof invoked the induction
  hypothesis at `r - 1 = 2`, whose equality statement is false, so
  `F - x = K_3` did not follow.  The statement was true and verified on all
  `3`-connected graphs with `n <= 9`; the proof did not establish it.
  - Added **Lemma (paths in 2-connected graphs)**: in a `2`-connected graph `H`,
    `p_H(a, b) >= 2`, and `p_H(a, b) = 2` iff `H` is a cycle.
  - Redid the `r = 3` case from it; the `r >= 4` case is unchanged.
  - Corrected `Q_r >= Q_4 = 5` to `Q_r >= Q_3 = 2` in the same argument (the
    former is false at `r = 3`).
  - Theorem A was unaffected; the paper now records that its equality analysis
    never used the Path Lemma's equality statement.

### Added

- Pipeline stage 2a' checks the new lemma on all `2`-connected graphs with
  `n <= 8`: `210 233` pairs, 6 cycles, 0 violations.
- `scripts/check_paper.py` statically validates `paper/main.tex`.  The paper
  also now compiles with **zero** undefined references or citations
  (verified with `tectonic`; 15 pages).
- Regression tests for the new lemma; the suite is 97 tests.

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
- **Lemma (paths in 2-connected graphs).**  In a 2-connected graph `H` and for
  `a != b`, `p_H(a,b) >= 2` and `p_H(a,b) = 2` iff `H` is a cycle.  This
  classifies the `r = 2` equality cases and supplies the `r = 3` case of the
  path lemma; verified exhaustively for `n <= 7`.
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

- 97 tests covering primitives, generators, bounds, spectra and the stated
  theorems; the suite runs in about three minutes.
- `experiments/run_all.py` writes JSON results with a provenance block
  (versions, git commit, timestamp, `randomness_used: false`).
- `scripts/check_paper.py` statically validates `paper/main.tex` (brace balance,
  environment matching, dangling `\ref`/`\cite`, missing figures).
- Paper `paper/main.tex` compiles standalone; no BibTeX required.

[1.0.1]: https://github.com/rajveersinh-is-dev/cycle-spectra-connectivity/releases/tag/v1.0.1
[1.0.0]: https://github.com/rajveersinh-is-dev/cycle-spectra-connectivity/releases/tag/v1.0.0