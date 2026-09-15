"""Fetch BHO Thurloe pages (raw HTML) into thurloe/html/."""
import sys, os, urllib.request, time
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "html")
os.makedirs(OUT, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
PAGES = {
    "vol5_pp72-83": "https://www.british-history.ac.uk/thurloe-papers/vol5/pp72-83",
    "vol5_pp258-271": "https://www.british-history.ac.uk/thurloe-papers/vol5/pp258-271",
    "vol5_pp333-350": "https://www.british-history.ac.uk/thurloe-papers/vol5/pp333-350",
}
for extra in sys.argv[1:]:          # e.g. vol1/pp430-440
    PAGES[extra.replace("/", "_")] = "https://www.british-history.ac.uk/thurloe-papers/" + extra
for name, url in PAGES.items():
    dest = os.path.join(OUT, name + ".html")
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print("have", name); continue
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        open(dest, "wb").write(data)
        print("ok", name, len(data))
    except Exception as e:
        print("FAIL", name, url, e)
    time.sleep(2)
