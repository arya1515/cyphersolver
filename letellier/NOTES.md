# Le Tellier -> Marquis de Castelnau, 12 May 1657 — tracker item #15

Ciphertext: cryptiana transcription `LeTellier_Castelnau1657.txt` (202 tokens after "le dessein de Sa Majesté
estant"); image `LeTellier1657.jpg`. Three numeric classes (plain 3-72, macron 2-53, double-prime 12-48) plus
letter tokens (a c l p f t m h o q, h- ss J- x- y- z- m- p-, ap rp ff oo tt, &). Most frequent: ~28 (9), 13 (6),
20 (6), ~3, ~23, ~30, l (5 each).

Tried 2026-09-15:
- Le Tellier-Colbert Cipher 2 (Dec 1650) table applied directly: gibberish.
- Hypothesis from Ciphers 1/1A (alphabetical CV syllabary at consecutive numbers, one offset per class), exhaustive
  offsets -20..79 per class scored with the French quadgram LM (`offsets.py`): best -6.24/quadgram = noise.
Verdict: skipped. Too short for an unconstrained syllabic solve; the 1657 table is not a simple alphabetical run.
Would need a Lasry-style syllable-cipher solver plus a known-plaintext (the King's instructions of the same date
may be the plaintext summary — worth checking in the Le Tellier papers, BnF fr. 4187 ff. / SHD A1 series).
