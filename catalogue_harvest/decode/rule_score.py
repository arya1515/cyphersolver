"""First-pass, rule-based scoring of the DECODE groups (batch_*.json) into out_<N>.jsonl for merge.py.

Used when the per-batch review agents could not run. Every entry says in score_note that it was scored by rule
from DECODE metadata and not reviewed; entries reviewed by hand later replace their line.
Signals: DECODE status; a key record cited in the notes or in the same archive series; a decipherment on the
leaf; an edition cited; page count; cipher type; who wrote to whom.
"""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

REGION_BY_CITY = {
    "London": "England", "Kew": "England", "Madrid": "Spain", "Simancas": "Spain", "Valladolid": "Spain",
    "Barcelona": "Spain", "Vatican City": "Papacy", "Paris": "France", "The Hague": "Low Countries",
    "Brussels": "Low Countries", "Naples": "Italy", "Modena": "Italy", "Milano": "Italy", "Mantova": "Italy",
    "Venice": "Italy", "Florence": "Italy", "München": "Germany", "Dresden": "Germany", "Marburg": "Germany",
    "Berlin": "Germany", "Budapest": "Hungary", "Stockholm": "Scandinavia", "Uppsala": "Scandinavia",
    "Umeå": "Scandinavia", "Vienna": "Austria", "Klášter (by Nepomuk)": "Bohemia", "Zürich": "Switzerland",
    "Strassburg": "Germany", "New Haven": "Other",
}
SHORT = [("British Library", "BL"), ("The National Archives", "TNA"), ("Vatican Secret Archive", "ASV"),
         ("Bibliotheca Apostolica Vaticana", "BAV"), ("Biblioteca de la Real Academia de la Historia", "RAH"),
         ("Bibliotheque nationale de France (BnF)", "BnF"), ("Bibliothèque nationale de France (BnF)", "BnF"),
         ("Bibliothèque nationale de France", "BnF"), ("Archivo General de Simancas", "AGS"),
         ("State Archives of Modena", "ASMo"), ("Archivio di Stato di Napoli", "ASNa"),
         ("Algemeen Rijksarchief", "ARA Brussels"), ("Koninklijk Huisarchief (KHA)", "KHA The Hague"),
         ("Nationaal Archief", "NA The Hague"), ("Bavaria Main State Archive", "BayHStA"),
         ("National Archives of Hungary", "MNL OL"), ("Österreichisches Staatsarchiv", "ÖStA"),
         ("Riksarkivet", "Riksarkivet"), ("State Archives of Milano", "ASMi"), ("State Archives of Venice", "ASVe"),
         ("Státní oblastní archiv v Plzni", "SOA Plzeň")]
LANG_REGION = {"French": "France", "Spanish": "Spain", "Italian": "Italy", "English": "England", "German": "Germany",
               "Dutch": "Low Countries", "Swedish": "Scandinavia", "Hungarian": "Hungary", "Latin": None,
               "Portuguese": "Portugal", "Czech": "Bohemia", "Polish": "Poland"}
PRINCIPAL = re.compile(r"(?i)\b(king|queen|emperor|empress|pope|cardinal|duke|duchess|prince|princess|elector|"
                       r"viceroy|regent|archduke|landgrave|stadholder|nuncio|ambassador|envoy|secretary of state|"
                       r"philip|charles|henri|henry|elizabeth|mary|ferdinand|louis|william|maximilian|rudolf|"
                       r"leopold|gustav|christina|oxenstierna|richelieu|mazarin|granvelle|orange|farnese|borromeo|"
                       r"medici|este|sforza|gonzaga|habsburg|stuart|cecil|walsingham|throckmorton|olivares|lerma)\b")
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def short(h):
    h = re.sub(r"\s+", " ", h or "").strip(" .,")
    for a, b in SHORT:
        h = h.replace(a, b)
    return h[:140]


def fmt_date(d):
    m = re.match(r"(\d{3,4})(?:-(\d\d))?(?:-(\d\d))?", d or "")
    if not m:
        return None, "undated"
    y, mo, dd = m.groups()
    s = y
    if mo and 1 <= int(mo) <= 12:
        s = f"{MON[int(mo) - 1]} {y}"
        if dd and int(dd):
            s = f"{int(dd)} {s}"
    return int(y), s


