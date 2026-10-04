# Mathematical notes: derivations, dead ends, and open doors

Working notes behind the paper.  Kept because the dead ends are informative and
because a reader who wants to extend the work should not have to rediscover
them.

---

## 1. The two identities, from scratch

### 1.1 Cone identity

Let `v` be any vertex of `G` and `F = G - v`.  Cycles of `G`:

* **avoiding** `v` ⟺ cycles of `F`;
* **through** `v`: meets `N(v)` in exactly two vertices `x, y`, and `C - v` is a
  simple `x`–`y` path in `F`.

So
$$\boxed{\,c(G)=c(G-v)+\sum_{\{x,y\}\in\binom{N(v)}{2}}p_F(x,y)\,}\qquad(\star)$$

Sanity checks: `F = C_m` (so `G = W_{m+1}`) gives `c(W_n) = 1 + 2 C(n-1,2) =
(n-1)(n-2)+1`; `G = K_{k+1}` gives `c(K_{k+1}) = c(K_k) + C(k,2) Q_k`.

### 1.2 The path constant

$Q_k = p_{K_k}(x,y) = \sum_{j=0}^{k-2}\binom{k-2}{j}j! = (k-2)!\sum_{i=0}^{k-2}1/i!$,
hence $Q_2=1$ and $Q_{r+1}=(r-1)!\,E_{r-1}=(r-1)(r-2)!E_{r-2}+1=1+(r-1)Q_r$.

Values: `Q_2..Q_9 = 1, 2, 5, 16, 65, 326, 1957, 13700`.  Check by hand:
$p_{K_4}(x,y) = 1 + 2 + 2 = 5$ (edge; two two-edge paths; two three-edge paths)
and $1 + 2\cdot 2 = 5$ ✓.

### 1.3 Theorem A by induction

`c(G) = c(G-v) + Σ p_{G-v}(x,y) >= c(K_k) + C(k,2) Q_k = c(K_{k+1})`.

The equality analysis at `k = 3` is the only delicate step: the path lemma's
equality statement is *false* for `r = 2` (`C_4` is a counterexample), so it
cannot be used to force `G - v = K_3`.  The fix: equality forces `c(G-v) = 1`,
so every vertex of `F = G - v` has degree 2; as `δ(G) >= 3` each must be adjacent
to `v`, so `d_G(v) = n - 1`, and combined with `d_G(v) = 3` this forces `n = 4`.

---

## 2. Dead ends (recorded so they are not repeated)

### 2.1 "Wheels minimise everything" — false

The first hypothesis was that the wheel $W_n$ minimises $c$ among `n`-vertex
3-connected graphs, by analogy with `m_2(n) = 1` for cycles.  **Refuted by
enumeration**: `m_3(6) = 14` (triangular prism) versus `c(W_6) = 21`, and
`m_3(8) = 26` versus `c(W_8) = 43`.  The correct theorem is order-free
(Theorem A) and cones are extremal only within their own class (Theorem B).

### 2.2 Trying to prove $c(G) \ge \binom{n-1}{2}$ directly

Attempts and why they stall:

* **Sum over vertices.**  `Σ_v c_v = Σ_C |C| <= n c(G)`, and `c_v >= 2 C(d(v),2)`,
  which for `δ >= 3` gives only `c(G) >= 6`.  The obstacle is that cycles in
  3-connected graphs are *long*, so per-cycle counting cannot yield a quadratic
  bound.
* **Path counting on `F = G - v` with a small neighbour set.**  With
  `d_G(v) = d` we get `c(G) >= c(F) + (k-1)C(d,2)`; for `d = 3` this is
  `>= (r+2)/2 + 6`, i.e. `~n/2`, far short of `n^2/2`.  To close the gap one
  needs a lower bound on `c(F)` in terms of `m` **and** on
  `p_F(s_i,s_j)` in terms of `m`, but 3-connectivity of `G` only says that every
  component of `F - {y,z}` meets `N(v)`; when `|N(v)| = 3` that condition does
  *not* prevent `F` from being "long and thin".
