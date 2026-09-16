# Word-segmentation log-score for spaceless Italian: Viterbi over an early-modern word list (u=v, i=j), unknown letters at a penalty.
import json,math,numpy as np
W=json.load(open('../vatican5/it_words.json'))
tot=sum(c for w,c in W); LOGP={}
for w,c in W:
    w=w.replace('v','u').replace('j','i')
    LOGP[w]=max(LOGP.get(w,-99),math.log(c/tot))
MAXL=max(len(w) for w in LOGP); UNK=-12.0
def score(text):
    """text: letters and '#'. Segments between '#' are scored independently; returns total log-score and segmentation."""
    total=0.0; segs=[]
    for chunk in text.split('#'):
        if not chunk: continue
        n=len(chunk); best=[-1e9]*(n+1); back=[0]*(n+1); best[0]=0.0
        for i in range(1,n+1):
            for l in range(1,min(MAXL,i)+1):
                w=chunk[i-l:i]; lp=LOGP.get(w)
                if lp is None:
                    if l==1: lp=UNK
                    else: continue
                if best[i-l]+lp>best[i]: best[i]=best[i-l]+lp; back[i]=l
        total+=best[n]; i=n; out=[]
        while i>0: out.append(chunk[i-back[i]:i]); i-=back[i]
        segs.append(' '.join(reversed(out)))
    return total,' # '.join(segs)
if __name__=='__main__':
    for t in ['lasupplicoafarlosaperealreetallaregina#etnonaltro','cnda#riiten#otiratamanientemapo#smooanniet#rrelinteesedo#aoagenerittor','hesisieuouenutiadasrasuamaestaattendonoasegguitiarfocrteififcariaterrapiuchema']:
        s,seg=score(t); print(round(s/len(t.replace('#','')),2),seg)
