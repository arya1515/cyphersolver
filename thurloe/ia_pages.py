"""Find leaf numbers in IA scans of Thurloe SP for our four letters and download page images to ia/.
usage: ia_pages.py"""
import urllib.request, json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "ia"); os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
QUERIES = {"collectionofstat05thur": ["Copinger", "Waddall", "Barriere", "greattar"],
           "collectionofstat01thur": ["Solebay", "Jongestall"]}
for item, qs in QUERIES.items():
    md = json.loads(get(f"https://archive.org/metadata/{item}"))
    server, d = md["server"], md["dir"]
    djvu = next((f["name"] for f in md["files"] if f["name"].endswith("_djvu.xml")), None)
    print(item, server, d, djvu)
    for q in qs:
        url = f"https://{server}/fulltext/inside.php?item_id={item}&doc={item}&path={d}&q={urllib.parse.quote(q)}"
        try:
            j = json.loads(get(url))
        except Exception as e:
            print("  inside.php FAIL", q, e); continue
        for m in j.get("matches", []):
            for p in m.get("par", []):
                leaf = p.get("page"); txt = m.get("text", "")[:160].replace("\n", " ")
                print(f"  {q}: leaf {leaf}: {txt}")
                dest = os.path.join(OUT, f"{item}_n{leaf}.jpg")
                if not os.path.exists(dest):
                    try:
                        open(dest, "wb").write(get(f"https://archive.org/download/{item}/page/n{leaf}_w1600.jpg"))
                        print("    saved", dest)
                    except Exception as e:
                        print("    img FAIL", e)
