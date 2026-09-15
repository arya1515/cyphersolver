"""Download Gallica IIIF manifest for an ark and list canvases whose label matches folios; optionally download images.
usage: python gallica_iiif.py <ark> <label-regex> [download-dir]"""
import sys, json, re, urllib.request, os, time
ark, pat = sys.argv[1], sys.argv[2]
outdir = sys.argv[3] if len(sys.argv) > 3 else None
H = {'User-Agent': 'Mozilla/5.0 (research script)'}
man = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/manifest.json', headers=H), timeout=120).read())
cvs = man['sequences'][0]['canvases']
print('canvases', len(cvs))
for i, c in enumerate(cvs, 1):
    lab = c.get('label', '')
    if re.search(pat, str(lab)):
        print(i, lab)
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            url = f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/full/0/native.jpg'
            fn = os.path.join(outdir, f'{ark}_f{i}.jpg')
            if not os.path.exists(fn):
                data = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=300).read()
                open(fn, 'wb').write(data); print('  saved', fn, len(data)); time.sleep(2)
