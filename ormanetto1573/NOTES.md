# Ormanetto 1573: copy of Philip II's letter to the nuncio, with two cipher passages. ATTEMPTED, OPEN

Catalogue item 259 (class C). ASV (AAV), Segreteria di Stato, Spagna 7 (DECODE "i. 1025, doss. 7"), ff. 303r–304r,
address leaf f. 320v. DECODE R116 (Non-decrypted, 2 images + address leaf, transcription by KL, 18 Aug 2020).

**Result (21 Sept 2026): not read.** The document and the cipher are identified. The key was not found, and no
ciphertext-only attack produced text that a matched control could not also produce.

## What the document is

DECODE's catalogue line ("Ormanetto to the nuncio of the Secretariat, 7 Jan 1573") comes from the volume heading
("Nunzio alla Segreteria, dal 7 gennaio 1573 al 31 dic 1573"), not from this item. The leaves hold:

- f. 303r, headed in Italian *Copia della l[ette]ra di S. M.tà al Nuntio*: a clear Spanish copy of Philip II's letter to
  "el obispo de Padua" (Niccolò Ormanetto, nuncio 1572–77). He has been ill and is now up. He will answer the points
  the nuncio raised for His Holiness. Then comes cipher passage **A**, 13 lines of figures (marginal "A." and "H").
  Italian note pasted over the heading: *Della sanità ragguagliata del Re* ("on the King's reported health").
- f. 304r: clear numbered answers. (1) Jurisdiction: already written to Don Juan de Zúñiga, the ambassador in
  Rome. (2) The order for dividing the Turkish slaves in Rome has been sent. (3) The affairs of the bishop of Liège,
  recommended by the Pope. Then cipher passage **B**, 10 lines (marginal "B."). Italian summary at the head:
  *Risposta del Re … 1 sopra la materia di giurisdittione, 2 della ripartitione de' schiavi, 3 de negotii del
  vescovo di Lieggi raccomandato dal papa*.
