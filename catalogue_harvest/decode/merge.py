"""Merge the scored agent output (out_*.jsonl) into catalogue.json as new entries.

Usage: python merge.py <path to catalogue.json> [--dry]
Checks that every DECODE id of every batch appears exactly once (entry or exclude), assigns ids after the
current maximum, adds DECODE record links, and writes excluded.json (the excluded ids with reasons).
Entries already merged (matched on decode_ids) are skipped, so it can be rerun as batches arrive.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = "https://de-crypt.org/decrypt-web/RecordsView/"
PERIODS = {"before 1497", "1497-1559", "1560-1589", "1589-1598", "1598-1610", "1611-1650", "1651-1700",
           "1701-1800", "1801-1900", "unknown"}
FIELDS = ["counted", "year", "date", "title", "correspondents", "place", "language", "region", "period",
          "shelfmark", "folio_note", "cls", "status", "why", "importance", "solvability", "difficulty",
          "score_note", "verify"]


def load_batches():
    lines, problems = [], []
    for f in sorted(glob.glob(os.path.join(HERE, "out_*.jsonl"))):
        n = os.path.basename(f)[4:-6]
        want = {i for g in json.load(open(os.path.join(HERE, f"batch_{n}.json"), encoding="utf-8")) for i in g["ids"]}
        seen = []
        for k, l in enumerate(open(f, encoding="utf-8"), 1):
            if not l.strip():
                continue
            try:
                o = json.loads(l)
            except Exception as e:
                problems.append(f"{f}:{k} bad json {e}")
                continue
            o["_batch"] = n
            seen += o.get("decode_ids", [])
            lines.append(o)
        missing, extra = want - set(seen), set(seen) - want
        dup = {i for i in seen if seen.count(i) > 1}
        if missing or extra or dup:
            problems.append(f"batch {n}: missing {sorted(missing)[:20]} ({len(missing)}), extra {sorted(extra)[:10]}, dup {sorted(dup)[:10]}")
    return lines, problems


def check(o):
    errs = [k for k in FIELDS if k not in o]
    for k in ("importance", "solvability", "difficulty"):
        if not isinstance(o.get(k), int) or not 1 <= o[k] <= 5:
            errs.append(f"{k}={o.get(k)!r}")
    if o.get("cls") not in ("A", "B", "C"):
        errs.append(f"cls={o.get('cls')!r}")
    if o.get("period") not in PERIODS:
        errs.append(f"period={o.get('period')!r}")
    return errs


def main():
    cat_path = sys.argv[1]
    dry = "--dry" in sys.argv
    cat = json.load(open(cat_path, encoding="utf-8"))
    E = cat["entries"]
    have = {tuple(sorted(e.get("decode_ids") or [])) for e in E if e.get("decode_ids")}
    lines, problems = load_batches()
    for p in problems:
        print("PROBLEM", p)
    nid = max(e["id"] for e in E) + 1
    added, excl = 0, []
    for o in lines:
        if o.get("type") == "exclude":
            excl.append({"decode_ids": o["decode_ids"], "reason": o.get("reason", ""), "batch": o["_batch"]})
            continue
        errs = check(o)
        if errs:
            print("SKIP", o.get("decode_ids"), o.get("title"), errs)
            continue
        ids = sorted(o["decode_ids"])
        if tuple(ids) in have:
            continue
        e = {"id": nid, "counted": bool(o["counted"])}
        for k in FIELDS[1:]:
            e[k] = o[k]
        e["ark"] = ""
        e["links"] = [{"label": f"DECODE R{i}", "href": REC + str(i)} for i in ids[:6]]
        if len(ids) > 6:
            e["links"].append({"label": f"+{len(ids) - 6} more records", "href": None})
        e["seen"] = "catalogue"
        e["source"] = "DECODE"
        e["decode_ids"] = ids
        if o.get("scored"):
            e["scored"] = o["scored"]
        if o.get("on_list"):
            e["on_list"] = o["on_list"]
        E.append(e)
        nid += 1
        added += 1
    print("added", added, "excluded lines", len(excl), "total entries", len(E))
    if not dry:
        json.dump(cat, open(cat_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(excl, open(os.path.join(HERE, "excluded.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
