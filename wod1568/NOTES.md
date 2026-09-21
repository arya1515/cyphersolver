# Catalogue 97: the two unidentified ciphers on BL Add MS 4136 (DECODE R2988, R2989)

Status: in progress (not read; blocked on the originals, see "Route in")

Catalogue entry 97 ("Unknown sender (Paris) to unknown recipient, 10 Jul – 8 Aug 1559") covers the two items
Tomokiyo lists as unsolved on cryptiana `unsolved.htm` (Nicholas Throckmorton 1559 / John Wod 1568). The
Throckmorton cipher text on both leaves is already read by Tomokiyo (Cipher 1 and Cipher 3; see `../throckmorton/`).
Each leaf also carries a second cipher that is **not** Throckmorton's. Those two are the targets here:

| record | leaf | the unread cipher |
|---|---|---|
| R2988 | f. 32 (old 9), Throckmorton to the Queen, Paris, 10 July 1559 | ~12 lines of small cursive signs in the lower margin and beside the subscription, including a clear date `… 1559`, a boxed group repeated three times, `/` and `//` separators, and a starred insertion keyed to a `*` note in the left margin |
| R2989 | f. 33 (old 10), Throckmorton to Cecil, Paris, 8 Aug 1559 | one line at the foot, docketed in the left margin "Mr John Wod to Secretary Cecil, 6 Sept 1568", with a traced signature "M. Jhone Wod" |

Images: `img/` (DECODE, git-ignored). Downloaded with the bordeaux cookie 2026-09-21.

## R2989: John Wood to Cecil, 6 September 1568

Transcription (`wood_line.txt`, my labels; 3x zoom on `IMG_R2989_I20715_P.jpg`):

    g x ob r3 Z pm x x x2 f x2 Z g D x2 e XX 3 · x zl x ob x3 x2 x x2 Z zl o d pm g x ob /  (J) o · Z D x2 zl

`x` plain saltire; `x2` saltire with a hooked stroke; `x3` inverted-v form; `ob` o with a flat bar; `r3` a reversed
curly 3; `Z` long-tailed ʒ; `3` a short numeral 3 followed by a point; `zl` z with a vertical (L over z);
`pm` a plus-minus sign; `D` triangle; `XX` a blotted x with a dotted x written above it. 34 signs on the main line
and 5 after the marker `(J)`, which may be an insertion or a separate item.

**Same family as the Moray→Wood cipher.** The symbol families (x with variants, ʒ/z with variants, g, o, e, f)
match Tomokiyo's transcription of Moray to Wood, 13 July 1568 (`../moray/`, unread after one session). Wood
was Moray's agent in London that summer, so this is very likely the same Scottish cipher, and a second sample
of it. Tomokiyo's labels cannot be aligned glyph-for-glyph without his image (`stewart.jpg`, 404), so the two
texts could not be pooled.

**Crib from Bain.** Bain, *Calendar of Scottish Papers* ii no. 804 (Wood to Cecil, Edinburgh, 6 Sept 1568,
Cecil Papers, holograph) prints one passage with the footnote "These words are in cipher": *"and says he must
neidis haif it be on meinis or uthir."* (42 letters). Tested against the line (`align3.py`, `align4.py`):
exhaustive alignment with each sign = one letter, a null, or a fixed string of up to 4 letters (up to 6 nulls and
12 multi-letter signs), with and without the `(J)` group, with *says/sayis*, forwards and reversed, and every
substring of the phrase of 8+ letters: **no consistent alignment**. The line opens and closes with the same
trigram `g x ob`, which the phrase cannot produce. Either the Add MS 4136 line is a different ciphered passage
of the letter (the copyist may have taken the last one; Bain's final sentence, with its garbled "sennwngist"
footnoted "Sinews", is a candidate), or Bain's footnote marks words that the original shows deciphered in a
form the copy does not reproduce. 39 signs is far below what a ciphertext-only attack on a ~30-sign homophonic
alphabet needs.

## R2988: marginal cipher on Throckmorton's letter of 10 July 1559

About 300 cursive signs in 12 lines: strokes, hooks and loops with points and superscript points, word-like
clusters separated by spaces, `/` and `//`; a boxed group (read upright something like `ʃro` with superscript
points, once as `rel ʃro`) occurs three times; the clear year `1559` appears in line 10. Mirroring and inverting
the image do not give Latin script. The look is of a shorthand or an abbreviated sign alphabet rather than the
letter-symbol alphabets of Throckmorton's three ciphers, and the sign inventory could not be fixed reliably
from the scan (variation in size, points and ligatures). Not transcribed; not attacked.

## Route in

1. R2989: the original Wood letter of 6 Sept 1568 in the Cecil Papers at Hatfield (Bain's "C.P., vol. I"). It
   should show where the cipher sits and whether it was deciphered, giving a true crib for the line and a second
   text for the Moray cipher.
2. Tomokiyo's image or glyph table for Add MS 32091 f. 213, to merge the Moray and Wood texts under one labelling.
3. R2988: a clean high-resolution photograph of f. 32 and a comparison with 16th-c. English shorthand and
   personal sign systems. The clear "1559" and the `*` note suggest a contemporary annotation, possibly by the
   decipherer, rather than a second despatch.

## Files

`rec2988.htm`, `rec2989.htm` (DECODE record pages) · `wood_line.txt` · `align*.py` (crib alignment) ·
`bain2.txt` (Bain ii OCR, not committed) · `img/` (not committed).
