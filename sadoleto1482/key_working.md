# Sadoleto 1482 cipher: working key

Built by aligning R1101 p. 2 with its contemporary clear copy 7a (Vestigia 1283) and R1104 with 13a (Vestigia 1295).
Word divisions are kept; clear words are mixed into the cipher; "quid" in clear letters stands for "perchè".
Confidence: H = seen in several aligned words; M = one or two; L = guess.

**20 Sep follow-up:** `verified_groups.md` supplies source comparisons for
alphabetic `dom` and the repeated X group referring to the Signoria of Venice.
Its C grade follows the repository convention, unlike this older confidence column.

**Page-reference correction:** the R1101 control cited here as "p. 2" is
DECODE I5655 (filename P2), showing the original letter's final page,
Vestigia 1284 photograph `(105)`. See `alignment_r1101.md` for the full crop
and its match to clear-copy page 3.

| glyph | value | conf | aligned words |
|---|---|---|---|
| ʒρ (z with looped tail) | a | H | pigliare, questa, impresa, stare, fara |
| –1 (dash + stroke), ┴ | a | H | "a" alone, amore, la |
| > (open angle) | b | M | benivolentia, Buda |
| \| (plain tall stroke) | c | H | che (\|2б), certa |
| φ (stem through loop) | d | H | de, modo, dice, Buda |
| б (flat-topped 6), ь | e | H | che, me, per, venire, dice, certa |
| 8 | f | H | fo, forse, fra, fara, facessino |
| → / ) | g | H | liga, pigliare, gli |
| 2 | h | H | che |
| ω | i | H | pigliare, impresa, dice, li, in, liga |
| π (double-stem) | l | H | la, liga, lo, pigliare |
| 4 | m | H | me, impresa, modo |
| 6 (round-topped) | n | H | non (636), in, ne, niente |
| 3, η | o | H | lo, modo, questo, non |
| Δ (arrow-A, stem through apex) | p | H | per, pigliare, impresa, pare |
| Δ with looped apex, A | q | H | questa, questo, quello |
| ſ (long r), Γ | r | H | per, sera, fara, certa |
| 7 | s | H | se, sera, questa, epsa |
| μ, ρ | t | H | et, stare, certa, questa |
| u, и | u | H | questa, Buda, sua |
| Ɣ (v with loop) | v | H | venire, vedera |
| ʉρ | et | H | |
| \|2б | che | H | |
| 636 | non | H | |
| quid (clear) | perchè | H | 13a "perche" = R1104 "quid" |

## Additional known-plaintext control: ss and e

**Stemless triangle:** z (C), controlled by R1101/7a's `cruzata` in the
queen passage. This resolves R1106 `anzi` (C). See `z_control.md` for the
independent alignment and distinction from stemmed p and looped q.

**Further control:** `ff_control.md` records a cross-stroked, looped upright
with descending stem as ff (C), aligned in R1101 `affinita`. It supports
R1102 A04 `offerta` (C); final-page `effecto` remains M because the following
e is not yet secure. Do not conflate this sign with d or the short-stemmed ss.

The old shape labels conflate distinct pen forms. R1101's final-page
`facesse` and `imparasse`, aligned with 7a page 3, establish a **double-s sign**:
a short ascending upright with a small loop at its foot, without the long
descending stroke of d. Its resemblance to the approximate Unicode `φ`
does not make it a d. The following e can also take a low angular/hooked
form rather than the conspicuous flat-topped 6 form. Consequently the old
ASCII-like glyph strings should not be decoded mechanically as exact shapes.

Controls: DECODE I5655 rectangles `(1930,335,2850,455)` and
`(1380,590,2200,720)`, reproduced in `img/ss_control_facesse.png` and
`img/ss_control_imparasse.png`. The latter includes the contrasting d of
the following `de`. Grade C: known plaintext, not a primary cipher key.

This distinction supports R1102 page 2 `fosse a` at the end of line 3 and
`gli facesse` at the beginning of line 4. Subsequent checks identified the
intervening group as K, referring to the Hungarian king (`repeated_k.md`),
and the word after `facesse` as `offerta` (`ff_control.md`). The exact royal
style represented by K remains unestablished. This distinction also explains why substituting
only the old single-letter labels produced implausible strings in these places.

| Additional group | Reading | Verification |
|---|---|---|
| Former `494` label | d-o-m | Alphabetic title; d/o/m matched locally in R1102, C |
| Former `3ί2ии`, X | [Signoria di Venetia] | Same group in R1106 p. 3 l. 3, aligned with 26b/Vestigia 4004; referent verified C, exact lexical expansion unspecified |
| K, six-sign group shared by R1102 A03/D01 | [Re di Hungaria] | R1101 I5655 `(1804,1352,2080,1432)` aligns to 7a's royal title; referent C, exact expansion/internal sign values unresolved; see `repeated_k.md` |
