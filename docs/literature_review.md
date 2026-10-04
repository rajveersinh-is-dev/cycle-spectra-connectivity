# Literature review and search log

This file records what we searched for, where, and what we found.  It is meant
to let a reader check our novelty claims rather than take them on trust.  All
searches were performed in October 2026.

## 1. How we searched

| channel | queries (representative) |
|---|---|
| arXiv listing / full text | `"cycle count" "3-connected"`, `"inseparable graph" McKay Zaslavsky`, `"Canonical Decompositions of 3-Connected Graphs"`, `"number of cycles in 3-connected cubic graphs"` |
| general web search | `minimum number of cycles in a 3-connected graph extremal lower bound`, `"inseparable" graph ear decomposition`, `"number of paths between two vertices" "k-connected" graph lower bound complete graph`, `"3-connected" graph "number of cycles" lower bound wheel minimizes` |
| publisher pages | Springer (Graphs & Combinatorics), Cambridge Core, ScienceDirect, SIAM, arXiv HTML full texts |
| OEIS | A002807 (cycles of `K_n`), A385523 / A385524 (exception lists of McCulloch et al.) |
| MathSciNet / zbMATH | not accessible from this environment — **recorded as a gap** |
| MathOverflow | scanned "bounds on number of simple paths in a graph" |

We deliberately searched *equivalent formulations* of our conjectures, not just
our own wording: "few cycles" / "minimum cycle count" / "extremal", "k-connected
/ vertex-connected / biconnected / triconnected / high connectivity", "wheel /
cone / join with `K_1` / dominating vertex", "paths between two vertices /
internally disjoint paths / Menger".

## 2. The paper that frames the project

**McCulloch, McKay, Salahshoori, Zaslavsky — *The cycle counts of graphs*,
Graphs and Combinatorics 42 (2026), 53–, preprint arXiv:2507.02260.**

* Determines `$S_2$`: every positive integer except `{2,4,5,8,9,16}` is the
  cycle count of a graph without a cut vertex (= 2-connected graph).
  Their term "inseparable" is Whitney's, and they note that for loop-free
  graphs with more than two vertices inseparability equals 2-connectivity.
* Main tool: an ear-path lemma (adding an ear between `v` and `w` adds as many
  cycles as there are `v`–`w` paths), plus Menger.
* Key reduction: cycles of a 2-connected outerplanar graph `G` with inner dual
  tree `T` correspond bijectively to subtrees of `T` (their Theorem 8);
  combined with Czabarka–Székely–Wagner on subtree counts of trees, this gives
  the result for all but finitely many small counts.
* **Section 6 states five conjectures** with computational evidence.  Their
  Conjecture 6(a): the integers missing from the 3-connected spectrum are
  exactly
  `{1,…,6, 8,…,12, 16,…,20, 27, 30, 32, 33, 34}`,
  with all other counts up to 3000 occurring.  Items (b)–(e) do the same for
  2- and 3-connected cubic graphs and their planar subclasses.
* Their stated missing counts for 3-connected *cubic* graphs go up to 459,
  which suggests the nonexistence proofs there are genuinely hard.

**Consequence for us.**  The existence direction of Conjecture 6(a) is beyond
reach for a project of this size (it needs constructions for *every* `m >= 35`).
The *nonexistence* direction is where a genuine contribution is possible, and it
reduces to a sharp order bound — which is why our Theorems A–C and Conjecture C
are aimed exactly there.

## 3. Closest existing work on "few cycles in highly connected graphs"

* **Barefoot, Barefoot, Čekan, Krajaničková, Širáň — `f_k(n)`** (introduced in
  the computational literature, discussed in the survey of extremal cycle
  problems): `f_k(n)` = the smallest number of cycles in any `k`-connected
  **cubic** graph on `n` vertices.  `f_1` is linear in `n`.
