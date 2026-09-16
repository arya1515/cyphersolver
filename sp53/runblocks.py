import homo,random,sys
lmf,path,iters,seed=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
random.seed(seed); lm=homo.LM(lmf); toks=homo.load_tokens(path)
B=homo.Blocks(toks,lm); best=B.anneal(iters,T0=30.0,T1=0.3,log=iters//10)
m=B.mapping(); t=''.join(m[v] for v in B.toks); print('BEST',round(best,1),'per-letter',round(best/len(t),3)); print(t)
print('BLOCKS',[(B.order[k], B.vals[(B.cuts[k-1] if k else 0)], B.vals[(B.cuts[k] if k < len(B.cuts) else B.n) - 1]) for k in range(len(B.order))])
