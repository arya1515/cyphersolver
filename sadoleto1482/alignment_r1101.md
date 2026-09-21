# R1101 / 7a: source map and control passage

20 September 2026. Status: in progress. The contemporary clear witness is
established; a complete word-level collation has not been made.

Additional local collation is in `r1101_queen_parallel.md`: five cipher rows
on original page 2, aligned to the lower first page of 7a, with unresolved
words retained and the original/witness a/cum difference recorded.

## Page identities

The original letter, Vestigia 1284, occupies **four written page surfaces**
in three photographs:

| Original surface | Photograph | Visible character |
|---|---|---|
| First page | `(103).JPG`, `v1284_1_...` | Predominantly cipher, with some ordinary words and a clear closing transition |
| Second page | Left of `(104).JPG`, `v1284_2_...` | Clear opening, then extensive mixed cipher/clear text |
| Third page | Right of `(104).JPG` | Cipher at top; two clear paragraphs; a further cipher paragraph at bottom |
| Final page | `(105).JPG`, `v1284_3_...` | Cipher and mixed passages above; ordinary closing paragraph, date and signature below |

The clear copy 7a, Vestigia 1283, has **three written page surfaces** in two
photographs: `(101).JPG` is the first page, while `(102).JPG` contains pages
labelled 2 and 3. All three were visually inspected. It is a continuous copy
of the letter, unlike R1106's short separate decipherment slips.

DECODE image `IMG_R1101_I5655_P2.png` shows the **final original page** and
matches Vestigia `(105).JPG`. Thus the earlier phrase `R1101 p. 2 ll. 1–3`
identifies the second cached DECODE image, not manuscript page 2. Use the
image ID or the final-page description when citing the key-building control.

## Direct control

The original final-page opening corresponds to the upper part of **clear
copy page 3**, not clear-copy page 2. The following readable passage is from
the clear witness, with abbreviation expansion and punctuation editorial:

> ... volesse unirse et pigliare questa impresa, et non lassasse pretermittere
> questa opportunita laquale mai piu fo, ne forse sera, et che lo facesse per
> lo amore et benivolentia, et per la affinita strectissima che l'ha cum tuta
> la liga, et per honore et gloria de sua Maesta, et abassare una volta
> Venetiani per modo che l'imparasse de stare fra li suoi fine.

This is **a transcription of the clear witness**, not a claim that every
word has independently been read from the cipher. The original visibly
retains `unirse` in ordinary writing at its first line, then enciphers the
following appeal. Several direct alphabetic matches support the existing key:
`pigliare questa impresa`, `non`, `ne forse sera`, `amore`, `benivolentia`,
`tuta la liga`, and `de stare fra li suoi fine`. The transition back to clear
writing, `Bene e vero che poi neli parlamenti...`, matches the next sentence
of 7a. These boundaries make the identification independent of a single word.

Source rectangles, in original 4320 × 3240 coordinates:

- Original `(105)`: `(1080,195,3290,710)`, displayed in
  `img/r1101_final_open_full.png` (90% scale).
- Clear `(102)`, right-hand page: `(2380,430,4070,920)`, displayed in
  `img/r1101_clear_control.png`.

The earlier crop `img/r1101_final_open.png` clips the beginnings of lines;
use the `..._full.png` crop for the control.

## Coverage conclusion

The first clear page begins with the letter's opening about the recipient's
letters and the Hungarian king. The last clear page includes the appeal above,
the ensuing negotiations and the closing discussion of letters/news from the
king and queen, followed by date and signature. The original final page has
the same sequence through its closing. These observations support the
identification of 7a as a whole-letter witness.

However, the presence of a beginning and ending cannot rule out internal
omissions. The original's long interior cipher passages still require detailed
collation. Accordingly, the profile now records the completeness of the
plaintext witness as **unknown**, replacing the earlier unverified `false`
value for `plaintext.partial`. This does not retract the firmly established
fact that a contemporary decipherment exists, or the local key control.
