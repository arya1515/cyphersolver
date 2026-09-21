"""Propose a code-group/plaintext alignment for the recovered Rechteren pair.

The 1785-87 key is missing, but contemporary Croiset nomenclators share a large
plaintext vocabulary.  We use that vocabulary only to choose plausible segment
boundaries in an independently known plaintext; cipher values are learned from
the recovered pair, never imported from the other key.
"""

import csv
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from decode_1765 import load_key


ROOT = Path(__file__).resolve().parent
KEY1803 = Path(r"C:\Users\dbour\Downloads\DOC_1035_2026-Jan-09-15-24-07_36531.csv")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "".join(re.findall(r"[a-z]", s.casefold()))


def read_pair(path):
    text = path.read_text(encoding="utf-8")
    plain, cipher = text.split("## Ciphertext", 1)
    plain = plain.split("## Plaintext (diplomatic normalization)", 1)[1]
    plain = norm(plain)
    if "(provisional palaeographic transcription)" in cipher:
        cipher = cipher.split("(provisional palaeographic transcription)", 1)[1]
        cipher = cipher.split("Mark classes", 1)[0]
    if "BEGIN GROUPS" in cipher:
        cipher = cipher.split("BEGIN GROUPS", 1)[1]
    tokens = re.findall(r"\d+(?:\^''|\^__|\^_|\^')?", cipher)
    return plain, tokens


def vocabulary():
    key, _ = load_key()
    values = [v for v in key.values() if not v.startswith("<")]
    with KEY1803.open(encoding="utf-8-sig", newline="") as fh:
        values.extend(row[1] for row in csv.reader(fh) if len(row) >= 2 and row[1])
    counts = Counter(norm(v) for v in values)
    counts.update({c: 50 for c in "abcdefghijklmnopqrstuvwxyz"})
    counts.pop("", None)
    return counts


def align(plain, tokens, counts):
    by_first = {}
    for value, freq in counts.items():
        by_first.setdefault(value[0], []).append((value, freq))
    # DP state (plaintext position, group count) -> (cost, previous state, value)
    dp = {(0, 0): (0.0, None, None)}
    n = len(tokens)
    for used in range(n):
        frontier = [(pos, item) for (pos, k), item in dp.items() if k == used]
        for pos, (cost, _, _) in frontier:
            if pos >= len(plain):
                continue
            candidates = list(by_first.get(plain[pos], []))
            # A diplomatic copy can contain spellings or abbreviations absent
            # from the surviving comparison keys.  Permit short literal
            # fallbacks, but price them far above attested nomenclator units so
            # they only bridge those local vocabulary gaps.
            candidates.extend((plain[pos:pos + width], -1) for width in (2, 3, 4)
                              if pos + width <= len(plain))
            for value, freq in candidates:
                if plain.startswith(value, pos):
                    # Homophone count is an empirical prior. A tiny per-character
                    # reward breaks ties in favor of meaningful multi-letter units.
                    step = (12.0 + len(value) if freq < 0 else
                            -math.log(freq + 0.25) - 0.015 * len(value))
                    state = (pos + len(value), used + 1)
                    new = cost + step
                    if state not in dp or new < dp[state][0]:
                        dp[state] = (new, (pos, used), value)
    state = (len(plain), n)
    if state not in dp:
        raise SystemExit(f"No exact alignment: chars={len(plain)} groups={n}")
    vals = []
    while state != (0, 0):
        cost, prev, value = dp[state]
        vals.append(value)
        state = prev
    return list(reversed(vals))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pair", nargs="?", default="R2032_known_pair.txt")
    args = ap.parse_args()
    pair = ROOT / args.pair
    plain, tokens = read_pair(pair)
    vals = align(plain, tokens, vocabulary())
    print(f"chars={len(plain)} groups={len(tokens)}")
    out = ROOT / f"{pair.stem.replace('_known_pair', '')}_alignment_probe.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["index", "cipher_group", "proposed_plaintext_unit"])
        for i, (token, value) in enumerate(zip(tokens, vals), 1):
            w.writerow([i, token, value])
    for i in range(0, len(tokens), 13):
        print(" ".join(f"{t}={v}" for t, v in zip(tokens[i:i+13], vals[i:i+13])))


if __name__ == "__main__":
    main()
