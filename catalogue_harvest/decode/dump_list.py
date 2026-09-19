"""Dump the DECODE (de-crypt.org) record list via its JSON API. Needs bordeaux/decode/cookie.txt
(logged-in browser cookie) and a JWT taken from any RecordsView page (API_JWT_TOKEN)."""
import json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "https://de-crypt.org/decrypt-web/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def cookie():
    return open(os.path.join(ROOT, "bordeaux", "decode", "cookie.txt"), encoding="utf-8").read().strip()

def get(url, hdr=None):
    h = {"User-Agent": UA, "Cookie": cookie()}
    h.update(hdr or {})
    return op.open(urllib.request.Request(url, headers=h), timeout=120).read().decode("utf-8", "replace")

def jwt():
    html = get(BASE + "RecordsView/7537")
    return re.search(r'"API_JWT_TOKEN":"([^"]+)"', html).group(1)

def api(path, tok):
    return json.loads(get(BASE + "api/" + path, {"X-Authorization": "Bearer " + tok}))

if __name__ == "__main__":
    tok = jwt()
    out, start = [], 1
    while True:
        d = api("list/Records?recperpage=500&start=%d" % start, tok)
        recs = d.get("records") or []
        out += recs
        print(start, len(recs), d.get("totalRecordCount"), flush=True)
        if len(recs) < 500: break
        start += 500
        time.sleep(1)
    json.dump(out, open(os.path.join(HERE, "list.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("total", len(out))
