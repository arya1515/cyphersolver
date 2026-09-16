# Chinese "gold bar" cryptograms, Shanghai 1933 — not an encryption

Source: Kevin McCurley's 1996 IACR page, <https://www.iacr.org/misc/china/> and its
<https://www.iacr.org/misc/china/cryptograms.html>. Seven bars allegedly issued to a "General Wang" in
Shanghai in 1933, said to certify a bank deposit of over $300,000,000. Sixteen distinct strings of Latin
letters, 8 to 25 characters, 263 letters in all, reused across the bars. Listed by Elonka Dunin among the
famous unsolved ciphers.

## Result

**The inscriptions are not enciphered text of any kind.** The corpus is a deliberately constructed uniform
letter multiset: *ten of every letter of the alphabet*, give or take a few. Twenty-one of the twenty-six
letters land on exactly ten in McCurley's transcription; the deviations (E, S +1; O, T -1; I +3) are not all
transcription noise, see the photograph check below.

```
A10 B10 C10 D10 E11 F10 G10 H10 I13 J10 K10 L10 M10 N10
O 9 P10 Q10 R10 S11 T 9 U10 V10 W10 X10 Y10 Z10
```

Twenty-one of the twenty-six letters occur exactly ten times. Ten of each would be 260 letters; the
transcription has 263.

| test | value |
|---|---|
| index of coincidence | 0.0350 (English 0.0667, random 0.0385) |
| chi-squared against uniform, 25 df | **1.251** |
| P(chi-squared <= 1.251) | **9.3 x 10^-13**, about 1 in a trillion |
| chi-squared against English letter frequencies | 1488 |
| Monte Carlo, 200 000 random 263-letter strings reaching this uniformity | **0** |

A chi-squared of 1.25 where chance predicts 25 means the text is twenty times *more* uniform than random
sampling permits. That rules out every encryption of a natural-language plaintext:

* simple substitution and any transposition preserve the plaintext's frequency skew (IC about 0.066);
* a short-key Vigenere flattens only part way (IC about 0.045);
* a long key or a one-time pad reaches IC 0.0385 **with the variance of random sampling** — chi-squared
  near 25, not near 1.

Only someone laying out ten of each letter and arranging them produces this. The arrangement *within* the
sixteen strings is then consistent with random dealing from that pool: 71 within-string repeated letters
observed against 65.6 expected when the same pool is shuffled into the same lengths.

## Reading

The inscriptions are decorative filler made to look like cryptograms. This sits with the other objections
already raised against the bars: the aircraft depicted on them is a model that did not fly until 1934-35,
after the claimed 1933 date; the banks rejected the deposit claim in the 1990s; and the attorney's file was
closed. There is no message to recover, so the item should be reclassified from "unsolved cipher" to
"constructed, not a cipher".

Reproduce: `python analyse.py` (corpus is in `corpus.py`; needs numpy/scipy). `python readings.py` gives the
same statistics for each defensible reading of the two doubtful strings.

## Independent corroboration, added 2026-09-15

Checking Schmeh's Top 50 list (entry 49) turned up the documentary case against the bars in fuller form
than we had it, and it agrees with the statistics from a completely different direction:

* the aircraft depicted is a **Boeing 247 class**, in service from 1934, after the claimed 1933 date
* **"General Wang Jialie"** was only promoted Lieutenant-General in 1936
* the year is given in the **Gregorian** calendar rather than the Republican (Minguo) reckoning a 1933
  Chinese document would use
* some characters are **simplified forms** not made official until 1955-56
* one bar references **1948**

Nick Pelling's reading is that they are a post-war fake, probably early-to-mid 1950s, produced in the
context of a live legal dispute over a claimed $300 million bank deposit - that is, with a fraud motive
behind the objects.

Two independent lines now agree. The letter distribution says the inscriptions were constructed rather
than enciphered (21 of 26 letters exactly ten times; chi-squared 1.251 on 25 df; P = 9.3e-13). The
objects themselves cannot date from 1933. Neither argument depends on the other.

Also worth recording: Pelling and Bret Bowen independently found the same flat letter distribution we did,
so the statistical result is reproduced. What this repo adds is the calibration - the Monte Carlo null that
turns "looks flat" into a p-value, and the demonstration that 0 of 200,000 random strings are this uniform.

## Transcription checked against the photographs (2026-09-15)

The statistics above were computed on McCurley's transcription as published, and the first version of this
note waved the five deviations away by quoting his caveat. That was an assumption. It has now been checked.

