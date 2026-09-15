"""Download DECODE thumbnail/preview images for records R2734 (Charost 1673), R2733 (Gravel 1674), R2678 (Ratisbon 1665)."""
import re, urllib.request, os
H = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('decode', exist_ok=True)
for rid in [2734, 2733, 2678]:
    html = urllib.request.urlopen(urllib.request.Request(f'https://de-crypt.org/decrypt-web/RecordsView/{rid}', headers=H), timeout=60).read().decode('utf-8', 'ignore')
    files = sorted(set(re.findall(r'filesrv/\?file=([A-Za-z0-9_\.]+)', html)))
    print(rid, files)
    for f in files:
        for variant in [f, f.replace('TH_', '')]:
            url = 'https://de-crypt.org/decrypt-custom/filesrv/?file=' + variant
            try:
                data = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120).read()
                fn = os.path.join('decode', variant)
                open(fn, 'wb').write(data)
                print('  ', variant, len(data))
            except Exception as e:
                print('  ', variant, 'ERR', e)
