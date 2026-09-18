"""Iterated local search for the fr. 3621 no. 97 substitution.

The random-move annealer in solve97b.py cannot converge on a 44-symbol homophonic cipher of
~1050 characters: a control with a KNOWN key reaches only 37-56% letter accuracy at -2.64
per character while the true key scores -1.62. The optimum is therefore well separated by
score and the failure is in the search, not in the information available.

This replaces the random move with a steepest-ascent sweep (for each symbol in turn, try
every plaintext letter and keep the best), run to convergence, then kicked out of the local
optimum by perturbing a few symbols, keeping the best key ever seen. Tuned against the
control until it recovers known keys, then applied to the manuscript.
"""
import random, math, sys

def sweep(st, NA, order=None, rnd=None):
    """One steepest-ascent pass over all symbols. Returns True if anything improved."""
    ns=st.P.ns
    idxs=list(range(ns))
    if rnd: rnd.shuffle(idxs)
    improved=False
    for si in idxs:
        cur=st.obj(); best=st.key[si]; bestv=cur
        for L in range(NA):
            if L==st.key[si]: continue
            u=st.set(si,L)
            if u is None: continue
            v=st.obj()
            if v>bestv: bestv=v; best=L
            st.undo(u)
        if best!=st.key[si]:
            st.set(si,best); improved=True
    return improved

def ils(P, State, NA, iters=400, kick=4, mu=0.0, seed=1, FREQ=None, log=None):
    rnd=random.Random(seed)
    fr=sorted(range(NA), key=lambda i:-FREQ[i])
    order=[s for s,_ in P.cnt.most_common()]
    key=[fr[0]]*P.ns
    for rank,si in enumerate(order): key[si]=fr[min(rank,NA-1)]
    st=State(P,key,mu)
    for _ in range(40):
        if not sweep(st,NA,rnd=rnd): break
    best=st.obj(); bestk=list(st.key)
    for it in range(iters):
        # kick
        for _ in range(kick):
            st.set(rnd.randrange(P.ns), rnd.randrange(NA))
        for _ in range(40):
            if not sweep(st,NA,rnd=rnd): break
        c=st.obj()
        if c>best:
            best=c; bestk=list(st.key)
            if log: print(f'  ils {it:4d}  obj {c:.4f}', file=log, flush=True)
        else:
            # restart from best
            for si in range(P.ns): st.set(si,bestk[si])
    return best,bestk
