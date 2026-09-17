import sys, time, re, html, urllib.request, os
vols = {'bsb10720286': 486, 'bsb10720287': 564, 'bsb10720288': 440}
for vid, n in vols.items():
    out = open(f'catinat1819_{vid}.txt', 'w', encoding='utf-8')
    for p in range(1, n + 1):
        url = f'https://api.digitale-sammlungen.de/ocr/{vid}/{p}'
        for attempt in range(6):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                data = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
                break
            except Exception as e:
                data = ''
                time.sleep(5 * (attempt + 1))
        words = re.findall(r"<span class='ocrx_word'[^>]*>(.*?)</span>|<span class=\"ocrx_word\"[^>]*>(.*?)</span>", data, re.S)
        lines = re.findall(r'<span class="ocr_line"[^>]*>(.*?)</span>\s*</span>', data, re.S)
        text = re.sub(r'<[^>]+>', ' ', data)
        text = html.unescape(re.sub(r'\s+', ' ', text))
        out.write(f'\n=====SCAN {p}=====\n{text}\n')
        out.flush()
        time.sleep(0.3)
    out.close()
    print(vid, 'done', flush=True)
