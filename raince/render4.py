"""Render the cluster stream with map_lm.json, one line per manuscript line."""
import json, pickle, sys
m={int(k):v for k,v in json.load(open('map_lm.json')).items()}
for kv in sys.argv[1:]:
    k,v=kv.split('='); m[int(k)]= '' if v=='_' else v
d=json.load(open('raince_tokens.json'))
out=[]
for page in d['regions']:
    ts=[t for t in d['tokens'] if t['page']==page]
    n=len(d['regions'][page]['lines'])
    out.append('## '+page)
    for k in range(n):
        row=sorted([x for x in ts if x['line']==k],key=lambda x:x['x0'])
        out.append(f'{k+1:02d} '+''.join(m.get(t['cl'],'') for t in row))
open('draft4.txt','w').write('\n'.join(out)+'\n')
print('\n'.join(out))
