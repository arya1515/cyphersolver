# TNA SP 106/10 — a codebreaker's worksheets and the intercepts they belong to (DECODE R657, R660, R664, R704, R720, R721, R722; key R725)

Outcome: read in part (2026-09-20). The seven records shown to be one case and dated to 1623-24; the codebreaker's
own key (R725) transcribed in full and the system explained; about 45 values of the three-figure code rebuilt and
phrases read. Neither long letter is read through yet. Written up as `docs/sp106box10.html`.

## The group

DECODE lists these as seven separate "partially decrypted" ciphertexts in TNA, State Papers 106 box 10,
dated only by the volume span "1558/1625", sender and recipient unknown, plaintext Italian/Spanish/French.

| record | shelfmark stub | pp. | DECODE note |
|---|---|---|---|
| R657 | TNA_SP106/10_UND_(0128-0138) | 9 | "clearly the worksheet of a codebreaker" |
| R660 | TNA_SP106/10_UND_(0139-0140) | 2 | intercept, 15 lines, solutions written above the code |
| R664 | TNA_SP106/10_UND_(0167-0169) | 3 | intercept, ~500 codegroups, 45 lines, partly solved |
| R704 | TNA_SP106/10_UND_(0186-0187) | 2 | intercept, 46 numbered lines, ~700 codegroups, letter-indicator "3" |
| R720 | TNA_SP106/10_UND_(0188-0189) | 2 | worksheets, probably for R704 |
| R721 | TNA_SP106/10_UND_(0190-0192) | 3 | intercept, 26 numbered lines, ~300 codegroups |
| R722 | TNA_SP106/10_UND_(0193-0195) | 3 | intercept, like R704 and R721 |
| **R725** | TNA_SP106/10_UND_(0202-0203;0205) | 3 | **key**: "Alphabet of Letters and Wordes" |

R725 is catalogued as a key record and was not part of the goal's list; it is the reconstructed key the
same codebreaker wrote out, and it unlocks the group. Images fetched from DECODE with the project cookie
(git-ignored in `img/`; rotated working copies in `rot/`).

## The cipher, as the contemporary codebreaker set it out (R725 p.3)

R725 p.3 is the codebreaker's fair summary, in four headed columns:

1. **"Alphabet of Single Letters"** — plain two-figure groups:

   A 10, 11 · B 31 · C 41 · D 25 · E 20, 90 · F 21 · G 51 · H 71 · I 30 · L 81 · M 91 · O 40 · P 42 ·
   Qu 72 · R 22 · S 94 · T 92 · V 50 · Z 93 (X blank)

   (R725 p.1, the rougher draft, has D 29, O 40, V 90 and "X. Z. & serve to bee Nulles" — the p.3 values
   are the corrected ones.)

2. **"Alphabet of letters that are woordes"** — single *letters* used as whole words:

   a = per · c = di · d = da · f = dal · g = il · h = in · n = ma · p = se · q = et · r = con ·
   t = non · v = chi · x = si · z = che  (b, l, m, o, s and & left blank)

3. **"Literarum resolutio"**, with the decisive note in the codebreaker's own hand:

   > "It seemes there are numbers of woordes expressed by this difference of — over the figures whereof in this Cifar."

   i.e. **a bar over a two-figure group makes it a word** from one nomenclator; the plain group is a letter.
   Values he had recovered: 11 tanto · 16 lettere · 18 relatione · 20 spedditione · 26 V. Signoria ·
   27 V. Paternità · 29 Sua Signoria · 30 uno · 37 Re d'Inghilterra (R725 p.1 writes "Re di Britania") ·
   42 Padre · 52 liga · 70 hay(?)

4. **"An Alphabet of Characters thus marked 10' 11' etc."** — a *third* series, marked with a tick/dot
   above the figure. "In these letters ycncontred":

   22 Il Principe · 23 Marques Inichiosa · 24 Imbassiatore di Venetia · 28 Imbassiatore · 32 Roma ·
   34 Palatinato · 49 Cattholico · 50 Stato · 57 Negocio or Occasione · 66 acciocche · 67 C. Barberino /
   andare(?) · 69 Governo · 71 havere · 73 habuto · 77 mento · 80 perche · 82 in cio · 84 questo or questa ·
   85 quello or quella · 89 tutte · 90 Papa · 91 Nuncio  (series runs 10–99; 16 liga on p.1)

