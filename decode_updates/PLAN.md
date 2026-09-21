# DECODE update plan

Status: draft, revised 2026-09-21 after George Lasry's reply. Nothing has been sent to DECODE.

Your account (danielbourdeau, user level 2) cannot edit records yet: `RecordsEdit` redirects with "You do not have
permission to edit the record" (tested 2026-09-21). George expects Beáta Megyesi to grant write access first.

## What each record gets (George's checklist)

1. **Status**: see the record table below.
2. **Additional information**: append, keeping what is there:
   `Updated by Dan Bourdeau, 2026: <read / read in part>. Key: <DECODE ID, or "reconstructed, see attached key file">.
   <External source, if any>. Write-up: <link>.`
3. **Key file** (`.txt`, DECODE key format), only where we rebuilt the key ourselves (group B below). Where the key
   is already in DECODE (group A), give its ID instead and upload nothing.
4. **Decoded text** (`.txt`) for every record we read, in DECODE's decryption layout (header lines, then each
   ciphertext line with its plaintext under it, as in Lasry's files, e.g. `acciaiuoli1757/decode/DOC_R195_D1657_1657.txt`).
5. **Descriptive fields** (Symbol Set, Cipher Type, languages), only for original decodes, where DECODE's values are
   wrong or blank.

### DECODE key format (from R936, `DOC_R936_D2668_2668.txt`)

```
#KEY: reconstructed
#CATALOG NAME: <record name>
#LANGUAGE: FR
#TRANSCRIBER NAME: Dan Bourdeau
#DATE OF TRANSCRIPTION: September 2026
#STATUS: reconstructed
#ORIGIN-CITY: ...
#ORIGIN-COUNTRY: ...
#DATE: 1754-01-01 - 1756-12-31

<NOTE ED free-text notes: nulls, homophones, open codes>

90 - a
99 - ai
```

## Per target

### A. Key already in DECODE: give the ID, no key upload

| Target | Records | Key to cite | External source to mention |
|---|---|---|---|
| bordeaux1653 | R8390, R8391, R8393 | R7537 (BL Add MS 32263 f. 1, English Deciphering Branch key) | none |
| deswart1782 | R1036, R1040 | R1038 (Croiset 1765 codebook) | none; say that R1040's first segment needs the missing Rechteren key |
| vanreede1787 | R1026, R1027 | R1024 (Grand Chiffre 1782); controls R1028/R1029 | none |
| rakoczi1707 | R902 (+R852, R912) | R639 (Fasc. 44/08) | none |
| alessandrino1568 | R93–R102, R115 | Lasry's reconstructed key, already attached to the same records | Serrano, *Correspondencia diplomática* (1914), for context |
| acciaiuoli1757 | R25, R195–R201 | Lasry's key on the same records | three contemporary decipherments on the leaves |
| ceva1632 | R75, R84 | Lasry's key on R74–R84 | none |
| sauli1579 | R190–R194 | Lasry's key on the same records | contemporary interlinear decipherments |

For the Lasry-key records (owner 6), our contribution is the plaintext text only, plus a few added code values. That
should be said plainly in the note.

### B. Key rebuilt here: upload a key file

