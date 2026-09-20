# Alonso Sánchez (Venice) to Charles V, 1522 — RAH Salazar 9/23–9/26, DECODE R9593–R9657

Status: read in part (R9635 f. 20r and R9653 f. 299r; the cipher itself was already solved by Tomokiyo 2025)

Catalogue entry "Alonso Sánchez (Venice) to Charles V, 29 ciphertexts" (Tomokiyo list, scored B).
Worked 2026-09-20.

## Prior art: the cipher was already reconstructed

**S. Tomokiyo, "Correspondence in Cipher of Imperial Ambassadors Alonso Sanchez and Juan Manuel (1522)",
<https://cryptiana.web.fc2.com/code/AlonsoSanchez.htm>, first posted 6 September 2025, last modified
9 September 2025.** Saved here as `tomokiyo/AlonsoSanchez.htm` / `.txt` / `.png`.

He reconstructed Sánchez's 1522 cipher from the contemporary decipherment attached to DECODE R9605,
after spotting `vog veg` = "en el" near the end. The article gives:

- the substitution alphabet, as a hand-drawn table (`tomokiyo/AlonsoSanchez.png`): homophones for
  a–z plus a null group, with `q`-with-double-bar as the plural ending `-s`;
- a nomenclature of ~177 three-letter codes and 17 two-letter codes (transcribed here to
  `key_codes.tsv`);
- the deciphered **opening lines only** of R9593–R9632, plus two longer passages (R9621 entire,
  R9623 last paragraph).

So the cipher itself is solved, and solved before this project touched it. That is the contamination
answer for the profile: a full reading of the system existed publicly from 6 September 2025.

Tomokiyo also reconstructed the parallel cipher of **Juan Manuel** (imperial ambassador at Rome,
DECODE R9499–R9529); that key is in the same article and in `key_codes.tsv`'s sibling section of the
saved text, not used here.

## What the catalogue entry got wrong

The catalogue entry said "RAH, Signatura 9/24 (29 items)", 1522–23, ending at the treaty of July 1523.
From the DECODE records themselves (`decode/rec*.htm`, metadata table below):

- the run is **9/23, 9/24, 9/25 and 9/26**, not 9/24 alone;
- every record in R9603–R9657 carries a 1522 date. **Nothing here reaches 1523**, so the July 1523
  treaty is outside this group;
- a third of the tail is not Sánchez at all but **Lope Hurtado de Mendoza** (R9634, R9644–R9646,
  R9648–R9650, R9652, R9656);
- almost every record has DECODE's `Inline Cleartext: Yes` — a contemporary decipherment is bound with
  the ciphertext. These letters were never really unread; they are unedited.

## Structure of the nomenclature

Codes are consonant–vowel–consonant over C1 ∈ `z y x v t s r p n m l h g f d c b` (16, running
backwards through the alphabet as the plaintext runs forwards), V ∈ `a e i o u`, C3 ∈ `b c d f g h l m n`
(9) — 720 slots, of which Tomokiyo recovered ~177. Sorting by (C1, C3, V) puts the plaintext in
alphabetical order, so an unassigned code is bracketed by its neighbours: `zid zod zud | zef zif | zog
zug | zel | zem zom | zen zun` gives a(h)un, ahun, al, allende, algun, alla, alli, antes, aqui,
aquell, arma, assi. The alphabetisation is the scribe's own and is loose at the edges (allende before
algun, cosa before concorda), so the bracket is a range, not a point.

The 17 two-letter codes are the highest-frequency words: `xa` con, `ta` es, `re` hombre, `ne` muy,
`ho` que, `lu` por, `do` venecia, `ma` occorie, `ge` rompe, ...

This is the 1496 Ferdinand-and-Isabella type of Spanish cipher; the vocabulary is large for the date.

## The records

Fetched from DECODE 2026-09-20 (`decode/getrec.py`, `decode/fetch.py`, bordeaux cookie).
Images in `img/`, git-ignored; RAH material, permission needed to republish.

