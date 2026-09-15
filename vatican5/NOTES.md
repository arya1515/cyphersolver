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

## 2026-09-15, third attempt: the two-digit-syllable prior also fails

New structural lead from re-reading Meister key no. 1: there the dot sits on the *antecedent* and selects a
four-member syllable series, so the digits that *follow* a dot are the series slots (a, e, i, o). In IA-2
those following digits are {2, 0, 7, 5}, which would make them the vowel slots and predict that much of the
text is two-digit syllables of the form (consonant lead)(vowel from {2,0,7,5}).

Tested directly, segmenting on the null 4:

| prediction | observed |
|---|---|
| {2,0,7,5} concentrated at alternate positions | even positions 0.587, odd positions 0.582 — no difference |
| word segments mostly even length | 280 even against 201 odd — no preference |

So the syllables are not laid out as fixed two-digit units in a regular phase. Together with the earlier
results (Meister keys 1-3 rejected by likelihood; trigram partition search recovers synthetic keys of the
polyphonic design but fails on the real text in both Italian and Spanish) the picture is of a
**variable-length code** mixing one- and two-digit groups, very likely with heavy nomenclature — which is
exactly the case no letter-level model can identify, and is consistent with Lasry, Megyesi and Kopal having
left it unsolved.

Remaining idea, untested: the fraction of the text that is nomenclature (arbitrary groups for words and
names) may simply be too large for any statistical attack, in which case the cipher needs the key itself
rather than cryptanalysis.

## 2026-09-15, fourth attempt: the model class is now excluded by a matched control

### A real structural finding first

Italian words end in a vowel about 97% of the time, so word-final enrichment (final rate divided by
overall rate) should separate vowel-bearing digits from consonant ones. Measured over the 481 segments
delimited by the null 4:

```
  1: 1.79   7: 1.76   3: 1.52   0: 1.49  |  6: 1.01  |  9: 0.64   2: 0.58   5: 0.25   8: 0.08
```

Digit 8 ends a word at one twelfth of its overall rate; digits 1, 7, 3, 0 are all enriched. And the
frequency masses of that split match Italian independently, to three decimals:

| group | cipher mass | Italian target |
|---|---|---|
| {7, 0, 3, 1} | 0.476 | all five vowels, 0.479 |
| {8, 5, 2, 6, 9} | 0.524 | all consonants, 0.521 |

Two independent signals agreeing. **The vowel-bearing digits are {7, 0, 3, 1}.** This is the first
positive structural result on the cipher beyond the null.

### The constrained search, and why it still fails

`vc.py` repeats the trigram partition search with vowels restricted to {7,0,3,1} and consonants to
{8,5,2,6,9}, cutting the space from 9^21 to 4^5 x 5^16 and removing vowel/consonant confusions. 24 runs:
still 24 different keys, mean Rand index against the best **0.861** where chance *in the same constrained
space* is **0.799**. The runs do not even agree on which vowel sits on which digit.

### The matched control settles it

`vc_syn.py` builds a synthetic ciphertext with exactly the structure the real one is believed to have --
real Italian plaintext, same 21-letter alphabet, same vowel/consonant digit split, same polyphony (16
consonants over 5 digits), same null density, same length of 6553 digits -- and runs the identical search.

```
TRUE KEY   7=i 0=o 3=u 1=ae 8=cdgv  5=fhr 2=lst 6=bpq 9=mnz
BEST RUN   7=i 0=o 3=u 1=ae 8=cdgvz 5=fhr 2=lst 6=bpq 9=mn
```

Recovery of the true key: **0.97** (one letter misplaced), and the search even beat the true key's own
likelihood, so it found the optimum. Agreement between independent runs: 0.90. Replicated on a second
seed: recovery 0.93, agreement 0.89.

| | agreement between runs | recovers a key? |
|---|---|---|
| synthetic, same design | 0.90 | **yes, 0.97** |
| real ciphertext | 0.86 (chance 0.80) | no |

**So the method works at this polyphony, this length and this alphabet. The real ciphertext is therefore
not a polyphonic single-digit substitution of Italian.** This is no longer "we could not find the key"; it
is "no key of this kind exists to find".

### Where that leaves it

