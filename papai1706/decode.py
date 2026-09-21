"""Decipher Pápai's letters with DECODE R580 ('Nemzetes Vitezlo Papai Janosnak adott Clavis', MNL OL G15 C 43/39).
Usage: python decode.py DOC_R823_*.txt  -> prints the reading, one line per transcription line.
Unknown numbers are printed as [n]; names in the nomenclator as {Name}."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
KEY = {}
for line in (ROOT/"DOC_R581_D2715_2715.txt").read_text(encoding="utf-8-sig").splitlines():
    m = re.match(r"^(\d+)(?:\|(\d+))?\s*-\s*(.+?)\s*$", line)
    if not m: continue
    v = m.group(3)
    for n in (m.group(1), m.group(2)):
        if n: KEY[int(n)] = v
KEY[304] = "n"  # R452 misprints 604; R580/R581 agree on 304
def show(n):
    v = KEY.get(n)
    if v is None: return f"[{n}]"
    if len(v) > 3 or v[0].isupper() and len(v) > 2 and v not in ("Ab","AB","Ök"): return "{" + v + "}"
    return v.lower()
def decode_line(s):
    s = re.sub(r"<[^>]*>", " | ", s)
    out = []
    for tok in re.split(r"\s{2,}|\|", s):
        t = tok.replace(" ", "").strip("—-–.,")
        if not t: continue
        if re.fullmatch(r"\d+", t): out.append(show(int(t)))
        elif re.fullmatch(r"[\d?/]+", t): out.append(f"[{t}]")
    return "".join(x if not x.startswith(("[","{")) else " "+x+" " for x in out)
def stats(text):
    nums = [int(t) for t in re.findall(r"(?<![\d?])((?:\d ?){1,4})(?![\d?])", "")]
if __name__ == "__main__":
    for f in sys.argv[1:]:
        tot = hit = 0
        print("=====", f)
        for line in Path(f).read_text(encoding="utf-8-sig", errors="replace").splitlines():
            if line.startswith("#") or ("<" in line and not re.search(r">\s*\d", line) and not re.search(r"\d\s*<", line)):
                if line.startswith("#IMAGE"): print(line)
                continue
            if re.search(r"<PLAINTEXT", line): continue
            r = decode_line(line)
            for tok in re.split(r"\s{2,}|\|", re.sub(r"<[^>]*>", "|", line)):
                t = tok.replace(" ", "").strip("—-–.,")
                if re.fullmatch(r"\d+", t):
                    tot += 1; hit += int(t) in KEY
            if r.strip(): print(r)
        print(f"-- groups {tot}, in key {hit} ({100*hit/max(tot,1):.1f}%)")
