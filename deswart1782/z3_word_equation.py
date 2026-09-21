"""Check whether a marked known pair admits a globally consistent segmentation."""

import re
import sys
import csv
from collections import defaultdict
from pathlib import Path

import z3

from align_known_pair import read_pair

ROOT = Path(__file__).resolve().parent


def main():
    record = sys.argv[1] if len(sys.argv) > 1 else "R2052"
    plain, _ = read_pair(ROOT / f"{record}_known_pair.txt")
    text = (ROOT / f"{record}_marked_groups.txt").read_text(encoding="utf-8").split("\n\n", 1)[1]
    tokens = re.findall(r'\d+(?:[:^+~="])?', text)
    loose = list(csv.DictReader(
        (ROOT / f"{record}_alignment_probe.tsv").open(encoding="utf-8"),
        delimiter="\t",
    ))
    observed_lengths = defaultdict(set)
    for token, row in zip(tokens, loose):
        observed_lengths[token].add(len(row["proposed_plaintext_unit"]))
    names = {token: z3.String(f"g_{re.sub(r'\W', '_', token)}") for token in set(tokens)}
    solver = z3.Solver()
    solver.set(timeout=300000)
    for token, var in names.items():
        lengths = {m for n in observed_lengths[token] for m in (n - 1, n, n + 1) if m >= 1}
        solver.add(z3.Or(*(z3.Length(var) == n for n in lengths)))
    solver.add(z3.Concat(*(names[token] for token in tokens)) == z3.StringVal(plain))
    result = solver.check()
    print(result)
    if result == z3.sat:
        model = solver.model()
        with (ROOT / f"{record}_z3_alignment.tsv").open("w", encoding="utf-8") as fh:
            fh.write("index\tcipher_group\tplaintext_unit\n")
            for i, token in enumerate(tokens, 1):
                value = model.eval(names[token], model_completion=True).as_string()
                fh.write(f"{i}\t{token}\t{value}\n")


if __name__ == "__main__":
    main()