| DECODE | RAH Salazar | date (1522) | pp | DECODE status | decipherment bound in | author |
|---|---|---|---|---|---|---|
| R9603 | 9/24, f. 13-14 | May | 6 | Non-decrypted | Yes | Sánchez |
| R9604 | 9/24, f. 18-19 | May | 4 | Non-decrypted | Yes | Sánchez |
| R9605 | 9/24, f. 39-44 | May | 11 | Decrypted | No | Sánchez |
| R9606 | 9/24, f. 44-45 | May | 2 | Non-decrypted | No | Sánchez |
| R9607 | 9/24, f. 65-68 | May | 8 | Non-decrypted | Yes | Sánchez |
| R9608 | 9/24, f. 96-97 | — | 3 | Non-decrypted | No | Sánchez |
| R9609 | 9/24, f. 107-109 | May | 6 | Non-decrypted | Yes | Sánchez |
| R9610 | 9/24, f. 132-134 | Jun | 6 | Non-decrypted | Yes | Sánchez |
| R9611 | 9/24, f. 139 | Jun | 2 | Non-decrypted | Yes | Sánchez |
| R9612 | 9/24, f. 167-169 | Jun | 6 | Non-decrypted | Yes | Sánchez |
| R9613 | 9/24, f. 203-206 | Jun | 11 | Decrypted | Yes | Sánchez |
| R9614 | 9/24, f. 208-210 | Jun | 6 | Non-decrypted | Yes | Sánchez |
| R9615 | 9/24, f. 218-219 | Jun | 4 | Non-decrypted | Yes | Sánchez |
| R9616 | 9/24, f. 224-228 | — | 9 | Non-decrypted | Yes | Sánchez |
| R9617 | 9/24, f. 241-245 | Jun | 9 | Non-decrypted | Yes | Sánchez |
| R9618 | 9/24, f. 246 | Jun | 2 | Non-decrypted | Yes | Sánchez |
| R9619 | 9/25, f. 16-17 | 10 Jul | 3 | Non-decrypted | Yes | Sánchez |
| R9620 | 9/25, f. 24 | Jul | 2 | Non-decrypted | Yes | Sánchez |
| R9621 | 9/25, f. 56 | 19 Jul | 1 | Non-decrypted | Yes | Sánchez |
| R9622 | 9/25, f. 75 | 19 Jul | 1 | Non-decrypted | Yes | Sánchez |
| R9623 | 9/25, f. 133-134 | 19 Jul | 4 | Non-decrypted | Yes | Sánchez |
| R9624 | 9/25, f. 135-136 | — | 4 | Non-decrypted | No | Sánchez |
| R9625 | 9/25, f. 137-139 | Aug | 4 | Decrypted | Yes | Sánchez |
| R9626 | 9/25, f. 141-144 | — | 9 | Non-decrypted | Yes | Sánchez |
| R9627 | 9/25, f. 145-148 | — | 4 | Non-decrypted | No | Sánchez |
| R9628 | 9/25, f. 156-157 | — | 2 | Non-decrypted | Yes | Sánchez |
| R9629 | 9/25, f. 158-159 | Aug | 3 | Non-decrypted | Yes | Sánchez |
| R9630 | 9/25, f. 180 | Aug | 2 | Non-decrypted | Yes | Sánchez |
| R9631 | 9/25, f. 182-189 | Aug | 15 | Non-decrypted | Yes | Sánchez |
| R9632 | 9/25, f. 198-205 | Aug | 18 | Non-decrypted | Yes | Sánchez |
| R9633 | 9/26, f. 4-7 | — | 8 | Non-decrypted | Yes | Sánchez |
| R9634 | 9/26, f. 14-16 | Sep | 6 | Non-decrypted | Yes | **Lope Hurtado** |
| R9635 | 9/26, f. 20–22 | — | 5 | Non-decrypted | Yes | Sánchez |
| R9636 | 9/26, f. 68–71 | — | 7 | Non-decrypted | Yes | Sánchez |
| R9637 | 9/26, f. 76 | Oct | 1 | Non-decrypted | Yes | Sánchez? |
| R9638 | 9/26, f. 104–108 | 11 Oct | 8 | Decrypted | Yes | Sánchez |
| R9639 | 9/26, f. 111–115 | Oct | 10 | Non-decrypted | Yes | Sánchez |
| R9640 | 9/26, f. 139–141 | Oct | 6 | Non-decrypted | Yes | Sánchez? |
| R9641 | 9/26, f. 173–174 | Oct | 4 | Non-decrypted | Yes | Sánchez? |
| R9642 | 9/26, f. 184–188 | — | 8 | N/A | Yes | Sánchez? |
| R9643 | 9/26, f. 189–191 | Oct | 6 | Non-decrypted | Yes | Sánchez? |
| R9644 | 9/26, f. 237–243 | 1 Nov | 14 | Decrypted | Yes | **Lope Hurtado** |
| R9645 | 9/26, f. 243–244 | Nov | 4 | Non-decrypted | Yes | **Lope Hurtado** |
| R9646 | 9/26, f. 252 | — | 2 | Non-decrypted | Yes | **Lope Hurtado**? |
| R9647 | 9/26, f. 257–259 | — | 6 | Non-decrypted | Yes | Sánchez? |
| R9648 | 9/26, f. 260–265 | 9 Nov | 12 | Non-decrypted | Yes | **Lope Hurtado** |
| R9649 | 9/26, f. 266–268 | 9 Nov | 6 | Non-decrypted | Yes | **Lope Hurtado**? |
| R9650 | 9/26, f. 269–272 | — | 10 | Decrypted | Yes | **Lope Hurtado** |
| R9651 | 9/26, f. 276–279 | — | 8 | Non-decrypted | Yes | Sánchez? |
| R9652 | 9/26, f. 295–296 | Nov | 2 | Partially decrypted | Yes | **Lope Hurtado** |
| R9653 | 9/26, f. 299–300 | 20 Nov | 4 | Non-decrypted | Yes | Sánchez |
| R9654 | 9/26, f. 301–302 | 20 Nov | 4 | Non-decrypted | Yes | Sánchez |
| R9655 | 9/26, f. 303 | Nov | 2 | Non-decrypted | Yes | Sánchez |
| R9656 | 9/26, f. 334–335 | Nov | 4 | Non-decrypted | Yes | **Lope Hurtado** |
| R9657 | 9/26, f. 354–355 | — | 3 | Non-decrypted | No | Sánchez? |

