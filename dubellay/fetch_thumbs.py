"""Fetch thumbnails of every canvas of fr. 3077 and fr. 3078 from Gallica IIIF (paced, waits out outages).

usage: python fetch_thumbs.py [width] [vol ...]
"""
import json, os, sys, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
VOLS = {"3077": "btv1b90599292", "3078": "btv1b9060311s"}
WIDTH = int(sys.argv[1]) if len(sys.argv) > 1 else 400
vols = sys.argv[2:] or list(VOLS)


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def wait_for_gallica():
    while True:
        try:
            get("https://gallica.bnf.fr/iiif/ark:/12148/btv1b90599292/f5/info.json", timeout=20)
            return
        except Exception as e:
            print("gallica down:", e, flush=True)
            time.sleep(90)


for vol in vols:
    ark = VOLS[vol]
    man = json.load(open(os.path.join(HERE, "ref", f"manifest_{ark}.json"), encoding="utf-8"))
    n = len(man["sequences"][0]["canvases"])
    out = os.path.join(HERE, "img", f"th{vol}")
    os.makedirs(out, exist_ok=True)
    for i in range(1, n + 1):
        fn = os.path.join(out, f"c{i:03d}.jpg")
        if os.path.exists(fn) and os.path.getsize(fn) > 2000:
            continue
        url = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{WIDTH},/0/native.jpg"
        fails = 0
        while True:
            try:
                data = get(url)
                if len(data) < 2000:
                    raise IOError("short response %d" % len(data))
                open(fn, "wb").write(data)
                print(vol, i, len(data), flush=True)
                break
            except Exception as e:
                fails += 1
                print(vol, i, "fail", fails, e, flush=True)
                if "429" in str(e):
                    time.sleep(120)
                else:
                    wait_for_gallica()
        time.sleep(1.3)
print("done")
