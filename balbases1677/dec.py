import json,collections,sys,glob
sys.stdout.reconfigure(encoding='utf-8')
from align2 import read_tx,ctok
P=json.load(open('paths.json',encoding='utf-8'))
cnt=collections.defaultdict(collections.Counter)
for r,p in P.items():
    for tok,sub in p:
        if tok is not None and len(sub)<=4: cnt[tok][sub]+=1
KEY={}
for tok,c in cnt.items():
    (s,n),=c.most_common(1); tot=sum(c.values())
    if n>=2 and n/tot>=0.5: KEY[tok]=s
if __name__=='__main__':
    json.dump(dict(sorted(KEY.items())),open('key_auto.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    for f in sys.argv[1:]:
        t,_=read_tx(f)
        print(f); print(' '.join(KEY.get(ctok(x),'['+x+']') if KEY.get(ctok(x),'x')!='' else '·' for x in t)); print()
