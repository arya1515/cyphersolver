import urllib.request, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "ia")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"}
item = sys.argv[1]
for leaf in sys.argv[2:]:
    dest = os.path.join(OUT, f"{item}_n{leaf}.jpg")
    if os.path.exists(dest): print("have", dest); continue
    url = f"https://archive.org/download/{item}/page/n{leaf}_w1600.jpg"
    open(dest, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
    print("saved", dest)
