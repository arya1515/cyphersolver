"""German character quadgram model for ADFGVX plaintext scoring.
Every quadgram window is scored; a window containing a digit or an unknown cell ('.') costs the floor,
so per-window averages are comparable across candidates: German prose about -3.3, junk about -7."""
import collections, glob, math, os, pickle, re
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'q4_de.pkl')

def clean(t):
    t = t.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        t = t.replace(a, b)
    return re.sub('[^a-z]', '', t).upper()

def build():
    cnt = collections.Counter()
    for f in glob.glob(os.path.join(HERE, 'corpus', 'de_*.txt')):
        t = open(f, encoding='utf-8', errors='ignore').read()
        s = t.find('*** START'); e = t.find('*** END')
        x = clean(t[s + 500:e] if s >= 0 else t)
        cnt.update(x[i:i + 4] for i in range(len(x) - 3))
    tot = sum(cnt.values())
    d = {k: math.log10(v / tot) for k, v in cnt.items()}
    floor = math.log10(0.01 / tot)
    pickle.dump((d, floor), open(CACHE, 'wb'))
    return d, floor

def load():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    return build()

D, FLOOR = load()
DIGIT_COST = -7.5  # a window containing a digit: nearly junk, digits are rare in this traffic
X_COST = -6.0      # a window crossing an X separator: dearer than text, cheaper than junk

def score(pt):
    s = 0.0
    n = len(pt) - 3
    if n <= 0:
        return -99.0
    for i in range(n):
        w = pt[i:i + 4]
        v = D.get(w)
        if v is None:
            if any(c.isdigit() for c in w):
                v = DIGIT_COST
            elif 'X' in w and w.isalpha():
                v = X_COST
            else:
                v = FLOOR
        s += v
    return s

def per(pt):
    return score(pt) / max(1, len(pt) - 3)

if __name__ == '__main__':
    D, FLOOR = build()
    print(len(D), FLOOR)
    for t in ('KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX',
              'SLIICR0WG0QBISVWLXDMQU0W.Q7XCWEQ5IAZUROW7.WYCUIWXJAL20Z8Q6XU09IEGH6ERP',
              'FFVREILSESE7WIEDERHQLETTELEGFWD3LMYMFLWF7WFFS8KFNC8RLTIWFWFAFQLL3F.QF7',
              'FNDME9RICHIRA9MI1KAEWXFUMQSTELLENUORO.GENIRRZIXHSBLNAX7RICLTIGENXNADHR'):
        print(round(per(t), 3), t)