* **Aldred & Thomassen — *On the number of cycles in 3-connected cubic graphs*,
  JCT-B 71 (1997), 79–84.**  Proves a superlinear lower bound for `f_3(n)`
  (quoted in the survey as `f_3(n) > 2 n^{0.17}` for large `n`).
* **Volkmann — *Estimations for the number of cycles in a graph*, Period. Math.
  Hungar. 33 (1996), 153–161**: minimum-degree bounds such as
  `c(G) >= n(δ-1)/2 + 1`.
* **Dvořák — *Bounding the number of cycles in a graph in terms of its degree
  sequence*** (2021): upper bounds on `c`, resolving conjectures of Király and of
  Arman–Tsaturian.

**Why our extremal function is genuinely different.**  `f_k(n)` restricts to
cubic graphs; we minimise over *all* `k`-connected graphs.  The minimisers we
compute are a wheel at `n = 5`, a prism at `n = 6` and a cubic graph at `n = 8`,
so the two extremal problems have different answers.  We therefore regard
Theorem A (`min` over the class) and `m_3(n)` (min at fixed order) as
complementary to Aldred–Thomassen rather than as competing claims.

## 4. Structural background we used

* **Whitney (1932), Trans. AMS 34, 339–362**: "non-separable" graphs; the ear
  characterisation (used verbatim as McCulloch et al. cite it, Theorem 19);
  adding an ear preserves inseparability.
* **Menger**: `G - v` is `(k-1)`-connected; `r` internally disjoint paths in an
  `r`-connected graph.
* **Carmesin & Kurkofka — *Canonical decompositions of 3-connected graphs*,
  Adv. Combin. 2025:7**: every `k`-connected graph becomes `(k+1)`-connected by
  adjoining a universal vertex, "so wheels are the 3-connected analogues of
  cycles"; wheels appear as elementary pieces of the 2-connected structure.
  This is what made the cone the natural object for us.
* **Czabarka, Székely, Wagner (2009)**: which integers count subtrees of some
  tree (sequence A184164) — the ingredient behind McCulloch et al.'s
  two-connected result, and the closest thing we found to a "which integers
  occur" theorem for a structured class.
* **McKay & Piperno (2014)**, **Brinkmann–Goedgebeur–McKay (2011)**,
  **Brinkmann & McKay (2007)**, **Read (1956)**, **Harary–Palmer (1973)**:
  the graph-enumeration toolchain we cite for context.  Our own generators do
  not use nauty/plantri; they use bliss canonical labelling via `igraph`.

## 5. What we searched for and did *not* find

For each of these we searched several formulations and read what we found:

| statement | outcome |
|---|---|
| `min{ c(G) : G k-connected } = c(K_{k+1})` | **no result found.** Closest: bounds on the minimum over `k`-connected *cubic* graphs (Aldred–Thomassen) and minimum-degree bounds (Volkmann). |
| "in an `r`-connected graph there are at least $Q_{r+1}$ paths between two vertices" | **no result found** with this constant. Follows from a short induction, so it may be folklore or an exercise. |
| wheels minimise `c` among 3-connected cones | **no result found.** |
| finiteness / decidability of `S_k` for `k >= 3` | **no result found**, but it is two lines from the fundamental-cycle bound; we assume it is unrecorded rather than deep. |
| exact `m_3(n)` beyond `n = 5` | **no result found.** |
| $c(K_n)$ | classical, OEIS A002807: `1, 7, 37, 197, 1172, 8018, 62814` — matches our independently computed values. |

## 6. Gaps in our search we acknowledge

* **MathSciNet and zbMATH were not accessible** from this environment, so we
  cannot rule out that Theorem A exists in the literature.  The paper says
  "apparently new" and quotes the table; it never says "first".
* We did not search in non-English sources, nor in the proceedings of
  specialized connectivity conferences beyond Google-indexed pages.
* Dvořák (2021) and Locke (1982) are cited from publisher landing pages with
  title and author only; we did not see volume/page numbers, and the paper
  therefore cites them without them.