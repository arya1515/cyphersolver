"""Walk Founders 'Preceding/Next' correspondent chain via Wayback; record coded letters.
python chain.py start_id out.tsv"""
import sys, re, os, html, time, requests
start, out = sys.argv[1], sys.argv[2]
s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0'
def get(i):
    p = f'fo/{i}.html'
    if os.path.exists(p) and os.path.getsize(p) > 2000:
        return open(p, encoding='utf8', errors='ignore').read()
    for k in range(4):
        try:
            r = s.get(f'https://web.archive.org/web/2025id_/https://founders.archives.gov/documents/Madison/{i}', timeout=60)
            if r.status_code == 200 and len(r.text) > 2000:
                open(p, 'w', encoding='utf8').write(r.text); return r.text
        except Exception: pass
        time.sleep(3)
    return ''
seen = {}
for direction in ('Preceding', 'Next'):
    cur = start
    while cur and cur not in seen or (cur == start and direction == 'Next'):
        t = get(cur)
        if cur not in seen:
            title = re.search(r'<title>(.*?)</title>', t, re.S)
            title = title.group(1).strip() if title else '?'
            nit = len(re.findall('font-style: italic', t))
            s2 = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', t)))
            m = re.search(r'(RC|FC|Tr|Dupl|Extract)[^.]{0,20}\( ?DNA.{0,400}', s2)
            code = 'code' if re.search(r'encoded|in code|decod', s2) else ''
            seen[cur] = (title, nit, code, (m.group(0)[:200] if m else ''))
            print(cur, title, nit, code, flush=True)
        m = re.search(direction + r'</dt><dd><a href="/documents/Madison/([^"]+)"', t)
        nxt = m.group(1) if m else None
        if nxt in seen: break
        cur = nxt
with open(out, 'w', encoding='utf8') as f:
    for k in sorted(seen):
        f.write('\t'.join([k] + [str(x) for x in seen[k]]) + '\n')
