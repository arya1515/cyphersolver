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

`key_partial.tsv` lists 17 glyph values with the evidence for each, 13 of them fixed by two or more
independent occurrences. The chain is: the interlinear gloss on f. 113r and the first line of the crib on
f. 124r both spell *capitaneo*, giving c, a, p, i, t, a, n, e, o and (from *un*) u; the second line of the
crib then spells *nominato* with the same glyphs for n, a, t, o and adds o, m, i. That the two letters,
written five weeks apart, use the same glyphs for the same letters is the check that the key is real.

What is **not** recovered: the full homophone set. Beyond line 1 and the word *nominato* the crib would
not align consistently under my transcription — at least two visually similar triangular glyphs and
several similar "3 / reversed-E / z" forms are not reliably separable on this microfilm at the
magnification available, and a value read as *c* in one line is demanded as *z* in the next, which cannot
both be true. That is a transcription problem, not a cipher problem, and it is where this attempt stopped.

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

## 5. The glyph pipeline: segmentation works, shape matching does not

Because no imaging libraries are installed, the pipeline was built in pure Python: `sips -s format bmp`
writes an uncompressed 24-bit BMP, which `glyphs.py` parses directly. `glyphs.py` does thresholding,
8-connected components and features; `glyphs2.py`/`glyphs3.py` add band detection from the horizontal ink
profile and merging of vertically stacked fragments; `glyphs4.py` does average-linkage agglomerative
clustering on normalised binary masks; `align.py` aligns a cluster sequence to a known plaintext by
iterated Needleman-Wunsch and reads off the key.

Run on the four-line crib of f. 124r (`./zoom.sh 128 4980 950 3650 560 cribfull 3650`), the results are:

| step | result |
|---|---|
| ink threshold | Otsu picks 153, which is paper; 130 is right, the paper floor being visible in the profile |
| text bands | 4 found, at y 34–75, 168–213, 310–352, 458–502: exactly the four cipher lines |
| components per line | 17, 48, 47, 53 = **165**, against **161** letters in the marginal decipherment |
| shape clustering | fails |

The segmentation is therefore good enough: the line detection is exact and the component count is within
about 3 % of the letter count, which independently confirms that the cipher is letter-for-letter. The
clustering is what fails. Aligned against the known plaintext, the best mapping is consistent for only
62 of 160 aligned positions (39 %), and single clusters absorb up to 29 glyphs spread over 12 different
letters.

The cause is measured, not guessed. On line 1, whose reading is known by eye (tie mark, then
u n c a p i t a n e o s u i), the pairwise Jaccard distance between normalised 16 × 16 masks is 0.41–0.50
for the closest pairs and 0.60–0.83 for unrelated ones. Same-letter pairs are therefore only marginally
closer than different-letter pairs, and no threshold separates them. Bounding-box normalisation plus
ink-density masks is too crude for this hand at microfilm resolution: stroke weight, the slant, and broken
or touching strokes dominate the distance.

What would fix it, in order of likely payoff: stroke thinning and shape-context or Zernike features rather
than raw masks; translation- and slant-tolerant matching; supervised templates seeded from the two
contemporary decipherments instead of blind clustering; and, above all, better images than a 1960s
microfilm. None of that was attempted here.

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
