"""Query Yale collections (Blacklight) JSON API for the Manchester papers items."""
import json, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from fetch import fetch

os.makedirs("yale", exist_ok=True)
queries = sys.argv[1:] or ["Stepney Manchester 1702", "Osborn fc37", "Manchester cipher 1702 Stepney"]
for i, q in enumerate(queries):
    url = "https://collections.library.yale.edu/catalog.json?" + urllib.parse.urlencode({"q": q, "search_field": "all_fields", "per_page": 50})
    out = f"yale/search_{i}.json"
    try:
        fetch(url, out)
        d = json.load(open(out, encoding="utf-8"))
        docs = d.get("data", []) or d.get("response", {}).get("docs", [])
        print("QUERY:", q, "->", len(docs), "results; total", d.get("meta", {}).get("pages", {}).get("total_count"))
        for doc in docs[:50]:
            a = doc.get("attributes", doc)
            title = a.get("title_tesim", {}).get("attributes", {}).get("value") if isinstance(a.get("title_tesim"), dict) else a.get("title_tesim")
            print("  ", doc.get("id"), "|", str(title)[:120])
    except Exception as e:
        print("FAIL", q, e)
