# Transcription convention (kurtz1639)

One output file per image: tr/<image-stem>.txt (e.g. tr/IMG_R3811_I23099_P.txt). Many images are two-page spreads:
mark each page with a line `## left` / `## right`. Write one manuscript line per text line, in order.

Within a line, tokens are separated by single spaces:
- cipher numbers exactly as written: `73 28 9 14 36`. Numbers are usually 1-2 digits; if unsure of a digit write `3?`.
  Where digits run together, split them the way the writer spaced them; if the grouping is unclear, write `?(7328)`.
- cipher letters as lowercase Latin letters: `w`, `a`, `z` ... ; Greek letters as `α β γ δ π` etc.;
  if a Latin letter carries a mark (dot, bar, hook), write it plus a note like `o.` (dotted), `c.` ; a crossed sign `x+`.
- any other graphic sign: `#name` with a short consistent name you define in a legend at the top of the file
  (e.g. `#z-tail` for a z/3 with a long tail stroke, `#ii`, `#pi`). Keep names consistent across files; reuse names from
  tr/LEGEND.md if it exists and add new ones there.
- clear (non-cipher) German/Latin text: put it in braces as your best reading, e.g. `{ist der feindt über}`;
  if unreadable write `{...}`. Do not spend long on clear text; the cipher is the priority.
- small interlinear decipherment letters written ABOVE a cipher token: attach with `=`: `28=r 26=t`. If a gloss sits above
  a group of tokens, attach it to the first and mark `+`: `9=wi+ 15`. Only record glosses you can actually see; `=?` if a
  gloss is present but illegible.
Do not guess plaintext. Accuracy of the numbers matters most.