Generated by `decode/meta.py` into `decode/metadata.md`. "Decipherment bound in" is DECODE's
`Inline Cleartext` flag. Nine of the 55 records name **Lope Hurtado de Mendoza** as author.

## Work in this session

- Prior-art search; Tomokiyo's article found and saved.
- DECODE metadata for R9603–R9657 pulled and tabulated; shelfmark, date and authorship errors in the
  catalogue entry corrected above.
- Nomenclature transcribed to `key_codes.tsv` and its ordering verified.
- Images fetched for the 9/26 tail (R9633–R9657), the part Tomokiyo's article does not cover.
- **The c-block numerals settled.** Tomokiyo has `cob` xviii, `cub` xix, `cad` xx … `cud` xxiv, `caf`
  xxv, and leaves the rest blank. The ordering fills the run: `cef` xxvi, `cif` xxvii, `cof` xxviii,
  `cuf` xxix, and below, `cab` xv, `ceb` xvi, `cib` xvii. `cef` and `cif` are then **confirmed in
  text** (see below); this also resolves the uncertain "[xxviii?]" in his reading of R9598 as `cof`.
  Added to `key_codes.tsv`, flagged as this project's.
- **R9653 read in part** (`read_r9653.md`), a record outside Tomokiyo's range. f. 299r is a mixed
  letter: six lines of cipher at the head, some thirty lines in clear, two lines of cipher at the
  foot. The clear middle is the news of the siege of Rhodes — five assaults to 10 October, mines and
  underwater mines, twenty thousand Turks dead by the Venetians' count and fifty thousand by a
  secretary of the Signoria's, the Sultan said to have withdrawn to the mainland, and a thousand
  infantry enough to save the island. (Rhodes capitulated a month later.) The foot cipher paragraph
  reads in part "**cartas de Francia de xxvi y xxvii del passado de …**". The head paragraph is
  defeated by ink bleed from the facing leaf at the resolution DECODE serves.

