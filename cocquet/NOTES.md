# Cocquet → Mangot, Rome, 13? November 1616 (BnF Clairambault 369, ff. 316-317)

Session 2026-09-16. Gate check only: fetched, measured, not attacked.

## Source

- Tomokiyo, *Ciphers during the Reign of Louis XIII* (cryptiana `louisxiii.htm`): "BnF Clair 369 (Gallica) contains a
  partially enciphered letter dated Rome, 13? November 1616 from Cocquet to Mangot (f.316). It is not deciphered." His
  image `BnFClair369f317.png` (632 × 456) is in `../gallica_siblings/src/`.
- Gallica: Clairambault 369 = `ark:/12148/btv1b9000782k`, 359 canvases, all labelled NP. Canvas 322 shows f. 310, so
  **f. 316 is canvas 328 and f. 317 canvas 329** (right pages; f. 316v on the left of canvas 329). Full-resolution IIIF
  images (about 6100 × 5000) saved as `img/c328_f316.jpg`, `img/c329_f317.jpg` (git-ignored); cipher block
  `img/block.jpg`; strips `lines/R01.png` … `R12.png`.
- f. 316 is entirely in clear (Turin and Savoy news: Béthune, the Grand Duke, the Duchess of Mantua, "la Royne" — Marie de
  Médicis). The cipher sits on f. 317, in the lower half, interleaved with clear French:
  "… que la Roy[ne] estoit mort a Millan … [86 …] … Cet homme est dangereux et mal[icieux?] … que le meschant discours
  … qui le poussent a faire ce qu'il fait … Vous me pardonnerez Monseigneur, si j'ose vous dire que le mo[y]en …
  y aura moyen qu'il sache ces affaires, ce sera le meilleur … soit faire la guerre … et encores a … ne tend a autre
  but que de pouvoir …" and a last cipher line with a flourish. Cribs are plentiful; the cipher runs are short.

## Measurement (the gate)

| | |
|---|---|
| Cipher runs | 9 (two full lines, the rest half-lines between clear phrases) |
| Tokens | about 150-170 glyphs (segmentation into units uncertain: letters run together in the hand) |
| Alphabet | letter shapes and ligatures (ſ, s, g, y, l, d, q, z, w-like ω, π, ct, ſt, a crossed t, a 8-with-tail ϑ, ⌗, $) with a few figures (86 ×3, ·89, 2, 4, 5, 6, 8) |
| Recurring units | "pu" (≥ 8), "ot" (≥ 6), ϑ (≥ 10), 86 (3), "ſq", "dq", "ϑd" |
| Marks | underlined pairs "y z" (twice) and an underlined "c"; ö with two dots (twice) |
| Distinct units (provisional) | about 40-50 |

## Key-application test

Tomokiyo reconstructs three ciphers from the same volume — de Baugy (f. 109: figures with umlaut, letters and syllables),
de Castille (ff. 11, 13: letter and ligature homophones, Caesar-like, nulls) and Du Maurier (ff. 229, 294: two-figure
syllabary) — and two anonymous keys from Clair 372 f. 169 and Clair 373 f. 303 (images in `../gallica_siblings/src/`).
None matches on sight: Baugy and Du Maurier are figure ciphers, Cocquet's is mostly letters; Castille's repertoire
(4, θ, //, ⊕, ∂, ſ, ſſ, q, ⊤, Ϫ …) shares only the generic ſ/q/g shapes, and its word codes (numbers 14-99) are not what
the plain numbers here look like. The anonymous Clair 372/373 keys use different letter forms and numeric word codes.
Not run as decodes — the repertoires do not overlap enough to map more than a handful of glyphs.

## Verdict

Not attacked. About 160 tokens over 40-50 units is the du Croc regime (`ducroc/`: 147 tokens, 40 symbols), where the
matched homophonic control was recovered at 28-41 % — below threshold without segmentation or a key. The cribs in clear
are the one lever (the runs sit inside French sentences whose gaps are constrained), but each run is 5-20 glyphs and a
crib-fixed anneal at this length cannot be validated against a control. **Below threshold; closed at the gate.**

What would reopen it: another Cocquet letter in the same cipher (Clair 368-373 hold the 1616-17 Mangot correspondence;
a contact sheet of canvases 280-359 of Clair 369 at 400 px was made but is too coarse to spot cipher — not checked), or
the ambassador's key (the French embassy in Rome in 1616 was the marquis de Trainel's; Cocquet is presumably an agent or
secretary — not identified here).

## Files

- `img/`, `lines/` — git-ignored; regenerate from the IIIF URLs above.
- Contact sheet: `../gallica_siblings/src/clair369_sheet/sheet.jpg` (git-ignored).

Checked: canvas identification, clear-text frame, run and token counts, repertoire comparison with five period keys.
Not checked: unit segmentation, a labelled transcription (not made), sibling letters in Clair 368-373, Cocquet's identity.
User must verify: the counts before quoting them.
