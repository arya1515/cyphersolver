from decrypt import dec
C="DGLNR"; k=None
for line in open('ct.txt',encoding='utf8'):
    line=line.rstrip('\n')
    if line.startswith('#') or not line: continue
    if line[1:2]==':': k=line[0]; line=line[2:]
    else: k=C[(C.index(k)+1)%5]
    print(k, dec(k,line))
