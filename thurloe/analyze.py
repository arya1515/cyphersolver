"""Task 2: statistics of each ciphertext + apply candidate known keys (from cryptiana) to (d) and (a)."""
import re, collections, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))

A1 = """113. 10. 26. 13. 13. 19. 29. 29. 26. 11. 222. 31. 17. 21. 22. 23. 23. 22.13. 30. 20. 18.
22. 23. 15. 13. 24. 22. 13. 24. 22. 17. 10. 15. 25. 23. 13. 329. 28. 15. 22. 20. 25. 20.
15. 25. 27. 28. 20. 27. 27. 20. 22. 17. 20. 15. 527. 16. 20. 21. 12. 19. 21. 29. 26. 20.
16. 27. 16. 19."""
A2 = """117. 211. 22. 25. 24. 22. 26. 15. 15. 17. 27. 30. 22. 21. 24. 14. 22. 23. 26. 6. 22. 17. 22. 13. 519. 21. 21.
27. 31. 32. 24. 16. 27. 31. 29. 24. 16. 19. 11. 29. 33. 16. 27. 31. 27. 21. 20. 13. 16. 19."""
A3 = "327. 20. 23. 29. 16. 6.20.24. 17. 15. 29. 17. 32. 20. 23. 15."
B = "18, 15, 4, 20, 87, q, t, 20, y, 1. | 12, m, 17, 24, 15, 8, 15, 17, f, 20, 18, 15, 9, 7, 6, 13, 20."
C = "2 3 1 4 7 4 6 4 9 7 2 3 | 0 9 3 7"
D_WORDS = [  # (cipher groups, clear text following)
    ("7 74 30 54 29 50", "of"), ("39 46 48", "sent to lie nere"), ("43 27 11 38 40 50 14", "and six"),
    ("17 38 63 60 11 48", "of"), ("243 226", "are"), ("79 29 50", "to strengthen"), ("14 53 37", "and"),
    ("43 37 11 56 50 14 86 38", "is so fare out of favour now, that"), ("50 14 15 46 51", "towlde me, he had a greattar mind to"),
    ("33 39 13", "him then"), ("33 37 48 11", ".")]

def toks(s): return re.findall(r"\d+", s)
def stats(name, groups):
    c = collections.Counter(groups)
    lo = [int(g) for g in groups if int(g) < 100]
    print(f"\n== {name}: {len(groups)} groups, {len(c)} distinct; low(<100) range {min(lo)}-{max(lo)} ({len(set(lo))} distinct); "
          f"codes>=100: {sorted(set(g for g in groups if int(g) >= 100), key=int)}")
    print("   freq:", " ".join(f"{k}:{v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], int(kv[0]))) if v > 1))
    # repeated bigrams/trigrams
    for n in (2, 3):
        ng = collections.Counter(tuple(groups[i:i+n]) for i in range(len(groups) - n + 1))
        rep = [(k, v) for k, v in ng.items() if v > 1]
        if rep: print(f"   repeated {n}-grams:", ", ".join(" ".join(k) + f" x{v}" for k, v in rep))

a_all = toks(A1) + toks(A2) + toks(A3)
stats("(a) Beverning/Vande Perre 1653", a_all)
stats("(b) du Gard 1656", toks(B)); print("   letters mixed in:", re.findall(r"\b[a-z]\b", B))
stats("(c) Brussels 12 Aug 1656", toks(C))
d_all = [g for w, _ in D_WORDS for g in w.split()]
stats("(d) Waddall 1656", d_all)

# ---- candidate keys for (d) ----
def blocks(spec):  # spec list of (start,end,letter)
    k = {}
    for s, e, l in spec:
        for n in range(s, e + 1): k[n] = l
    return k
marshall = blocks([(1,5,'a'),(6,9,'b'),(10,13,'c'),(14,17,'d'),(18,22,'e'),(23,26,'f'),(27,30,'g'),(31,34,'h'),(35,39,'i'),
    (40,43,'k'),(44,47,'l'),(48,51,'m'),(52,55,'n'),(56,60,'o'),(61,64,'p'),(65,68,'q'),(69,72,'r'),(73,76,'s'),(77,80,'t'),
    (81,85,'u'),(86,89,'w'),(90,93,'x'),(94,97,'y'),(98,99,'z')])
barwick = {}
for i, l in enumerate("abcdefghiklmnopqrstuwy"):
    for j in range(3): barwick[1 + 3*i + j] = l
barwick[63] = 'y'
westrope = {}
for i, l in enumerate("abcdefghiklmnopqrstuwxy"):
    for j in range(3): westrope[20 + 3*i + j] = l
hague = {}
for base in (20, 50, 78):
    for i, l in enumerate("abcdefghiklmnopqrstu"): hague[base + i] = l
KEYS = {"Marshall(1656-58)": marshall, "Barwick/Cooper(1656-59)": barwick, "Westrope(1655)": westrope, "Hague agent": hague}
print("\n== (d) under candidate keys (code numbers >=100 shown as [n]):")
for kn, k in KEYS.items():
    out = []
    for w, clear in D_WORDS:
        out.append("".join(k.get(int(g), f"[{g}]") for g in w.split()) + " " + clear)
    print(f"  {kn:24s}: " + " ".join(out))

# ---- (a): straight alphabetical assignments 10..33 (24 letters), all rotations/reversals, Dutch & French LM ----
def load_lm(path):
    j = json.load(open(path)); q = j["quad"]; tot = sum(q.values()); 
    return {k: math.log10(v / tot) for k, v in q.items()}, math.log10(0.01 / tot)
def score(txt, lm):
    q, fl = lm
    return sum(q.get(txt[i:i+4], fl) for i in range(len(txt) - 3)) / max(1, len(txt) - 3)
lms = {"nl": load_lm(os.path.join(HERE, "lm_nl.json")), "fr": load_lm(os.path.join(HERE, "lm_fr.json")),
       "en": load_lm(os.path.join(HERE, "..", "beale", "en_lm.json"))}
low = [int(g) for g in a_all if 10 <= int(g) <= 33]
print("\n== (a): straight alphabet on 10..33, best rotation/reversal per LM (score = mean log10 quadgram prob; random ~ -6)")
for alph in ("abcdefghiklmnopqrstuwxyz", "abcdefghijklmnopqrstuvwxyz"[:24]):
    for rev in (False, True):
        al = alph[::-1] if rev else alph
        for rot in range(24):
            key = {10 + i: al[(i + rot) % 24] for i in range(24)}
            pt = "".join(key[n] for n in low)
            for ln, lm in lms.items():
                sc = score(pt, lm)
                if sc > -3.6:
                    print(f"  alph={alph[:6]}.. rev={rev} rot={rot} {ln} score={sc:.2f} : {pt[:70]}")
print("  (nothing printed above => no plain alphabetical key scores better than -3.6)")
