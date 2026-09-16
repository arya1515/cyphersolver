# DP: choose for each marked digit a code-group span [m-a, m+b] (a+b+1<=maxw) so that all plain-digit runs have even length.
# Items: plain digit, marked digit (start of a code group), '|' wavy sign (separator or ignored), letters (dropped or separators).
import sys,itertools
from functools import lru_cache
g=open('ct2.txt').read().split()
def solve(letters_mode='drop',wavy_sep=True,maxw=3):
    items=[x for x in g if not (x.isalpha() and letters_mode=='drop')]
    n=len(items)
    # groups: for each marked m, candidate spans as (start,end) inclusive
    marks=[i for i,x in enumerate(items) if x[0].isdigit() and len(x)>1]
    def plain(j): return 0<=j<n and items[j][0].isdigit() and len(items[j])==1
    cands={}
    for m in marks:
        c=[]
        for a in range(maxw):
            for b in range(maxw-a):
                if all(plain(j) for j in range(m-a,m)) and all(plain(j) for j in range(m+1,m+b+1)): c.append((m-a,m+b))
        cands[m]=c
    sys.setrecursionlimit(10000)
    # scan left to right; state: (index, parity of current run, covered_until)
    @lru_cache(None)
    def f(i,par,cov):
        # returns number of solutions from position i; cov = last covered index (>=i-1 means item i covered)
        if i==n: return 1 if par==0 else 0
        x=items[i]
        if i<=cov: return f(i+1,par,cov)      # covered by a group already started
        if x=='|':
            if wavy_sep: return f(i+1,0,cov) if par==0 else 0
            return f(i+1,par,cov)
        if x.isalpha():
            return f(i+1,0,cov) if par==0 else 0   # letters as separators (letters_mode='sep')
        if len(x)>1:   # marked digit: choose span; spans starting before i would have had to be chosen earlier -> handle by lookahead
            tot=0
            for (s,e) in cands[i]:
                if s<i: continue   # backward spans handled via lookahead below
                if par!=0: return 0 if not any(s<i for s,e in cands[i]) else tot
                tot+=f(e+1,0,max(cov,e))
            return tot
        # plain digit: either continues run, or is the first digit of a backward-extending group of the next mark
        tot=0
        # option 1: plain letter digit
        tot+=f(i+1,par^1,cov)
        # option 2: start a code group here that includes a later mark within maxw
        if par==0:
            for k in range(1,maxw):
                m=i+k
                if m<n and len(items[m])>1 and items[m][0].isdigit():
                    for (s,e) in cands[m]:
                        if s==i: tot+=f(e+1,0,max(cov,e))
                    break
                if not plain(m): break
        return tot
    return f(0,0,-1)
for lm in ('drop','sep'):
    for ws in (True,False):
        for mw in (2,3):
            print(f'letters={lm} wavy_sep={ws} maxw={mw}: solutions {solve(lm,ws,mw)}',flush=True)