The word-final evidence says parts of the text behave like Italian letters with a vowel/consonant
structure. The failure of every letter-level model says parts of it do not. The reading that fits both is a
**mixed cipher**: polyphonic single digits for letters, interleaved with multi-digit groups for syllables,
words and names, and no marking to say which is which. Only about 6% of positions carry dots, far too few
to be the code markers, and the searches already exclude dotted contexts.

That is precisely the construction no statistical attack can resolve, and it explains why Lasry, Megyesi
and Kopal left this one unsolved while reading the rest of the collection. The route in is the key or a
matching plaintext in the Farnese correspondence, not cryptanalysis.

Reproduce: `python vc.py <seed>` (constrained search), `python vc_read.py consensus` (convergence),
`python vc_syn.py <seed>` (the matched control).

### The mixed lattice model, with the constraint, also fails

The C# lattice solver (`native/vsolve.exe`) already supports `--null`, `--vowdig` and `--consdig`, so the new
structural finding could be fed straight in: `--null=4 --vowdig=7031 --consdig=85269 --wcoef=3`. No previous
run had the right values. Four seeds, 120k iterations each.

The decodes *look* far better than anything before — real 16th-century vocabulary, `cosa`, `con la`, `et`,
`regno`, `imperatrice`, `figlia`, `signore`, `chiesa` — instead of the `che/non/per` loops the earlier runs
collapsed into. That appearance is worthless, and here is why.

**Dictionary coverage cannot judge itself.** The solver optimises coverage directly (`--wcoef`), so it will
manufacture Italian-looking words from any key. Calibrated at minlen 5 / top 5000:

| text | coverage |
|---|---|
| genuine Italian prose | **0.248** |
| constrained runs (vcn_1..4) | 0.204 – 0.232 |
| an earlier unconstrained run (nat_c4) | **0.279** |

An earlier run scored *higher than real Italian*. The metric is gameable and every "promising" coverage
number in this project's history should be read in that light.

**Convergence is the test the solver does not optimise, and it fails it.** Across the four constrained runs:

* only 1 to 3 of the 10 digits carry identical letter sets in any pair;
* pairwise Rand index over letter groupings 0.84 – 0.87, against the 0.80 chance level for this space;
* the runs disagree about which vowel sits on which digit (7 = i, i, a, i; 0 = a/u, e, i, a).

So the mixed model with polyphonic singles plus two- and three-digit codes is no more identifiable than the
pure letter model. The vowel-bearing *set* {7,0,3,1} is solid; the individual assignments are not
recoverable from 6553 digits at this ambiguity.

### Status

Unsolved, and now for a documented reason rather than for want of trying. Four model classes tested, two of
them against matched synthetic controls that the same code solves correctly. The cipher needs its key, or a
matching plaintext in the Farnese correspondence.

## 2026-09-15, fifth attempt: the level is settled, and so is why this one resisted

Resumed with a directive to solve it. It is still not solved. But the session produced the first
positive structural results since the vowel set, a third independent confirmation of that set, and -
more usefully - an explanation of why the sibling cipher fell and this one did not.

### The finding that matters most is not cryptanalytic

Part 4 of the same challenge series is ASV Portugal IA-1, and it was solved. Compare the two
transcripts as delivered:

| transcript | single spaces between digits | **double spaces** |
|---|---|---|
| Portugal IA-1 (Part 4, solved) | 7603 | **3210** |
| Spain IA-2 (Part 5, this one) | 6412 | **6** |

The Portugal transcriber recorded the scribe's word division; the Spain transcriber did not. The
division exists on the parchment - sixteenth-century chancery clerks grouped their cipher digits -
but it is absent from the only transcript in circulation. Every attack mounted here and, presumably,
by everyone else has been run on a stream with its word boundaries deleted. That is a large part of
the difficulty asymmetry between Part 4 and Part 5, and it is fixable only from the images.

### One key, not several

A page-by-page comparison of digit distributions against the document mean gives chi-squared between
3.4 and 12.6 on 9 degrees of freedom across the six substantial pages. Nothing approaches
significance, so the whole of ff. 70r-73v is in a single key. The "mixed keys" explanation for the
failure is excluded.

### Three structural results, each against a control

