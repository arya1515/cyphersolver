# Scorpion letters, 1991 (Schmeh Top 50 no. 12) — attempted 2026-09-15

Two of the five cipher passages sent to John Walsh in 1991 are public: S1 (10 x 7 = 70 symbols) and S5
(12 x 15 = 180 symbols). S2-S4 are held by law enforcement. Sources: Schmeh's Top 50 article (scans from
Oranchak's site), Nick Pelling's Cipher Mysteries posts 2014-2018, the Cipher Foundation page, and the
zodiackillerciphers.com forum thread "Scorpion = Zodiac?".

## Files

* `s5.txt` — S5 as a numeric sequence (symbols 1-145 in order of first appearance), from the forum thread.
  The letter writes 15 symbols per row; the forum re-wraps the same sequence at 16, the period of every repeat.
* `s1.txt` — S1 transcribed here from the Cipherbrain scan (454 px, upscaled 3x), descriptive symbol names,
  uncertain identities flagged in the file. 70 symbols, 53 distinct, matching the published count.
* `unicity.py` — the two calculations below (needs the English LM built by `../copenhagen/solve.py`).

## What the two ciphers are, measured

**S5.** 180 symbols, 145 distinct. Every one of the 43 repeat pairs lies at a distance that is a multiple
of 16 (9 at 16, 5 at 32, 6 at 48, ... 1 at 160). Read in 16 columns, the columns hold 6 to 11 distinct
symbols out of 11 or 12. So S5 behaves like 16 substitution alphabets used in strict rotation, as Pelling
and "Teddy" found in 2007-2014. Two further numbers:

| test | observed | 16 monoalphabetic English alphabets (simulated) |
|---|---|---|
| within-column repeats | 35 | 47.7 +- 4.9 (z = -2.6) |
| spread of repeats across columns (variance) | 2.28 | 1.38, P(>= observed) = 0.05 |

Too few repeats for 16 plain 26-letter alphabets, as GeoffLaT also found; two homophones for the seven
commonest letters in each alphabet would fit the total (32.6 +- 4.5) but makes the uneven spread across
columns less likely still (P = 0.014). Column 1 (the first symbol of each 16-run) repeats far more than
the rest: 7 distinct symbols in 12, against 10 or 11 in most columns.

**S1.** 70 symbols, 53 distinct, 22 repeat pairs. Eight of the 22 lie at distances that are multiples of 5,
against 4.1 expected by shuffling (P = 0.036); four at multiples of 10 (1.9 expected, P = 0.12). That is the
whole of the evidence for Pelling's "five cycling alphabets"; it depends partly on my identifications of
the filled-square and half-circle glyph families, which are the uncertain ones. S, lambda and K each recur
in positions that break a strict period of 5.

## Why neither can be solved from what is published

**Unicity.** A homophonic key assigning each distinct symbol one of 26 letters carries about log2(26) bits
per symbol; English text supplies about 3.2 bits of redundancy per letter.

| cipher | key information | redundancy of the text | ratio |
|---|---|---|---|
| S1 | 53 x 4.70 = 249 bits | 70 x 3.2 = 224 bits | 1.11 |
| S5 | 145 x 4.70 = 682 bits | 180 x 3.2 = 576 bits | 1.18 |

Both sit below the unicity distance: more than one fluent English plaintext is consistent with each
ciphertext, so no ciphertext-only method can single out the right one. Adding the 16-alphabet structure
makes it worse, not better (16 independent alphabets is far more key), unless the alphabets are tied to
each other by a rule, and the fact that no symbol ever recurs across two columns means the ciphertext
itself offers no such tie.

**Matched control.** `unicity.py` enciphers random English passages of 70 and 180 letters with random
homophonic keys of exactly 53 and 145 symbols and attacks them with the same 5-gram English annealer:

| control | letter accuracy of the best solution | its score against the true text |
|---|---|---|
| S1-sized, trial 1 | 0.13 | found -112 vs truth -107 |
| S1-sized, trial 2 | 0.13 | "snotconcetorasestayalongdispointent..." |
| S5-sized, trial 1 | 0.03 | found -330 vs truth -326 |
| S5-sized, trial 2 | 0.12 | found -334 vs truth -301 |

The solver returns fluent English every time and it is never the plaintext. Any "solution" of S1 or S5
produced by AZdecrypt-style search, including the three claimed ones on record (Farmer 2007, Roberts
2016, "Rubislaw32" 2022), should be read in that light: fluent output is guaranteed at this multiplicity
and proves nothing.

## Status

Not solvable from the published material, for a reason that is quantitative rather than a matter of
effort. What would change it: release of S2-S4 (more text under the same 16 alphabets, if the writer kept
the system); a glyph-feature transcription of S5 testing whether shape families run in diagonals across
the 16 alphabets, which is the one hypothesis that would tie the alphabets together; or the author's own
statement that "all of my ciphers can be decoded simply, once the limited patterns and systems are
discovered", which, if true, points to a systematic key table rather than a random one.
