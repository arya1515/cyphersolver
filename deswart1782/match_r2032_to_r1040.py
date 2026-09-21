"""List R2032 learned units alongside every same-number R1040 symbol variant."""

import csv
import re
from collections import defaultdict

from probe_r1040_first_key import first_section_rows


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("record", nargs="?", default="R2032")
    args = ap.parse_args()
    variants = defaultdict(set)
    for _, raw, _ in first_section_rows():
        variants["".join(re.findall(r"\d", raw))].add(raw.strip())
    with open(f"{args.record}_alignment_probe.tsv", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    with open(f"{args.record}_to_R1040_candidates.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["index", "base_number", "proposed_plaintext", "R1040_raw_variants"])
        for row in rows:
            base = "".join(re.findall(r"\d", row["cipher_group"]))
            opts = " | ".join(sorted(variants.get(base, [])))
            if opts:
                w.writerow([row["index"], base, row["proposed_plaintext_unit"], opts])
    print(f"wrote {args.record}_to_R1040_candidates.tsv")


if __name__ == "__main__":
    main()
