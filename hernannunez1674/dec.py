import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
K=json.load(open('../balbases1677/key.json',encoding='utf8'))
K.update({'d':'que','N':'','N_':'','30':'p','6+':'o','4':'t','161':'resolucion','os':'para','a':'','>':''})   # unstruck d as transcribed by DECODE = struck d
for f in sys.argv[1:]:
    C=[];M=[]
    for line in open(f,encoding='utf8'):
        if line.startswith('C:'): C+=line[2:].split()
        elif line.startswith('M:'): M.append(line[2:].strip())
    out=[];un=0
    for t in C:
        t2=t.strip('()=').rstrip('?')
        v=K.get(t2)
        if v is None: out.append('['+t+']');un+=1
        else: out.append(v)
    print('=====',f,len(C),'tokens, unknown',un)
    print(''.join(out));print('--- margin:');print(' '.join(M))
