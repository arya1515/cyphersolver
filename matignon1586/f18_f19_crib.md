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

## One warning for whoever aligns it

The figure values coming out of this crib do **not** agree with the ones the f. 196/201 crib gives
under the same ad-hoc names: the f. 18 crib wants (reading my own shorthand) Δ = e, x = m, t = i,
where f. 196's crib wanted Δ = r, x = a, t = e. Two readings are possible and they must be
distinguished before any of this is trusted:

1. the shapes really are different and my ASCII shorthand has collided — which is likely, since
   this cipher has several near-identical figures and the shorthand was never grounded in an image;
2. or ff. 18-21 and ff. 196/201 are **not in the same key**, and Tomokiyo's single paragraph has
   lumped together two ciphers. Note that f. 18 is written *by* Mayenne (it confers "avec Monsieur
   le Mareschal de Matignon"), while f. 196 is written *about* him ("Monsieur du Mayne vous a faict
   une autre despesche"), so they are not from the same desk.

The way to settle it, and the reason this crib is worth the work, is to stop naming figures
altogether: segment f. 18r/18v into glyph boxes, align the boxes to f. 19's known plaintext, and
keep the **images** as labelled exemplars. Then match each undeciphered leaf's boxes against those
exemplars by shape. That answers the question and builds the table in the same pass.

## Why this is the thing to do next

Everything attempted here has been limited by transcription, not by cryptanalysis, and every
confusable pair that has been separated was separated by a crib. This crib is an order of
magnitude larger than the f. 196/201 one:

1. With the plaintext known, a transcription of the cipher does not have to be right — it has to be
   *alignable*. A mis-seen figure shows up as a mismatch against a known letter and is corrected on
   the spot, instead of having to be guessed from context.
2. 2,500 aligned figures give many exemplars of every homophone, which is what the shape
   classifier needed and never had (`shapes.py` failed on 30 exemplars).
3. The result is the complete Mayenne–Forget Cipher-1 table — not Tomokiyo's partial one — after
   which the eight undeciphered leaves are a transcription exercise with no unknown figures left.

## Set-up already done

`hi/f18r.jpg`, `hi/f18v.jpg`, `hi/f19r.jpg` fetched at native resolution; `hi/f19rflat.png`
flattened and `f19r_lines.txt` fitted (32 lines, pitch 125, clean). `mtile.py` now snaps each
fitted centre to the local ink maximum, so the per-leaf offset that cost so much time no longer has
to be set by hand.
