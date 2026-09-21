import re
import csv
import textwrap
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KEY_TXT = ROOT / "R1038_key_transcription.txt"

# Entries that the R1038 transcriber left illegible but which are determined by
# repeated grammatical contexts in R1036. Brackets flag editorial expansion or
# an inflection that varies with context.
R1036_INFERRED = {
    "7": "te",
    "25^_": "ie",
    "27^_": "ig",
    "57": "volgen",
    "77": "een",
    "104^_": "ig",
    "114^_": "ing[en]",
    "118^^": "missive",
    "236^_": "zich",
    "242^_": "van",
    "311^_": "land",
    "340^_": "mar",
    "370^_": "oorlogend",
    "404^_": "lijk",
    "445^_": "Keizer",
    "462^\"": "acte",
    "521^_": "Keizerin",
    "673^\"": "propositie",
    "689^\"": "conven",
    "715": "beid",
    "737^o": "bewuste",
    "810": "Groot",
    "833^^": "[ge]sloten",
    "881": "nje",
    "924": "het",
    "952^_": "onder",
    # second pass (2026-09-21), each value fits every occurrence in R1036
    "2": "een",
    "3^o": "stel",
    "39": "hun",
    "176^^": "mpli",
    "363^o": "tusschen",
    "410^_": "zij",
    "681^_": "mogendheden",
    "724": "welgeval",
    "741": "haar",
}


def load_key(path=KEY_TXT):
    key = {}
    conflicts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*([^#<].*?)\s+-\s+(.*?)\s*$", line)
        if not match:
            continue
        left, value = match.groups()
        if not re.fullmatch(r"[0-9A-Za-z^\"_|?]+", left.replace("CircleWithHorizontalBar", "")):
            continue
        for code in left.split("|"):
            code = code.strip()
            if not re.fullmatch(r"\d+(?:\^\"|\^_|\^\^|\^o|\^CircleWithHorizontalBar)?", code):
                continue
            if code in key and key[code] != value:
                conflicts.setdefault(code, {key[code]}).add(value)
                if key[code] in {"<IL>", "<EMPTY>", "<EMMPTY>"} and value not in {"<IL>", "<EMPTY>", "<EMMPTY>"}:
                    key[code] = value
            else:
                key[code] = value
    return key, conflicts


def normalize_group(raw):
    digits = "".join(re.findall(r"\d", raw))
    if not digits:
        return None
    if "^+" in raw:
        suffix = "^CircleWithHorizontalBar"
    elif "^{''}" in raw or "^''" in raw or '^"' in raw:
        suffix = '^"'
    elif "^o" in raw:
        suffix = "^o"
    elif "^^" in raw:
        suffix = "^^"
    elif "^_" in raw:
        suffix = "^_"
    else:
        suffix = ""
    return digits + suffix


def tokenize_transcript(path):
    text = path.read_text(encoding="utf-8")
    body = text.split("> (", 1)[1]
    body = re.sub(r"<CLEARTEXT[^\n]*", "", body)
    body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)
    # In this manual transcript, each visual line ends at a group boundary even
    # when the final comma was omitted.
    body = body.replace("\r", "").replace("\n", ",")
    tokens = []
    for raw in body.split(","):
        token = normalize_group(raw)
        if token:
            tokens.append((token, raw.strip()))
    return tokens


def tokenize_pages(path):
    text = path.read_text(encoding="utf-8")
    pages = {}
    for block in re.split(r"(?m)^#IMAGE NAME:\s*", text)[2:]:
        lines = block.splitlines()
        page = lines[0].strip()
        body = "\n".join(lines[1:])
        if "> (" in body:
            body = body.split("> (", 1)[1]
        body = re.sub(r"<CLEARTEXT[^\n]*", "", body)
        body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)
        body = body.replace("\r", "").replace("\n", ",")
        pages[page] = [(token, raw.strip()) for raw in body.split(",")
                       if (token := normalize_group(raw))]
    return pages


def consensus(left, right, key):
    """Merge two independent transcriptions of the same ciphertext page."""
    a = [token for token, _ in left]
    b = [token for token, _ in right]
    merged = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            merged.extend(left[i1:i2])
        elif tag == "replace" and i2 - i1 == j2 - j1:
            for lrow, rrow in zip(left[i1:i2], right[j1:j2]):
                lknown = key.get(lrow[0]) not in {None, "<IL>", "<EMPTY>", "<EMMPTY>"}
                rknown = key.get(rrow[0]) not in {None, "<IL>", "<EMPTY>", "<EMMPTY>"}
                merged.append(rrow if rknown and not lknown else lrow)
        else:
            lseg, rseg = left[i1:i2], right[j1:j2]
            def score(seg):
                return sum(key.get(t) not in {None, "<IL>", "<EMPTY>", "<EMMPTY>"}
                           for t, _ in seg) - abs(len(seg) - max(len(lseg), len(rseg)))
            merged.extend(rseg if score(rseg) > score(lseg) else lseg)
    return merged


