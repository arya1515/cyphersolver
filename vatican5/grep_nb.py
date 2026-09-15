"""Grep the downloaded Nuntiaturberichte OCR volumes for the 15 April 1542 Farnese->Poggio letter and Poggio's 1542 cipher."""
import re, pathlib, glob
HERE = pathlib.Path(__file__).parent
pats = [r'15\.?\s*April\s*1542', r'Aprile\s*1542', r'Osma', r'Montepulciano', r'Poggio', r'Spira', r'[Cc]hiffr', r'Ziffer', r'dechiffr', r'1542']
for p in sorted(HERE.glob('nb_*.txt')):
    t = p.read_text(encoding='utf-8', errors='ignore')
    head = re.sub(r'\s+', ' ', t[:6000])
    m = re.search(r'([A-Za-zä]+ter|Erster|Zweiter|Dritter|Vierter|Fünfter|Sechster|Siebenter|Achter|Neunter|Zehnter|Elfter|Zwölfter)\s+Band', head)
    counts = {pt: len(re.findall(pt, t)) for pt in pats}
    print(f"{p.name:36} {m.group(0) if m else '?':18} " + ' '.join(f'{k[:8]}={v}' for k, v in counts.items()))
