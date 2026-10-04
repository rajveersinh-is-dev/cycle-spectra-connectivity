import sys, time; sys.path.insert(0, "src")
from cycle_spectra.generation import two_connected_graphs, three_connected_graphs
from cycle_spectra.cycles import count_cycles
t=time.time(); g9 = two_connected_graphs(9); print("2conn(9)", len(g9), f"{time.time()-t:.1f}s", flush=True)
t=time.time(); g10 = three_connected_graphs(10); print("3conn(10)", len(g10), f"{time.time()-t:.1f}s", flush=True)
best=None; mins=[]
for g in g10:
    c=count_cycles(g)
    if best is None or c<best: best,mins=c,[g]
    elif c==best: mins.append(g)
print("m_3(10) =", best, "num minimisers", len(mins), [m.degrees() for m in mins[:4]], flush=True)