def period(y):
    if y is None:
        return "unknown"
    for lo, hi, p in [(0, 1496, "before 1497"), (1497, 1559, "1497-1559"), (1560, 1588, "1560-1589"),
                      (1589, 1597, "1589-1598"), (1598, 1610, "1598-1610"), (1611, 1650, "1611-1650"),
                      (1651, 1700, "1651-1700"), (1701, 1800, "1701-1800"), (1801, 1900, "1801-1900")]:
        if lo <= y <= hi:
            return p
    return "unknown"


DISPLAY = [("Thorkmorton", "Throckmorton"), ("Cecill", "Cecil"), ("Vespanian", "Vespasian"), ("ambassor", "ambassador"),
           ("unkwown", "unknown"), ("Constantinopel", "Constantinople")]


def ent(s):
    s = re.sub(r"&[lr]squot;|&[lr]squo;", "'", s or "").replace("&amp;", "&")
    for x, y in DISPLAY:
        s = s.replace(x, y)
    return s


def clean(s):
    s = ent(s or "").strip()
    return "" if s.lower() in ("", "none", "unknown", "?", "n/a", "-") else s


def score(g):
    rs = g["records"]
    info = " ".join(r["info"] for r in rs)
    li = info.lower()
    author = clean(g["key"][2]) or clean(rs[0]["sender"])
    recv = clean(g["key"][3])
    authors = {clean(r["author"]) for r in rs if clean(r["author"])}
    if len(authors) > 1:            # a merged series: name the sender once, without co-signers or descriptors
        author = min(authors, key=len).split(",")[0].rstrip("? ")
    recvs = []
    for r in rs:
        x = clean(r["receiver"]).split(",")[0].rstrip("? ")
        if x and x not in recvs:
            recvs.append(x)
    if len(recvs) > 1:
        recv = " / ".join(recvs[:3]) + (" and others" if len(recvs) > 3 else "")
    origin = next((r["origin"] for r in rs if r["origin"]), "")
    city = g["key"][0]
    dates = [fmt_date(r["date"]) for r in sorted(rs, key=lambda r: r["date"] or "9999") if fmt_date(r["date"])[0]]
    years = [d[0] for d in dates]
    y = years[0] if years else None
    if not dates:
        date_s = "undated"
    elif len(rs) == 1 or years[0] == years[-1] and len(dates) == 1:
        date_s = dates[0][1]
    else:
        date_s = f"{dates[0][1]} – {dates[-1][1]}" if dates[0][1] != dates[-1][1] else dates[0][1]
    pages = sum(int(r["pages"]) for r in rs if (r["pages"] or "").isdigit())
    partial = any(r["status"] == "Partially decrypted" for r in rs)
    types = ", ".join(sorted({t for r in rs for t in r["cipher_types"].split(", ") if t})) or "type not given"
    syms = ", ".join(sorted({t for r in rs for t in r["symbols"].split(", ") if t})) or "symbols not given"
    access = "public" if all(r["access"] == "public" for r in rs) else "login"
    plain = next((r["plain"] for r in rs if r["plain"]), "") or next((r["clear"] for r in rs if r["clear"]), "")
    plain = plain.replace("?", "").strip()
    lang = plain or "unknown"

    cited_key = bool(re.search(r"for the key to the cipher see|key attached|contains a key|reconstructed key|"
                               r"including the key to this cipher|the key was reconstructed", li))
    on_leaf = bool(re.search(r"deciphered within the letter|decipherments within the letter|solution is written in "
                             r"the margin|deciphered in (the )?original|solution of the codematerial is written|with cipher and decryption|interlinear decipherment|"
                             r"possibly already deciphered", li))
    printed = bool(re.search(r"\bprinted in\b|deciphered is printed|\bed\. |article published", li))
    series_keys = g.get("decode_keys_total", 0)
    near_key = any(k["year"] and years and abs(k["year"] - y) <= 10 for k in g.get("decode_keys", []))

    key_record = bool(re.search(r"for the key to the cipher see", li))
    residue = bool(re.search(r"could not read them with the reconstructed key|some (passages|symbols) are not deciphered", li))
    # class and solvability
    if key_record:
        cls, solv, diff = "A", 5, 1
    elif cited_key or on_leaf:
        cls, solv, diff = "A", 4, 2
    elif near_key:
        cls, solv, diff = "A", 4, 3
    elif series_keys or partial:
        cls, solv, diff = "B", 3, 3
    else:
        cls, solv, diff = "C", 2, 4
    if partial and cls != "A":
        solv = max(solv, 3)
    if cls == "C" and pages >= 6:
        solv = 3                      # enough text for statistics
    if pages <= 1 and cls == "C":
        solv = max(1, solv - 1)
    if "nomenclator" in types and cls != "A":
        diff = min(5, diff + (1 if cls == "C" else 0))
    if types in ("simple substitution", "homophonic") and cls == "C":
        diff = 3
    if "polyphonic" in types:
        diff = max(diff, 3)
    if not lang or lang == "unknown":
        solv = max(1, solv - 1)

    # importance
    who = f"{author} {recv}"
    imp = 2
    if author and recv:
        imp = 3 if PRINCIPAL.search(who) else 2
    elif author or recv:
        imp = 2
    else:
        imp = 1 if not y else 2
    if len(rs) >= 5 and imp >= 2:
        imp = min(4, imp + 1)       # a whole despatch series
    if y and y < 1500 and imp < 4:
        imp += 1                     # early ciphers are scarce

    if residue:
        imp = max(1, imp - 1)        # mostly read already with the reconstructed key; only a residue is open
    counted = bool(author or recv) and bool(y)
    if on_leaf:
        counted = False              # read at the time; a transcription job, not a cipher problem

    ids = g["ids"]
    rec = f"DECODE R{ids[0]}" if len(ids) == 1 else f"DECODE R{ids[0]}–R{ids[-1]} ({len(ids)} records)"
    st = "Partially decrypted" if partial else "Non-decrypted"
    status = (f"{rec}: {st}, {pages or '?'} pp., {types}; {syms}; images {access}. "
              f"Not viewed here. ")
    notes = []
    if cited_key:
        notes.append("DECODE's notes point to a key or a reconstructed key")
    if on_leaf:
        notes.append("DECODE's notes say there is a contemporary decipherment on the leaf")
    if printed:
        notes.append("DECODE cites a printed text or article: check whether it already reads the cipher")
    if series_keys and not cited_key:
        notes.append(f"{series_keys} key record(s) from the same series on DECODE" +
                     (f", nearest R{g['decode_keys'][0]['id']} ({g['decode_keys'][0]['year']})" if g['decode_keys'] else ""))
    if on_leaf:
        notes.append("so the text was read at the time and this is a transcription job, listed as noted rather than open")
    if residue:
        notes.append("the uploader read it with a reconstructed key except some passages, so only a residue is open")
    if key_record:
        notes.append("the key itself is a DECODE record, so a reading should be direct")
    if notes:
        status += "; ".join(notes) + ". "
    hold = " ".join(r["holder"] for r in rs)
    special = ""
    if city == "Vatican City" and "Segretario di Stato" in hold:
        status += ("Nunciature ciphers were normally deciphered on arrival, and the decifrati are often filed in the same "
                   "busta or printed in the Nunziature series: look for them before attacking. ")
        special = "Look for the decifrati in the same busta and in the printed Nunziature volumes, then view the images."
    if re.search(r"Add MS 32(2[5-9]\d|30\d)", hold) or re.search(r"State Papers.*106|SP ?106", hold):
        status += ("Deciphering Branch / SP 106 material: such intercepts were usually deciphered at the time, so DECODE's "
                   "status may only mean no decipherment was uploaded. ")
        special = "Search the same volume and the Calendars for the contemporary decipherment first."
    snippet = next((r["info"] for r in rs if r["info"]), "")
    if snippet:
        status += "DECODE note: " + snippet[:260] + ("…" if len(snippet) > 260 else "")

    shelf = short(rs[0]["holder"]) if len(rs) == 1 else short(g["key"][1]) + f" ({len(rs)} items)"
    region = REGION_BY_CITY.get(city) or LANG_REGION.get(lang.split(",")[0].strip()) or "Other"
    if city in ("London", "Kew") and lang and lang not in ("English", "unknown"):
        region = LANG_REGION.get(lang.split(",")[0].strip()) or region
    a = author or "Unknown sender"
    r_ = recv or "unknown recipient"
    place = " → ".join(x for x in (origin, "") if x) if origin else ""
    title = f"{a}{f' ({origin.split(',')[0]})' if origin else ''} to {r_}"
    if len(rs) > 1:
        title += f", {len(rs)} ciphertexts"
    why = (f"Ciphered {('despatches' if len(rs) > 1 else 'letter')} of {a} to {r_}"
           f"{f', {date_s}' if y else ''}; what the cipher hides is not known.")
    if on_leaf:
        verify = "Open the images and check how much of the cipher the contemporary decipherment covers."
    elif cited_key or near_key:
        verify = "Fetch the images and the key record(s); test the key on the first lines."
    elif printed:
        verify = "Read the cited publication first: it may already give the reading."
    else:
        verify = (f"Search {'CSP / the Calendars' if region == 'England' else 'the printed correspondence and Tomokiyo'}"
                  " for a decipherment; then view the images (DECODE login) and transcribe.")
    if special:
        verify = special + " " + verify
    return {
        "type": "entry", "decode_ids": ids, "counted": counted, "year": y, "date": date_s, "title": title,
        "correspondents": f"{a} → {r_}", "place": place or city, "language": lang, "region": region,
        "period": period(y), "shelfmark": shelf, "folio_note": "", "cls": cls, "status": status.strip(),
        "why": why, "importance": imp, "solvability": solv, "difficulty": diff,
        "score_note": "Scored by rule from DECODE metadata (class from key signals, solvability from key, length and "
                      "language, importance from the correspondents); not yet reviewed by hand.",
        "verify": verify, "on_list": "", "scored": "rule",
    }


