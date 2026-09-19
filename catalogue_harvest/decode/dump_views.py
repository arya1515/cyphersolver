"""Fetch full API views for every DECODE ciphertext record not marked Decrypted. Resumable (views.jsonl)."""
import json, os, time, dump_list as D
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "list.json"), encoding="utf-8"))
want = [r["id"] for r in L if r["record_type"] in ("1", None, "3") and r["status"] != "1"]
p = os.path.join(HERE, "views.jsonl")
have = set()
if os.path.exists(p):
    have = {json.loads(l)["id"] for l in open(p, encoding="utf-8")}
for q in ("views_b.jsonl", "views_c.jsonl"):
    qq = os.path.join(HERE, q)
    if os.path.exists(qq): have |= {json.loads(l)["id"] for l in open(qq, encoding="utf-8") if l.strip()}
tok = D.jwt()
with open(p, "a", encoding="utf-8") as f:
    for n, i in enumerate(want):
        if i in have: continue
        for t in range(3):
            try:
                v = D.api("view/Records/%s" % i, tok)["records"]; break
            except Exception as e:
                time.sleep(5); tok = D.jwt()
        else:
            print("fail", i); continue
        f.write(json.dumps(v, ensure_ascii=False) + "\n"); f.flush()
        if n % 100 == 0: print(n, len(want), flush=True)
        time.sleep(0.25)
print("done")
