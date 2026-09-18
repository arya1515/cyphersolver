import json,sys
from solve import beam, segment
import os;key=json.load(open(os.environ.get("KEY","key.json")))
AL=list('abcdefghilmnopqrstuxyz')
def decode(line, width=300):
    toks=line.split()
    cand={t:(key[t] if t in key else AL) for t in set(toks)}
    b=beam(toks,cand,width)
    return b[0][0]
if __name__=='__main__':
    out=[]
    for line in open(sys.argv[1],encoding='utf-8'):
        line=line.strip()
        if not line: continue
        out.append(decode(line))
    joined=''.join(out)
    print(segment(joined))
    print()
    for i,o in enumerate(out,1): print(i, segment(o))
