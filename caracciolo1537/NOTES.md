# Cardinal Caracciolo (Milan) to Charles V, 14 November 1537 (AGS Estado leg. 1184 fol. 110; DECODE R9966) — NOTES

Status: read

**Verdict: read (96% of plaintext letters, measured: 453 read, 18 unread; second pass 21 Sept 2026), with Wanruo Luo's Cifrario 38, unchanged.** Catalogue
entry for DECODE R9966 is resolved and removed. Worked in one session on 2026-09-21.

## The document

DECODE R9966, 4 images (`rec9966.htm`). The images were fetched with the shared cookie into the main checkout's
`caracciolo1537/img/` and are git-ignored. DECODE's image order is not the archive order:

| DECODE image | AGS scan | content |
|---|---|---|
| P4 | 0408 (f. 110r) | "Sacra Cat.ca & Ces.a M.ta". Clear Italian: the Dauphin and the Grand Master crossing into Italy, the King at Briançon, Marnol and the Colonel of the Isola recalling the Swiss in French service |
| P1 | 0409 (f. 110v) | clear text on the Grisons, then 11 lines of cipher |
| P3 | 0410 (f. 111r) | one cancelled cipher line, then clear: the Duchess's departure; dated "In M.lo ali xiiij de Nov.e M. D. xxxvij", signed "il Car.l Caracciolo" |
| P2 | 0411 (f. 111v) | address "Sacre Cat.ce & Ces.e M.ti", docket "A Su Mag.d del Cardenal Caracciolo xiiij de Nov.e 1537", foliation 110 |

The letter is in Italian. Its clear parts are not ciphered and are not transcribed here beyond what frames the cipher.

## The cipher and the key

- Luo (2021), *El lenguaje cifrado de Isabel de Portugal (1530-1539)*, PhD thesis, Universitat de València
  (RODERIC, PDF p. 665 = thesis p. 657): **Cifrario 38**, "cifrario mixto, usado por Carlos V y Protonotario
  Caracciolo entre 1530-1538", reconstructed from AGS Estado leg. 38 doc. 190. The PDF was downloaded to the main
  checkout's `caracciolo1537/prior/` (not committed).
- System: a homophonic alphabet (a has six signs; e: n+, Eo, n, 9-with-hook; i: E, et, n; l: a, ap, P, θ;
  n: t, Eo, ~w; o: S, to; p: 9, 9-with-bar; r: ♀; s: 6; t: 3; u: ʃ, 8; z: ∿), plus a syllabary in which a base sign
  for the consonant takes a superscript digit for the vowel: **5 = a, 6 = e, 7 = i, 8 = o, 9 = u**. Bases:
  b a̲, c a+, d a̲o, f ap, g e̲, h et, j e̲o, l P, m o̲, n ꝑ, p ♀, q n̲, r n̲o, s 2, t 4, v 3, y 3x, z ʄ.
  Signs with superscripts 2, 3, 4 (and a few others) are nulls. ll = R. Code words: Génova bru, Rey sen, Su
  Magestad te.
- The key read the letter from the first line with no change. Line 1: 2⁷ a̲o⁸ 3⁶ + 9 n̲o⁵ θ 4⁷ a+⁵ n̲o⁶ ♀⁶ ♀
  o̲⁵ ♀ ꝑ⁸ a 2⁶ 3⁸ P⁶ 3⁵ ꝑ⁸ a+⁸ t a+⁸ ♀ a̲o⁵ ♀ 2⁶ = si dove a practicare per Marno a se volevano concordarse.

## The reading

`reading.txt`. In short: Caracciolo explains how Marno (the imperial agent with the Swiss) was to be dealt with:
treat with the Swiss if they would come to terms, as with the Suizari; he has written several times to Marno to
send Panizone in his name and pay him; the Grisons at Como are to be offered terms gratis "facendo capituli
convenienti"; so far Marno has had no passage for the Grisons; Marno now "se accorge hora de la malignita et
perfidia" of the Swiss and their ministers.

The names are given as the cipher spells them. "Marno" is read in the clear f. 110r as "Mons.or di Marnol".

## Prior solution (contamination question)

- Tomokiyo, cryptiana "Spanish ciphers during the reign of Charles V", Luo update section (copy in
  `vasto1527/prior/spanish2C_now.htm`): "This can be read with Lu.38. Those versed in Italian will be able to
  complete the deciphered text", with a reading of the first four lines ("solo si dovea practicare per marno a se
  volevano concordarse como erano suizari et in tal caso ho scripto piu volte a Marno a che manda il panizone in mio
  nome et pagabo quale e a e f ressolvi perche io se r ri a conbento ...."). Found before the reading, and it pointed
  to the key. His lines 1-4 were confirmed (pagabo → pagato, conbento → contento). Lines 5-11 are read here.
- Luo does not edit this letter (full-text search of the PDF for 1184, Marno, Panizone, Grisoni: nothing).
- There is no decipherment on the leaves.

## Second pass (21 Sept 2026)

Every line re-read at 4x with autocontrast. Three rules settled most of the first pass's gaps:
- A superscript belongs to the sign **before** it (it is written as an exponent). In line 5 this gives 3⁶ 4⁷ et =
  *ve ti i*, so "a Elvetii" (the Swiss), not "tte hi".
- A bare ♀ is the letter r; ♀ with a superscript is the p-syllable. Line 8: et⁵ ♀ n̲o⁷ + ꝑ⁸ = *ha r ri a no* =
  "harriano" (would have); line 7: ♀⁵ ♀ 2⁸ = *pa r so* = "parso".
- The g-shaped sign with a bar is an f homophone: line 6 "del frumento". "La tracta del frumento gratis" is the
  duty-free grain export licence offered to the Grisons.
- Dotted signs are nulls (line 5 "#·"); the hooked 9 is an e homophone (line 4); line 11 3⁸ a 4⁶ = "volte".
- The cancelled line continues line 11: "far-/riano quello hora fan po[..]", then a run of null-marked signs.

## Remaining signs

About 10 of roughly 330 cipher signs (estimated, no sign-by-sign count), listed in `reading.txt`: 'a fe' and
'serria' in line 4, two a-homophones in line 5, one sign each in lines 7 and 8, '2 a' in line 10, one syllable in
the cancelled line. None blocks the sense.
