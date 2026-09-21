# R1103: image evidence and limits of the reading

**Current update:** `vostro` is now accepted as an isolated C word after
direct comparison with R1101's controlled `nostro` and the established v
form. No continuous sentence is established. Earlier non-promotion reports
below describe previous checks and are superseded only for this one word.

20 September 2026. Status: in progress. No continuous decipherment has been
established from the four-line block. This report records a source comparison,
not a claim that the cipher is intrinsically unsolvable.

## Which images contain the block?

Vestigia 1294 has five cached image files, all 4320 × 3240:

| File prefix | Photograph/content |
|---|---|
| `v1294_1_` | `(115).JPG`, first written page |
| `v1294_2_` | `(116).JPG`, spread containing manuscript pages 2 and 3 |
| `v1294_3_` | `(117).JPG`, final written page |
| `v1294_4_` | `1387570335.jpg`, duplicate view of first page |
| `v1294_5_` | `1387570335-2.jpg`, duplicate view of the middle spread |

The cipher is on the **left page of the middle spread**, in the gap between
ordinary-text paragraphs. Contact sheet: `img/r1103_sources.jpg`.

The spread pair was compared at identical coordinates. At 540 × 405 pixels,
using Pillow's default RGB resize, the mean absolute channel difference is
**0.4407 on the 0–255 scale**, with flattened RGB correlation **0.99980537**.
Their page geometry, stains and shadows match visually. This supports treating
them as versions of the same exposure, not independent photographs that might
restore different faded strokes. The metric alone is not proof of identical
provenance; the visual comparison is part of the conclusion.

## Reproducible viewing region

The source rectangle `(200,1170,2180,1930)` includes ordinary writing above
and below all four cipher lines. Views made during this audit:

- `img/r1103_block_raw.png`: colour crop from `(116).JPG`.
- `img/r1103_block_alternate.png`: same crop from the duplicate spread.
- `img/r1103_block_blue.png`: blue-channel local-background contrast view of
  the first crop, using a Gaussian background radius of 22 and a darkness
  multiplier of 6, clipped to 0–255. No strokes were generated or filled in.

The cipher occupies approximately y=1550–1820 in the original. Use the wider
context crop when separating cipher strokes from the neighbouring prose.
Some marks remain visible in colour and contrast, but weak/missing strokes
make segmentation and letter identification unstable. Increasing contrast
also amplifies paper texture and cannot be counted as new textual evidence.

## Reading decision

The earlier notes proposed isolated fragments such as `se tener che`,
`vostro`, and `meco`. Those fragments are **tentative**, not a decoded sentence.
The present comparison did not establish a new continuous phrase and did not
justify filling the gaps from the surrounding political discussion. In
particular, the clearly written `Io credo...` **below** the cipher block is
ordinary prose and cannot be counted as cipher successfully deciphered.

No independent clear witness for the block has been located. An actually
different photograph, a better source scan, or a contemporary decipherment
could change this result; the cached duplicate spread does not supply such
evidence. Further work on the other Sadoleto letters remains useful, but
repeatedly enhancing this same exposure should not be reported as successive
decipherment progress without newly verifiable signs.

## Follow-up fragment check

A later 20 September inspection compared the existing raw colour and
blue-channel views directly, then enlarged the left portion of the final
cipher line. `img/r1103_lastline_left.png` derives from the raw context crop
rectangle `(0,530,1050,680)`, doubled in size; in the original photograph
this is `(200,1700,1250,1850)`.

The repeated n/o/n-shaped group is visible, but the adjoining signs did not
support a securely transcribed clause. A possible word concerning reasons
was considered and rejected as an accepted reading because its internal
letters could not be resolved independently. The older `vostro` and `meco`
proposals were likewise not promoted. No new accepted plaintext resulted
from this check. This is a negative verification result, not a new source or
an advance in deciphered coverage.

## Recheck after the ff control

The new ff mapping from R1101 was tested against the existing four-line
view. Two additional colour crops preserve the inspected left portions:
`img/r1103_line1_left_control.png`, original `(240,1535,1250,1680)`, and
`img/r1103_lines34_left_control.png`, original `(240,1650,1320,1835)`.
Neither establishes a secure new ff occurrence or continuous phrase. The
previous fragment proposals remain tentative. This is a negative control,
not new recovered coverage; subsequent work returned to R1106's clearer
known-plaintext passages instead of repeatedly amplifying the same pixels.

## Direct nostro/vostro control

The six-sign R1103 word in the third cipher line is now read **vostro, C**,
using the reconstructed alphabet. Original photograph `(116)` rectangle
`(385,1660,770,1785)` is enlarged threefold in `img/r1103_vostro_test.png`.
The first sign has the established v form; the remaining signs are comma/o,
angular 7/s, upright-with-right-loop t, long r, and final 3-like o.

Control: R1101 I5654 rectangle `(550,790,890,890)`, enlarged threefold in
`img/r1101_nostro_test.png`, contains `nostro` in the passage `del facto
nostro`, independently aligned with clear witness 7a. See
`r1101_queen_parallel.md` and `img/r1101_regina_clear.png`. Its o/s/t/r/o
sequence directly matches the R1103 word, while its initial round n differs
from R1103's looped v. The established v value, rather than the surrounding
political context, supplies the initial letter.

This is an alphabet-based reading of one word, not discovery of a clear
witness for R1103. No adjoining word is accepted, and no pronoun referent,
sentence, or decoded percentage is inferred. Other earlier fragments remain
tentative. The colour image supplies the evidence; no generated or filled
strokes were used.

## Following word and alternate-scan search

The word after `vostro` was tested against R1102's `mandato`. The crop
`img/r1103_after_vostro_test.png`, original rectangle `(680,1645,1090,1780)`,
does not securely show the expected a and d forms. `Mandato` is therefore
not accepted and the adjoining text remains unread.

Vestigia 1294 supplies the archival reference `DF 294375-1`. On 20 September
2026 a browser search for `294375` in the official MNL Collectio Diplomatica
Hungarica catalogue (https://adatbazisokonline.mnl.gov.hu/adatbazis/dldf)
returned `Nincs találat` (no results). No alternate scan was recovered.
This is a search result, not proof that MNL holds no corresponding image.
