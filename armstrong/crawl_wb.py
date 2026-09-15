"""Follow Founders Online 'Preceding/Next between these correspondents' links through the Wayback Machine,
starting from known Armstrong->Madison documents, and record which pages contain code numbers."""
import re, json, sys, time, urllib.request, html
seen = {}; queue = ['99-01-02-3466', '99-01-02-2728', '99-01-02-2733', '99-01-02-3462', '99-01-02-3503']
def fetch(id):
    url = f'https://web.archive.org/web/2024id_/https://founders.archives.gov/documents/Madison/{id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        return urllib.request.urlopen(req, timeout=90).read().decode('utf-8', 'ignore')
    except Exception as e:
        return None
while queue and len(seen) < 120:
    id = queue.pop(0)
    if id in seen: continue
    t = fetch(id)
    if not t:
        seen[id] = {'ok': False}; print(id, 'MISSING', flush=True); continue
    title = re.search(r'<title>(.*?)</title>', t, re.S); title = html.unescape(title.group(1)).strip() if title else ''
    body = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)))
    nums = re.findall(r'\b\d{3,4}\b\.', body)
    links = sorted(set(re.findall(r'documents/Madison/(99-01-02-\d+)', t)))
    seen[id] = {'ok': True, 'title': title[:80], 'ncodes': len(nums), 'links': links}
    print(id, '|', title[:70], '| codes:', len(nums), '| links:', links, flush=True)
    if 'Armstrong' in title:
        for l in links:
            if l not in seen: queue.append(l)
    time.sleep(1)
json.dump(seen, open('wb_crawl.json', 'w'), indent=1)
print('DONE', len(seen))
