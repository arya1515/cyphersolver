# Third pass brief (one page per agent): split the merged glyph tokens using the calibrated guide

Working dir: C:\Users\dbour\cypher\pelissier1592 (Git Bash; python). Page files: t<folio>.txt (token transcription; a frozen
copy of the pass-2 state is t<folio>_p2.txt), img/c<canvas>.jpg (full-res scan).
Canvas map: 46r=100 46v=101 47r=102 47v=103 48r=104 48v=105 49r=106 49v=107 50r=108.

READ FIRST: GLYPHS.md (the calibrated glyph guide, from 1,764 signs of Pelissier's letters nos. 45/46 aligned with their
clear-text decipherment), then look at the exemplar crops in cal/atlas/ (and the contact sheets cal/crops/sheet*.png)
until you know the split shapes: 4 / z4 / 4y / 4_ ; X / #x / x ; + / Lo ; o / dc / Q / D ; pi / tt ; 6 / 6^ / 6c ;
8 / Z8 ; 56 / s6 ; T / Tp / Tz / Tr ; q / q9 ; E / e3 ; 7 (= b).
Key facts that change earlier readings: plain 4 is n or m, NOT t (t is z4 / 4y / h); T with a tail is s, not g; 56 plain = y,
flourished s6 = c; 7 = b; + is never e; II is never e; pi is never s; A is never n; the barred 8 (Z8) = q.

Decoder: `python beam.py t<folio>.txt` (candidates in cands.txt; do NOT edit it; tell me if a token is missing).
Crop tools: `python crop.py img/cNNN.jpg X0 Y0 X1 Y1 out.jpg 1900` (Read the jpg to view); `python bands3.py NNN X0 X1 Y0 Y1 400`.
Put scratch crops in crops/p3_<folio>_*.jpg. Crop about 500-700 px of original width per view.

Task:
1. Go through EVERY cipher row of t<folio>.txt against the image, left to right, and replace each token from a merged family with
   its split token as seen in the image (e.g. `4` -> `z4` where the 4 has the hooked lead-in; `o` -> `dc` / `Q`; `T` -> `Tz`;
   `56` -> `s6`; `8` -> `Z8`; `X` -> `#x`). Also fix genuine misreadings, missed or doubled signs. Never change a sign only to
   make French appear; every change must be visible in the image. Save the file after every few rows (work survives interruption).
   Keep clear-text [[...]] lines and # comments; add a `# p3:` comment for notable changes.
2. Run the decoder and re-read rows that still don't make French (they are where the remaining misreadings are).
3. Rewrite reading_<folio>.md in the same format as before (continuous 1592 French, deciphered stretches in {braces}, [?] for
   unrecovered words, (?) for doubtful; English summary; glosses checked; rows still unresolved). Improve on reading_<folio>_p2.md;
   don't lose readings it already had unless the image contradicts them.
Report back: rows revised, how many [?] remain vs. before (count them in both files), the new readings of formerly open passages,
and any glyph that GLYPHS.md doesn't cover (with a crop filename).
