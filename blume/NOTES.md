# "BLUME SALAMANCA" telegrams, Zurich → London, 8 January 1937 — in progress, paused 15 Sept 2026

Two telegrams were sent from Zurich via London (one annotated *via Angleterre Eastern*) to Spain on 8 January
1937. Both begin *BLUME SALAMANCA*, most likely a telegraphic address (Blume, Salamanca) followed by five-letter
groups. The historian Regula Bochsler found them in the Swiss Federal Police files on Werner Oswald, founder of
the Emser Werke (*Nylon und Napalm*, 2022), and Klaus Schmeh posted them on Facebook. Oswald told the police
they concerned "wool business" in Spain; Bochsler doubts that, given his ties to Franco's side. Salamanca was
Franco's headquarters in January 1937.

**Status: not solved.** No plaintext has been recovered. The type of cipher is identified, and a large part of
the key space has been excluded with methods proven on planted messages.

## Transcription

Only the first telegram is reachable. The photograph was retrieved from Schmeh's Facebook post at
1,134 × 1,012 px (`telegram1.jpg`); the second telegram is not in the public preview. `tg.py` holds
**123 groups, 615 letters**. The transcription checks against the form: 123 groups + BLUME + SALAMANCA =
**125 words**, the figure written in the *Wörter* box, with the pencilled (50) and (100) at the right groups.
Group 121 (`RBEEP`) has a red stroke through it but is counted.

## Established

**It is a transposition, and the language is Spanish.** The index of coincidence is **0.0699**, the value of a
natural language (random letters give 0.038, codes and polyalphabetic ciphers much less). Letter frequencies
in place fit Spanish best: chi-squared 102, against French 150, English 207, Italian 217 and German 582. A
transposition keeps every letter as itself, so the plaintext's letters are all present, merely reordered.

Two irregularities are worth keeping in mind:
* `x` occurs 6 times in 615 letters, where Spanish expects about 1. It probably marks stops or padding
  (`ANANX`, `REFLX`).
* `p` runs high (5.7% against 2.5%). That may point to telegraphic *punto* or to padding.

## Excluded (each search first shown to find planted Spanish of the same length)

| family | search | planted control | real telegram |
|---|---|---|---|
| rail fence, 2–60 rails, all offsets | exhaustive (`families.py`) | found exactly | best −6.34 per quadgram (Spanish −4.1, shuffled −6.3) |
| skip / decimation, every step and start | exhaustive | found exactly | at shuffle level |
| route transpositions, grids 2–60 wide: columns up/down/snake, rows reversed/snake, diagonals, spirals | exhaustive, both directions | found exactly | at shuffle level |
| single columnar transposition, widths 4–20 | annealing (`trans.py`) | recovers widths 9, 14, 19 | best −6.03 |
| double columnar, small widths 5–12 × 5–12 | Python annealing (`double.py`) | weak, about 1 in 4 | nothing (28 pairs completed) |

107,594 fixed-pattern readings were scored in all.

## Tools built for double transposition (not yet completed on the real telegram)

**`dt/dt.exe`** is a multithreaded C# simulated-annealing solver for double columnar transposition, same key
or two keys. Planted 615-letter Spanish tests:

| widths | result |
|---|---|
| same key 17 | **615/615**, 2.8 s |
| same key 20, 23, 26, 29 | not found |
| different keys 11 / 14 | **615/615**, 6.9 s |
| different keys 15/16, 17/13, 18/19, 16/21, 19/23, 23/19, 25/21, 13/27 | not found |

So it has power up to same-key width 17 and different keys of about 11 × 14.

**`dt/dt2.exe`** is the same solver with the reversed direction (`DT_INV=1`: plaintext written down the columns
in key order, read out by rows). Planted tests: same key 13 → 615/615; different keys 9/12 → key found
(score equals the true key's; 369 letters placed, the rest a scoring tie).

**`dt/idp.exe`** is a divide-and-conquer attack for long keys, after Lasry, Kopal & Wacker (2014). It anneals
the second key alone, scored by IDP: whether undoing it leaves columns that pair into good Spanish letter
pairs. It then solves the first key as a single columnar transposition. The score separates the true key on a
planted 19/23 case (−2.22 against −2.39 for a random key). A short test search (20,000 steps, sharing the CPU)
did not yet reach it.

## Runs in progress when paused

The real telegram was being run through `dt.exe` (same key, widths 2–40, then different keys 2–16 × 2–16).
The run was stopped on request before it wrote results, so **none of that range is excluded yet**.

## Next steps, in order

1. Re-run `dt.exe` on the real telegram over its power range (same key 2–17; different keys to 14 × 14), in
   both directions (`dt.exe` and `DT_INV=1 dt2.exe`). About an hour on 24 cores.
2. Scale `idp.exe` (millions of steps, all cores), prove it on planted 15–25-wide keys, then run it over widths
   15–25.
3. Try the rectangular widths the length suggests: 615 = 3 × 5 × 41, so 15 and 41 give complete columns.
4. Crib-constrained search with likely words (*lana*, *pesetas*, *francos*, *punto*, *Burgos*, *Oswald*).
5. Needs outside help: **the second telegram** (from Bochsler or Schmeh). Same day and same sender almost
   certainly means the same keys, and two messages under one key can be attacked jointly.

Reproduce: `python families.py`, `python trans.py 4 20 4`, `python double.py control`, `dt/dt.exe plant ...` /
`dt/dt.exe solve ../ct1.txt ...` (build with .NET Framework `csc.exe /o+`; needs `q4_es.bin` from the export
step in these notes).
