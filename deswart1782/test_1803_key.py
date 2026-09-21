import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = Path(r"C:\Users\dbour\Downloads\DOC_1035_2026-Jan-09-15-24-07_36531.csv")


def load_key():
    out = {}
    with KEY.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2:
                out[row[0].strip()] = row[1].strip()
    return out


def tokenise(text):
    # Remove metadata and cleartext markup, then split only likely cipher groups.
    body = text.split("> (", 1)[1]
    body = re.sub(r"#IMAGE NAME:.*", "", body)
    body = re.sub(r"#COMMENTS:.*", "", body)
    for raw in body.split(","):
        raw = raw.strip()
        digits = "".join(re.findall(r"\d", raw))
        if not digits:
            continue
        if "^{''}" in raw:
            mark = '"'
        elif "^+" in raw:
            mark = "+"
        elif "^o" in raw:
            mark = ":"
        elif "^^" in raw:
            mark = "^"
        elif "^_" in raw:
            mark = "~"
        else:
            mark = ""
        yield digits + mark, raw


def main():
    key = load_key()
    text = (ROOT / "R1036_transcription.txt").read_text(encoding="utf-8")
    toks = list(tokenise(text))
    decoded = [key.get(tok, f"[{tok}]") for tok, _ in toks]
    hits = sum(not x.startswith("[") for x in decoded)
    print(f"tokens={len(toks)} hits={hits} ({hits/len(toks):.1%})")
    for i in range(0, min(len(decoded), 600), 30):
        print(" ".join(decoded[i:i+30]))


if __name__ == "__main__":
    main()
