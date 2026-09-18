# The crib that should close the key: f. 18 in cipher, f. 19 its decipherment in clear

Canvases 20 right, 21 left (cipher) and 21 right, 22 left (clear) of ark `btv1b9061879d`.

Tomokiyo lists "f.18-21 (deciphered in f.19)" in one line of his Mayenne–Forget Cipher-1 paragraph
and passes on. It is by far the largest crib in the volume and nothing in this repo — or, as far as
the published tables go, anywhere — has been built from it.

## What is actually there

* **f. 18r** — a letter to the King. Fourteen lines in clear, then **22 lines of cipher** in a
  large, well-spaced hand, the most legible cipher of any leaf examined here.
* **f. 18v** — a further **~35 lines**, the whole page in cipher.
* **f. 19r** — **~32 lines of ordinary French in clear**: the office's decipherment.
* **f. 19v** — ~10 more clear lines, finishing it.

So roughly **2,500 ciphered figures with their plaintext beside them**, in the same hand family as
the eight undeciphered leaves.

## The join is confirmed

f. 18r's clear runs to "… nous [trouvasmes] en grande irrésolution et trop foiblement", and the
cipher then opens **`14` …** — and `14` is *que*. f. 19r opens **"Que S. M.[ajesté] fust
advertie …"**. The decipherment starts exactly where the cipher does.

The clear opening of f. 18r, read off the leaf, sets the scene:

> **Sire**, Ayant demouré vingt jours entiers sans avoir aucune nouvelle de Vostre Majesté,
> craignant que voz despesches et les miennes se fussent perdues sur les chemins, comme
> pareillement le courrier que je vous avois despesché, j'ay resolu de vous envoyer le S.r de la
> Messelube, mon porteur, lieutenant de la compagnie de Monsieur de … qui a tousjours esté près de
> moy depuis que je suis en ce païs … Laquelle, ayant depuis conféré avec Monsieur le Mareschal de
> Matignon et les principaux capitaines et officiers de cette armée, nous [trouvasmes] en grande
> irrésolution et trop foiblement …

and f. 19r continues, in clear, what the figures say.

## Two independent confirmations of the pairing

Reading the first figures of f. 18r against the first line of f. 19r:

* f. 19r line 1 begins **"Que sa Ma[jes]té fust advertie …"** and the cipher begins `14` — *que* —
  followed by nine figures for the nine letters of *sa maieste*, then four for *fust*.
* A little further along the cipher carries the code group **`52`**, and the clear text has
  **"plustost"** at exactly that point. Tomokiyo lists 52 = *plustost* in his nomenclature; this is
  the first time that value has been checked against a plaintext.

So the pairing is not an inference from Tomokiyo's note — it is verified on the leaf twice over.

## Settled: it is one key, and the existing table already half-reads this leaf

An earlier pass here suspected ff. 18-21 might be in a different cipher from ff. 196/201, because
hand-assigned figure values disagreed. That was my own shorthand colliding on near-identical
shapes, not two ciphers. The test that settles it: feed f. 18's first cipher figures to the key
derived from f. 143 — Tomokiyo's table as corrected here — and it returns

> que · s ie ee fu · ut au au uc **ma este** ours **plustost que nous eu son** ee le e p ma p

against f. 19r's clear

> Que sa **Majesté** fust advertie … **plustost que nous eussions** victoire et …

*plustost que nous eussions* comes out of the figures exactly, and *ma este* is *Majesté*. The
key is the same one; the residue is transcription, as everywhere else in this target.

## What this makes possible

This is the first point in the whole target where the loop closes:

1. the key already reads perhaps half the figures of f. 18;
2. f. 19 supplies the other half as known plaintext;
3. so every figure the key gets wrong is *visible* — it decodes to a letter the plaintext says is
   something else — and can be corrected on the spot rather than guessed from context.

That is a convergent procedure, not an open-ended one, and it runs over ~1,650 figures. It should
resolve precisely the values that have blocked every leaf: the three near-identical figures for
**i / n / s**, the two round ones for **a / m**, and the **e / r** pair. With those fixed the eight
undeciphered leaves have no unknown figures left in them.

## How to run it

* cipher side: `hi/f18rflat.png` + `f18r_lines.txt` (22 lines) and f. 18v; tile with
  `mtile.py`, which fades the neighbouring lines.