- **R9635 read in part** (`read_r9635.md`), 16 Sept 1522, Salazar 9/26 f. 20–22, also outside Tomokiyo's
  range. f. 20r is a full page of cipher in a clean hand with a *patchy* contemporary decipherment
  between the lines. Read: "das cartas de vuestra magestad", "los de esta republica", "del señor
  infante", "ducados allende de los otros xviii mil", "**mas de xv mil ducados**", "todos los … mil
  ducados luego de esto", with the glosses *obligados … fuessen restituydas sus bienes*. The subject is
  the sums owed by the Signoria under the capitulation and the restitution of goods seized from
  imperial vassals — the same business R9638 (11 Oct) carries entirely in clear.
- **`cab` = xv attested**, in "ped xig cab pol9 vud+s" = *mas de xv mil ducados*. That is a third
  predicted numeral confirmed in text (with `cef`, `cif`), and none of the seven is contradicted.
- Notation settled: `pol9` = `pol` (mi) + the letter sign for **l** = *mil* (the `l` sign reads as a `g`
  in this hand); `gɣ lal` = letters *r-e* + `lal` (publica) = *republica*; the opening nulls are padded
  with the meaningless clear words *como* / *quien*, which is what Tomokiyo's "como quierr" note under
  the nulls column means.
- `decode_tokens.py` resolves a token string against the key and brackets unknown codes by their
  alphabetical neighbours.

## The letter alphabet, and why the spelled runs are still open

Tomokiyo gives the substitution alphabet only as a hand-drawn table
(`tomokiyo/AlonsoSanchez.png`). Read off at high zoom it is about thirty signs over twenty-two
letters (a b c d e f g h i l m n o p q r s t u x y z), most letters having two or three homophones:

| a | b | c | d | e | f | g | h | i | l | m |
|---|---|---|---|---|---|---|---|---|---|---|
| n, ʒf | ᵹ | z, Ә | ∞, 3, ɸ | 4, ʒ | P | ∞(bold), L | x, m∞ | a₄ | 9 | β, ✗ |

| n | o | p | q | r | s | t | u | x | y | z |
|---|---|---|---|---|---|---|---|---|---|---|
| ᶻ, ᵺ₄ | #, ǂ | a₀, tt | 8, ϙ | Ɋ | ǂ(q-crossed), ✗ₒ, P | q, Lo | m, ʃ# | o, ʑ | ʒ | A |

Two things this settles:

- **The "q with a double bar" is the letter `s`.** It is not a separate plural marker: the plural
  ending is simply the letter s written after a code group. Tomokiyo's guess ("may well be the plural
  ending -s") is right for the wrong reason.
- **`r` is a different sign** — a q with a loop — and the two are easy to confuse in this hand.

`alpha.py` holds the map in the transcription labels used for the code groups and spells a run out.
It verifies on runs taken from R9635 f. 20r: `nx#gn` = **ahora**, `ttn#n` = **nada**.

