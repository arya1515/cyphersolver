# Paris nunciature, bishop of Bergamo / archbishop of Nazareth, 1585–86 (ASV Segr. Stato Francia 18; DECODE R15–R17) — NOTES

**Result: read in part** (codes 18/48, about 16 R16 slips and 5 R17 codes open; see Remaining gaps). R15 read before (Lasry); R16 and R17 read here. Write-up: docs/bergamo1585.html.

Catalogue entry 242. Checked on 2026-09-21 as part of a sweep of the Paris-nunciature records on DECODE (see
[damiata1624/](../damiata1624/NOTES.md) for the 1625 volume).

## The three records

- **R15** (Francia 18/1, ff. 7r–v): **already read.** Lasry's decryption (DOC D3102) with the F18 key (D3103,
  fixed-length homophonic; "also found in Meister p. 324 and in the French book, Ragazzoni"). Nothing added.
- **R16** (Francia 18/2, f. 206r–v; cleartext heading "3 di Marzo 1586"): **decrypted here, in part.** DECODE's
  decryption file for R16 (D3104) is byte-for-byte the R15 decryption (19,639 bytes, same text), attached to the
  wrong record, so R16 had never actually been decrypted. The F18 key (D3105, same as R15's) applied to the DECODE
  transcription D1610 (TimB) with `decode_with_key.py` gives readable Italian at once: 1,410 letter pairs, 66
  unknown (transcription slips and phase breaks). Output in `R16_decryption.txt`.
  Content: *hoggi il [58] mi ha mandato a dire … la bolla … la congregatione del clero … mal contenti dela
  concessione dela bolla … l'alienatione … appellarsi ad futurum concilium …* — the French clergy's resistance
  to the papal bull permitting the alienation of church property, 1586.
  **Nomenclator (same day):** Meister p. 324 no. 2 prints Ragazzoni's 1583 Paris key, the same letter alphabet with
  its nomenclator (OCR in the main checkout's `vatican5/meister.txt`, ll. 59655–59920; realigned in
  `meister324_nomenclator.txt`). Added to the decoder with a one-digit resync for transcription slips: unknowns fall
  from 66 to 18. Confirmed by context: 26¸ che, 36¸ per, 28+ questi, 98+ essere, 20- non, 0^. con, 34 Re
  Christianissimo, 58 Duca di Guisa (who asks for Metz), 14 Nostro Signore. **Not confirmed:** 18 and 48 (Meister's
  Ferrara/Parma) turn up where no duke fits; the 1586 table may have moved them. The letter: Guise will not let the
  King sell church property under the bull unless he gets Metz and money; the clergy's assembly means to appeal to a
  future council, hoping for the Pope's help.
  **Open (was):** about 20 nomenclator codes marked with a cedilla, + or – (26¸, 28+, 36¸, 20-, 58, 34, 70, …) are
  not in Lasry's key. 26¸ behaves like *che*, 20- like *non*, 58 is a person (probably the King or a prelate), 34
  another (probably the Pope). Filling them needs context work or Meister's full table.
- **R17** (Francia 18/3, ff. 233r–235v): **read (same day).** Meister p. 393 no. 40 (Morosini, 1587), already
  keyed in `morosini1588/decrypt.py`, reads DECODE's transcription D1611 on all five pages with 5 unknown codes:
  the Duke of Lorraine and Guise, the German reiters, the Queen Mother, Schomberg (`R17_decryption.txt`). So R17 is
  a Morosini-period letter (1587–88), not Bergamo/Nazareth. Earlier note: DECODE's key (D3186, ASV F22) is a different system:
  variable-length and *not deterministic* (1–3 digit elements, 8 and 80–89 null). The note says it is incomplete
  and that the full key is Meister p. 393 no. 40. DECODE's decryption file is a Java crash (NullPointerException),
  so R17 had no decryption before this.

## Files

`key_F18_lasry.txt` (DECODE D3105), `R16_transcription_decode.txt` (DECODE D1610), `decode_with_key.py`,
`R16_decryption.txt`. Images are on DECODE (login); not re-transcribed here: the R16 reading rests on TimB's
transcription.

## Remaining gaps

- R16 nomenclator codes 18 and 48 - blocker: open-codes; Meister's Ferrara/Parma values do not fit the contexts; the 1586 table may have moved them
- R16 remaining ~16 unknown pairs - blocker: open-codes; unknowns after the one-digit resync; mostly transcription slips in TimB transcription D1610, images not re-read
- R17 five unknown codes - blocker: open-codes; Meister p. 393 no. 40 reads all five pages except 5 codes

## Escalation

- [x] siblings: R15-R17 all opened; R16 decryption file found to be a copy of R15
- [n/a] clear-pages: no clear pages or interlinear decipherments are reported on R15-R17
- [x] known-keys: Lasry F18 key (D3105), Meister p. 324 no. 2 (Ragazzoni 1583), Meister p. 393 no. 40 (Morosini) tried; all fit
- [x] print: Meister 1906 key tables used; no printed decipherment of R16/R17 sought beyond Meister
- [ ] key-rebuild: not done - fill 18/48 and the R17 codes by alphabetical bracketing and LM context over Morosini-period letters
- [ ] retry: not done - re-read the R16 images for the slip positions, then rerun decode_with_key.py
