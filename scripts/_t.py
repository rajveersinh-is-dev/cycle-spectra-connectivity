import sys; sys.path.insert(0, "src")
from cycle_spectra import *
from cycle_spectra.bounds import lower_bound, B_order
g = wheel(8)
print("W_8 c =", count_cycles(g), "kappa =", vertex_connectivity(g), "B_fund =", B_fundamental(g), "B_star =", B_star(g), "B_dom =", B_dominating(g))
print("cone_cycles(W_6 minus hub) check:", cone_cycles(prism_graph(4), 0))
print("B_order(34, 3) =", B_order(34, 3))
print("2conn minimal counts:", list(exhaustive_two_connected_cycle_counts(7).items())[:12])
