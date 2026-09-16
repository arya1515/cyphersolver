import seg,sys,time
def toks_from_spaced(path):
    out=[]
    for x in open(path).read().split():
        if x[0] in '%:+-': out.append('#'+x)
        elif x.isalpha(): continue
        else: out.append(x)
    return out
if __name__=="__main__":
  restarts,iters=int(sys.argv[1]),int(sys.argv[2])
  for nsym in (40,60):
    for seed in (1,2,3):
        toks=toks_from_spaced(f'cpair{nsym}_{seed}.txt'); pl=open(f'cpair{nsym}_{seed}_plain.txt').read()
        t=time.time(); r=seg.solve(toks,restarts=restarts,iters=iters)
        acc=sum(a==b for a,b in zip(r[1],pl) if b!='#')/sum(1 for c in pl if c!='#')
        print(f'nsym={nsym} seed={seed} score={r[0]:.3f} windows={r[4]} acc={acc:.2f} {r[1][:70]} ({time.time()-t:.0f}s)',flush=True)
