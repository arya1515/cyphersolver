"""Align a token transcription with a known plaintext (DP, each token = 1 unit: letter, syllable, word, or null).
usage: python align.py <trans.csv> <plaintext string file> [seed key json]"""
import sys,csv,json,re,collections
K=json.load(open('somogyi_key.json'))
units=set('abcdefghilmnopqrstuvxz')|set(K['syllables'].values())|set(K['geminates'].values())|{'et','in','che'}
seed=json.load(open(sys.argv[3])) if len(sys.argv)>3 else {}
toks=[]
for r in csv.DictReader(open(sys.argv[1],encoding='utf-8')):
    t=r['token'].strip()
    if t.startswith('[clear'): continue
    toks.append((int(r['line']),r['idx'],re.sub(r'\?$','',t)))
P=re.sub(r'[^a-z]','',open(sys.argv[2],encoding='utf-8').read().lower().replace('ch','ch'))
n=len(toks); m=len(P)
NEG=-1e9
# dp[i][j] best score aligning first i tokens with first j letters
import numpy as np
dp=np.full((n+1,m+1),NEG); bp={}
dp[0][0]=0
def sc(tok,unit):
    v=seed.get(tok)
    if v is not None: return 2.0 if v==unit else -3.0
    return 0.0
for i in range(n):
    tok=toks[i][2]
    for j in range(m+1):
        if dp[i][j]==NEG: continue
        # null (consume 0)
        s=dp[i][j]-1.5+(2.0 if seed.get(tok)=='null' else 0)
        if s>dp[i+1][j]: dp[i+1][j]=s; bp[(i+1,j)]=(j,'null')
        for L in (1,2,3):
            if j+L<=m:
                u=P[j:j+L]
                if u in units:
                    s=dp[i][j]+0.5+(0.3 if L>1 else 0)+sc(tok,u)
                    if s>dp[i+1][j+L]: dp[i+1][j+L]=s; bp[(i+1,j+L)]=(j,u)
# also allow skipping plaintext letters (cipher omitted) with penalty
        for L in (1,2,3):
            if j+L<=m:
                s=dp[i][j]-2.5*L
                if s>dp[i][j+L]: dp[i][j+L]=s; bp[(i,j+L)]=(j,'skip:'+P[j:j+L])
# end
best=max(range(m+1),key=lambda j:dp[n][j]); print('score',dp[n][best],'letters used',best,'of',m)
i,j=n,best; out=[]
while (i,j)!=(0,0):
    pj,u=bp[(i,j)]
    if u.startswith('skip'): out.append((None,u)); j=pj
    else: out.append((toks[i-1],u)); i-=1; j=pj
out.reverse()
json.dump([[t[0],t[1],t[2],u] for t,u in out if t is not None],open(sys.argv[1].replace('.csv','_aligned.json'),'w'))
votes=collections.defaultdict(collections.Counter)
line=None
for t,u in out:
    if t is None: print(f'   [{u}]',end=' '); continue
    if t[0]!=line: line=t[0]; print(f'\nL{line:02d}:',end=' ')
    print(f'{t[2]}={u}',end=' '); votes[t[2]][u]+=1
print('\n\n== token -> values')
for t,c in sorted(votes.items(),key=lambda x:-sum(x[1].values())):
    print(f'{t:8s} {dict(c)}')
