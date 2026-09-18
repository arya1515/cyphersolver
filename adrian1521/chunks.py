import re
def cipher_tokens():
    toks=[]
    for line in open('transcription.txt',encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        m=re.match(r'(p\d\.\d\d)\s+(.*)',line)
        if not m: continue
        lab,body=m.groups()
        body=re.sub(r'\[[^\]]*\]','',body)          # drop editorial notes / clear text
        body=re.sub(r'\(.*?\)','',body)
        for t in re.findall(r'\{[^}]*\}|\S+',body):
            toks.append((lab,t))
    return toks
def plain_words():
    t=open('gredilla_1880s.txt',encoding='utf-8').read()
    t=re.sub(r'#.*','',t)
    return t.split()
if __name__=='__main__':
    ct=cipher_tokens(); pw=plain_words()
    # plaintext starts at "la una es" -> after 'avisar'
    start=pw.index('avisar')+1
    pw=pw[start:]
    ci=[i for i,(l,t) in enumerate(ct) if t=='xif']
    pi=[i for i in range(len(pw)-1) if pw[i].startswith('V.') and pw[i+1].startswith('M')]
    print(len(ci),len(pi))
    cprev=0; pprev=0
    for k in range(max(len(ci),len(pi))):
        c=ci[k] if k<len(ci) else len(ct); p=pi[k] if k<len(pi) else len(pw)
        print(f'--- chunk {k}  [{ct[cprev][0]}]')
        print('  C:',' '.join(t for _,t in ct[cprev:c]))
        print('  P:',' '.join(pw[pprev:p]))
        cprev=c+1; pprev=p+2
