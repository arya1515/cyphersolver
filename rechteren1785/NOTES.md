# Rechteren (St Petersburg) to the Griffier, 23 Sept / 4 Oct 1785 — DECODE R1039

Status: read (deciphered at the time; the decipherment is bound with the cipher)

- **Source.** Nationaal Archief, 1.01.02 Staten-Generaal, inv. 7407; DECODE R1039
  (`NA_1.01.02_SG_unr7407_by_C.A._graaf_van_Rechteren_1785-10-04`), 5 images, 5448–5452. Catalogue entry 'Christiaan
  Albrecht graaf van Rechteren … to States General', scored by rule, DECODE status "Non-decrypted".
- **Writer.** Christiaan Albrecht graaf van Rechteren tot Borgbeuningen, envoy extraordinary of the States General to
  Catherine II, 1785–89, writing on arrival to the Griffier (Fagel), "Hoog Edele Gestrenge Heer".

## What the record holds

| Image | Content |
|---|---|
| 5448–5449 | **"Ont cyfferde Missive van den Heer Grave van Rechteren tot Borgbeuningen"**, marked *Secreet*, dated 23 Sept/4 Oct 1785, received 25 Oct 1785: the Griffie's clear decipherment, signed copy form "(: geteekend :)". |
| 5450–5452 | The cipher itself: 424 three-digit groups with digit marks (two dots, bar, dot), a numerical nomenclator; same heading, dates and "Ik heb de Eer" close. |

DECODE's transcriber (IB, 2020) transcribed images 5448–5449 as `<CLEARTEXT>` with many `<IL>` and did not note the
heading "Ont cyfferde" (deciphered), so the record was catalogued as undeciphered. It was read at the time.

## Reading

Full transcription: `R1039_decipherment.txt` (read from the scans 21 Sept 2026; DECODE's version is mostly illegible).
In short: De Swart (the resident secretary) told Rechteren on arrival not to hand his letter to the Grand Duke Paul,
since it would only rouse jealousy at Catherine's court and harm the Republic, as with Meinertzhagen, who also kept his
back; Rechteren complied and hopes this part of his instructions left unexecuted will not be held against him. Sure that
**all his letters are opened**, he asks leave to send couriers when absolute secrecy is needed and asks for the reply
**in cipher**, "alzo een ongecijfferd de ontdekking van het cyffer zou faciliteeren" (an unciphered reply would help the
discovery of the cipher). This is the letter de Leeuw (2000, note on Russian interception) cites for complaints of letter
opening in Russia; he does not print the text.

## Checks

- 310 plaintext words against 424 groups: a normal ratio for a code that spells some words by syllables.
- Neither provisional Rechteren-family key from `deswart1782` (R2051, R2052 alignments, marks dropped) gives Dutch on
  R1039 (`parse_test.py`: 75 and 79 base hits, mutually conflicting). The marks are part of the code.
- Not checked here: a group-by-group alignment of the cipher against the decipherment.

## Why this matters beyond R1039

R1039 is a **424-group known-plaintext pair in Rechteren's own code**, the "missing Rechteren-family nomenclator" that
blocks the first 1,928 groups of R1040 (`deswart1782/METHOD_AND_STATUS.md`). It is larger and cleaner than R2051/R2052
and has per-digit mark transcription on DECODE. Aligning it is the next step for R1040, not for this target.

## Files

- `decode/` — DECODE page, images (git-ignored) and `DOC_R1039_D3590_3590.txt` transcription.
- `R1039_groups.tsv` — cipher groups parsed from the DECODE transcription (image 5451 + 5452; raw, base, marks).
- `R1039_decipherment.txt` — the contemporary decipherment, transcribed.
