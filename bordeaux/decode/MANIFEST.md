# DECODE downloads needed for Bordeaux → Brienne, 30 May 1653 (BL Add MS 4200 f. 88)

Public metadata read 2026-09-16 from `https://de-crypt.org/decrypt-web/RecordsView/<id>` (saved here as
`rec<id>.htm`). Every full image is "Access mode: Authentication required"; the file server is
`https://de-crypt.org/decrypt-custom/filesrv/?file=<name>`. Thumbnail names carry a `TH_` prefix (200 px wide,
already downloaded here, useless for glyphs); the full image is the same name **without** `TH_`.
Save everything into this folder under the DECODE file names. Either run `python fetch_decode.py` with a
`cookie.txt` (see its docstring) or save the images by hand from the browser.

The BL note on every record: "The image is not in the public domain. Publishing it is only possible with the
permission of the Library." So the images stay local (git-ignored); only derived transcriptions are committed.

## Priority 1 — R7537, BL Add MS 32263 f. 1: the Deciphering Branch's key, 1653, receiver "Mr. Bordeaux"

Catalogued: Key, numerical, simple substitution, notes "Syllables", plaintext language English, 1 page
(2 images), created 2023 by lehoanna. Thumbnail shows a dense multi-column table. If it is the English
reconstruction of the 1653 letter's cipher, it reads the letter outright.

| file | what |
|---|---|
| IMG_R7537_I34037_P1.jpg | key table, recto |
| IMG_R7537_I34037_P2.jpg | second image (verso or continuation) |

## Priority 1 — R8390, Add-MS-4200_5: the letter itself, 7 pages

| file | what |
|---|---|
| IMG_R8390_I38812_P1.jpeg … IMG_R8390_I38812_P7.jpeg | the seven pages of ciphertext (f. 88 ff.); last line ends in cleartext "on n'a point icy" |

## Priority 2 — R8392, Add-MS-4200_7: 3 pages, graphic signs + alphabet + numerical, no cleartext, no note

Not in the earlier NOTES; it could be a second letter in the same cipher (the hoped-for depth) or an
unrelated item. Check the symbol inventory against `../ciphertext.txt` as soon as it arrives.

| file | what |
|---|---|
| IMG_R8392_I?_P1-3.jpeg | run `fetch_decode.py 8392` or read the names from `rec8392.htm` |

## Priority 3 — duplicates and English worksheets (control on the transcription, possible partial English decrypt)

| record | files | what |
|---|---|---|
| R8391 Add-MS-4200_6 | IMG_R8391_I38820_P1-3.jpeg | duplicate of the last section of R8390; f. 92 = frequency counts of the whole ciphertext (Tomokiyo) |
| R8393 Add-MS-4200_8 | IMG_R8393_I38824_P.jpeg | duplicate of the beginning of R8390 |
| R8389 Add-MS-4200_4 | IMG_R8389_I38803_P1-3.jpeg | frequency count for R8390 |
| R8386 Add-MS-4200_1 | IMG_R8386_I38792_P1-4.jpeg | contact tables: symbols before/after "d" etc. (f. 74) |
| R8388 Add-MS-4200_3 | IMG_R8388_I38802_P1-5.jpeg | contact tables: before/after "u" (f. 78) |

R8387 (Add-MS-4200_2, Montague, English, decrypted) is unrelated and not needed.

## After download

1. `crop_lines.py` (to write): crop each R8390 page into lines at 2-3x, re-read every token's mark (prime,
   two dots, overbar, stroke) and glyph variant into `ct2.txt`; log divergences from Tomokiyo's string.
2. Read R7537 into `key7537.txt` (number → syllable/word), then apply to `ct2.txt`. If it reads, the item is
   solved by the historical key; if only partly, use the reading as a crib for `../solver.py`.
