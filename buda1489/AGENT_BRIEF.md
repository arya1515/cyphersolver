# Transcription brief: Milanese embassy at Buda ciphers (1489-92)

You are transcribing a 15th-century Italian diplomatic cipher (Maffeo da Treviglio's key, Buda 1489-92).
The cipher text is a run of separate signs written in one line with no word breaks. Each sign is a
cursive letter, an Arabic numeral, or a small mark, sometimes with a diacritic (a small superscript
letter, a bar, a dot, a stroke through the ascender). Homophones and syllable signs exist, so the
SAME base letter with a DIFFERENT diacritic is a DIFFERENT sign. Record exactly what you see, not what
you think it means.

## Input
Numbered strips in `seg/strips/`, named `<page>_L<line>_<part>.png`. Every glyph found by the segmenter
has a box and an index printed above it (blue = even, red = odd). Boxes are imperfect: a box may
contain two signs, a sign may be split into two boxes, and a superscript may have its own box.
Read left to right. Report ONE row per real sign, using the index of the box it sits in (if two signs
share a box, use `12a`, `12b`; if one sign spans two boxes, use the first index and skip the second).

## Token alphabet (use exactly these spellings)
Base shapes:
- lowercase letters as they look: `a b c d e f g h i k l m n o p q r s t u v w x y z`
  - the "e" of this hand is a Greek-epsilon shape (ε): write `e`
  - `u` and `v`: write `v` for the pointed form, `u` for the round form
  - `i` has a dot above it; a plain short vertical stroke without a dot is `l` if tall, `/` if slanted
- capitals: `L M E S`
- numerals: `2 3 4 6 8 9 0` (the `3` is a rounded z-like shape; the `6` has a closed loop; `8`, `9`, `4` as printed)
- marks: `//` two short parallel slashes (very common, one sign); `/` single slash; `)` right crescent
  (a bracket-like curve, sometimes with a dot inside: write `).`); `(` left crescent; `-` short horizontal
  dash; `=` double dash; `:` colon; `.` lone dot; `÷` dash with dots above and below; `+` cross
Modifiers (append to the base, in this order, no spaces):
- superscript small letter above/right of the sign: `^a ^e ^o ^u ^t ^s ^i ^r` (e.g. `q^e`, `m^a`, `b^t`, `m^o`)
- bar / macron over the sign: `~` (e.g. `m~`)
- stroke through the ascender or body: `|` (e.g. `b|`, `p|`, `l|`)
- dot immediately after the sign at mid height: `.` (e.g. `d.`)
- horizontal stroke attached to the right: `-` (e.g. `x-`, `b-`)
If two modifiers apply, write both (e.g. `b|.`). Unsure about the base? Give your best guess and add `?`
(e.g. `6?`). Clear-text words (Latin/Italian in normal script, e.g. "La Ex.tia vra", "Lo") are NOT
signs: write them as one row with token `[clear: ...]`.

## Output
Write a CSV `trans/<page>.csv` with header `line,idx,token` and one row per sign, lines in order.
At the end, list any indices you could not read at all and any box that clearly contains ink the
segmenter missed (e.g. "line 3: an unboxed sign between 17 and 18: `//`").
Do not attempt to decipher. Do not skip signs. Look at every strip at full size (Read the PNG).
