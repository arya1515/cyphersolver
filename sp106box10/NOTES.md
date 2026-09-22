# TNA SP 106/10 — a codebreaker's worksheets and the intercepts they belong to (DECODE R657, R660, R664, R704, R720, R721, R722; key R725; also R656, R662 (catalogue 58); worksheets R658, R661, R663, R667, R684, R701, R702)


Status: in progress (R722, the 1625 Venetian letter found 2026-09-21, and systems A-C are not yet decoded through).
Outcome: read in part (2026-09-20). The seven records shown to be one case and dated to 1623-24; the codebreaker's
own key (R725) transcribed in full and the system explained; about 45 values of the three-figure code rebuilt and
phrases read. Neither long letter is read through yet. Written up as `docs/sp106box10.html`.

Update 2026-09-21 (catalogue id 62): the seven further "unknown to unknown" records R658, R661, R663, R667, R684,
R701, R702 are more sheets of the same file. R658 is the codebreaker's own grid of the three-figure code, which R701
calls **"the Venetian Cifer"**; with it the code is rebuilt as a systematic syllabary (117 values in
`cat62/venetian_code.tsv`, 102 written by the codebreaker, 15 predicted), and three values in the section below are
corrected (260 ta, 262 ti, 263 to, 459 r). A second three-figure code is worked on R667/R684/R701 p.3/R702 p.1: that is the lost 46-line letter of the R703
section above. See "Catalogue 62" at the end.

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
| R722 | TNA_SP106/10_UND_(0193-0195) | 3 | intercept: **the 1625 Venetian letter in the second three-figure code** (catalogue 58 section), not system C |
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

## Catalogue 62: the rest of the file (R658, R661, R663, R667, R684, R701, R702), 2026-09-21

Catalogue entry 62 ("Unknown sender to unknown recipient, 7 ciphertexts", DECODE R658-R702) lists seven more
records from the same box and the same hand. None of them is an intercept. They are the codebreaker's work
sheets, and two of them hold his solved tables. Images fetched as before (`cat62/img.py`, cookie; git-ignored).

("Second code" = the three-figure code of the lost 46-line letter, R703 section above.)

| record | ff. | what it is |
|---|---|---|
| R658 | 125 | **The Venetian code grid.** Every group 136-565 set out in columns by hundreds, with his count of occurrences under each and his value over it; a side list of word groups (238 esser, 349, 369 nostro/nostra/nostre, 411 qui, 430 passato/passata, 467 questo, 568 vostro, 440 Spagn-). Upside down in the scan. |
| R661 | 141-143 | An English political draft in clear ("It may bee evident to all men that frame judgment of affaires… to cutt of that supply of treasure that the K. of Sp. hath for the Indies… Portugall…"), reused: three-figure lines of second-code in the margin, and on p.2 numbered lines of the intercept (l. 1-38) with his trial words ("il Re", "lo haveva", "bisogno", "allora che come"). |
| R663 | 20 | Italian syllable drills (ba be bi bo bu, baba bebe…) and an Italian-English word list (Laicale, Lambiccare "to distill", Lasciare "to permitt"…), with a few second-code groups. |
| R667 | 164-166 | **Second-code count grid**, groups 200-577 in ruled boxes with occurrence counts and a few values (244 ra, 245 re, 246 ri, 247 ro; 540, 541 dal, 542 del, 543 dil); p.2 a dictionary trawl for words in *gra-/gua-* and trial syllable patterns. |
| R684 | 170-171 | Second-code: lines of the intercept (l. 2-27) with trial syllables; groups by frequency ("3 times", "9 times", "13 times", "15 times": 244 fifteen times); trial pairs *da ba, da ca, da fa…* |
| R701 | 175-177 | p.1: a syllabary (Ba Be Bi… Sta Ste…) and **"Wordes marked with letters in the Venetian Cifer: 369° nostro, 340° misura(?), 467° questo, 369ᵉ nostre, 420' altri, 233ʳ esser, 121ᶜ, 430ᵃ passata"**. p.2: a short text in a letter cipher (below). p.3: second-code values in runs (366-370 la le li lo lu; 375-378 da de di do; 209-213 va ve vi vo vu; 231-235 sa se si so su; 333-336 cha che chi cho; 322-326 pra pre pri pro pru; 510-514 sta… ; 244 ri, 245 re). |
| R702 | 181-182 | p.1: Italian-English dictionary trawl (Bala-, Cola-, Fala-, Mala-) against numbered lines of the second-code intercept (li. 25 `495 391 540 395 207` "a ta n do"; li. 32, 38, 42, 44). **p.2: system B phrases with his glosses** (below). |

