# Brief: transcribing Gramont to Montmorency, Rome, 11 October [1529] (BnF fr. 3091 no. 23, ff. 45r-47v)

## Task
Transcribe the cipher on your assigned page at glyph level, decode it with Lasry's key, and produce a
reading. The letter is in French (1529, Rome; Gabriel de Gramont, bishop of Tarbes, French ambassador to
Clement VII, writing to Anne de Montmorency, grand maître). Apart from the clear opening words it is wholly
in cipher. The key is SOLVED (Lasry 2023); nobody has published the plaintext. Your job is careful reading,
not cryptanalysis.

## Images (already downloaded, do NOT re-fetch from Gallica)
Two-page openings, about 8700 x 5860 px, in C:\Users\dbour\cypher\gramont1529\full\
* btv1b9060253s_c049.jpg: right page = f. 45r (x ~ 0.55-0.97 of width)
* btv1b9060253s_c050.jpg: left = f. 45v (x ~ 0.08-0.50), right = f. 46r (x ~ 0.53-0.96)
* btv1b9060253s_c051.jpg: left = f. 46v, right = f. 47r
* btv1b9060253s_c052.jpg: left = f. 47v (9 cipher lines, then the clear close)
Make your own crops with Python/PIL, e.g. `python crop.py <img> x0 y0 x1 y1 out.png [maxwidth]`
(fractions of the image; autocontrast). Best reading size: one line split into 2-3 pieces, each about
1300-1800 px of source, no downscaling (or 1.5x up). Line pitch is about 115-120 px. Lines slant a
little, so use tall enough strips (about 180 px) and follow the baseline. Put crops in your own subfolder
(e.g. work_45r/) so nothing collides with other agents.

## Key (Lasry, "BNF Francais 3040", 05/11/2023): see img/BnF_fr3040_f16.png (and enlarged k3040.png)
Alias letters for `decode.py` (one ASCII char per glyph):

| plain | glyph -> alias |
|---|---|
| A | small ring "o" -> `o`; small triangle "Δ" -> `A`; double upright crossed "ǂǂ/#" with ONE bar each way, loose -> `H` |
| B | "ß/β" (8 with open top-left) -> `B` |
| C | lying eight "∞" -> `C` |
| D | plain cross "+" -> `+` |
| E | caret with hook "ʌ" -> `L`; capital "R" -> `R`; "W" -> `W` |
| F | "ρ / P with loop" -> `F` |
| G | inverted T with underline "⊥" -> `G` |
| H | "7" -> `7` |
| I | "4" -> `4`; long "j" with dot/ring at foot -> `J`; dumbbell "o-o" -> `i`; crossed flourish "ꝭ/ⱡ with bars" -> `Y` |
| L | "L" with small o at right ("Lo") -> `l` |
| M | hash "#" (two bars each way, compact) -> `#` |
| N | "8" -> `8` |
| O | cross over ring "♀" -> `q`; "9" with cross -> `g`; bold saltire "X" -> `X` |
| P | check "✓" -> `v` |
| Q | bold "B" -> `b` |
| R | bar with hooks at both ends (a wavy "π" / "ᚁ") -> `r` |
| S | lozenge "◇" with tail -> `s` |
| T | long stacked spring "ʒʒʒ" (vertical zigzag) -> `t`; "σ" with bar (T over o) -> `d` |
| V | "K" -> `k`; "n" -> `n`; filled eye / blot "●" -> `e` |
| X | "Z" -> `z` |
| Z | "ɱ / m with tail" -> `y` |
| LL `=` (bold bar); MM `M` (big L-shape); NN `N` ("Rx"); PP `P` (bar with small m on it); RR `U` (8 with open top, "ꝏ"); SS `S` (8 on a crossed bar); TT `E` ("Ш" on a bar) |
| ET: flat "T" bar with stem (like a table) -> `T` |
| heart "♡" = a person's name -> `&`; "Lo" with dots (L° with two dots) = CON -> `c` |
| nulls / word separators: vertical stroke `|`; reversed "9 / ɔ" -> `)`; "-o-" -> `~`; "4 with a flag" -> `f` |
| unknown: pencil shape -> `!`; other -> `?` (describe it in the notes) |

Hard pairs to watch: "4"(I) vs "4 with flag"(null); "#"(M) vs "ǂǂ"(A); "B"(Q) vs "ß"(B) vs "8"(N) vs "S"(SS 8-on-bar)
vs "U"(ꝏ RR); "L"(E caret) vs "l"(Lo = L); "T"(ET) vs "d"(σ-bar = T) vs "G"(⊥).
Superscript marks above a glyph (a tilde, a small o) may be abbreviation marks: note them.

## Method
1. Crop line by line. Write each line's glyph aliases, e.g. `dr R+W C4#L e T A k l t r R e ...`
2. Decode: `python decode.py "dr R+W C4#L e"` (from C:\Users\dbour\cypher\gramont1529). Read the output as
   16th-century French (no word division; `&` = et; `<P>` = a person sign). Where a glyph is ambiguous, try the
   alternatives and keep the one that gives French. Words for context: le pape, l'empereur, le roy,
   Madame [Louise de Savoie], le grant maistre, Bouloigne (Bologna, where Pope and Emperor met Nov 1529),
   Florence, Perouse, le prince d'Orange, Andre Doria, Venise, le duc de Ferrare, le duc de Milan (Francesco
   Sforza), Anthoine de Leyve, le cardinal de Medicis, la paix de Cambray, Messeigneurs les enfans (the
   hostage princes), la royne Eleonor, Genes, Naples, Hongrie, le Turc, concile, Monsieur de Bayonne, Raince.
3. Deliverable: write `<page>_transcription.md` in C:\Users\dbour\cypher\gramont1529\ (e.g. `f45r_transcription.md`):
   for every line, `Lnn | aliases | decoded | word-divided French reading`, with (?) for doubts and
   `[illegible]` where you truly cannot see. Then a continuous modern-French reading of the page and a
   5-10 line English summary. Do not invent: accuracy over completeness, but cover every line.
4. Report back: how many lines, your estimate of the share read confidently, and any corrections to the key
   (glyphs that clearly mean something other than the table says).
