"""Diagnostic transfer of base-number mappings from a known plaintext pair.

This deliberately ignores digit-level marks.  It only transfers a base number
when every occurrence in one known pair received the same aligned plaintext
unit.  Output is evidence for (or against) key reuse, not a final decipherment.
"""

import csv
import re
import sys
import textwrap
from collections import defaultdict
from pathlib import Path

from probe_r1040_first_key import first_section_rows

ROOT = Path(__file__).resolve().parent


def main():
    record = sys.argv[1] if len(sys.argv) > 1 else "R2051"
    rows = list(csv.DictReader(
        (ROOT / f"{record}_alignment_probe.tsv").open(encoding="utf-8"),
        delimiter="\t",
    ))
    values = defaultdict(set)
    for row in rows:
        values[re.sub(r"\D", "", row["cipher_group"])].add(row["proposed_plaintext_unit"])
    learned = {base: next(iter(vs)) for base, vs in values.items() if len(vs) == 1}

    target = first_section_rows()
    rendered = []
    hits = 0
    for _, raw, _ in target:
        base = "".join(re.findall(r"\d", raw))
        value = learned.get(base)
        if value is None:
            rendered.append(f"[{raw.strip()}]")
        else:
            rendered.append(value)
            hits += 1
    (ROOT / f"R1040_first_key_{record}_base_probe.txt").write_text(
        textwrap.fill(" ".join(rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    print(f"record={record} learned_unique_bases={len(learned)} "
          f"target_hits={hits}/{len(target)} ({hits/len(target):.1%})")
    print(" ".join(rendered[:500]))


if __name__ == "__main__":
    main()