- Address leaf (DECODE doc 1342, f. 320v): *All'Ill.mo et R.mo S.r mio Col.mo Mons.r Ill.mo Cardinal di Como. A Roma.
  Per servitio di N. S.re*, docketed *73 / a 17 Junii*. So this is the nuncio's despatch to Tolomeo Galli
  (Cardinal of Como, Gregory XIII's secretary of state), received or answered 17 June 1573. The King's letter
  itself is undated in the copy (spring 1573).

The cipher passages are therefore in the nunciature's cipher with Como. The nuncio enciphered the King's
confidential points for Rome, or copied them as the King's office sent them. The plaintext language is not
established: the clear frame is Spanish, the filing notes are Italian.

## The ciphertext

`r116_cipher.txt`, from DECODE's transcription (DOC_R116_D2580) and checked against the images at 2–3× for lines
1–2 of A. There are 1,098 digits in 23 lines: A 756 signs, B 568 (dots and underlines kept; `.` = dot over the digit,
`_` = underlined).

- Digits 0–9 with dots above (0̇ very common: 148; 4̇ 46; 5̇ 36). Many runs are underlined by a later hand.
- A "t"-like cross-stroke, transcribed by DECODE as a digit **1**, joined to the digit before it: 2t, 4t, "st"
  (5t). In the image it is a separate stroke fused to the previous digit, not a bare 1. Before-"1" counts:
  2 74×, 4 59×, 5 51×, others ≤10.
- No word division. Lines are not pair-aligned: second-digit parity is 60/40 at both offsets.
- The same system (dotted digits, barred 4) is on R118, Ormanetto/Clementino 1576–77 (`ormanetto1576/`): two
  samples of one nunciature cipher.

## Keys tried (all fail)

| Key | Source | Result |
|---|---|---|
| Spain nunciature 1568 (Castagna), polyphonic digit = 2 letters, Lasry | `alessandrino1568/decrypt.py` | nonsense (−3.0/item) |
| Crivelli, nuncio in Spain 1561: polyphonic an/so/ti/re…, codes X9/X3/X5 | Meister 1906 p. 259 (V.8) | nonsense (−3.7) |
| "Cifra col cardinal di Como" with Spain nomenclator (Zayas, Idiáquez, card. Deza, Antonio Pérez, Cruzada) | Meister pp. 262–264 (VI.1), `key1.py`, `decrypt.py` | nonsense. Its nomenclator marks (hooked 2, crossed 4/6) resemble the "t" here, but letters with an odd second digit do not parse. The Idiáquez and Deza entries date it after 1578 (Sega). |
| "Cifra col s. card. di Como", nulla 8, *che/chi* 116 | Meister p. 264 (VI.2) | bigram hits 347/1323, no parse |
| Spain–Flanders cipher, nulla 1, even-digit pairs | Meister p. 265 (VI.3) | impossible: 330 odd digits |

Meister VI.2 comes with the rules of "la cifra ordinaria di mons. nuntio di Spagna" (p. 265): null 8 at the end of
each word, a dot over nomenclator groups for *chi, che, qua, que, qui, et, mente*. The ordinary Spain key
itself is not printed. The dots here fit that practice, but the rules alone do not give the table.

## Ciphertext-only attacks (all fail)

- Simple and homophonic substitution over three sign sets (single digits with or without dots; digit + dot +
  underline; "0̇X" and "X t" as units, 31 signs, IC 0.055), Spanish and Italian 4-gram models with a unigram-KL
  penalty (`fa.py`, the Caprile annealer). Control: an Italian text of the same length with 28 homophones comes out
  largely readable. R116 gives nothing readable in any setting.
- Polyphonic digit = two letters (the 1568 family), letter pairs annealed with a Viterbi pass (`polyanneal.py`,
  `pa3.py`). Control: Alessandrino R97, 1,100 digits, recovers 7 of 9 of Lasry's pairs at −2.18/char. R116:
  −2.30 to −2.47, and five restarts give five different keys (`pa_it.txt`, `pa_es.txt`). With 1 as a null and
  0 as a letter digit: −2.36, again unstable.

## What would move it

1. The decifrato of the Como despatch of June 1573. Nunciature ciphers were deciphered in Rome, and the decifrato
   may sit in Spagna 7 near f. 303 or in the Nunziatura di Spagna registers. DECODE has no other record for 1573.
2. The King's minute (AGS Estado, Roma legajos, 1573) or the original letter sent to Ormanetto, if the cipher was
   the King's own. PARES catalogues only Ormanetto items of 1575 (EST,LEG,1407,217/218).
3. Carini, *Mons. Niccolò Ormaneto … nunzio apostolico alla corte di Filippo II* (Rome 1894), which prints
   nunciature documents. Not found online.
4. The key of the ordinary Spain nunciature cipher of 1572–77. Meister prints only its rules. Pooling R116 with R118
   (389 digits) for a second ciphertext-only pass is worth trying once the system is guessed.

## Remaining gaps

- Passage A (756 signs) and passage B (568 signs): unread. Blocker: no-key-material.

## Escalation

Every step open from here was checked, and each is blocked by something outside the ciphertext.

- siblings: DECODE has no other 1570-80 Spain nunciature record except R118 (unread, same system) and R5624
  (Sega 1579, N/A). Done.
- clear-pages: the record's two images and the address leaf are all read. No decifrato is imaged. The rest of
  Spagna 7 is not digitised. Blocker: needs-physical-access (AAV).
- known-keys: five period keys tried (1568 Spain, Crivelli 1561, Meister VI.1-VI.3). Meister prints only the
  rules of the Spain ordinary cipher, not its table. Done.
- print: Carini 1894 is not online (web, archive.org, Google Books). PARES has no 1573 minute. Olarra-Larramendi
  covers Philip III. Blocker: needs-physical-access.
- key-rebuild: homophonic and polyphonic annealers read same-length controls but not R116. The system is not
  identified, so there is no hypothesis left that the text is long enough to test. Blocker: too-short for an
  unknown system.
- pooled with R118 (21 Sept, second pass): 1,660 undotted signs, R116's 4t = R118's barred 4 (X). Polyphonic
  annealer (`pa_pool.py`): -2.37 to -2.46/char against -2.18 for the control, and the restart keys disagree.
  No fit. Only 11 undotted sign types, so plain homophonic substitution over them cannot carry an alphabet.
- academic print search: Fernández Terricabras, "El nuncio Niccolò Ormaneto y la reforma de las órdenes
  religiosas" (Madrid, Felipe II y las ciudades, iii, 2000, pp. 321-332) has no online full text. No edition of the
  1572-77 nunciature registers was found. Blocker: needs-physical-access.
- retry: nothing read, nothing to regrade.

## Files

- `r116_cipher.txt` the ciphertext; `tok.py` reads DECODE's transcription, `units.py` builds the sign sets.
- `key1.py` + `decrypt.py` Meister VI.1 test; `poly.py` Crivelli test; `polyanneal.py`, `pa3.py` polyphonic
  annealer; `fa.py` homophonic annealer with its control (`CTL=1`).
- `decode/` (git-ignored): DECODE images, transcription, statistics, the Meister page scans.
