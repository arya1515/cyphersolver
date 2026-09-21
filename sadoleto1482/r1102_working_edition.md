# R1102: consolidated working edition

20 September 2026. Status: in progress. This is the current reading of the
encrypted passages, superseding the uncorrected 19 September text in
`reading_r1102.md`. It is **not complete**. Ordinary intervening prose has not
been edited here, and the extracts below must not be joined into one speech.

C = read with the alphabet reconstructed from contemporary known plaintext.
M = uncertain proposed reading. `[Uxx]` = unread material of unmeasured length.
Punctuation, apostrophes and most word divisions are editorial. Parentheses
around `e bastardo` occur in the manuscript. `[Signoria di Venetia]` expands
one code group whose Venetian-government referent is verified; its exact
lexical expansion is not established. `[Re di Hungaria]` similarly expands
group K by its verified referent. See `verified_groups.md` and `repeated_k.md`.

## A. Manuscript page 2, bottom seven lines

Source: DECODE I5657, also Vestigia 1286 photograph `(110).JPG`.

```text
A01  essendo in Buda per partire per venire a Posonia
A02  sapi per gran secreto da dom Francesco como [Signoria di Venetia] haveva
A03  scripto ad Francesco Quirino che e qua fosse a [Re di Hungaria]
A04  gli facesse offerta como [Signoria di Venetia] voleva havere seco bona
A05  amicitia et voleva dargli Vegla et voleva lo fi-
A06  -gliolo (e bastardo) per loro capitaneo de l'armata
A07  per mare et gli voleva dare ogni anno cento milia
```

Accepted wording follows the existing C reading and the later corrections;
U01's K group now has a verified royal referent; U02 is `offerta` (C). `dom` is the literal
alphabetic title. Identifying Francesco as Francesco d'Aragona or the son as
János Corvin is historical inference, not additional cipher text.

The later double-s control in `key_working.md` supplies `fosse a` and
`facesse` (C): compare the ss/e sequence in R1101's known-plaintext
`facesse` and `imparasse`. R1102 source views are `img/l3_end_context.png`
and `img/l4_start_context.png`. Earlier U01/U02 labels included these newly
read words. Subsequent comparison resolved U01's group as K, referring to the
Hungarian king. The earlier `pregare` suggestion is superseded. The separate
ff control in R1101 `affinita` now supports `offerta` (C); `ff_control.md`
records the source rectangles and the complete o-ff-e-r-t-a sequence.

The existing segmentation supplies the following **inspection envelopes**.
They include overlapping strokes and occasional marks from adjacent lines;
they are not reliable character segmentation or character counts.

| Unit | Envelope (x0,y0,x1,y1), original pixels |
|---|---|
| A01 | 299,2320,2128,2422 |
| A02 | 308,2343,2072,2484 |
| A03 | 304,2457,2038,2559 |
| A04 | 282,2496,2030,2620 |
| A05 | 286,2608,2026,2704 |
| A06 | 280,2646,1936,2774 |
| A07 | 280,2729,2145,2880 |

Derived from `seg/r1102b_glyphs.json` by taking the union of its component
boxes for each line and adding its (280,2320) offset. Native unboxed line
strips are in `img/L/b2_L0n_k.png`. Use original images to resolve overlaps.

## B. Page 3, opening continuation

This directly continues A07. Source rectangle `(2280,365,4150,665)` in the
same photograph; enlarged overlapping views `img/cont0.png`, `img/cont1.png`.

```text
B01  ducati. ma voleva potere soldare et [U20] cauare gente
B02  de questo regno. et questo l'aveva saputo sua [U03]
B03  per subtile via et non volse per cosa del mondo che
B04  io monstrasse saperne cosa alcuna.
```

The latest 20 September reinspection corrects `subtil via` to **`subtile via`**:
`img/cont0.png`, third cipher line, shows an additional low angular e after
the double-stem l and before the looped v of `via`. The sequence is
s/u/b/t/i/l/e, followed by v/i/a (C). The earlier acceptance of `subtil`
overlooked this final sign; it was not an intentional normalization.
The full-width B01 view supports `soldare` and `cauare gente` (C), replacing
their former M status. In the second word the third sign is u-shaped; `cavare`
is a normalized spelling, not the literal sign label retained here. A small
cross-shaped mark between `et` and `cauare` was previously omitted and is now
preserved as U20. Its function is unresolved; no null or additional plaintext
word is inferred. Source: `img/r1102_recruitment_full.png`, rectangle
`(2280,365,4230,525)`, and `img/r1102_recruitment_detail.png`, rectangle
`(3080,370,4130,475)` enlarged twofold. A stain crosses the upper strokes of
`soldare`; the visible sequence and lower strokes support the reading, but
the viewing aid does not restore the obscured ink.

