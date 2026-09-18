import json,sys,collections
key=json.load(open('hand/key_counts.json'))
best={t:max(c,key=c.get) for t,c in key.items()}
conf={t:max(c.values())/sum(c.values()) for t,c in key.items()}
for f in sys.argv[1:]:
    for l in open(f,encoding='utf-8'):
        if ':' not in l or l.startswith('#'): continue
        lab,rest=l.split(':',1); toks=rest.split()
        out=[]
        for t in toks:
            if t in best and sum(key[t].values())>=3: out.append(best[t] if conf[t]>=0.5 else best[t].upper())
            else: out.append('['+t+']')
        print(lab+':',''.join(out))
