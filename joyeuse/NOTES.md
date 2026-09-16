# Cardinal de Joyeuse → Villars, admiral de France, Rome, 15 February 1594 (BnF 500 de Colbert 33, f. 539)

Session 2026-09-16. Fetched, transcribed at glyph level, attacked on the letter layer against three matched controls; **not solved**. Short-list candidate 5 of 2026-09-16
("Gallica figure-cipher siblings"), together with `cocquet/` and Blancmesnil (see below).

## Source

- Tomokiyo, *Ciphertexts Left Undeciphered by François Viète (1593-1594)* (cryptiana `viete.htm`): "(f.539) Cardinal de
  Joyeuse to Villars, admiral de France, Rome, 15 February 1594 (in unidentified symbol cipher, undeciphered). The cipher
  seems different from the alphabet of f.530." His page image `500Colbert33_f539.png` (680 × 622) is in
  `../gallica_siblings/src/`.
- Gallica: 500 de Colbert 33 = `ark:/12148/btv1b10033958p`, 616 canvases, all labelled NP. Canvas 546 shows f. 541, so
  **f. 539 is canvas 544** (right page; verso blank on canvas 545). Full-resolution IIIF image 7580 × 5347 saved as
  `img/c544_f539.jpg` (git-ignored), cipher block `img/block.jpg`, line strips `lines/L01a.png` … `L11b.png`.
- The clear frame: "Monsieur, j'ay receu la lettre que vous m'avez fait ceste faveur de m'escrire, et j'ay considéré tout ce
  que vous m'y mandez en chiffre. Ce qui m'a confirmé en l'opinion que j'avois desjà de moy mesmes de la plus part de ce que
  vous me mandez. Je vous baise les mains de ces advis, et vous asseure que je m'en serviray bien. Ce que je vous puis dire
  d'icy en substance n'est autre chose sinon que [CIPHER, 11 lines] Je vous baise les mains de l'asseurance que vous me
  donnez de vouloir que nous soyons bien joints ensemble en toutes nos resolutions … Rome, ce xv fevrier 1594."
  Villars (André de Brancas) was the League governor of Rouen; his treaty with Henry IV followed on 27 March 1594.

## Transcription and measurement

`ct_f539.txt`: glyph-level transcription, 11 lines, one reader, single pass; base-shape names with the mark as a suffix
(`.` one dot, `:` two dots, `+` cross, `#` hash, `^` hat, `_` bar or flag). Provisional: several base identities are
judgement calls (the tall compound at line 2, `Ez#pi`; `3015` may be `30 15`; a few `dia`/`dia'`/`dia_` splits).

| | |
|---|---|
| Tokens | **358** (the first estimate of 260 undercounted the dense lines) |
| Distinct | 147, hapax 71 |
| Numbers | 29 tokens, 18 values: 2, 3, 4, 6, 30, 54, 86, 88, 89, 128, 152 (x3), 174, 184, 196, 199, 209, 223, 3015 |
| Roman numerals | xiiij, xvj (and `x`, `xi` as glyphs) |
| **Unmarked** tokens | 234 over 81 symbols, hapax 32; top: ofo 11, oo 10, Lam 9, til 8, par 8, dia 7, w 7 |
| **Marked** tokens | 95 over 48 symbols, hapax 26; marks: + 30, : 18, _ 14, # 13, . 8, ^ 3 |

Reading of the structure: an unmarked homophonic alphabet of about 80 signs (2-4 homophones per letter, 22-letter French
alphabet), a marked series of about 50 signs used once or twice each (a syllable table or small nomenclature), and a
numeric nomenclature for names. This is the design Segur's correspondent describes in 500 Colbert 401 f. 143 ("lettres,
syllabes, doubles, nulles") realised in graphic signs. The five-mark test that unlocked Segur (figure blocks mod 5 =
syllable rows) has no analogue here: marks are 27 % of tokens, not a vowel index over every consonant, and graphic signs
carry no ordering to exploit. `par` (8), `til` (8) and `dd` (4) may be nulls or separators; untested.

## Attack: letter layer with syllables as wildcards

