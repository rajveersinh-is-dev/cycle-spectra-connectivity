# Cycle spectra of connectivity classes — v1.0.1

Patch release. **No theorem statement, numerical result, or figure changed.**
One proof gap in `v1.0.0` is closed, and the disclosure is kept in the paper
rather than quietly repaired.

## The gap

The Path Lemma states that for an `r`-connected graph `F`, `p_F(x,y) >= Q_{r+1}`,
with equality only for `F = K_{r+1}` when `r >= 3`. In `v1.0.0` the `r = 3`
case of the equality analysis argued as follows:

> `F - x` is 2-connected with `p_{F-x}(z,y) = Q_3 = 2`, so by the induction
> hypothesis `F - x = K_3`.

The induction hypothesis at `r - 1 = 2` is a statement that is **false** —
equality at `r = 2` is achieved by every cycle, not only by `K_3` (e.g. `C_4`
has `p(x,y) = 2 = Q_3` but `C_4 != K_3`). So the step was invalid at exactly
that index.

The statement itself is true, and it had been verified on every `3`-connected
graph with `n <= 9` (80 890 classes, no counterexample). But a verified
statement is not a proved statement. This is recorded as the general lesson in
`docs/novelty_audit.md` §E and `docs/methodology.md`.

## The fix

* **New Lemma (paths in 2-connected graphs).** In a `2`-connected graph `H` and
  for `a != b`, `p_H(a,b) >= 2`, and `p_H(a,b) = 2` **iff `H` is a cycle**.
  Proved from Menger's theorem plus the classical `C`-path argument, written out
  with two explicit claims: every component `W` of `H - V(C)` satisfies
  `|N(W) cap V(C)| >= 2`, and `C u E(P)` contains an `a`-`b` path using an edge
  of the `C`-path `P`.
* **Path Lemma, `r = 3`:** `F - x` is a cycle by the new lemma; every vertex of
  `F - x` has degree 2 there and, since `delta(F) >= 3`, is adjacent to `x`;
  hence `|V(F - x)| = d_F(x) = 3` and `F = K_4`. The `r >= 4` case keeps the
  induction and is unchanged.
* **A second defect in the same paragraph:** excluding `xy not in E(F)` needed
  `Q_r >= Q_3 = 2`, not the written `Q_r >= Q_4 = 5`, which is false at `r = 3`.

**Theorem A was never affected.** Its equality analysis uses only the induction
hypothesis, the `2`-connected corollary and a degree count — never the Path
Lemma's equality statement. The paper now says so explicitly.

## Also in this release

* Pipeline stage 2a' checks the new lemma on all `2`-connected graphs with
  `n <= 8`: **210 233 pairs, 6 cycles, 0 violations.** The claim in the paper is
  therefore reproducible rather than a one-off claim.
* `scripts/check_paper.py` — static validation of `paper/main.tex` (brace
  balance, environment matching, dangling `\ref`/`\cite`, missing figures).
  The paper now compiles with **zero** undefined references or citations
  (verified with `tectonic`; 15 pages).
* The limitations section previously described the `r = 2` equality cases as
  "structurally unclassified". The new lemma shows they are *exactly* the
  cycles, so that wording is superseded and corrected.
* Regression tests for the new lemma. The suite is **97 tests**.

## Reproduce

```bash
python -m pytest tests -q                # 97 tests, ~3 min
python experiments/run_all.py            # ~12 min, max_n 9
python scripts/validate_generators.py 7  # brute-force generator validation
python scripts/check_paper.py            # paper sanity checks
```

No previously reported value changed: `results/` differs from `v1.0.0` only by
the new `two_connected_lemma` block and the provenance fields (git commit,
timestamp).