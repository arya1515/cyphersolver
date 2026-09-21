# Rodrigo Niño (Naples) to Charles V, 19 March 1522 — BNE MSS/20213/27 (DECODE R1182)

Status: no write-up — skipped (attempted, not read). The cipher system was already rebuilt in print (Kolosova 2017, Cifra 15),
but I could not get her key, and a ciphertext-only attempt on this one block failed. Catalogue entry 151 is marked
"skipped" until Kolosova's key or a better scan is in hand (see "What would move it").

## The document

- Biblioteca Nacional de España, MSS/20213/27 (Gayangos collection; stamp "PASCUAL de GAYANGOS" on f. 1).
  DECODE R1182, 3 images (authenticated; not public domain, so the images stay git-ignored):
  `IMG_R1182_I5903_P1.png` (f. 1r), `IMG_R1182_I5904_P2.png` (opening f. 1v–2r), `I5905_P3` (did not download).
- Headed "S.a C.a C.a M.t", dated at the top and at the foot "Napoles 19 de março 1522"; signed by Rodrigo Niño.
- **The letter is almost all clear Spanish.** It covers the death of the viceroy (Ramón de Cardona, d. 10 March
  1522), the Council's steps to govern the kingdom, pleas for a successor, Don Juan Manuel, the duke of Sessa's arrival,
  Marco Antonio Colonna, the French in Lombardy, and financial business (the *pagamentos fiscales*, Salmona, the sale
  of offices). **One paragraph is ciphered**: 8 lines on f. 1v (lower half of the left page), opening with
  `[mer]` and closing `[mer por]`. It comes after the paragraph about the duke of Sessa and Juan Manuel and before one
  on the tension in Naples between the popolo and the nobles, so it probably concerns the viceroyalty or Juan Manuel.
- DECODE describes it as "homophonic; graphic signs, numerical", date "1522", sender Rodrigo Niño, Naples. That is right.

## Prior art (checked first)

- **Tomokiyo, cryptiana `spanish2C_now.htm` (copy at `vasto1527/prior/`), "Ko.15 Rodrigo Niño (1522)"**: Olga Kolosova
  reconstructed Niño's cipher "from three letters in Spanish from 1522. This is a simple substitution cipher. The
  specimen includes three symbols for words/phrases (e.g. 'g e' = gente de armas) ... three- or two-letter
  combinations such as 'por', 'pu', 'mor', 'mer', looking like codes, are used as nulls (p. 458-459)."
  **This block opens with `mer` and closes with `mer por`**, which fits her description exactly. So this is the same
  system, and very probably one of her three letters (her corpus is Salazar y Castro at the RAH plus BNE letters).
- Kolosova, O. (2017), *El lenguaje secreto de la diplomacia de Carlos V (1521-1527)*, doctoral thesis, Universitat de
  València (RODERIC hdl 10550/66216). **The RODERIC PDF (148 pp., `lit/`, git-ignored) is a short version with no Niño
  chapter**; Tomokiyo cites 854 pp. The 2024 book (Ediciones Universidad de Salamanca, doi 10.14201/0MX001, 20 €, not
  open access) has a "Cifrarios" section at pp. 171–224, which should contain the Niño alphabet.
- So a reading probably exists in Kolosova's thesis edition. I have not seen it, and I cannot confirm this letter is
  among her three.

## Attempt (21 Sept 2026)

- `cipher_p2.txt`: an eye transcription of the 8 lines, one ASCII letter per sign, spaces kept. 128 words, 336 signs;
  `#` (a double-barred cross) follows many other signs and is 19% of all signs. Recurring words: `oto` ×7, `xzH` ×7
  (probably *que*), the single-sign words `T` ×5 and `w` ×4 (probably *y* and *a*).
- `anneal.py` + `nulltest.py` + `mergetest.py`: simulated annealing with `lang` es-golden-age 5-grams, at most two
  signs per letter, and with variants: `#` dropped as a null, `o` dropped, both dropped, `#` merged into the sign
  before it. **Best −2.9 to −3.5 per character; real Spanish scores about −1.1.** Nothing readable.
  (The first run, with no cap on signs per letter, collapsed to all-'i'. The cap is needed.)
- Why it fails: the signs are small cursive shapes at DECODE's resolution (about 12 px high). Several pairs
  (`g`/`9`, `l`/`L`, `4`/`+`, the barred signs) cannot be separated reliably, and the null groups (Kolosova's
  `mer/mor/pu/por`, plus possibly `ao`, `eo`, `oe`, `mo`) cannot be pinned down without the key. 336 signs with
  unresolved nulls and a doubtful transcription is below what a blind attack needs.

## What would move it

1. Kolosova 2024, "Cifrarios" (pp. 171–224) or the full 2017 thesis: the Ko.15 alphabet would read the block at once.
2. A better image: BNE Biblioteca Digital Hispánica may hold MSS/20213 at full resolution (the DECODE note points there).
3. Niño's other ciphered 1522 letters (RAH Salazar or BNE MSS/20213): more text for a proper attack.
