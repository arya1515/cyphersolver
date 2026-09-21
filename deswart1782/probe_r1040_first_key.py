"""Probe R1040's first section against the surviving 1803 Croiset key.

The despatch's first nomenclator uses the same seven mark classes as that key,
but its manuscript notation differs.  This is a diagnostic comparison, not an
assertion that the 1803 key itself was used in 1787.
"""

import csv
import re
import textwrap
from pathlib import Path

from decode_1765 import tokenize_pages


ROOT = Path(__file__).resolve().parent
KEY_PATH = Path(r"C:\Users\dbour\Downloads\DOC_1035_2026-Jan-09-15-24-07_36531.csv")


def load_key():
    key = {}
    with KEY_PATH.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2:
                key[row[0].strip()] = row[1].strip()
    return key


def normalize_first_key(raw):
    digits = "".join(re.findall(r"\d", raw))
    if not digits:
        return None
    # Longest/most specific marks first. Braced forms occur in a few places.
    compact = raw.replace("{", "").replace("}", "").replace(" ", "")
    if "^__" in compact or compact.count("__") >= 1:
        suffix = "="
    elif "^''" in compact or '^"' in compact:
        suffix = '"'
    elif "^+" in compact:
        suffix = "+"
    elif "^o" in compact:
        suffix = ":"
    elif "^_" in compact:
        suffix = "~"
    elif "^'" in compact:
        suffix = "^"
    else:
        suffix = ""
    return digits + suffix


def first_section_rows():
    pages = tokenize_pages(ROOT / "R1040_transcription.txt")
    rows = []
    for page in [f"{n}.png" for n in range(5453, 5459)]:
        rows.extend((page, raw, normalize_first_key(raw)) for _, raw in pages[page])
    # The first key continues for 179 groups on image 5459. Group 180 is 'dit'.
    rows.extend(("5459.png", raw, normalize_first_key(raw))
                for _, raw in pages["5459.png"][:179])
    return rows


def main():
    key = load_key()
    rows = first_section_rows()
    decoded = [key.get(code) for _, _, code in rows]
    hits = sum(value is not None for value in decoded)
    print(f"tokens={len(rows)} direct_1803_matches={hits} ({hits / len(rows):.1%})")
    rendered = [value if value is not None else f"[{code}]" for (_, _, code), value in zip(rows, decoded)]
    (ROOT / "R1040_first_key_1803_probe.txt").write_text(
        textwrap.fill(" ".join(rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    with (ROOT / "R1040_first_key_1803_probe.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["index", "page", "code_1803_notation", "transcribed_group", "1803_value"])
        for i, ((page, raw, code), value) in enumerate(zip(rows, decoded), 1):
            writer.writerow([i, page, code, raw, value or ""])
    print(" ".join(rendered[:500]))


if __name__ == "__main__":
    main()
