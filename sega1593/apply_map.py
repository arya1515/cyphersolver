# Decode a page's cluster sequence with a given cluster->class mapping (JSON dict or python literal) via the beam decoder.
# usage: apply_map.py clusters.json page_key "MAP-literal" [beam]
import sys, json, ast, numpy as np
sys.path.insert(0,'sega1593')
import anneal_poly as A
cl=json.load(open(sys.argv[1]))
if sys.argv[2]!='-': cl=cl[sys.argv[2]]
mp_d=ast.literal_eval(sys.argv[3]); B=int(sys.argv[4]) if len(sys.argv)>4 else 200
names=A.PAIRS+A.CODES+['SEP']
for k in sorted(cl,key=int):
    toks=[c for c in cl[k]]
    mp=np.full(max(max(toks),max(mp_d))+1,A.NCLS,np.int64)
    for c,v in mp_d.items(): mp[c]=names.index(v)
    tokens=np.array(toks,np.int64)
    sc,seq=A.beam_text(tokens,mp,A.tab,A.opt_n,A.opt_len,A.opt_seq,B)
    print(k, ''.join(A.ALPHA[i] for i in seq))
