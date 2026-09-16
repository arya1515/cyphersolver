# Getting the folios (a browser step; scripts are blocked)

Both holders of the images sit behind an interactive check that a script cannot pass from this network
(see NOTES.md §3). Either route below takes a few minutes in a browser.

## Route A: BNE Digital (full manuscript, public domain)

1. Open https://bnedigital.bne.es/bd/card?oid=0000174344&site=bdh (the old links
   `bdh.bne.es/bnesearch/detalle/bdh0000174344` and `bdh-rd.bne.es/viewer.vm?id=0000174344` redirect here).
   Cloudflare shows "Un momento…" once; a real browser passes it.
2. Use the viewer's download button for the whole item as PDF, or the per-page image download for the openings
   that carry ff. 34–38. Save as `ottobon/ms994_full.pdf` (or the page images into `ottobon/img/`).
3. `python render.py ms994_full.pdf` renders every page at 300 dpi into `img/` and prints the page index; the
   letter is item 5 of the volume, the openings after the blank f. 33 and before the blank f. 39 (inventory:
   fols. 9, 14–21, 25, 33, 39 blank; fols. 10–12 and 14–21 missing, so folio numbers run ahead of image numbers).

## Route B: DECODE record R2252 (nine openings, needs a login)

https://de-crypt.org/decrypt-web/RecordsView/2252 is "BNE_ms.994_LuisValledelaZerda_5_34r_63v", 9 images,
symbol sets Alphabet + Numerical, origin Venice. After login the image files are
`https://de-crypt.org/decrypt-custom/filesrv/?file=IMG_R2252_I160NN_PM.png` with (NN, M) = (36,1) … (44,9).
From the thumbnails (decode/th_R2252_P*.png): image 1 = f. 33v blank + f. 34r heading (Valle's cartouche and
description); 2 = f. 34v blank + f. 35r cipher; 3, 4 = ff. 35v–37r cipher, both pages full; 5 = f. 37v full +
f. 38r short, signature, seal; 6 = f. 38v (address side) + f. 39 blank; 7–9 blank openings.
Save the nine PNGs into `ottobon/decode/` under their DECODE names; `render.py --decode` splits each into
left and right pages.

## Then

Transcribe into `ct.txt` with the grammar in parse.py (one line per written line, `# f.35r l.1` labels),
run `python structure.py ct.txt`, and follow the plan in NOTES.md §5.