So: **two-figure groups, Italian, three readings distinguished by the mark over the figure** — bare = single
letter, barred = word list 1, dotted = word list 2 — plus single alphabetic letters standing for common words.

## Dating, from the key's own vocabulary

DECODE gives only the volume span 1558/1625. The recovered nomenclature dates the group much more closely:
**Palatinato**, **Il Principe**, **Re d'Inghilterra**, **Papa**, **Nuncio**, **C. Barberino**,
**Imbassiatore di Venetia**, and above all **"Marques Inichiosa"** — the Marqués de la Inojosa, Spanish
ambassador extraordinary in England from spring 1623 to summer 1624. Cardinal Francesco Barberini was created
cardinal in October 1623. The intercepts therefore belong to **1623–1624**, the Spanish Match and Palatinate
negotiations, and the "codebreaker" is a servant of the English Secretary of State of those years, not Phelippes
(d. 1625) on the evidence so far.

## Next

- Read R725 p.2 (third key page).
- Transcribe R664 / R704 / R721 / R722 and apply the key; fill the gaps from context.

## The group is not one cipher but three

Working through the images shows the seven "ciphertext" records fall into three systems, all in the same
codebreaker's file:

| system | records | form | plaintext |
|---|---|---|---|
| A. two-figure nomenclator | R657 worksheets; key R725 | `10 11 31 41 …`, bare / barred / dotted | Italian |
| B. three-figure syllabic code | R660, R664; worksheets R720 | `533 359 515 …`, partly in clear | Italian |
| C. letter-plus-figure syllabary | R704, R721, R722 | `Z6 n54 m56 g42 … b41 b33` | Italian |

System A is the one R725 sets out (above). Systems B and C are different ciphers of the same case: the
codebreaker wrote his solutions **above the groups, syllable by syllable**, in all three.

## System B read in part (R664, R660)

R664 and R660 are letters written half in clear and half in code — the writer encodes only what matters and
leaves the connective Italian open, which is what made them breakable. R664 f. 1 lines 44 is wholly clear:

> "potrete continuare nel modo cominciato, osservando però il [mutamento … alle volte … col … numeri suppositi]"

— the correspondents discussing the working of their own cipher.

The code is **syllabic**: one three-figure group per letter or syllable. Values recovered here by aligning the
codebreaker's interlinear solutions against the groups (each confirmed by at least one unambiguous word):

    111 al    145 nume(ri)  146 nu    151 ra    152 re    153 tri   154 ro    165 che
    211 del   233 ?         240 et    245 si    252 se    253 si    254 so    255 sa
    260 mento 261 ta/te     262 to    263 ti    312 ?     316 ta    319 cu    320 in
    340 lette(re) 344 el    356 i     357 l     359 n     366 col   367 ?     411 que
    430 a     433 la        434 le    436 lo    439 ?     456 o     459 v     461 ve
    463 volte 468 quel(lo)  515 da    516 de    518 do    533 ?     535 mi    536 mol
    537 mu    542 quan      544 gua   560 za    568 vostre

Worked example — R664 f. 1 line 38 deciphers straight off:

    211 433 436 154 253 319 152 560 312 359 518 367 433
    del la  lo  ro  si  cu  re  za  ·   n   do  ·   la
    → "della loro sicurezza … -ndo … la"

and line 41: `240 | hoggi terzo giorno | 468 434 516 146 456 461 252 359` + line 42 `560`
→ "et hoggi terzo giorno quelle de nuovo senza…".

Enough of the code is fixed to show the letters are Italian, are about "la loro sicurezza", the cipher's own
working, dated letters counted by "il terzo giorno", and belong with the 1623–24 nomenclature of R725.

## R703 and a fourth letter: the "Venetian cifar" dossier (2026-09-21)

Catalogue entry 66 (DECODE R703, TNA_SP106/10_UND_(0184-0185), "worksheets of a codebreaker", Italian) was taken
up on its own and turned out to belong to this file. **It is not a letter and holds no text to read.** Both pages are
the codebreaker's working sheets on a three-figure letter of 46 numbered lines that is **not among the DECODE images**:

- **p. 2** (ff. 185) is a positional index, headed *linea*: every group from 200 to 399 with the lines where it stands
  (`201. 5.13.19.21.26.31.33`, `280. 2.6.9.20 ф 24.25`, `340. 6`), notes such as "201 is a finall sillable after an
  entire word", and counts ("201. 7 tunes", "297. 11 tunes").