* **Girth / Moore bound.**  In a graph of minimum degree `δ >= 3` and girth `g`,
  the number of cycles of length `≤ g` is `≥ n 2^g / (2 g^2)`, and for cubic
  graphs Moore gives `g ≤ 2 log_2 n`, so `c(G) = Ω(n^2 / log^2 n)` *in that
  regime*.  This beats quadratics asymptotically but only when `g` is large; for
  small `girth` it gives nothing, and combining the regimes is delicate.
* **Topological `K_{k+1}` inside `G`.**  Since `c` is subdivision-invariant and
  every `k`-connected graph contains a subdivision of `K_{k+1}`, Theorem A also
  follows from that classical fact.  We did *not* use this in the paper because
  it moves the difficulty into a theorem we could not verify precisely; it is
  worth noting in the discussion as an alternative proof route.

Conclusion: an order-sensitive bound needs a genuinely new counting object.
The most promising candidate, suggested by the data, is **the number of cycles
through a fixed vertex** rather than the number of paths: in the extremal
configuration (a cone) all cycles but one pass through the apex.

### 2.3 Trying to close the induction for `k >= 5`

With `p_F(x,y) >= max(d_F(x), d_F(y))` one gets `c_v >= C(d,2)(k-1)`, and
`c(K_k) + C(k,2)(k-1)` falls short of `c(K_{k+1})` for `k >= 5`
(e.g. `k=5`: `37 + 60 = 97 < 197`).  The correct constant is `Q_k`, which is
what Lemma 3 supplies; the shortfall of the naive bound is instructive: it
measures how much path structure connectivity forces beyond Menger's minimum.

### 2.4 Minimum path count in `r`-connected graphs

The observed minimum of `p(x,y)` over `r`-connected graphs of order `n` is
`Q_{r+1}` exactly when `n = r+1`, and grows with `n` (`r = 3`: `5, 7, 8, 11, 13`
for `n = 4, 5, 6, 7, 8`).  So `Q_{r+1}` is sharp but the *equality* case
`r = 2` is structurally wild (every cycle).  This is why the equality statement
is restricted to `r >= 3`.

---

## 3. Open doors

1. **Prove or refute Conjecture C.**  $c(G) \ge \binom{n-1}{2}$ for
   3-connected `G$.  If true, the nonexistence half of the 3-connected spectrum
   below 35 becomes a finite computation, since `$|V| <= 9$`.
2. **Is $m_3(n)$ attained by graphs as regular as parity allows?**  Six data
   points say yes for `n <= 9`.  A structural induction on ears might work.
3. **Spectra of $S_4$, $S_5$.**  The minima are known exactly
   (`c(K_5)=37`, `c(K_6)=197`); the exception sets are not.
4. **Order-sensitive Theorem A.**  What is $\min\{c(G): G\ k\text{-connected},
   |V|=n\}$ in closed form?  For `k = 3` it is the erratic sequence
   `7, 13, 14, 24, 26, 42`.
5. **Cubic restriction.**  Aldred–Thomassen's `f_3(n)` and our `m_3(n)` are
   different; their ratio `m_3(n)/f_3(n)` measures the cost of dropping
   regularity and might itself be a nice quantity.

---

## 4. Notation table

| symbol | meaning |
|---|---|
| `c(G)` | number of cycles of `G` |
| `p_G(x,y)` | number of simple `x`–`y` paths |
| `P(F)` | $\sum_{\{x,y\}}p_F(x,y)$, total number of paths |
| `κ(G)` | vertex connectivity |
| `$S_k$` | $\{c(G): G\ k\text{-connected}\}$ |
| `$m_3(n)$` | $\min\{c(G): G\ 3\text{-conn}, |V|=n\}$ |
| `Q_k` | `$p_{K_k}(x,y)$`, the constant of the path lemma |
| `$c_n$` | `c(K_n)` |
| `μ(m)`, `κ(m)` | least order / greatest connectivity realising a cycle count `m` |
| `W_n` | wheel: `C_{n-1}` plus a hub |
| `K_1 ∨ F` | cone over `F` |