U03 is the short abbreviation/sign
after `sua`, previously labelled `[S.]`; no expanded identity is supplied.
This is a working reading, not an assertion that every glyph in these four
lines has an independent control match.

A07–B01 directly supply **cento milia ducati**, so the denomination does not
depend on importing it from the August letter or later correspondence.

## C. Page 3, short middle cipher span

Separated from B by ordinary prose. Source `(2300,995,4200,1225)`;
`img/cont2.png`, `img/short_left.png`, `img/short_right.png`.

```text
C01  gli poteriano fare tale
C02  grande partito che epsa non scia che [U06]
```

These are local C extracts. Neither the intervening clear prose nor this
sentence has been read continuously. See `reading_r1102_additional.md`.

The later local comparison resolves U05 as **epsa** (e/p/s/a) and the
opening of former U06 as **scia che** (s/c/i/a, c/h/e), C. The source
rectangle `(3070,1110,4200,1235)` is preserved in
`img/r1102_epsa_scia_control.png`. Initial s in scia is the angular 7,
followed by the tall plain c, omega-like i, and looped a. Retain `scia`
rather than normalizing to `sappia`. U06 now denotes only the remaining
word after che, whose interior signs have not been securely read. Its
f-like first sign is not sufficient for a complete restoration.

**U04 resolved: tale (C).** The colour enlargement
`img/r1102_u04_tale_test.png`, I5657 rectangle `(3590,1040,4220,1150)`
at 3x, shows t/a/l/e after `fare`: the upright with right loop, looped-tail
a, double-stem l, and low angular e. The final low e is distinct from the
long descending r visible in the preceding `fare`; its form is already
documented by the R1101 doubled-s/e controls in `key_working.md`.
The word therefore joins the two cipher lines as `fare tale / grande
partito`, without supplying the still-unread final word U06. No new
alphabet value or historical identification is inferred from this reading.

**U06 sign audit:** colour rectangle `(3660,1110,4240,1250)`, enlarged
3x in `img/r1102_u06_colour.png`, preserves the entire ending to the fold.
`img/r1102_u06_contrast.png` uses blue-channel background subtraction
(Gaussian radius 18, multiplier 4). Comparison with the independent
R1101 `img/ss_control_facesse.png` makes an opening `facesse` plausible:
f/a/c/e, a short upright with a small dark loop, and a low angular stroke.
The latter two signs remain an ss/e hypothesis, not a new accepted word.
There are further signs to the right, including a double-stem form and a
comma-like form, followed by less secure strokes at the fold. Word boundaries
are unproved. A restoration consisting only of `fare` fails to account for
the visible sequence. No complete U06 reading is accepted, and it is not
assumed that the ending is a single word. The earlier phrase “remaining
word” above describes an old working segmentation, not an established count.

## D. Page 3, later monetary passage

Separated from the preceding span. The broader mixed region is approximately
`(2300,1310,4250,1950)`; the following extracts appear in `img/money0.png`
and `img/money1.png`.

```text
D01  [...] per ogni modo disponerse ad dare a questo [Re di Hungaria] cento milia
D02  ducati ogni anno sino a sei o septe anni che [U08]
D03  questa suma che li domanda et non seria gran suma alla
D04  liga considerata la [infinita utilita: M] [U09]
D05  non scio percio se sua maesta [U12] monstra desiderare et haver piu bisogno [U13]
D06  [U14] principio. ma [U15] alla liga [U16]
D07  tractare et non e da perder tempo et se [U17]
D08  [U18] a questo tempo et fare la bona [U19]
```

U08–U09 represent unedited surrounding material, not measured numbers of
missing symbols or words. D is not a complete transcription of the broader
mixed region. The duration in D02 must not be attached to the Venetian offer
in A without resolving the intervening discussion and its referents.

U08 has been narrowed: its initial **che** is now accepted C, from c/h/e
at the right edge. `img/r1102_u08_right.png`, source rectangle
`(3690,1360,4310,1530)`, shows the following s/e/r/i-like sequence but not a
secure final a at the fold. `seria` remains a candidate (M), compared with
the darker accepted `seria` on the next line in
`img/r1102_seria_control.png`, rectangle `(3160,1440,3740,1530)`.
The resemblance does not justify completing the obscured ending.

