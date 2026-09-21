"""R2234: decrypt with the R2235 Schrijf Tafel (letters a-z without j; u/v distinct).
Section capital = alphabet. Decryption = inverse of the Schrijf row."""
import sys
P = "abcdefghiklmnopqrstuvwxyz"
SCHRIJF = {
 'D': "yfdgaktlepmnqisrhzvowcxub",
 'G': "ukgtypvmasnqrezhlbwicdxof",
 'L': "optvuswnyzqrhablmfcedgxik",
}
def inv(s): return "".join(P[s.index(c)] for c in P)
SCHRIJF['R'] = inv(SCHRIJF['D']); SCHRIJF['N'] = inv(SCHRIJF['G'])
for k, v in SCHRIJF.items(): assert sorted(v) == sorted(P), k
DEC = {k: {v[i]: P[i] for i in range(25)} for k, v in SCHRIJF.items()}
def dec(k, t): return "".join(DEC[k].get(c, c) for c in t.lower().replace('j', 'i'))
if __name__ == "__main__":
    k = None
    for line in open(sys.argv[1], encoding='utf8'):
        line = line.rstrip('\n')
        if line[:2] in ('D:', 'G:', 'L:', 'N:', 'R:'): k, line = line[0], line[2:]
        if line.startswith('#') or not line.strip(): continue
        print(line); print('  ', dec(k, line))
