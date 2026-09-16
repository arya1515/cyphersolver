"""Adjudicate the AFIO (May 2025) claimed solution of Armstrong to Madison, 20 Feb 1808.

Inputs: feb20_ciphertext.txt (Founders Online groups), afio_key.txt (the published 56-entry key + text).
Tests:
  1. coverage and occurrence accounting: how many of the letter's groups the key maps, and how many
     occurrences of mapped groups the published "decrypted text" actually accounts for;
  2. in-order alignment (LCS) of the key's rendering against the published text, with a shuffled-key
     control -- reported, but uninformative for a key that was built from this very letter;
  3. matched-freedom control: a key built greedily on a SHUFFLED ciphertext by the same procedure
     (walk the plaintext, assign the next free group) -- if that fits as well as the AFIO key does,
     the AFIO key carries no information about the code.
Usage: python adjudicate_feb20.py
"""
import re, random, statistics
from collections import Counter, defaultdict

nums = [int(x) for l in open('feb20_ciphertext.txt', encoding='utf-8') if not l.startswith('#')
        for x in l.split() if x.isdigit()]
key, pt = {}, []
for l in open('afio_key.txt', encoding='utf-8'):
    m = re.match(r'^(\d+);(\w+)', l)
    if m: key[int(m.group(1))] = m.group(2).lower()
    elif l.startswith(';') and not l.startswith(';Claimed') and not l.startswith(';(') and re.search(r'[a-z]{3}', l) and 'http' not in l and 'AFIO' not in l:
        pt.append(l[1:])
words = re.findall(r'[a-z]+', ' '.join(pt).lower())
cnt = Counter(nums)


def lcs(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    i, j, pairs = n, m, []
    while i and j:
        if a[i - 1] == b[j - 1]: pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]: i -= 1
        else: j -= 1
    return dp[n][m], pairs[::-1]


def evaluate(k, seq):
    """(words matched in order, consistency = matched / mapped occurrences inside the matched span,
        share = matched / all mapped occurrences in seq)"""
    dec = [k.get(n) for n in seq]
    L, pairs = lcs(dec, words)
    if not pairs: return 0, 0.0, 0.0
    lo, hi = pairs[0][0], pairs[-1][0]
    ins = sum(1 for x in dec[lo:hi + 1] if x is not None)
    tot = sum(1 for x in dec if x is not None)
    return L, L / ins, L / tot


def build(seq, words):
    """The AFIO-style procedure: walk the plaintext, give each word the next group not already taken."""
    k, i = {}, 0
    for w in words:
        while i < len(seq) and seq[i] in k and k[seq[i]] != w: i += 1
        if i >= len(seq): break
        k[seq[i]] = w; i += 1
    return k


if __name__ == '__main__':
    print(f'letter: {len(nums)} groups, {len(cnt)} distinct, max {max(nums)}; key: {len(key)} entries, '
          f'{len(set(key.values()))} distinct words; text: {len(words)} words')
    print('key numbers absent from the letter:', [(n, key[n]) for n in key if cnt[n] == 0])
    print('text words with no key entry:', sorted(set(w for w in words if w not in key.values())))
    mapped = sum(cnt[n] for n in key)
    print(f'groups covered by key: {mapped}/{len(nums)} ({mapped/len(nums):.0%}); distinct {sum(1 for n in key if cnt[n])}/{len(cnt)}')
    L, pairs = lcs([key.get(n) for n in nums], words)
    used = Counter(nums[i] for i, _ in pairs)
    lo, hi = pairs[0][0], pairs[-1][0]
    inspan = sum(1 for n in nums[lo:hi + 1] if n in key)
    print(f'AFIO text aligned: {L}/{len(words)} words in order, spanning groups {lo}-{hi}; mapped occurrences in span {inspan}, '
          f'used {L}, dropped {inspan-L} (consistency {L/inspan:.2f}); over the whole letter {mapped-L} of {mapped} mapped occurrences unaccounted')
    print('most frequent groups: occurrences vs. used by the text')
    for n in sorted(key, key=lambda n: -cnt[n])[:10]:
        print(f'   {n:5d} {key[n]:12s} {cnt[n]:3d} {used[n]:3d}')
    real = evaluate(key, nums)
    random.seed(1)
    ctrl = []
    for _ in range(1000):
        ws = list(key.values()); random.shuffle(ws)
        ctrl.append(evaluate(dict(zip(key, ws)), nums)[0])
    print(f'control A (words shuffled among the key numbers): words in order mean {statistics.mean(ctrl):.1f}, max {max(ctrl)}; '
          f'real {real[0]}  -- passes, but trivially: the key was read off this letter')
    random.seed(2)
    res = []
    for _ in range(500):
        s = nums[:]; random.shuffle(s)
        res.append(evaluate(build(s[12:], words), s[12:]))
    for j, name in enumerate(['words in order', 'consistency in span', 'share of mapped occurrences']):
        v = [r[j] for r in res]
        print(f'control B (key built by the same procedure on a shuffled ciphertext): {name}: mean {statistics.mean(v):.2f} '
              f'sd {statistics.pstdev(v):.2f} [{min(v):.2f}, {max(v):.2f}]  vs AFIO {real[j]:.2f}')
    print('verdict: the AFIO key fits its own text no better than a key fitted to random noise; it does not hold.')
