"""Download all frames of an M31/M35 reel from the NARA catalogue (manifest from the proxy search).
Usage: python dl.py objects_reel012.json img012 [start end]"""
import sys, os, json, time
import requests
from concurrent.futures import ThreadPoolExecutor
man, out = sys.argv[1], sys.argv[2]
objs = [o for o in json.load(open(man)) if o[2].endswith(".jpg")]
if len(sys.argv) > 4:
    a, b = int(sys.argv[3]), int(sys.argv[4])
    objs = [o for o in objs if a <= int(o[2].split('-')[-1][:4]) <= b]
os.makedirs(out, exist_ok=True)
def get(o):
    size, url, name = o
    p = os.path.join(out, name)
    if os.path.exists(p) and os.path.getsize(p) > 10000:
        return
    s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (research)'
    for k in range(4):
        try:
            r = s.get(url, timeout=180)
            if r.status_code == 200 and len(r.content) > 10000:
                open(p, 'wb').write(r.content); return
        except Exception as e:
            pass
        time.sleep(5)
    print('FAIL', name, flush=True)
with ThreadPoolExecutor(6) as ex:
    list(ex.map(get, objs))
print('done', out)
