import sys, json, numpy as np, os
sys.path.insert(0,'sega1593')
import anneal_poly as A
from wordscore import WordScorer
WS=WordScorer()
cl=json.load(open('sega1593/control_poly_clusters.json')); tr=json.load(open('sega1593/control_poly_truth.json'))
names=A.PAIRS+A.CODES+['SEP']
toks=[]
for k in sorted(cl,key=int)[:10]: toks+=[c for c in cl[k] if c!=tr['junk']]
tokens=np.array(toks,np.int64)
def mk(d):
    mp=np.full(max(toks)+1,A.NCLS,np.int64)
    for c,v in d.items(): mp[int(c)]=names.index(v)
    return mp
cases={'truth':mk(tr['truth']),
'found':mk({0: 'ix', 1: 'an', 2: 'an', 3: 'cp', 4: 'cp', 5: 'dq', 6: 'er', 7: 'fs', 8: 'fs', 9: 'bo', 10: 'gt', 11: 'bo', 12: 'hu', 13: 'hu', 14: 'hu', 15: 'fs', 16: 'ly', 17: 'mz', 18: 'cp', 19: 'mz', 22: 'er', 23:'SEP',24:'SEP'}),
'degen2':mk({str(c):('er' if c%2 else 'an') for c in range(23)}|{'23':'SEP','24':'SEP'})}
import time
for name,mp in cases.items():
    t0=time.time(); sc,seq=A.beam_text(tokens,mp,A.tab,A.opt_n,A.opt_len,A.opt_seq,48); txt=''.join(A.ALPHA[i] for i in seq)
    w=WS.score(txt); print(name,'lm',round(sc,1),'word',round(w,3),'combined(mu=2)',round(sc+2*len(txt)*w,1),f'{time.time()-t0:.2f}s'); print('   ',txt[:120])
