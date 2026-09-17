"""Score hand transcriptions with the sp53 French 6-gram LM; report coverage.
Usage (from raince/): python score_trans.py trans/f29r.txt [more...]"""
import sys, re, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sp53'))
from homo import LM

lm = LM(os.path.join(os.path.dirname(__file__), '..', 'sp53', 'fr6.pkl'))

for fn in sys.argv[1:]:
    txt = open(fn, encoding='utf-8').read()
    lines = [l for l in txt.splitlines() if re.match(r'^\d\d(-\d+)? ?\|', l)]
    body = ' '.join(l.split('|', 1)[1].strip() for l in lines)
    body = re.sub(r'\[[^\]]*\]', ' ', body)
    nq = body.count('?')
    clean = re.sub(r"[^a-z ]", '', body.lower().replace('?', ''))
    clean = re.sub(r'  +', ' ', clean).strip()
    letters = clean.replace(' ', '')
    sc = lm.score(letters) / max(len(letters), 1)
    print(f"{fn}: {len(lines)} lines, {len(letters)} letters, {nq} '?', 6-gram/letter {sc:.2f}")
