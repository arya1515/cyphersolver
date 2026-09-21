"""Decode the fresh image transcriptions in tr/ with the R639 table."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
key = {}
for line in (ROOT / "DOC_R639_D2752_2752.txt").read_text(encoding="utf-8-sig", errors="replace").splitlines():
    m = re.match(r"\s*([0-9| ]+)\s+-\s+(.*?)\s*$", line)
    if m:
        v = "" if "NULL" in m.group(2).upper() else m.group(2).strip()
        for c in re.findall(r"\d+", m.group(1)):
            key[c] = v
# Corrections read from the key image (IMG_R639_I3927): DECODE gives S 95 and T 96 for the
# overwritten 45 and 47; Z's line has "100/110?" (the image has 110). 173 and 174 are skipped by the
# table's numbering but are used as "de" in the letters (grade C).
key.update({"45": "S", "47": "T", "95": "es", "96": "Q", "54": "Z", "55": "Z", "110": "Z",
            "173": "de", "174": "de",
            "561": "nt", "562": "nt"})  # 561/562 outside the table; "poi-nt", "souve-nt" (grade C)
def decode(name):
    out, n, k = [], 0, 0
    for line in (ROOT / "tr" / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        words = []
        for g in line.replace("-", " ").split():
            d = re.sub(r"\D", "", g)
            if not d:
                words.append(g); continue
            n += 1
            if d in key:
                k += 1
                if key[d]: words.append(key[d] + ("?" if "?" in g else ""))
            else:
                words.append(f"[{d}]")
        out.append(" ".join(words))
    return "\n".join(out), n, k
if __name__ == "__main__":
    for name in sys.argv[1:]:
        text, n, k = decode(name)
        print(f"== {name}: {k}/{n}"); print(text)
