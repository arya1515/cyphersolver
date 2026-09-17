# Baudouin-Desportes to Aldobrandini and to Frachetta, Paris 22 July 1593 (catalogue no. 20)

Session of 17 September 2026. Catalogue task: the "papal-side" letters of the week of Henri IV's abjuration in BnF
fr. 3984 (nos. 6, 8, 88 = f. 186, 90 = f. 189) and fr. 3985 no. 7, scored class A because same-day siblings are
deciphered in the same volume (f. 184, f. 177). Outcome: **not read**. The key is known (Tomokiyo's League
polyphonic cipher), the deciphered sibling is aligned glyph by glyph, but the two target letters are c. 5,000
hand-drawn glyphs whose classes a classifier trained on the sibling reads at 75-79 %, and the polyphonic decoder
needs better than 90 %. The item is closed as *not solvable with the present tools*; what would reopen it is at the end.

## What the leaves are (all from `btv1b9060633d`, microfilm, canvas ≈ 2 × folio − 26 in this stretch)

| folio | canvas | content | state |
|---|---|---|---|
| f. 175 | c. 326 | "22 de Juillet 1593 · Memoire", clear French, the same peculiar hand as ff. 186/188 | clear |
| f. 176-176v | c. 327-328 | Baudouin-Desportes → Clement VIII, 22 July, two pages wholly in cipher (45 + 45 lines) | deciphered on f. 177 |
| f. 177 | c. 329 | the office's decipherment of f. 176 ("Tressainct pere / Ne l'avenue aux yeux et l'ame plaine de desespoir …"), one dense page, secretary hand with abbreviations | clear |
| f. 184-185 | c. 343-345 | decipherment of f. 188 (Baudouin-Desportes → bishop of Lisieux), endorsed "Ce 26 Juillet" | clear (prior session transcribed it: `f185_plain.txt`) |
| f. 186-186v | c. 347-348 | no. 88, → Pietro Aldobrandini, "22 de Juillet 1593 · Illustrissimo Monseigneur, Si je nay escrit a Sa Sainteté et a Vre Seigneurie Illme aussi souvent que le devoir me le commande deux choses m'y ont empesché …": clear opening, then c. 25 lines of cipher on the recto with clear phrases between, 33 lines of cipher on the verso, clear close | **cipher, unread** |
| f. 188-188v | c. 351-352 | original of f. 184: mostly clear (the odd chancery hand that the catalogue took for cipher), cipher from line 2 of the verso to the end (20 lines) | ground truth |
| f. 189 | c. 353 | no. 90, → Girolamo Frachetta, one page, 33 lines wholly in cipher, dated "… uillet 1593" | **cipher, unread** |
| f. 274 | c. 508-514 | Lisieux → Desportes, Rome July 1593, same cipher, interlined decipherment (Roman hand) | deciphered |

fr. 3985 no. 7 (Mauclerc → Creil, `btv1b90606498` c. 6-13) was fetched by the previous session but not examined
here; the catalogue's "no. 4 deciphered" sibling claim is unverified.

Tomokiyo, *A Polyphonic Substitution Cipher of the Catholic League (1592-1593)* (cryptiana `mayenne.htm`), already
lists every one of these folios, gives the reconstructed key (`tmp/mayenne.png`, 654 × 255 px) and says of f. 186
"enciphered passages are undeciphered" and of f. 189 "undeciphered". So the task was never key recovery but
transcription of two pages in a known polyphonic cipher.

## The cipher

Eleven glyphs each stand for two letters (a/n, b/o, c/p, d/q, e/r, f/s, g/t, h/u, i/x, l/y, m/z), plus signs for
*que*, *qui*, *pour* and at least one code sign (the decipherer leaves "S" for the Infanta and "#"-type names). In
Desportes' hand, as fixed from f. 188v against f. 185 (`gold_f188v.json`, `tmp/refsheet.png`):

- a/n: "4" with a z-shaped tail at the foot (a second form with an extra crossbar)
- b/o: ring – stem with descender – ring ("oꝑo")
- c/p: "4" with a small loop at the foot of the stem
- d/q: "4" with a double crossbar and hooks
- e/r: a ring at the head of a descending stem, often with a second ring at the left ("ꝋ|")
- f/s: a long bar with a triangle hanging from it ("▽̅")
- g/t: a small v-shape with a bar to the right ("ᴜ‾")
- h/u: a double ring with a bar through it ("ϴϴ")
- i/x: a small "ʒ"
- l/y: a bracket ("Ꞁ")
- m/z: a tall stroke with a hook ("ʃꝫ")
- que: "y"; qui: "4" with a bar across the top; pour: "2"

The *pour* sign is used inside words ("pou-voyent", "pour-ront"); "e/r e/r e/r" runs are common ("reparer");
there are occasional null strokes (four between *pour* and *ront* on f. 188v l. 7) and the decipherer normalised
spellings (cipher "oposer", "eclesiastiques" vs f. 185 "opposer", "ecclesiasticques").

## What was built and measured (all in this directory)

1. **Pages.** Full-resolution IIIF canvases (4950 × 6660) in `img/`; line crops `lines/<page>_lNN.png` from the
   previous session's deskew and profile segmentation (`seglines.py`): f188v 23 lines, f189 33, f186v 33, f186r 41,
   f176 (verso only) 45.
