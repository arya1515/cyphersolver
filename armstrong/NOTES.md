# Armstrong -> Madison 1808 (the "outlier" code) — cryptiana unsolved item #2

Two distinct problems on cryptiana's list under Armstrong:
1. **Postscript in code, 30 Aug 1808** (Founders 99-01-02-3466): 49 groups in Armstrong's usual **THE=972**
   code. cryptiana partially decodes it. THIS is tracker item #2.
2. **Letter of 20 Feb 1808** (Founders 99-01-02-2728): ~380 groups in a *different, unique* code,
   genuinely unsolved. A 2025 AFIO-contest solution (Apelbaum) is disputed by Tomokiyo.

## Sources gathered
- Full ciphertexts pulled from Founders Online (via Wayback: Founders blocks the scraper). See `wb_*.html`.
- **Rosetta**: DUSMF microfilm M34 roll 13 (NARA naId 188671172, "Nov 12 1804-Dec 27 1807"), 393 images in
  `img13/`. Several Armstrong despatches there are written in THE=972 with the State Dept clerk's **pencil
  decode above each cipher number** (esp. images 0196-0201). These are a running plaintext<->number key.
- cryptiana's own partial THE=972 table (from the known-plaintext 4 May 1806 letter) harvested to
  `code972_partial.json` (227 entries), the authoritative base.

## Status of the 30 Aug 1808 postscript — SOLVED (2026-09-14)
Ciphertext checked against the LOC manuscript (mjm reel 10, fr. 0521; `loc_0521.jpg`, crop `loc_0521_last.png`):
Founders prints **1218** where the MS has **1216** (= an); the 4th-line group is 1319 (li), not 1391.

> **P.S. Rus-s-el ought to be the consul: he is an American by birth, and is much better qualified than
> any other candidate. In a word, he is above men in general. Next to him in fitness is O'Mealy, but he
> is, like Warden, an Irishman.**

Group-by-group (`decode972.py ps`; H = pencil interlinear, C = cryptiana 4 May 1806, * = inferred here):
```
1394 ru*   1116 s    1273 el*   250 ought*  1165 to   1405 be   | 972 the  148 consul  1459 he  1482 is
1201 a     821 n     130 America 821 n      | 1429 by  720 bir*  970 th   | and | 1482 is | much better |
992 qua*   1319 li   1048 fi(ed)* 584 than  687 any   249 other 736 can  1013 di  750 da  967 te |
In a word | 1459 he  1482 is  1202 above  1561 men | in general. Next to | 927 him  1090 in  1052 fit
832 ness   1482 is   934 o     510 mea     860 ly    | but | 1459 he 1482 is |
1320 like* 384 ward* 1280 en   1216 an     1481 ir   1483 ish*  555 [man]
```
Evidence for the inferred groups:
- **1394 = ru**: 22 Feb 1808 letter "972 1394 1090 1354 946 985 608 899" = *the ru-in of Gu-sta-va-us*
  (Gustavus IV, Sweden); roll-13 sheet 0194R10 "417 1394 910" under pencil *Yrujo* (Y-ru-jo); sheet
  0201L12 "1292 1394 876" under *Etruria* (Et-ru-ria). Earlier sessions took the clerk's pencil dash over
  1394 as a "null" — the dash is his continuation mark for syllables of a word already written.
- **1273 = el**, **250 = ought**, **720 = bir**, **584 = than**, **1320 = like**, **384 = ward**, **1483 = ish**:
  each sits in the right alphabetical slot of its block (1272 eight < el < 1279 Emp; 249 other < ought <
  252 own; 719 Ba < bir < 723 bo; 582 ted < than < 585 their; 1319 li < like < 1325 long; 383 w < ward <
  385 was; 1482 is < ish < 1484 it). 1483 = ish is also forced by "752 1483 61" = *Dan-ish Minister* (22 Feb).
- **992 qua / 1048 fi(ed)**: 993 = qui; 1046 fi, 1050 fi, 1052 fit bracket 1048.
- **555**: = *re* on sheet 0195R5 (1120 555 = *sco-re*), which makes no sense after *Irish*; 1555 = *man*
  (H, twice on the same sheet). Read as Armstrong's slip for 1555. (Alternative: "an Irish re—" cut off.)
- **O'Mealy** = Michael O'Mealy, Baltimore merchant resident in France since 1793 (PJM-SS 10:497 n.2).
  **Warden** = David Bailie Warden, Irish-born secretary of legation, whom Armstrong opposed for the Paris
  consulate (cf. Armstrong to Madison, 3 Mar 1811: "not a single grain of attachment to the U.S.").
  **Russel** = presumably Jonathan Russell (R.I. merchant trading to Europe; chargé at Paris 1810).
  Letter body: "my opinion of the fitness of M. Warden for the consular office at Paris" — the PS is the
  candid ranking Armstrong would not put in clear.

## Bonus: 22 Feb 1808 letter (Founders 99-01-02-2733), largely read with the same table
"The ruin of Gustavus is at last resolved. Russia is to seize Finland, while France & Denmark take
possession of Sweden. Denmark cannot ha[ve] very willingly … independence … [it has] … her … of her … and
[like]wise … of conduct and thrown her completely into the arms of France, while the Danish Minister was
this morning pouring out his complaints to me upon this subject, and stating the [dread?] of his government
and the means taken by it to avert the introduction into Denmark of a general army … of Hamburg waited in
the antichamber … Yet wonderful to tell, Russia not only does not [oppose?] … [but] actually assists him
in accomplishing one half of the object … a state of the most complete … "  (`decode972.py feb`).
Fresh readings from it: 297 resolve, 946 Gu, 26 Denmark, 758 dep, 825 nce, 1224 arm, 1257 duct, 752 dan,
1572 morning, 396 while, 943 upon, 193 govern, 1082 rt, 305 Russia, 947 only, 765 does, 1132 sist,
655 pli, 1126 sh, 917 half. Some Founders digits there are suspect (631 for 651 *plain*; 916 for 921 *have*).

## Files
- `decode972.py` — merges `code972_partial.json` + `pairs.txt` + inferences; `python decode972.py ps|feb|all|table`.
- `pairs.txt` — ~500 number→syllable pairs harvested from roll-13 pencil decodes (sheets 0194–0201).
- `loc_0521.jpg`, `loc_0522.jpg` — LOC master images of the letter (tile.loc.gov/storage-services/master/mss/mjm/10/0500/052x.jpg).
