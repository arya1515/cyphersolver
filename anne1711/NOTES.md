# Queen Anne → Peterborough, instructions of 22 Feb 1711/12 (BL Add MS 4107 ff. 184–185; DECODE R4878)

Status: closed, already in print (clear text in Parke 1798), identified and matched here 21 Sept 2026. Catalogue item 86.

## The document

- BL Add MS 4107 ff. 184r, 184v, 185r (DECODE R4878, three images, BL copyright, login only). DECODE: Queen Anne →
  Charles Mordaunt, 22 Feb 1711, "Non-decrypted", cipher type unknown, numerical; note "Instruction ... For his
  embassy to Turin".
- Signed original: *Instructions for Our Right Trusty and Right Welbeloved Cousin and Councillor Charles Earl of
  Peterborow and Monmouth. Given at Our Court at St James's the Two and Twentieth day of February 1711/2 in the
  Tenth Year of Our Reign*, sign manual *Anne R* at head and foot. The date is Old Style: **22 Feb 1712** new style
  (DECODE's end year 1712 is the same letter).
- Clear English with 61 runs of numerical code, 414 groups (242 distinct, 76–2269), dot-separated. The scribe writes
  8 as a looped ơ. Two groups lost in the gutter of f. 184v (`52?`, `33?`). Transcription: `transcription.txt`.

## Found in print

Gilbert Parke (ed.), *Letters and Correspondence, Public and Private, of ... Henry St. John, Lord Visc. Bolingbroke*
(London 1798), vol. 1 pp. 310–311, in a note to St John's letter to the Queen: "Lord Peterborough's instructions was
as follow", the whole text in clear, from the office draft (archive.org `letterscorrespon01boliiala`, djvu text
lines 11994–12050; excerpt in `print/parke1798_v1_p310-311.txt`). Found by grepping the archive.org text of Parke
for "Peterborow" after the DECODE key search failed.

**What the cipher hides.** Not the Turin embassy. The Electoral Prince of Saxony (Frederick Augustus, the future
Augustus III) was on his way to Rome to abjure Protestantism before marrying an archduchess. Peterborough is to
join him, if possible before he reaches Rome, as if by accident; give him the Queen's letter; urge him to stay
Protestant; if he wavers, tell him he will be welcome in England; if he fears he must abjure to escape danger and
wants to flee, concert "the proper measures for rescuing him out of the hands he is in, and bringing him safe to our
dominions, or those of any other Protestant Prince or State". If already at Turin, he is to tell the Duke of Savoy
that the Queen has given him leave, at his request, to see Rome, so as to "prevent any suspicion of the true intent
of your going thither". He is not to correspond with either Secretary of State, and may come back to Turin when he
judges his attendance on the Prince of no further use. Every enciphered stretch is the Saxon business or the cover
story; the clear parts are generic.

## The match (alignment.tsv, align.py)

All 61 runs fall at the right places in the print, in order, and the recurring groups hold their meaning:
894 = *him* (runs 20, 22, 23, 31, 40, 43 *him*·1098 *self*, 50), 466 = *he* (34, 35 end, 42, 51), 609 = *his*
(18, 24, 29, 44, 47), 981 = *your* (19, 28, 30, 56, 59), 1373 = *religion* (13, 27, 44), 1219.563 = *Protestant*
(9, 53; 563 also in 27), 1369 = *Rome* (7, 18, 55), 1076 = *Prince* (10, 17, 61) and 2211 = *Prince* (4, 53),
1095 = *State* (53, 58), 820 = *this* (40, 57), 783 = *on* (22, 31, 61), 422 = *ab-* (12 *abandon*, 44 *abjuring*),
1068 = *our* (23, 36, 53), 534 = *to* at all eight places (2, 14, 17, 23, 31, 55, 58, 60), 678 = *the* (9, 17, 22,
30, 55, 61), 839 = *you* (17, 31, 55, 57), 2101 = *Turin* (60), 2089 = *Saxony* (5). Two runs have no counterpart word in the print: 8 (`91`, between *Rome and* and *the
infinite*) and 39 (`261`, *affairs 261 bring*); nulls or small differences between the draft and the fair copy.

The code is heavy with nulls: 414 groups for 232 printed words (1.8 per word). *his* is written 328.333.388.467 in
run 37 and *him* 326.332.349.467.2269 in runs 48–49, so a word's real group is padded with dummies, and several words
have more than one group (*Prince* 1076/2211, *Rome* 1369/519.488, *him* 894/326...). Groups are not in
alphabetical order (466 *he* < 609 *his* < 894 *him* < 981 *your*), so it is a two-part or shuffled table, not the
printed one-part forms of SP 106/7.

## Key search (negative)

155 transcribed British key records on DECODE (all of TNA SP 106 boxes 6–8 and every BL/TNA/Bodleian key dated
1690–1730 that has a DOC transcription) were tested for 894 = him, 466 = he, 1098 = self, 981 = your: none fits.
BL Add MS 61575 ff. 62–65 (R8763/R8764) is Marlborough's small name list, not this code. The code table was not
rebuilt beyond the anchors above; the print makes it unnecessary.

## Contamination

The reading existed in print since 1798 (Parke). The model found it on the second search route (after the DECODE
key sweep), before any cryptanalysis beyond anchor guesses (894 = him, 466 = he, 894.1098 = himself, 981 = your) made
from the clear context.

## DECODE corrections to send

R4878: status Decrypted (clear text printed, Parke 1798 i 310–311); date 22 Feb 1711/12 O.S. = 1712; subject is the
mission to the Electoral Prince of Saxony, not the Turin embassy; cipher type nomenclator (code with nulls).