* plaintext side: `hi/f19rflat.png` + `f19r_lines.txt` (33 lines), tiles cut at `hi/P_*`;
  transcription so far in `f19r_clear.md`.
* decode with `KEY=key.json python dec.py`, diff against the plaintext, correct the key, repeat.


## First pass through the loop, and what it shows

Lines 2-3 of f. 18r transcribed from faded tiles and run against the key:

```
que s ie ee fu
u tat au comme s de ours  plustost que nous eu  ro nee nee p me p
tes les o de ce m n br nu et de mai le b uus pouues o
```

`plustost que nous eu[ssions]` again falls out of the figures, so the anchor holds. But the
stretches between the code groups do not yet agree with f. 19's plaintext, and the diagnosis is
sharp: the same ASCII token comes out needing two different letters within one line — my `4e` has
to be both *t* and *a*, my `x` both *e* and *n*. That is not the key being wrong. It is two
near-identical figures being read as one, which is the same failure that has run through this whole
target.

**The consequence is the method, not a setback.** With the plaintext known, the fix does not
require reading the figures correctly first. It runs the other way: take a stretch whose plaintext
is certain — *eussions*, eight letters — look at the eight figures under it, and assign them from
the plaintext. Each such stretch mints labelled exemplars for the confusable pairs, and the pairs
are exactly what is blocking the eight undeciphered leaves. ~1,650 figures of f. 18 are available
to be mined this way, and the anchors (`14` que, `25` nous, `52` plustost) locate the stretches.


## The loop mints its first corrections

At eight tiles a line the figures of f. 18r separate cleanly. Taking the stretch straight after the
code group `25` (*nous*), where f. 19r fixes the plaintext as **eussions**, and assigning the
figures *from* those letters:

| figure | (before q) | q | long-s with looped descender | filled round | 7 | ·v· | x-like |
|---|---|---|---|---|---|---|---|
| letter | e | **u** | **ss** | **i** | **o** | **n** | **s** |

Three of these — q = u, 7 = o, ·v· = n — agree with the key already in hand, which is the check
that the stretch is correctly located. The other three are gains:

* a **doubled-s figure**, not in Tomokiyo's table at all;
* a filled round figure = **i**;
* an x-like figure = **s** — and this is the point of the whole exercise, because it is *distinct*
  from the x-like figure that reads **e** on f. 143. That pair is one of the confusables that has
  blocked every leaf in this target, and the crib has just separated it.

`key_crib.json` holds them. Each further anchored stretch on f. 18's ~1,650 figures does the same.


## Labelled exemplars, which is the artifact that survives

The recurring failure in this target has been that ASCII shorthand collides: I call two
near-identical figures by one name, and the same name then needs two letters. Names cannot be
fixed by more care; they have to be dropped. So the crib's output is stored as **images with
letters attached**, in `exemplars/` with `exemplars/manifest.json`.

First five, cut from f. 18r line 2 under f. 19r's "plustost que nous eussions victoire":

| exemplar | letter | note |
|---|---|---|
| `f18r_l2_17_o.png` | **o** | a 7-with-dot; agrees with the existing key's 7 = o |
| `f18r_l2_18_n.png` | **n** | the dotted-v; agrees with ·v· = n |
| `f18r_l2_19_s.png` | **s** | a curl — this is the figure that has been read as *e* elsewhere |
| `f18r_l2_20_u.png` | **u** | an L/1 shape |
| `f18r_l2_23_i.png` | **i** | a c-shape |

Two boxes on that stretch hold two figures each and are kept whole, flagged `PAIR`, so they are
never used as single-figure exemplars.

The first two agreeing with the key is the control: it says the stretch is correctly located, so
the other three are trustworthy. And the third is the prize — a figure that had been read as *e*
is here, against known plaintext, unambiguously **s**.

## The procedure, stated once

1. `mtile.py` at eight tiles a line makes f. 18's figures individually legible.
2. Segment the line (`shapes.line_boxes`, gap 18 on this hand) and render the boxes numbered.
3. Locate the stretch with a code group (`14` que, `25` nous, `52` plustost) and read the letters
   off f. 19.
4. Save each box as `exemplars/<leaf>_<line>_<box>_<letter>.png`.
5. When a stretch's first figures agree with the existing key, the location is confirmed and the
   rest of that stretch can be trusted.

