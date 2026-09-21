"""Decode a System A' transcription with the R9427-gloss key; resolve each E as d or ch by LM context."""
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lang import lm
M = lm.load('de-1500s', spaces=False)
K0 = dict(kv.split('=') for kv in "#=g +=r -=i 2=r 3=u 4=e 5=a 6=d 7=m 8=n 9=o :=i @=w A=u B=s D=f H=a J=k L=s O=t Q=g R=i S=h Y=r Z=u a=e b=l c=c d=l g=r j=h m=i n=w o=a p=i q=n r=l t=z v=r w=e x=s y=t |=e X=e".split())
K = dict(K0, **{'β': 'be'})
def score(s): return M.score_idx(M.encode(s))
def decode(sig):
    sig = sig.replace('jo', 'j').replace('a+', 'β')
    out = ''
    for i, c in enumerate(sig):
        if c == 'E':
            left = out[-8:]
            right = ''.join(K.get(x, '') for x in sig[i+1:i+8] if x != 'E')
            out += max(('d', 'ch'), key=lambda v: score(left + v + right))
        else:
            out += K.get(c, '?') if c not in '?.' else ''
    return out
src, dst = sys.argv[1], sys.argv[2]
res = []
for l in open(src, encoding='utf8'):
    if l.startswith('=='): res.append(l.strip()); continue
    m = re.match(r'\s*(?:P\d\s*)?L?(\d+)[\s:|.]+(.*)', l)
    if not m or l.strip().startswith(('g:', '#')): continue
    res.append(m.group(1) + ' ' + re.sub(r'(\[[^\]]*\])|([^\[\] ]+)', lambda x: x.group(1) or decode(x.group(2)), m.group(2)))
open(dst, 'w', encoding='utf8').write('\n'.join(res) + '\n')
print('\n'.join(res[:8]))
