import re, collections
BS = chr(92)
R9410 = {'8':'8','5':'5','p':'n','b':'b','4':'4','w':'w','Q':'q','0':'o','o':'o','P':'p','v':'v','3':'3','9':'9',
         'y':'y','K':'J','7':'7','r':'c','E':'E','X':'X',BS+'x':'x','T':'Q','q':'Q?','D':'D','d':'d','H':'#','.H':'#?',
         'm':'m','g':'g','L':'L','@':'A','S':'S','^':'t','6':'6','e':'a','+':'+','z':'j','n':'m?','A':'(none)',
         '8o':'b?','4o':'R','e+':'a+','r+':'c+?','e-':'a','+^':'+t'}
cnt = collections.defaultdict(collections.Counter)
for ln in open('aligned_full.tsv', encoding='utf8').read().splitlines()[1:]:
    f = ln.split('\t')
    if len(f) < 5: continue
    a = re.sub(r'\[.*?\]', '', f[4]); a = re.sub(r'\(initial.*?\)', '', a)
    for s, v in re.findall(r'(\S+?)=(\S+)', a):
        weak = '?' in v
        v = v.replace('?', '').split('/')[0].strip('()')
        if not v: continue
        cnt[s][v] += 0.5 if weak else 1
out = ['sign\tletter(s)\tcount(weak=0.5)\tall_readings\tR9410_code']
for s in sorted(cnt, key=lambda s: -sum(cnt[s].values())):
    best = cnt[s].most_common(1)[0][0]
    out.append(f"{s}\t{best}\t{sum(cnt[s].values()):g}\t{' '.join(f'{k}:{v:g}' for k,v in cnt[s].most_common())}\t{R9410.get(s,'?')}")
out.append('X\tF.G. (code)\t5\tcode sign after w3v (ewr)\tX')
open('key_full.tsv', 'w', encoding='utf8').write('\n'.join(out) + '\n')
print('\n'.join(out))
