"""Fetch selected canvases of fr. 3077 / fr. 3078 at a given width from Gallica IIIF (paced, outage-tolerant).

usage: python fetch_pages.py WIDTH VOL RANGE [RANGE ...]      e.g.  python fetch_pages.py 2000 3077 112-130 140-150
"""
import os, sys, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
VOLS = {"3077": "btv1b90599292", "3078": "btv1b9060311s"}
width = sys.argv[1]
vol = sys.argv[2]
ark = VOLS[vol]
canvases = []
for r in sys.argv[3:]:
    a, _, b = r.partition("-")
    canvases += list(range(int(a), int(b or a) + 1))
out = os.path.join(HERE, "img", f"p{vol}_{width}")
os.makedirs(out, exist_ok=True)


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


for i in canvases:
    fn = os.path.join(out, f"c{i:03d}.jpg")
    if os.path.exists(fn) and os.path.getsize(fn) > 20000:
        continue
    size = "full" if width == "full" else f"{width},"
    url = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{size}/0/native.jpg"
    fails = 0
    while True:
        try:
            data = get(url)
            if len(data) < 20000:
                raise IOError("short response %d" % len(data))
            open(fn, "wb").write(data)
            print(vol, i, len(data), flush=True)
            break
        except Exception as e:
            fails += 1
            print(vol, i, "fail", fails, e, flush=True)
            time.sleep(120 if "429" in str(e) else 60)
    time.sleep(3.0)
print("done")
