"""Download IIIF images from Yale collections: python yale_iiif.py <first_id> <count> <prefix>"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fetch import fetch

first = int(sys.argv[1]); n = int(sys.argv[2]); prefix = sys.argv[3]
os.makedirs("img", exist_ok=True)
for i in range(n):
    iid = first + i
    out = f"img/{prefix}_{i+1:02d}.jpg"
    if os.path.exists(out):
        print("have", out); continue
    url = f"https://collections.library.yale.edu/iiif/2/{iid}/full/full/0/default.jpg"
    try:
        fetch(url, out)
    except Exception as e:
        print("FAIL", url, e)
        try:
            fetch(f"https://collections.library.yale.edu/iiif/2/{iid}/full/max/0/default.jpg", out)
        except Exception as e2:
            print("FAIL2", e2)
