# Reading the Raince 1526 cipher (BnF fr. 2984) — calibration sheet

The cipher is a monoalphabetic substitution with homophones (Tomokiyo 2020, key image
`img/key3x.png` — look at it first). Plaintext is 1526 diplomatic French (no accents, u/v and
i/j interchangeable, spellings like "estoit", "faict", "icy", "moys", "seigneur", "monseigneur",
"l'empereur", "le pape", "Savoye", "Venise", "Rome", "Bourgoigne", "Bourbon" possible).

## Glyph table as it appears on this microfilm

| plaintext | cipher glyphs |
|---|---|
| a | small plain circle `o`; circle with small cross/plus attached below; `×` |
| b | circle crossed by a horizontal bar (θ-like) |
| c | small SQUARE/rectangle with a dot inside |
| d | circle with a straight tail going down (ϙ/ρ-like) |
| e | ψ (trident); `7`; a small circle at the base of a vertical stem with a bar on TOP (the single most frequent glyph); ◇ diamond |
| f | △ triangle |
| g | 6-like / b-with-flag |
| h | ε |
| i | ✕ (looks like two x's or a double cross); Roman `I` with serifs; a heavy filled dot; 9-like |
| l | round `s` shape |
| m | long `f`-like shape (on film it can look s-ish) |
| n | see note below |
| o | see note below |
| p | `T` (T with flat top bar) — VERIFIED in "depesches", "party", "pour" |
| q | the "ni"-shaped glyph (two minims joined, looks like the letters ni or nv) — VERIFIED in "quatriesme", "qui" |
| r | `4`-like glyph (φ/⌀, a loop crossed by a rising stroke); variants look like "-o" or `H` — VERIFIED in "party", "pour", "venir" |
| s | ∧ (caret / lambda without foot) — VERIFIED in "depuis", "les", "s'est" |
| t | ℓ (cursive ell with loop) — VERIFIED in "estoit", "party" |
| u/v | `V`; `R`-shaped glyph; `Ƶ`/2-without-loop — VERIFIED in "depuis", "vous", "venir" |
| y | `E`-shaped glyph; ω — VERIFIED in "moys", "Savoye", "icy", "party" (final y) |
| nulls (skip) | λ; a "ny"/"my"-looking ligature; `K` |

n and o: one of them is the `ꝛ`/2-with-loop ("z-with-flourish") glyph. In "pour" (p-o-u-r =
T-?-V-4) the glyph in o position is the 2/z-like one. The other of the pair is an `n`-like
shape. When you meet either, decide from French context (both are frequent).

Word signs (single glyph = whole word): `L`-with-crossed-tail = **con**; a curly double-loop
(e-with-loop-below, like ꝭ) = **l'empereur**; a `y`-like glyph = **le pape**.

## Method — follow exactly

You get, per manuscript line, TWO images: `<page>_<NN>L.png` (left half) and `<page>_<NN>R.png`
(right half). They OVERLAP by a few glyphs in the middle — do not transcribe the overlap twice.
The target line is the LOWER, complete line of writing in each crop (the crop includes the
bottom of the line above for context; ignore it). Some crops show faint verso show-through:
ignore anything faint/mirrored.

You also get the machine draft for that line (connected-component clustering decoded with the
key). It is about 80–85 % correct. Lowercase letters in it are usually right; CAPITAL letters
mark unreliable clusters; it also merges or splits some glyphs. Use it as scaffolding, not truth.

Per line:
1. Look at the L image, read the glyphs one by one against the table; then the R image.
2. Reconcile with the draft line: keep draft letters the image confirms, fix the rest.
3. Drop nulls (λ, ny, K). Expand word signs (con, l'empereur, le pape).
4. Segment into French words. The lines run on: a word broken at the line end continues on the
   next line — leave it broken, do not invent the rest.
5. Where a glyph or short run stays unreadable, write `?` per uncertain letter or `[...]` for an
   unreadable run. NEVER invent plausible French to fill a gap: a wrong confident reading is
   worse than a hole. It is normal for 1–3 spots per line to stay open.

Output format, one block per line, nothing else:

```
NN | <french reading with word spaces, ? and [...] where unsure>
NN-note | <only if needed: one short remark, e.g. "draft had X, image shows Y">
```

## Worked example (f29r line 20)

Draft: `squiestoiterIacoUrtdesavoyesestpartypourvenirScy`
Image reading: ∧(s) ni(q) V(u) ✕(i) 7(e) ∧(s) ℓ(t) o(a?→no, context "estoit") ...
Result: `20 | s qui estoit en la court de savoye s est party pour venir icy`
(The capital I after "estoiter" was a junk cluster = "n"+"la" merged; "S" before "cy" was i.)

This is the continuation of a sentence from line 19 ("...un personnage") — expect run-ons.
