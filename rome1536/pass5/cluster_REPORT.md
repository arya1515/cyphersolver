# Mâcon ciphers (fr. 3053, R4233-R4248): pass 4, shape clustering and LM lattice decoding

## Summary, stated plainly
- **Shape clustering worked only as a visual check. It did not produce a linked dataset.** `seg.py` binarises the page
  (Sauvola), takes connected components and keeps the tall ones: 1,262 instances from 14 pages (R4234 P8/9/11/12/16/17/19,
  R4235 P2/3/8, R4239 P3/4/6/7). `tall/` holds the instance bitmaps. HOG plus bitmap features, PCA 40 and Ward agglomerative
  clustering (k=24) give the contact sheets `sheetA.png` and `sheetB.png`. The sheets separate at least FIVE shapes that the
  readers wrote as one alias, `ǂ`:
  (1) long f with a hooked top and one bar (k14): the key's O, `f`;
  (2) £, a pound sign with a looped foot (k18): the key's U;
  (3) a straight stroke with two short bars, ≠ (in k2/k17): the key's P;
  (4) q with a crossbar on the descender (k21/k11): the key's M;
  (5) a stem with a looped p-top (k22): probably the key's F.
  The clusters are not pure: k2, k17 and k21 mix ≠, q, 7 and 4. I did NOT link instances to transcription tokens, so there is
  **no image-based cluster × letter contingency table**. Doing that needs line-by-line alignment of components to tokens, and
  the readers' crops and line numbers are not consistent enough to do it quickly. What the images do show is that the ǂ
  ambiguity comes from the transcription, not from the cipher. The key's distinct signs O, U, P, M and F are all present and
  can be told apart by eye. The real fix is to re-transcribe the `ǂ` tokens by shape (next step, below).
- **The fallback was done: LM lattice decoding over the readers' alias transcriptions.**
  1. `extract.py` pulls 499 cipher lines and their readings from origin/main.
  2. `align.py` runs an EM forced alignment of tokens to the readings. It gives per-file emission tables P(letters|alias),
     with pooled backoff.
  3. `decode.py` runs a beam search (width 96) under fr-1600-letters (5-gram, no spaces, 'early' norm).
     - Emission weight 2. Letter bonus 1.5 per letter, which stops the LM from choosing nulls.
     - Barred-family aliases are widened to {o,u,p,f,m,qu,a,h}.
     - Codes are fixed: {20}=lempereur, {30}=pape, {40}=roy.

