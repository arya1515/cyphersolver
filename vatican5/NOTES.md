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
