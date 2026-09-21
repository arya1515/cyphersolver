"""Apply the matching Fasc. 44/08 codebook to R852, R912, and R902."""

from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parent


def plain_value(text: str) -> str:
    if "NULL" in text.upper():
        return ""
    return unicodedata.normalize("NFC", text.strip())


def load_key() -> dict[str, str]:
    key = {}
    path = ROOT / "DOC_R639_D2752_2752.txt"
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        match = re.match(r"\s*([0-9| ]+)\s+-\s+(.*?)\s*$", line)
        if not match:
            continue
        for code in re.findall(r"\d+", match.group(1)):
            key[code] = plain_value(match.group(2))
    return key


def parse_line(line: str, superscripts: bool = False) -> list[str]:
    if superscripts:
        # In this hand the leading hundreds/tens digit is raised. DECODE
        # renders that leading form as a stand-alone `1^.` before the rest
        # of the same number. Other carets merely annotate a digit and do
        # not consume the following separator.
        line = re.sub(r"1\^\s*\.", "1", line)
        line = re.sub(r"([0-9])\^", r"\1", line)
    key_codes = set(load_key())

    def split_run(digits: str) -> list[str]:
        if len(digits) <= 3:
            return [digits]
        candidates: list[list[str]] = []

        def visit(offset: int, pieces: list[str]) -> None:
            if offset == len(digits):
                candidates.append(pieces.copy())
                return
            for size in (3, 2):
                piece = digits[offset:offset + size]
                if len(piece) == size and piece in key_codes:
                    pieces.append(piece)
                    visit(offset + size, pieces)
                    pieces.pop()

        visit(0, [])
        return min(candidates, key=lambda parts: (len(parts), -sum(len(part) == 3 for part in parts))) if candidates else [digits]

    groups = []
    for raw in re.split(r"\.+|--+", line):
        digits = "".join(re.findall(r"\d", raw))
        if digits:
            groups.extend(split_run(digits))
    return groups


def decode_document(filename: str, superscripts: bool = False) -> tuple[str, list[str]]:
    key = load_key()
    source = (ROOT / filename).read_text(encoding="utf-8-sig", errors="replace").splitlines()
    output = []
    groups_all = []
    image = ""
    for line in source:
        if line.startswith("#IMAGE NAME"):
            image = line.split(":", 1)[-1].strip()
            output.append(f"\n## {image}\n")
            continue
        if not re.match(r"\s*[0-9Ggloiv]", line):
            continue
        groups = parse_line(line, superscripts=superscripts)
        if not groups:
            continue
        groups_all.extend(groups)
        pieces = []
        for group in groups:
            value = key.get(group)
            pieces.append(value if value is not None else f"[{group}]")
        output.append(" ".join(piece for piece in pieces if piece != ""))
    return "\n".join(output).strip() + "\n", groups_all


for filename, superscripts, output_name in (
    ("DOC_R852_D2171_2171.txt", False, "R852_key08_read.txt"),
    ("DOC_R912_D2230_2230.txt", False, "R912_key08_read.txt"),
    ("DOC_R902_D1951_1951.txt", True, "R902_key08_read.txt"),
):
    decoded, groups = decode_document(filename, superscripts)
    (ROOT / output_name).write_text(decoded, encoding="utf-8")
    known = sum(1 for group in groups if group in load_key())
    print(f"{output_name}: {known}/{len(groups)} groups in key")