ROOT = os.path.dirname(os.path.dirname(HERE))
_CORPUS = None


def corpus():
    """Repo text that records existing targets: every NOTES.md, the trackers, the catalogue, Tomokiyo's list."""
    global _CORPUS
    if _CORPUS is None:
        parts = {}
        for p in glob.glob(os.path.join(ROOT, "*", "NOTES.md")) + glob.glob(os.path.join(ROOT, "*", "CANDIDATES.md")) + [
                os.path.join(ROOT, f) for f in ("TARGETS.md", "CATALOGUE.md", "catalogue.json", "SOLVED_CATALOGUE.md")]:
            if os.path.exists(p):
                parts[os.path.relpath(p, ROOT)] = open(p, encoding="utf-8", errors="ignore").read()
        tom = os.path.join(ROOT, "unsolved.htm")
        parts["unsolved.htm"] = re.sub(r"<[^>]+>", " ", open(tom, encoding="utf-8", errors="ignore").read()) if os.path.exists(tom) else ""
        _CORPUS = parts
    return _CORPUS


def shelf_patterns(h):
    pats = []
    m = re.search(r"Fran[çc]ais\s*(\d{3,5})", h)
    if m:
        pats.append(r"(?:fr\.|Français|français)\s*" + m.group(1) + r"\b")
    m = re.search(r"Add(?:itional)?\.? MS\.?\s*(\d{4,5})", h)
    if m:
        pats.append(r"Add(?:itional)?\.? MSS?\.?\s*" + m.group(1) + r"\b")
    m = re.search(r"(Cotton MS \w+ \w+ \w+|Harley MS \d+|Sloane MS \d+|SP ?\d+/\d+)", h)
    if m:
        pats.append(re.escape(m.group(1)))
    m = re.search(r"Sf\. (?:Ung\. )?b?\.? ?(\d{3})", h)
    if m:
        pats.append(r"(?:Sf|Sforzesco)[^\n]{0,40}" + m.group(1))
    m = re.search(r"Ambasciatori[^,]*b\. ?(\d/\d+)", h)
    if m:
        pats.append(r"Ambasciatori[^\n]{0,30}" + re.escape(m.group(1)))
    m = re.search(r"Signatura (\d/\d+)", h)
    if m:
        pats.append(r"\b" + re.escape(m.group(1)) + r"\b")
    m = re.search(r"leg\. ?(\d{2,5})", h)
    if m and "Simancas" in h or m and "AGS" in h:
        pats.append(r"leg\.? ?" + m.group(1) + r"\b")
    return pats


