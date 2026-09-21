"""Normalize DECODE's digit-by-digit transcription of R1026 and R1027."""
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def groups(record_id: int) -> list[str]:
    source = next((ROOT / "decode").glob(f"DOC_R{record_id}_*.txt"))
    result: list[str] = []
    for raw_line in source.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw_line.startswith(("#", "<")):
            continue
        # The transcribers' J/J+ is the ordinary handwritten digit 3.
        line = raw_line.replace("J+", "3").replace("J", "3")
        for field in line.split("."):
            digits = "".join(re.findall(r"\d", re.sub(r"\?.*", "", field)))
            if 1 <= len(digits) <= 5:
                result.append(digits.lstrip("0") or "0")
    return result


all_groups: dict[int, list[str]] = {}
for rid in (1026, 1027):
    tokens = groups(rid)
    all_groups[rid] = tokens
    (ROOT / f"ciphertext_R{rid}.txt").write_text(" ".join(tokens) + "\n", encoding="utf-8")
    counts = Counter(tokens)
    print(f"R{rid}: {len(tokens)} tokens, {len(counts)} distinct")
    print("  most common:", " ".join(f"{g}:{n}" for g, n in counts.most_common(25)))
    print(f"  range: {min(map(int, tokens))}..{max(map(int, tokens))}")

shared = set(all_groups[1026]) & set(all_groups[1027])
print(f"shared: {len(shared)} groups")
print(" ".join(sorted(shared, key=lambda x: (-sum(all_groups[r].count(x) for r in all_groups), int(x)))))