At D08, `img/r1102_dinari_left.png`, rectangle `(2290,1840,3280,1980)`,
shows a d/i/n/a/r-like sequence within U18. A monetary word such as `dinari`
is plausible, but its final sign and preceding word are not secure. U18
remains unexpanded. The image filename records the hypothesis, not a
verified reading. No amount or payer is inferred from this fragment.

The wider source view `img/r1102_money_context_above.png`, rectangle
`(2260,1120,4270,1510)`, extends D01: ordinary writing supplies
`per ogni modo disponerse`, followed by alphabetic cipher `ad dare a questo`
before K and `cento milia`. These are local C readings of the mixed line.
Former U07's group is now identified with K and its verified royal referent;
the earlier ellipsis retains the preceding unedited prose. This establishes
the king as recipient, but neither the payer nor the full conditional/proposal
syntax is yet securely transcribed. It does not identify this proposal with
the earlier Venetian offer.

D05–D08 extend the extract toward the end of the mixed passage. They are
local C readings, with gaps explicitly retained; the unit IDs are editorial
extract IDs and not a count of manuscript lines. Source region
`(2270,1480,4240,1980)` is reproduced in `img/r1102_money_end.png`.
The phrase `monstra desiderare` is also enlarged in
`img/r1102_desiderare.png`; the right-hand continuation is in
`img/r1102_money_last_right.png`. A proposed completion of U19 as `spesa`
is not accepted here. A subsequent full-height right-edge crop,
`img/r1102_final_word.png` from `(3300,1860,4320,1995)`, restores the lower
strokes but still leaves the penultimate sign ambiguous against the present
key. The contextual plausibility of `spesa` does not settle that sign. These extracts
do not establish who is showing desire/need or what negotiation is urged.

A further local reading extends D05 backward: `non scio percio se sua
maesta` (C), visible in `img/r1102_nonso_clause.png`, original rectangle
`(2520,1570,4120,1690)`. The original has the c sign in `scio`; it should
not be normalized silently to `so`. U12 retains the intervening unresolved
wording before `monstra`. The phrase identifies a royal subject in this
clause but does not complete its syntax or identify all earlier referents.

**U12 inspection:** `img/r1102_u12_colour.png` enlarges I5657 rectangle
`(3670,1580,4320,1740)` threefold. Its contrast companion subtracts the
blue channel from a Gaussian-radius-18 background and amplifies darkness
fourfold. The group after `maesta` tentatively segments as
`a / t / e / n / t / a / ss / e`, suggesting `atentasse` (M).
This is a diagnostic hypothesis, not accepted plaintext: the identification
of the upright/loop signs and the group's word boundary need an independent
comparison. Additional faint signs remain between it and the fold, before
the next line's `monstra`. U12 is therefore not replaced or treated as a
single recovered word. No interpretation of the king's intention follows
from this tentative sequence.

A direct comparison with R1101 `ss_control_facesse.png` and
`ss_control_imparasse.png` finds the proposed terminal ss/e pair compatible
with both controls: the upright has a small foot loop and the following
stroke is low and angular. This is supporting evidence for only that pair,
not independent confirmation of `atentasse` as a word. The earlier signs
and fold-adjacent continuation are still the limiting evidence. Repeating
the same ss/e comparison is unlikely to resolve U12; a complete parallel
occurrence or better evidence for those other signs is required before
promoting the full reading.

At the following line break, `img/r1102_bisogno_right.png` (source
`3150,1570,4320,1790`) and `img/r1102_principio_left.png` (source
`2300,1670,3250,1790`) support testing `in questo principio`. The fold-adjacent
middle letters are not secure, so U13/U14 remain unexpanded. The candidate
is M and must not be used as a verified continuous quotation.

## E. Page 4, final cipher line

Source: Vestigia 1286 photograph `(111).JPG`, context rectangle
`(1370,810,2960,1030)`; `img/r1102_p4_context.png` and `img/p4_wide.png`.

```text
E01  se bene non la mandato a questo [U11]
```

The opening six signs support `se bene` (C), resolving former U10: s, the
flat-topped e, b, another e, round n, and the low angular e form. Source
rectangle `(1390,900,1720,975)` is enlarged in `img/p4_open_word.png`.
The last word has been tested as `effecto` (M/contextual proposal), but its
ff sign now has a known-plaintext control, but the following e is not securely
separated from its cross-stroke; U11 remains. See `ff_control.md`.
The enlarged last-word crop is `img/p4_end_word.png`, source rectangle
`(2620,900,2920,1020)`. The ff value comes from R1101, not this proposal.

