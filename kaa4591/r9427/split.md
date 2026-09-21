# R9427 f.287: splitting d -> d/K and # -> #/U (following sysA/r9410_split.md)

Method: image rotated 180°. P1 lines 11-35 and all of P2 were checked in three-line bands
(left half and right half, ~1500 px wide crops, autocontrast, upscaled to 2400 px). Lines 1-10 of P1 were converted from R9427
codes to R9410 codes with `key_full.tsv`. Their H (= R9410 #) was split using the interlinear gloss rather than the shape.
Output: `transcription_v2.txt`, built by `build_v2.py` from `transcription.txt` plus a list of edits.
The bands are ~3x magnification, below the ~15x close zooms used for R9410. Calls marked `?` need a close zoom.

## Counts in v2 (whole letter)

| code | count | value (R9410) |
|---|---|---|
| d (small δ) | 90 | l |
| K (big looped S/ℓ) | 9 (2 doubtful) | word sign |
| # (slanted ‡‡, bar overhangs both sides) | 88 | g |
| U (upright H, left stem hooked, no left overhang) | 17 (4 doubtful) | u/v |

## K (from d)

| where | context | note |
|---|---|---|
| P1.12 end | `E3vE K b nn w` | tall looped form before the lollipop b |
| P1.17 last sign | `...yE4q K` | line-final large loop |
| P1.25 | `x9dnmEwv K w4q` | clear large ſ-loop, much taller than the δ in `x9d` just before it |
| P1.27 first sign | `K mywvjo9v...` | line-initial large loop (was `d?`) |
| P1.30 last sign | `...A w K?` | tall, line-final; doubtful |
| P2.11 first sign | `K v3wEwv...` | big flourish with its tail sweeping left, as at R9410 l.10 |
| P2.24 | `dw7 K b t3#w` | was `b? d`: the sign order is δ-form then lollipop, and the δ is the large looped K |

K keeps turning up at line starts and ends and before `vertrag-` type groups, as in R9410.
Every other δ is the small form (e.g. `x9dE`, `5dx`, `jo5dnn`, `D4dy`, `5dy`) and stays d.

## U (from #)

| where | context | basis |
|---|---|---|
| P1.01 | `dwUEy` durchlEUchtig | gloss H=u |
| P1.02 | `m?m?U4` neUe | gloss H=u |
| P1.05 | `X U9q` (F.G.) Von | gloss H=v/u |
| P1.11 | `a+U9qo` | upright hooked H |
| P1.12 | `a+Uwvyg5#` | upright; `Uwvy..#` = ver-trag pattern (R9410 `Uwvyv5#48` vertragen) |
| P1.13 | `mQ U 8 #x` | first of the pair is upright, the second slanted |
| P1.22 | `# U? wy` | a second H-form follows the ‡‡ that the old transcription dropped (inserted, doubtful) |
| P1.23 | `y Uwvm?j3` | upright, ver- pattern |
| P1.23 | `ny U? m@` | doubtful |
| P1.24 | `4v Uwvyg9xy` | upright, vertrag- pattern |
| P2.02 | `ADd Uw#4q` | upright H followed by a proper ‡‡ |
| P2.03 | `o U qQwv` | small upright H |
| P2.08 | `Uwvo3qdy` | line-initial upright, ver- pattern |
| P2.09 | `v? U? qnnwv` | doubtful |
| P2.18 | `nnwv U? wqEwq48` | no left overhang; doubtful |

All the other # have the ‡‡ shape, with the crossbar projecting on both sides, and stay # (g).
In lines 1-10 the gloss reads H=g in five places. The H's whose gloss value is unclear (k, m, n?, t?, w?, d, b?) default to #.

## Other corrections

- P1.24: `y 8? # q` -> `y b # q`: the sign is the lollipop b, not a round 8.
- P2.24: `7 b? d t3` -> `7 K b t3` (see above).
- P1.22: U inserted after the first # (see above).
- Not changed but worth a close zoom: P1.12 `5xd7` (the d looks like a gapped 8), P1.35 `qb?d?84w` (the image seems to show
  only a lollipop and an 8 there, `qb84w`), P1.34 `5dd?b4q`, P2.22 `ywb5q` and P2.23 `wbwA` (these b's may be tall δ).
- The R9427 sign A (lines 1-10, gloss b/n) has no R9410 code. It is written `{A}`.
