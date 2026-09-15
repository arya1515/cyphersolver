"""Is the IA-2 digit stream laid out in two-digit units, and is there a marker digit?

Everything established so far says the cipher is not a polyphonic single-digit substitution: a matched
synthetic control of exactly that design is solved by the same code, and the real text is not
(NOTES.md). The reading left standing is a mixed cipher with multi-digit codes. Meister's key no. 1,
"Cifra data a Monsig. Montepulciano" and dated between 1539 and 1542 - the very courier this letter
names - shows what that family looks like:

    single digits   8=Ac 6=eu 4=id 2=ot 7=bfg 5=ln 3=prz 0=ms/et
    two-digit codes 49=da 69=de 89=do | 24=na 26=ne 28=ni 29=no | 96=ta 98=te 99=ti | 82=qua 84=que 86=qui
    dotted          .8=sa .6=se .4=si .2=so (dot on the antecedent) | 8.=ra 6.=re 4.=ri 2.=ro
    Nulla 1, and "pongasi la nulla al fine di ogni parola"

Note what the two-digit codes have in common: digit 9 is doing structural work, appearing in most of
them, while the letter-digits carry the rest. So a key of this family has a MARKER digit as well as a
null.

This script asks three questions of the real text, none of which needs a key:

  1. PARITY. If two-digit units dominate, the stretches between nulls should prefer even lengths.
     Tested against a binomial null, because the earlier pass looked at this and waved it away.
  2. PHASE. If there is a fixed two-digit grid inside each stretch, the digit distribution at even
     offsets should differ from the one at odd offsets. Measured as a chi-squared over the 10 digits
     and calibrated by shuffling each segment.
  3. MARKER. A digit doing the structural job of key-1's 9 will have unusually peaked neighbours.
     Measured as KL of P(next|d) and P(prev|d) from the unconditional digit distribution, against a
     shuffle null.

Usage: python phase.py
"""
import collections, math, random, re, sys


def load():
    t = open('ASV_i1025_SdS_Spain_IA-2.txt', encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<CLEARTEXT.*?>', '|', t, flags=re.S)
    t = re.sub(r'#[^\n]*', '', t)
    out = []
    for m in re.finditer(r'(\d)(\^?[._]?)|(\|)', t):
        if m.group(3):
            out.append(('|', ''))
        else:
            out.append((m.group(1), m.group(2)))
    return out


def segments(seq, null='4'):
    """Runs of digits between nulls, not crossing a cleartext break."""
    segs, cur = [], []
    for d, mk in seq:
        if d == '|':
            if cur:
                segs.append(cur)
            cur = []
        elif d == null:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append((d, mk))
    if cur:
        segs.append(cur)
    return segs


def chi2(a, b):
    """Chi-squared between two count dicts over the digits."""
    keys = set(a) | set(b)
    na, nb = sum(a.values()), sum(b.values())
    if not na or not nb:
        return 0.0
    tot = 0.0
    for k in keys:
        ea = (a.get(k, 0) + b.get(k, 0)) * na / (na + nb)
        eb = (a.get(k, 0) + b.get(k, 0)) * nb / (na + nb)
        if ea > 0:
            tot += (a.get(k, 0) - ea) ** 2 / ea
        if eb > 0:
            tot += (b.get(k, 0) - eb) ** 2 / eb
    return tot


def kl(p, q):
    return sum(v * math.log(v / q[k]) for k, v in p.items() if v > 0 and q.get(k, 0) > 0)


def norm(c):
    n = sum(c.values())
    return {k: v / n for k, v in c.items()} if n else {}


def main():
    seq = load()
    segs = segments(seq)
    digs = [d for d, m in seq if d != '|']
    print('%d digits, %d segments between nulls (digit 4)' % (len(digs), len(segs)))

    # ---------------------------------------------------------------- 1. parity
    lens = [len(s) for s in segs]
    ev = sum(1 for L in lens if L % 2 == 0)
    od = len(lens) - ev
    n = len(lens)
    z = (ev - n / 2) / math.sqrt(n * 0.25)
    print('\n=== 1. PARITY OF SEGMENT LENGTHS')
    print('   even %d, odd %d of %d   z = %+.2f' % (ev, od, n, z))
    print('   mean length %.2f' % (sum(lens) / n))
    print('   An Italian word is about 4.5 letters, so these stretches are not single words.')

    # ---------------------------------------------------------------- 2. phase
    print('\n=== 2. PHASE: digit distribution at even vs odd offsets inside a segment')
    A, B = collections.Counter(), collections.Counter()
    for s in segs:
        for i, (d, m) in enumerate(s):
            (A if i % 2 == 0 else B).append if False else (A if i % 2 == 0 else B).update([d])
    obs = chi2(A, B)
    rnd = random.Random(11)
    null_vals = []
    for _ in range(2000):
        a, b = collections.Counter(), collections.Counter()
        for s in segs:
            ds = [d for d, m in s]
            rnd.shuffle(ds)
            for i, d in enumerate(ds):
                (a if i % 2 == 0 else b).update([d])
        null_vals.append(chi2(a, b))
    mu = sum(null_vals) / len(null_vals)
    sd = (sum((x - mu) ** 2 for x in null_vals) / len(null_vals)) ** 0.5
    beat = sum(1 for x in null_vals if x >= obs)
    print('   chi-squared even vs odd = %.1f ; shuffle null mean %.1f sd %.1f ; z = %+.2f ; p = %.4f'
          % (obs, mu, sd, (obs - mu) / sd if sd else 0, beat / len(null_vals)))
    pa, pb = norm(A), norm(B)
    print('   digit   even    odd     ratio')
    for d in sorted(set(pa) | set(pb)):
        r = pa.get(d, 0) / pb[d] if pb.get(d) else float('inf')
        print('     %s    %.4f  %.4f  %.2f' % (d, pa.get(d, 0), pb.get(d, 0), r))

    # ---------------------------------------------------------------- 3. marker digit
    print('\n=== 3. MARKER DIGIT: how peaked is each digit\'s neighbourhood?')
    s = [d for d, m in seq if d != '|']
    uncond = norm(collections.Counter(s))
    print('   digit  freq    KL(next)  KL(prev)  sum      shuffled sum')
    rows = []
    for d in sorted(set(s)):
        nx = norm(collections.Counter(b for a, b in zip(s, s[1:]) if a == d))
        pv = norm(collections.Counter(a for a, b in zip(s, s[1:]) if b == d))
        kn, kp = kl(nx, uncond), kl(pv, uncond)
        # shuffle null for this digit
        vals = []
        pool = list(s)
        for _ in range(60):
            rnd.shuffle(pool)
            n2 = norm(collections.Counter(b for a, b in zip(pool, pool[1:]) if a == d))
            p2 = norm(collections.Counter(a for a, b in zip(pool, pool[1:]) if b == d))
            vals.append(kl(n2, uncond) + kl(p2, uncond))
        rows.append((kn + kp, d, uncond[d], kn, kp, sum(vals) / len(vals)))
    for tot, d, f, kn, kp, sh in sorted(rows, reverse=True):
        print('     %s   %.4f  %.4f    %.4f    %.4f   %.4f' % (d, f, kn, kp, tot, sh))


if __name__ == '__main__':
    main()
