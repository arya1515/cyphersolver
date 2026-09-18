# Forget / Matignon / Mayenne, BnF fr. 15572 (+ fr. 15571), 1586

Catalogue item 12 (`CATALOGUE.md`), class B, solvability 5. Ten leaves that S. Tomokiyo
(`cryptiana`, *Henry III's Cipher with Ambassadors*) marks **undeciphered** although he publishes
partial tables for the two keys involved.

## What the target actually is

Tomokiyo's list, checked against the live page on 17 Sept 2026:

* **Mayenne–Forget's Cipher-1** (used among Mayenne, Forget de Fresnes, Villeroy and Henri III).
  Deciphered siblings in the same volume: **f. 14** (deciphered in f. 15), **ff. 18-21**
  (deciphered in f. 19), **ff. 78-79** and **ff. 91-92** (deciphered in the margin).
  Undeciphered: **ff. 110, 123-124, 143, 150, 154, 173, 196, 201**.
* **Matignon's Cipher-3**: deciphered f. 189 (in f. 190), ff. 277-278 (in ff. 279-280), f. 282
  (margin); undeciphered **f. 276**, and **f. 179 of fr. 15571**.
* fr. 15572 **f. 43** is in the catalogue line but is *not* open: George Lasry solved it in 2022.
* The catalogue's "fr. 15571 ff. 218-219" is a slip for **fr. 15572 ff. 218-219** (Matignon in
  Mayenne–Forget's Cipher-2).

Prior art checked: no printed decipherment of these despatches was found (searches on the BnF
catalogue and on the literature, 17 Sept 2026). Tomokiyo publishes short openings for ff. 143,
150, 154 and for "f. 111" (probably a slip for f. 110).

## Access: folio to Gallica canvas

fr. 15572 = ark `btv1b9061879d` (385 canvases); fr. 15571 = ark `btv1b90618802` (226).
**Each canvas is a double-page opening**, so the recto of folio *f* is the *right* page of a
canvas, and the verso of *f* is the *left* page of the next. The leaf carries two foliations,
the older one struck through; **the valid number is the lower of the two**. The offset from
folio to canvas drifts (about +2 at f. 14, +6 from f. 99 to f. 137, +7 by f. 142), so it has to
be read off the leaf. Fixed here:

| folio | canvas (page) | content |
|---|---|---|
| 14r / 14v | 16 right / 17 left | Forget to Villeroy, 24 Jan 1586; 4-line ciphered postscript on 14v |
| 15r | 17 right | the decipherment of that postscript, in clear, 3 lines |
| 78v, 79r | 85 left, 85 right | Mayenne to the King, camp de Tonneins(?), March 1586; cipher blocks with marginal decipherment |
| **110** | **116 right** | one leaf wholly in cipher, c. 48 lines, ending "De Bellebourg … jour de Mars 1586" |
| **123-124** | **129 right – 131 left** | despatch to the King: f. 123r opens in clear, then c. 140 lines of cipher over four pages |
| **143** | **150 right** | Mayenne to the King: clear first half (Marmande, Sainte-Bazeille, Castets, the capitulation), then 22 lines of cipher |
| **150** | **158 left** | a full page of cipher |
| **150** | **157 right – 158 left** | a page and a half wholly in cipher |
| **154** | **161 right** | clear opening, then c. 25 lines of cipher |
| **173** | **180 right** | "Sire" in clear, then c. 30 lines of cipher |
| **196** | **203 right** | clear to *auquel*, then 32 lines of cipher to the foot |
| **201** | **208 right** | the **same despatch**: clear a line and a half further, cipher, then clear again for the last three lines |

The clear openings identify the despatches: f. 123r "Sire, la dernière que j'ay eu l'honneur est
du huict[iesm]e de ce moys…"; f. 143 Marmande, Sainte-Bazeille, Castets and the capitulation;
f. 154 "Monseigneur, vous avez veu par la despesche du S.r Delorme … qui partit d'icy la veille de
Pasques" (Easter 1586 = 6 April), so f. 154 is to Villeroy, not to the King; f. 173 "Sire, Vostre
Majesté a esté suffisamment advertie par les deux dernières despesches de Monsieur du Mayne";
ff. 196 and 201 both "Sire, Depuis le partement du S.r de Bosseval…".

**ff. 196 and 201 are the same despatch** — see [`f196_f201.md`](f196_f201.md). That pair is now
the most tractable target in the item: it carries two cribs (f. 201 is in clear where f. 196 is in
cipher, at the head and again at the foot) and the two ciphered blocks are the same plaintext
enciphered twice, i.e. in depth.

All eight Mayenne–Forget leaves are now located on the image. f. 143 is the best conditioned:
a large, well-spaced hand, 21 lines. ff. 110 and 123–124 are the same cipher in a small, dense
hand — f. 123r alone runs to 38 lines — and are where the volume of text is.

## Method

1. `fetch.py` / `corners.py` / `folgrid.py` — IIIF fetch of the volume and of the folio-number
   corners, to build the index above.
2. `mklm.py` — a character 6-gram model of period French built from the 10 MB of Berger de
   Xivrey's *Recueil des lettres missives de Henri IV* already in `../bethune/xivrey/`
   (6.4 M characters after normalising: accents stripped, v→u, j→i, as the cipher does not
   distinguish them).
3. `flatten.py` — divides out a Gaussian background (flattens the parchment), then unsharp-masks.
   This is the single biggest gain in legibility of anything tried here and should be the first
   step on any new leaf. `tiles2.py` then cuts the block into per-line tiles for transcription by
   eye; `fitlines.py` + `recenter.py` place the lines.
4. `solve.py` / `dec.py` — a beam search over the token sequence where each glyph token carries a
   *set* of candidate letters, scored by the language model, then a dictionary word-segmenter.
   This is what makes the key usable: several glyphs of this cipher are genuinely confusable
   (Tomokiyo boxes three near-identical "6" shapes standing for **i, n, s**), so a
   one-glyph-one-letter transcription is not achievable by eye and the ambiguity has to be
   carried into the decoder.

## The key, as re-derived from the manuscript

Verified against the complete f. 14v/f. 15r crib ("Vous pouez juger que ceste ouverture n'est pas
toute nouvelle …") and against the cipher of f. 143. Values in **bold** are not in, or not
legible in, Tomokiyo's published table.

| glyph | letter | glyph | letter |
|---|---|---|---|
| ɑ (a with tail), Δ | a | ·v·, **ʄʄ (ff-ligature)** | n |
| ʠ | b, z | 7, H | o |
| ʃ (long s) | c | ᴄ, R | p |
| ϖ (m with overbar), ∞ | d | £, Ɛ, e | r |
| t, ʓ, Ƨ, ʋ | e | ∂, ɟ, **ɣɣ = ss** | s |
| M | f | m, **Ƶe** | t |
| 8, ▽, y | g | ʃ, s, Ɋ, ⊐ (box), **ꝉ (crossed t)** | u / v |
| f | h | θ, **₸ (crossed 4)** | m |
| o, 6, β, ε, 3, **ƀ** | i / j | n, A, **ʰe** | l |

Code groups seen so far: 12 *il*, 13 *qui*, 14 *que*, 47 *tous*, **49 (unidentified, frequent)**,
76 *le roi de Navarre*, 26 *vous/leur*.

## Result so far

**f. 143 (Mayenne to Henri III): 21 lines transcribed, about half read.** See
[`f143_reading.md`](f143_reading.md) for the text, `cipher_f143.txt` for the glyph transcription
and `reading_f143.txt` for the decoder's raw output. Tomokiyo printed
"s'estant laisse entendre 49 il se voulloit de partir du 76 duquel je scai quil est tres
malcontant et ayant considere que je lai tousjours ou y tenir pour le meilleur …". The reading
here agrees and runs on:

> … m'estant laissé entendre [49] il se vouloit départir du **roi de Navarre**, duquel je scai
> qu'il est très malcontant; et ayant considéré que je l'ay tousjours ou y tenir pour le meilleur,
> comme de [49] commandement qu'il ayt, et que ce ne seroit [une] petite faveur pour ses affaires
> que de …

Later stretches read "… le et service; il m'a promis de vous … faire pendant ce temps …",
"… ou à la vérité il s'est résolu … la composition de sa place, laquelle estoit encore …",
"… de séjour qui nous est très … parce qu'il m'eust fallu passer …". Lines 8-9, 14-15 and 19-21
still carry glyph errors and are not offered as a reading.

A practical note for whoever continues: **measure the line positions, do not assume they are
evenly spaced.** Cutting f. 143 on a uniform grid put the bands up to 60 px off by line 15 and
turned the second half of the page into noise; correlating a comb against the row-ink profile,
then refining each line on the local maximum, fixed it.

## Open / next

* Finish f. 143's weak lines (8-9, 14-15, 19-21). Everything there turns on telling apart the
  three "6" shapes (i / n / s) and the two round shapes (a / m); a labelled glyph atlas cut from
  the lines that already read would settle them.
* **ff. 196 / 201 first**: transcribe both blocks, align them, solve jointly against the two
  cribs. This is the one place in the item where the evidence is doubled.
* f. 110 is faded and dense (c. 48 lines); ff. 123-124 is the prize (four pages, c. 140 lines,
  opening in clear: "Sire, la dernière que j'ay eu l'honneur est du huict[iesm]e de ce moys …").
* A word-aware decoder (`wdec.py`, beam over letters *and* word boundaries, unigram word model
  swapped in for the character model over each closed word) was tried against the character
  decoder and does **not** help: on f. 143 the two agree on the lines that read and both fail on
  the same lines. That is the evidence that the residue is transcription, not decoding.
* The f. 18-21 / f. 19 crib has not been used yet and should settle the remaining homophones and
  the value of code 49.


## Where the work actually stops, measured

Two leaves have now been pushed hard enough to measure the cost of this cipher:

* **f. 143** (21 lines, the largest and cleanest hand of the eight) took *three* passes — three
  tiles a line, then five, then eight on the survivors — to reach about two thirds read. Lines
  1-7, 9-14 and 17 are continuous French; 8, 15-16 and 18-21 give clauses only. Line 8 resists
  even at eight tiles a line and flattened: it decodes to "a r o m e ? e [car] l m a l a i c t e
  d e n e p o r t e ..." and no reading of it is French, which most likely means a place or
  person name in it.
* **f. 196** (36 lines, small hand) is not yet transcribed: the line fit alone needed a comb, a
  spacing-constrained DP, re-centring on glyph boxes and a manual offset, and still does not place
  every line well enough to tile. That is before a figure is read.

So the cost is roughly three tool-calls per line to get tiles the eye can settle, and about
fifteen per cent of figures resist anyway, to be recovered — or not — by the language model. The
eight Mayenne-Forget leaves are about 300 lines. This is a multi-session job, and the constraint
is the transcription of a 16th-century hand, not the cipher, which is solved.

### The order to do it in

1. **ff. 196 / 201** — the only place where the evidence is doubled (same plaintext twice) and
   where cribs at head and foot let segmented glyph boxes be *labelled*, which is the only thing
   that has actually broken a confusable pair so far.
2. **f. 143's** remaining eight lines.
3. **f. 154, 173** (clear openings, ~25-30 lines each).
4. **f. 110** (48 lines, faded) and **ff. 123-124** (140 lines) last: most text, worst conditions.


## Line placement is the unglamorous blocker

Worth writing down because it cost more than anything else here. Tiling a block into per-line
images needs the line centres to within about a fifth of the line pitch, or the tile clips and the
figures cannot be read. On these leaves the pitch is *not* constant — it wanders by 10-15 % from
line to line — so none of these alone is enough:

* a uniform grid from a comb fit (drifts; this is what silently corrupted the second half of the
  first f. 143 pass);
* local refinement on the ink profile (jumps to a neighbouring line);
* re-centring on the median glyph-box centre (`recenter.py` — returns almost no correction,
  because the boxes are already symmetric about the wrong centre);
* centre of mass of the x-height band (`center2.py` — best of the four, still leaves a systematic
  offset that varies per leaf and has to be found by eye on an overlay).

What works, and what the next pass should just do: draw the fitted lines on the flattened block,
look at the overlay, and set the per-leaf offset by hand — then tile with a band of about half the
pitch. f. 143 and f. 201 both fitted cleanly this way; f. 196 (the smallest hand) still does not,
and that is why its 32 lines are untranscribed while f. 201's fit is ready to use.


## The f. 18/f. 19 crib and the figures-to-French pipeline

The second half of the 17 Sept 2026 work turned on a crib Tomokiyo mentions in one clause and never
uses: **f. 18 is ciphered and f. 19 is its decipherment in clear**, about 1,650 figures with their
plaintext beside them. Full account in [`f18_f19_crib.md`](f18_f19_crib.md). In short:

* The pairing is verified twice on the leaf — f. 19r opens *"Que sa Majesté fust advertie"* against
  a cipher opening with `14` (*que*), and the cipher carries `52` where the clear reads *plustost*,
  the first check of Tomokiyo's nomenclature against a plaintext.
* It is **one key** across the leaves; an apparent contradiction with the ff. 196/201 crib was my
  own shorthand colliding on near-identical figures, not two ciphers.
* The confusable figures were **measured**: i/n, s/i and e/u sit at 0.91–0.93 correlation on the
  manuscript. They are not separable by shape at any resolution available, so **at the level of
  reading this cipher is polyphonic** — a figure is a small set of letters and only the language
  chooses. That explains every dead end: the shape classifier was always going to fail, and the
  early workaround `"6": ["i","n","s"]` in `key.json` was the right model all along.
* So the crib's output is stored as **labelled images**, not names: `exemplars/` with a manifest.
  103 figures over 18 of 22 letters at the time of writing; missing h, q, x, y, z.
* `readleaf.py` reads a line from figures alone — segment, match against exemplars, beam-decode
  with code groups — and recovers about **70 % of plaintext characters** on the crib leaf, with
  f. 18r line 3 read end to end: *"re et conseil des sembler de castille bour"*.
* Every free parameter is pinned by measurement against known plaintext, not by taste: segmenter
  gap 14, per-character bonus 1.6, code similarity floor 0.93.
* `baseline.py` scores the pipeline so a later pass can tell whether it helped — and its first job
  was to show that three lines is too small a test set to detect anything.

**The variable that remains is letter coverage.** Line 3 reads at 94 % because its letters are
covered; line 4 at 45 % because *instruction* wants p and q. Nothing else in the pipeline is
uncertain.

Two practical findings for whoever continues: **proper names are the densest exemplar source** (they
are spelled out rather than hidden in code groups — *Matignon* on f. 19r line 13 is nine consecutive
certain figures), and **exemplars do not transfer between scribal hands** — the same pipeline run on
f. 143 gives noise, because that is a different secretary.

## Session of 18 Sept 2026: six leaves read, and the target is not one cipher

**Read in substance or in stretches, all in the solved Cipher-1:** f. 143r+v (earlier), **f. 150**
(13 ciphered lines over a clear Forget letter to Villeroy, April 1586), **f. 154** (28 lines, the
army's pay crisis), **f. 173** (33 lines, to the King: no one will lend and no one will go surety),
**f. 196** (26 lines) and **f. 201** (30 lines) — one despatch on two leaves, a siege report naming
**"le mareschal de Matignon"**, and **fr. 15571 f. 177** (28 lines, Mayenne's design for Gascony,
31 Dec 1585). See the `f*_reading.md` files.

**The ff. 196/201 check.** The two leaves were transcribed independently and share **23 runs of
eight consecutive identical figures**. That is not reachable by chance, and it validates both
transcriptions at once.

**The target is at least three ciphers** — see `ciphers.md`. ff. 123–124 and f. 110 do not answer to
the solved key, on figure statistics and on a crib. fr. 15571's ciphered page at canvas 187 left is
a fourth hand again, untested.

**A crib for the second cipher exists**: f. 79r (canvas 85 right), Mayenne's own letter from the
camp at Tonneins, 5 March 1586, carries a seven-line cipher block **with its decipherment down the
left margin**. "rouergue" matches the block's figures in exactly one place, giving `4+`=r, `6`=o,
`h`=u, `f`=e, `B`=g.

### Additions to the folio index

| folio | canvas (page) | content |
|---|---|---|
| **79r** | **85 right** | Mayenne to the King, camp de Tonneins 5 March 1586, signed Charles de Lorraine; 7 cipher lines **with marginal decipherment** — the crib for Cipher-2 |
| **125r** | **131 right** | clear letter: Castets besieged, the battery, M. d'Alincourt, Matignon, Mayenne |
| **fr. 15571 177** | **185 right** | Forget, 31 Dec 1585, 28 cipher lines in Cipher-1 (foliated 190 struck / 177) |
| **fr. 15571 178v** | **187 left** | a full page of cipher in a fourth hand, untested |
| **fr. 15571 180** | **188 right** | (fixes the foliation: f. 180 recto is canvas 188 right) |

### Tools added

`rowcut.py` cuts rows with **alternate rows tinted**, so a row's left and right halves carry the
same wash and the join never depends on a line number — the fix for a full hour lost on f. 173 to
halves joined one row apart. `fitlines.py` fits and snaps a line grid. `hillclimb.py` is a cold
solver (annealing over figure→letter maps, `FIX=` to hold known values, `SEEDKEY=` to start from a
known key).

### A defect in the language model, found and fixed

Built with `v→u` and `j→i`, the corpus's Roman numerals became runs of `i`, and a page of `iiiiii`
scored **better** than French (−1.53 vs −1.51 per character) — so the cold solver collapsed every
figure onto `i`. Dropping Roman-numeral tokens and requiring a context to be attested 15 times gives
French −1.51, all-`i` −2.16, random −3.99. The old model is kept as `lm_v1.pkl`, the old scorer as
`solve_v1.py`.
