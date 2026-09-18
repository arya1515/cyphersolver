"""Decode my transcription with Lasry's (2023) key, choosing among each sign's readings with a French quadgram model
(richelieu/fr_quadgrams.json). Beam search runs through each cipher run; clear text in [..] passes through and sets context."""
import json, math, re, collections, sys
Q = json.load(open('../richelieu/fr_quadgrams.json'))
T3 = collections.Counter()
for k, v in Q.items(): T3[k[:3]] += v
def lp(q):
    v = Q.get(q)
    return math.log10(v / T3[q[:3]]) if v else math.log10(0.3 / (T3.get(q[:3], 0) + 50))
KEY = {'J':'A','c':'F','s':'H','t':'I','u':'L','v':'L','g':'N','r':'O','d':'R','o':'R','l':'V',
       'a':'TPAB','e':'EG','m':'SDX','n':'MQ','D':'R',
       'i':'ECZG'}   # the short-stroke sign: Lasry's i = C/Z, but this hand also writes e that way
PRIOR = {('i','E'):0.0,('i','C'):-0.3,('i','Z'):-1.5,('i','G'):-1.5,('a','B'):-1.0,('a','A'):-0.7,('m','X'):-1.0,('e','G'):-0.7}
def decode_run(run, ctx, B=400):
    beams = [(0.0, ctx, '')]
    for ch in run:
        if ch == ' ':
            beams = [(s, (c + ' ')[-3:], o + ' ') for s, c, o in beams]; continue
        cands = KEY.get(ch, '?')
        nb = {}
        for s, c, o in beams:
            for p in cands:
                s2 = s + (lp((c + p.lower())[-4:]) if len(c) == 3 else 0) + PRIOR.get((ch, p), 0)
                c2 = (c + p.lower())[-3:]; k = (c2, o[-8:] + p)
                if k not in nb or nb[k][0] < s2: nb[k] = (s2, c2, o + p)
        beams = sorted(nb.values(), key=lambda x: -x[0])[:B]
    return beams[0]
def main():
  out = []
  for line in open('transcription.txt', encoding='utf-8'):
      line = line.rstrip('\n')
      if line.startswith('#'): continue
      if line.startswith('=='): out.append('\n' + line); continue
      ctx, res = '   ', []
      for part in re.split(r'(\[[^\]]*\])', line):
          if part.startswith('['):
              res.append(part[1:-1].lower()); ctx = ('   ' + re.sub('[^a-z ]', '', part[1:-1].lower()))[-3:]
          elif part.strip():
              s, ctx, o = decode_run(part.strip(), ctx); res.append(o)
      out.append(' '.join(res))
  txt = '\n'.join(out)
  open('decoded.txt', 'w', encoding='utf-8').write(txt + '\n'); print(txt)

if __name__ == "__main__": main()
