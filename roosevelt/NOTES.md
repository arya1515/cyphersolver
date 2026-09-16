# Roosevelt cryptogram, 1935 (Schmeh Top 50 no. 17) — numeric block, attempted 2026-09-16

A sheet received by the Secret Service on 24 April 1935 (receiving stamp), headed "Secret Service", with three
lines of handwritten digits, two lines of letters, a skull and crossbones and a dagger through a boot, and a
diagonal "261" top right. William Friedman reproduced it as fig. 2 of his first lecture (*The Friedman
Legacy*, NSA Center for Cryptologic History 1992, p. 8) as "an authentic example of a transposition cipher",
solved only the letter part ("Did you ever bite a lemon?" read from every second letter of
NDOIMDEYLOAUEETVIEBR?, followed by OR ELSE YOU DIE!! in clear) and said nothing about the digits. Klaus Schmeh
posted it in October 2015 (German) and as Top 50 no. 17 in December 2017. In the comments to the 2017 post
Thomas Ernst argued that the digit block is a "doodle, if not a fake" because the tick-joined pairs give every
number from 10 to 52 exactly once; Gerd extended this to 1..52 with the single digits. The only images in
circulation are the 614 px Cipherbrain scan and the book figure.

Sources used: the two Cipherbrain posts and their comment threads (`../top50/arts/17.txt`), the FDLP PDF of the
NSA book (fig. 2 is embedded at only 426 x 354 px) and the Internet Archive 300 ppi page scan of the same book
(`friedman_legacy_fig2_300ppi.png`, cropped from item friedman_tribute-nsa, leaf 0018), which is the sharpest
copy available and is the basis of the reading below.

## Reading

`cipher.txt`. At glyph level the "apostrophes" of Schmeh's transcription are short ticks written between and
above two digits; the two digits under a tick are one number. Digits without a tick are single numbers. Zeros
are written in groups. This reading agrees with Schmeh's transcription and with Gerd's number list character
for character:

```
17 2 | 10 15 17 19 21 26 | 8 | 32 33 20 37 | 000000 | 16 27 12 34 38
28 22 39 40 41 42 48 44 | 000000 | 9 3 13 | 000 | 18 4 23 24 | 000
46 29 35 51 5 43 47 | 000 | 6 11 36 50 52 30 49 45 25 31 14 -
```

The pencil marks under
the lines that Andreas and Ernst noticed, presumably Friedman's or the Secret Service's trial letters, are not
recoverable from either scan.

**Ernst's claim is confirmed.** The 43 tick-joined pairs are exactly {10, ..., 52}, each once. The nine single
digits are exactly {1, ..., 9}, each once, in the order 1 7 2 8 9 3 4 5 6. The 18 zeros come in groups of
6, 6, 3, 3. So the block is a permutation of 1..52 with four zero-group separators, nothing more.

## Structure of the permutation (`structure.py`)

Sequence: 1 7 2 10 15 17 19 21 26 8 32 33 20 37 | 16 27 12 34 38 28 22 39 40 41 42 48 44 | 9 3 13 | 18 4 23 24 46 29 35 51 5 43 47 | 6 11 36 50 52 30 49 45 25 31 14.

| statistic | observed | uniform random permutation of 52 | p (200 000 shuffles) |
|---|---|---|---|
| Spearman correlation of value with position | +0.39 | 0 | 0.002 |
| adjacent pairs differing by exactly +1 | 5 (incl. 39 40 41 42) | ~1 | 0.003 |
| rising sequences (riffle-shuffle decomposition) | 16 | ~26.5 | < 5e-6 (none in 200 000 below 17) |
| adjacent pairs summing to 53 | 4 (three of them across zero groups: 37|16, 44|9, 47|6) | ~1 | 0.018 |

The rising sequences are long chains of consecutive values whose positions increase: 1-6, 7-9, 21-25, 26-31,
32-36, 37-43. Numbers were written down in several interleaved upward sweeps. Cycle structure 1 + 5 + 46,
no fixed grid signature (no width w gives a surplus of adjacent differences of w beyond w = 5, 6 at 5 and 6
pairs), so it is not a columnar rearrangement of 1..52.

Two generating processes were compared with the uniform null:

- *Hand-written "random" permutation (Ernst's doodle).* A person enumerating 1..52 once each without a list
  tends to drift upward (positive rank correlation), to fall back to skipped low numbers, and to run through
  short consecutive bursts when fresh numbers run out (39 40 41 42, 23 24, 32 33). Every anomaly in the table
  is of this kind. *This is an inference about human behaviour, not a fitted model; no corpus of
  hand-generated permutations was available to fit.
- *Shuffled deck of 52 cards (the one natural object with 52 items).* Under the Gilbert-Shannon-Reeds model,
  16 rising sequences is typical of 4 riffles (P = 0.09), but the joint event of 16 or fewer rising sequences
  with rank correlation >= 0.39 and >= 5 consecutive adjacencies has probability 0.003 at 4 riffles and 0.023
  at 3. A riffled deck with this few rising sequences would not also drift upward this strongly. The deck
  reading is disfavoured but not excluded.

Neither process produces text.

## Cipher readings that are testable, and their result (`solve_ordered.py`)

A permutation of 1..52 can only be a cipher if every cipher number is used once: a homophonic substitution
with 52 homophones each used once, or a numerical transposition key derived from a 52-letter phrase by ranking
its letters (XMAS -> 4 2 1 3, Norbert's suggestion). With an unordered key either reading can yield any text
at all and is untestable (Thomas's comment #5 and Gerd's reply show this). With an *ordered* key, homophones
assigned to letters in alphabetical order, or the phrase recovered from the inverse permutation with letters
nondecreasing along the ranks, the plaintext is determined by 51 boundary choices, roughly 66 bits, against
about 70 bits of redundancy in 52 letters of English, so the readings are testable at the edge of what
52 letters allow.

Method: simulated annealing over nondecreasing maps 1..52 -> a..z, scored with the Copenhagen character
5-gram English model (`../copenhagen/lm_en.bin`), six readings: sequence order and inverse permutation,
alphabet a..z and z..a, zero groups as word breaks or ignored. Controls: 52-letter passages from Dickens and
Melville, enciphered with ordered homophonic keys sized by the passage's letter counts, homophones shuffled
within each letter, attacked identically.

Runs: `run_main.log` (40 restarts x 20 000 steps) and `run_main_long.log` (60 x 60 000) on the block;
`run_control.log` and `run_control_long.log` on the controls with the same settings.

| reading | best score per letter (either run) | best candidate |
|---|---|---|
| sequence, a..z | -3.02 | abadefillbookofmdoomloorstsbadfallsnowassadovyouslod |
| sequence, z..a | -3.18 | uttooooonsnnolonominoffeedertootooenlatedtoldandenno |
| sequence, a..z, zero groups as breaks | -2.70 | abadefillbooko endoonloorsus dad falltoowast adovyouslod |
| sequence, z..a, zero groups as breaks | -2.79 | uttoooooornnol ooonlookiiide rto otoodonated toldanddono |
| inverse permutation, a..z | -2.63 | derssteeretiryehereheissuehistwehisthinnootrustoutst |
| inverse permutation, z..a | -3.03 | ttheeetsiteseatstetstreeatssedassseesspooneibeendeed |

Controls (60 x 60 000): 7 of 8 recovered to readable English, 88-100 % of letters correct, best scores -1.48 to
-1.97 per letter (true plaintext -1.50 to -1.97); the eighth landed at 46 % and -2.37 with the truth at -1.62,
so the search does fail on about one passage in eight. Nothing from the block comes within 0.6 nats per letter
of a recovered control, and no candidate contains a run of English longer than a chance word.

Note that both cipher readings force the low numbers onto early letters of the alphabet: under a..z the singles
1-9 must all be a, b or c, so the sequence's opening 1 7 2 becomes "aba..." in every candidate. The block's
structure is itself hostile to an ordered key.

## Verdict

Ernst's arithmetic is right and the permutation's statistics point to a hand-written list rather than to a
cipher or to a shuffled deck. The one cipher family that is testable at this length, ordered homophonic or
rank-key readings, fails while matched controls succeed. Unordered keys remain possible in principle and would
make the block a one-time key with no ciphertext, which is indistinguishable from a doodle. Closed as
explained, not read.

What would reopen it: the original sheet at the NSA William F. Friedman Collection (the typed text on the
other side and the pencil trials under the digits), or a second message from the same sender.

Checked: glyph-level reading against both scans; Ernst's 10..52 and Gerd's 1..52 claims; permutation
statistics against 200 000 uniform shuffles and GSR riffle simulations; ordered-key annealing with controls.
Not checked: unordered homophonic keys (untestable); the pencil marks under the digits; the reverse side of
the sheet; whether the "261" or the zero groups mean anything. User must verify: nothing here is an
independent reading of the document; all output unvalidated until reviewed.