### System B = "the Venetian Cifer", rebuilt

R701 p.1 names the three-figure code with superscript word-endings "the Venetian Cifer", and those words (369
nostro, 467 questo, 430 passato) are the ones on R658's side list, so the grid R658 is that code, the code of R664
and R660. The grid shows it is a **systematic syllabary**: each consonant takes five consecutive rows in the order
a e i o u, and each hundreds column a different consonant:

    row  x51-x55: 1 ra-ru   2 sa-su   3 sca-scu  4 stra-stru  5 sta-stu
    row  x42-x46: 1 na-nu   2 pa-pu   3 ?        4 pra-pru    5 qua-quo
    row  x60-x64: 1 ?       2 ta-tu   3 tra-tru  4 va-vu      5 za-zu
    row  x56:     a  e  i  o  s(?)     x57-x59: single consonants (157 b, 257 f, 357 l, 457 p; 158 c, 258 g, 358 m, 458 q; 159 d, 359 n, 459 r)
    x33-x37: 4 la-lu, 5 ma-mu;  x15-x19: 3 ca-cu, 5 da-du;  words: 339 liga, 340 lettere, 439 per, 165 che, 465 quel

A word group takes a superscript letter for its ending (369° nostro, 369ª nostra, 369ᵉ nostre): these are the
"wordes marked with letters". The table is in `cat62/venetian_code.tsv` (grade H where the codebreaker wrote the
value, P where only the pattern predicts it).

**Check.** `cat62/check_r702.py` decodes every group string the codebreaker glossed on R702 p.2: 46/46 groups
fall in the table, and each string gives his gloss:

    356 318 436 143 435   i co lo ne li      "i colonelli"
    341 433 436 154       del la lo ro       "della loro"
    252 359 518 253       se n do si         "sendosi"
    167 252 459 [459] 253 con se r (r) si   "conservarsi"
    165 245 556 253 156 526 445 534 261 459  che po s si a mo pro me te r  "che possiamo prometter"
    260 359 263           ta n to            "(in) tanto"
    260 261               ta te              "(capi)tate"

He also glossed "di 24 di maggio", "del campo", "per nome suo", "sono capitate", "nol portar", "efficacia",
"medesime conciette" on the same sheet: the letter he was reading dates from late May and speaks of a camp and of
colonels, which fits 1624 (Mansfeld's levies) or 1625 but is not proof.

**Corrections to the 2026-09-20 values** (from gloss alignment on R664 alone): 260 is ta (not "mento"), 262 ti (not
to), 263 to (not ti), 459 r (not v), 411 is qui in the grid (R664 gloss "que"); 316 "ta" does not fit the
ca-cu run 315-319 and is doubtful.

### Which code is "the Venetian Cifer"? (reconciling with the R703 section)

The R703 session, working the same day in parallel, read R701's heading as naming the code of the lost 46-line
letter. The heading's words, though, are the words of R658's side list (369 nostro/nostra/nostre, 467 questo, 430
passato/passata), and R658 is the grid of the R664/R660 code (111-568: 152 re, 154 ro, 165 che, 560 za, all fixed on
R664). The lost letter's table (R701 p.3: 244 ra, 245 re, 366-370 la-lu) is a different table (R658: 244 pi, 245
po, 433-437 la-lu). So the label belongs, on the evidence of the sheet itself, to the R664/R660 code; the lost letter
is in a second table, perhaps a later key of the same Venetian correspondence. Either way, both are three-figure
syllabaries built the same way (consonant runs with the vowel in the last digit).

