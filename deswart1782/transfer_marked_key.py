"""Transfer a manually classified known-pair key to R1040's first section."""

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
    marked_text = (ROOT / f"{record}_marked_groups.txt").read_text(encoding="utf-8")
    marked_text = marked_text.split("\n\n", 1)[1]
    marked = re.findall(r"\d+(?:[:^+~=])?", marked_text)
    aligned = list(csv.DictReader(
        (ROOT / f"{record}_alignment_probe.tsv").open(encoding="utf-8"),
        delimiter="\t",
    ))
    assert len(marked) == len(aligned)

    candidates = defaultdict(set)
    evidence = defaultdict(list)
    for token, row in zip(marked, aligned):
        assert re.sub(r"\D", "", token) == re.sub(r"\D", "", row["cipher_group"])
        value = row["proposed_plaintext_unit"]
        candidates[token].add(value)
        evidence[token].append(int(row["index"]))
    learned = {token: next(iter(values)) for token, values in candidates.items()
               if len(values) == 1}
    conflicts = {token: values for token, values in candidates.items() if len(values) > 1}

    target = first_section_rows()
    rendered = []
    hits = 0
    rows = []
    for i, (page, raw, code) in enumerate(target, 1):
        value = learned.get(code)
        rows.append((i, page, raw, code, value or ""))
        if value is None:
            rendered.append(f"[{raw.strip()}]")
        else:
            rendered.append(value)
            hits += 1
    (ROOT / f"R1040_first_key_{record}_marked_probe.txt").write_text(
        textwrap.fill(" ".join(rendered), width=140, break_long_words=False) + "\n",
        encoding="utf-8",
    )
    with (ROOT / f"R1040_first_key_{record}_marked_probe.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["index", "page", "raw", "normalized_group", "plaintext"])
        w.writerows(rows)
    with (ROOT / f"{record}_reconstructed_key.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["normalized_group", "plaintext", "source_group_indices"])
        for token in sorted(learned):
            w.writerow([token, learned[token], ",".join(map(str, evidence[token]))])
    print(f"record={record} known_occurrences={len(marked)} key_entries={len(learned)} "
          f"conflicts={len(conflicts)} target_hits={hits}/{len(target)} ({hits/len(target):.1%})")
    for token, values in conflicts.items():
        print("CONFLICT", token, sorted(values), evidence[token])
    print(" ".join(rendered[:700]))


if __name__ == "__main__":
    main()
