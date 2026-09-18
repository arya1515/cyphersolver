# Reading the Raince 1526 cipher (BnF fr. 2984) — calibration sheet

The cipher is a monoalphabetic substitution with homophones (Tomokiyo 2020, key image
`img/key3x.png`). Plaintext is 1526 diplomatic French (no accents, u/v and i/j interchangeable,
spellings like "estoit", "faict", "icy", "moys", "seigneur", "monseigneur", "l'empereur",
"Savoye", "Venise", "Rome", "Bourgoigne", "Bourbon").

## The key, read off the image by measurement (not by eye)

Tomokiyo's table is a header row of plaintext letters over up to four rows of cipher glyphs.
The columns are narrow and easy to misread by one place. `img/key_labelled.png` is a contact
sheet of every glyph cropped out of the key and labelled; it was built by locating the white
header letters and the ink blobs in `key3x.png` and assigning each blob to the nearest header
column (every assignment came out within 15 px of a column centre, columns being ~78 px apart),
so the table below is measured, not guessed.

| plaintext | cipher glyphs |
|---|---|
| a | `o` small plain circle; `ꝗ` circle on top of a crossed stem; `×` |
| b | `θ` circle with a bar drawn across the inside |
| c | small square/rectangle with a dot inside |
| d | small circle on top of a plain vertical stem running down |
| e | `ψ` trident; `7`; `ƀ` small circle at the foot of a stem barred near the top; `◇` diamond |
| f | `△` triangle |
| g | circle with a long horizontal bar driven through it, bar projecting to the right |
| h | `ε` |
| i | `✕✕` double cross (like two x's sharing a stroke); serifed `I`; a heavy filled blob |
| l | `9` with a curved lead-in at the foot; the same 9 preceded by a big `C` stroke |
| m | small round `s` / `5` shape |
| n | long `f` with a crossbar |
| o | `ꝛ` circle with a long diagonal stroke rising through it to the right; `z` |
| p | `T` with a flat top bar; a small circle with a dash to its right |
| q | `n` (two minims joined) |
| r | `4`-shape: a loop or triangle crossed by a rising stroke, with a descender; a dash then a circle |
| s | `∧` caret; `H` |
| t | `ℓ` cursive ell with a loop |
| u / v | `v` / `✓`; `R`; `Ƶ` (2 with a bar) |
| x | *no glyph in the key* |
| y | `E` |
| z | `ω` |
| nulls (skip) | `λ`, usually drawn as a single thick sweeping arc; a `ny`/`my` ligature; `K` |

Word signs (one glyph = one whole word): a looped `L`/`&` with a tail = **con**; two small circles
side by side joined by a U-curve underneath = **l'empereur**; a cursive `y` with a descending
tail = **le pape**. Note that the *letter* y is `E`, so a y-looking glyph is *le pape*.

### Corrections to the earlier calibration sheet

The first version of this file had **l, m and n shifted by one column**: it read the round `s` as
l, the long `f` as m, and left n open. The measured table above is l = `9`, m = round `s`,
n = long `f`. That single error is what produced the old machine draft's "dongUeaent" for
*longuement*, "egsembde" for *ensemble* and "SonseigEur" for *monseigneur*; `handmap.json` and
every file derived from it (`hand_decode2.txt`, `draft3.txt`, `greedy70map.json`) carry the same
shift and should not be trusted as letter readings. The old sheet also put `H` under r; it is
measured under s. The old sheet's claim that the most frequent glyph (`ƀ`) is an e is correct.

## Confusable pairs to watch on this film

* `ψ` (e) / `4` (r) / long `f` (n) — all are a stem with something on top. `ψ` has a forked or
  rounded top with the stem running through; `4` closes a loop or triangle and drops a longer
  descender; `f` has a crossbar and a head curving to the right.
* `ƀ` (e) / g — `ƀ` is a *vertical* stem, bar near the top, circle at the foot; g is a
  *horizontal* bar through a circle, projecting right, sitting at mid height.
* `o` (a) / `ϙ` (d) / `9` (l) — a is a bare circle; d adds a straight stem below; l is a closed
  9 whose tail curves.
* `∧` (s) / `v` (u) / `×` (a) / `✕✕` (i) — the caret peaks, the vee opens.
* `θ` (b) / g — b's bar stays inside the circle, g's bar runs out past it.

## Method

`bands3.py` writes one PNG per manuscript line to `img/lines/<page>_<NN>.png`: the line cut into
four overlapping quarters, stacked, at 2x. The quarters are labelled a–d down the left edge and
**overlap by about three glyphs**, so do not transcribe the overlap twice. The target line is the
lower, complete line of writing in each strip; the crop includes the feet of the line above.
`zoom.py PAGE LINE FRAC0 FRAC1 [Z]` cuts any fraction of a line's x-extent at higher
magnification for a spot that will not resolve. `lineinfo.py PAGE [LINE]` prints the token count
and cluster ids of a line, which is a check on how many glyphs a line should have.

Per line: read the glyphs against the table; drop the nulls; expand the word signs; segment into
French words. The lines run on — a word broken at the line end continues on the next line, so
leave it broken and do not invent the rest. Where a glyph stays unreadable write `?` per
uncertain letter, or `[...]` for an unreadable run. **Never invent plausible French to fill a
gap**: a wrong confident reading is worse than a hole.

Output format, one block per line:

```
NN | <reading, with ? and [...] where unsure>
NN-note | <only if needed: one short remark>
```

## Worked control (f29r line 20)

Glyphs: `∧ λ n v ✕✕ 7 ∧ ℓ ꝛ I ℓ 7 f 9 o ⊡ ꝛ v 4 ℓ ϙ 7 ∧ o R ꝛ E ψ ny 7 ∧ ℓ T o 4 ℓ E T ꝛ v 4 R 7 f ✕✕ 4 I ⊡ E`
→ `s [λ] qui estoit en la court de savoye [ny] est party pour venir icy`

Every glyph in that line resolves, which is the evidence that the measured table is right: the
line contains a, c, d, e (three of the four homophones), i (two), l, n, o, p, q, r, s, t, u/v and
y, plus two of the three nulls.
