"""Test whether R2238 is a simple renumbering of Euler's R1024 key.

This is deliberately a negative-control attack: it tests historical-looking
renumberings (cyclic shifts, small affine maps, complements, and decimal digit
permutations) and ranks the resulting French with a character n-gram model.
It does not claim that a high-scoring fragment is a decipherment.
"""

from __future__ import annotations

import itertools
import json
import math
import re
import unicodedata
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KEY = json.loads((ROOT / "key1024" / "key.json").read_text(encoding="utf-8"))

CIPHER = """
1087,638,1193,1083,1531.18.536.503,537.788,2510,1114.137,719,648,639,537,
1154,251,1731,509.66.506,554.50,621,724,91,1202,56,153,702,709,93,729,
119,534.504.705,145,1216,173,1102.585.1204,624,1107,561,1227,1101,604,
281,148,532.1264.1241,638,624.286,534,1147,571,54.1014.764.69.91,
594,687,665,501.537.1183.116,1272,583,504.53.1012.583,231,213.585,
94,1257,
26.607.1012,534,111.26,1203.127,56,268,668,
503.595,41.1012,648,31,611,56,764,
1217,1628,233,561,271,94,1087,508.174,26.537.248,503.48.724,
94,1127,802.12,251,1203.137.18,664.578,1117,508.1115,141.18,659,788,173
"""

WORDS = [[int(n) for n in word.split(".")] for word in re.findall(r"\d+(?:\.\d+)*", CIPHER)]

CORPORA = (
    "https://www.gutenberg.org/ebooks/27807.txt.utf-8",  # 18th-c. memoirs
    "https://www.gutenberg.org/cache/epub/13629/pg13629.txt",  # correspondence
    "https://www.gutenberg.org/cache/epub/11176/pg11176.txt",  # Napoleonic memoirs
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z' ]+", " ", text)
    return re.sub(r"\s+", " ", text)


def train_ngrams(n: int = 4) -> tuple[Counter[str], int, float]:
    chunks = []
    for url in CORPORA:
        with urllib.request.urlopen(url, timeout=30) as response:
            chunks.append(response.read().decode("utf-8", errors="ignore"))
    text = "^^^" + normalize(" ".join(chunks)) + "$$$"
    counts = Counter(text[i : i + n] for i in range(len(text) - n + 1))
    floor = math.log(0.05 / sum(counts.values()))
    return counts, sum(counts.values()), floor


def key_value(number: int) -> str | None:
    values = KEY.get(str(number))
    if not values:
        return None
    value = values[0] if isinstance(values, list) else values
    if isinstance(value, dict):
        value = next(iter(value.values()), "")
    return normalize(str(value)).strip()


def decode(transform) -> tuple[str, int]:
    out = []
    missing = 0
    for word in WORDS:
        parts = []
        for number in word:
            value = key_value(transform(number))
            if value is None:
                missing += 1
                value = "xqz"
            parts.append(value.replace(" ", ""))
        out.append("".join(parts))
    return " ".join(out), missing


def score(text: str, counts: Counter[str], total: int, floor: float, n: int = 4) -> float:
    text = "^^^" + normalize(text) + "$$$"
    value = 0.0
    for i in range(len(text) - n + 1):
        count = counts.get(text[i : i + n], 0)
        value += math.log(count / total) if count else floor
    return value / max(1, len(text))


def candidates():
    modulus = 5000
    for shift in range(modulus):
        yield f"shift {shift:+d}", lambda n, s=shift: ((n + s - 1) % modulus) + 1
    for a in range(-25, 26):
        if a in (-1, 0, 1) or math.gcd(a, modulus) != 1:
            continue
        for shift in range(modulus):
            yield f"affine a={a:+d} b={shift:+d}", lambda n, a=a, s=shift: ((a * n + s - 1) % modulus) + 1
    for perm in itertools.permutations(range(4)):
        def digit_permutation(n: int, perm=perm) -> int:
            digits = f"{n:04d}"
            return int("".join(digits[i] for i in perm))
        yield f"digits {''.join(map(str, perm))}", digit_permutation
        yield f"digits9 {''.join(map(str, perm))}", lambda n, p=perm: int(
            "".join(str(9 - int(f"{n:04d}"[i])) for i in p)
        )


def main() -> None:
    counts, total, floor = train_ngrams()
    best: list[tuple[float, int, str, str]] = []
    for name, transform in candidates():
        plaintext, missing = decode(transform)
        value = score(plaintext, counts, total, floor) - missing * 0.02
        best.append((value, missing, name, plaintext))
    best.sort(reverse=True)
    for value, missing, name, plaintext in best[:30]:
        print(f"{value: .5f}  missing={missing:3d}  {name}")
        print(plaintext[:500])
        print()


if __name__ == "__main__":
    main()
