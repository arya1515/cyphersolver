# Sormano and de Vaulx from Ferrara to François I, February–March 1529 (BnF fr. 3096 nos. 62–67)

**Status: not read. The documentary problems are solved and the key is partly recovered; the ciphered
passages themselves are not deciphered.** (18 Sept 2026)

This is catalogue item 8. The target was set with a status line that described the item as already
"read (17 Sept 2026), nos. 65 and 66 in full, no. 63 as far as its leaves go", by applying "Lasry's 2023
key" through a glyph-level pipeline of "18,273 glyph boxes from ten page sides, clustered and
hand-labelled, a k-NN classifier". **No such work exists in this repository, and nothing here reproduces
it.** No published Lasry key for this manuscript could be found (searched Cryptologia, HistoCrypt,
academia.edu and the DECRYPT project pages). What follows is what could be verified from the images in
one session, and it both confirms and corrects parts of that status line. Nothing below depends on it.

## 1. What the volume actually contains

Gallica ark `btv1b9060015d`, 150 canvases, each canvas one black-and-white microfilm frame of a
double-page opening (9120 × 6250 px). The digitisation was made from the substitute microfilm MF 31394,
not from the original. **Canvas = folio + 4**, fixed on two leaves (canvas 115 carries the foliation
"111", canvas 117 carries "113") and consistent throughout. So canvas *n* shows f. (n−5)v on the left and
f. (n−4)r on the right.

The piece list is in the BnF notice (`src/aem_fr3096.html`, ark cc49559v). In its flattened form the
folio number printed after a description belongs to the piece that **follows** it; this was checked
against the leaves (piece 60/61, the two Trivulzio avisos, sit on f. 111, which the notice prints before
"60"). Corrected list for the group:

| no. | letter | leaves | cipher |
|---|---|---|---|
| 62 | Gaspar Sormano → the King, Ferrara, 22 March 1529 | ff. 113–114 | short runs, **with interlinear decipherment** |
| 63 | Sormano and Joachin de Vaulx → the King, Ferrara, *penultimo* February 1529 | ff. 115, 116 **and 123** | four sides, dense; one interlinear gloss |
| 64 | Jean de Langeac and de Vaulx → the King, Venice, 6 May 1529 | ff. 117–118 | **none** |
| 65 | Sormano and de Vaulx → the King, Ferrara, 23 February 1529 | ff. 119–120 | three sides, dense |
| 66 | the same, docketed "duplicata" | ff. 121–122 | three sides, dense |
| 67 | Sormano's copy of his own letter to the Duke of Urbino | f. 124 | four lines, **with marginal decipherment** |

Three corrections to the catalogue and to the status line the goal carried:

* **No. 63 is complete, and its last sheet is f. 123.** The letter breaks off mid-sentence at the foot of
  f. 116v, and the status line said only that "its last leaf is not at f. 117". It is f. 123, bound out of
  order after the duplicate: f. 123r is numbered **"3"** at the foot (ff. 115 and 116 are numbered "1" and
  "2" in the same place), it continues the broken sentence, and it ends with the subscription and the
  signatures "Sormano, Joachin". Its blank verso f. 123v carries the address docket, written sideways,
  "…et Sormano / de penultimo febraro 1529".
* **No. 63 is dated after all**, on that third sheet: "Da Ferr[ara] p[en]ultimo de Febraro M D XXVIIII".
  The status line's "the letter itself carries none on the leaves seen" is true only of ff. 115–116.
  *Penultimo* February 1529 is the **27th** (February had 28 days that year), so the catalogue's "28 Feb"
  is one day out.
* **No. 64 has no cipher at all** and should not be grouped with the rest.

## 2. The cipher, and why nos. 65 and 66 crib each other

A homophonic **symbol** substitution: Greek-looking and geometric glyphs, letter for letter, several
glyphs per common letter, with at least one nomenclator group and two structural signs (below). The
letter-for-letter ratio is fixed by the crib on f. 124r: the marginal decipherment runs to 161 letters
against about 158 glyphs.

Sormano says so himself, in clear, in no. 62 (f. 113r): *"Mando a vra Mta un doppio di quanto Monsr di
Vaulx mi scrive et prega che scriva a vra Mta **in la mia cifra**, il che faccio"* — it is his own cipher,
and he is enciphering de Vaulx's material in it.