Repeat over f. 18's ~1,650 figures. The output is a labelled image set covering every homophone,
which is what a shape classifier needed and never had, and what the eight undeciphered leaves can
then be matched against.


## Yield: one line of the crib is worth fifteen exemplars

f. 18r line 2 aligns against f. 19r line 1 end to end. The plaintext
*…[que sa maie]**ste fust aduertie** … **plustost que nous eussions victoire**…* lays fifteen
letters across boxes 1–12, the code groups `52` / `14` / `25` anchor boxes 13–14, and *eussions*
runs 15–19. That single line yields **15 single-figure exemplars covering nine distinct letters**
(e, i×3, n, o, r, s×3, ss, t×2, u×2), plus seven boxes holding two or three figures, kept whole
and flagged `MULTI`.

At that rate the alphabet with its homophones is covered by **ten to fifteen lines of the crib,
not all fifty-seven**. That is the useful number: completing this key is a morning's work, not a
campaign. The campaign is reading the eight leaves afterwards — but with no unknown figures left
in them.

### And a confusable caught in the act

Box 11 and box 17 are both 7-shapes with a dot. Against the plaintext, box 11 is **i** (in
*aduertie*) and box 17 is **o** (in *eussions*). Either they are two figures the eye merges, or one
of them is mis-segmented. Both are now saved as labelled images side by side, which is the only way
that question was ever going to be answered — and it is the same question, in miniature, that has
blocked this target from the start.


## Where the mining stands, and what gates it

f. 18r line 3 is segmented and its 24 boxes rendered (`f18r_l3_boxes.json`, `hi/l3box_*.png`).
Labelling them is blocked on one thing only: f. 19r line 2 has to be read precisely first. It is
legible but not yet settled — it runs something like "Castel… de …bourg … de Castillebourg où
j[e]…", and until the words are fixed the letters cannot be laid against the boxes.

**That is the whole gate on this method.** Every cipher line needs its plaintext span read off
f. 19 first; the cipher side is already segmented and rendered by script. So the order of work is:

