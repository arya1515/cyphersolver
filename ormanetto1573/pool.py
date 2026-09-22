from tok import load
def pooled():
    seqs=[]
    for p in load():
        if not p: continue
        s=''.join(d for d,a,u in p).replace('41','X')
        seqs.append(list(s))
    for l in open('../ormanetto1576/r118_cipher.txt'):
        if not l.startswith('#'): seqs.append(list(l.strip()))
    return seqs
