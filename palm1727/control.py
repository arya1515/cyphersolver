import random,re,sys,json,collections
random.seed(int(sys.argv[1]))
txt="der koenig von england hat in seiner rede an das parlament erklaeret dass er die rechte seiner krone und die handlung seiner unterthanen gegen alle angriffe schuetzen wolle und dass die flotte in bereitschaft stehe um gibraltar zu entsetzen wofern der kaiser und spanien die belagerung fortsetzen solten man glaubt hier allgemein dass die hollaender sich endlich erklaeren werden"
lines=[l.split() for l in open('ct.txt',encoding='utf8') if not l.startswith('#')]
toks=[t for l in lines for t in l]
syms=sorted({int(t) for t in toks if t.isdigit() and int(t)<100})
cnt=collections.Counter(int(t) for t in toks if t.isdigit() and int(t)<100)
plain=[c for c in txt if c!=' ']
# assign true key: letters by frequency get homophones proportionally
lf=collections.Counter(plain); order=[l for l,_ in lf.most_common()]
key={}; S=syms[:]; random.shuffle(S)
for i,s in enumerate(S): key[s]=order[i%len(order)]
inv=collections.defaultdict(list)
for s,l in key.items(): inv[l].append(s)
pi=0; out=[]
for l in lines:
    o=[]
    for t in l:
        if t.isdigit() and int(t)<100:
            c=plain[pi%len(plain)]; pi+=1
            while not inv[c]: c=plain[pi%len(plain)]; pi+=1
            o.append(str(random.choice(inv[c])))
        else: o.append(t)
    out.append(' '.join(o))
open('ct_control.txt','w',encoding='utf8').write('\n'.join(out)+'\n')
# pins: true values of the six most frequent symbols
used=collections.Counter(int(t) for l in out for t in l.split() if t.isdigit() and int(t)<100)
pins={str(s):key[s] for s,_ in used.most_common(6)}; pins['230']='der'
json.dump({'key':{str(k):v for k,v in key.items()},'pins':pins},open('control_key.json','w'))
print(json.dumps(pins))
