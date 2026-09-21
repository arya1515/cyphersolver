# Brief: reading the cipher passages of Mâcon's letters to Montmorency (BnF fr. 3053, 1536-37)

## Task
Letters from Charles Hémard de Denonville, bishop (from Dec 1536 cardinal) of Mâcon, French ambassador in Rome,
to Anne de Montmorency, grand maître. Mostly written in clear French; some passages (a few lines to ~15 lines) are in
cipher. The key is KNOWN ("Mascon's cipher": Tomokiyo, reconstructed from fr. 3053 itself; Lasry 2023). Nobody has
published the plaintext of these letters. Your job is careful reading, not cryptanalysis.

For each assigned DECODE record: (1) give the date/place of the letter (from the clear text, usually at the end) and a
2-4 sentence summary of the clear text around the cipher; (2) transcribe every cipher line to aliases, decode, and give
a word-divided French reading; (3) note any contemporary interlinear or marginal decipherment (some margins carry one:
compare it with your reading and use it to correct the key if needed).

## Images (already downloaded; do NOT fetch anything from the web)
C:\Users\dbour\cypher\rome1536\img\IMG_R<rec>_I<id>_P<n>.jpg - each is a horizontal CROP of a page (about 3000 px wide),
consecutive P numbers overlap and go down the page, pages in order; the missing P numbers are not needed.
Contact sheets (small) in C:\Users\dbour\cypher\rome1536\view\sheet<rec>.jpg to find the cipher blocks.
Crop with Python/PIL (ImageOps.autocontrast), one line split in 2 halves of ~1400 px source, strip height ~260 px,
no downscaling. Put crops in C:\Users\dbour\cypher\rome1536\work_<rec>\ only.

## Key
Read C:\Users\dbour\cypher\gramont1529\macon_key.md fully (glyph descriptions, aliases, hard pairs, code groups
30 = pape, 40 = roy, 20 = l'Empereur). Key tables as images: C:\Users\dbour\cypher\gramont1529\img\francisMacon.png,
francisMacon2.png, francisMacon3.png (Tomokiyo, from fr. 3053) and BnF_fr3071_f9.png (Lasry). Look at them first.
Decoder: `python C:\Users\dbour\cypher\gramont1529\macon_decode.py "<aliases>"` (spaces ignored; {nn} = code group;
[..] copied through; unknown alias printed in parentheses). Unknown glyph: `?` and describe it.
Observed in this volume: a hooked sign like "ʃa"/"ʃo" (probably E, ring with long tail) and "ʃ" alone (D), "≠" (P),
"G-loop" (T), "Δ" (I), "X" saltire (L), "10" (L), "m over ʒ" (U). Numbers written as pairs (20, 30, 40, maybe others)
are code groups: record any other number and guess its meaning from context.

## Output
Write C:\Users\dbour\cypher\rome1536\R<rec>.md per record AS YOU GO (append after each passage, so nothing is lost
if you are interrupted): letter heading, clear-text summary, then per cipher line: `aliases` / decoded / reading, then
a clean running reading of the whole passage with [?] for doubtful words and a confidence estimate (% of letters).
Also a short section "Key notes" for any glyph that behaved differently from macon_key.md, and new code numbers.
Final message: for each record, date, cipher line count, confidence, and a one-paragraph English summary of what
the cipher says.