**Segment lengths prefer even.** The stretches between the null 4 run 278 even against 202 odd,
chi-squared 12.0 on 1 df. The fourth attempt looked at this and recorded "no preference"; that was
wrong, and it matters, because it is the signature of two-digit units.

**There is a real two-digit phase.** Inside those stretches the digit distribution at even offsets
differs from the one at odd offsets: chi-squared 39.4, against a null of 8.3 +- 4.1 built by
shuffling each segment, z = +7.6. Digit 9 sits at even offsets 1.60 times as often as odd, digit 8 at
0.84.

**Doubled digits are suppressed without exception.** All ten, and some severely - 00 occurs 6 times
against 117 expected, 44 twice against 35, 99 twice against 21. Six ordered pairs are suppressed
below an eighth of expectation; 400 shuffles of the same digits produce a mean of 0.01 such pairs and
never more than 1.

### The word-final units, and a third confirmation of the vowel set

Scanning every n-gram for enrichment immediately before a null gives two dominant word endings:

| unit | occurrences | before a null | p |
|---|---|---|---|
| **27** | 265 | 86 | 7.4 x 10^-33 |
| **80** | 349 | 82 | 4.2 x 10^-21 |
| 73 | 222 | 38 | 9.8 x 10^-7 |
| 37 | 73 | 17 | 1.7 x 10^-5 |

Every enriched ending terminates in a digit from {7, 0, 3, 1}. Italian ends about 97% of its words in
a vowel, so this is a third independent line - after word-final enrichment of single digits and after
the frequency masses - agreeing that those digits are the vowel-bearing ones. **{7, 0, 3} is now solid
on all three.**

### But the level is not letters, and that is now demonstrable

If each digit stood for one letter, the alternation of vowel-digits and consonant-digits would have to
look like the alternation of vowels and consonants in Italian. It does not:

| | cipher | period Italian |
|---|---|---|
| vowel share | 0.475 | 0.464 |
| mean vowel run | 1.604 | 1.301 |
| mean consonant run | 1.769 | 1.504 |
| consonant runs of 3 or more | **0.183** | **0.059** |

The share matches and the runs do not. Runs three times too long are what you get when letters are
sometimes written as two digits of the same class.

Worse for the letter model, the three tests disagree about which digits are the vowels. Frequency mass
picks {7,0,3,1}; a search over all subsets for the best match to Italian's run profile picks
{0,2,3,7}; the final-digit distribution picks {7,0,3,6}. All three agree on {7,0,3} and contradict
each other on the fourth. **No single letter-level assignment satisfies all three**, which is what one
expects when the units are not letters.

### The repetition says codebook

| | real | shuffle of its own digits |
|---|---|---|
| repeated 7-grams | **441** | 5 |
| repeated 8-grams | **244** | 0 |

And greedy byte-pair encoding, which lets the text name its own units, separates the real text from
both controls - compression gain +1.6% for the cipher, **-8.2% for genuine Italian pushed through a
polyphonic single-digit cipher of the believed design**, -14.0% for a shuffle. The units BPE recovers
are 15% one digit, 32% two, 29% three: a variable-length nomenclator, not a fixed grid.

### Arithmetic that now hangs together

6068 non-null digits over 480 segments is 12.64 digits per segment. If units average two digits that
is about 3000 units; at roughly 2.3 units per word that is about 1300 words of some 4.6 letters, which
is ordinary Italian and consistent with four folios. The null therefore marks about 37% of word ends,
not all of them - which is why the segments are far too long to be words.

### Status

Not solved. The model is now pinned much more tightly than before: **a variable-length syllabic code,
mostly two-digit units over vowel-bearing digits {7,0,3}+ and consonant-bearing {8,5,2,6,9}-, with 27
and 80 as the dominant word-final units and 4 as an intermittent word null.** What is missing is not
another search. It is the word division, which exists in the manuscript and was dropped in
transcription, or the key, or a matching plaintext.

New files: `phase.py` (parity and phase), `escape.py` (suppressed pairs, after Lasry's dictionary
escape in the sibling cipher), `units2.py` (unit inventory), `bpe.py` (unsupervised units with
controls), `cvtest.py` (the vowel/consonant run test).
