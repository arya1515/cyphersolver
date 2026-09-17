import json, sys
m={int(k):v for k,v in json.load(open('map140.json')).items()}
d=json.load(open('raince140_tokens.json'))
out=[]
for page in d['regions']:
    ts=[t for t in d['tokens'] if t['page']==page]
    n=len(d['regions'][page]['lines'])
    out.append('## '+page)
    for k in range(n):
        row=sorted([x for x in ts if x['line']==k],key=lambda x:x['x0'])
        out.append(f'{k+1:02d} '+''.join('' if m[t['cl']]=='_' else m[t['cl']] for t in row))
open('draft5.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
