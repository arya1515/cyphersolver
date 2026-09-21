# R1102: repeated group K in two unresolved regions

Status: referent verified C by contemporary clear witness; exact expansion
and internal encoding remain unresolved. K is an editorial label.

Direct colour comparison identifies the same ordered six-sign sequence in
two places previously treated as separate unread material:

| Unit | Immediate context | Source rectangle, DECODE I5657 |
|---|---|---|
| A03 / U01 | `fosse a K` | `(1685,2475,1960,2550)` |
| D01 / U07 | `ad dare a questo K cento milia` | `(3565,1300,3840,1375)` |

The unenhanced fourfold enlargements are paired in
`img/r1102_repeated_k_comparison.png`. The sequence consists approximately
of a stemmed triangle, a two-horned low form, a descending angular form,
a right-facing curved form, a looped/tail form, and a forked upright.
The second occurrence is faded but preserves the same order and distinctive
forms. This is a graphic recurrence, not an assertion that every stroke has
been segmented into its final cipher unit.

## Consequence for reading

The older proposal that A03 U01 might be `pregare` should not be preferred
from that sentence alone: the same sequence occurs after `questo` as the
object of a proposed payment. Both occurrences must be explained together.

**Initial hypothesis M, superseded by the control below:** K denotes the Hungarian king, or a title referring to him.
This fits both the ambassador being sent to someone and money being given
to someone. It is not yet verified by a clear-witness match, and no exact
Italian expansion is accepted. A nomenclator entry is possible but not
proved; the six forms must not be assigned new alphabetic values solely
to force this interpretation.

The next discriminating check is an occurrence of K in R1101 or R1106
aligned to an independently read royal title. Until then the working edition
links U01 and U07 with the shared K label and retains them as unresolved.
This group is graphically distinct from the established Venetian-government
group X and from R1101's still-unresolved W01.

## Retrieval test

Visual inspection of the existing R1106 page-2 and page-3 crops did not
establish a clear-witness occurrence of K. A look at R1104's opening paragraph
also did not establish one; these are limited inspections, not absence claims.

`find_k_candidates.py` tests single-scale normalized cross correlation on
R1102, using local darkness at quarter resolution. The A03 template retrieves
the known D01 occurrence at **rank 19 of 30**, score **0.3924**, box
`(3552,1292,3828,1372)`. Its own occurrence scores 1.0. The coordinate result
agrees with the manually identified group. Results are reproducible in
`k_template_test.json`; the manually inspected candidate sheet is
`img/k_template_test_contact.jpg`.

Many higher-ranked detections are page edges, prose, or different cipher
words. No additional K occurrence was accepted from the sheet. This is a
limited positive retrieval control with substantial false positives, not
an automatic sign recognizer. Before extending it, restrict searches to
observed writing regions and continue manual comparison of candidates.
Failure to retrieve a group cannot establish its absence.

## Clear-witness verification in R1101

`search_k_r1101.py` restricts retrieval to observed writing regions and tests
0.8, 1.0 and 1.2 template scales. Candidate 2 in DECODE I5655 is a graphic
match, original box **`(1804,1352,2080,1432)`**, score 0.4786. The score is
only a retrieval aid; the signs and surrounding passage were checked visually.
Its context is `img/k_context_I5655_2.png`.

Original context reads approximately `lo che ha ditto poi K ad vno ...`,
followed by mention of the queen and Francesco. Clear copy 7a, page 3,
reads across consecutive lines `lo che ha detto poi / la M.ta del S. Re
di Hungaria ad uno ... ala Regina et ... Francesco / Fontana ...`.
Abbreviation expansions are editorial and some intervening ordinary words
remain unedited. The shared preceding clause and following recipients anchor
the alignment independently of the proposed meaning of K.

The witness is Vestigia 1283 photograph `(102)`, right page, reproduced in
`img/k_clear7a_p3_middle.png`, source rectangle `(2300,880,4150,2100)`.
This establishes **the Hungarian king as K's referent (C)**. It does not
establish which abbreviated or full royal style was intended as K's exact
lexical expansion. The working edition uses `[Re di Hungaria]` editorially.

Two further graphic candidates in I5654, boxes `(3496,732,3716,796)` and
`(500,1756,720,1820)`, are retained for additional collation; they are not
needed to claim the single verified I5655/7a correspondence. The full search
results are `k_r1101_candidates.json` with two candidate contact sheets.

### Second checked correspondence

I5654 candidate 1, `(3496,732,3716,796)`, has now been collated as well.
The original context `credo io che K la desi...` matches 7a page 2:
`pace et credo io che la M.ta del S. Re d'Hungaria la desidera ...`.
The succeeding discussion of the war's damage to the kingdom confirms
the paragraph position. This supplies a second direct royal-title alignment,
independent of the I5655 passage above, within the same original/clear pair.

Original view: `img/k_context_I5654_1.png`. Clear view:
`img/k_clear7a_p2_context.png`, from photograph `(102)` rectangle
`(0,1030,2200,1890)`, reduced to 80% for inspection. Candidate 12 in I5654
remains uncollated. Exact lexical expansion and K's internal structure are
still unspecified; two semantic matches do not manufacture an alphabetic key.
