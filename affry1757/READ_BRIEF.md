# Brief: read an undeciphered d'Affry 1757 code letter with the rebuilt key

Folder C:\Users\dbour\cypher\affry1757. Same code as the letters Lyonet deciphered (align/*.tsv are group-by-group
alignments of 7 deciphered letters; key_M.json is the key voted from them, amb_M.json lists ambiguous groups).
`python read.py R<rec>` prints the letter with the key ([n] = unknown group). `python view.py U R<rec> a b` shows
groups with positions. The code: groups 1-1199 stand for words, syllables, letters, names; homophones; 13 = full stop;
105/107/797/245 are sometimes nulls. Printed context for 1757: Bussemaker, BMHG 27 (1906), Dutch summaries in
bussemaker.txt (search the letter's date).

DECODE's digit transcription (decode/DOC_R<rec>_*.txt) has slips: 8 read as 0, groups run together or dropped,
lines repeated. Where the reading breaks, check the digits on the image: `python crops.py img/<file>.png -90 <tag> 4`
(sm/<tag>_k.jpg). Also check the DOC file for clear-text lines on the pages and note where the cipher sits in the letter.

Task for R<rec>:
1. Produce read/R<rec>.md: header (date, addressee, number, pages); then the French reading in running text with word
   division, accents optional. Mark unresolved groups as [n], and inferred values (not in key_M) in {braces}.
   Then a short English summary of the content, and a comparison with Bussemaker's summary for that date if any.
2. Produce read/R<rec>_new.tsv: group, inferred value, confidence (H/M/?), evidence (context, repeated occurrences).
3. Final message: fraction of groups read (keyed + inferred), the main content in 3-4 sentences, DECODE digit
   corrections found, and the new values list.
Do not edit key_M.json, align/, or other letters' files. Do not commit. At most ~10 image crops.
