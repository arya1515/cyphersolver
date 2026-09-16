# Cardinal de Joyeuse → Villars, admiral de France, Rome, 15 February 1594 (BnF 500 de Colbert 33, f. 539)

Session 2026-09-16. Gate check only: fetched, measured, not attacked. Short-list candidate 5 of 2026-09-16
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

## Measurement (the gate)

| | |
|---|---|
| Cipher lines | 11 (ten full, one of about nine tokens) |
| Tokens | about 260 (line counts 24-27; each number and each Roman numeral counted once) |
| Numeric tokens | about 18: 88, 196, 223, 184, 152 (×3), 89 (×2), 86, 209, 30, 3015 or 30 15, 174, 179, 199?, 54, 128, 2 |
| Roman numerals | xiiij, xvj |
| Symbol repertoire | graphic signs (◇, ⊥, ⊤, ω, ∞, α, β, ρ, θ, ϑ, Γ, ⊐, ⅃, ⊞, ⊠, Λ, x, y, F, H, 4, 7, 3, ~, :, ) …) **plus the same bases carrying marks**: one dot, two dots, a cross, a double cross, a "#", a small bar or flag above or below |
| Distinct tokens (provisional, by eye) | well over 100 at 260 tokens; a labelled count needs the glyph-level transcription, not made |

The marked series is the structural fact. Unmarked base symbols with dotted, crossed and hashed variants are the signature of
a syllabary or nomenclature laid over an alphabet (cf. the Brienne-office ciphers in `bordeaux/`, where the diacritic
series run through the syllabary), and the code numbers are a nomenclature on top of that. Two-thirds of the tokens are
therefore not letters of a homophonic alphabet.

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

Not attacked. About 260 tokens over a marked-symbol system with more than 100 distinct tokens and a numeric nomenclature is
the regime in which the SP 53 (507 and 644 tokens, 132 and 102 symbols) and Bordeaux (810 tokens, 156 symbols) attacks
failed their matched controls this week; at less than half those lengths a ciphertext-only run here would produce a
fluent false solution and nothing else. No key is online. **Below threshold; closed at the gate.**

What would reopen it: the key, or a second Joyeuse letter in the same cipher (Joyeuse's 1594 despatches from Rome are in
BnF fr. 3623-3625 and 500 Colbert 33 passim; not searched), or Viète's own decipherment if it survives elsewhere in the
volume (the volume is "despatches deciphered by Viète" — f. 539 is an original he apparently did not break).

## Files

- `img/c544_f539.jpg`, `img/block.jpg`, `lines/` — git-ignored; regenerate with the IIIF URL above
  (`/f544/full/full/0/native.jpg`) and the crop box in `../gallica_siblings/src/` history.
- Tomokiyo's images and Lasry's key images: `../gallica_siblings/src/`.

Checked: canvas identification, clear text, token and line counts, presence of marked series and numbers, shape comparison
with the f. 555 and f. 530 keys. Not checked: a labelled glyph transcription (not made), whether other Joyeuse letters of
1594 in the same cipher exist on Gallica. User must verify: the token count (±10) before quoting it.
