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
