# Brief: shape-true re-transcription of the Mâcon ciphers (BnF fr. 3053, 1536-37), pass 5

Goal: raise every record from the readers' ~75-86 % to ~93-95 % of letters by transcribing each sign by its
**shape** (not the old collapsed aliases), then decoding with the key map and the French LM.

## Read first
- `work_shape/pilot.md` and `work_shape/catalogue.md` + `catalogue.png` (the sign IDs: `Of` long hooked f = O,
  `Up` £ looped foot = U/V, `Pn` two-bar stroke = P, `F` looped p-top = F, `Mq` crossbar q = M, the Q sign before £,
  hooked 5 = G vs 5 = D, bow-tie `Uv`, ...). The pilot cut CER from 9.2 % to 5.8 % on ground-truth lines.
- `work_shape/trans.txt` (the transcription format) and `work_shape/shapedec.py` (direct map + 5-gram beam; needs env
  `LANGWT` = a checkout of origin/main containing `lang/`; make your own with
  `git -C C:\Users\dbour\cypher worktree add <your scratch>\langwt origin/main` — never switch the shared checkout's branch).
- `C:\Users\dbour\cypher\gramont1529\macon_key.md`, key images `gramont1529\img\francisMacon*.png`, `BnF_fr3071_f9.png`.
- The previous readings (context, and what to beat): `git -C C:\Users\dbour\cypher show origin/main:rome1536/<file>`
  (R4233.md, R4234.md, R4234_P8-P12.md, R4234_P15-P20.md, R4235.md, R4235_P2-P3.md, R4235_P8D.md, R4238.md,
  R4239.md, R4239b.md, R4239_pass3.md, R4240.md, R4247.md, R4247_letter2.md) and `work_cluster/R<rec>_pass4.md`.
- Crib/corrections from a companion letter to the King: `work_clearcopy/dupuy44_parallels.md` (summary table at end).

## Images
- DECODE crops: `rome1536\img\IMG_R<rec>_I<id>_P<n>.jpg` (P-numbered horizontal crops; `.jpeg` = low-res full page).
- **Better: Gallica native scans of fr. 3053**, ark `btv1b90601432`:
  `https://gallica.bnf.fr/iiif/ark:/12148/btv1b90601432/f{VIEW}/full/full/0/native.jpg` (fetch ≤1 req/s; low-res
  preview `.../f{VIEW}/full/600,/0/native.jpg`). Low-res previews some views already in `work_clearcopy\fr3053\lo_<VIEW>.jpg`.
  Find the view for each folio by the folio number in the recto corner (roughly view ≈ 2×folio + small offset;
  verify). Save natives under `rome1536\work_shape\gallica\f<folio><r|v>.jpg` and append the view map to
  `work_shape\gallica_views.md` (check it first — another agent may have filled part).
- Fix line geometry first: deskew / follow each line's baseline (pages are warped); do not use fixed rectangles.

## Method per line
1. Crop the line (2x zoom, autocontrast), transcribe sign by sign with catalogue IDs, alternatives as `{Of|Up}`.
   Transcribe BEFORE looking at the old reading of that line.
2. Decode: direct map, then LM beam (`shapedec.py`). Word-divide. Compare with the old reading; where they differ,
   look at the image again and decide. Use glosses/clear copies where they exist.
3. Mark residue `[?]` honestly. Codes: 20 = l'Empereur, 30 = pape, 40 = roy.

## Output (write AS YOU GO, append after every few lines)
`rome1536\work_shape\R<rec>_pass5.md`: header (folio, Gallica view, date), then per line: signs / direct / LM /
final word-divided reading / changes vs old; then a running reading of the whole letter (clear text in *italics*
summarised is fine), and a **measured** coverage: letters read with confidence ÷ cipher letters, and CER on any
ground-truth lines. New sign IDs → append to `work_shape\catalogue_additions.md`.
No repo-tracked edits, no commits. At most one image sub-agent of your own, if any.

Final message: per record, lines, coverage before → after (how measured), main new readings, what stays open and why
(and whether it is physically unreadable on the Gallica native scan — that is the "impossible" record).
