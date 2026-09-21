"""Align a plaintext/cipher pair while enforcing repeated-symbol identity."""

import csv
import heapq
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from align_known_pair import read_pair, vocabulary

ROOT = Path(__file__).resolve().parent


def marked_tokens(record):
    text = (ROOT / f"{record}_marked_groups.txt").read_text(encoding="utf-8")
    text = text.split("\n\n", 1)[1]
    return re.findall(r'\d+(?:[:^+~="])?', text)


def align(plain, tokens, counts, allowed_lengths=None, beam_size=300000):
    by_first = {}
    for value, freq in counts.items():
        if value:
            by_first.setdefault(value[0], []).append((value, freq))
    remaining = Counter(tokens)
    # (position, sorted active assignments) -> (cost, path)
    beam = {(0, ()): (0.0, ())}
    for index, token in enumerate(tokens):
        remaining[token] -= 1
        next_beam = {}
        groups_left = len(tokens) - index - 1
        for (pos, frozen), (cost, path) in beam.items():
            assignments = dict(frozen)
            if token in assignments:
                candidates = [(assignments[token], counts.get(assignments[token], 0))]
            elif pos < len(plain):
                candidates = by_first.get(plain[pos], [])
                if allowed_lengths is not None:
                    candidates = [(value, freq) for value, freq in candidates
                                  if len(value) in allowed_lengths[token]]
            else:
                continue
            for value, freq in candidates:
                end = pos + len(value)
                if not plain.startswith(value, pos):
                    continue
                # Every remaining group must consume at least one character.
                if end + groups_left > len(plain):
                    continue
                new_assignments = assignments.copy()
                if remaining[token] > 0:
                    new_assignments[token] = value
                else:
                    new_assignments.pop(token, None)
                frozen_new = tuple(sorted(new_assignments.items()))
                key = (end, frozen_new)
                step = -math.log(freq + 0.25) - 0.015 * len(value)
                new_item = (cost + step, path + (value,))
                if key not in next_beam or new_item[0] < next_beam[key][0]:
                    next_beam[key] = new_item
        if not next_beam:
            raise SystemExit(f"beam exhausted at group {index + 1}/{len(tokens)} token={token}")
        if len(next_beam) > beam_size:
            keep = heapq.nsmallest(beam_size, next_beam.items(), key=lambda item: item[1][0])
            beam = dict(keep)
        else:
            beam = next_beam
        if (index + 1) % 20 == 0:
            best = min(item[0] for item in beam.values())
            print(f"group={index + 1} states={len(beam)} best={best:.2f}")
    finals = [item for (pos, _), item in beam.items() if pos == len(plain)]
    if not finals:
        furthest = max(pos for pos, _ in beam)
        raise SystemExit(f"no exact final alignment; furthest={furthest}/{len(plain)}")
    return min(finals, key=lambda item: item[0])[1]


def main():
    record = sys.argv[1] if len(sys.argv) > 1 else "R2052"
    plain, base_tokens = read_pair(ROOT / f"{record}_known_pair.txt")
    tokens = marked_tokens(record)
    if [re.sub(r"\D", "", t) for t in tokens] != [re.sub(r"\D", "", t) for t in base_tokens]:
        raise SystemExit("marked transcription does not match base-number sequence")
    loose_path = ROOT / f"{record}_alignment_probe.tsv"
    loose = list(csv.DictReader(loose_path.open(encoding="utf-8"), delimiter="\t"))
    lengths = defaultdict(set)
    for token, row in zip(tokens, loose):
        size = len(row["proposed_plaintext_unit"])
        lengths[token].update(range(max(1, size - 6), size + 7))
    values = align(plain, tokens, vocabulary(), lengths)
    out = ROOT / f"{record}_alignment_consistent.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["index", "cipher_group", "plaintext_unit"])
        for i, (token, value) in enumerate(zip(tokens, values), 1):
            w.writerow([i, token, value])
    print(f"wrote {out.name}; chars={len(plain)} groups={len(tokens)}")
    for i in range(0, len(tokens), 12):
        print(" ".join(f"{t}={v}" for t, v in zip(tokens[i:i+12], values[i:i+12])))


if __name__ == "__main__":
    main()
