"""Assemble the image-verified IA-2 transcript (decode/reread/*.txt, one file per page, written 2026-09-18
from the 400 dpi DECODE images) into ../IA-2_reread.txt in the MysteryTwister format, so parse5.load works.

Each reread file carries 'N: tokens' lines already corrected (transcriber dittographies removed, omitted
digits inserted, dots added or moved). Struck-through digits noted in the DIFF lines are removed here.
Cleartext is not re-transcribed; a placeholder <CLEARTEXT IT ...> marks where it interrupts the cipher.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["070r", "070v", "071r", "071v", "072r", "072v", "073r"]
# 072v: cipher lines 2-3 end run A, lines 18-23 start run B (4-17 cleartext); the reread numbers from the block
BREAK_AFTER = {("072v", 3)}
STRUCK = {("072v", 3): (32, 35)}  # 1-based digit positions cancelled in the MS


def lines_of(page):
    out = []
    for raw in open(os.path.join(HERE, "reread", page + ".txt"), encoding="utf-8"):
        m = re.match(r"^L?(\d+)(?: \([^)]*\))?:\s(.*)$", raw.rstrip("\n"))
        if not m:
            continue
        n, body = int(m.group(1)), m.group(2)
        body = re.split(r"\s{2,}<-|\s+#", body)[0]
        toks = body.split()
        if (page, n) in STRUCK:
            a, b = STRUCK[(page, n)]
            k, keep = 0, []
            for t in toks:
                if t[0].isdigit() or t[0] == "?":
                    k += 1
                    if a <= k <= b:
                        continue
                keep.append(t)
            toks = keep
        out.append((n, toks))
    return out


def main():
    res = [r"#CATALOG NAME: \Segr. Stato Spagna 1A\2\ (image-verified reread, 2026-09-18)", ""]
    for p in PAGES:
        res.append("#IMAGE NAME: %s.jpg" % p)
        if p == "070r":
            res.append("<CLEARTEXT IT (070r cleartext frame, not re-transcribed)>")
        for n, toks in lines_of(p):
            res.append(" ".join(toks))
            if (p, n) in BREAK_AFTER:
                res.append("<CLEARTEXT IT (072v cleartext: pasta delli intendetti / apparati Turcheschi)>")
        res.append("")
    res.append("#IMAGE NAME: 073v.jpg")
    res.append("<CLEARTEXT IT (073r-073v closing cleartext, Da Roma alli XV di Aprile 1542)>")
    open(os.path.join(HERE, "..", "IA-2_reread.txt"), "w", encoding="utf-8").write("\n".join(res) + "\n")


if __name__ == "__main__":
    main()
