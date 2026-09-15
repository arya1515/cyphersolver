"""Download several cryptiana pages and grep them for keywords."""
import re, html, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fetch import fetch

pages = ["blencowe.htm", "blencowe2.htm", "glorious.htm", "wallis2.htm", "wallis3.htm",
         "1709richards.htm", "hardnuts.htm", "davys_e.htm", "state.htm", "rijswijk.htm"]
os.makedirs("cryptiana", exist_ok=True)
for p in pages:
    out = os.path.join("cryptiana", p)
    if not os.path.exists(out):
        try:
            fetch("https://cryptiana.web.fc2.com/code/" + p, out)
        except Exception as e:
            print("FAIL", p, e)
            continue
    raw = open(out, "rb").read().decode("utf-8", "replace")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt = re.sub(r"\s+", " ", txt)
    for kw in ["Manchester", "Stepney", "454", "Kimbolton", "Montagu"]:
        for m in re.finditer(kw, txt):
            s = max(0, m.start() - 250); e = min(len(txt), m.end() + 250)
            print(f"--- {p} [{kw}]: ...{txt[s:e]}...")
