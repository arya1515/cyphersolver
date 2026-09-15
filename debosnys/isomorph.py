"""Crib test: do the No. 10 cipher lines encode lines 1-8 of the French poem written below them?

If glyphs are syllables, the same syllable should keep falling on the same glyph. Align the glyph sequence
to a syllable sequence monotonically (a few insertions/deletions allowed, since the syllable count of French
verse is itself uncertain), and score consistency:

    score = sum over glyph types of (its most frequent aligned syllable count)
          + sum over syllable types of (its most frequent aligned glyph count)  - aligned pairs

A perfect monoalphabetic syllabary scores the number of aligned pairs; noise scores far less. The same
annealer is run on control texts: other 8-line windows of French verse with a similar syllable count.
"""
import collections, glob, math, os, random, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n10_transcription import tokens
from unitstats import verse_lines

POEM = """Oh! mes amis je vous supplie en grâce
de bien vouloir un instant m'écouter
Car en ce lieu, pour un moment je passe
montrez moi un peu d'humanité
Oui croyez le, mon coeur a plus qu'une blessure
dont je pourrai vous en faire le triste récit
j'ai bien souffert, je crois les peines les plus dures
Ah! offrez moi vos mains en bons amis
Consolez-vous, car je veux rester brave
Cessez de me plaindre. je ne peux plus pleurer
Le passé pour moi, ne fut qu'un nuage
Que le vent emporte, et que je ne veux pas regretter
Car devant moi l'avenir est beau et plus sûr
C'est là, où je veux aller pour l'éternité""".split('\n')

# hand syllabification of lines 1-8 as sung (mute e counted before consonants, elided before vowels)
HAND = ("oh mes a mis je vous sup pli en grâ ce | de bien vou loir un in stant mé cou ter | "
        "car en ce lieu pour un mo ment je pas se | mon trez moi un peu du ma ni té | "
        "oui cro yez le mon cœur a plus qu'u ne bles su re | dont je pour rai vous en fai re le tris te ré cit | "
        "j'ai bien souf fert je crois les pei nes les plus du res | ah of frez moi vos mains en bons a mis").replace('|', '').split()

V = 'aeiouyàâäéèêëîïôöûùüÿœ'


def auto_syllables(text_lines):
    out = []
    for l in text_lines:
        for w in re.findall("[a-zàâäéèêëîïôöûùüÿœç]+", l.lower()):
            parts = re.findall('[^%s]*[%s]+' % (V, V), w)
            tail = re.sub('^(?:[^%s]*[%s]+)*' % (V, V), '', w)
            if not parts: out.append(w); continue
            if tail: parts[-1] += tail
            if len(parts) > 1 and re.fullmatch('[^%s]*e?s?' % V, parts[-1]) is None and parts[-1].endswith('e'):
                pass
            out.extend(parts)
    return out


def score(pairs):
    g2s = collections.defaultdict(collections.Counter); s2g = collections.defaultdict(collections.Counter)
    for g, s in pairs:
        g2s[g][s] += 1; s2g[s][g] += 1
    return sum(c.most_common(1)[0][1] for c in g2s.values()) + sum(c.most_common(1)[0][1] for c in s2g.values()) - len(pairs)


def align(G, S, ops):
    """ops: sorted list of (position in G, 'g' skip glyph | 's' skip syllable)."""
    pairs, i, j = [], 0, 0
    opd = collections.defaultdict(list)
    for p, t in ops: opd[p].append(t)
    while i < len(G) and j < len(S):
        for t in opd.get(i, []):
            if t == 's': j += 1
        if j >= len(S): break
        if 'g' in opd.get(i, []):
            i += 1; continue
        pairs.append((G[i], S[j])); i += 1; j += 1
    return pairs


def anneal(G, S, k_ops=10, iters=6000, rnd=None):
    rnd = rnd or random.Random(0)
    ops = sorted((rnd.randrange(len(G)), rnd.choice('gs')) for _ in range(k_ops))
    cur = best = score(align(G, S, ops)); best_ops = ops
    T0 = 2.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.05
        new = list(ops)
        k = rnd.randrange(len(new))
        if rnd.random() < 0.7:
            p, t = new[k]; new[k] = (min(len(G) - 1, max(0, p + rnd.randint(-6, 6))), t)
        else:
            new[k] = (rnd.randrange(len(G)), rnd.choice('gs'))
        new.sort()
        v = score(align(G, S, new))
        if v >= cur or rnd.random() < math.exp((v - cur) / T):
            ops, cur = new, v
            if v > best: best, best_ops = v, new
    return best, best_ops


def run(G, S, restarts=4):
    return max(anneal(G, S, rnd=random.Random(r))[0] for r in range(restarts))


if __name__ == '__main__':
    G = tokens(drop_pictograms=True)
    print('glyphs', len(G))
    poem_auto = auto_syllables(POEM[:8])
    print('poem lines 1-8: hand %d syllables, auto %d' % (len(HAND), len(poem_auto)))
    real_hand = run(G, HAND); real_auto = run(G, poem_auto)
    print('score vs poem (hand syllables) %d, (auto) %d' % (real_hand, real_auto))

    rnd = random.Random(7)
    L = verse_lines(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus', 'fr*.txt')))
    ctrl = []
    for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        while True:
            i = rnd.randrange(len(L) - 10)
            S = auto_syllables(L[i:i + 8])
            if abs(len(S) - len(poem_auto)) <= 6: break
        ctrl.append(run(G, S))
    ctrl.sort()
    # also: the later lines of the same poem, and the poem shuffled at syllable level
    later = run(G, auto_syllables(POEM[6:14]))
    shuf = []
    for r in range(10):
        S = list(poem_auto); random.Random(r).shuffle(S); shuf.append(run(G, S))
    print('controls (other French verse, n=%d): median %d, max %d, 95th pct %d' % (len(ctrl), ctrl[len(ctrl) // 2], ctrl[-1], ctrl[int(.95 * len(ctrl))]))
    print('poem lines 7-14: %d;  poem 1-8 shuffled: median %d max %d' % (later, sorted(shuf)[5], max(shuf)))
    print('poem 1-8 beats %d of %d controls' % (sum(1 for c in ctrl if real_auto > c), len(ctrl)))
