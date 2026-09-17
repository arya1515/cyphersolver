"""predline.py PAGE LINE [PAGE LINE ...] : the current machine reading of a line, one entry per
token index, to check against img/idx/<page>_<NN>.png. '_' = the decoder dropped the token."""
import json, sys
b=json.load(open('raince140_tokens.json'))
try: pred=json.load(open('pred.json'))
except FileNotFoundError: pred={}
gold={}
for ln in open('gold/labels.txt'):
    if ln.startswith('#') or not ln.strip(): continue
    p,l,s=ln.split(); gold[(p,int(l))]=s
args=sys.argv[1:]
for i in range(0,len(args),2):
    page,L=args[i],int(args[i+1])
    row=sorted([t for t in b['tokens'] if t['page']==page and t['line']==L-1],key=lambda t:t['x0'])
    cells=[]
    for j,t in enumerate(row,1):
        c=pred.get(f"{t['page']}|{t['line']}|{t['x0']}",'?')
        cells.append(f"{j}{c}")
    print(f"{page} {L:02d}  n={len(row)}  {'DONE' if (page,L) in gold else ''}")
    for k in range(0,len(cells),10):
        print('   ', ' '.join(f"{c:>4}" for c in cells[k:k+10]))
    print('    guess:', ''.join(pred.get(f"{t['page']}|{t['line']}|{t['x0']}",'?') for t in row))