def overlap(e, g):
    """Flag entries whose shelfmark already appears in repo notes, or whose sender is on Tomokiyo's list."""
    hits = []
    for r in g["records"][:3]:
        for pat in shelf_patterns(r["holder"]):
            for name, text in corpus().items():
                if name != "unsolved.htm" and re.search(pat, text):
                    hits.append(name)
    out = {}
    if hits:
        out["repo_overlap"] = sorted(set(hits))
    author = e["correspondents"].split("→")[0]
    toks = [t for t in re.findall(r"[A-ZÀ-Ý][a-zà-ÿ]{5,}", author)
            if t not in ("Unknown", "Secretariat", "Cardinal", "Spanish", "French", "English", "Emperor", "Marques",
                         "Nicolo", "Charles", "Philip", "Henry", "Louis", "Ferdinand", "Maximilian", "William")]
    tom = corpus()["unsolved.htm"]
    for t in toks:
        for m in re.finditer(re.escape(t), tom):
            ctx = tom[max(0, m.start() - 120): m.end() + 120]
            if e["year"] and re.search(r"\b1[4-9]\d\d\b", ctx) and any(abs(int(y) - e["year"]) <= 3 for y in re.findall(r"\b(1[4-9]\d\d)\b", ctx)):
                out["tomokiyo_hint"] = re.sub(r"\s+", " ", ctx)[:240]
                break
        if "tomokiyo_hint" in out:
            break
    return out


