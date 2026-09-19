"""Group DECODE non-decrypted / partly decrypted ciphertext records into candidate targets and write a digest."""
import json, os, re, html, collections as C
HERE = os.path.dirname(os.path.abspath(__file__))
known = set(json.load(open(os.path.join(HERE, "known_ids.json"))))
V = {}
for f in ("views.jsonl", "views_b.jsonl", "views_c.jsonl"):
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); V[r["id"]] = r
STATUS = {"1": "Decrypted", "2": "Non-decrypted", "3": "Partially decrypted", "4": "N/A"}
def txt(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = s.replace("The image is not in the public domain. Publishing it is only possible with the permission of the Library.", "")
    return re.sub(r"\s+", " ", s).strip()
def n(s): return (s or "").strip() if s not in (None, "None") else ""
def date(r):
    y, m, d = n(r["start_year"]), n(r["start_month"]), n(r["start_day"])
    s = "-".join(x for x in (y, m.zfill(2) if m else "", d.zfill(2) if d else "") if x)
    if n(r["end_year"]) and n(r["end_year"]) != y: s += "/" + n(r["end_year"])
    return s
def holder_base(h):
    """Series-level shelfmark: cut at the first folio / item / page reference."""
    h = re.sub(r"\s+", " ", h or "")
    h = re.split(r"[,\s]+(?:f|ff|fol|fols|fo|folio|folios|no|nr|n°|nº|doc|p|pp|document|item|pieza|núm|num)\.?\s*\d", h, maxsplit=1, flags=re.I)[0]
    return h.strip(" ,.;")[:90]
rows = []
for r in V.values():
    if r.get("record_type") != "1" or r.get("status") not in ("2", "3"): continue
    rows.append(r)
groups = C.defaultdict(list)
for r in rows:
    y = n(r["start_year"]); dec = (int(y) // 10 * 10) if y.isdigit() else None
    k = (n(r["current_city"]), holder_base(n(r["current_holder"])), n(r["author"]) or n(r["sender"]), n(r["receiver"]), dec // 50 * 50 if dec else None)
    groups[k].append(r)
out = []
for k, rs in sorted(groups.items(), key=lambda kv: (kv[0][4] or 9999, kv[0][0], kv[0][1])):
    rs.sort(key=lambda r: int(r["id"]))
    ids = [int(r["id"]) for r in rs]
    out.append({
        "key": list(k), "n": len(rs), "ids": ids, "known": [i for i in ids if i in known],
        "records": [{
            "id": int(r["id"]), "name": n(r["name"]), "holder": n(r["current_holder"]), "city": n(r["current_city"]),
            "date": date(r), "author": n(r["author"]), "sender": n(r["sender"]), "receiver": n(r["receiver"]),
            "origin": ", ".join(x for x in (n(r["origin_city"]), n(r["origin_region"])) if x),
            "clear": n(r["cleartext_lang"]), "plain": n(r["plaintext_lang"]), "pages": n(r["number_of_pages"]),
            "status": STATUS.get(r["status"]), "cipher_types": n(r["cipher_types"]), "symbols": n(r["symbol_sets"]),
            "cipher_other": n(r["cipher_type_other"]), "symbol_other": n(r["symbol_set_other"]),
            "access": "public" if r.get("access_mode") == "1" else "login", "info": txt(r["additional_information"])[:600],
        } for r in rs]})
json.dump(out, open(os.path.join(HERE, "groups.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "records", len(out), "groups", sum(1 for g in out if not g["known"]), "groups with no known id")
