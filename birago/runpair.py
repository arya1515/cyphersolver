import json,sys,seg,time
P=json.load(open('pairings.json')); lo,hi=int(sys.argv[1]),int(sys.argv[2]); restarts=int(sys.argv[3]); iters=int(sys.argv[4])
for k in range(lo,hi):
    s=P[k]; toks=[('#'+t) if t=='|' else t for t in s]   # wavy sign as a break too
    t=time.time(); r=seg.solve(toks,restarts=restarts,iters=iters)
    print(f'pairing {k} score={r[0]:.3f} nsym={r[3]} win={r[4]} {r[1]} ({time.time()-t:.0f}s)',flush=True)