McCurley's page carries fifteen photographs (images 5.1 to 13.2; the four already in this directory are
`bar9.1`, `bar10.1`, `bar11.1`, `bar12.1`). Seven carry Latin lettering: 5.1, 7.2, 9.1, 10.2, 11.1, 12.1 and
13.1. The other eight show only the cursive signatures and portraits. Every text block on the seven was cut out,
enlarged three to four times and contrast-stretched, and read against the sixteen strings. The bars are casts
with raised lettering about 12 px high in the 1152 px scans, so a letter is legible when the cast is clean and
not otherwise; most strings appear on three or more bars, which is what makes the check possible.

| string | letters | bars where read | result |
|---|---|---|---|
| SKCDKJCDJCYQSZKTZJPXPWIRN | 25 | 5, 10 (three times), 13 | matches |
| MQOLCSJTLGAJOKBSSBOMUPCE | 24 | 9, 10 (three times), 11, 13 | matches |
| RHZVIYQIYSXVNQXQWIOVWPJO | 24 | 9, 10 (twice), 13 | matches |
| FEWGDRHDDEEUMFFTEEMJXZR | 23 | 9 (twice), 10 (twice), 11, 13 (twice) | matches |
| XLYPISNANIRUSFTFWMIY | 20 | 5, 11, 13 | matches |
| HFXPCQYZVATXAWIZPVE | 19 | 5, 9, 11, 13 | matches |
| YQHUDTABGALLOWLS | 16 | 5, 7, 9, 13 (twice) | matches |
| **UGMNCBXCFLDBEY** | 14 | 5, 7, 12 | **13 letters on all three bars.** Bar 12 (the largest, clearest cast) and bar 5 read `UGMNCBXCFLDEY`; bar 7 could be read `UGMNCBXCFLDBY`. McCurley evidently kept both candidate letters |
| ABRYCTUGVZXUPB | 14 | 5, 7, 11, 13 | matches; the V is clear on bar 5, but the same position on bar 11 is cast as a Y-shaped glyph |
| JKGFIJPMCWSAEK | 14 | 5, 7, 10, 13 | matches |
| **KOWVRSRKWTMLDH** | 14 | 5, 7, 9, 13 | the K after RSR is not visible on bars 5, 7 or 13, which read more like `KOWVRSRWTMLDH` (13); the casts are too coarse there to be sure either way. Unresolved |
| HLMTAHGBGFNIV | 13 | 7, 9, 11 (twice), 13 | matches |
| MVERZRLQDBHQ | 12 | 7, 9, 11 | matches |
| VIOHIKNNGUAB | 12 | 5, 7, 9, 11 | matches |
| GKJFHYXODIE | 11 | 5 (twice), 7, 11 | matches |
| ZUQUPNZN | 8 | 5, 7, 9, 11, 13 (twice) | matches |

So fourteen of sixteen strings are confirmed letter for letter, one is a letter shorter than published, and one
has a single letter in doubt. The three "extra" letters over 260 are not, as the first draft of this note
assumed, five independent misreadings that would vanish on a better scan. Some of the deviations are on the
bars. I is 13 on every reading; the I-heavy strings (RHZVIYQIY..., XLYPISNANI...) are clear on bars 10 and 13.

Counts under each defensible reading (`python readings.py`):

| reading | letters | exactly ten | off by | chi-squared (25 df) | P |
|---|---|---|---|---|---|
| McCurley 1996 as published | 263 | 21 | E+1 I+3 O-1 S+1 T-1 | 1.251 | 9.3e-13 |
| H = UGMNCBXCFLDEY | 262 | 20 | B-1 E+1 I+3 O-1 S+1 T-1 | 1.374 | 2.8e-12 |
| H = UGMNCBXCFLDBY | 262 | 22 | I+3 O-1 S+1 T-1 | 1.176 | 4.4e-13 |
| H = ..DEY, K without second K | 261 | 19 | B-1 E+1 I+3 K-1 O-1 S+1 T-1 | 1.490 | 7.4e-12 |
| H = ..DBY, K without second K | 261 | 21 | I+3 K-1 O-1 S+1 T-1 | 1.291 | 1.4e-12 |

The conclusion does not move. Under every reading the chi-squared sits between 1.2 and 1.5 where random
sampling predicts 25, and the probability of a random 261 to 263 letter string being this flat stays near one
in a trillion. What changes is the wording: the bars carry *about* ten of each letter, with a few letters
genuinely one off and I genuinely three over, not *exactly* ten with a noisy transcription. That is still
something only a hand laying out letters produces; a person counting out ten of each and losing track by one
or two is exactly the pattern.

Working files: the fifteen downloaded images and the crops are in `work/` (ignored by git); the four bars
already tracked are enough to re-check H (bar 12) and the confirmed strings.
