"""Small fetch helper: python fetch.py URL OUTFILE"""
import sys, urllib.request, ssl

def fetch(url, out, timeout=60):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        data = r.read()
    with open(out, "wb") as f:
        f.write(data)
    print(f"{url} -> {out} ({len(data)} bytes)")

if __name__ == "__main__":
    fetch(sys.argv[1], sys.argv[2])
