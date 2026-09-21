"""Apply S. Tomokiyo's partial Cecil-Norris 1568 table to Forbes's Norreys groups (transcription.txt).
Token->letter map read off the table (signs in any orientation). '?' = sign not in the table.
Note: transcription token 'J' covers two shapes (2-with-f tail = r; 4-with-hook = e); map as r, see NOTES.
Control: same tokens, letters shuffled among mapped tokens (seeded), scored by dictionary-word hits."""
import random, re, sys
M = {'T':'a','perp':'a','dash-a':'a','Gam':'a','xi':'b','hash':'c','L':'d','n':'e','cup':'e','sqc':'e',
     'E':'e','varpi':'f','cap':'h','v':'h','flat':'i','phi':'i','oo':'l','m':'n','sh':'n','lam':'o','P':'o',
     '4':'p','4:':'p','2':'r','J':'r','3':'s','3b':'s','3u':'s','s2':'t','s:':'t','5:':'t',':t':'t','7':'u',
     '7:':'u','7d':'u','9':'y','X':'x','o':'o','rc':'m','sig':'r','+':'a'}
def groups():
    cur=None
    for ln in open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','transcription.txt'),encoding='utf-8'):
        ln=ln.strip()
        if ln.startswith('['): cur=ln.split()[0][1:]
        elif re.match(r'\d+:',ln):
            k,v=ln.split(':',1); yield cur,k,v.split()
def dec(toks,m): return ''.join(('#' if t.startswith('#') else m.get(t,'?')) for t in toks)
WORDS='the and that his her lord papists realms rothes earl stayed reason ruin master steward have with'.split()
def score(m): return sum(dec(t,m).count(w) for _,_,t in groups() for w in WORDS)
if __name__=='__main__':
    for d,k,t in groups(): print(d,k.rjust(2),dec(t,M))
    real=score(M); vals=list(M.values()); r=random.Random(1); sc=[]
    for _ in range(1000):
        r.shuffle(vals); sc.append(score(dict(zip(M,vals))))
    print('word hits real',real,'| shuffled mean %.2f max %d'%(sum(sc)/len(sc),max(sc)))
