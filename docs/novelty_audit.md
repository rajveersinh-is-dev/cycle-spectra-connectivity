# Novelty audit

Claim-by-claim assessment.  Labels follow the scheme requested for this
project: **known**, **apparently known**, **folklore**, **obvious
consequence**, **potentially new**, **apparently new**, and
**novelty not established**.

Throughout: *we did not find a prior result establishing* X.  We never write
"this is the first", and we could not access MathSciNet/zbMATH (see
`docs/literature_review.md` §6).

---

## A. Results we prove

### A1. Cone counting identity

$$c(G)=c(G-v)+\sum_{\{x,y\}\in\binom{N(v)}{2}}p_{G-v}(x,y).$$

**Label: known.**  It is the same observation as the ear-path lemma of
McCulloch–McKay–Salahshoori–Zaslavsky (their Lemma 4) and as counting cycles
through the apex of a cone.  **We claim no novelty.**  We include it because it
is the cleanest possible route to A2 and because the *derived* bound A2 is new.

### A2. Theorem B (cone minimum)

For 2-connected `F` on `m >= 3` vertices, `c(K_1 ∨ F) >= m(m-1) + 1`, equality
iff `F = C_m`.  Equivalently `c(W_n) = (n-1)(n-2) + 1` and `W_n` is the unique
`n`-vertex 3-connected graph with a dominating vertex minimising `c`.

**Label: apparently new in this form.**  Searched: "wheel minimises cycles",
"cone over 2-connected graph", "dominating vertex sparse cycles", "wheel
extremal 3-connected".  Found nothing matching.  It is a two-line consequence
of A1 plus Menger, so it is small; we present it as a clean complete result
rather than a deep one.

### A3. Path lemma

In an `r`-connected graph, `p(x,y) >= Q_{r+1}` where `Q_k` = number of paths
between two vertices of `K_k`; for `r >= 3` equality forces `K_{r+1}`.

**Label: probably folklore.**  The proof is a short induction from Menger's
theorem (`F - x` is `(r-1)`-connected, and each neighbour of `x` contributes
`>= Q_r` paths).  The *sharpness* statement we verified exhaustively
(210 233 pairs, 0 violations, minima equal `Q_3 … Q_8` exactly).

Sub-claim A3a: the recurrence `Q_2 = 1`, `Q_{r+1} = 1 + (r-1) Q_r`.
**Label: obvious consequence** of `Q_m = (m-2)! · Σ_{i≤m-2} 1/i!`, proved in
Appendix A of the paper.

