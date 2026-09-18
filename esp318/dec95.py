import pickle, numpy as np, sys
from scipy.cluster.hierarchy import fcluster
from assign95 import CL2L
d = pickle.load(open('f122r_glyphs.pkl','rb'))
lab = fcluster(d['Z'], 110, 'maxclust')
meta = d['meta']
order = sorted(range(len(meta)), key=lambda i: (meta[i]['line'], meta[i]['x0']))
lines = {}
for i in order:
    lines.setdefault(meta[i]['line'], []).append(CL2L.get(int(lab[i]), '.'))
txt = []
for ln in sorted(lines):
    txt.append(''.join(lines[ln]))
open('f122r_decode.txt','w').write('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(txt)))
cov = sum(c != '.' for t in txt for c in t); tot = sum(len(t) for t in txt)
print(f'glyphs {tot}, assigned {cov} ({cov/tot:.0%})')
print('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(txt)))
