import sys, walign as W, align as A, walign2 as W2
sys.stdout.reconfigure(encoding='utf-8')
def red(t): return t if not t.isdigit() else 'r%d'%((int(t)//1000)*100+int(t)%100)
DATA=[(n,[red(x) for x in t],w) for n,t,w in W.DATA]
for x in sys.argv[3:]:
    n,cf,pf=x.split(':'); DATA.append((n,[red(x) for x in A.read_cipher(cf)],W.words(pf)))
best=None
for s in range(int(sys.argv[2])):
    r=W2.run(DATA,int(sys.argv[1]),s); print('seed',s,round(r[0]),flush=True)
    if best is None or r[0]<best[0]: best=r
tot,cnt,prev=best
for tok in sorted(cnt,key=lambda k:int(k[1:])):
    c={a:b for a,b in cnt[tok].items() if b>0}
    if c: print(tok, sorted(c.items(),key=lambda x:-x[1])[:6])
