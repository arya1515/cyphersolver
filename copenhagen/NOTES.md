# Copenhagen cryptogram (Schmeh Top 50 no. 23) — attempted 2026-09-15

Three lines on a slip found, probably in the late 1950s, behind an 1835 portrait of a Danish general in a
Copenhagen military museum, sent to the American Cryptogram Association and never solved or written up
there. Klaus Schmeh received a scan from ACA member Kent Ramliden (a Swede in Florida, died 2016) and
published it in January 2015 (German), August 2017 (Top 50 no. 23) and October 2021 (German and English
"cold case" posts). Museum, general and finder are unknown. Sources: the three Cipherbrain posts and their
comments; the only image in circulation is the 614 x 147 px scan `Danish-General-Cryptogram.jpg`.

## Transcription

`cipher.txt` is this session's reading from the scan upscaled 4x and 6x per half-line; `cipher_sw.txt` is
the 25-symbol reading posted by "ShadowWolf" in the comments of the October 2021 German post. The two
agree symbol for symbol except that ShadowWolf splits what I merged: the backslash with a dot after it
from the backslash with dots on both sides, the slash with a trailing dot from the slash with a leading
dot, the small raised double tick after the first caret pair, four caret shapes (a tall lambda-like one
opening line 1 and closing line 3, a small one, one with a trailing dot opening line 2, and one after the
zero in line 2), and he reads the second tall stroke around "13" in line 3 as the digit 1. With those
splits the symbol count is 25, which is Schmeh's figure; merged it is 20. Both readings were attacked.

Counts (merged reading, 103 symbols plus 4 long strokes, counted mechanically from cipher.txt): 3 x16, backslash-dot x14,
n x13, slash-dot x8, free dot x8, caret x6, + x6, o x5, 2 x5, 0 x5, v x4, 9 x3, 1 x2, 8 x2, 7 6 X ṅ or-glyph double-tick x1.
Digits 4 and 5 never occur. The letter o occurs five times and every time directly after n ("no3", "no9",
"+no", "non", "non3"); "non" occurs twice in line 3. The doubled pair "vv" occurs once.

## Attack

`solve.py`: character 5-gram language models built from Gutenberg texts in Danish, Swedish, Norwegian,
German, Dutch, French, English, Latin, Icelandic and Finnish (0.6 to 2.4 million letters each, corpus not
in the repo; fetch with the Gutendex API, ids in the session log), simulated annealing over an injective
symbol-to-letter map with 60 to 80 restarts, the long strokes treated as sentence boundaries, and the top
candidates re-ranked by dictionary coverage, which the annealer does not optimise. Conventions tested on
the merged reading: free dot as a letter, dropped, as a boundary, or fused to the following stroke; the
long stroke as a letter; the dotted n merged with n. `solve_sp.py` tests the hypothesis that the two
dotted strokes are word separators (which would give 22 words averaging 3.7 letters) with a space-aware
model and whole-word hits. The 25-symbol reading was run as is.

Result: nothing readable in any language under any convention. Best per-letter scores:

| language | best score per letter (any convention) | what it looked like |
|---|---|---|
| Latin | -2.69 | fxsisted tine togeteom scie ... |
| Danish | -2.77 | junindel dige dskedesf ... / ... udstødes ... velsigne ... |
| Norwegian | -2.81 | bærersag sena stjasatm ... |
| Swedish | -2.81 | honensam sera stfasatv ... |
| English | -2.88 | cydidsea sine stbesetf ... |
| German | -2.93 | uchthien itze irbeierm ... |
| French | -2.97 | chiailes lape ltbeletr ... |
| Dutch, Icelandic, Finnish | -3.07 to -3.30 | |

The word-separator hypothesis scores -4.6 per letter under the spaced model (real text about -2.3) and
yields only isolated Danish words: "er", "elle", "unge", "død", "døde". The last two come from the n-o-n
pattern with n = d, o = ø, 3 = e, which also turns "no3" into "døe", the pre-1900 spelling of "dø". It is
the one suggestive fragment in the whole search and it does not extend: the rest of that reading is noise.

## The control that makes the negative result mean something

`control.py`: passages of 103 letters with three sentence breaks, drawn at random from the same corpora,
enciphered with random simple substitutions of about 20 symbols, attacked with the identical solver.

Three trials per language, 40 restarts each (the real cryptogram got 60 to 80, then 300):

| language | letters in key | accuracy | score found / true text |
|---|---|---|---|
| Danish | 19, 19, 18 | 0.99, 0.99, 0.99 | -1.99/-1.85, -1.93/-1.96, -1.85/-1.76 |
| German | 22, 19, 22 | 0.96, 0.79, **0.14** | -1.88/-1.78, -2.64/-1.75, **-3.42/-1.81** |
| English | 20, 21, 20 | 1.00, 0.99, 1.00 | -1.44/-1.44, -1.99/-1.85, -1.67/-1.67 |
| Latin | 18, 18, 19 | 1.00, 1.00, 0.99 | -2.09/-2.09, -1.74/-1.74, -1.87/-1.72 |
| Swedish | 22, 22, 22 | 1.00, **0.05**, 1.00 | -1.95/-1.95, **-3.49/-1.59**, -1.99/-1.99 |

Twelve of fifteen are recovered essentially completely; the true text always scores between -1.4 and
-2.1 per letter. Two trials fail outright and one partly, and in each case the true key would have scored
far better than what the annealer found: these are search failures at 40 restarts, most likely with
22-letter keys, and they show that a single failed run on the real text would prove nothing. That is why
the strongest candidate languages were rerun with 300 restarts on both readings (table below). The
cryptogram never scores better than -2.7 in any language or under any reading. So either it is not a
simple substitution of a text in these ten languages, or the transcription conflates or splits letters in
a way that both independent readings share. Danish, the default assumption since 2015, fits no better than
Latin or Norwegian. Matthew Brown's Danish quadgram hill-climb reported in the 2021 comments came to the
same nothing.

## 300-restart confirmation

Best per-letter score with 300 restarts (seed 5), merged reading in the `full` and `nodot` conventions and the
25-symbol reading; the `dotattach` runs were still going when this was written and had not beaten these:

| language | merged, full | merged, no dot | 25-symbol reading |
|---|---|---|---|
| Latin | -2.90 | -2.82 | -3.16 |
| Danish | -3.04 | -2.90 | -3.16 |
| Swedish | -3.17 | -2.99 | -3.20 |
| Norwegian | -3.12 | -3.01 | -3.17 |
| English | -3.20 | -3.13 | -3.28 |
| German | -3.29 | -3.32 | -3.46 |

Five times the restarts move nothing: the same ceiling, 0.7 to 1.4 nats per letter below what genuine text
of this length scores in every one of these languages. Search failure is excluded as the explanation.

## Status

Not solved. Closed from the scan that exists. Routes that would reopen it: the original slip or a better
scan (the ACA received it from the museum; Ramliden's papers or the ACA archive), identification of the
painting (an 1835 portrait of a Danish general in Copenhagen points to the Tøjhusmuseet, now the Danish
War Museum), or the possibility, not testable here, that the strokes and dots are a shorthand or a private
code rather than letters, in which case no substitution model applies.
