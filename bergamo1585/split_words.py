"""Insert word breaks into a run-on Italian letter stream with the spaced it-cinquecento model (beam search).
Bracketed tokens ([NAME], [123?]) are kept whole as words. usage: python split_words.py < stream > text"""
import os,re,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from lang import lm
M=lm.load('it-cinquecento',spaces=True)
def split(run,B=40):
    beam=[(0.0,' ')]
    for ch in run:
        nb=[]
        for sc,s in beam:
            nb.append((sc+M.score(s[-5:]+ch)-M.score(s[-5:]),s+ch))
            if s[-1]!=' ': nb.append((sc+M.score(s[-5:]+' '+ch)-M.score(s[-5:]),s+' '+ch))
        beam=sorted(nb,reverse=True)[:B]
    return beam[0][1].strip()
out=[]
for line in sys.stdin:
    line=line.rstrip('\n')
    if not line or line.startswith('=='): out.append(line);continue
    parts=re.split(r'(\[[^\]]*\])',line)
    out.append(' '.join(split(p.lower()) if not p.startswith('[') else p for p in parts if p.strip()))
print('\n'.join(out))
