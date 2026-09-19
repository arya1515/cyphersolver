# Tabulate token -> letter from align_113.txt ; writes table_113.txt
import re, collections
KEY = {  # Tomokiyo key / TOKENS.md letter(s) for each token (my split tokens mapped to the family's key value)
 'q':'a','T':'a','x':'a','f':'a','y':'b','z':'c','v':'d','6':'d','n':'d','g':'e','D':'e','t':'e','e3':'e','S':'e',
 'w':'et','12':'g','19':'f','9':'f','+':'h','7':'h','pi':'i','6^':'i','33':'i','ph':'i','60':'i/y','I':'l','II':'l',
 'p':'l','m':'l','HH':'m','oo':'m','4_':'m','4b':'m','8':'n/q','s':'n','4':'n/t','o.':'n','o':'o','dl':'o','Lo':'o',
 'F':'o','24':'o/t','z4':'t','E':'p','26':'p','Tp':'p','H':'q','28':'q','r':'r','30':'r','Q':'r','Q8':'r','rr':'rr',
 '80':'s','dz':'s','k':'s','tt':'s','Tz':'s','Tl':'s','J':'ss','4y':'t','h':'t','L':'u','A':'u','d':'u','36':'u',
 'X':'u/_','Xu':'u','oH':'x','44':'y','56':'c/y','s6':'c','Z':'z','#':'_','#o':'_','#x':'_','...':'_','C':'_',
 'lam':'_','dc':'c','6c':'c','r0':'f','Hh':'h','bc':'_','Xb':'b','Y':'b/d','B':'?','s5':'?','gz':'g','fe':'?',
 'D-':'?','sQ':'s','Sc':'s','Sg':'e','6f':'?','6d':'d','bo':'c','Z8':'q','Te':'?','e#':'?','#3':'?','Ip':'?',
 'Ib':'o','7y':'b','4#':'?','262':'code','x0':'?','Tx':'?','3':'b/_','rho':'?','8?':'?',
}
lines=open('align_113.txt',encoding='utf-8').read().splitlines()
rows={}
for ln in lines:
    m=re.match(r'^([RPVQ])(\w+):\s*(.*)$',ln)
    if m: rows[(m.group(1),m.group(2))]=m.group(3).split()
cnt=collections.defaultdict(collections.Counter); refs=collections.defaultdict(lambda: collections.defaultdict(list))
total=0; bad=[]
for (k,rid),toks in rows.items():
    if k not in 'RV': continue
    pl=rows.get(({'R':'P','V':'Q'}[k],rid))
    if pl is None: continue
    if len(pl)!=len(toks): bad.append((k+rid,len(toks),len(pl))); continue
    for i,(t,l) in enumerate(zip(toks,pl)):
        total+=1; cnt[t][l]+=1; refs[t][l].append(f'{k}{rid}.{i+1}')
out=[]
out.append(f'# token -> aligned letter counts, f.113r rows R*, f.113v rows V* (align_113.txt). {total} signs aligned.')
out.append('# letters with ? are unsure; "?" alone = not forced.  Key column = Tomokiyo/TOKENS.md value.')
if bad: out.append('# LENGTH MISMATCH rows (skipped): '+str(bad))
out.append('')
for t in sorted(cnt,key=lambda t:-sum(cnt[t].values())):
    c=cnt[t]; n=sum(c.values())
    out.append(f'{t:5s} n={n:3d}  key={KEY.get(t,"-"):6s}  '+'  '.join(f'{l}:{v}' for l,v in c.most_common()))
out.append('\n# Disagreements with key (letters not in the key value; nulls/unsure ignored), with row refs:')
for t in sorted(cnt):
    kv=set(KEY.get(t,'-').replace('_','_').split('/'))
    for l,v in cnt[t].items():
        L=l.rstrip('?')
        if L in ('?','') : continue
        if L not in kv:
            out.append(f'{t:5s} -> {l:4s} x{v}: '+' '.join(refs[t][l][:12]))
out.append(open('families_113.txt',encoding='utf-8').read())
open('table_113.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
print('\n'.join(out))
