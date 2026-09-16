"""Compare the DECODE transcription of record 92 (or 91) with the MysteryTwister text of IA-2.

Usage:  python compare_transcripts.py [DOC_R92_D1633_1633.txt] [../ASV_i1025_SdS_Spain_IA-2.txt]

Reports, page by page: digit count, dotted-digit count, marked word breaks (spaces / separators), and an
alignment (difflib on the bare digit stream) listing every insertion, deletion and substitution, so the
"transcript lost the word division" question in NOTES.md gets a concrete answer.
"""
import collections
import difflib
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import parse5  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load_generic(path):
    """DECODE transcriptions use the same header/cleartext conventions as MysteryTwister (the challenge
    text was exported from DECODE), so parse5.load usually works. Fall back to a flat parse otherwise."""
    try:
        pages = parse5.load(pathlib.Path(path))
        if pages and sum(len(s) for _, s in pages):
            return pages
    except Exception:  # noqa: BLE001
        pass
    text = open(path, encoding="utf-8", errors="replace").read()
    body = re.sub(r"<CLEARTEXT[^>]*>", " ", text)
    return [("(whole file)", [("D", parse5.tokens(body))])]


def summarize(pages, label):
    print("== %s" % label)
    tot = 0
    for name, segs in pages:
        toks = [t for k, v in segs if k == "D" for t in v]
        dots = sum(1 for t in toks if "^" in t or "_" in t)
        unc = sum(1 for t in toks if "?" in t)
        print("  %-10s digits %5d  dotted %4d  uncertain %3d  cleartext segs %d"
              % (name, len(toks), dots, unc, sum(1 for k, _ in segs if k == "C")))
        tot += len(toks)
    print("  total digits %d" % tot)
    return tot


def raw_stream_with_spaces(path):
    """Digit stream keeping whitespace as word-break markers: returns list of ('d', digit+marks) / ('sp',)."""
    text = open(path, encoding="utf-8", errors="replace").read()
    text = re.sub(r"#.*", " ", text)
    text = re.sub(r"<CLEARTEXT[^>]*>", " | ", text, flags=re.S)
    out = []
    for m in re.finditer(r"(\d(?:\^[.,]?|_[.,]?|\?|<-|/|,)*)|(\s+)|(\|)", text):
        if m.group(1):
            out.append(("d", m.group(1)))
        elif m.group(3):
            out.append(("clear",))
        else:
            if out and out[-1][0] == "d":
                out.append(("sp",))
    return out


def main():
    dec = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "DOC_R92_D1633_1633.txt")
    mt = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "ASV_i1025_SdS_Spain_IA-2.txt")
    if not os.path.exists(dec):
        sys.exit("missing %s (download it first, see MANIFEST.md)" % dec)

    a = load_generic(mt)
    b = load_generic(dec)
    summarize(a, "MysteryTwister " + os.path.basename(mt))
    summarize(b, "DECODE " + os.path.basename(dec))

    sa = [t for _, segs in a for k, v in segs if k == "D" for t in v]
    sb = [t for _, segs in b for k, v in segs if k == "D" for t in v]
    da, db = [t[0] for t in sa], [t[0] for t in sb]
    sm = difflib.SequenceMatcher(None, da, db, autojunk=False)
    print("\n== bare-digit alignment (MT -> DECODE), ratio %.4f" % sm.ratio())
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n += 1
        print("  %-8s MT[%d:%d]=%s  DEC[%d:%d]=%s" % (tag, i1, i2, "".join(da[i1:i2]), j1, j2, "".join(db[j1:j2])))
    print("  %d differing regions" % n)

    # marks on aligned equal digits
    md = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            continue
        for k in range(i2 - i1):
            if sa[i1 + k] != sb[j1 + k]:
                md += 1
                if md <= 60:
                    print("  mark diff at MT#%d: %s vs %s" % (i1 + k, sa[i1 + k], sb[j1 + k]))
    print("  %d aligned digits with different marks" % md)

    # spacing: the MysteryTwister text spaces every digit and Lasry (e-mail, 16 Sep 2026) says the manuscript
    # has no visual separators between tokens, so a gap wider than one space is the only thing worth counting.
    for label, path in (("MT", mt), ("DECODE", dec)):
        text = open(path, encoding="utf-8", errors="replace").read()
        text = re.sub(r"#[^\n]*", " ", text)
        text = re.sub(r"<CLEARTEXT[^>]*>", " ", text, flags=re.S)
        gaps = collections.Counter(len(g) for g in re.findall(r"(?<=\d)[ \t]+(?=\d)", text))
        print("\n== %s gap widths between digits: %s" % (label, dict(sorted(gaps.items()))))


if __name__ == "__main__":
    main()
