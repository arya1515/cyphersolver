"""Apply securely learned Rechteren-key entries to R1040's first section."""

import csv
import re
import textwrap
from collections import defaultdict
from pathlib import Path

from probe_r1040_first_key import first_section_rows


ROOT = Path(__file__).resolve().parent


def learn_conservative():
    by_base = defaultdict(list)
    for record in ("R2032", "R2052"):
        rows = list(csv.DictReader((ROOT / f"{record}_to_R1040_candidates.tsv").open(encoding="utf-8"), delimiter="\t"))
        for row in rows:
            row["record"] = record
            by_base[(record, row["base_number"])].append(row)
    learned = {}
    evidence = {}
    for (record, base), group in by_base.items():
        variants = group[0]["R1040_raw_variants"].split(" | ")
        values = {row["proposed_plaintext"] for row in group}
        if len(variants) == 1 and len(values) == 1:
            raw, value = variants[0], next(iter(values))
            if raw not in learned or learned[raw] == value:
                learned[raw] = value
                evidence.setdefault(raw, []).append(f"{record} alignment; unique R1040 variant")
            else:
                learned.pop(raw, None)
                evidence.pop(raw, None)
    return learned, evidence


def main():
    learned, evidence = learn_conservative()
    with (ROOT / "R1040_first_key_reconstructed.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["transcribed_group", "plaintext", "evidence"])
        for raw, value in sorted(learned.items()):
            w.writerow([raw, value, "; ".join(evidence[raw])])
    rows = first_section_rows()
    rendered = []
    hits = 0
    for page, raw, _ in rows:
        value = learned.get(raw.strip())
        if value is None:
            rendered.append(f"[{raw.strip()}]")
        else:
            rendered.append(value)
            hits += 1
    (ROOT / "R1040_first_key_partial_decipherment.txt").write_text(
        textwrap.fill(" ".join(rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    print(f"learned_entries={len(learned)} target_tokens={len(rows)} decoded={hits} ({hits/len(rows):.1%})")
    print(" ".join(rendered[:500]))


if __name__ == "__main__":
    main()
