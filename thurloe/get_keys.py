import urllib.request, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "keys"); os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
names = sys.argv[1:] or ["charlesii2a.jpg", "charlesii2.jpg", "charlesii2b.jpg", "charlesii2c.jpg",
                         "marshall.jpg", "hague.jpg", "stamford.jpg", "butler.jpg", "charlesII1.jpg", "kingston1.jpg"]
for n in names:
    dest = os.path.join(OUT, n)
    if os.path.exists(dest): print("have", n); continue
    req = urllib.request.Request("https://cryptiana.web.fc2.com/code/" + n, headers={"User-Agent": UA})
    try:
        data = urllib.request.urlopen(req, timeout=60).read()
        open(dest, "wb").write(data); print("ok", n, len(data))
    except Exception as e:
        print("FAIL", n, e)