**The duplicate cribs its twin.** No. 66 is docketed "duplicata" and repeats no. 65 almost word for word,
but the two clerks enciphered **different stretches**. Where no. 66 reads in clear "fatta che hebbimo la
reverentia a Madama Rainea et al Sr Don Hercole", no. 65 has that inside a cipher run; where no. 66 has
in clear "per la grandezza sua ricercava tempo per meglio pensarvi, presimo aspettar la sua final
risposta, et in sto mezzo col Sr Don Hercole di nuovo fossimo, et fattogli intender", no. 65 ciphers it;
and conversely no. 65 gives in clear "et presentato le lre di vra Mta di credenza … et in nome di vra Mta"
and "nel modo ch Jo scrissi a vra Mta veramente non havesse" where no. 66 ciphers. This was found here by
direct comparison of the two openings and **confirms** that part of the status line. It is the route to
reading the pair: every such stretch is a crib of known plaintext against known ciphertext.

Two contemporary decipherments also survive, and they gloss the same news, because no. 62 encloses a copy
of the Urbino letter ("Mando ancora a vra un doppio d'una lra la qual scrivo al Sr Duca d'Urbin"):
* **f. 113r**, interlinear, above two short runs: "de un capitaneo suizaro ch si chiamando calzolari qual
  si ritrova ne laquilla".
* **f. 124r**, in the left margin, keyed to the cipher by a double-crossed tie mark: "un cappitaneo
  suizzeri nominato calzolite ch al p[rese]nto si retrovava ne l'aquila con numero de mille due cento
  fanti tra suissari et lanspueinelt [lanzichenecchi] ch desidera a retrovarse al beneficio de la lega".
* **f. 116v** carries a third, unrecorded gloss: the words "de Venetiani" written above a two-glyph group,
  which shows the cipher had a nomenclator for the Venetians. The catalogue notes decipherments only in
  nos. 62 and 67.

## 3. The partial key

`key_partial.tsv` gives 18 glyph values with the evidence for each. The chain is short and checkable:

* **Line 1 of the f. 124r crib is read glyph by glyph.** At high magnification (`crops/z128_L1exact.jpg`)
  it is exactly 13 glyphs, and the marginal decipherment gives exactly 13 letters for them,
  "n capitaneo sui" (the tie mark and the *u* of *un* falling outside the segmented range). That fixes
  n, c, a, p, i, t, a, n, e, o, s, u, i on twelve distinct glyphs.
* **Line 2 then confirms four of them independently.** Its opening reads "...eri nominato"
  (`crops/z128_L2start.jpg`), and *nominato* is spelled with the same glyphs for n, a, t and o that line 1
  gives, five words later and in a different word. It adds e, r, i, o, m, i.
* The interlinear gloss on f. 113r spells *capitaneo* with the same glyphs again, five weeks earlier.

The cipher's design is therefore clear: a homophonic symbol alphabet with three or four alternatives for
each common vowel (a has at least two forms, i at least four, o two, e two) and one or two for consonants.

**Verified on an independent letter.** The strongest check does not use the 1529 decipherer at all. No. 66
reads in clear "et il parlar suo fu di sorte ch Jo Sormano mi parue quasi", and no. 65 ciphers that same
sentence from "Jo" onward, so the twin supplies the plaintext in the clerk's own spelling. Applying the key
to those 21 glyphs of no. 65 returns

    expected   i o s o r m a n o m i p a r u e q u a s i
    key gives  i o s ? r m a n o m i p a r u ? ? ? a s i

17 of 21 letters, in a different letter of the correspondence, in words the crib never contained. Three of
the four gaps then resolved: the inverted triangle is q and capital H is u (completing "quasi"), and a
3-shape is a third form of o. Immediately after "quasi" the cipher continues with six glyphs that read
**c-h-i-a-r-o**, giving the three-barred E as h. That stretch is enciphered in *both* copies, so
"il parlar suo fu di sorte che Jo Sormano mi parue quasi chiaro" is text that has not been read before.

