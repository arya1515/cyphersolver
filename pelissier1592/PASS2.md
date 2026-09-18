# Second pass brief (one page per agent)

Working dir: C:\Users\dbour\cypher\pelissier1592 (Git Bash; python). Page files: t<folio>.txt (token transcription),
img/c<canvas>.jpg (full-res scan). Canvas map: 46r=100 46v=101 47r=102 47v=103 48r=104 48v=105 49r=106 49v=107 50r=108.

Read TOKENS.md first, INCLUDING the "Corrections after the first full pass" section (56 = c; token o is o OR r; fr = f).
Decoder: `python beam.py t<folio>.txt` (candidates in cands.txt, which you must NOT edit; comments there start with //).
Crop tools: `python crop.py img/cNNN.jpg X0 Y0 X1 Y1 out.jpg 1900` and `python bands3.py NNN X0 X1 Y0 Y1 400` (third-width
bands in b3/NNN/). Put scratch crops in crops/p2_<folio>_*.jpg.

Tasks:
1. Run the decoder. For every cipher row whose decode is not readable French, re-read the glyphs at high zoom (crop about
   600-700 px of original width, show at 1600) and correct genuine misreadings in t<folio>.txt. Typical fixes: r-glyph
   written as `o` -> `Q`; 24/26/28 vs z+digit; 4 vs 4y vs 4_; I vs T; X vs null; 6 vs 6^; t vs e3 vs +; missed or
   doubled glyphs at crop joins; rows joined wrongly across the slant. Never change a glyph only to make French appear;
   every change must be visible in the image.
2. Then write reading_<folio>.md: the page as continuous text in 1592 French (keep period spelling; expand cipher runs
   into words; put clear-text passages in plain type and the deciphered parts in the same flow, marking deciphered
   stretches with {braces}), with [?] for words you cannot recover and (?) after doubtful words. Follow it with a short
   English summary of the page's content (5-10 sentences: who, what, where), a list of interlinear glosses you verified
   (gloss text + the tokens it sits over + whether it agrees with the key), and a list of rows still unresolved.

Report back: counts of rows fixed, the reading, and anything about the key that contradicts TOKENS.md (with evidence).