2. **Glyph segmentation** `seg2.py`: column-gap segmentation with 6-px merging and valley splitting. On f. 188v
   l. 3, 57 boxes for 55 glyphs; across a page roughly 10 % of boxes are merged pairs and 10 % ring fragments or
   specks. Montages: `montage2.py`, `montage_lab.py`.
3. **Ground truth.** f. 188v ll. 3-22 (1,108 boxes) aligned to the f. 185 text with clear words removed
   (`f185_cipher_only.txt`) by a DP with match / null / letter-deletion / two-letter-merge moves (`boot2.py` kNN,
   `boot3.py` CNN), seeded by two hand-read lines (`gold_f188v.json`, 103 glyphs). Checked by eye on ll. 5-8: the
   alignment labels are right for c. 85-95 % of boxes (`tmp/v5-8.png`).
4. **Classifier.** `cnn.py` (3 conv layers, 40 × 32 crops, affine augmentation). Trained on the aligned labels of
   ll. 5-22 (597-718 boxes) and tested on the hand-read ll. 3-4: **top-1 0.73-0.79, top-2 0.83-0.85** for the CNN,
   0.71-0.74 for PCA+SVM/kNN (`exp.py`). Held out ll. 7-10 against alignment labels: 0.57-0.73. Confusions are
   e/r ↔ b/o (ring position), f/s ↔ g/t ↔ h/u (bar shapes), i/x and m/z ↔ a/n. Self-training with up to 4,666 confident
   pseudo-labels from the unread pages: top-1 0.786, top-2 0.825 over three rounds — no real gain.
5. **Decoders.** `decode_line.py` (hard class strings) and `soft_decode.py` (class probabilities × LM, with skip and
   merge moves). With a perfect class string the beam decoder reads 95-98 % of a French control (`poly_decode.py
   test`). The repo's `sp53/fr6.pkl` LM produced English words in the beams; `fr6_period.pkl` was trained here on the
   Henri IV *Lettres missives* (Xivrey, t. III-V) and the Bordeaux corpus with j→i, v→u (9.6 M letters).
6. **End-to-end control.** Soft decoding of the held-out f. 188v ll. 7-10 gives only fragments of the known text
   ("…tre parer encore…", "…nous en…", "…ces que uous luy auons…"), 30-40 % of letters in place. That is the
   pipeline's real power on this hand, and it is far short of what a polyphonic cipher needs.
7. **Crib search** `crib_search.py`: local alignment of each unread line's probability sequence against the f. 185
   text, with the word-shuffled text as control. Validation on held-out f. 188v ll. 7-10: real 18-54 vs shuffled
   10-19 (3 of 4 flagged). f. 189 (33 lines) and f. 186v (33 lines): **no line scores above its shuffled control**,
   so the Frachetta and Aldobrandini letters do not repeat the Lisieux letter verbatim in any 12+-letter stretch.
8. **Hand reading.** My own glyph-by-glyph reading at 4× (f. 188v l. 7, blind, then compared) is c. 70 % right:
   the same confusions as the classifier. Two hand-read lines of f. 189 (`tmp/m189_2.png`) decode to nothing.

## Why it is closed

The letters are readable in principle: the key is published, the hand is consistent, and the sibling gives 1,100
labelled glyphs. But every route to the class string tried here — hand reading, kNN, SVM, CNN, CNN with
self-training, soft LM decoding — stalls at three glyphs in four, and the polyphonic layer (each glyph = two
letters, with *e/r* covering a quarter of the text) turns a 25 % class error into unreadable output; the LM then
hallucinates plausible French (see the held-out control). No verbatim crib from the deciphered sibling exists.

## What would reopen it

- A larger labelled set in the same hand: f. 176 (90 cipher lines) against f. 177, which needs a paleographer's
  transcription of f. 177 (my reading of its first 14 lines is in this file's history; the hand is a fast
  secretary cursive with heavy abbreviation). With c. 3,500 more labels the CNN might pass 90 %.
- Or a human transcription of f. 189 and f. 186 glyph by glyph by someone trained on `tmp/refsheet.png`; the decoder
  and LM are ready (`decode_line.py`, `fr6_period.pkl`).
- Or the office's decipherments, if they exist elsewhere: Aldobrandini's and Frachetta's papers (Archivio Aldobrandini,
  Frascati; Frachetta's letters in the Vatican *Fondo Borghese*) could hold the clear copies.

## Files

`seg2.py` segmenter · `boot2.py`/`boot3.py` alignment bootstrap · `cnn.py` classifier · `predlab.py` predictions →
montage labels · `soft_decode.py`, `decode_line.py`, `eval_soft.py` decoders · `crib_search.py` · `exp.py`,
`selftrain.py` experiments · `gold_f188v.json` hand labels · `f185_plain.txt`, `f185_cipher_only.txt` sibling text ·
`fr6_period.pkl` period LM · `lines/*_g2.json` boxes · `tmp/` renders (refsheet, montages, f. 177 strips). The
previous session's cluster/EM scripts (`anneal_poly.py`, `em_*.py`, `cluster*.py`, `control_*`) failed their
controls and are kept for the record.