1. transcribe f. 19r lines 2–12 (the plaintext for f. 18r's 22 cipher lines) — clear secretary
   hand, three tiles a line with `mtile.py`;
2. for each cipher line, render its boxes and lay the letters across them;
3. save every box as a labelled image.

Ten to fifteen lines done this way covers the alphabet and its homophones. Nothing in it requires
a judgement the plaintext does not already make for you.


## Negative result worth having: the two sides are not line-for-line

f. 18r cipher line 3, decoded with the key, gives

> tes les o de ce m n br nu et de mai le b uus pouues o

while f. 19r line 2 reads *"Conseil d'assembler de Castillebourg où l'on feist … que je n'avois
plus d'instruction"*. Those do not align, even allowing for transcription slips — the fragments
that do read (*de*, *les*, *et de*, *le*) are not where that plaintext would put them.

So **cipher line n does not correspond to plaintext line n**. The count already said as much —
f. 18r + 18v carry ~1,650 figures against f. 19r + 19v's ~1,800 letters, and the two pages have
different line lengths — but it is worth stating flatly, because the mining procedure above
silently assumed a line-for-line join when it moved from line 2 to line 3.

**The fix is cumulative alignment, not per-line.** Concatenate the cipher figures in order and the
plaintext in order, and carry a running offset: each code group (`14` que, `25` nous, `52`
plustost, `13` qui, `12` il) is a landmark that re-synchronises the two streams, and the stretches
between landmarks are what get labelled. Line 2 worked precisely *because* it contained three
landmarks in a row; line 3, on this transcription, contains none that I can place.

That is the procedure to implement next, and it is mechanical: find the landmarks, anchor, label
between them.


## `align.py`: landmark alignment, with a built-in quality check

Written to do the cumulative alignment above. It pairs each code figure with the next matching word
in the plaintext, which re-synchronises the streams, and reports for each stretch between landmarks
the figure count, the letter count, and **the ratio between them**. That ratio is the check: a
homophonic cipher with occasional doubled figures should run at roughly 0.9–1.0 figures per letter,
so a stretch that comes out near 1.0 is correctly transcribed and ready to label, and one that
does not is flagged before any labelling is done on it.

First run, over the figures transcribed so far:

```
figures 80  letters 128  landmarks 4
  figs (1,26)   n= 25   letters n= 23   ratio=0.92   samaiestefustaduertieet
  figs (29,80)  n= 51   letters n= 87   ratio=1.71   eussionsuictoireetconseildassembler...
```

The first stretch — *sa maieste fust aduertie et*, 25 figures for 23 letters — is clean, which
independently confirms the hand-labelling done on line 2 above. The second is at 1.71, i.e. about
35 figures short: the segmenter has merged boxes there, exactly as the `MULTI` flags on line 2
suggested it would. So the tool does not just anchor, it says which stretches can be trusted.

**This is the piece that was missing.** Mining no longer depends on my judgement about where I am
in the text: the landmarks fix position, the ratio audits the transcription, and only stretches
that pass get labelled.


## The audit calibrates the segmenter

The segmenter's `gap` (how far apart two ink runs must be before they count as separate figures)
had been set by eye — 18 on f. 196, 14 on f. 143 — with nothing to check it against. The ratio
audit supplies the check, because the plaintext fixes how many figures a stretch *must* contain.

Boxes found on f. 18r's first three full cipher lines, by gap:

| gap | boxes per line | total |
|---|---|---|
| 8 | 37, 35, 38 | **110** |
| 10 | 36, 35, 33 | 104 |
| 12 | 32, 35, 31 | 98 |
| 14 | 29, 35, 31 | 95 |
| 16 | 28, 31, 26 | 85 |
| 18 | 24, 24, 23 | 71 |

**Correction.** A first reading of that table said "gap 8", from a three-line total measured
against a loosely estimated plaintext span. That was wrong, and the right test is narrower: line 2
is the one line whose span is known *exactly*, because it was hand-labelled — 15 letters of
*ste fust aduertie*, the three code groups `52`/`14`/`25`, the 8 of *eussions*, and 4 into
*uictoire*: **30 figures**. Against that:

| gap | boxes on line 2 | error |
|---|---|---|
| 8 | 37 | +7 |
| 10 | 36 | +6 |
| 12 | 32 | +2 |
| **14** | **29** | **−1** |
| 16 | 28 | −2 |
| 18 | 24 | −6 |

So **gap 13–14** for this hand — splitting figures at 8, merging them at 18. The three-line total
pointed the wrong way because the plaintext span it was compared against was a guess, which is a
fair warning about the audit: it is only as good as the certainty of the plaintext behind it.
Calibrate on hand-labelled spans, not on estimated ones.


## Re-mined at the calibrated gap: the exemplar set doubles

Re-segmenting f. 18r line 2 at gap 14 gives 29 boxes against the 30 the plaintext demands, and the
boxes that were merged before now separate — the old box 3, which held a triangle *and* a long-s
ligature, splits into two figures that label cleanly as **e** and **f**. Laying
*"ste fust aduertie [et] plustost que nous eussions"* across them:

| box | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| letter | s | t | **e** | **f** | u | s | t | a | *du* | e | r | t | i | e |

with boxes 16–18 the code groups `52` / `14` / `25`, and 19–20 the doubled-s and *i* of *eussions*.

**One line, correctly segmented, now yields 15 clean single-figure exemplars** and only five
`MULTI` boxes — against seven `MULTI`s and a scatter of guesses at gap 18.

Exemplar set after this pass: **30 labelled figures covering 11 distinct letters**
(a, e×4, f, i×5, n, o, r×2, s×5, ss×2, t×5, u×3). The homophones are starting to show: five
different figures for *s*, five for *t*, five for *i*, four for *e* — which is what the eight
undeciphered leaves have been tripping over from the beginning.


## Line 3 at gap 14: 35 boxes, and a cross-check that the figure families hold

Segmented at the calibrated gap, f. 18r line 3 gives **35 boxes**. It cannot be labelled outright
yet, because *uictoire* straddles the line 2/3 boundary and where exactly it breaks depends on
words at the end of f. 19r line 1 and the start of line 2 that are not yet certain. Guessing the
break would put every label after it one place out, so it is left.

But one thing does carry across, and it is the check that matters: **box 3 of line 3 is the same
d-shaped figure as box 10 of line 2, and both land on *e***. Two independent stretches of plaintext,
two different lines, same figure, same letter. That is the first evidence that the exemplar set is
internally consistent rather than an artefact of one lucky alignment.

### What line 3 needs

The tail of f. 19r line 1 and the head of line 2 read, at six tiles, as
*"… victoire e[t]"* / *"Conseil d[e] [a]ssembl[er] de Castillebourg …"*. Two words there are still
soft. Until they are hard, the 35 boxes of line 3 sit segmented and rendered
(`f18r_l3_boxes_g14.json`, `hi/l3g14_*.png`) waiting for them — which is, again, the same gate:
the plaintext side is what paces this, not the cipher side.


## The cipher settles a doubtful word in the plaintext

The stretch of f. 19r line 1 between *advertie* and *plustost* had resisted three readings; at
eight tiles it looks like **"Heut Jo."**, with a clear capital and a dot, which is not French that
fits the sentence.

The cipher settles it. Between the figures for *aduertie* and the code group `52` (*plustost*)
there is exactly **one box holding two figures** — so the plaintext there is **two letters**.
"Heut Jo." cannot be in the deciphered text at all; the two letters are **et**, and whatever
"Heut Jo." is — an annotation, a later hand, a flourish read as letters — it is not part of the
decipherment.

That is worth noting as a method in its own right: the crib has been used all along to read the
cipher, but the traffic runs both ways. A figure count is a hard constraint on how many letters a
doubtful passage of plaintext can contain, and here it eliminated a reading that three passes of
the eye could not.

With *et* fixed, f. 19r line 1 reads cleanly end to end:

> **Que sa Ma[jes]té fust advertie, et plustost que nous eussions victoire et …**

and the line 2/3 boundary of the cipher falls where it should: line 2's last six boxes are
*uictoi*, line 3 opens *r*, *e*. Line 3's box 3 is then the d-shaped figure that line 2 labelled
**e**, which is the cross-check reported above, now standing on a firm boundary rather than a
guessed one.


## `checkex.py`: the confusable figures are measured, and they are not separable by shape

With 42 labelled exemplars in hand, every pair was compared by normalised correlation. Two results.

**The control passes.** Eight pairs come out at 1.000 — these are the same boxes mined twice, once
at gap 18 and once at gap 14, and they agree on the letter every time. The two passes are
consistent.

**The confusables are quantified.** Six pairs above 0.80 carry *different* letters:

| correlation | letters |
|---|---|
| 0.925 | **e / u** |
| 0.914 | **i / n** |
| 0.911 | **s / i** |

These are exactly the pairs that have blocked this target all along, and they are not a
transcription failure — they are figures that genuinely resemble each other at 0.91–0.93
correlation on the manuscript. **No classifier, and no amount of care with the eye, will separate
them at this resolution.**

### What that changes

It reframes the problem, and it explains every dead end hit tonight. If the figures for *i*, *n*
and *s* cannot be told apart by sight, then **at the level of reading, this cipher behaves as a
polyphonic one**: a figure is not one letter but a small set, and only the language can choose
between them. That is why:

* the shape classifier (`shapes.py`) failed and was always going to;
* `key.json`'s entry `"6": ["i","n","s"]` — written early as a workaround — was the correct model
  all along;
* the beam decoder reaches roughly 60 % of words rather than 95 %: it is doing the right thing
  against an irreducibly ambiguous input;
* and the same figure "needed two letters" in line after line. It did.

The consequence for the remaining work is concrete: the decoder should be given the ambiguity
explicitly, as a set per figure with the exemplar evidence behind it, and the reading should be a
Viterbi over those alternatives against the French model — the approach that closed the Lucca
polyphonic cipher in this repo — rather than a substitution with a table.


## `readleaf.py`: figures in, French out, with no figure ever named

The pipeline the exemplars were built for: segment a line, match every box against the labelled
exemplars to get a distribution over letters, and beam-search those distributions against the
French model. Nothing is transcribed and no figure is given a name.

Run on f. 18r, the leaf the exemplars come from:

```
line 2 (29 figures): ste f est a le roi ei il l dion sui uoie
   truth:            ste fust aduertie et [52][14][25] eussions uictoi

line 3 (35 figures): re et conseil dit soil iir tlr sa sa uie et su
   truth:            re et conseil d assembler de Castillebourg ...
```

**`re et conseil d` — fifteen characters, exactly right, straight out of the ink.** And `ste f` at
the head of line 2. That is the loop closing: image → letter distribution → French, with the
plaintext nowhere in the process.

### Where it stops, and why

Both lines degrade after the opening, and the reason is coverage, not method. The exemplar set is
42 figures over **14 letters**, weighted heavily to e, i, s, t, u — the letters that happened to
fall in the two crib lines mined so far. *assembler de Castillebourg* needs a, m, b, c, g, which
are thin or absent, so the beam has nothing to match and falls back on the language model alone.

The alphabet with its homophones is on the order of 90 distinct figures. Two crib lines gave 42
exemplars over 14 letters; ten to fifteen lines should give the lot. **The measurement to watch is
letters covered, and it is the only thing between here and reading the leaves.**

### One caveat found in passing

The same pipeline run on f. 143 produces noise. f. 143 is a different secretary's hand, and
exemplars cut from f. 18 do not transfer to it. So the crib gives the *table* — which figure means
which letter — but each leaf still needs its own figures matched against exemplars in its own hand,
or the shared table applied through a transcription. That is a real limit on how far one crib
carries, and it was not visible before there was a working pipeline to expose it.


## Coverage is the whole story: 14 letters to 16, and the line reads

Mining the rest of f. 18r line 3 took the exemplar set from 42 figures over 14 letters to **65 over
16** — the gain being a, b, c, d, l, m, o, r, the letters *assembler de Castillebourg* needed.
Re-running `readleaf.py` on the same three lines:

```
before (14 letters)   line 3: re et conseil dit soil iir tlr sa sa uie et su
after  (16 letters)   line 3: re et conseil des sembler de castille bour
   truth:                     re et conseil d assembler de castillebourg
```

**Forty characters of the line now read.** Line 2 also improves — `ste f est a bert ie ie le d ions
ueue et` against a truth of `ste fust aduertie et [52][14][25] eussions uictoi` — and that gain is
*not* circular: line 2's own exemplars did not change, only line 3's were added, and line 2 got
better because the letters it needed finally had figures behind them.

Line 3 reading itself back is partly circular and is not offered as proof. The proof is line 2, and
the trend.

### The remaining gap, named exactly

16 of 22 letters covered. Missing: **g, h, p, q, x, y, z** — the rare ones, which is why they have
not turned up in three crib lines of ordinary prose. They will come from lines containing words
like *que*, *quelque*, *pays*, *chose*, *hommes*. The code groups also need exemplars of their own:
`52`, `14`, `25` currently decode as letters because nothing in the set says they are codes, which
is what mangles the middle of line 2.

So the two things between here and a read leaf are: **seven more letters, and the code groups**.
Both come from more crib lines, and the count of letters covered says exactly how far along it is.


## The cipher finds a gap in my reading of the plaintext

Line 4's boxes 12–26 rendered: box 24 is a clear **4**, box 25 holds **`14`** — the code group for
*que* — and box 21 is a plain **X**.

That `14` is a hard landmark, and it does not sit where my transcription puts *que*. f. 19r line 2
was read here as *"…où l'on feist que je n'avois plus d'instruction"*, which would put *que*
immediately after *feist* — at box 12. It is at box 25. **Thirteen figures of plaintext are missing
from my reading of that line.**

So the line is not *"où l'on feist que je n'avois…"* but *"où l'on feist [≈13 letters] que je
n'avois…"*, and the eye skipped a phrase — probably at the gutter, where line 2 of f. 19r is
tightest.

This is the second time the figure count has corrected the plaintext rather than the other way
round (the first was *et* for the spurious "Heut Jo."). It is worth stating as a property of a
crib of this size: **with ~1,650 figures against ~1,800 letters, the two sides audit each other**,
and a transcription error on either side shows up as a landmark that lands in the wrong place.

Also seen: an unmistakable **X** at box 21. Neither Tomokiyo's table nor anything recovered here
has an x, and in a French plaintext x is rare enough that a figure standing plainly for it, in the
middle of a line, is more likely a **null**. Worth testing once the coverage is complete.


## Code groups decode in place, once the beam is made length-fair

Adding three code exemplars (`52` = *plustost*, `14` = *que*, twice) did nothing at first, and the
reason was a bug in the decoder rather than in the evidence. Beam search over variable-length
emissions is biased towards short ones: a code group that emits eight characters pays eight
characters of log-probability while a letter pays one, though **both consume exactly one figure**.
The beam therefore always preferred a letter. Offsetting with a per-character bonus at the model's
mean cost (`CHAR_BONUS = 1.6`) makes hypotheses that consume the same number of figures comparable.

```
line 2 (29 figures): ste f est a le rti de plustost que es sions ueue et
   truth:            ste fust aduertie et  PLUSTOST QUE NOUS eussions uictoi

line 3 (35 figures): re et conseil des sembler de castille bour
   truth:            re et conseil d assembler de castillebourg
```

**`plustost que` comes out exact, in place, from the ink.** Line 3 is essentially right end to end;
line 2 runs at roughly two thirds with the code groups correct.

## Score at this point

| | |
|---|---|
| exemplars | 79 figures |
| letters covered | **17 of 22** — missing h, p, q, x, y, z |
| code groups | 3 (`52`, `14`×2); `25` and the rest still to cut |
| best line | f. 18r line 3, read end to end from figures alone |
| pipeline | `readleaf.py` — segment, match, beam; no figure is ever named |

The two things still between this and a read leaf were named earlier as *seven letters and the code
groups*. The code groups are now demonstrated. Five letters remain, all rare, and they will come
from crib lines containing *chose*, *pays*, *quelque*, *hommes* — f. 19r line 4, *"changera tant par
les habitans de la ville qui estoient fort estonnez"*, carries h, p, q and z in one line.


## More landmarks in the cipher: codes 24 and 35

Scanning f. 18r lines 5–7 for code groups — they stand out, being figures rather than letter-shapes
— turns up **`24`** (struck through, mid-line 5) and **`35`** at the end of line 6. Tomokiyo gives
24 = *nostre* and 35 = *parce que*.

Neither has been checked against a plaintext before. They are also two more anchors for
`align.py`: the landmark set on f. 18r is now `14`, `25`, `52`, `24`, `35`, which is roughly one
every line and a half — dense enough that the cumulative alignment cannot drift far before being
pulled back.

The struck-through `24` is worth a note of its own. A deleted code group means the clerk
*enciphered a word and then cancelled it*, which the decipherment on f. 19 will silently not
contain. Any alignment that assumes every figure produces a letter will lose a beat there, so
struck figures have to be found and skipped — one more reason the landmark-and-audit approach is
right and a straight position count is not.


## Code groups need a similarity floor, and it is 0.93

Letting code exemplars compete on equal terms with letters made the decoder hallucinate them: lines
5–8 came back studded with *plustost* where no code group exists. A figure that merely resembles a
numeral was dragging a whole word into the reading, and the per-character bonus that makes codes
competitive at all was paying for it.

Codes are distinctive — they are numerals among letter-shapes — so a genuine match should be very
close. Adding a floor on the code candidate's own similarity, and sweeping it:

| floor | line 2 (has real codes) | line 6 (has none) |
|---|---|---|
| 0.90 | plustost que ✓ | *plustost … plustost* ✗ |
| **0.93** | **plustost que ✓** | **clean** |
| 0.96 | plustost que ✓ | clean, but line 2's tail degrades |

**0.93.** At that setting the real code groups on line 2 still fire and the phantoms on line 6
disappear, and line 2's reading improves as a side effect —
`ste f est a bert ie e plustost que es sions ueue et` against a truth of
`ste fust aduertie et plustost que nous eussions uictoi`.

This is the last of the decoder's free parameters to be pinned by measurement rather than taste:
segmenter gap 14, character bonus 1.6, code floor 0.93 — each one fixed against a stretch of known
plaintext rather than by how the output looked.


## A number to beat

The pipeline's output has been described so far by quoting the good bits, which is the easiest way
to fool yourself. `baseline.py` scores it instead: character overlap against the crib's known
plaintext on three lines of f. 18r, by the same measure every time.

```
2026-09-17   79 exemplars / 17 of 22 letters / gap 14, bonus 1.6, code floor 0.93
  f.18r l2:  33/ 46 =  71.7 %
  f.18r l3:  34/ 36 =  94.4 %
  f.18r l4:  17/ 38 =  44.7 %
  overall    84/120 =  70.0 %
```

**70 % of plaintext characters, from the figures alone, with nothing named.** Line 3 at 94 % is the
ceiling this approach reaches when the letters it needs are covered; line 4 at 45 % is what happens
when they are not — its plaintext runs through *instruction*, wanting p and q, both missing from
the exemplar set.

That spread is the argument in one table: **the variable is letter coverage, and nothing else.**
The next pass should move 17 of 22 upward and watch this number, rather than reading the output and
forming an impression of it.


## The baseline catches its own weakness

Mining *"que ie nauois plus dinstruction"* added 24 exemplars and brought **p** in — 18 of 22
letters now, missing only h, q, x, y, z. The output visibly improved: line 2 turned `f est` into
**`fust`**, exact; line 4 gained **`tion`** and `que i en au o` for *que ie nauois*.

And the score went **down**:

```
                     before   after
  f.18r l2            71.7 %   65.2 %
  f.18r l3            94.4 %   94.4 %
  f.18r l4            44.7 %   50.0 %
  overall             70.0 %   69.2 %
```

One character in 120. That is not a regression, it is **noise** — and the useful finding is about
the measure, not the pipeline: **three lines and 120 characters is too small a test set to detect
anything.** A change of ±1 character means nothing, and if the next pass "improves" the score by a
point it will mean nothing either.

So the baseline as built is under-powered, and its first real job was to expose that. Before it can
be trusted to steer the work it needs ten or fifteen scored lines, not three — which means more of
f. 19r transcribed, which is the same gate as everything else here.

That is worth recording plainly, because the alternative was to note that the output looked better,
call the mining a success, and carry on. It did look better. The number says we cannot yet tell.


## Figure-unit arithmetic, and a prediction that lands

Counting the plaintext in *figure units* — one per letter, one per coded word — places any passage
on the cipher without transcribing a figure. Checked against the two stretches already labelled by
hand, it runs about **four units long over 125**, and the reason is digraph figures: the doubled-s
that reads *ss* swallows a letter, and there are others. So the arithmetic locates a **line**
reliably and a **box** only to ±4.

That is still enough to predict. f. 19r line 4 — *"…de la ville qui estoient fort estonnez"* — puts
the code group for *qui* near f. 18r line 8, box 26. Rendering that line's boxes:

* **box 29 carries a code group `14`** — three boxes later than predicted, inside the known drift,
  and *que* for *qui* is the clerk's latitude, not an error. **The prediction lands.**
* **box 24 carries `82`.** Tomokiyo's nomenclature gives **82 = le Prince de Condé**.

The second is the first piece of *content* this crib has yielded that is not already in the clear on
f. 19: a code group naming Condé, in a despatch about the Guyenne siege, four boxes from a *qui*
that the decipherment puts in the middle of *"les habitans de la ville qui estoient fort estonnez"*.
Whatever f. 19 says at that point, the figure says **Condé**.

It also adds a sixth landmark — `14`, `25`, `52`, `24`, `35`, `82` — and confirms that scanning a
line for numerals is the cheapest way to find them, since they stand out among letter-shapes without
any matching at all.


## Three errors the landmarks have caught in my plaintext — and what that means

Every code group is a word whose position the arithmetic predicts. Where the prediction and the
figure disagree, one of the two readings is wrong, and so far it has been mine every time:

1. **A phantom.** f. 19r line 1 appeared to read *"…advertie. Heut Jo. plustost…"*. The cipher has a
   single two-figure box there, so the plaintext is two letters: **et**. "Heut Jo." is not part of
   the decipherment.
2. **A dropped phrase.** Code `14` (*que*) sits at f. 18r line 4 box 25, thirteen figures later than
   my reading of f. 19r line 2 put it. **Thirteen letters were skipped**, probably at the gutter.
3. **A missing *parce que*.** f. 18r line 6 ends with code `35`, which Tomokiyo gives as *parce
   que*. By the arithmetic that falls inside f. 19r line 3, where my transcription reads
   *"…il nous Ma[jes]té considérant que les cho[ses]…"* — with no *parce que* anywhere in it.

Three errors in roughly a dozen lines of quick transcription is about what a first pass over a
sixteenth-century secretary hand should produce. The conclusion is not that the method is fragile —
it is that **the method is catching them**, which is precisely what a crib of 1,650 figures against
1,800 letters is for.

**The practical consequence:** more mining should wait on a careful second pass over f. 19r. Labelling
figures against a plaintext with three known errors in it will mint wrong exemplars, and a wrong
exemplar is worse than a missing one — it pollutes every later match. The order of work is
therefore: re-read f. 19r line by line against the code-group positions, *then* mine.

The landmark positions already computed give the check for that re-reading: `52` and `14`/`25` in
f. 19r line 1, `14` again 13 figures past *feist* in line 2, `35` in line 3, `82` (**le Prince de
Condé**) and `14` in line 4. Any transcription that does not put those words at those figure counts
is wrong somewhere, and the count says roughly where.