`solve.py`: homophonic simulated annealing on the 234 unmarked tokens, marked tokens and numbers treated as context
breaks (word-boundary padding), scored with the spaced 16th-century French 5-gram model from `../ducroc/fr5.npy`
(9.4 M characters of Catherine de Medicis, Teulet and Labanoff). 120 000 steps, swap and reassign moves, half the seeds
frequency-initialised.

`control.py`: matched controls: 234 letters over 72-76 homophones distributed by French letter frequency, 91-95
syllable tokens from a 48-entry table, 2-5 number tokens, enciphering a run of the same corpus (a different file per
seed). Same solver, same settings, accuracy against the true key:

| control | letter tokens | accuracy over 4 seeds |
|---|---|---|
| 1 | 234 | 0.02, 0.09, **0.18**, 0.01 |
| 2 | 236 | 0.13, 0.13, 0.08, 0.13 |
| 3 | 234 | 0.06, 0.09, 0.09, 0.11 |

Best control recovery 18 %; chance for a 22-letter alphabet is about 5 %. The letter layer of this design is not
recoverable ciphertext-only at 234 tokens with 40 % of the text hidden in syllables. Run on the target for the record
(`run_target.log`, six seeds): six mutually unrelated fluent fragments ("son a en uerre", "de tami ci r ... monsier",
"la nico sl g ... uous"), no two seeds agreeing on any span: the false-solution signature, exactly what the controls
predict. **Not solved; closed against controls.**

## Key-application test

- **Lasry's key for f. 555** (Senecey to the Archbishop of Lyon, Rome, February 1594; HistoCrypt 2022; images
  `500Colbert33_f555Solution*.png`) is the natural sibling: same volume, same city, same fortnight, same League embassy.
  Its 79 symbols are unmarked graphic signs with five word codes and no numbers. f. 539 shares perhaps a dozen base shapes
  (ω, ⊥, ∞, ⊞, ⊠, α, ρ, β, 4, Δ, ⊐) — the common repertoire of the period — but has no counterpart to the marked series or to
  the numbers, and the f. 555 letter has no marked symbols at all. The two ciphers are not the same key.
  *Not run as a decode: without a labelled transcription there is nothing to feed it, and the structural mismatch already
  decides it.*
- Tomokiyo's partial alphabet at f. 530 (Pelissier ↔ Joyeuse, same month): he states it does not fit, and its shapes
  (n, o, ρ, φ, ʒ, ¬, ⊤, ≠ …) are again unmarked.
- Nevers-collection and Viète-volume keys on cryptiana: none is a marked-symbol cipher of this shape.

## Verdict

Not solved. 358 tokens of a three-layer design (80-sign homophonic alphabet, 50-sign marked syllabary, numeric
nomenclature): the letter layer alone is 234 tokens and fails its matched controls at 2-18 %, and no key is online.
The same regime as SP 53 and Bordeaux this week, at a third of their length.

What would reopen it: the key, or a second Joyeuse letter in the same cipher (Joyeuse's 1594 despatches from Rome are in
BnF fr. 3623-3625 and 500 Colbert 33 passim; not searched), or Viète's own decipherment if it survives elsewhere in the
volume (the volume is "despatches deciphered by Viète" — f. 539 is an original he apparently did not break).

## Files

- `ct_f539.txt`: the transcription. `solve.py`, `control.py`: solver and control generator; `control_N.txt`,
  `control_N_key.txt`, `control_N_plain.txt`, `run_control*.log`, `run_target.log`: the runs above.
- `img/c544_f539.jpg`, `img/block.jpg`, `lines/`: git-ignored; regenerate with the IIIF URL above
  (`/f544/full/full/0/native.jpg`); the crop box is (575, 295, 990, 495) in 1100-px-wide view coordinates.
- Tomokiyo's images and Lasry's key images: `../gallica_siblings/src/`.

Checked: canvas identification, clear text, glyph transcription (one pass), layer counts, shape comparison with the f. 555
and f. 530 keys, three matched controls, six target seeds. Not checked: the transcription against a second reader; whether
`par`/`til`/`dd` are nulls; whether other Joyeuse letters of 1594 in the same cipher exist on Gallica. User must verify:
the transcription before any later work builds on it.
