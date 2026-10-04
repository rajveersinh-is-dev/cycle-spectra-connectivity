"""Stage 6: figures.  Each figure answers one mathematical question."""

from __future__ import annotations

import json

from common import FIGURES, ROOT, setup_matplotlib

plt = setup_matplotlib()

COLOUR = {
    "present": "#3b6ea5",
    "missing": "#c0504d",
    "accent": "#e08214",
    "grey": "#7f7f7f",
    "green": "#4f8a4f",
}


def _load(name: str) -> dict:
    return json.loads((ROOT / "results" / f"{name}.json").read_text(encoding="utf-8"))


def fig_spectra(bound: int = 50) -> str:
    """Which integers in [1, bound] occur as the cycle count of a k-connected graph?"""
    data = _load("spectra")
    rows = [
        ("k=1 (connected)", [], COLOUR["green"]),
        ("k=2 (2-connected)", data["S_2_missing_below_bound"], COLOUR["present"]),
        ("k=3 (3-connected)", data["S_3_missing_below_bound"], COLOUR["accent"]),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 1.5 + 0.55 * len(rows)))
    for i, (label, missing, colour) in enumerate(rows):
        y = len(rows) - i
        present = [m for m in range(1, bound + 1) if m not in set(missing)]
        ax.barh(y, len(present), left=1, height=0.55, color=colour, alpha=0.85)
        for m in missing:
            ax.add_patch(plt.Rectangle((m - 0.5, y - 0.275), 1.0, 0.55, color=COLOUR["missing"]))
        ax.text(bound + 1.2, y, f"{len(present)}/{bound} realised", va="center", fontsize=8)
        if missing:
            ax.text(0.0, y + 0.45, "missing: " + ",".join(str(m) for m in missing),
                    fontsize=7, color=COLOUR["missing"])
    ax.set_yticks(range(1, len(rows) + 1))
    ax.set_yticklabels([r[0] for r in rows][::-1])
    ax.set_xlim(0, bound + 12)
    ax.set_ylim(0.2, len(rows) + 0.9)
    ax.set_xlabel("cycle count $m$")
    ax.set_title("Spectrum of cycle counts shrinks as connectivity grows")
    fig.tight_layout()
    path = FIGURES / "fig_spectrum.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def fig_extremal() -> str:
    """How does the minimum cycle count of an n-vertex 3-connected graph grow?"""
    data = _load("extremal_m3")["extremal_function_m3"]
    ns = [r["n"] for r in data]
    m3 = [r["m3"] for r in data]
    wheel = [r["c_wheel"] for r in data]
    comp = [r["conjectured_lower_bound"] for r in data]
    comp_l = [(n - 1) * (n - 2) / 2 for n in ns]
    comp = [r["conjectured_lower_bound"] for r in data]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.semilogy(ns, m3, "o-", color=COLOUR["accent"], label=r"$m_3(n)$ (computed, exhaustive)")
    ax.semilogy(ns, comp_l, "--", color=COLOUR["missing"], label=r"$\binom{n-1}{2}$ (Conj. C)")
    ax.semilogy(ns, wheel, "s:", color=COLOUR["grey"], label=r"$c(W_n)=(n-1)(n-2)+1$")
    ax.semilogy(ns, [r["c_complete"] for r in data], "^-.", color=COLOUR["green"],
                label=r"$c(K_n)$")
    for n, m in zip(ns, m3):
        ax.annotate(str(m), (n, m), textcoords="offset points", xytext=(0, 7),
                    fontsize=7, ha="center", color=COLOUR["accent"])
    ax.set_xlabel("order $n$")
    ax.set_ylabel("number of cycles (log scale)")
    ax.set_title("Extremal function $m_3(n)$ for 3-connected graphs")
    ax.set_xticks(ns)
    ax.set_ylim(2, 2e5)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    path = FIGURES / "fig_extremal.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def fig_theorem_a() -> str:
    """Is the minimum over k-connected graphs exactly c(K_{k+1})?"""
    data = _load("path_lemma_and_theorem_a")["theorem_a"]["minimum_over_k_connected"]
    ks = sorted(int(k) for k in data)
    obs = [data[str(k)]["min_cycles"] for k in ks]
    pred = [data[str(k)]["min_cycles"] for k in ks]
    ccomp = {str(n): v for n, v in _load("path_lemma_and_theorem_a")["theorem_a"]["c_complete"].items()}
    target = [ccomp[str(k + 1)] for k in ks]
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.plot(ks, target, "s--", color=COLOUR["missing"], label=r"$c(K_{k+1})$ (predicted)")
    ax.plot(ks, obs, "o-", color=COLOUR["present"], label="observed minimum")
    for k, o, t in zip(ks, obs, target):
        if o != t:
            ax.annotate(str(o), (k, o), textcoords="offset points", xytext=(4, 4), fontsize=7)
    ax.set_yscale("log")
    ax.set_xlabel("connectivity $k$")
    ax.set_ylabel("minimum number of cycles")
    ax.set_title("Theorem A: the minimum is exactly $c(K_{k+1})$, attained by $K_{k+1}$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = FIGURES / "fig_theorem_a.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def fig_cone() -> str:
    """Theorem B: the cycle is the unique cone minimiser."""
    rows = _load("cone_theorem")["rows"]
    ns = [r["base_order"] for r in rows]
    mn = [r["min_cone_cycles"] for r in rows]
    mx = [r["max_cone_cycles"] for r in rows]
    pred = [r["predicted_min"] for r in rows]
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.fill_between(ns, mn, mx, color=COLOUR["present"], alpha=0.18,
                    label="range over all 2-connected $F$")
    ax.semilogy(ns, mn, "o-", color=COLOUR["present"],
                label="minimum (attained only by $F=C_n$)")
    ax.semilogy(ns, pred, "--", color=COLOUR["missing"], label=r"predicted $n(n-1)+1$")
    for n, m in zip(ns, mn):
        ax.annotate(str(m), (n, m), textcoords="offset points", xytext=(0, 7),
                    fontsize=7, ha="center", color=COLOUR["present"])
    ax.set_xlabel("order $n$ of the base graph $F$")
    ax.set_ylabel(r"$c(K_1 \vee F)$ (log scale)")
    ax.set_title("Theorem B: wheels are the sparsest 3-connected cones")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    path = FIGURES / "fig_cone.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def fig_pathlemma() -> str:
    """The constant Q_k of the Path Lemma."""
    q = _load("path_lemma_and_theorem_a")["path_lemma"]["Q_table"]
    ks = sorted(int(k) for k in q)
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.semilogy(ks, [q[str(k)] for k in ks], "o-", color=COLOUR["accent"],
                label=r"$Q_k=p_{K_k}(x,y)$")
    ax.semilogy(ks, [2 ** (k - 1) for k in ks], ":", color=COLOUR["grey"],
                label=r"$2^{k-1}$")
    ax.set_xlabel("$k$")
    ax.set_ylabel("number of paths")
    ax.set_title("The Path Lemma constant grows like a factorial")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = FIGURES / "fig_path_lemma.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def fig_growth() -> str:
    """How fast do the enumerated classes grow, and how long do they take?"""
    data = _load("cardinalities")
    two = {int(k): v for k, v in data["two_connected_counts"].items()}
    three = {int(k): v for k, v in data["three_connected_counts"].items()}
    t2 = {int(k): v for k, v in data["timings_seconds"]["two_connected"].items()}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.6))
    ax1.semilogy(sorted(two), [two[n] for n in sorted(two)], "o-",
                 color=COLOUR["present"], label="2-connected")
    ax1.semilogy(sorted(three), [three[n] for n in sorted(three)], "s-",
                 color=COLOUR["accent"], label="3-connected")
    ax1.set_xlabel("order $n$")
    ax1.set_ylabel("isomorphism classes")
    ax1.set_title("Class counts (log scale)")
    ax1.legend(fontsize=8)
    ns = sorted(t2)
    ax2.semilogy(ns, [t2[n] for n in ns], "o-", color=COLOUR["present"])
    ax2.set_xlabel("order $n$")
    ax2.set_ylabel("generation time (s)")
    ax2.set_title("Cost of the 2-connected generator")
    fig.tight_layout()
    path = FIGURES / "fig_growth.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return str(path)


def main() -> list[str]:
    print("stage 6: figures")
    FIGURES.mkdir(parents=True, exist_ok=True)
    return [
        fig_spectra(),
        fig_extremal(),
        fig_theorem_a(),
        fig_cone(),
        fig_pathlemma(),
        fig_growth(),
    ]


if __name__ == "__main__":
    main()