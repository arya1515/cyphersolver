import re,glob
def load(rec):
    f=glob.glob('decode/DOC_R%s_*.txt'%rec)[0]
    toks=[];plain=[]
    for line in open(f,encoding='utf-8',errors='replace'):
        line=line.rstrip('\n')
        if not line.strip() or line.startswith('#'): continue
        m=re.match(r'<(PLAINTEXT|CLEARTEXT) ?(\w*) (.*)>',line)
        if m:
            if m.group(1)=='PLAINTEXT': plain.append(m.group(3))
            continue
        if line.startswith('<'): continue
        for g in re.split(r'\s{2,}',line.strip()):
            toks.append(g.replace(' ',''))
    return toks,plain
if __name__=='__main__':
    import sys
    t,p=load(sys.argv[1]); print(' '.join(t)); print('---'); print(' / '.join(p))
