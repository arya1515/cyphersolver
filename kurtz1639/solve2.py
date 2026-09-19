"""Structured solver for the Kurz table.

Numbers 41-100 are consonant+vowel signs: each ten is split into two halves (41-45, 46-50, ...), one consonant per half,
and within a half the units run o i e a u (41 ro, 42 ri, 43 re, 44 ra, 45 ru). Numbers 1-40 and the letter/graphic signs
are single letters (or nulls). The solver anneals one consonant per half and one letter per single sign.

    python solve2.py [--records R3811,R3813] [--iters 40000] [--fix fix.json] [--out key2.json]
"""
import argparse, collections, json, math, os, random, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solve import model, LETTERS
from parse import load
from lang import lm

VORD = 'oieau'
CONS = ['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'w', 'z', 'ch', 'sch', 'st', 'qu']
MULTI = ['ch', 'sch', 'st', 'ss', 'en', 'er', 'un', 'ei', 'ng', 'nn', 'tt', 'ck', 'ff', 'll', 'mm', 'tz', 'ie', 'au', 'et', 'us', 'um', 'em', 'ti', 'si', 'ru', 'is', 'es', 'as', 'us', 'ra', 're', 'ri']
SEED_HALF = {41: 'r', 51: 'n', 56: 'm', 61: 'l', 71: 'h', 81: 'd', 91: 'b'}


def half(n):
    return 41 + ((n - 41) // 5) * 5


def value(tok, halves, singles):
    if tok in singles:
        return singles[tok]
    if tok.isdigit() and 41 <= int(tok) <= 95:
        n = int(tok)
        return halves[half(n)] + VORD[(n - 1) % 5]
    return singles.get(tok, '?')


def keymap(halves, singles, syms):
    return {s: value(s, halves, singles) for s in syms}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records')
    ap.add_argument('--iters', type=int, default=40000)
    ap.add_argument('--restarts', type=int, default=2)
    ap.add_argument('--fix')
    ap.add_argument('--out', default='key2.json')
    ap.add_argument('--kl', type=float, default=1.0)
    ap.add_argument('--show', type=int, default=40)
    a = ap.parse_args()
    runs, _ = load(a.records.split(',') if a.records else None)
    runs = [(f, [t.strip('~[]') for t in r if '?' not in t and t not in ('/', '#ins')]) for f, r in runs]
    runs = [x for x in runs if len(x[1]) >= 2]
    m = model()
    cnt = collections.Counter(t for _, r in runs for t in r)
    syms = sorted(cnt)
    fix = json.load(open(a.fix, encoding='utf-8')) if a.fix else {}
    fixh = {int(k[1:]): v for k, v in fix.items() if k.startswith('H')}
    fixs = {k: v for k, v in fix.items() if not k.startswith('H')}
    halfs = sorted({half(int(s)) for s in syms if s.isdigit() and 41 <= int(s) <= 95})
    singles_syms = [s for s in syms if not (s.isdigit() and 41 <= int(s) <= 95)]
    enc = {c: i for i, c in enumerate(lm.alphabet('early', False))}
    seqs = [r for _, r in runs]
    ref = collections.Counter(lm.norm(open(os.path.join(HERE, 'corpus_de17.txt'), encoding='utf-8').read()[:400000], 'early', False))
    rt = sum(ref.values())
    refp = {c: ref[c] / rt for c in LETTERS}

    def total(h, s):
        k = keymap(h, s, syms)
        text = ''.join(''.join(k[t] for t in q) for q in seqs)
        x = np.array([enc[c] for c in text if c in enc], dtype=np.int64)
        sc = m.score_idx(x)
        c = collections.Counter(text)
        n = len(text)
        kl = n * sum((c[ch] / n) * math.log((c[ch] / n) / max(refp.get(ch, 1e-4), 1e-4)) for ch in c if ch in refp)
        nul = sum(2.5 * cnt[t] for t in s if s[t] == '')
        return sc - a.kl * kl - nul

    best_all = None
    for r in range(a.restarts):
        random.seed(r + 7)
        h = {x: fixh.get(x, SEED_HALF.get(x, random.choice(CONS))) for x in halfs}
        s = {t: fixs.get(t, random.choice('enirstadhulgcmobwfkz')) for t in singles_syms}
        freeh = [x for x in halfs if x not in fixh]
        frees = [t for t in singles_syms if t not in fixs]
        cur = total(h, s)
        best = (cur, dict(h), dict(s))
        for it in range(a.iters):
            T = 4.0 * (1 - it / a.iters) + 0.05
            if freeh and random.random() < 0.15:
                x = random.choice(freeh); old = h[x]; h[x] = random.choice(CONS)
                new = total(h, s)
                if new >= cur or random.random() < math.exp((new - cur) / T):
                    cur = new
                else:
                    h[x] = old
            else:
                t = random.choice(frees); old = s[t]
                r_ = random.random()
                s[t] = random.choice(LETTERS) if r_ < 0.8 else (random.choice(MULTI) if r_ < 0.97 else '')
                if s[t] == old:
                    continue
                new = total(h, s)
                if new >= cur or random.random() < math.exp((new - cur) / T):
                    cur = new
                else:
                    s[t] = old
            if cur > best[0]:
                best = (cur, dict(h), dict(s))
        print(f'restart {r}: {best[0]:.1f}', flush=True)
        if best_all is None or best[0] > best_all[0]:
            best_all = best
    _, h, s = best_all
    out = {'H%d' % k: v for k, v in sorted(h.items())}
    out.update(s)
    json.dump(out, open(os.path.join(HERE, a.out), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('halves:', ' '.join(f'{k}-{k+4}:{v}' for k, v in sorted(h.items())))
    print('singles:', ' '.join(f'{t}={s[t] or "0"}({cnt[t]})' for t in sorted(s, key=lambda t: -cnt[t])))
    k = keymap(h, s, syms)
    for f, q in runs[:a.show]:
        print(f[-12:], ''.join(k[t] for t in q))


if __name__ == '__main__':
    main()
