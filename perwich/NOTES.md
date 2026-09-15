# William Perwich to Lord Arlington, Paris, 9 April 1670 — it is not a transposition

TNA SP 78/129 f.180, published by the National Archives in August 2025 and transcribed by Satoshi
Tomokiyo. Roughly 500 cipher cells laid out as a grid across two manuscript pages, embedded in an
otherwise plain English despatch about the Dauphin's christening, the droit d'aubaine, and the King's
forthcoming progress.

Everyone has read it as a transposition. The TNA blog presents it that way; Tomokiyo's own post is
titled "an undeciphered **transposition** cipher"; this project's tracker repeated the guess and added
"possibly one of Morland's".

**Two independent tests say it is not.**

## What the cells tell you before any analysis

Alongside single letters the grid holds **ye**, **yt**, **wt** and **ym** — the standard early-modern
abbreviations for *the*, *that*, *with* and *them* — bare numbers (40, 60, 61, 96, 97, 192, 910), a few
odd groups (QR, Rom, nd, pa, rq), and, as the very last cell, the plain English word **likelyhood**.
So the plaintext is English of 1670 and there is a small nomenclature in play.

## Test 1: the frequency profile is a substitution signature

| | observed | English, ~500 letters |
|---|---|---|
| index of coincidence | 0.0629 | 0.0667 (random 0.0385) |
| chi-squared **in place** | **154.7** | about 25 |
| chi-squared **sorted** | **8.7** | about 12 |

A transposition moves letters about but leaves each one as itself, so its in-place chi-squared is
ordinary. This one is six times too large. Meanwhile the sorted profile — the frequency shape with
the identities discarded — fits English *better* than a typical English sample of the same length.
Identities scrambled, shape preserved: that is substitution.

The language is English and not close: sorted chi-squared 11.0 for English against 43.9 for French
and 72.2 for Latin, which matters because the writer was in Paris.

One detail supports the transcriber. Tomokiyo notes in his own file, "I'm still wondering whether 'U'
is actually 'll'". Reading his U as a doubled l improves the sorted fit from 11.0 to **8.7**, and it
moves the two worst outliers — l far too rare, u far too common — in the right direction at once.

## Test 2: there is no transposition signal at all

Repeated digrams survive a substitution but are destroyed by a transposition, so a columnar key can be
hunted without knowing the substitution: hill-climb the column order to maximise digram repeats. Done
for every period from 4 to 24, and repeated on **shuffles of the same letters** as a control:

```
period    4    8   12   16   20   24
real    260  267  270  278  283  284
shuffle 258  270  274  275  281  287
```

The scores rise with period on random data exactly as they do on the cipher. This is overfitting, not
a key. There is no transposition.

Three further attacks failed consistently with that: reading down the transcribed columns, annealing
the column order against an English model at every period, and ten reading routes over the grid and
over each page separately.

## But it is not a simple substitution either

Twelve restarts of a quadgram hill-climber over monoalphabetic keys reach −3227 where real English of
this length scores −2076, and the top two keys agree on **6 of 26** positions. No convergence.

## Reading

A **homophonic substitution, or a substitution with nomenclature** — which is precisely what English
diplomatic practice of 1670 used, and what the bare numbers and letter-groups in the grid look like.
The grid layout is how the clerk wrote it out, not the cipher: the transcribed rows run from 21 to 28
cells, which no rectangular transposition produces.

That is a correction to the published framing rather than a solution, but it redirects the attack.
The next step is a homophonic solver with the nomenclator cells held out, not another transposition
search.

Reproduce: `python masc.py` (substitution attempt and calibration), `python routes.py` (route reads),
`python stream.py` (columnar periods), `python grid.py show` (the parsed grid).
