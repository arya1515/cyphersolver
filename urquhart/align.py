# Align a numeric transcription of the octastich to the pages of The Jewel using Urquhart's habit: the number for
# each letter is the index of the FIRST word on that page beginning with the letter. That property holds without
# knowing the plaintext, so a DP over (token j -> page p) with page skips (numbers missing from the transcription)
# and token drops (spurious numbers) finds the alignment and shows where the transcription is defective.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages as PG
from ct import OCTASTICH

P = PG.load()
NP = 284


def is_first(p, n):
    ws = P.get(p, [])
    if n > len(ws):
        return None      # out of range on this page (TCP text shorter than print, or wrong page)
    return PG.first_index(ws, ws[n - 1][0]) == n


def letter(p, n):
    ws = P.get(p, [])
    return ws[n - 1][0].upper() if n <= len(ws) else '_'


def align(seq, skip_cost=1.0, drop_cost=1.5, hit=1.0, miss=-0.6, oor=-0.3):
    """DP: state (j tokens consumed, p pages consumed). Moves: match token j to page p (score by first-occurrence),
    skip page (transcription lost a number), drop token (transcription has an extra number)."""
    J = len(seq)
    NEG = -1e9
    best = [[NEG] * (NP + 1) for _ in range(J + 1)]
    bp = [[None] * (NP + 1) for _ in range(J + 1)]
    best[0][0] = 0.0
    for j in range(J + 1):
        for p in range(NP + 1):
            b = best[j][p]
            if b <= NEG / 2:
                continue
            if j < J and p < NP:
                f = is_first(p + 1, seq[j])
                s = hit if f else (oor if f is None else miss)
                if b + s > best[j + 1][p + 1]:
                    best[j + 1][p + 1] = b + s; bp[j + 1][p + 1] = ('M', j, p)
            if p < NP and b - skip_cost > best[j][p + 1]:
                best[j][p + 1] = b - skip_cost; bp[j][p + 1] = ('S', j, p)
            if j < J and b - drop_cost > best[j + 1][p]:
                best[j + 1][p] = b - drop_cost; bp[j + 1][p] = ('D', j, p)
    # end: all tokens consumed, any page count (remaining pages free)
    pe = max(range(NP + 1), key=lambda p: best[J][p])
    path = []
    j, p = J, pe
    while (j, p) != (0, 0):
        mv, pj, pp = bp[j][p]
        path.append((mv, pj, pp))
        j, p = pj, pp
    path.reverse()
    return best[J][pe], path


if __name__ == '__main__':
    seq = [v for l in OCTASTICH for v in l]
    line_of = []
    for li, l in enumerate(OCTASTICH):
        line_of += [li] * len(l)
    score, path = align(seq)
    print('score', score, 'tokens', len(seq))
    out = []; cur_line = 0; buf = ''; hits = 0; tot = 0
    for mv, j, p in path:
        if mv == 'M':
            if line_of[j] != cur_line:
                out.append(buf); buf = ''; cur_line = line_of[j]
            L = letter(p + 1, seq[j]); f = is_first(p + 1, seq[j])
            buf += L if f else (L.lower() if f is not None else '_')
            tot += 1; hits += 1 if f else 0
        elif mv == 'S':
            buf += '?'          # a page with no number in the transcription: a letter is missing here
        elif mv == 'D':
            buf += '(%d)' % seq[j]
    out.append(buf)
    print('first-occurrence hits %d / %d matched tokens' % (hits, tot))
    for i, l in enumerate(out):
        print(i + 1, l)
    # page map for reference
    pm = [(j, p + 1) for mv, j, p in path if mv == 'M']
    print('first token -> page', pm[:3], 'last', pm[-3:])