- **p. 1** (f. 184, half written upside down) carries glossed fragments of that letter under "Finall sillables" and
  "Entire wordes assured by reiteration": `l.1 540 212 | una che`, `l.2 280 367 464 432`, `l.6 340 367 misciendosi`,
  `l.7 245 510 Almeno`, `l.14 297 506 395 e che quello`, `l.24 325 232 540 406 432`, `l.46 540 464`; and grids of trial
  syllables (*no a me pre / ple / ro-bo-bra …*, *resa resan resar …*) and trial words (*Rovere, Rogare, Rolare, Romano*).

The index and the fragments agree with each other (280 in line 2, 340 in line 6), and they are **not** R664 or R660:
211 stands in R664 line 38 but the index does not list line 38 for it, and 540 is *Spagnoli* in R660 but *una/n* here.
Nor is the letter in system C (R704 and its fellows R721-R724 are letter-plus-figure).

The same lost letter is worked on six other records in the box, which DECODE lists separately:

| record | ff. | what it is |
|---|---|---|
| R661 | 141-143 | fragments by line (`l.1`, `l.11`, `l.22`, `l.42 che 250 … 540 395 207 …`) with an English memorandum |
| R667 | 164-166 | tally grids of every group 200-599 by column (2xx/3xx/4xx/5xx) with counts, and trial syllable lists |
| R684 | 170-171 | "wordes … in this Cifer", frequency lists by line (`232. l.44.48`, `369. l.2.31`) and more fragments: `l.7 504 207 495 … 510 al meno`, `l.25 495 391 540 395 207` |
| R701 | 175-177 | **p. 1 headed "Wordes marked wth letters in the Venetian Cifar"**: 369º nostro, 340º misura(?), 467º questo, 420ⁱ altri, 233ʳ esser, 121ᶜ, 43ºª passata; a syllable table Ba…Sto. **p. 3 his partial key** (below). p. 2 a line of a different, letter cipher |
| R702 | 181-182 | fragments `li.25 495 391 540 395 207` "a ta n do", `li.32 495 464 491 540 244 436` "al re s ta ua no", `li.38 525 495 541` "si a te", `li.42`, `li.44`; and an Italian-English word list copied from a dictionary (Ballatore … Galante … Maladetto) |
| R703 | 184-185 | this record |
| R720 | 188-189 | fragments (`l.2 280 367 464 432 434`, `l.6 542 290 | 280 367 464 432`, `l.16 350 541 513 507`, `l.22 che 525 245 541 449`), trial words |

So **system B is the codebreaker's "Venetian cifar"**, and superscript letters on a group mark it as a whole word.
R720 belongs with this letter rather than with R664.

**His partial key (R701 p. 3)** is a syllabary with the vowel carried in the last digit:

    209 va 210 ve 211 vi 212 vo 213 vu · 231 sa 232 se 233 si 234 so 235 su · 244 ra 245 re
    333 cha 334 che 335 chi 336 cho · 322-326 pr- (pra … pru?) · 313 cu(?) 314 cn(?)
    366 la 367 le 368 li 369 lo 370 lu · 375 da 376 de 377 di 378 do · 510 sha(?) 511 she 512 shi(?)

It does not carry the fragments to a reading: of the 28 groups quoted on R703 it values four, and the codebreaker's
own glosses conflict with it (R702 li.32 glosses 244 as *ta*, the key gives *ra*; R703 glosses 540 variously as
*una* and *n*). He had not broken this letter when the file stops, and without the intercept itself (46 lines, ~500
groups) the fragments are too few for a reading here.

**Outcome for catalogue entry 66: explained, not read.** R703 is identified (a worksheet, not a letter), placed in its
case (the 1623-24 SP 106/10 file) and tied to six sibling records and the codebreaker's own name for the cipher. The
intercept may survive elsewhere in SP 106/10 or among the Venetian material of SP 99 / SP 106 and is worth a search
at Kew; with it, R701 p. 3 and the fragments would be a strong start.

## Not yet done

- Finish the gloss-alignment pass over R664 ff. 2–3, R660 and the R720 worksheets; the three-figure code can
  very likely be carried to a full reading of both letters, since the codebreaker glossed most of it.
- System C (R704, R721, R722) has the same kind of interlinear solution and should yield the same way.
- System A: R657's nine worksheet pages against the R725 key.
- Identify the letters' sender and recipient (the Venetian ambassador's, the nuncio's, or the Spanish
  ambassador's correspondence), and the codebreaker.
