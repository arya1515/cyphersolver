"""Read R1026/R1027 with key R1024, choosing the digit behind each DECODE 'J+' sign.

The DECODE transcriber used 'J+' as a catch-all for a sign 'not represented by other
signs'. The R1028 control (no J+) reads cleanly with R1024, so the key is right and the
J+ sign hides different digits. Each J+ is tried as 0-9; a beam search with a French
character n-gram model (18th-c. diplomatic French, hellen1752/corpus_fr.txt) picks the
reading. Output: resolved_R<n>.txt (groups) and reading_R<n>.txt (text).
"""

from collections import defaultdict
from itertools import product
from pathlib import Path
import math
import re
import sys
import unicodedata

ROOT = Path(__file__).parent
N = 6


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z' ]", " ", s)
    return re.sub(r" +", " ", s)


def build_lm():
    text = norm((ROOT.parent / "hellen1752" / "corpus_fr.txt").read_text(encoding="utf-8", errors="replace"))
    text = text[:6_000_000]
    counts = [defaultdict(int) for _ in range(N + 1)]
    for n in range(1, N + 1):
        c = counts[n]
        for i in range(len(text) - n + 1):
            c[text[i:i + n]] += 1
    return counts


def lp(counts, ctx, ch):
    # stupid backoff
    pen = 0.0
    for k in range(min(N - 1, len(ctx)), -1, -1):
        h = ctx[len(ctx) - k:] if k else ""
        num = counts[k + 1].get(h + ch, 0)
        den = counts[k].get(h, 0) if k else sum(counts[1].values())
        if num:
            return pen + math.log(num / den)
        pen += math.log(0.4)
    return pen + math.log(1e-6)


def score(counts, ctx, word):
    s, c = 0.0, ctx
    for ch in norm(" " + word):
        s += lp(counts, c, ch)
        c = (c + ch)[-(N - 1):]
    return s, c


def load_key():
    key = {}
    for line in (ROOT / "decode" / "DOC_R1024_D2881_2881.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^\s*(\d+)\s+-\s+(.*?)\s*$", line)
        if m:
            key[int(m.group(1))] = m.group(2)
    return key


def groups(doc):
    """Return list of items: ('g', pattern) with J for the unknown sign, or ('c', clear)."""
    items = []
    for line in (ROOT / "decode" / doc).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#"):
            continue
        pos = 0
        for m in re.finditer(r"<(?:CLEAR|PLAIN)TEXT\s+[A-Z?]+\s+(.*?)>", line):
            items += parse(line[pos:m.start()])
            items.append(("c", m.group(1)))
            pos = m.end()
        items += parse(line[pos:])
    return items


def parse(chunk):
    out = []
    chunk = re.sub(r"\{.*?\}|\^\S*", "", chunk).replace("J+", "J").replace("J?", "J")
    for part in chunk.split("."):
        p = re.sub(r"[^0-9J?/]", "", part)
        if "/" in p:
            p = p.split("/")[0]
        if p and re.search(r"[0-9J]", p):
            out.append(("g", p))
    return out


def candidates(pat, key):
    if "?" in pat:
        pat = pat.replace("?", "J")
    k = pat.count("J")
    if k == 0:
        v = int(pat)
        return [(pat, key.get(v, f"[{pat}]"))]
    cands = []
    for digits in product("0123456789", repeat=k):
        it = iter(digits)
        s = "".join(next(it) if ch == "J" else ch for ch in pat)
        v = int(s)
        if v in key:
            cands.append((s, key[v]))
    return cands or [(pat, f"[{pat}]")]


def solve(doc, counts, key, beam=40):
    items = groups(doc)
    beams = [(0.0, " ", [])]
    for kind, val in items:
        if kind == "c":
            beams = [(s, " ", out + [("c", val)]) for s, c, out in beams]
            continue
        new = []
        for s, c, out in beams:
            for num, word in candidates(val, key):
                w = word if not word.startswith("[") else ""
                d, c2 = score(counts, c, w) if w else (-8.0, c)
                new.append((s + d, c2, out + [("g", val, num, word)]))
        new.sort(key=lambda x: -x[0])
        beams = new[:beam]
    return beams[0][2]


def main():
    counts = build_lm()
    key = load_key()
    for rec, doc in [(1026, "DOC_R1026_D1852_1852.txt"), (1027, "DOC_R1027_D2299_2299.txt")]:
        out = solve(doc, counts, key)
        text, grp = [], []
        for item in out:
            if item[0] == "c":
                text.append(f"\n[clear: {item[1]}]\n")
            else:
                _, pat, num, word = item
                grp.append(f"{pat}={num}" if "J" in pat or "?" in pat else num)
                text.append(word if "J" not in pat else f"{word}")
        (ROOT / f"resolved_R{rec}.txt").write_text(" ".join(grp) + "\n", encoding="utf-8")
        (ROOT / f"reading_R{rec}.txt").write_text(" ".join(text) + "\n", encoding="utf-8")
        print(f"R{rec}: {sum(1 for i in out if i[0]=='g')} groups")


if __name__ == "__main__":
    main()
