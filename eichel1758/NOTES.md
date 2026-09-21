# Eichel 1758, TNA SP 106/7 (DECODE R595), catalogue 65

Status: explained. The sheet carries no message: every group is a null, or a number the key leaves blank.

## The record

- DECODE R595, "TNA_SP106/7_Anne_(0020)", 1 image (IMG_R595_I3870_P1), Non-decrypted, nomenclator, numerical.
  Sender "Mr. Eichel", receiver unknown. The date "1 Jan 1758" is DECODE's 1758-01-01/1758-12-31 span.
  Record note: "An unsolved letter by Mr. Eichel, probably from Russia. The code maybe found in
  TNA_SP106/7_Anne_(0021-0022)" (= key R594).
- The sheet is a bifolium opened out. Dockets on the blank half read "Cypher from Mr Eichel 1758",
  "Prussia 1758" (pencil) and "Mr Eichel". "Prussia", not Russia: August Friedrich Eichel was Frederick II's
  cabinet secretary. A figure at the top right of the cipher half looks like "1754" or "1758".
- 18 lines, 139 groups (DECODE transcription by LW, 2020, checked against the image). Many groups end in 7.
- No decipherment is on the sheet, and none was found in the volume's other records.

## The key: R596, not R594

- R594 (SP 106/7 0021-0022, "Russia 1758") is a French nomenclator with about 1,100 values, mostly 1-1300. On the
  letter it gives nonsense and leaves 61% of the groups unassigned. It is not the key.
- The DECODE transcriptions of the 21 other SP 106 and Prussian key records were scored for coverage
  (`decode/score.py`). R596 (SP 106/7 0013-0017, French, 1,696 values 504-3293, undated on DECODE) carries a
  heading in French that sets out its nulls:
  > Tous les nro où je trouve un ou plusieurs 7 sont les nonvaleurs dans le présent chiffre, de même que les nro
  > depuis 1 jusqu'à 503 inclusivement et depuis 1115 jusqu'à 1198, tout comme aussi depuis 1483 jusqu'à 1999
  > [one line reads 1599], depuis 2600 jusqu'à 2802.
  The key contains no number with a 7 in it, and its values start at 504. This is the only key in the series
  whose rules match the letter's pattern: many groups ending in 7, and runs of 19xx and 26xx-28xx.

## The result

Under R596's rules, 117 of the 139 groups are declared nulls. That is 84%, where a random draw from 1-3299 would
give about 55%. The remaining 22 groups are:

    2512 1480 1413 2492 1434 3026 2093 3143 853 3150 3161 966 1291 1253 1311 1413 861 2853 2264 2264 863 911

Twenty-one of these 22 fall on cells that R596 leaves **blank** (transcribed `<EMPTY>`; e.g. 2511 montrer,
**2512 —**, 2513 mont; 852 armement, **853 —**, 854 arranger). Blank cells are 107 of the 1,527 live numbers,
7%, so twenty-one hits in twenty-two by chance has a probability of about 10^-23. The writer drew these numbers
from the unassigned cells on purpose. The one exception, 1480 = "écus", was transcribed "1 4? 8? 0".

The transcriber's "8?" is a looped glyph that is probably a 0 in this hand (2001, 2002). Read that way, the
survivors become 27 groups: 20 on blank cells, plus 1400 deu, 1100 Ci, 1405 difficile (twice), 1095 chose,
2053 françois, 1110 Clo. These make no sentence, so the conclusion stands under both readings.

**Conclusion.** The "letter" is a dummy, written entirely in non-values of the R596 cipher: nulls by rule, and
blank cells of the table. It hides no text. It was probably a specimen or test of the cipher, or a blind, rather
than a despatch. Why the Deciphering Branch held it with R596 is not known. Whether R596 is Eichel's own key, or
a key the Branch attached to Prussian material, is not settled by this sheet. Its French vocabulary includes
Moravie, Mecklenbourg, Hollande and Saxe.

## Open

- R596 is undated on DECODE. Its vocabulary could date it and tie it to Eichel's cabinet.
- The key images were not read cell by cell against the transcription's `<EMPTY>` cells. The coincidence
  argument does not depend on that, but a page-by-page check would confirm it.

## Files

- `decode/score.py`: parses the DECODE key transcriptions, scores their coverage, applies the R596 null rules.
- DECODE images, record pages and DOC transcriptions stay local (`decode/`, git-ignored).
