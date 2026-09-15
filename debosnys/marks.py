"""Decompose transcribed glyphs into their component marks (the 'monogram' hypothesis)."""
import re, collections
from verse_transcription import lines

WHOLE = {  # glyphs that are one drawn sign: (marks)
    'X': ['x'], 'XD': ['x', '.'], 'XS2': ['x', '//'], 'XBAR': ['x', '-'], 'CX': ['cx'], 'HX': ['hx'], 'BX': ['bx'],
    'VENUS': ['o', '+'], 'ODOWN': ['o', 'v'], 'OX': ['o', 'x'], 'OPLUS': ['o', '+'], 'MARS_II': ['o', '^', '"'],
    'UPARROW': ['.', '^'], 'O_HOOK': ['o', 'j'], 'HOOK_O': ['j', 'o'], 'O_STEM': ['o', '|'], 'O_EQ_HOOK': ['o', '-', 'j'],
    'TARGET_J': ['o', '.', 'j'], 'T_O_II': ['+', 'o', '"'], 'CARET_O': ['^', 'o'], 'PLUS_O': ['+', 'o'], 'Q': ['o', '|'],
    'DELTA': ['D'], 'DELTA_RING': ['D', 'o'], 'DELTA_BAR': ['D', '-'], 'SIGMA': ['S'], 'OMEGA': ['W'], 'THETA': ['o', '-'],
    'ALPHA': ['a'], 'GAM': ['g'], 'Y': ['y'], 'YB': ['y', '-'], 'UPS': ['u'], 'V': ['v'], 'V_RING': ['v', 'o'],
    'VCURL': ['v', '.'], 'DSMALL': ['d'], 'DCURL': ['d', 'j'], 'D_COLON': ['d', ':'], 'Z3': ['z', '-'],
    'TCURL': ['~', 's'], 'LOOP': ['l'], 'DBLWAVE': ['~', '~'], 'DBLWAVE_XX': ['~', '~', 'x', 'x'], 'MTAIL': ['m'],
    'HEART': ['h'], 'CHECK_DOT': ['v', '.'], 'CRES_E': ['c', 'e'], 'GATE': ['n', '/', ':'], 'NOTE': ['n'],
    'TAURUS': ['o', 'c'], 'LEO': ['l'], 'STAR': ['*'], 'HASH': ['#'], 'GRID': ['#'], 'OSLASH': ['o', '/'], 'PM': ['+', '-'],
    'EIGHT': ['o', 'o'], 'QBAR': ['?', '-'], 'CHEV_O': ['<', 'o'], 'CHEV_DASH': ['<', '-'], 'CHEV_O_CHEV': ['<', 'o', '>'],
    'O_SL2_EQ': ['o', '//', '='], 'CARET_RING': ['^', 'o'], 'CUP_III': ['u', '"', "'"], 'U_EQ': ['u', '='],
    'TICKS_BAR': ['"', '-', '"'], 'BARS_II': ['=', '"'], 'BARS_O': ['-', 'o', '-'], 'EQ3_O': ['=', '-', 'o'],
    'N_COLON': ['~', ':'], 'N_DASH_X': ['~', '-', 'x'], 'N_SLO': ['~', '/', 'o'], 'N_SL2': ['~', '//'], 'N_W': ['~', 'o', 'o'],
    'SL2_BAR_O': ['//', '-', 'o'], 'II_EQ': ['"', '='],
}
PART = {'O': ['o'], 'OO': ['o', 'o'], 'X': ['x'], 'OX': ['o', 'x'], 'CUP': ['u'], 'BAR': ['-'], 'EQ': ['='], 'II': ['"'],
        'ARCH': ['n'], 'CC': ['c', 'c']}
MARK = {'o': 'o', 'd': '.', 'x': 'x', 't': "'", 'p': '+', 'y': 'y', '22': '22', '': None}


def decompose(g):
    if g in WHOLE: return WHOLE[g]
    if g.startswith('PIC') or g == '?': return None
    m = re.match(r'(B?SL)\(([^,]*),([^)]*)\)', g)
    if m:
        out = ['/' if m.group(1) == 'SL' else 'BS']
        for p in (m.group(2), m.group(3)):
            if MARK.get(p): out.append(MARK[p])
        return out
    parts = g.split('_')
    out = []
    head = {'N': ['~'], 'EQ': ['='], 'II': ['"'], 'ARCH': ['n'], 'CC': ['c', 'c']}
    for p in parts:
        if p in head: out += head[p]
        elif p in PART: out += PART[p]
        else: return None
    return out


if __name__ == '__main__':
    miss = collections.Counter()
    per_line, sizes, allm = [], collections.Counter(), collections.Counter()
    for l in lines():
        n = 0
        for g in l:
            d = decompose(g)
            if d is None:
                miss[g] += 1; continue
            n += len(d); sizes[len(d)] += 1; allm.update(d)
        per_line.append(n)
    print('undecomposed:', dict(miss))
    print('marks per line:', per_line, 'mean %.1f' % (sum(per_line) / 20))
    tot = sum(sizes.values())
    print('marks per glyph:', {k: '%.2f' % (v / tot) for k, v in sorted(sizes.items())}, 'mean %.2f' % (sum(k * v for k, v in sizes.items()) / tot))
    print('mark frequencies:', allm.most_common())
