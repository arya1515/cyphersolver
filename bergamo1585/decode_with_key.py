import re,sys
K={}
for l in open(sys.argv[1],encoding='utf8',errors='replace'):
    m=re.match(r'^(\S+) - (.*)$',l.strip())
    if m:
        for c in m[1].split('|'): K[c]=m[2].split('|')[0]
out=[];bad=0;tot=0
for l in open(sys.argv[2],encoding='utf8',errors='replace'):
    if l.startswith('#'): continue
    l=re.sub(r'<CLEARTEXT[^>]*>',lambda m:' ['+m[0][10:-1].strip()+'] ',l)
    toks=re.findall(r'\[[^\]]*\]|\d[^\s\d]*',l)
    i=0;w=''
    while i<len(toks):
        t=toks[i]
        if t.startswith('['): out.append(w+t);w='';i+=1;continue
        if t=='8': out.append(w);w='';i+=1;continue
        if re.search(r'[^\d]',t) or i+1>=len(toks):  # marked single
            out.append(w+'<'+t+'>');w='';i+=1;continue
        a=toks[i+1]
        if a.startswith('['): w+='<'+t+'>';i+=1;continue
        code=t+a
        if re.search(r'[^\d]',a):
            if i+2<len(toks) and not toks[i+2].startswith('[') and toks[i+2]!='8':
                pass
            w+=K.get(code,'<'+code+'>');i+=2;tot+=1;continue
        tot+=1
        if code in K: w+=K[code]
        else: w+='<'+code+'>';bad+=1
        i+=2
    out.append(w)
print(' '.join(x for x in out if x))
print('\n#pairs',tot,'unknown',bad,file=sys.stderr)
