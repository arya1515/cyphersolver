# Chinese "gold bar" cryptograms, Shanghai 1933 — not an encryption

Source: Kevin McCurley's 1996 IACR page, <https://www.iacr.org/misc/china/> and its
<https://www.iacr.org/misc/china/cryptograms.html>. Seven bars allegedly issued to a "General Wang" in
Shanghai in 1933, said to certify a bank deposit of over $300,000,000. Sixteen distinct strings of Latin
letters, 8 to 25 characters, 263 letters in all, reused across the bars. Listed by Elonka Dunin among the
famous unsolved ciphers.

## Result

**The inscriptions are not enciphered text of any kind.** The corpus is a deliberately constructed uniform
letter multiset: *exactly ten of every letter of the alphabet*, with five one-off deviations that McCurley's
own caveat already covers ("some of the letters are hard to read so there may be inaccuracies").

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

Reproduce: `python analyse.py` (corpus is in `corpus.py`; needs numpy/scipy).

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
