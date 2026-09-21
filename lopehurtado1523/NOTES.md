# Lope Hurtado de Mendoza (Rome) to Charles V, 1523–24 — catalogue no. 148

Status: read in part

RAH Salazar A-28 (Signatura 9/28) and A-30 (9/30). DECODE R9667, R9683, R9695, R9846, R9866, R9867,
R9868, R9869. All eight marked "Non-decrypted". Opened 2026-09-21.

The catalogue entry calls this "Jun 1523, unknown recipient, 8 ciphertexts". Neither label is right: the
eight records are **five letters to the Emperor and at least two to a "muy Illustre señor"**, running from
May 1523 to March 1524, in two different volumes.

## The eight records

| rec | folios | date (from the document) | to | state |
|---|---|---|---|---|
| R9667 | 9/28 ff. 6-9 | Rome, 5 May 1523 | Emperor | clear with cipher runs; the mirrored "Claro" leaf beside it is the **Abbot of Nájera's** clear of 2 May 1523, not Hurtado's; CSP Spain ii **548** abstracts it from a contemporary deciphering not among the images |
| R9683 | 9/28 f. 171 | Rome, 10 June 1523 | Emperor | clear with 8 cipher lines; no decipherment; not in CSP |
| R9695 | 9/28 ff. 339-340 | Rome, viij **July** 1523 (DECODE: June) | Emperor | autograph draft, clear with cipher lines, much struck through; not in CSP |
| R9846 | 9/30 ff. 130-133 | Rome, 3 and 5 Feb 1524 | Emperor | almost all cipher (ff. 130r-132v); **clear version on f. 133r** (first third imaged); CSP Spain ii **617** |
| R9866 | 9/30 ff. 285-286 | Rome, 28 Feb 1524 | Grand Chancellor Gattinara | half cipher; no decipherment; not in CSP |
| R9867 | 9/30 f. 351 | Rome, 4 Jan 1524 (date spelled in cipher) | Emperor | wholly cipher, 30 lines; not in CSP |
| R9868 | 9/30 ff. 430-431 | Rome, 20 Mar 1524 | Grand Chancellor Gattinara | half cipher; not in CSP |
| R9869 | 9/30 ff. 444-445 | Rome, 28 Mar 1524 | Emperor | half cipher; not in CSP |

The CSP check used Bergenroth's CSP Spain vol. 2, pp. 547–709 (fetched to `csp/`), grepping "Salazar. A. 28/30. f."
for each folio. R9667 = no. 548 (A. 28 ff. 6-9) and R9846 = no. 617 (A. 30 ff. 130-133). The other six folios are not
calendared.

## Cipher

It is the same system as the 1522 letters (`lopehurtado/`, catalogue 144): latin-trigram codes (`ton` que, `zar` de,
`xul` lo, `rab` vuestra magestad, `taf` papa, `yub`/`ɣub` el, `tu` no, `tod` otro, `teg` para, `sed`, `xug` la) plus a
letter alphabet of cursive signs. The 1522 key is the starting point.

## The key from R9846's clear (the way in)

R9846 f. 133r is the clerk's clear of the first third of the 5 Feb 1524 letter. Aligned clause for clause
against ff. 130r-130v (38 cipher lines): `key_1524.tsv`, 105 values (65 confirmed), plus `key_1524_additions.tsv`
and `key_1523_additions.tsv`. Most of the homophonic letter alphabet falls out of exact-count spelled runs
(`r9846_alignment.md`). 1522 values n/e/a/o re-confirmed; 25 of the 1522 codes re-confirmed.
**The key moved between 1522 and 1524:** `tef` is *paz* in 1522 but *nec-* (necesidad, necesario) three times in 1524;
`L` is i in 1522 but r here.

R9667's "Claro" leaf is a trap: mirrored, docketed "Del abbad de Najera a dos de mayo" - the clear of the Abbot
of Nájera's letter, bound beside Hurtado's. No crib for R9667.

## What was read (all "read in part"; coverage = tokens with a value, an upper bound)

| rec | cipher tokens valued | reads as Spanish | gist |
|---|---|---|---|
| R9667 | fragments | little | benefices for the Pope's servants (list on f. 7); CSP 548 has the content |
| R9683 | 67/91 | fragments | clear: Pope well disposed since Volterra's arrest; restore benefices of the camarero and Francisco |
| R9695 | 184/249 | no | clear: rumoured poisoning, Duke of Camarino's men in prison, naturalisations for the Pope's intimates |
| R9846 | crib third read; rest per CSP 617 | first third | Beaurain's coming; the Pope wants France ruined or a truce |
| R9867 | 418/467 | ~60% | Beaurain has left the Pope content; the Emperor must not show need of money |
| R9866 | 561/649 | a quarter to a third | to Gattinara: the French mean to stay this side of the Alps; the writer's unpaid salary |
| R9868 | 328/353 | f. 430r mostly | to Gattinara: Capua gone, all business hangs on the Datary, who must be satisfied |
| R9869 | 310/339 | about two thirds | Pope's money offer via Beaurain; Florence undecided; the archbishop of Capua to be well received |

Readings in `read_r*.md`. Where it stops: about 30 code groups (`xun`, `xor`, `zad`, `ʃal`, `ʃub`, `rub` vs `yub`...),
and look-alike signs (∂ vs barred ∂, two- vs three-bar crosses, barred m = f or c) needing better images than DECODE's.
The unimaged f. 133v (rest of R9846's clear) would give more; RAH Biblioteca Digital, Salazar A-30.