Sub-claim A3b (added after red-teaming; see §E, Reviewer D): if `H` is
2-connected and `a ≠ b`, then `p_H(a,b) >= 2`, and `p_H(a,b) = 2` iff `H` is a
cycle.  **Label: standard**, via Menger plus the `$C`-path` argument, and
verified exhaustively on all 2-connected graphs with `n <= 7`.  This is the
statement that makes the `r = 3` equality case of A3 go through, and it is
*false* in the shape one would first guess (`r = 2` equality is every cycle, not
just `K_3`).

### A4. Theorem A (sharp minimum)

For `k >= 3`, `min{ c(G) : G k-connected } = c(K_{k+1})`, equality iff
`G = K_{k+1}`.

**Label: apparently new.**  This is the paper's headline claim.  Searches run:
"minimum number of cycles in a 3-connected graph", "few cycles highly connected
graph", "min cycles k-connected", "extremal cycle count connectivity", plus
equivalent formulations.  What exists:

* bounds on the minimum over `k`-connected **cubic** graphs (Aldred–Thomassen
  1997), a different extremal problem;
* minimum-degree bounds valid for all graphs (Volkmann 1996);
* upper bounds on `c` in terms of degree sequences (Dvořák 2021).

None of these determines the minimum over a connectivity class.  We verified
Theorem A exhaustively for `k = 3 … 8` on all 3-connected graphs with `n <= 9`
(80 890 classes).

Caveat we state in the paper: it might exist as an exercise; we could not
verify either way.

### A5. Theorem C (finiteness) and C′ (decidability)

A `k`-connected graph with `c(G) <= K` has `|V| <= floor(2(K-1)/(k-2))`; hence
`S_k` is computable for `k >= 3`, `min S_k = c(K_{k+1})`, and
`kappa(m) = O(m^{1/3})`.

**Label: obvious consequence**, of the fundamental-cycle bound `c(G) >=
|E| - |V| + 1` together with `|E| >= k|V|/2`.  Two lines.  **Novelty not
established**, and we do not claim it: the value is the *formulation*
(``the spectra are computable, with an explicit reduction''), and the observation
that this fails for `k <= 2` is, we believe, worth recording.

---

## B. Computations

### B1. Generators are complete and cross-validated

**Label: methodology, not novelty.**  The generators (ear extension for
2-connected; vertex extension + Menger pruning for 3-connected) are classical
devices.  The contribution is the *validation protocol*: comparison against
exhaustive brute force as **sets of canonical labels** for `n <= 7`, not merely
counts, plus matching the published cardinalities
(`1, 3, 10, 56, 468, 7123, 194066` and `1, 3, 17, 136, 2388, 80890`).

### B2. `m_3(n)` for `4 <= n <= 9`

**Label: new computation.**  Values `7, 13, 14, 24, 26, 42` with minimisers
identified.  We found no source for `m_3(n)` at all, and none for the closely
related cubic-restricted function beyond Aldred–Thomassen's superlinear bound.

### B3. Recomputation of the exception sets of `S_2` and `S_3` below 51

**Label: independent confirmation of a conjecture.**  Our `S_2` computation
returns exactly `{2,4,5,8,9,16}` — the list McCulloch et al. *prove* — and our
`S_3` computation returns exactly their *conjectured* 21-element list.  This is
evidence, not a proof: our enumeration only covers `n <= 9`, and
Conjecture C (Section C1 below) is what would be needed to extend it to all `n`.

---

## C. Conjectures (explicitly *not* theorems)

### C1. Sharp order-sensitive bound

$$c(G)\ \ge\ \binom{n-1}{2}\qquad\text{for 3-connected }G\text{ on }n\ge 4.$$

**Label: potentially new; open.**  Verified exhaustively for `n <= 9`.  The
second half (wheels minimise among 3-connected graphs with a dominating vertex)
*is* a theorem (A2).

### C2. Extremisers of `m_3(n)` are as regular as parity allows

Every minimiser we computed is 3-regular when `3n` is even.

**Label: potentially new; open; purely heuristic.**  Six data points.  We
present it as a direction, not a claim.

### C3. The 3-connected spectrum of McCulloch et al.

**Not our conjecture.**  We reproduce the low part and state precisely what is
missing (B3 above and Section 9 of the paper).

---

## D. Things we explicitly did *not* claim

* Not "the first" anything.
* Not that the path lemma is new.
* Not that `m_3(n)` for `n <= 9` was previously unknown — only that we found
  no source, and that our value at `n = 5` is a wheel while the cubic-restricted
  function of Aldred–Thomassen is a different object.
* Not that the $3$-connected nonexistence results follow: they follow from our
  computation only up to $n = 9$, and the completeness of that step needs C1.
* Not that our exception list for `S_3` proves the conjecture of
  McCulloch et al.

---

## E. Adversarial questions, answered

> **Reviewer A (pure mathematician).** *Is the induction in Theorem A sound?*
> The induction step uses `p_{G-v}(x,y) >= Q_k` for the `(k-1)`-connected graph
> `G - v`, which has at least `k` vertices — so Lemma 3 with `r = k-1` applies,
> requiring `|V| > k-1`, satisfied.  The base case is `k = 3`, whose equality
> analysis we verified in detail (a subtle point: at `r = 2` the path lemma's
> *equality statement* fails, and we handle `k = 3` separately using
> `delta(G) >= 3`; this is written out in the proof and flagged in the paper and
> as a regression test).  The earlier version of our proof used the `r >= 3`
> equality statement at `k = 3` and was wrong; the fix is in the released proof.

> **Reviewer B (computational mathematician).** *Could the generators miss or
> invent classes?*  Cross-validated as label sets against brute force for
> `n <= 7` (`scripts/validate_generators.py`), and cardinalities match published
> values.  *Could the cycle counter be wrong?*  Validated against
> `networkx.simple_cycles` and an independent edge-subset brute force.  *Are the
> figures fabricated?*  All are generated by `experiments/stage6_figures.py`
> from `results/*.json`.

> **Reviewer C (research reviewer).** *Is this derivative?*  It reuses known
> tools (Menger, ears, canonical labelling) to obtain a sharp statement we could
> not find in the literature, plus an exact independent recomputation of a
> current conjecture.  *Is it overclaimed?*  We removed the strongest phrasing
> ("new"), labelled the path lemma folklore, and stated the open parts as open.

> **Reviewer D (adversarial referee, pass 2 — a real gap that was found and
> fixed).**  *Walk through the `r = 3` equality case of the Path Lemma.*  The
> released proof used to say: equality forces `p_{F-x}(z,y) = Q_r`, and by the
> induction hypothesis `F - x ≅ K_r`.  But at `r = 3` the induction hypothesis
> is the `r = 2` case, where the equality statement is *false* (every cycle is an
> equality case, and `C_4 ≠ K_3`).  So the argument was invalid for `r = 3`:
> `F - x` is 2-connected with `p_{F-x}(z,y) = Q_3 = 2`, which does **not** force
> `F - x = K_3`.  We had verified the *statement* by brute force over all
> 3-connected graphs with `n <= 9` and found no counterexample, so the
> statement is true — but the written proof did not establish it.
>
> **Fix.** Proved the missing ingredient as its own lemma (A3b above): in a
> 2-connected graph, exactly two `a-b` paths forces a cycle.  Then the `r = 3`
> case is: `F - x` is a cycle ⇒ every vertex of `F - x` has degree 2 there and,
> since `delta(F) >= 3`, is adjacent to `x` ⇒ `|V(F - x)| = d_F(x) = 3` ⇒
> `F = K_4`.  The `r >= 4` case keeps the induction.  The paper states
> explicitly that Theorem A does *not* depend on this equality statement, so
> Theorem A was never affected.
>
> **Second defect found in the same pass.** The exclusion of `xy ∉ E(F)` was
> written as "`Q_r >= Q_4 = 5 > 1`", which is wrong at `r = 3` (where
> `Q_r = Q_3 = 2`).  The needed bound is `Q_r >= Q_3 = 2 > 1`; corrected.
>
> Both fixes are covered by regression tests
> (`tests/test_theorems.py::test_paths_in_two_connected_graphs`,
> `::test_path_lemma_equality_fails_for_r_eq_2`).  The lesson we record:
> *exhaustive verification of a statement does not license a proof of it, and an
> induction step can quietly be invalid at its first non-trivial index while
> remaining true.*  Read the base cases of inductions explicitly.