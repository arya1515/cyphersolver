import json
import pathlib
import re


ROOT = pathlib.Path(__file__).parent
KEY = json.loads((ROOT / "key1024" / "key.json").read_text(encoding="utf-8"))
TEXT = (ROOT / "ciphertext.txt").read_text(encoding="utf-8")

# Omit dates and prose inside the square-bracket annotations.
CIPHER_LINES = [line for line in TEXT.splitlines() if line and not line.startswith("#")]
CIPHER = "\n".join(CIPHER_LINES)
CIPHER = re.sub(r"\[.*?\]", " ", CIPHER)
CODES = [int(x) for x in re.findall(r"(?<![\^\d/])\d+", CIPHER)]

COMMON = {
    "de": 7, "la": 7, "le": 7, "les": 7, "des": 7, "du": 7, "un": 6,
    "une": 6, "et": 7, "que": 7, "qui": 7, "il": 7, "elle": 6, "ils": 6,
    "je": 7, "j'ai": 7, "nous": 7, "vous": 7, "on": 6, "en": 7, "dans": 6,
    "pour": 7, "par": 6, "avec": 6, "sans": 6, "sur": 6, "ce": 6, "cette": 6,
    "ces": 6, "son": 6, "sa": 6, "ses": 6, "au": 6, "aux": 6, "mais": 6,
    "plus": 6, "pas": 6, "ne": 6, "est": 7, "sont": 6, "a": 5, "à": 6,
    "avoir": 5, "être": 6, "faire": 6, "fait": 6, "tout": 6, "très": 5,
    "comme": 6, "même": 5, "encore": 5, "bien": 5, "dont": 5, "leur": 5,
    "me": 6, "se": 6, "lui": 5, "moi": 5, "mon": 5, "ma": 5,
    "ministre": 4, "roi": 4, "prince": 4, "réponse": 4, "reponse": 4,
    "partir": 4, "lettre": 4, "affaire": 4, "affaires": 4, "gouvernement": 4,
}


def norm(value: str) -> str:
    return re.sub(r"[^a-zàâçéèêëîïôûùüÿæœ']", "", value.lower())


def score_offset(offset: int):
    vals = []
    score = 0
    hits = 0
    for code in CODES:
        options = KEY.get(str(code + offset), [])
        value = options[0] if options else "?"
        vals.append(value)
        n = norm(value)
        if n in COMMON:
            score += COMMON[n]
            hits += 1
        if 1 <= len(n) <= 3 and n != "?":
            score += 0.25
    return score, hits, vals


ranked = []
for offset in range(-2500, 4001):
    score, hits, vals = score_offset(offset)
    ranked.append((score, hits, offset, vals))

for score, hits, offset, vals in sorted(ranked, reverse=True)[:40]:
    print(f"offset={offset:+5d} score={score:6.2f} hits={hits:2d}")
    print(" | ".join(vals[:50]))

