import sys, json, numpy as np
sys.path.insert(0,'sega1593'); sys.argv=[sys.argv[0]]+sys.argv[1:]
import anneal_poly as A
cl=json.load(open('sega1593/control_poly_clusters.json')); tr=json.load(open('sega1593/control_poly_truth.json'))
names=A.PAIRS+A.CODES+['SEP']
toks=[]
for k in sorted(cl,key=int)[:10]: toks+=[c for c in cl[k] if c!=tr['junk']]
tokens=np.array(toks,np.int64)
mp=np.full(max(toks)+1,A.NCLS,np.int64)
for c,v in tr['truth'].items(): mp[int(c)]=names.index(v)
for B in (64,400):
    s,nl=A.beam(tokens,mp,A.tab,A.opt_n,A.opt_len,A.opt_seq,B); print('truth B',B,round(s,1),round(s/len(tokens),3))
found={0: 'fs', 1: 'ix', 2: 'hu', 3: 'dq', 4: 'ly', 5: 'cp', 6: 'er', 7: 'ly', 8: 'fs', 9: 'gt', 10: 'an', 11: 'bo', 12: 'hu', 13: 'an', 14: 'mz', 15: 'an', 16: 'gt', 17: 'dq', 18: 'cp', 19: 'bo', 22: 'an', 23: 'SEP', 24: 'SEP'}
mp2=np.full(max(toks)+1,A.NCLS,np.int64)
for c,v in found.items(): mp2[c]=names.index(v)
for B in (64,400):
    s,nl=A.beam(tokens,mp2,A.tab,A.opt_n,A.opt_len,A.opt_seq,B); print('found B',B,round(s,1))
txt,sc=A.decode_text(tokens,mp,400); print(txt[:300])
