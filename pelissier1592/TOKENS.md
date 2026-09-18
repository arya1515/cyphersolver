# Pelissier cipher (BnF fr. 3982) — token vocabulary

Transcription files (`t46r.txt` etc.) use one token per cipher sign, space-separated, one cipher run per `Cn:` line.
Clear-text passages go in `[[...]]`. Lines starting `#` are comments. Decode with `python beam.py t46r.txt`
(candidates in `cands.txt`).

Key = Tomokiyo's reconstruction (`league2_key.png`, zoomed crops `crops/k0.png`..`k3.png`), checked on f. 46r.

| token | glyph | letter |
|---|---|---|
| q | loop with long descender (ϙ / ϱ) | a (rarely f "9") |
| T | T with hooked top (ፐ) | a |
| x | plain small x | a |
| f | long ʃ with crossbar | a |
| y | ɤ/ƴ with crossbar | b |
| z | small z / 2 on its own | c |
| v | ɤ-like v with loop | d |
| 6 | plain 6 | d |
| n | cursive n / ʍ (like "n" joined) | d |
| g | g / ʒ with long tail | e |
| D | ∂ (backward-6 / delta curl) | e |
| t | small ɛ with tail / "ŧ" (the common small cross-e) | e |
| e3 | ε (open e / epsilon, often with tail below) | e |
| S | ∫∫ tall double long-s (ʃʃ, "ff"-like) | e |
| w | ʊʊ / vv | et |
| 12 | "12" / "Tz" | g |
| 19 | "19" | f |
| + / 7 | plus-cross / 7 | h |
| pi | π (ᴨ) | i |
| 6^ | 6 with bar/stroke on top (б) | i |
| 33 | 33 | i |
| ph | φ | i |
| 60 | 60 (with or without mark) | y / i |
| I | capital I with serifs (Ɨ) | l |
| II | ⫴ / box-like double bar (∐) | l |
| p | long p with descender | l |
| m | cursive m | l |
| HH | ⧺ (hash-like, two verticals with bars) | m |
| oo | oo | m |
| 4_ | 4 with underline / ǂ-cross with base | m (maybe o) |
| 8 | 8 | n |
| s | small s | n |
| 4 | plain 4 | n (or t) |
| o. | o followed by a dot | n |
| o | δ-like o with tall ascender (ᵹ) | o |
| Lo | ⊥ inverted T | o |
| F | Ƒ / ŧ with two crossbars | o |
| 24 | 24 | o |
| E | E / ɛ capital | p |
| 26 | 26 | p |
| H | ℋ slanted H | q |
| 28 | 28 | q |
| r | ξ / ʓ zigzag (§-like, tall) | r |
| 30 | 30 | r |
| Q | ᘓ loop (Q-like) | r |
| 80 | 80 | s |
| dz | ʤ / "ẟz" (δ over z, ligature) | s |
| k | k | s |
| tt | π with tail (ϖ, "π~") | s |
| J | ℑ / script J (tall hooked) | ss |
| 4y | ɣ / "y" with loop (like "4y" ligature) | t |
| h | h (ɦ) | t |
| L | ℓ loop-l | u |
| A | A (cursive, tall) | u |
| d | d (looped ascender) | u |
| 36 | 36 | u |
| X | x with bar (ӿ). NB a bold ✗ is a NULL; if clearly the null form write `#x` | u / null |
| oH | "oH" (o + H) | x |
| 44 | 44 | y |
| 56 | 56 (s6, often with a flourish) | **c** (NOT y: gives catholique, cens, action, ceste) |
| Z | boxed z (Ƶ) | z |
| # | ‡ triple-barred cross | null |
| #o | ƒ/‡ standing on a δ loop (cross over 8/δ) | null |
| ... | ııı three short strokes | null |
| C | C | null |
| lam | λ-like ✗ with long ascending stroke | null |
| ? | illegible / blot | — |

Two-digit numbers: write them as ONE token when you are sure (24, 26, 28, 30, 33, 36, 44, 56, 60, 80, 12, 19).
If a "z" is followed by 4/6/8 and you can't tell whether it is "24/26/28" or z + digit, write `z 8` etc.
(the decoder tries both).

Scribe habit: when a line is restarted, the tail of the previous line may be repeated at the start of the next line;
transcribe each repeated run once and note it in a `#` comment.

## Corrections after the first full pass (all pages)

- `56` = **c** (third glyph in the key's c column), not y. Decoder now prefers c.
- Token `o` has been used for two similar glyphs: **δ with a straight ascender = o**, and **ᘓ / ∂ with a closed loop and
  curled top = r** (key r column, 2nd cell; token `Q`). Where you can tell, write `Q` for the r-glyph. The decoder now
  lets `o` be o or r.
- `fr` = a small plain r-shaped glyph = **f**. `19`/`1 9` = f. `12` = g (confirmed by the gloss "langaige").
- `315` = a three-digit code group, apparently a word (occurs after "au"); decoded as [ROY] provisionally.
- Boxed/barred 8 (`Z`): z, s (ilz) or n by context.
- Comments in cands.txt start with `//` (not `#`, which is the null token).