**Where it stops.** Line 2 continues with nine glyphs that the crib says must spell *calzolite*, and two
of those positions demand *l* where the same shapes elsewhere demand *i*. So the hand uses at least two
rho-like forms that this microfilm will not separate, and the same is true of the triangle/alpha,
chi/hooked-4 and stroke/tailed-4 pairs. That is the wall: not the cipher, but the image.

## 4. What the letters say, from the clear text alone

All of §4 comes from passages in clear; nothing here is decoded. Full transcriptions in `ct/clear_texts.md`.

The embassy of February 1529. De Vaulx ("Jo Gian Joachino") reached Ferrara "Zobia passata" (last
Thursday), went straight to the lodging of the resident ambassador Sormano, showed him the King's
instruction and mandate, and the two settled the line to take. They made their reverence to **Madama
Rainea** (Renée de France, married to Ercole d'Este the year before) and to **Don Hercole**, presented
their credentials, and put the King's proposal to Duke Alfonso I with "molte efficacissime ragion",
reminding him of "la grande opera che in beneficio della sua persona, stato, casa et successione vra Mta
havea fatto". The Duke's answer was long; they thanked him "della cosi grande et honorata offerta che gli
era piaciuto fargli", and he "disse nõ solo contentarsi ma con ogni instanza pregar vra Mta ch la volesse
[cipher]", persuading himself the King "nõ sara astretta far se nõ cosa conveniente et ragionevole". He
would not answer at once: "la cosa per la grandezza sua ricercava tempo per meglio pensarvi", so they
waited on his final reply and worked meanwhile through Don Hercole, "veramente desideroso far servicio a
vra Mta", who promised his offices "di buon cuore". The letter of the 27th reports the business still
open, "considerata la natura et qualita ⟨de Venetiani⟩", and that the Duke "mostra che la cosa debba
esser nõ poco difficile".

Their fallback is **Marshal Trivulzio**, named three times: his "auttorita et credito" with the Duke "assai
conferira et servira"; he is expected to pass through Ferrara on his way to Venice; de Vaulx will wait
three or four days more for him; and the 23 February letters end "Jo Joachin qua aspettaro il Sr Marechial
Triulzo, et siamo d'openione ch sua S[ignori]a, dal p[redet]to Sr Duca molto stimata, a beneficio di questa
causa s'adopri". The status line's "fall back on Ercole d'Este and on Trivulzio" is **confirmed**, and from
clear text.

A postscript on f. 123r: after the letter was written the Duke told them he had letters from Rome of the
18th, whose contents are in cipher.

No. 67 is a different matter, and its substance is readable because of the margin note. A Swiss captain
named Calzolari was at L'Aquila with 1,200 foot, Swiss and landsknechts, who wanted to come over to the
league; Sormano judged this "nõ de picolo momento a beneficio della lega et damno d'inimici", the Venetians
would pay only their own share, there was no money to be had in Ferrara, and rather than wait for the
King's answer and let the thing spoil he pledged his own credit to the Duke of Urbino, promising a good
bank bill at Ferrara or Florence and that the King would pay.

**What the status line claims and this attempt cannot support:** that Alfonso d'Este refused the kingdom of
Naples for himself and the captaincy of the French army, and pleaded want of provisions, and that the
agents called his difficulties pretexts. Those are exactly the passages both clerks enciphered in both
copies. The clear text gives only "so great and honoured an offer", the request for time, and the Duke's
insistence that the King would require nothing but what was reasonable. The content of the offer is not
read here, and I found no evidence for it in these leaves.

## 5. The glyph pipeline: what it does and where it fails

No imaging libraries are installed, so the pipeline is pure Python: `sips -s format bmp` writes an
uncompressed BMP and `glyphs.py` parses it. `glyphs2/3.py` add band detection from the horizontal ink
profile; `clean.py` drops edge artefacts, splits run-together glyphs at vertical profile minima and
absorbs stray fragments; `glyphs6.py` holds the shape metric; `solve.py` and `align.py` derive a key from
a crib. On the four-line crib of f. 124r the results are:

| step | result |
|---|---|
| ink threshold | Otsu returns 153, which is paper; 130 is right |
| text bands found | 4 of 4, at y 34–75, 168–213, 310–352, 458–502 |
| components after cleanup | 13, 48, 45, 55 = **161**, against **161** letters in the decipherment |
| line 1 against the crib | 13 components, 13 letters, read correctly glyph by glyph |
| shape classification | fails: 26 % on line 2 from line 1 templates, 40 % under blind clustering |

The segmentation is sound, and the fact that cleanup lands on 161 components for 161 letters is itself
independent proof that the cipher is letter-for-letter with no syllable groups in this passage.

**The shape metric was tuned, measured, and is still not good enough.** Binary overlap (Jaccard) on a hand
this thin fails outright: a one-pixel offset destroys the overlap, and on line 1 it ranked wrong pairs as
the closest. Blurring the mask before comparing fixes the gross failure. Sweeping grid size, aspect
handling and blur against line 1, where every glyph identity is known, the best variant is a 24 x 24
stretched mask, one box-blur pass, cosine distance minimised over shifts of +/- 2 cells: it makes the one
true repeated pair on that line (the two *n*'s) the global minimum, at 0.122 against a nearest wrong pair
at 0.139. But that margin is 0.017, and the median pair distance is only 0.41. Same-glyph and
different-glyph distances overlap heavily, so clustering 161 glyphs into about 30 groups is mostly wrong,
and a classifier trained on line 1 reads line 2 at 26 %.

The confusions are specific and they are the ones a human eye also fails on here: two rho-like forms
(i against l), triangle against alpha, chi against hooked-4, plain stroke against tailed-4. Some are
harmless, because the two forms encode the same letter (V and round-u are both *a*), and some are fatal.

What would remove the wall, in order: better images, since 50–60 pixels per glyph on a 1960s microfilm is
the binding constraint and the IIIF service serves no more than the film holds; then stroke-based features
(skeleton, junctions, shape context) instead of blurred masks; then joint decoding, using the
self-cribbing pair's long known plaintexts and Italian letter statistics to constrain the assignment
rather than deciding each glyph on shape alone.

## 6. What remains, and the route

1. **Make the glyph classifier work** (§5). The segmentation is done and reusable; the shape metric is not
   good enough. This is the one blocking step: with a working classifier the f. 124r crib alone should fix
   most of the alphabet, since the alignment machinery is already written and tested.
2. **Use the self-cribbing pair first.** Align nos. 65 and 66 stretch by stretch; each place where one is
   clear and the other ciphered is a crib, and between them they cover most of the letter of 23 February.
   The 161-letter crib on f. 124r and the shorter one on f. 113r pin the alphabet independently.
3. **Higher-resolution images.** The IIIF service serves only this microfilm; the originals are colour-shot
   nowhere as far as I can see. A reader in Paris, or a request for a new capture, would settle the
   ambiguous glyph forms that stopped this attempt.
4. Not checked: whether any of these letters is printed. The obvious places (Molini, *Documenti di storia
   italiana*; the Ferrara and Modena archive editions; Charrière) were not searched.

## 7. Files

`fetch.sh` (openings), `region.sh` (one page at full resolution), `zoom.sh` (an upscaled IIIF region for
glyph reading), `crop.sh` (bands from a fetched page), `glyphs.py` / `glyphs2.py` / `glyphs3.py` /
`glyphs4.py` (BMP parsing, components, band detection, clustering), `align.py` (crib alignment and key
read-off), `ct/clear_texts.md` (clear-text transcriptions), `key_partial.tsv` (the key with evidence),
`src/` (the IIIF manifest and the BnF notice), `img/` and `crops/` (page images and reading crops, not
committed).

Checked: the folio-to-canvas mapping, on two foliated leaves; the piece list against the leaves; the sheet
numbers 1, 2, 3 of no. 63 and its date, subscription and docket; that no. 64 carries no cipher; that nos. 65
and 66 encipher different stretches, on four matched passages; the two contemporary decipherments and the
third gloss; 17 glyph values, 13 of them twice over; that the segmentation finds 165 components against 161 letters on the crib. Not checked: the Marburg-style question of whether the
originals differ from the microfilm; any printed edition; the remaining homophones. User must verify: every
reading here comes from a microfilm image and is unvalidated; the palaeography of "calzolite / calzolari"
and of the docket on f. 123v is uncertain, and the identification of the box glyph as *f* rests on one word.
