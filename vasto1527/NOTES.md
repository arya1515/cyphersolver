# BnF fr. 3022 nos. 6, 10, 20: del Vasto and Ranzo ciphers, 1527–28 (catalogue item 7)

Gallica ark `btv1b90601558` (view = canvas; ink folio ≈ (view+1)/2; the BnF notice's folio numbers run about
3 higher than the ink foliation). Work done 2026-09-18.

## Verdict per item

| no. | ink ff. / views | what it is | status |
|---|---|---|---|
| 10 | ff. 26–28 (views 51–55) + loose f. 39 (views 76–77) | del Vasto to Charles V, "De Ysola" (Ischia), 27 Sept 1527 | **solved, prior art.** George Lasry (2023) with Satoshi Tomokiyo's edited text (2026), cryptiana GL.htm §"Gasto–Charles V Cipher 1"; copy in `prior/BnF_fr3022_f26_decryption.txt`. Some groups are still marked `?` there. |
| 6 | ff. 16v–17v (views 32–34) | catalogued as "Rapport … à l'empereur", no author; actually del Vasto to Charles V, [Rome, early Dec 1527]: it cites his letters of 6 Nov and 27 Sept and names Castaldo as bearer | **read.** Lasry's 2026 preliminary letter-level decryption (Cipher 2) was checked against the f. 16v ciphertext. This session identified ~40 of the three-letter code groups from context and gives an edited reading: `n6_reading.md`. About 15 codes and the "…" stretches remain open. |
| 20 | ff. 44r–46v (views 86–91) | Italian letter, Madrid 11 April 1528, **to "Garbino"** (endorsement, f. 47v); the writer is almost certainly **Hieronimo Ranzo**, Gattinara's man (same code as Ranzo's signed letters, below) | **not solved.** Code structure established, full transcription made, function-word skeleton only. See below. |

Also in the volume:
- **f. 16r–v** is clear text.
- **ff. 40–43 (no. 19, 6 Nov 1527)** is Cipher 2. Its content is summarised in CSP Spain III.2 no. 233 (from RAH Salazar A-41 f. 329).
- **ff. 48–50v (nos. 20bis–21)** is Garbino's espionage kit:
  - A jargon sheet: cover letters are signed "Antonio de Cosenza" and addressed to "Andrea Romano in Valencia", and news is disguised as grain prices.
  - A code-name list, e.g. Imperatore = "Joan Jacobo", Marchese del Guasto = "portolano de Gergenti", Garbino = "antonio petra".
  - The **"Aditione nel zifra"** (`additione.json`).

## No. 6 / Cipher 2 (del Vasto, Dec 1527)

Caesar +1 over a 21-letter alphabet with homophones, plus b-/c-/d- three-letter codes. The code identifications,
with evidence, are in `n6_reading.md`. The surest are:
- Lautreque (doz); la Marca (deh); buelta (bog); hombre (ceg)
- quiere (daf); para (dor); primero (baf); mi (raq); qual (dnd); quando (dod); si (don); su (dum); ni (cez)
- dinero (dnb); duque (biq); estado (boq); gente (cef)

Some of Lasry's short "homophone" labels are systematically off: "con" is como, some "al" are el, and some
"fin" are (de)mas. The content is del Vasto's plan to take the army out of Rome toward Tuscany: secure Siena,
threaten Florence, take Perugia and the state of Urbino, and pass into the Marche. He also warns that the army
cannot be sustained "desta manera" without money.

## No. 20 / the Garbino–Ranzo code

**System.** Each group is a base letter with a superscript number: c170, i100, p149 and so on. The addition
sheet (f. 50) shows that the base letter is the initial of the word or syllable (a327 apresso, c327 Cartagenia,
g215 Garbino, h106 havendo, s395 soa santita). It also shows that entries continue each letter's base list
(a1–326, b1–156, c1–326, …, z1–35).

**The numbering within a letter is not alphabetical.** Tested in `n20/alphatest.py`:
- no. 20 scores z = −0.5 against a shuffled-order null.
- The test's power check, a genuinely alphabetical code applied to Castiglione's letters, scores z ≈ +6.5.

So a number carries no positional information. Other bases:
- **z** (z6–z9, z15): behaves as nulls or punctuation.
- **y** (y2–y53, ~130 tokens): a genuine list of unknown initial. Its glyph resembles the addition sheet's x.
- **Q** and **D**: rare extra lists.

**Ciphertext in the same code.**

| source | groups | notes |
|---|---|---|
| no. 20 (`n20/f44r.txt` … `f46v.txt`) | 1,315 (546 types) | transcribed from full-resolution scans |
| Ranzo's signed letters, BnF fr. 2988 ff. 2r–v, 9r–10v (ark btv1b9059908w, views 6, 7, 17–20) | ~2,600 | `n20/ranzo_c0*.txt`, transcribed by six subagents. f. 2v is marked "dup.ª" (duplicate). |
| **Total** | ~3,900 | 316 group types shared between the two sources |

fr. 2988's other "pièces en chiffre" (views 43–87, alternating with clear copies of Doria letters, July–Aug 1528) are a dense symbol cipher of the French side, not this code; checked views 56 and 60. Not yet transcribed: Ranzo in fr. 3019 no. 27 (f. 73, ark btv1b9059994n, view ≈ 140–148 not located) and
possibly fr. 3019 no. 36 (f. 94, "Reporto de homo … venuto da Genova", chiffré).

**Clair. 327 ff. 279–280** (btv1b9000764n views 263–264) is an 18th-century copy of no. 20. It is headed
"Vol. 86 fol. 44 … Lettre non signée écrite au seigneur Garbino du 11 d'avril 1528 … partie en chiffre, partie
non", and has no decipherment. **Clair. 314 f. 337** (btv1b90007741 view 252) copies the addition and jargon
sheets. No French decipherment and no base key was found.

**Attack (`n20/solve2.py`).** A word-substitution annealer:
- each group type maps injectively to a word with the right initial
- z-groups are optional nulls
- scoring is a Kneser–Ney word-bigram model on Castiglione's *Lettere* (1769–71 ed., long-s OCR repaired) plus Guicciardini/Machiavelli from Wikisource

It was validated on a held-out 3,900-word Castiglione control encoded the same way: **token accuracy ~46%,
type accuracy ~9%**. So on the real text it can deliver only the function-word skeleton. That skeleton is
stable across six restarts:
- che (c170), il (i100), per (p149), la/le (L10/L47), re (r41), non (n38), si (s8), sua (s233)
- tanto (t89), tempo (t10), ma (m8), ne (n8), mi (m170), più (p246), molto (m7), nel (n90)
- ha/ho (h57/h30), in (i29), perché (p150), con (c227), a (a127), o (o113), io (i286), al (a137)

Content words are not recovered. **A reading needs the base key or real cribs.** The most promising crib
sources are:
- Garbino's side of the correspondence;
- Ranzo's letters in Spanish or Italian archives with contemporary decipherments;
- Gattinara's papers.

## Files

- `n6_reading.md`: no. 6 edited reading and code table
- `n6_codes.json`, `n6_subst.txt`, `n6_lasry_joined.txt`: working files
- `n20/`: transcriptions (no. 20 and Ranzo), `load.py`, solvers (`solve.py` and `anchor.py` assume
  alphabetical order, now refuted; `free.py`, `solve2.py`), `alphatest.py`, `calib.py`
- `additione.json`: the addition sheet (f. 50–50v)
- `prior/`: Lasry/Tomokiyo decryption files and key images
- `bho/`: CSP Spain III.2 pages (BHO)
- `ita/prep.py`: corpus preparation. The corpus texts themselves are not committed.
