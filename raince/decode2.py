"""Beam decode over the classifier posteriors (post.npy) plus the space-free French 6-gram LM.
Writes draft9.txt and scores it against the hand-labelled lines in gold/labels.txt."""
import json, pickle, sys, collections
import numpy as np
D=pickle.load(open('frns6.pkl','rb')); N=D['n']; P=D['p']; BACK=D['back']
CLS=json.load(open('post_cls.json')); LPV=np.load('post.npy')
b=json.load(open('raince140_tokens.json'))
LMW=float(sys.argv[1]) if len(sys.argv)>1 else 0.7
BEAM=int(sys.argv[2]) if len(sys.argv)>2 else 900
TOPK=6
def lp(ctx,ch):
    d=P.get(ctx); return d.get(ch,BACK) if d else BACK
order={(t['page'],t['line'],t['x0']):i for i,t in enumerate(b['tokens'])}
out=[]; pred={}
for page in b['regions']:
    rows=[sorted([x for x in b['tokens'] if x['page']==page and x['line']==k],key=lambda x:x['x0'])
          for k in range(len(b['regions'][page]['lines']))]
    stream=[order[(t['page'],t['line'],t['x0'])] for r in rows for t in r]
    beams={' '*(N-1):(0.0,())}
    for i in stream:
        v=LPV[i]; cand=np.argsort(-v)[:TOPK]; nb={}
        for ctx,(sc,path) in beams.items():
            for j in cand:
                ch=CLS[j]; e=float(v[j])
                if ch=='_': k2=ctx; s=sc+e; p=path+('_',)
                else:
                    c2 = 'u' if ch=='v' else ch
                    s=sc+e+LMW*lp(ctx,c2); k2=(ctx+c2)[-(N-1):]; p=path+(ch,)
                if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,p)
        beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:BEAM])
    sc,path=max(beams.values(),key=lambda v:v[0])
    out.append('## '+page); j=0
    for k,r in enumerate(rows):
        for t,ch in zip(r,path[j:j+len(r)]): pred[order[(t['page'],t['line'],t['x0'])]]=ch
        out.append(f'{k+1:02d} '+''.join(c for c in path[j:j+len(r)] if c!='_')); j+=len(r)
open('draft9.txt','w').write('\n'.join(out)+'\n')
tot=ok=0
for ln in open('gold/labels.txt'):
    if ln.startswith('#') or not ln.strip(): continue
    p,l,s=ln.split(); L=int(l)-1
    row=sorted([t for t in b['tokens'] if t['page']==p and t['line']==L],key=lambda t:t['x0'])
    for t,ch in zip(row,s):
        if ch in '?C': continue
        g=pred[order[(t['page'],t['line'],t['x0'])]]
        tot+=1; ok += (g==ch or (ch in 'uv' and g in 'uv'))
print(f'LM weight {LMW}: token accuracy on gold lines {ok}/{tot} = {ok/tot:.3f}')

json.dump({f"{t['page']}|{t['line']}|{t['x0']}": pred[order[(t['page'],t['line'],t['x0'])]]
           for t in b['tokens']}, open('pred.json','w'))
