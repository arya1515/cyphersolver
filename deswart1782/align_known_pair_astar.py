"""Optimal consistent known-pair alignment using an unconstrained DP heuristic."""

import csv
import heapq
import itertools
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from align_known_pair import read_pair, vocabulary
from align_known_pair_consistent import marked_tokens

ROOT = Path(__file__).resolve().parent


def main():
    record = sys.argv[1] if len(sys.argv) > 1 else "R2052"
    plain, base = read_pair(ROOT / f"{record}_known_pair.txt")
    tokens = marked_tokens(record)
    assert [re.sub(r"\D", "", x) for x in tokens] == [re.sub(r"\D", "", x) for x in base]
    counts = vocabulary()
    loose = list(csv.DictReader(
        (ROOT / f"{record}_alignment_probe.tsv").open(encoding="utf-8"),
        delimiter="\t",
    ))
    observed_lengths = defaultdict(set)
    for token, row in zip(tokens, loose):
        observed_lengths[token].add(len(row["proposed_plaintext_unit"]))
    allowed_lengths = {
        token: {m for size in sizes for m in range(max(1, size - 3), size + 4)}
        for token, sizes in observed_lengths.items()
    }
    by_first = {}
    for value, freq in counts.items():
        if value:
            cost = -math.log(freq + 0.25) - 0.015 * len(value)
            by_first.setdefault(value[0], []).append((value, cost))

    n, m = len(tokens), len(plain)
    inf = float("inf")
    # Exact best suffix cost when symbol identity is ignored. This is an
    # admissible lower bound for the constrained search.
    h = [[inf] * (m + 1) for _ in range(n + 1)]
    h[n][m] = 0.0
    for i in range(n - 1, -1, -1):
        min_left = n - i - 1
        for pos in range(m - 1, -1, -1):
            best = inf
            for value, cost in by_first.get(plain[pos], ()): 
                end = pos + len(value)
                if end <= m - min_left and h[i + 1][end] < inf:
                    best = min(best, cost + h[i + 1][end])
            h[i][pos] = best
    if h[0][0] == inf:
        raise SystemExit("unconstrained alignment is impossible")

    remaining = Counter(tokens)
    last = {token: max(i for i, item in enumerate(tokens) if item == token)
            for token in set(tokens)}
    serial = itertools.count()
    start = (0, 0, ())
    heap = [(h[0][0], 0.0, next(serial), start)]
    best_g = {start: 0.0}
    parent = {}
    expanded = 0
    final = None
    while heap:
        _, g, _, state = heapq.heappop(heap)
        if g != best_g.get(state):
            continue
        i, pos, frozen = state
        if i == n:
            if pos == m:
                final = state
                break
            continue
        token = tokens[i]
        assigned = dict(frozen)
        if token in assigned:
            value = assigned[token]
            candidates = [(value, -math.log(counts.get(value, 0) + 0.25) - 0.015 * len(value))]
        elif pos < m:
            candidates = ((value, cost) for value, cost in by_first.get(plain[pos], ())
                          if len(value) in allowed_lengths[token])
        else:
            continue
        for value, cost in candidates:
            end = pos + len(value)
            if not plain.startswith(value, pos) or end > m or h[i + 1][end] == inf:
                continue
            new_map = assigned.copy()
            if last[token] > i:
                new_map[token] = value
            else:
                new_map.pop(token, None)
            new_state = (i + 1, end, tuple(sorted(new_map.items())))
            ng = g + cost
            if ng < best_g.get(new_state, inf):
                best_g[new_state] = ng
                parent[new_state] = (state, value)
                heapq.heappush(heap, (ng + h[i + 1][end], ng, next(serial), new_state))
        expanded += 1
        if expanded % 100000 == 0:
            print(f"expanded={expanded} frontier={len(heap)} i={i} pos={pos}", flush=True)
    if final is None:
        raise SystemExit(f"no consistent alignment; expanded={expanded}")
    values = []
    state = final
    while state != start:
        prev, value = parent[state]
        values.append(value)
        state = prev
    values.reverse()
    out = ROOT / f"{record}_alignment_astar.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["index", "cipher_group", "plaintext_unit"])
        for i, (token, value) in enumerate(zip(tokens, values), 1):
            w.writerow([i, token, value])
    print(f"wrote {out.name}; expanded={expanded} cost={best_g[final]:.3f}")
    for i in range(0, n, 12):
        print(" ".join(f"{t}={v}" for t, v in zip(tokens[i:i+12], values[i:i+12])))


if __name__ == "__main__":
    main()
