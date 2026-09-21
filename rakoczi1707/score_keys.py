"""Identify which preserved Fasc. 44 table generated R852/R912."""

from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parent


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if ch.isascii() and ch.isalnum())


def levenshtein(a: str, b: str) -> int:
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def parse_key(path: Path) -> dict[str, str]:
    key = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        match = re.match(r"\s*([0-9| ]+)\s+-\s+(.*?)\s*$", line)
        if not match:
            continue
        value = "" if "NULL" in match.group(2).upper() else norm(match.group(2))
        for code in re.findall(r"\d+", match.group(1)):
            key[code] = value
    return key


def parse_blocks(path: Path):
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    blocks = []
    for i, line in enumerate(lines[:-1]):
        match = re.match(r"\s*<PLAINTEXT\s+FR\s+(.*?)>\s*$", line, re.I)
        if not match:
            continue
        codes = [re.sub(r"\D", "", group) for group in re.split(r"[.\-,]", lines[i + 1])]
        codes = [code for code in codes if code]
        blocks.append((norm(match.group(1)), codes))
    return blocks


blocks = parse_blocks(ROOT / "DOC_R852_D2171_2171.txt") + parse_blocks(ROOT / "DOC_R912_D2230_2230.txt")
for path in sorted(ROOT.glob("DOC_R6*.txt")):
    key = parse_key(path)
    decoded = []
    expected = []
    covered = total = 0
    for plain, codes in blocks:
        pieces = [key.get(code) for code in codes]
        total += len(codes)
        covered += sum(piece is not None for piece in pieces)
        if all(piece is not None for piece in pieces):
            decoded.append("".join(pieces))
            expected.append(plain)
    a = "".join(decoded)
    b = "".join(expected)
    distance = levenshtein(a, b) if a and b else 10**9
    similarity = 1 - distance / max(len(a), len(b), 1)
    print(f"{path.name}: entries={len(key)} coverage={covered}/{total} exact_blocks={len(decoded)} similarity={similarity:.3f}")
    if path.name.startswith(("DOC_R633", "DOC_R634", "DOC_R639", "DOC_R640", "DOC_R641")):
        anchors = ["64", "533", "259", "22", "144", "140", "491", "26", "133", "368", "254", "265", "360", "435", "99"]
        print("  anchors:", " | ".join(f"{code}={key.get(code, '?')}" for code in anchors))
