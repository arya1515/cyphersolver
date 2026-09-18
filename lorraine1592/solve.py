"""Homophonic substitution solver for fr. 3621 no. 97, with incremental 4-gram scoring.

Each cipher cluster maps independently to a plaintext letter, so a letter may have several cipher forms
(as these League ciphers do) and over-segmentation from the glyph clustering is absorbed. Scored by a
4-gram model of 16th-century French (Montaigne, spaceless). Simulated annealing with restarts.
usage: python3 solve.py CLUSTERFILE [restarts] [iters] [seed]
"""
import sys, json, random, math, collections

M=json.load(open('src/fr4ns.json'))
LP=M['lp']; FLOOR=M['floor']; AL=M['al']; FREQ=M['freq']

def load(path):
    rows=[l.strip() for l in open(path) if l.strip() and not l.startswith('#')]
    return ''.join(rows)

def solve(ct, restarts=8, iters=40000, seed=0):
    rnd=random.Random(seed)
    n=len(ct)
    syms=sorted(set(ct))
    pos=collections.defaultdict(list)
    for i,c in enumerate(ct): pos[c].append(i)
    # windows affected by a change at position i: starts i-3..i
    aff={s: sorted({max(0,min(p-k, n-4)) for p in pos[s] for k in range(4)}) for s in syms}
    g=LP.get
    def win(dec, st): return g(dec[st]+dec[st+1]+dec[st+2]+dec[st+3], FLOOR)
    sizes=collections.Counter(ct)
    targets={L: len(ct)*FREQ.get(L,0.0) for L in AL}
    MU=float(__import__('os').environ.get('MU','0.9'))
    def fpen(m):
        got=collections.Counter()
        for s_,c_ in sizes.items(): got[m[s_]]+=c_
        return sum(abs(got.get(L,0)-targets[L]) for L in AL)
    freq=collections.Counter(ct)
    order=[s for s,_ in freq.most_common()]
    lets=sorted(AL, key=lambda c:-FREQ.get(c,0))
    best=None
    for r in range(restarts):
        m={}
        for i,s in enumerate(order):
            m[s]=lets[min(int(i*len(lets)/max(1,len(order))), len(lets)-1)]
        if r:
            for s in syms:
                if rnd.random()<0.35: m[s]=rnd.choice(AL)
        dec=[m[c] for c in ct]
        total=sum(win(dec,i) for i in range(n-3)) - MU*fpen(m)
        T0,T1=0.9,0.015
        for it in range(iters):
            T=T0*(T1/T0)**(it/iters)
            s=rnd.choice(syms); old=m[s]; new=rnd.choice(AL)
            if new==old: continue
            ws=aff[s]
            before=sum(win(dec,i) for i in ws) - MU*fpen(m)
            for p in pos[s]: dec[p]=new
            m[s]=new
            after=sum(win(dec,i) for i in ws) - MU*fpen(m)
            d=after-before
            m[s]=old
            if d>0 or rnd.random()<math.exp(min(0.0,d)/max(1e-9,T*25)):
                total+=d; m[s]=new
            else:
                for p in pos[s]: dec[p]=old
        txt=''.join(dec)
        total=sum(win(dec,i) for i in range(n-3)) - MU*fpen(m)
        if best is None or total>best[0]: best=(total,dict(m),txt)
        print(f'  restart {r}: {total/ n:.3f}/char  {txt[:72]}', file=sys.stderr)
    return best

if __name__=='__main__':
    ct=load(sys.argv[1])
    R=int(sys.argv[2]) if len(sys.argv)>2 else 8
    I=int(sys.argv[3]) if len(sys.argv)>3 else 40000
    S=int(sys.argv[4]) if len(sys.argv)>4 else 0
    print(f'ciphertext {len(ct)} glyphs, {len(set(ct))} distinct', file=sys.stderr)
    sc,m,dec=solve(ct,R,I,S)
    print(f'best {sc/len(dec):.3f} per char', file=sys.stderr)
    print(dec)
    print('\nkey:', json.dumps(m, sort_keys=True), file=sys.stderr)
