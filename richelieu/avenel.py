"""Download Avenel vol. III (1628-1630) full text from Internet Archive and grep for context terms."""
import requests, re, pathlib, sys
HERE = pathlib.Path(__file__).parent
ID = 'bub_gb_OIQItRIybmIC'
p = HERE / 'avenel3.txt'
if not p.exists():
    meta = requests.get(f'https://archive.org/metadata/{ID}', timeout=60).json()
    txt = [f['name'] for f in meta['files'] if f['name'].endswith('_djvu.txt')]
    print('files:', txt)
    r = requests.get(f'https://archive.org/download/{ID}/{txt[0]}', timeout=300)
    p.write_bytes(r.content)
t = p.read_text(encoding='utf-8', errors='ignore')
print(len(t), 'chars')
terms = sys.argv[1:] or ['Ranc', 'Brassac', 'Vincennes', 'Bonneuil', 'Vautier', 'Marcheville', 'Privat', 'Aigremont']
for term in terms:
    hits = [m.start() for m in re.finditer(term, t)]
    print(f'\n===== {term}: {len(hits)} hits')
    for h in hits[:40]:
        s = t[max(0, h-250):h+350].replace('\n', ' ')
        print('...', re.sub(r'\s+', ' ', s), '...\n')