| Target | Records | How the key was rebuilt | Cite in Additional information | Key source file to convert |
|---|---|---|---|---|
| warsaw | R1408 | ciphertext-only | nothing | `warsaw/key_*.json` (pick the final one) |
| lucca | R2159 | crib (the opening from Tomokiyo's unsolved page) | Tomokiyo, cryptiana | not in repo as a key file: derive from `plaintext.txt` |
| lopehurtado | R9644, R9648, R9650 (+R9652 is clear) | crib: the clerk's clear version bound with the cipher | nothing (not in Tomokiyo 2025) | `key_codes.tsv` |
| kauderbach1754 | R1043, R1044, R1954, R1958, R1959, R2078–R2082 | one-to-one annealing onto the vocabulary of the 1761 key | R936 (same design, different numbers) | `key.json` |
| balbases1677, hernannunez1674, ronquillo1676 | R985–R998, R1012–R1015, R966–R984, R1001 | one key, rebuilt from the contemporary margins on these records | "key from the marginal decipherments on R985 etc." | `balbases1677/key.json` (+ the hernannunez additions) |
| kurtz1639 | R3811–R3815, R4625, R4645, R4734, R4736 | from the interlinear glosses on R3811 | Márka 2012 (summary of R3811; no key printed) | `key.json` / `KEY.md` |
| affry1757 | R1054, R1065, R1070, R1072–R1074, R1076, R2067 | aligned on Lyonet's clear copies (R1052, R1053, R1062, R1063, R1066, R1069, R1075) | Bussemaker, *BMH* extracts; Lyonet, NA 1.01.50 inv. 221/223 | `key_U.json` |
| sessa1524 | R9877, R9878 | from Sessa's decrypted sibling letters R9897, R9893, R9834 | nothing | `key_working.md` (needs finishing) |
| soria1523 | R9488–R9498 | key A rebuilt; key B also in R9844 with the court's decipherment | R9844 for key B | `keyA.md`, `keyB.md` |
| buda1489 | R1098 | Somogyi's numeric key re-anchored to the signs | Somogyi 2016 (key and lines 1–2 of the 22 Nov 1489 letter) | `key.json` |
| sanchez1522 | R9635, R9653 | Tomokiyo's published key, plus the c-block numerals we added | Tomokiyo, cryptiana, Sept 2025 | `key_codes.tsv` (additions only, marked) |

### C. Descriptive fields to correct (original decodes; DECODE value now → proposed)

| Records | Field | Now | Proposed |
|---|---|---|---|
| R1408 (warsaw) | Cipher type; language | homophonic + simple; none | homophonic + nomenclator; Italian |
| R2159 (lucca) | Cipher type; plaintext language | unknown; none | homophonic + polyphonic; Italian |
| R1043, R1044, R1954 … (kauderbach) | Cipher type | unknown | nomenclator |
| R9644–R9656 (lopehurtado), R9877/R9878 (sessa), R9488–R9498 (soria), R9635/R9653 (sanchez) | Cipher type; plaintext language | unknown; blank | homophonic + nomenclator; Spanish |
| R8390, R8391, R8393 (bordeaux) | Cipher type; plaintext language | unknown; none | homophonic + nomenclator; French |
| R1098 (buda) | Cipher type; plaintext language | blank; "Italian?" | homophonic + nomenclator; Italian |
| R902 (rakoczi) | Plaintext language | none | French |
| R1036 (deswart) | Plaintext language | "Dutch or French" | Dutch |

Symbol sets on these records already match (numerical; graphic + alphabet for the Spanish ones), so no change there.
Values here come from our profiles and a sample of records. Check each record's view before editing.

## The queue and the upload package

The record list is now kept in `decode_updates/queue.json` (one entry per target: key source, citation, field
changes, and per record the current DECODE status, the proposed one, the note and the reading file). It holds 118
records across 26 targets; `sadoleto1482` and `sp106box10` are marked skip until they are read further.

- `python decode_updates/queue.py status` shows what is queued and what still says TODO.
- `python decode_updates/queue.py add <folder>` queues a newly finished target from its profile.json (the /writeup
  skill does this; `docs/_check_writeup.py` reports MISS until it is done).
- `python decode_updates/build.py [target]` writes `decode_updates/out/R<id>/` (git-ignored): `additional_information.txt`,
  `fields.txt`, `key.txt` (rebuilt keys only, DECODE key format) and `decryption.txt` (DECODE header + our reading).
- After editing a record on DECODE, set its `"sent": true` in queue.json.

Keys converted by hand, where the key lived in code rather than a file: `decode_updates/keys/` (warsaw, lucca,
r1892, riksarkivet1628). The table below is the first snapshot (21 Sept); queue.json is the current list.

## Decryption files: cleaned, and what to review before upload

`decode_updates/decryptions/R<id>.txt` holds the public text of each record (116 files; R190/R191 need none), written
to `decode_updates/CLEANING_BRIEF.md`: the letter text only, page markers, `<nnn>` unread groups, `{word}` inferred,
`word?` uncertain, `[clear: ...]`, `[contemporary decipherment: ...]`. No letter of our readings was changed; the
cleaning split run-on streams into words, normalised gap marks and dropped notes. build.py uses these files.

Review by a reader of the language before upload:
- **Machine streams split into words, many runs left joined with `?`:** alessandrino1568 (all 11), papai1706
  (R757, R765 worst), kurtz1639 (all 9; split by script, ~40% of lines carry `?`), deswart1782 (R1036, R1040),
  rakoczi1707 R902 (not split), ronquillo1676 R971, R974, R983, R1001 (`<W>chad<r>` artefacts, likely a glitch in
  `ronquillo1676/read.py`; regenerate them from a fixed decoder).
- **Thin: little of the letter is read:** sanchez1522 R9635/R9653, rome1536 R4234/R4235/R4239, sauli1579 R192-R194
  (cipher passages only; the clear text was summarised in English), ceva1632 R75/R84, soria1523 R9494,
  kauderbach1754 R1954, affry1757 R1072, kurtz1639 R4645/R4734/R4736.
- **Only the contemporary decipherment, not ours:** affry1757 R1065, lopehurtado R9644/R9648/R9650, rome1536 R4248.
- **Choices to confirm:** bordeaux R8391 (where the duplicate ending starts, check ff. 93-93v); r1892 struck groups
  dropped; soria R9491 folio order; acciaiuoli code words written `{word}` though most come from sibling
  decipherments; sessa R9878 treated as a token-for-token duplicate of R9877.

## Records (100)

| Record | Target | DECODE now | Proposed | Note | Write-up |
|---|---|---|---|---|---|
| [R25](https://de-crypt.org/decrypt-web/RecordsView/25) | acciaiuoli1757 | Partially decrypted | **Decrypted** | All eight letters read at letter level with Lasry's key + 3 clear decipherments; ~27 codes open. | [page](https://dbourdeau.github.io/cyphersolver/acciaiuoli1757.html) |
| [R75](https://de-crypt.org/decrypt-web/RecordsView/75) | ceva1632 | Partially decrypted | **(no change)** | R75, R84 read for the first time (~92% tokens valued); most nomenclator names still open. | [page](https://dbourdeau.github.io/cyphersolver/ceva1632.html) |
| [R84](https://de-crypt.org/decrypt-web/RecordsView/84) | ceva1632 | Partially decrypted | **(no change)** | R75, R84 read for the first time (~92% tokens valued); most nomenclator names still open. | [page](https://dbourdeau.github.io/cyphersolver/ceva1632.html) |
| [R93](https://de-crypt.org/decrypt-web/RecordsView/93) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R94](https://de-crypt.org/decrypt-web/RecordsView/94) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R95](https://de-crypt.org/decrypt-web/RecordsView/95) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R96](https://de-crypt.org/decrypt-web/RecordsView/96) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R97](https://de-crypt.org/decrypt-web/RecordsView/97) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R98](https://de-crypt.org/decrypt-web/RecordsView/98) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R99](https://de-crypt.org/decrypt-web/RecordsView/99) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R100](https://de-crypt.org/decrypt-web/RecordsView/100) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R101](https://de-crypt.org/decrypt-web/RecordsView/101) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R102](https://de-crypt.org/decrypt-web/RecordsView/102) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R115](https://de-crypt.org/decrypt-web/RecordsView/115) | alessandrino1568 | Partially decrypted | **Decrypted** | All 11 read with Lasry's polyphonic key + language model; isolated letters uncertain. | [page](https://dbourdeau.github.io/cyphersolver/alessandrino1568.html) |
| [R190](https://de-crypt.org/decrypt-web/RecordsView/190) | sauli1579 | Partially decrypted | **Decrypted** | Read from the contemporary decipherments + Lasry's key; a few codes open. | [page](https://dbourdeau.github.io/cyphersolver/sauli1579.html) |
| [R191](https://de-crypt.org/decrypt-web/RecordsView/191) | sauli1579 | Partially decrypted | **Decrypted** | Read from the contemporary decipherments + Lasry's key; a few codes open. | [page](https://dbourdeau.github.io/cyphersolver/sauli1579.html) |
| [R192](https://de-crypt.org/decrypt-web/RecordsView/192) | sauli1579 | Partially decrypted | **Decrypted** | Read from the contemporary decipherments + Lasry's key; a few codes open. | [page](https://dbourdeau.github.io/cyphersolver/sauli1579.html) |
| [R193](https://de-crypt.org/decrypt-web/RecordsView/193) | sauli1579 | Partially decrypted | **Decrypted** | Read from the contemporary decipherments + Lasry's key; a few codes open. | [page](https://dbourdeau.github.io/cyphersolver/sauli1579.html) |
| [R194](https://de-crypt.org/decrypt-web/RecordsView/194) | sauli1579 | Partially decrypted | **Decrypted** | Read from the contemporary decipherments + Lasry's key; a few codes open. | [page](https://dbourdeau.github.io/cyphersolver/sauli1579.html) |
| [R195](https://de-crypt.org/decrypt-web/RecordsView/195) | acciaiuoli1757 | Partially decrypted | **Decrypted** | All eight letters read at letter level with Lasry's key + 3 clear decipherments; ~27 codes open. | [page](https://dbourdeau.github.io/cyphersolver/acciaiuoli1757.html) |
| [R201](https://de-crypt.org/decrypt-web/RecordsView/201) | acciaiuoli1757 | Partially decrypted | **Decrypted** | All eight letters read at letter level with Lasry's key + 3 clear decipherments; ~27 codes open. | [page](https://dbourdeau.github.io/cyphersolver/acciaiuoli1757.html) |
| [R902](https://de-crypt.org/decrypt-web/RecordsView/902) | rakoczi1707 | Non-decrypted | **Decrypted** | Cipher solved; transcript noisy, 72% clean. | [page](https://dbourdeau.github.io/cyphersolver/rakoczi1707.html) |
| [R966](https://de-crypt.org/decrypt-web/RecordsView/966) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R969](https://de-crypt.org/decrypt-web/RecordsView/969) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R970](https://de-crypt.org/decrypt-web/RecordsView/970) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R971](https://de-crypt.org/decrypt-web/RecordsView/971) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R972](https://de-crypt.org/decrypt-web/RecordsView/972) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R973](https://de-crypt.org/decrypt-web/RecordsView/973) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R974](https://de-crypt.org/decrypt-web/RecordsView/974) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R981](https://de-crypt.org/decrypt-web/RecordsView/981) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R982](https://de-crypt.org/decrypt-web/RecordsView/982) | ronquillo1676 | Non-decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R983](https://de-crypt.org/decrypt-web/RecordsView/983) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R984](https://de-crypt.org/decrypt-web/RecordsView/984) | ronquillo1676 | Non-decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R985](https://de-crypt.org/decrypt-web/RecordsView/985) | balbases1677 | Partially decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R991](https://de-crypt.org/decrypt-web/RecordsView/991) | balbases1677 | Partially decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R992](https://de-crypt.org/decrypt-web/RecordsView/992) | balbases1677 | Non-decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R993](https://de-crypt.org/decrypt-web/RecordsView/993) | balbases1677 | Partially decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R995](https://de-crypt.org/decrypt-web/RecordsView/995) | balbases1677 | Partially decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R996](https://de-crypt.org/decrypt-web/RecordsView/996) | balbases1677 | Non-decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R997](https://de-crypt.org/decrypt-web/RecordsView/997) | balbases1677 | Non-decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R998](https://de-crypt.org/decrypt-web/RecordsView/998) | balbases1677 | Non-decrypted | **Decrypted** | Key rebuilt from margins; all 14 letters, 97% of groups; R992/996-998 read for the first time. | [page](https://dbourdeau.github.io/cyphersolver/balbases1677.html) |
| [R1001](https://de-crypt.org/decrypt-web/RecordsView/1001) | ronquillo1676 | Partially decrypted | **Decrypted** | All 20 letters read in gist (70-94% per letter). | [page](https://dbourdeau.github.io/cyphersolver/ronquillo1676.html) |
| [R1012](https://de-crypt.org/decrypt-web/RecordsView/1012) | hernannunez1674 | Partially decrypted | **Decrypted** | Read with the Balbases key; margins verified. | [page](https://dbourdeau.github.io/cyphersolver/hernannunez1674.html) |
| [R1015](https://de-crypt.org/decrypt-web/RecordsView/1015) | hernannunez1674 | Partially decrypted | **Decrypted** | Read with the Balbases key; margins verified. | [page](https://dbourdeau.github.io/cyphersolver/hernannunez1674.html) |
| [R1026](https://de-crypt.org/decrypt-web/RecordsView/1026) | vanreede1787 | Non-decrypted | **Decrypted** | Read with the Grand Chiffre R1024 (452/472 groups). | [page](https://dbourdeau.github.io/cyphersolver/vanreede1787.html) |
| [R1027](https://de-crypt.org/decrypt-web/RecordsView/1027) | vanreede1787 | Non-decrypted | **Decrypted** | Read with the Grand Chiffre R1024 (452/472 groups). | [page](https://dbourdeau.github.io/cyphersolver/vanreede1787.html) |
| [R1036](https://de-crypt.org/decrypt-web/RecordsView/1036) | deswart1782 | Non-decrypted | **Decrypted** | Read with the 1765 Croiset code R1038; 56 groups open. | [page](https://dbourdeau.github.io/cyphersolver/deswart1782.html) |
| [R1040](https://de-crypt.org/decrypt-web/RecordsView/1040) | deswart1782 | Non-decrypted | **Partially decrypted** | Second segment only; first needs the missing Rechteren key. | [page](https://dbourdeau.github.io/cyphersolver/deswart1782.html) |
| [R1043](https://de-crypt.org/decrypt-web/RecordsView/1043) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R1044](https://de-crypt.org/decrypt-web/RecordsView/1044) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R1054](https://de-crypt.org/decrypt-web/RecordsView/1054) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1065](https://de-crypt.org/decrypt-web/RecordsView/1065) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1070](https://de-crypt.org/decrypt-web/RecordsView/1070) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1072](https://de-crypt.org/decrypt-web/RecordsView/1072) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1073](https://de-crypt.org/decrypt-web/RecordsView/1073) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1074](https://de-crypt.org/decrypt-web/RecordsView/1074) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1076](https://de-crypt.org/decrypt-web/RecordsView/1076) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R1098](https://de-crypt.org/decrypt-web/RecordsView/1098) | buda1489 | Partially decrypted | **Decrypted** | Read in gist with Somogyi's key re-anchored to the signs. | [page](https://dbourdeau.github.io/cyphersolver/buda1489.html) |
| [R1408](https://de-crypt.org/decrypt-web/RecordsView/1408) | warsaw | Non-decrypted | **Decrypted** | Every spelled word read; ten word codes glossed. | [page](https://dbourdeau.github.io/cyphersolver/warsaw.html) |
| [R1954](https://de-crypt.org/decrypt-web/RecordsView/1954) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R1958](https://de-crypt.org/decrypt-web/RecordsView/1958) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R1959](https://de-crypt.org/decrypt-web/RecordsView/1959) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2067](https://de-crypt.org/decrypt-web/RecordsView/2067) | affry1757 | Non-decrypted | **Decrypted** | Nine undeciphered letters read from key rebuilt on Lyonet's clear copies (87% of groups). | [page](https://dbourdeau.github.io/cyphersolver/affry1757.html) |
| [R2078](https://de-crypt.org/decrypt-web/RecordsView/2078) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2079](https://de-crypt.org/decrypt-web/RecordsView/2079) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2080](https://de-crypt.org/decrypt-web/RecordsView/2080) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2081](https://de-crypt.org/decrypt-web/RecordsView/2081) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2082](https://de-crypt.org/decrypt-web/RecordsView/2082) | kauderbach1754 | Non-decrypted | **Decrypted** | All ten read; 99.8% of 8,512 groups valued. | [page](https://dbourdeau.github.io/cyphersolver/kauderbach1754.html) |
| [R2159](https://de-crypt.org/decrypt-web/RecordsView/2159) | lucca | Non-decrypted | **Decrypted** | Every group read. | [page](https://dbourdeau.github.io/cyphersolver/lucca.html) |
| [R3811](https://de-crypt.org/decrypt-web/RecordsView/3811) | kurtz1639 | Partially decrypted | **(no change)** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R3812](https://de-crypt.org/decrypt-web/RecordsView/3812) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R3813](https://de-crypt.org/decrypt-web/RecordsView/3813) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R3814](https://de-crypt.org/decrypt-web/RecordsView/3814) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R3815](https://de-crypt.org/decrypt-web/RecordsView/3815) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R4625](https://de-crypt.org/decrypt-web/RecordsView/4625) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R4645](https://de-crypt.org/decrypt-web/RecordsView/4645) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R4734](https://de-crypt.org/decrypt-web/RecordsView/4734) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R4736](https://de-crypt.org/decrypt-web/RecordsView/4736) | kurtz1639 | Non-decrypted | **Partially decrypted** | Key complete (rebuilt from R3811 glosses); 55-80% of each letter coherent. | [page](https://dbourdeau.github.io/cyphersolver/kurtz1639.html) |
| [R8390](https://de-crypt.org/decrypt-web/RecordsView/8390) | bordeaux | N/A | **Decrypted** | Read 2026-09-18 with the 1653 English key R7537. | [page](https://dbourdeau.github.io/cyphersolver/bordeaux1653.html) |
| [R8391](https://de-crypt.org/decrypt-web/RecordsView/8391) | bordeaux | N/A | **Decrypted** | Read 2026-09-18 with the 1653 English key R7537. | [page](https://dbourdeau.github.io/cyphersolver/bordeaux1653.html) |
| [R8393](https://de-crypt.org/decrypt-web/RecordsView/8393) | bordeaux | N/A | **Decrypted** | Read 2026-09-18 with the 1653 English key R7537. | [page](https://dbourdeau.github.io/cyphersolver/bordeaux1653.html) |
| [R9488](https://de-crypt.org/decrypt-web/RecordsView/9488) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9489](https://de-crypt.org/decrypt-web/RecordsView/9489) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9490](https://de-crypt.org/decrypt-web/RecordsView/9490) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9491](https://de-crypt.org/decrypt-web/RecordsView/9491) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9492](https://de-crypt.org/decrypt-web/RecordsView/9492) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9493](https://de-crypt.org/decrypt-web/RecordsView/9493) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9494](https://de-crypt.org/decrypt-web/RecordsView/9494) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9495](https://de-crypt.org/decrypt-web/RecordsView/9495) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9496](https://de-crypt.org/decrypt-web/RecordsView/9496) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9497](https://de-crypt.org/decrypt-web/RecordsView/9497) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9498](https://de-crypt.org/decrypt-web/RecordsView/9498) | soria1523 | Non-decrypted | **Partially decrypted** | Key-A letters read nearly throughout; key-B in substance. | [page](https://dbourdeau.github.io/cyphersolver/soria1523.html) |
| [R9635](https://de-crypt.org/decrypt-web/RecordsView/9635) | sanchez1522 | Non-decrypted | **Partially decrypted** | Parts read beyond Tomokiyo 2025 (credit his key). | [page](https://dbourdeau.github.io/cyphersolver/sanchez1522.html) |
| [R9644](https://de-crypt.org/decrypt-web/RecordsView/9644) | lopehurtado | Decrypted | **(no change)** | Clerk's full contemporary clear version is on the leaves. | [page](https://dbourdeau.github.io/cyphersolver/lopehurtado.html) |
| [R9648](https://de-crypt.org/decrypt-web/RecordsView/9648) | lopehurtado | Non-decrypted | **Decrypted** | Duplicate of R9644. | [page](https://dbourdeau.github.io/cyphersolver/lopehurtado.html) |
| [R9650](https://de-crypt.org/decrypt-web/RecordsView/9650) | lopehurtado | Decrypted | **(no change)** | Clerk's full contemporary clear version is on the leaves. | [page](https://dbourdeau.github.io/cyphersolver/lopehurtado.html) |
| [R9652](https://de-crypt.org/decrypt-web/RecordsView/9652) | lopehurtado | Partially decrypted | **N/A** | No cipher on this leaf; it is entirely in clear (DECODE says partially decrypted). | [page](https://dbourdeau.github.io/cyphersolver/lopehurtado.html) |
| [R9653](https://de-crypt.org/decrypt-web/RecordsView/9653) | sanchez1522 | Non-decrypted | **Partially decrypted** | Parts read beyond Tomokiyo 2025 (credit his key). | [page](https://dbourdeau.github.io/cyphersolver/sanchez1522.html) |
| [R9877](https://de-crypt.org/decrypt-web/RecordsView/9877) | sessa1524 | Non-decrypted | **Partially decrypted** | Read in part from decrypted siblings. | [page](https://dbourdeau.github.io/cyphersolver/sessa1524.html) |
| [R9878](https://de-crypt.org/decrypt-web/RecordsView/9878) | sessa1524 | Non-decrypted | **Partially decrypted** | Read in part from decrypted siblings. | [page](https://dbourdeau.github.io/cyphersolver/sessa1524.html) |

## Left out (20)

| Record | Target | Why |
|---|---|---|
| R657 | sp106box10 | not read far enough |
| R660 | sp106box10 | not read far enough |
| R664 | sp106box10 | not read far enough |
| R704 | sp106box10 | not read far enough |
| R720 | sp106box10 | not read far enough |
| R721 | sp106box10 | not read far enough |
| R722 | sp106box10 | not read far enough |
| R1052 | affry1757 | already Decrypted |
| R1053 | affry1757 | already Decrypted |
| R1062 | affry1757 | already Decrypted |
| R1066 | affry1757 | already Decrypted |
| R1069 | affry1757 | already Decrypted |
| R1071 | affry1757 | not read far enough |
| R1075 | affry1757 | already Decrypted |
| R1101 | sadoleto1482 | not read far enough |
| R1102 | sadoleto1482 | not read far enough |
| R1103 | sadoleto1482 | not read far enough |
| R1106 | sadoleto1482 | not read far enough |
| R1893 | vanreede1787 | not read far enough |
| R9656 | lopehurtado | not read far enough |

## Still to decide

- Our reads that are not DECODE records yet (Gallica/BnF, AGS, BL targets such as toledo1565, segur, rennes1563):
  propose them as new records once write access exists.
- Owners 6 (Vatican set) and 19 (Dutch/Brussels set) may want to review before we edit their records.