### The second three-figure code (the lost letter)

R667, R684, R701 p.3, R702 p.1 and the R661 margins work a different code: groups 200-599, the same syllable read
in several series (do = 207 and 378; a = 495 and 430?), laid out in ascending runs (366-370 la-lu, 209-213 va-vu,
231-235 sa-su, 333-336 cha-cho). The intercept it belongs to is the lost 46-line letter of the R703 section and is not among the
imaged records; only its line fragments survive here, glossed as trial syllables. Not read.

### R701 p.2, a short letter cipher

    Esg frp rohxog x rygo fa ombhpeip / nb waltmg bxdos ipdlts kd kek rxiro /
    ids pydo pnydquosdpr np oi ia / xohocfog frp bhpeocfscu kssp ttmoh / tt aal

(ε and δ-shaped letters transcribed E/d.) The codebreaker underlined the repeats *frp … frp* and *rygo / pydo*. A
one-to-one substitution annealed against Italian, English, Spanish, French and Latin models (`cat62/mono701.py`)
gives nothing: not a simple substitution as transcribed, or too short. Open.

### Outcome for catalogue 62

Explained: all seven records are worksheets of the SP 106/10 codebreaker, not intercepts; two are his solved
tables, which rebuild the Venetian code of R664/R660 and correct it. No new letter is read through. Catalogue id
62 removed. Open: the second code and its missing intercept (see the R703 section), the R701 p.2 letter cipher, R661's English draft (not
identified).

## Remaining gaps
- R664 ff. 1-3 and R660 (system B, the Venetian code) continuous reading - blocker: not-attempted; code rebuilt to 117 values from R658, the letters never decoded through with it
- R704, R721 (system C letter-plus-figure syllabary; R722 turned out to be the second three-figure code) - blocker: not-attempted; the codebreaker's interlinear solutions exist, no alignment pass done
- R657 worksheets (system A) against key R725 - blocker: not-attempted; listed under "Not yet done"
- R722, the 1625 Venetian letter in the second three-figure code (found 2026-09-21; fragments on R656, R661, R667, R684, R701 p.3, R702 p.1, R703, R720) - blocker: not-attempted; code rebuild from the full intercept plus the worksheet glosses not yet done
- R931 (1645 royalist numerical code, catalogue 58) - blocker: key-missing; Lasry's SP 106 keys and the Culpeper 1645 key do not fit
- R701 p.2 short letter cipher - blocker: too-short; about 120 letters, simple-substitution annealing in five languages gave nothing
- sender, recipient and codebreaker - blocker: not-attempted; depends on the continuous readings

## Escalation
- [x] siblings: R657-R725 and the catalogue-62 worksheets R658-R702 all opened and placed
- [x] clear-pages: the codebreaker's interlinear glosses on R664 and R702 p.2 aligned (46/46 groups)
- [x] known-keys: R725 key and the R658 grid applied
- [ ] print: not done — CSP Venice vol. 18 (1623-25) and CSP Domestic 1623-25 not searched for these letters ("di 24 di maggio", colonels, "la loro sicurezza")
- [x] key-rebuild: Venetian code rebuilt as a systematic syllabary (cat62/venetian_code.tsv, 117 values)
- [ ] retry: not done — decode R664 and R660 in full with venetian_code.tsv, and align system C's glosses on R704/R721/R722

## Catalogue 58: R656, R662, R722, R931, and the "lost" letter found (2026-09-21)