OVERRIDES = json.load(open(os.path.join(HERE, "overrides.json"), encoding="utf-8"))


def apply_overrides(e):
    """Hand decisions (overrides.json): exclude an entry, or add a note, a list tag and score changes."""
    ids = set(e["decode_ids"])
    for ov in OVERRIDES:
        if not ids & set(ov["ids"]):
            continue
        if ov["action"] == "exclude":
            return {"type": "exclude", "decode_ids": e["decode_ids"], "reason": ov["reason"], "title": e["title"]}
        e["status"] = e["status"].rstrip() + " " + ov["note"]
        e.update(ov.get("patch", {}))
        if ov.get("on_list"):
            e["on_list"] = ov["on_list"]
        e["repo_overlap_checked"] = True
    return e


DATE_FIX = {985: "1677-08-03"}   # DECODE typo: the record name reads ..._1677Aug03, sent from Nijmegen
JUNK_ORIGIN = {"Western manuscripts", "unknown", "Unknown", "..."}
GENERIC = re.compile(r"(?i)^(the secretariat|unknown|unknown sender|[.]{3}|idem.*|unkwown.*|)$")


ALIAS = {"morosino": "morosini", "thorkmorton": "throckmorton"}


def norm_author(a):
    """Sender's name for merging: before the first comma, no dates or query marks, spelling variants folded."""
    a = re.sub(r"\(.*?\)|\?", "", ent(a or "")).split(",")[0].lower()
    a = re.sub(r"[^a-zà-ÿ]+", " ", a).strip()
    return " ".join(ALIAS.get(w, w) for w in a.split())


def prepare(G):
    """Fix known DECODE slips, then merge groups of one named sender within one archive series."""
    for g in G:
        for r in g["records"]:
            if r["id"] in DATE_FIX:
                r["date"] = DATE_FIX[r["id"]]
            if r["origin"] in JUNK_ORIGIN:
                r["origin"] = ""
            m = re.match(r"(\d{4})[^/]*/(\d{4})$", r["date"] or "")
            if m and int(m.group(2)) - int(m.group(1)) > 30:      # a volume's date span, not the letter's date
                r["info"] = f"DECODE's date {m.group(1)}/{m.group(2)} is the span of the volume. " + r["info"]
                r["date"] = ""
    merged, index = [], {}
    for g in G:
        a = g["key"][2]
        base = re.sub(r"(,\s*\d+[a-z]?)+(?=,|$)", "", g["key"][1])
        g["key"][1] = base
        k = (g["key"][0], base.split(",")[0].strip(), norm_author(a))   # one named sender within one archive
        if GENERIC.match(a or "") or not norm_author(a):
            merged.append(g)
            continue
        if k in index:
            h = index[k]
            h["records"] += g["records"]
            h["ids"] = sorted(h["ids"] + g["ids"])
            h["n"] += g["n"]
            if g["key"][3] and g["key"][3] not in h["key"][3].split(" / "):
                h["key"][3] = " / ".join(x for x in (h["key"][3], g["key"][3]) if x)
            seen = {x["id"] for x in h["decode_keys"]}
            h["decode_keys"] += [x for x in g["decode_keys"] if x["id"] not in seen]
            h["decode_keys_total"] = max(h["decode_keys_total"], g["decode_keys_total"])
        else:
            g = json.loads(json.dumps(g))
            index[k] = g
            merged.append(g)
    return merged


def main():
    for f in sorted(glob.glob(os.path.join(HERE, "batch_*.json"))):
        n = os.path.basename(f)[6:-5]
        G = prepare(json.load(open(f, encoding="utf-8")))
        with open(os.path.join(HERE, f"out_{n}.jsonl"), "w", encoding="utf-8") as o:
            for g in G:
                e = score(g)
                for k, v in e.items():
                    if isinstance(v, str):
                        e[k] = ent(v)
                e.update(overlap(e, g))
                e = apply_overrides(e)
                o.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(n, len(G))


if __name__ == "__main__":
    main()
