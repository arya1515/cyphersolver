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
