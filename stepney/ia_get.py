"""Download OCR djvu text for archive.org items."""
import json, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from fetch import fetch

ids = sys.argv[1:] or ["courtsocietyfrom02mancuoft", "EighthReportHistoricalMSS", "courtsocietyfrom01mancuoft"]
os.makedirs("ia", exist_ok=True)
for ident in ids:
    meta = f"ia/{ident}_meta.json"
    if not os.path.exists(meta):
        fetch(f"https://archive.org/metadata/{ident}", meta)
    d = json.load(open(meta, encoding="utf-8"))
    files = d.get("files", [])
    txts = [f["name"] for f in files if f["name"].endswith("_djvu.txt")]
    print(ident, "files:", len(files), "txt:", txts)
    for name in txts:
        out = f"ia/{ident}_djvu.txt"
        if not os.path.exists(out):
            fetch(f"https://archive.org/download/{ident}/{urllib.parse.quote(name)}", out)
