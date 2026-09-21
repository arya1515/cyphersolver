# Louis XIII to Melchior de Sabran and to Brûlart de Léon, 1615–1631 — BnF Baluze 155, fr. 18043, fr. 18044 — NOTES

Status: no write-up

**Verdict: already solved by others.** Catalogue entry 191 (DECODE R2748, R2785, R2786) is covered by published
work: nothing about the text is added here. Entry 192 (Farnese to Sabran, 1637, R2753) is solved too and was removed
alongside it. Session 2026-09-21.

The catalogue grouped three unrelated items because DECODE lists all three with Louis XIII as author:

| record | shelfmark | date | route | DECODE status | who read it |
|---|---|---|---|---|---|
| R2748 | BnF Baluze 155 f. 79–80 | Dijon, 28 Mar 1631 | Louis XIII (countersigned Bouthillier) → Melchior de Sabran, resident in Genoa | Non-decrypted | George Lasry, 2022 |
| R2785 | BnF fr. 18043 f. 83–84 | Poitiers?, 15 Sep 1615 | Louis XIII (countersigned Brûlart de Sillery) → Brûlart de Léon, ambassador in Venice | Partially decrypted | Satoshi Tomokiyo, 2021 |
| R2786 | BnF fr. 18044 f. 109–110 | Paris, 25 Jul 1617 | same | Partially decrypted | Satoshi Tomokiyo, 2021 |

## Sources

- Tomokiyo, "French Ciphers during the Reign of Louis XIII", https://cryptiana.web.fc2.com/code/louisxiii.htm,
  sections "Brûlart de Léon" (the key to the 1615–18 cipher) and "Louis XIII-Sabran Cipher (1631)": "a paragraph in
  cipher, which was solved by George Lasry in 2022". Lasry also found the same cipher in Sabran's own letters to
  Bouthillier, BnF fr. 4134 (1633) and fr. 4135 (1635).
- Tomokiyo, "George Lasry's solutions", https://cryptiana.web.fc2.com/code/GL.htm, "Melchior de Sabran (1631)" and
  "Odoardo Farnese, Duke of Parma (1637)": both "solved as follows", with the keys as images.
- DECODE R2785, R2786 (uploader Tomokiyo, Aug 2021): "Some passages are not deciphered. The uploader could not read
  them with the reconstructed key. They may be partially or totally nulls" (R2785); "At least some of them are
  insignificant (because of cancelling symbols)" (R2786). That is the only residue, and it is probably nulls.

## What was done

1. Fetched the three record views with the shared DECODE cookie; the R2748 images (4, f. 79–80, Gallica scans) into
   `decode/` (git-ignored). f. 79r: a clear letter with two cipher paragraphs of mixed letters, digits and signs
   (c. 20 lines); f. 80 is blank.
2. Fetched louisxiii.htm and GL.htm; both state the solution. The key was not applied to a transcription here, so
   this session did not check the reading itself.

## Not done

A fresh check of Lasry's key on f. 79 and an attempt on Tomokiyo's residue in R2785/R2786. Neither adds much: the
residue is probably nulls, and the owners of both readings have published them.
