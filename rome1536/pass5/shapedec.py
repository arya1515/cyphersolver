# Decode shape-true transcriptions (trans.txt): direct key map, then LM lattice; CER vs readers' refs from calib.
import os, sys, re, math, collections
WT = os.environ['LANGWT']; sys.path.insert(0, WT)
from lang import lm as LM
M = LM.load('fr-1600-letters', spaces=False); IDX = M.index; LP = M.lp; A = M.A; ORD = M.order
KEY = {'A+':'a','A3':'a','A8':'a','B':'b','C4':'c','Cr':'c','D5':'d','E9':'e','Eo':'e','Eb':'e','F':'f','Gh':'g','H':'h',
 'I':'i','I#':'i','Il':'i','L10':'l','Lx':'l','LL':'ll','M1':'m','Mq':'m','N7':'n','Nx':'n','Of':'o','OD':'o','Pn':'p','Pc':'p',
 'PP':'pp','Q':'q','R27':'r','Rr':'r','RR':'rr','S6':'s','Sinf':'s','Sr':'s','SS':'ss','Tg':'t','Tx':'t','Up':'u','Um':'u','Uv':'u',
 'X':'x','ET':'et','nE':'','n*':'','20':'lempereur','30':'pape','40':'roy','Y':'y'}
# known hand-level conflations (penalised alternatives for the lattice only)
CONF = {'N7':['b','r'],'B':['n'],'C4':['r'],'R27':['c'],'Lx':['n'],'D5':['s','g'],'Gh':['d'],'Rr':[''],'Q':['i'],'I':['j','y','q',''],
        'Of':['u','p','f'],'Up':['o','v','p','f'],'Um':['o'],'Uv':['o'],'Pn':['o','f','u','r'],'F':['p','o','u'],'Mq':['e','n'],
        'E9':['m',''],'Eb':['ss'],'SS':['e'],'Tg':['s'],'A+':[''],'?':[]}
def alts(tok):
    return re.match(r'\{(.*)\}', tok).group(1).split('|') if tok.startswith('{') else [tok]
def direct(toks):
    out = ''
    for t in toks:
        a = alts(t)[0]
        out += KEY.get(a, '?') if a != '?' else '?'
    return out
def cands(t):
    d = {}
    for k, a in enumerate(alts(t)):
        pen = 0 if k == 0 else math.log(0.5)
        if a == '?':
            for c in 'abcdefghilmnopqrstuxyz': d[c] = math.log(1 / 22)
            continue
        base = KEY[a]; d[base] = max(d.get(base, -99), pen)
        for c in CONF.get(a, []): d[c] = max(d.get(c, -99), pen + math.log(0.03))
    return d
def lm_step(ctx, ch):
    k = 0
    for c in ctx: k = k * A + c
    k = k * A + IDX[ch]
    return float(LP[k]), ctx[1:] + (IDX[ch],)
def beam(toks, w=2.0, bonus=1.5, width=128):
    ctx0 = tuple(IDX[c] for c in LM.norm('esque', 'early', spaces=False)[-(ORD - 1):])
    beams = {ctx0: (0.0, '')}
    for t in toks:
        nb = {}
        for ctx, (sc, h) in beams.items():
            for s, lp in cands(t).items():
                if any(ch not in IDX for ch in s): continue
                v = sc + w * lp + bonus * len(s); c = ctx
                for ch in s: l, c = lm_step(c, ch); v += l
                if c not in nb or nb[c][0] < v: nb[c] = (v, h + s)
        beams = dict(sorted(nb.items(), key=lambda x: -x[1][0])[:width])
    return max(beams.values())[1]
def ed(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[len(b)]
def nrm(s): return LM.norm(s, 'early', spaces=False)
MAP = {'R4234_P16_L4':21,'R4234_P16_L5':23,'R4234_P16_L6':25,'R4234_P16_L7':27,'R4234_P16_L8':29,'R4234_P16_L9':31,'R4234_P16_L10':33,
 'R4234_P16_L11':35,'R4234_P16_L12':37,'R4234_P16_L13':39,'R4234_P16_L14':41,'R4234_P16_L19':50,'R4234_P16_L20':52,'R4234_P19_C1':93,
 'R4234_P19_C2':94,'R4234_P19_C5':100,'R4234_P19_C6':102,'R4234_P20_C7':107,'R4234_P20_C8':108}
FILE = lambda k: ('R4234_P15-P20', MAP[k]) if k in MAP else (('R4235_P8D', {'1':8,'2':11,'3':13,'4':15}[k[-1]]) if k.startswith('R4235') else ('R4240', 19 + int(k.split('L')[-1])))
old = {}; cur = None
for ln in open('_old_calib.txt', encoding='utf-8'):
    m = re.match(r'(R\d+\S*):(\d+)$', ln.strip())
    if m: cur = (m.group(1), int(m.group(2))); old.setdefault(cur, {}); continue
    m = re.match(r'\s+(ref|arg|lm)\s+(\S*)', ln)
    if m and cur and m.group(1) not in old[cur]: old[cur][m.group(1)] = m.group(2)
tot = collections.Counter(); rep = []
for ln in open('trans.txt', encoding='utf-8'):
    if ln.startswith('#') or not ln.strip(): continue
    k, sig = ln.rstrip('\n').split('\t')
    toks = [t for t in sig.split() if t not in ('|', '~')]
    o = old[FILE(k)]; ref = o['ref']
    dr = nrm(direct(toks).replace('?', 'x')); lat = nrm(beam(toks))
    grp = 'R4240' if k.startswith('R4240') else 'uni'
    for name, h in [('old_arg', o['arg']), ('old_lm', o['lm']), ('new_direct', dr), ('new_lm', lat)]:
        tot[(grp, name)] += ed(h, ref)
    tot[(grp, 'n')] += len(ref)
    rep.append(f"### {k} ({FILE(k)[0]}:{FILE(k)[1]})\n- signs: `{sig}`\n- ref:        {ref}\n- old+LM:     {o['lm']}  ({ed(o['lm'],ref)} err)\n- new direct: {dr}  ({ed(dr,ref)} err)\n- new+LM:     {lat}  ({ed(lat,ref)} err)\n")
open('pilot_lines.md', 'w', encoding='utf-8').write('\n'.join(rep))
for g in ['uni', 'R4240']:
    n = tot[(g, 'n')]
    if n: print(g, n, ' '.join(f"{x} {tot[(g,x)]/n:.3f}" for x in ['old_arg', 'old_lm', 'new_direct', 'new_lm']))
