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

## The claimed solution of 2018, tested (2026-09-15)

Forum user "Rubislaw32" posted full homophonic readings of S1 and S5 on zodiackillermystery.freeforums.net
(first on 19 October 2018; the thread "Scorpion's Ciphers - The Zodiac, 1991 and beyond" carries them;
Cipher Mysteries lists the claim under 2022). S1: "A picture in collection of people: Bagel Bob's Old Dairy
Frothy Late Cofee. Pour action." S5: "I am sending other picture of people for the collection of recent
hybrid genders with edge, kept from artistic fee, if person of age has to purchase pick of university
uglies. Espresso NYP cofee forces a cold enema review."

`claimed.py` applies the one hard test a homophonic key must pass, that every repeated symbol decodes to the
same letter, against the transcriptions in this directory:

| cipher | repeated symbols | consistent | conflicts |
|---|---|---|---|
| S1 (this repo's transcription) | 13 | 10 | crosshair N/L; two symbols this repo marked uncertain (circL, sqnotchBR) |
| S5 (forum numeric transcription) | 27 | 26 | symbol 41 reads C, G, C |

So the claim is a valid homophonic reading in the weak sense: it honours nearly all of the two dozen equality
constraints the ciphertexts impose. That is cheap. With 53 symbols over 70 letters the constraints fix about
17 letters, and with 145 over 180 about 35; the rest is free choice. The English is the tell:

| text | 5-gram English score, nats per letter |
|---|---|
| claimed S1 | -2.74 |
| claimed S5 | -2.61 |
| genuine English (reference passage) | -1.58 |
| the controls' false solutions (unicity.py) | -1.60 (70 letters), -1.83 and -1.86 (180 letters) |

The claimed plaintexts score worse than the fluent false solutions the annealer produced for random keys
in `unicity.py`. `alternatives.py` makes the point constructively: it fills each cipher with real English
words under exactly the same-symbol-same-letter rule and lists other "solutions" that fit as well or better
(results in `results_alternatives.txt`). None of them is the plaintext either. The claim cannot be verified
from S1 and S5 alone, and nothing in it is more probable than the alternatives.