**Why the spelled runs are nevertheless not yet read continuously.** Tomokiyo transliterates the code
groups with latin labels (`zid`, `vog`, …) drawn from a set that includes `v`, which is not one of the
twenty-two plaintext letters; so the code labels and the alphabet do not share one transliteration, and
each sign has to be matched to both by eye. At the resolution DECODE serves, distinguishing the
homophone pairs — `Ɋ` (r) from `ǂ` (s), `9` (l) from `Ɋ` (r), `∞` (d) from bold `∞` (g) — is a
judgement call per occurrence. Getting it wrong silently produces plausible-looking Spanish that is not
what the page says, so the runs are left marked rather than filled in.

The way through is the one the glosses offer: collate the patchy interlinear decipherment on R9635
f. 20r word by word against the signs beneath it, which pins each homophone in *this* scribe's hand,
and then the unglossed lines and the rest of the group follow. That is edition work against a published
key, not cryptanalysis.

## R9605 gives ground truth, and it changes two things

R9605 (9/24 f. 39-44, 7 May 1522) is the record Tomokiyo broke the cipher from, and its images show
why: the **cipher and the clerk's full contemporary decipherment sit on facing leaves**. Fetched here
and aligned at the end of the letter (`calibration_r9605.md`):

> *plegue adios* `nuf` `pac` `ɡɣβ4q4` `vog` `veg` `zn·β·aɥ` `nuf` = "plegue a Dios **no lo yerre en el
> camino**"

`vog veg` = *en el* is Tomokiyo's own way in, met here in situ. Two things follow that the key alone
could not give:

1. **Code groups are used for syllables, not only whole words.** `nuf` is *no* the adverb, and in the
   next breath the final syllable of *cami-no*. A reading that assumes one group = one word will
   mis-segment.
2. **The lookalike signs separate.** *camino* needs `β` = **m**; *ahora* (`nx#Ɋn`, R9635 f. 20r) needs
   `Ɋ` = **r**; the bold `∞` is **g**. All three are a "g"-shape at DECODE's resolution and they are
   the single largest source of error in the spelled runs.

This is the calibration route: align the whole of R9605's cipher against its decipherment - several
hundred signs of ground truth - to fix each homophone in this scribe's hand, then carry it to the
unglossed pages. That is the next session's work.

## What is left

The other 27 records. Most of them have a contemporary decipherment bound in — though R9635 shows the
glossing can be patchy — so the work there is transcription and edition, not cryptanalysis: the cipher is Tomokiyo's, and this folder's key file is
enough to check any passage. The Lope Hurtado de Mendoza letters are **not** in Sánchez's cipher — see below.

## Lope Hurtado de Mendoza writes in a third cipher

R9648 (9/26 f. 260–265, 9 Nov 1522) is Lope Hurtado to Charles V, and mixes clear and cipher inline
within the sentence, in the same general style. But his code groups take finals that Sánchez's key
does not have. Sánchez's third position is strictly C3 ∈ `b c d f g h l m n`; Lope Hurtado's leaf
gives `tep`, `tap`, and groups ending in `z`. Juan Manuel's Rome cipher, by contrast, does use
`p r s t z` as finals (`jap` papa, `jir`, `jus`, `boz`, `qat`).

So Lope Hurtado's key is a third member of the same family, not Sánchez's. Whether it is Juan
Manuel's own is not settled here: none of the groups legible on f. 260v (`ton`, `tep`, `tap`, `xul`,
`xild`, `zar`, `xurzun`) has a value in Tomokiyo's Juan Manuel table either, but that table is itself
only a partial recovery, so absence does not decide it. The nine Lope Hurtado records deserve
their own target.

f. 260r opens in clear: "La carta de V. M[agestad] recebi de xxvj de octubre; don Juan era ya ydo
quando yo llegue aqui; yo yua para el duque a Mariño donde estaua, para hazer con el lo que V. M. me
embio a mandar que hiziese con don Juan si aqui estouiera; y el duque vino a su S[eñoria] con las
cartas de V. M., y bolui con el, que le tope en el camino. Parecele que yo deuia residir aqui
continuamente para seruir mejor a V. M. …" — the same letters of 26 October that R9653's foot cipher
paragraph reports arriving at Venice.
