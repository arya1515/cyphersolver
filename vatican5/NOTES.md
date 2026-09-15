# Vatican Challenge Part 5 (MysteryTwister) — work in progress

Ciphertext: ASV Segr. Stato Spagna 1A/2 (Farnese → nuncio Poggio, Rome 15 Apr 1542), transcript
`ASV_i1025_SdS_Spain_IA-2.txt` from the MysteryTwister challenge (G. Lasry, 2019). 6553 digit tokens,
dots on some digits (`^.`), a few uncertain readings (`?`).

## Established facts (statistical)

| finding | evidence |
|---|---|
| digit **4 is a null / word separator** | bias-corrected I(x;y \| middle=4) = 0.030, identical to Italian across-word-boundary MI (0.028); every other digit 0.08–0.17 (letter-like). Only 482 of ~1100 word ends are marked. |
| 7 is *not* a null | I(x;y \| 7) = 0.153 |
| 8 and 5 never end words (5 and 16 of 482) | → consonant groups; 7, 0, 3 dominate word-final position (161/103/79) → vowel-carrying |
| top bigrams 80/57/27/03/73 are 3–5 % of all bigrams | far too frequent for 2-digit syllable codes → mostly single-digit polyphonic letters |
| dotted digits are mainly 7^ (107), 2^ (39), 0^ (33); the digit after a dot is 2/0/7/5 (~36 each) | matches Meister key no.1 mechanics (dot on the *preceding* digit selects a syllable series; 4 syllables) |
| Meister 1906 keys nos. 1–4 (pp. 176–177) as printed do not fit | tested |
| Lasry–Megyesi–Kopal 2021 §5.5: S1/IA-2 unsolved, "another key" than IA-1 | their 2-letters-per-digit polyphonic SA failed |

## Tools

* `parse5.py` — tokenizer; `mi3.py` — bias-corrected MI diagnostics; `sepwords.py d` — segments between digit *d*;
  `fitfreq.py` — fit letter groups to overall / word-initial / word-final marginals; `dots2.py` — dotted contexts.
* `build_it_lm.py` — period-Italian corpus from Nuntiaturberichte OCR (`nb_*.txt`, not in repo) → `it_ngrams.json`,
  `it_words.json`; `export_native.py` / `export_native_sp.py` → `lm5.bin` / `lm5sp.bin` (dense 5-gram tables).
* `native/Program5.cs` → `vsolve.exe` (C# 5, build with `csc.exe /o+ /platform:x64`): lattice/beam-Viterbi solver
  with simulated annealing + greedy sweeps over a key of polyphonic single digits, dotted singles, after-dot singles,
  2-digit and dotted 3-digit codes. Objective = 5-gram LM + KL(letter freq) + MDL code penalty + dictionary word
  coverage (`--wcoef`). See `--help`-less option list at top of `Main`.
* `make_syn.py`, `make_syn1.py` — synthetic ciphers (Meister key-2 / key-1 style) with known keys for testing;
  `syn_fix.py`, `syn1_fix.py` — `--fix` spec of the true key; `lmscore.py`, `wordscore.py`, `wordcov.py` — evaluate a decode.

## Lessons

* Fixed-length chunking split dotted 3-digit codes → true keys scored −8000 nats worse than garbage. Chunk
  boundaries now avoid dotted positions and a penalised skip transition exists.
* On a key-1-style synthetic the pure LM objective is **not identifiable** (a wrong key scores as well as the truth);
  dictionary coverage (words ≥5 letters, top-5000) separates them cleanly (0.52 vs 0.21).

## 2026-09-15 session (resumed)

* Dot mechanics re-derived from Meister p.176-177: key no.2 ("Cifra ultima con Mons. Poggio mandata per il
  Montepulciano") puts the dotted codes on 8x/0x (ta te ti to, qua que qui, che chi non, N.S., S.Mta), but in IA-2
  the digit after a dotted digit is 2/0/7/5 (~36 each) and the dotted digits are 7/2/0 → key-1 *type* (dot on the
  antecedent selects a 4-syllable series; dot on the digit itself another series), with {7,2,0,5} as the four
  "vowel" digits. Key 2 as printed rejected (trigram LL −49047).
* Key no.3 (Piacenza/Dandino 1545) has **Nulla 4** — same null as IA-2 — and vowel digits 2 5 7 9 0. Tested:
  trigram LL −44038 (search optima −39659, random best −45545) → rejected; the null coincidence is just that.
* New objective `bigramfit.py` / `trigramfit.py`: exact multinomial likelihood of the digit bi/trigram counts under a
  grouped Italian letter model (4 = boundary, dotted contexts excluded), SA over partitions of 21 letters into 9
  digits. Result: 24 runs → 24 different partitions with scores within 500 nats of each other (−39659 … −40157),
  Rand index vs best ≈ 0.85 (chance level). **The polyphonic single-digit model is not identifiable on this text**
  — consistent with the earlier 5-gram lattice failure and with Lasry–Megyesi–Kopal's failure.
* `decode_poly.py` — trigram Viterbi decode for any "d=letters" key; `consensus.py` — compare partitions.
* Hypotheses left: (a) plaintext not Italian (transcript tags some cleartext "SP" = Spanish) — being tested with a
  Don Quijote trigram model (`trigramfit_es.py`); (b) most digits belong to 2-digit syllable codes (key-2 style)
  so the letter model is wrong; (c) transcription noise.
* **Decisive diagnostics (2026-09-15):** synthetic control (`syn_tri.py`: 7000 Italian letters, random key-1-style
  polyphonic key, 45 % word ends marked with 4) → the trigram partition SA recovers the true key (2/3 runs exact up to
  b/z; score −40932 vs truth −40994). On the real cipher: 24 Italian runs and 12 Spanish runs (`trigramfit_es.py`,
  Don Quijote model) all fail to converge (Rand ≈ 0.87 = chance). **So IA-2 is not a plain polyphonic
  single-digit cipher in Italian or Spanish**; the digit stream must contain substantial multi-digit code content
  (key-2-style syllabary with other numbering), which no letter-level model can identify. Next attack would be a
  mixed model with explicit 2-digit syllable codes seeded by the key-2 layout (cX/dX/lX/mX/nX/rX/sX series) and
  dotted 4-series on {2,0,7,5}; the old C# lattice solver had this class but no structural prior.
