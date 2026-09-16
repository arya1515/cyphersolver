import numpy as np,collections,json,sys
def sukhotin(seq,nvow=None):
    syms=sorted(s for s in set(seq) if s is not None); si={s:i for i,s in enumerate(syms)}; n=len(syms)
    M=np.zeros((n,n))
    for a,b in zip(seq,seq[1:]):
        if a is None or b is None: continue
        M[si[a],si[b]]+=1; M[si[b],si[a]]+=1
    np.fill_diagonal(M,0)
    vow=[]; rows=M.sum(1).copy(); cons=set(range(n))
    while True:
        cand=[i for i in cons if rows[i]>0]
        if not cand: break
        i=max(cand,key=lambda k:rows[k])
        if rows[i]<=0: break
        vow.append(i); cons.discard(i)
        for j in cons: rows[j]-=2*M[i,j]
        if nvow and len(vow)>=nvow: break
    return {syms[i] for i in vow},syms
def seq_from_toks(toks):
    out=[]
    for t in toks:
        out.append(None if t[0]=='#' else t)
    return out
if __name__=='__main__':
    import control_match
    for seed in range(4):
        toks,pl,key=control_match.make(seed); seq=seq_from_toks(toks)
        inv={v:k for k,vs in key.items() for v in vs}
        V,syms=sukhotin(seq)
        truth={s for s in syms if inv[s] in 'aeiou'}
        tp=len(V&truth); fp=len(V-truth); fn=len(truth-V)
        # weighted by token count
        c=collections.Counter(s for s in seq if s)
        acc=sum(c[s] for s in syms if (s in V)==(s in truth))/sum(c.values())
        print(f'control {seed}: symbols {len(syms)} vowel syms {len(truth)} predicted {len(V)} tp {tp} fp {fp} fn {fn} token-weighted acc {acc:.2f}')
    P=json.load(open('pairings.json')); toks=[t if t!='|' else '#|' for t in P[0]]; seq=seq_from_toks(toks)
    V,syms=sukhotin(seq); c=collections.Counter(s for s in seq if s)
    print('target: symbols',len(syms),'vowel-class',len(V),'tokens in vowel class',sum(c[s] for s in V),'of',sum(c.values()))
    print('vowel class:',sorted(V,key=lambda s:-c[s]))
    print('consonant class:',sorted(set(syms)-V,key=lambda s:-c[s]))
