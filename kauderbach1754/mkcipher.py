# write cipher/R<rec>.txt: realigned code pairs (nulls 5/8 and stray digits removed), one run per line
import re, glob, os, decode

FILES = sorted(glob.glob('decode/DOC*.txt')) + sorted(glob.glob('trans/R*.txt'))
os.makedirs('cipher', exist_ok=True)
allp = []
for f in FILES:
    rec = re.search(r'R(\d+)', os.path.basename(f)).group(1)
    t = open(f, encoding='utf-8-sig').read()
    t = re.sub(r'#.*', '', t)
    lines = []
    for p in re.split(r'<CLEARTEXT[^>]*>', t):
        for chunk in re.split(r'[,%]', p):
            d = re.sub(r'[^0-9]', '', chunk).replace('5', '').replace('8', '')
            if len(d) < 2:
                continue
            tk = [x for x in decode.align1(d) if not x.startswith('*')]
            if tk:
                lines.append(' '.join(tk))
    open(f'cipher/R{rec}.txt', 'w').write('\n'.join(lines))
    allp += lines
open('cipher/all.txt', 'w').write('\n'.join(allp))