def canonical_r1036(path, key):
    pages = tokenize_pages(path)
    rows = []
    for page in ("5415.png", "5416.png", "5417.png", "5418.png"):
        rows.extend(pages[page])
    rows.extend(consensus(pages["5419.png"], pages["5421.png"], key))
    rows.extend(consensus(pages["5420.png"], pages["5422.png"], key))
    rows.extend(pages["5423.png"])
    return [(token, raw, (value if value not in {None, "<IL>", "<EMPTY>", "<EMMPTY>"} else None))
            for token, raw in rows for value in [key.get(token)]]


def decode_file(path, key):
    tokens = tokenize_transcript(path)
    rows = []
    for token, raw in tokens:
        value = key.get(token)
        known = value is not None and value not in {"<IL>", "<EMPTY>", "<EMMPTY>"}
        rows.append((token, raw, value if known else None))
    return rows


def main():
    key, conflicts = load_key()
    key.update(R1036_INFERRED)
    with (ROOT / "R1038_key_parsed.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["code", "plaintext", "status"])
        for code in sorted(key, key=lambda c: (int(re.match(r"\d+", c).group()), c)):
            writer.writerow([code, key[code], "contextual inference" if code in R1036_INFERRED else "R1038 transcription"])
    rows = canonical_r1036(ROOT / "R1036_transcription.txt", key)
    hits = sum(value is not None for _, _, value in rows)
    print(f"key_entries={len(key)} conflicts={len(conflicts)}")
    print(f"tokens={len(rows)} decoded={hits} ({hits / len(rows):.1%})")
    rendered = [value if value is not None else f"[{token}]" for token, _, value in rows]
    (ROOT / "R1036_machine_decipherment.txt").write_text(
        textwrap.fill(" ".join(rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    with (ROOT / "R1036_tokens.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["index", "code", "transcribed_group", "plaintext"])
        for index, (token, raw, value) in enumerate(rows, 1):
            writer.writerow([index, token, raw, value or ""])
    unknowns = Counter(token for token, _, value in rows if value is None)
    (ROOT / "R1036_unknowns.txt").write_text(
        "\n".join(f"{count:4d} {token}" for token, count in unknowns.most_common()) + "\n",
        encoding="utf-8",
    )

    r1040_pages = tokenize_pages(ROOT / "R1040_transcription.txt")
    page_stats = []
    r1040_rows = []
    for page, page_rows in r1040_pages.items():
        decoded_page = [(token, raw, (value if value not in {None, "<IL>", "<EMPTY>", "<EMMPTY>"} else None))
                        for token, raw in page_rows for value in [key.get(token)]]
        hits_page = sum(value is not None for _, _, value in decoded_page)
        page_stats.append((page, len(decoded_page), hits_page))
        page_number = int(page.split(".")[0])
        # R1040 changes nomenclators part-way through image 5459.  The first
        # 179 groups belong to the Rechteren-family key; group 180 ("dit
        # alles") is the first group encoded with De Swart's 1765 key.
        if page_number == 5459:
            r1040_rows.extend(decoded_page[179:])
        elif page_number > 5459:
            r1040_rows.extend(decoded_page)
    r1040_rendered = [value if value is not None else f"[{token}]" for token, _, value in r1040_rows]
    (ROOT / "R1040_second_key_machine_decipherment.txt").write_text(
        textwrap.fill(" ".join(r1040_rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    with (ROOT / "R1040_second_key_tokens.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["index", "code", "transcribed_group", "plaintext"])
        for index, (token, raw, value) in enumerate(r1040_rows, 1):
            writer.writerow([index, token, raw, value or ""])
    (ROOT / "R1040_1765_page_stats.tsv").write_text(
        "page\ttokens\tdecoded\trate\n" + "\n".join(
            f"{page}\t{total}\t{hits}\t{(hits / total if total else 0):.3%}" for page, total, hits in page_stats
        ) + "\n", encoding="utf-8"
    )
    for start in range(0, len(rendered), 30):
        print(" ".join(rendered[start:start + 30]))


if __name__ == "__main__":
    main()
