import json,sys,collections
code=sys.argv[1]; paths=json.load(open(sys.argv[2])); keyf=f'key_{code}.json'
k=json.load(open(keyf,encoding='utf8'))
seeded=set(int(x) for x in k)
vals=collections.defaultdict(list)
for name,p in paths.items():
    steps=[(i,t,s) for i,t,s in p if t is not None]
    for n,(i,t,s) in enumerate(steps):
        if s in('P','C'): continue
        left=steps[n-1][1] in seeded and steps[n-1][2] not in('P','C') if n>0 else False
        right=steps[n+1][1] in seeded and steps[n+1][2] not in('P','C') if n+1<len(steps) else False
        vals[t].append((s,left and right))
new={}
for t,v in vals.items():
    if t in seeded: continue
    ss=set(s for s,_ in v)
    if len(v)>=2 and len(ss)==1 and len(v[0][0])<=8: new[str(t)]=v[0][0]
    elif len(v)==1 and v[0][1] and len(v[0][0])<=6: new[str(t)]=v[0][0]
k.update(new); json.dump(k,open(keyf,'w',encoding='utf8'),ensure_ascii=False)
print('added',len(new),'total',len(k)); print(new)
