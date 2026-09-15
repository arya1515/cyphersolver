"""Search archive.org for the printed sources."""
import json, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from fetch import fetch

queries = [
    'title:("court and society" elizabeth anne)',
    'title:("historical manuscripts" eighth report)',
    'title:(manuscripts duke of manchester)',
    'title:(eighth report) AND creator:(historical manuscripts)',
    'stepney AND title:(letters OR papers) AND date:[1700-01-01 TO 1930-12-31] AND mediatype:texts AND (subject:stepney OR title:stepney)',
]
os.makedirs("ia", exist_ok=True)
for i, q in enumerate(queries):
    url = ("https://archive.org/advancedsearch.php?q=" + urllib.parse.quote(q) +
           "&fl[]=identifier&fl[]=title&fl[]=date&fl[]=volume&rows=50&output=json")
    out = f"ia/search{i}.json"
    try:
        fetch(url, out)
        d = json.load(open(out, encoding="utf-8"))
        print("QUERY:", q)
        for doc in d["response"]["docs"]:
            print("  ", doc.get("identifier"), "|", str(doc.get("title"))[:90], "|", doc.get("date"), "|", doc.get("volume"))
    except Exception as e:
        print("FAIL", q, e)
