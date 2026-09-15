"""Shape search: which 20-line verse windows match the cipher poem's line-length profile and rhymes?

Profile = glyphs per line (verse_transcription.py). For a candidate window: units per line (syllables,
words, letters) and their Pearson correlation with the profile; plus rhyme structure - lines 2k-1 and 2k
should rhyme (couplets), consecutive couplets should not, and couplet 1 should rhyme with couplet 9.

Usage: python shape.py en|fr FILE [FILE ...]
"""
import math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verse_transcription import lines

PROFILE = [len(l) for l in lines()]
V = 'aeiouyàâäéèêëîïôöûùüÿœ'


def syl_en(w):
    w = re.sub(r"[^a-z]", '', w.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r'(?:[^laeiouy]es|[^laeiouy]ed|[^laeiouy]e)$', '', w)
    w = re.sub(r'^y', '', w)
    return max(1, len(re.findall(r'[aeiouy]{1,2}', w)))


def syl_fr(line):
    words = re.findall(r"[a-zàâäéèêëîïôöûùüÿœç]+", line.lower())
    n = 0
    for i, w in enumerate(words):
        if w in ('l', 'd', 'j', 'm', 'n', 's', 't', 'c', 'qu'):
            continue
        v = len(re.findall('[%s]+' % V, w))
        if re.search(r'[^aeiouy]es?$', w) and v > 1:
            nxt = words[i + 1] if i + 1 < len(words) else None
            if nxt is None or nxt[0] in 'aeiouyhàâéèêîôû':
                v -= 1
        n += max(v, 1)
    return n


def rhyme_key(line, lang):
    w = re.findall(r"[a-zàâäéèêëîïôöûùüÿœç]+", line.lower())
    if not w: return ''
    w = w[-1]
    if lang == 'fr' and len(w) > 3:
        w = re.sub(r'(es|ent|e|s|x|t)$', '', w)
    m = re.search('[%s]+[^%s]*$' % (V, V), w)
    return m.group(0) if m else w[-2:]


def pearson(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    if sa == 0 or sb == 0: return 0.0
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def score_window(W, lang):
    if lang == 'en':
        syl = [sum(syl_en(w) for w in re.findall(r"[A-Za-z']+", l)) for l in W]
    else:
        syl = [syl_fr(l) for l in W]
    words = [len(re.findall(r"[A-Za-zÀ-ÿ']+", l)) for l in W]
    letters = [len(re.findall(r'[A-Za-zÀ-ÿ]', l)) for l in W]
    rk = [rhyme_key(l, lang) for l in W]
    return dict(r_syl=pearson(syl, PROFILE), r_words=pearson(words, PROFILE), r_let=pearson(letters, PROFILE),
                couplets=sum(1 for k in range(0, 20, 2) if rk[k] and rk[k] == rk[k + 1]),
                across=sum(1 for k in range(1, 19, 2) if rk[k] and rk[k] == rk[k + 1]),
                r19=bool(rk[0]) and rk[0] == rk[16], syl=syl, mean_syl=sum(syl) / 20)


def windows(path):
    """Every 20-line window inside runs of consecutive verse-like lines (blank lines break a run)."""
    txt = open(path, encoding='utf-8', errors='ignore').read()
    runs, cur = [], []
    for l in txt.split('\n'):
        l = l.strip()
        if 12 <= len(l) <= 90 and re.search(r'[a-zà-ÿ]', l) and not l.startswith('###'):
            cur.append(l)
        else:
            if len(cur) >= 20: runs.append(cur)
            cur = []
    if len(cur) >= 20: runs.append(cur)
    for run in runs:
        for i in range(len(run) - 19):
            yield run[i:i + 20]


def main():
    lang = sys.argv[1]
    res = []
    for f in sys.argv[2:]:
        for W in windows(f):
            s = score_window(W, lang)
            s.update(first=W[0][:55], file=os.path.basename(f))
            res.append(s)
    print('profile', PROFILE)
    print('%d windows' % len(res))
    good = [s for s in res if s['couplets'] >= 7 and s['across'] <= 2]
    print('%d windows in couplets (>=7 of 10 rhyming, <=2 across)' % len(good))
    good.sort(key=lambda s: -s['r_syl'])
    for s in good[:12]:
        print('  syl r=%.2f  words r=%.2f  letters r=%.2f  couplets %d across %d  1=9 %s  mean syl %.1f  %s | %s'
              % (s['r_syl'], s['r_words'], s['r_let'], s['couplets'], s['across'], s['r19'], s['mean_syl'], s['file'], s['first']))
    allr = sorted(s['r_syl'] for s in res)
    if allr:
        print('distribution of syllable r over all windows: median %.2f, 95th pct %.2f, 99th %.2f, max %.2f'
              % (allr[len(allr) // 2], allr[int(.95 * len(allr))], allr[int(.99 * len(allr))], allr[-1]))


if __name__ == '__main__':
    main()
