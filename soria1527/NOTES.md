# Lope de Soria (Mirandola) to Charles V, 13 Dec 1527 (not 1517) — RAH Salazar 9/17 ff. 31–34, DECODE R9487

Status: no write-up

**Verdict: read at the time. The court's decipherment ("Claro", sections A, B, C) is bound with the letter as
f. 34r.** The date is 1527, not 1517. Catalogue entry 142 is resolved and removed. Checked in one session on
2026-09-21.

## Sources

- DECODE R9487 ("Non-decrypted", 4 images, 13 Dec 1517). The images were fetched with the shared cookie into
  `decode/`. They are git-ignored, and RAH permission is needed to reproduce them.
- Sibling target `soria1523/` (Soria in Genoa, 1523; key B rebuilt there from R9844).

## The document

| image | folio | content |
|---|---|---|
| 1 right | 31r | "Sacra Ces. y Cat. Md." Opens in clear: "Por diversas vias tengo escrito a V. Ces. Md. despues que se perdio Genova ... recibi en Ferrara a los seis de otubre". A: 7 cipher lines (torn at the right), then clear islands about Venice, Ferrara, Lombardy, the Pope and cardinals, "lo perdido ... temor que todos tiene", and more cipher lines at the foot |
| 2/3 left | 31v | 9 intact cipher lines, then clear: the galleys of France and Venice, Sicily, the Duke of Ferrara having entered the league, "restituir el estado a Federico", and cipher at the foot |
| 2/3 right | 32r–33r | clear: five thousand Germans, Bologna; waiting at Mirandola with the Duke of Genoa(?) for the Emperor's orders. On 33r: 5 cipher lines (C), clear "todos los enemigos se retiraron de cabe Milan ... Antonio de Leyva y corre por do quiere", then more cipher (torn) |
| 4 left | 33v | clear: "el papa ... ya era ido el papa a Orvieto", two Spanish and two German hostages, "el papa en su libertad enteramente", Antonio de Leyva |
| 4 right | 34r | docket "Al Rey. De Lope de Soria de la Mirandula xiij de deziembre [1]527"; **decipherment** "Claro" A, B, C in a secretary's hand. Transcribed in `claro.md` |

## Date: 1527

The pencilled "1517. 13. de Dec." at the head of f. 31r, which DECODE copied, is a misreading. The content is that of
Dec 1527. Genoa has been lost (to the French and Andrea Doria, Aug 1527). Clement VII has left Rome for Orvieto (7–8
Dec 1527) and is "en su libertad". Antonio de Leyva holds the field around Milan. Bourbon's jewels are pawned at Genoa
(Bourbon died at Rome in May 1527). Federico is to be restored (Gonzaga of Bozzolo?). The docket on f. 34r ends in
"…27".

## Checking the decipherment against the cipher

The cipher is the three-letter code plus homophonic letters of Soria's 1523 key B (`soria1523/keyB.md`), used here
four years earlier.

- C (f. 33r, the 5 intact lines): `4∞Lc4zryqr zof xab` = *matrimonio con Francia* (4=m/i, ∞=a, L=t, c=r, r=o, y=n,
  zof=con, xab=Francia); `si tef` = *por no*; `y∞τ7ε∞c zof` = *navegar con*; `sub` = *que*. The claro has "fazer
  matrimonio con Francia ... por no recebir daño pues son gentes que saben navegar con todos vientos".
- A (f. 31r): `zrLqL∞yh∞ zog` = *[q]uitança[s] de*, and the claro has "les haya fecho quitanças de toda la suma".

So f. 34r is the decipherment of this letter's cipher.

## Gaps

- Claro B and the start of C are torn (see `claro.md`). The f. 31v cipher block (9 lines) is intact. Decoding it with
  key B would fill the claro's gaps if it is section B. Not attempted in this session: the sign-by-sign transcription
  is not done. Blocker: not-attempted.
- The last cipher lines on f. 31r and f. 33r are torn and faded.

## Why no write-up

The letter was read at the time, and its decipherment is bound with it. The new results are identifying f. 34r as
that decipherment and correcting the date to 1527. Per CLAUDE.md this is `Status: no write-up`. The DECODE date and
status correction are queued in `decode_updates/queue.json`.
