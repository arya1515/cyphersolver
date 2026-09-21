# Duke of Sessa → Charles V, February–April 1523 — RAH Salazar A-27 (9/27), DECODE R9660–R9666

Catalogue entry 146 ("Luis Fernández? (Sesa) to unknown recipient, 7 ciphertexts"). Worked 2026-09-21.

## 1. Identification: seven despatches of the Duke of Sessa to Charles V

RAH signatura 9/27 is **Colección Salazar y Castro A-27**. "Luis Fernández" is Luis Fernández de Córdoba, 2nd Duke
of Sessa, imperial ambassador in Rome (not his secretary); every letter is headed *S. C. C. M.*, so the recipient
is the Emperor. "Sesa" is right for the first letter only, which is dated from his duchy. Dates are read from the
letters' own date lines; CSP = Bergenroth, *Calendar of State Papers, Spain* vol. 2 (1866).

| DECODE | ff. | date line | CSP vol. 2 | status |
|---|---|---|---|---|
| R9660 | 141–147 | "En Sesa a xx de hebrero de 1523" | not calendared | cipher, **no decipherment** |
| R9661 | 149–152 | "En Roma, miercoles iiij de março 1523" | no. 534 (from the f. 190 copy, "cipher with contemporary deciphering") | duplicate of CSP 534 |
| R9662 | 308–326 | [12 Apr 1523] | no. 541, "a duplicate of the preceding despatch" | duplicate of CSP 540 |
| R9663 | 327–341 | [11 Apr 1523] | no. 540, ff. 327–343, "autograph in cipher, contemporary deciphering" | in print (calendar) |
| R9664 | 418–422 | "De Roma xxv de abril 1523" | no. 544, ff. 424–430 deciphered | duplicate of CSP 544 |
| R9665 | 437–438 | "De Roma xxvj de abril 1523" | not calendared | short, mostly clear |
| R9666 | 439–441 | "De Roma … abril 1523" | no. 545 (27 Apr, arrest of Cardinal Soderini of Volterra) | clear, "autograph" |

So four of the seven are the letters (or duplicates of letters) whose content Bergenroth calendared in English from
the court's decipherments kept in the same volume (ff. 190, 342–343, 424–430). Those decipherment leaves are not in
the DECODE records, so DECODE marks the ciphertexts "Non-decrypted".

## 2. The cipher is the 1524 Sessa cipher

The same code groups as [sessa1524](../sessa1524/NOTES.md) recur on every page: `gap` que, `sof` de, `suf` de la,
`qib` el, `mus` la, `kef` lo, `dim` se, `cob` si, `ka` le, `coh` Su Santidad, `bas` V.Md., `Jap` papa, `pu3 qes`
franceses, `lip` ningun-, `put` forma, `log` muy, `sis` despues, `njn` ha, the `f~` clear/cipher switch and the
`v db` null opener. The key rebuilt there (about 110 groups plus the letter alphabet, from the court's decipherments
of 1523–25 letters) applies unchanged.

## 3. Sample reading (R9660, uncalendared)

The second cipher paragraph of f. 141r read by eye with the 1524 key: [reading_f141.txt](reading_f141.txt). About
half the tokens resolve at once (*muy despues … a V.Md. de la … forma que el papa … de franceses … a ver a Su
Santidad* [clear: *mas con color*] *… de ningun …* [clear: *disposicion de entender*] *… lo que V.Md. …*).

## 4. Where it stops

Outcome: **identified; four letters already in print (calendared from contemporary decipherments); the two
uncalendared cipher letters (R9660, 20 Feb; R9665, 26 Apr) read in part only.** A full reading of the ~50
cipher-bearing pages is a transcription job with the existing key (the token-tile method of sessa1524), not a
cryptanalytic one; nothing about the cipher remains unknown beyond the groups already open in sessa1524. Next
step if resumed: tokens.py over R9660 ff. 141–147, then read against key_working.md; for the calendared letters,
compare Bergenroth's abstracts with the ciphertext as a check on the key.

Images: `img/` (DECODE, fetched with the saved cookie; RAH permission required, git-ignored). Metadata: `decode/`.

## Remaining gaps
- R9660 (20 Feb 1523, ff. 141-147), all but the sample paragraph of f. 141r - blocker: not-attempted; the key applies unchanged (section 2), only the token-tile transcription was not done
- R9665 (26 Apr 1523, ff. 437-438), its cipher passages - blocker: not-attempted; short and mostly clear, never transcribed
- R9661-R9664 cipher text (CSP 534, 540, 541, 544) - blocker: not-attempted; content known from Bergenroth's calendar of the contemporary decipherments, but the ciphertext was not re-read against the key
- groups open in the sessa1524 key (vo, per, ruc, hay) wherever they occur - blocker: open-codes; inherited residue of sessa1524

## Escalation
- [x] siblings: all seven records R9660-R9666 fetched and dated; the sessa1524 sibling key identified from shared groups
- [ ] clear-pages: not done — fetch the decipherment leaves ff. 190, 342-343, 424-430 of 9/27 (not in these DECODE records) or look for them on neighbouring DECODE records
- [x] known-keys: sessa1524 key_working.md applied; it fits unchanged
- [x] print: Bergenroth CSP Spain vol. 2 matched by folio (nos. 534, 540, 541, 544, 545); R9660 and R9665 not calendared
- [ ] key-rebuild: not done — use the CSP 534/540/544 abstracts against their ciphertext to confirm and extend the key (vo, per, ruc, hay)
- [ ] retry: not done — run tokens.py over R9660 ff. 141-147 and R9665 and read them with sessa1524/key_working.md

Outcome class (21 Sept 2026): **already solved**. The court deciphered these letters at the time and Bergenroth
calendared them; this project read only a sample of R9660, so "read in part" overstated its own share. The gaps above
stay as the to-do list for a full transcription.