Catalogue entry 58 ("Unknown sender to unknown recipient, 4 ciphertexts", DECODE R656, R662, R722, R931) grouped four
unrelated SP 106/10 records by their shared "unknown" metadata. Images and DECODE texts fetched with the cookie
(`../sp106c58/decode/` in the shared checkout, git-ignored).

**R722 is the "lost 46-line intercept" of the second three-figure code, and it is not system C.** The notes above
(and DECODE's pointer "704; 720; 721") put R722 with the letter-plus-figure records; no one had looked at it. Its page 2
line 1 ends `540 212 una di questi matine`, the fragment R703 quotes as `l.1 540 212 una che`; line 3 carries
`280 367 464 432` (R720 `l.2`), line 6 `340 367 misciandosi` (R703 `l.6 340 367 misciendosi`), line 8 `245 510 Almeno`
(R684 `l.7 … 510 al meno`), line 15 `297 506 395 … e che quello` (R703 `l.14 297 506 395 e che quello`); the
codebreaker's line count runs one behind the page's written numbers in places (he seems not to count a half line). It has 48
numbered lines (DECODE: "48 in sum total, roughly 500 codegroups"), written half in clear Italian, half in groups
200-599, with the codebreaker's trial syllables between the lines. The endorsement (p.1, f.195v) reads:

> **"Cypher of a Venetian Secretary to the Embassador of that nation in …"**, and on the fold "1625".

The clear passages give the letter's matter: *Parmi che …*, *Io mi credo che questi siano …*, *Ho visto chiaramente
che V. E. …*, *Il S[igno]re … di dire a V. E. che … gran pratica*, *proposito che ella procurasse*, *di satisfattione
con honor di …*, **il Spinola sotto Breda**, **di Bruselles si è inteso …**, *di Roma*, and a Pontifical figure
(*Pontificio … il quale disse … di voler esser …*). Spinola's siege of Breda ran from August 1624 to 5 June 1625, so the
letter is of the first half of 1625: a Venetian secretary (plausibly in the Low Countries or at Rome) writing to the
Venetian ambassador in England. This also settles which code is the Venetian one: **both** three-figure codes of the
file are Venetian, and the "second code" is that of this 1625 letter. Transcription: `cat58/r722_transcription.txt`
(lines 1-15 group by group; 16-48 the clear passages and the quoted fragments, line numbers approximate).

The code is not broken here. R701 p.3's partial key and the codebreaker's glosses conflict (see above), and the
clear context is enough to fix only a few values. With the full intercept now in hand, a gloss- and context-driven
rebuild of the second code is the next step: every line fragment on R656, R661, R667, R684, R701-R703, R720 can now be
checked against its source line.

**R656** (f. 67, 1 p.): the back of an English Exchequer draft (a sheriff's answer about "the yearly value of 90li et
16li", "the Remembrancer", "the said Sheriff", "Wm Nosse, Roger Rowley, Robert Sherborne and Thomas Franke"), reused
by the codebreaker for more second-code fragments by line: `l.16.17 350 541 513`, `l.21 350 495 395 207`,
`l.11 350 273 463 353`, `l.27 541 442 215 444`, `l.23 541 449`, `l.12 313 541 377 238 254`, `l.25 542 204 395`,
`l.38 495 541 280 495 201`, `l.10 254 513 350`, `l.15 495 391 541 364`, `l.42 446 540 395 377 290`, and at the head
`l.7 350 446 432 494 347 395`. These are R722's lines (l.12 `313 541 377 238 254` is R722 line 12 verbatim). DECODE's
"ten lines of ciphertext between lines of cleartext… unlikely that the cleartext is the solution" is right: the English
is an unrelated legal draft. **Explained.**

**R662** (f. 8, 1 p.): a torn vertical strip of the codebreaker's own English memorandum on how the code is built,
not a letter: "… series of sillables beginning …", "… places out of the series …", "… entire words …", "436 is like to
be …", "297.436 n no seemes to …", "anno / diranno", "247.367.24x vo le va", "another series of …", "every series doth
begin …", "the vowels a.e.i. for every consonant", "n.r.o.", "commonly m. 540", "doth turne at 3", "the most frequent
… di …", "may beginne at". It describes a syllabary in consonant series with the vowel stepping in the last digit,
which is the second code's layout (R701 p.3 runs 366-370 la-lu, 209-213 va-vu). DECODE's "mid 17th century" and "mostly
solved" are wrong: it is the 1625 codebreaker's note. **Explained.**

**R931** (f. 251, 1 p.) is unrelated to the 1623-25 file: a strip of ~190 numbers 10-260 with clear words ("(1)
septembre 1645", "earnestly", "reasons", "from", "(2)"), an English royalist letter of September 1645 in a numerical
code (104 distinct numbers in 192 tokens: a nomenclator, not a letter cipher). Tried and failed on it: all of Lasry's
1645-46 SP 106 keys (TNA SP 106, SP106-2, -5, -8; the June 1645 Goring key of the next record R932; coverage ≤ 0.45,
gibberish), and the Charles I → Culpeper 1645 key (BL Add MS 32256 f. 6-7, DECODE R9117/R9118: letters 1-78, words
300-600, nothing in 100-260). **Attempted, open**; needs the matching key (Digby / Nicholas / Goring correspondence
of autumn 1645, BL Add MS 32256 ff. 4-9 or Egerton 2550).

### Outcome for catalogue 58

R722 identified (the file's missing 1625 Venetian intercept, endorsement read, clear passages read, dated by Breda);
R656 and R662 explained (worksheet fragments of R722; the codebreaker's memorandum on the code); R931 attempted, open.
Catalogue entry 58 is narrowed to R931.

### R722: full transcription and a first attack on the code (2026-09-21, later)

`cat58/r722_groups.txt` now holds all 48 lines: **420 groups, 117 types**, plus the clear Italian. Line 45-46 adds
*"… soliti concetti del Pontifice il quale disse a Bethune di voler esser risarcito di 150 m[ila] …"*: Philippe de
Béthune, French ambassador in Rome, and the Pope's demand to be compensated (the Valtelline forts, 1625). The writer
relays Rome and Brussels news to "V. E.", the Venetian ambassador.

Fixed values (C = confirmed by clear context):
- crib, line 24: *che* **525 245 541 449** *lo haveva assecurato* = *che il Re glie-lo haveva*: 525 il, 245 re, 541 gli,
  449 e (C);
- line 8: **245 510** *Almeno* = *resta. Almeno*: 510 sta (C), matching R701 p.3's 510-514 sta-stu;
- 334 che (C: R701 p.3 333-336 cha-cho, and the codebreaker glosses 334 "che" throughout).
R701 p.3's table therefore belongs to this letter and is right where it can be checked: 209-213 va-vu, 231-235 sa-su,
244 ra, 245 re, 322-326 pra-pru, 333-336 cha-cho, 366-370 la-lu, 375-378 da-do (377 di, 9 occurrences), 510-514 sta-stu.

`cat58/solve722.py` anneals the remaining groups against `it-cinquecento` (5-gram, per-character baseline, at most
two groups per syllable, bonus for R701-style runs of five). Four configurations were run (free; length-normalised;
R701 values fixed; R701 fixed + strong run bonus + no word groups), 12-20 restarts of 400k steps each. **Failed**: every
restart ends in different Italian-sounding word salad, and no two agree beyond the fixed values. With about 70 free
groups over 420 tokens the text does not determine the code. The codebreaker's own trial glosses on R722 disagree
with each other and with R701 p.3 in places, and he did not break it either.

What would move it: (a) another letter in the same code (the Venetian correspondence of 1625, ASVe or SP 99 at Kew);
(b) the rest of the table, if more of R701-style run sheets survive among the unimaged SP 106/10 leaves; (c) a
careful pass fixing only values forced by clear-text junctions (line ends before and after clear passages), then
re-annealing.
