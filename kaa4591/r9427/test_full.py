import re, sys
sys.path.insert(0, r'C:\Users\dbour\cypher')
# key in R9410 codes, from key_full.tsv (my sign -> R9410 code)
K = {'4':'e','q':'n','w':'e','E':'d','y':'t','x':'s','5':'a','m':'i','#':'g','9':'o','3':'u','v':'r','n':'b',
     '7':'m','8':'n','Q':'g','t':'z','b':'l','D':'f','6':'d','c':'c','d':'l','g':'r','L':'s','p':'i','o':'a',
     'J':'k','j':'h','R':'und','X':'[FG]','+':'','a':'k','A':'m'}
R9409 = {'V':'v','P':'n','c':'a','T':'Q','z':'j','S':'X','Y':'y','C':'c','H':'#'}
def dec(s, conv=None):
    out = []
    s = s.replace('jo','j').replace('zo','z')
    for ch in s:
        if ch == '[' or ch == ']': out.append(ch); continue
        if conv: ch = conv.get(ch, ch)
        out.append(K.get(ch, '.' if not ch.isspace() else ' '))
    return ''.join(out)
def strip_clear(line):
    return re.sub(r'\[[^\]]*\]', lambda m: m.group(0), line)
res = []
res.append('== R9410 P1 decoded with key_full (R9410 codes) ==')
for ln in open(r'C:\Users\dbour\cypher\kaa4591\sysA\r9410.txt', encoding='utf8'):
    m = re.match(r'^(\d\d) (.*)$', ln.rstrip())
    if not m: continue
    parts = re.split(r'(\[[^\]]*\])', m.group(2))
    d = ''.join(p if p.startswith('[') else dec(p) for p in parts)
    res.append(f'{m.group(1)} {m.group(2)}\n   {d}')
res.append('\n== R9409 P1 lines 1-10 (R9409 codes mapped to R9410 codes) ==')
n = 0
for ln in open(r'C:\Users\dbour\cypher\kaa4591\r9409\transcription.txt', encoding='utf8'):
    m = re.match(r'^(\d\d) (.*)$', ln.rstrip())
    if not m: continue
    n += 1
    if n > 10: break
    parts = re.split(r'(\[[^\]]*\])', m.group(2))
    d = ''.join(p if p.startswith('[') else dec(p, R9409) for p in parts)
    res.append(f'{m.group(1)} {m.group(2)}\n   {d}')
txt = '\n'.join(res)
open(r'C:\Users\dbour\cypher\kaa4591\r9427\test_full.txt', 'w', encoding='utf8').write(txt + '\n')
print(txt)
