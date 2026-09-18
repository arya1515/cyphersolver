"""Minimal PARES client: search, and download the images of a record."""
import re, sys, os, urllib.parse, urllib.request, http.cookiejar
BASE = 'https://pares.cultura.gob.es/ParesBusquedas20'
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [('User-Agent', 'Mozilla/5.0')]

def get(url):
    return op.open(url, timeout=60).read()

def search(text, pages=1):
    out = []
    for p in range(1, pages + 1):
        q = urllib.parse.urlencode({'nm': '', 'texto': text, 'tambloque': 100, 'pagina': p})
        h = get(f'{BASE}/catalogo/find?{q}').decode('latin-1')
        for m in re.finditer(r'href="/ParesBusquedas20/catalogo/description/(\d+)\?nm"[^>]*?(?:title=\'([^\']*)\')?[^>]*>([^<]*)<', h):
            seg = re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', h[m.end():m.end() + 1500]))
            f = re.search(r'Fechas: (\S+(?: / \S+)?) Signatura: (\S+)', seg)
            title = (m.group(2) or m.group(3)).replace('&nbsp;', '').strip()
            out.append((m.group(1), f.group(2) if f else '?', f.group(1) if f else '?', title))
        if 'raquo' not in h: break
    return out

def images(nid, outdir, prefix):
    h = get(f'{BASE}/catalogo/show/{nid}').decode('latin-1')
    codes = sorted(set(re.findall(r'txt_id_imagen=(\d+)&txt_rotar=0&txt_contraste=0&dbCode=(\d+)', h)), key=lambda x: int(x[0]))
    os.makedirs(outdir, exist_ok=True)
    files = []
    for i, db in codes:
        fn = os.path.join(outdir, f'{prefix}_{i}.jpg')
        if not os.path.exists(fn):
            data = get(f'{BASE}/ViewImage.do?accion=42&txt_descarga=1&dbCode={db}&txt_id_imagen={i}&txt_zoom=10&txt_contraste=0&txt_polarizado=&txt_brillo=10.0&txt_contrast=1.0&txt_transformacion=-1')
            open(fn, 'wb').write(data)
        files.append(fn)
    return files

if __name__ == '__main__':
    if sys.argv[1] == 'search':
        seen = set()
        for r in search(' '.join(sys.argv[2:]), pages=3):
            if r[0] in seen: continue
            seen.add(r[0])
            if r[1].startswith(('EST', 'PTR', 'CCA')): print(*r, sep=' | ')
    elif sys.argv[1] == 'img':
        print(images(sys.argv[2], 'img', sys.argv[3]))
