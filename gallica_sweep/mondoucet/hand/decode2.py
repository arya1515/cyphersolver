import sys; sys.path.insert(0,'hand'); from key_manual import KEY
for f in sys.argv[1:]:
    for l in open(f,encoding='utf-8'):
        if ':' not in l or l.startswith('#'): continue
        lab,rest=l.split(':',1); toks=rest.split(); out=[]
        for t in toks:
            k=KEY.get(t,'{'+t+'}')
            if k=='': continue
            out.append(k if '/' not in k else '('+k+')')
        print(lab+':',''.join(out))
