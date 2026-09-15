"""Build quadgram counts for Dutch / French from Project Gutenberg texts -> lm_<lang>.json"""
import urllib.request, json, re, os, sys, collections, time
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=90).read()
lang = sys.argv[1]            # nl or fr
want = int(sys.argv[2]) if len(sys.argv) > 2 else 6
books = []
url = f"https://gutendex.com/books?languages={lang}&sort=popular"
while url and len(books) < want:
    j = json.loads(get(url))
    for b in j["results"]:
        if b["languages"] != [lang]: continue
        fmts = b["formats"]
        txt = next((v for k, v in fmts.items() if k.startswith("text/plain")), None)
        if txt: books.append((b["title"], txt))
        if len(books) >= want: break
    url = j.get("next")
cnt = collections.Counter(); total = 0
ALPH = "abcdefghijklmnopqrstuvwxyz"
for title, u in books:
    try:
        raw = get(u).decode("utf-8", "replace")
    except Exception as e:
        print("FAIL", title, e); continue
    m = re.search(r"\*\*\* ?START.*?\*\*\*(.*)\*\*\* ?END", raw, re.S)
    body = m.group(1) if m else raw
    # fold accents
    body = body.lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"), ("ä", "a"), ("ù", "u"), ("û", "u"),
                 ("ü", "u"), ("ô", "o"), ("ö", "o"), ("î", "i"), ("ï", "i"), ("ç", "c"), ("œ", "oe"), ("æ", "ae")]:
        body = body.replace(a, b)
    s = re.sub("[^a-z]", "", body)
    for i in range(len(s) - 3):
        cnt[s[i:i+4]] += 1
    total += len(s)
    print("ok", title[:50], len(s))
    time.sleep(1)
json.dump({"quad": cnt, "total": total}, open(os.path.join(HERE, f"lm_{lang}.json"), "w"))
print("quads", len(cnt), "chars", total)
