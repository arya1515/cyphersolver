# Transcription brief v2: Maffeo da Treviglio's cipher (Buda 1489-90) — transcribe straight to VALUES

The key is known (Somogyi 2016, pinned to glyphs in this project). Your job is to read each cipher sign on the
numbered strips and write its VALUE, using the exemplar sheet `GLYPHS.png` (also split as GLYPHS_1.png and
GLYPHS_2.png; Read them first and keep them in mind). The language is Italian chancery prose of 1490 (Lombard
forms: "olduto", "ali 8", "de qua", "Ser.mo Re", "Vostra Excellentia"). Decode as you go: the values of a line
must form Italian; if they do not, re-examine the signs you were unsure of.

## The signs (value ← sign)
Letters: a ← "r" (small r), "i" (dotted i), "f"; m ← "a"; b ← "m" with a macron; d ← "x"; e ← "//" (two short
parallel slashes, the commonest sign), "4" (a 4-shaped sign with a tail, also looks like a q); l ← "d" with a
looped top; s ← the other d-form (straight ascender, no loop) and "b" with a bar through it; t ← "p" with a
stroke through the descender, "o" with a horizontal bar; u/v ← "6", pointed "v"; r ← angular "z" (flat top
stroke); o ← rounded "3", epsilon "ε"; n ← "g" (with a long tail), "b" with a small superscript t, "v"?;
q ← ")" crescent (often with a dot inside); p ← "c"; i ← "n" (cursive n); c ← "s" (small s); h ← "9".
Syllables and words: co ← "b"; ca ← "b" with a stroke; ce ← stroked b with a dot; no ← b with superscript o;
ne ← b with superscript e; ra ← q with superscript a; ro ← q with superscript s; re ← q with superscript e;
so ← m with superscript u; sa ← m with superscript a; si/se ← m with superscript o / e; ta ← "L" with
superscript a or a barred l; te ← "L" followed by a colon; ti ← tall l/k with a dot; to ← "t" without descender;
et ← "x" with a bar or "r" with a stroke; in ← "n g"? (unconfirmed); che ← unknown sign; g ← "8"? ;
"Ser.mo Re de Hungaria" ← capital "M" with a colon; "S.V." ← capital S with a dot; "madonna Bianca",
"zo. Corvino", "il vescovo varadino", "la sua Maesta" ← unknown signs (report any capital or odd sign).
Nulls: "w", "÷", isolated dashes and dots (write `-`).
Distinguish carefully: z (r) vs 3 (o); looped d (l) vs straight d (s); "6" (u) vs "b" (co); "o" (t) vs "ε" (o);
"c" (p) vs "s" (c); superscripts change the value (b, b^t, b^o, b^e, b-stroke are five different signs).

## Input / output
Strips in `seg/strips/<page>_L<line>_<part>.png` (boxes and indices; boxes are imperfect: a box may hold two
signs, a sign may be split, a superscript may have its own box — the superscript belongs to the sign to its
left/below). Write `trans/<page>_v.csv` with header `line,idx,value` — one row per sign, `idx` = the box index
(12a/12b if two signs share a box). For an unknown sign write `?<description>` (e.g. `?w-with-tilde`).
Also write `trans/<page>_v.txt`: the decoded text line by line, words separated as you understand them, with
`[?]` for unknowns. Report rows per line and the unknown signs at the end. Touch no other files.