Word division, including `la` (possibly editorial `l'a`), remains provisional. Faint ordinary annotations
immediately above some cipher words appear to gloss the line, including
approximately `mandato` and `a questo`. Their complete wording and extent are
unverified. No separate complete clear copy of R1102 has been located.

**Catalogue qualification:** `source_cache_audit.md` records Vestigia's legacy
note reporting decipherments on pasted and attached sheets. Three previously
uncached images were retrieved and inspected, but no separate decipherment
sheet was identified in them. The existence reported by the catalogue must
be distinguished from plaintext actually recovered and collated here.

## What this edition establishes and leaves open

The seven-line Venetian offer, its immediate continuation, further page-3
spans, and page-4 line are now kept distinct in one source-referenced record.
The stable U labels identify places to revisit; **U labels do not count
unread words or unread cipher groups**. There is still no
complete symbol inventory from which a solved percentage can be calculated.
The next transcription work must retain doubtful signs and disagreements
with the key, rather than turning word-level proposals into accepted glyph
values through repetition.

**Cross-passage resolution:** `repeated_k.md` identifies the same six-sign
sequence K in A03/U01 and D01/U07 and verifies its Hungarian-king referent
against R1101 I5655 and clear witness 7a. `[Re di Hungaria]` is an editorial
expansion (C for referent), not a recovered alphabetic spelling or proof of
the exact royal style intended. U01/U07's shared group is now resolved at
that semantic level; `profile.json` records the preceding research stages.
The later monetary passage therefore proposes giving the sum to this king;
the payer and complete proposal syntax remain to be established.

## 21 September re-reading of section D (native crops of I5657, 1.5-3x)

Crops of rectangles `(2260-4330, 1300-1990)` in four bands, read sign by sign against `key_working.md`:

- **D02/U08:** `che seri[a]`. The sequence c/h/e, s/e/r/i ends at the fold. The following line opens `questa suma che li
  domanda`, so the clause reads `sino a sei o septe anni, che seri[a] questa suma che li domanda` (M: final a hidden).
- **D04/U09:** after `liga considerata la`: i/n/d/u/b/i/t/a/t/a (the b is the open angle `>`, not o), then
  **`victoria`** v/i/c/t/o/r/i/a (C, every sign in the key), then `che sua m[aesta]` at the fold. `indubitata` is M because
  of a suspension stroke over its end. Proposed: `considerata la indubitata victoria che sua m[aesta] ...`.
- **Next line:** `s?a` + p/r/o/m/e/?/K-form/e + clear `est lo modo che mai fo la migliore opportunita`. A form of
  `promettere` fits but is not accepted (the K-shaped sign is unassigned).
- **D05:** `atentasse` (U12) as before, M.
- **D05-D06/U13-U14:** `monstra desiderare et haver piu bisogno in qu/esto principio.` (C): h/a/v/e/r, p/i/u,
  b/i/s/o/g/n/o, i/n, q/u; the next line has p/r/i/n/c/i/p/i/o. This promotes the earlier M `in questo principio`.
- **D06/U15:** `ma` + a word in ordinary script (`rima`/`fima`?) + cipher p/i/a/c/e/d/e (Δ with stem = p). Unresolved.
  `alla liga` follows, as already read.

What is still open is limited by the image, not by the key. Stains and the binding fold cover U06, U11, U15-U19, and
R1103's block is faded. No sign value is in doubt except the K-shaped form and U20's cross mark.

### Blue-channel enhancement of the stained right edge (21 Sep)

Background-subtracted crops (Gaussian 18, x4) of `(3250,1780,4330,1990)` and `(2250,1860,3300,1990)`:

- **D07/U17 -> D08/U18:** `et se` + v/o/l/e/n/a (the l is the double-stem form) + s/p/e/n at the fold, followed on the next line
  by d/i/n/a/r/i + `a questo tempo`. Proposed: **`et se vol[e]no spen[dere] dinari a questo tempo`**. `dinari` and
  `a questo tempo` are C. `volen[o]` and `spen[dere]` are M, partly under the fold.
- **D08/U19:** after `et fare la bona`, the sign before the final a is the angular 7 (s), so the word is s/p/e/s/a,
  **`spesa`** (C after enhancement; it was an unaccepted proposal before).

The passage now runs: "...non e da perder tempo, et se vol[e]no spen[dere] dinari a questo tempo et fare la bona
spesa ...". It urges the League to spend now. U15/U16 (`ma [clear word] piacede(?) alla liga`) and U06, U11 remain
open after the same enhancement.