## Contingency: alias × letter (EM alignment to the readers' readings, all files pooled)
| alias | n | letters (aligned to readers' readings) |
|---|---|---|
| `ǂ` | 731 | u 330, o 232, f 60, ∅ 45, p 30, qu 6, rr 5, c 4 |
| `£` | 74 | qu 47, u 26, i 1 |
| `F` | 65 | f 30, o 18, p 7, u 6, ∅ 4 |
| `f` | 70 | o 43, u 27 |
| `∩` | 205 | p 187, f 15, u 2, a 1 |
| `P` | 97 | p 92, f 5 |
| `q` | 246 | m 225, ∅ 17, q 3, e 1 |
| `M` | 45 | m 38, u 3, e 1, f 1, mm 1, n 1 |
| `U` | 121 | qu 60, u 47, o 6, ∅ 4, m 1, a 1, e 1, p 1 |
| `V` | 108 | u 76, qu 24, e 3, x 1, i 1, s 1, a 1, m 1 |
| `ꭓ` | 32 | u 26, ∅ 2, t 2, s 1, qu 1 |
| `N` | 63 | u 55, n 3, ∅ 3, q 2 |
| `ƀ` | 83 | e 55, h 9, ∅ 5, ss 5, z 4, o 2, d 1, s 1 |
| `✱` | 7 | ∅ 3, u 2, r 1, a 1 |
| `⋈` | 17 | ∅ 8, u 7, l 1, p 1 |
| `ʍ` | 35 | u 35 |
| `∫` | 20 | ∅ 11, p 7, r 2 |
| `Δ` | 851 | i 668, q 101, ∅ 61, qu 11, s 3, o 2, f 2, e 1 |
| `4` | 715 | c 544, r 122, ∅ 17, t 9, ch 7, f 4, e 3, u 2 |
| `7` | 835 | n 734, b 65, ∅ 20, r 6, t 2, u 2, d 1, e 1 |
| `X` | 382 | l 346, n 26, ∅ 4, x 4, a 1, e 1 |
| `5` | 568 | d 492, g 46, s 16, ∅ 12, t 1, l 1 |
| `S` | 209 | d 143, e 27, g 15, ss 14, h 5, a 2, s 2, r 1 |

Reading the table: the readers' `ǂ` covers U 330, O 232, F 60, P 30. That is the O/U/P/F/M shape split seen on the
contact sheets. `Δ` is I, but it is Q (101 times) before `£` in QUE: the readers conflated the key's ᴧa (Q) with the Δ
triangle. `7` is N, and B 65 times. `4` is C, and R 122 times. `5` is D, and G 46 times (the hooked 5). `X` is L, and N 26 times.

## Calibration (held out, measured)
The ground-truth lines were removed from training: R4234 P16 lines checked against the clear copy on P15, the P19-20 lines
with the margin decipherment, R4235 P8 passage D against the clear copy on P6, and the whole of R4240 against its
contemporary decipherment. The measure is the character error rate against the readings of those lines.

| subset | chars | argmax per alias (no LM) | lattice + LM |
|---|---|---|---|
| unicode-transcribed lines (R4234 P16/P19-20, R4235 P8D) | 791 | 14.4% | **9.2%** |
| R4240 (ASCII transcription, noisy) | 856 | 24.9% | 23.8% |

The LM fixes the ǂ/£/Δ choices well: LES NOUVELLES, ROYAUME, LEVEES, POUR LUY, FAIRE, FLORENCE, LIBERTE, DEVOTION all
come out right. It cannot fix a transcription that has dropped or misread signs. R4240's alias line lacks most R signs,
and the lattice there is no better than argmax.

## Per-record coverage (proxy, INFLATED, not a % of letters read)
The proxy is the share of non-null signs whose letters fall inside dictionary words: corpus words of 3 or more letters with
frequency 20 or more, plus a closed list of short function words.
- Before: the readers' readings, aligned to the signs.
- After: the lattice output.
| record | letter signs | before | after |
|---|---|---|---|
| R4233 | 1435 | 76.7% | 87.9% |
| R4234 | 5280 | 81.6% | 90.5% |
| R4235 | 1613 | 91.4% | 91.9% |
| R4238 | 753 | 83.3% | 90.0% |
| R4239 | 4466 | 77.7% | 84.8% |
| R4240 | 856 | 86.0% | 89.7% |
| R4247 | 2558 | 86.9% | 92.8% |

**Do not quote the 'after' column as % read.** On unread lines the lattice makes plausible French fragments ("la deu ren ant
les mes"). Those fragments score as covered even though they are not readings. The honest numbers are the held-out CERs
above. By that measure the method would take well-transcribed lines from about 86% to about 91% of letters correct. It
gives nothing on badly transcribed ones. The 95% goal is not reached.

## Lines where the lattice adds something (checked against context, not yet against the image)
- R4234 P16 L15: "dessus et non au[?] a ce qu'il vous plaise ne pa..." (reader: ~50%).
- R4234 P16 L16: "... autre car autrement comme je vous ..." (reader: not aligned). The clear copy on P15 has "comme je vous
  ay dernierement escript", which supports this.
- R4239b P16 l.4-6: "au roy ce que me semble[roit]", "... et me mandes ...", "... sa ... la dicte audience". These agree
  with the reader's partial readings but add nothing secure.
- R4239b P16 l.2-3 and P26 l.5 stay unread (fragments only).

## Still open
R4239b P16 l.1-3 and P26 l.1-5; R4235 P8 passage D l.5 onward; R4234 P16 L6 (middle run) and L16-17; the P19 C3/C4
block; R4247 letter 2; R4233 passages 3-5 beyond the glosses; all of R4240's lines, which need re-transcription (missing R
signs).

## Next step that would reach ~95%
Re-transcribe every `ǂ` token by its shape class: long-f → O, £ → U, ≠ → P, crossbar-q → M, looped-p → F. This can be
done by hand from the line crops using the contact sheets as the reference. Once the ǂ tokens carry the key's value, the
same lattice runs with singleton sets. On the unicode lines the remaining error is mostly ǂ/£/Δ ambiguity plus a few
dropped signs.

## Files (all in rome1536/work_cluster/)
seg.py, sheet.py, extract.py, align.py, decode.py, calib.py, run_all.py; lines.json, emit_counts.json, alignments.json,
coverage.json, lex.json; tall/ (instance bitmaps), tall_rows.json, tall_feats.npy, tall_lab24.npy, sheetA.png, sheetB.png,
_sheet_p16.png; R4233_pass4.md, R4234_pass4.md, R4235_pass4.md, R4238_pass4.md, R4239_pass4.md, R4240_pass4.md,
R4247_pass4.md (per line: signs, lattice best, word-divided with [residue], reader reading, coverage).
