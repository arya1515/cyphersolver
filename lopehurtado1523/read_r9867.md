# R9867 — f. 351r, wholly cipher (read in part)

**Source:** img/IMG_R9867_I45990_P.jpg, right page = f.351r (25 lines of cipher, a flourish at the end; no clear text).
**Left page (f.350v):** the back of a different, folded letter with two seal patches; its address is too faded to read
(only "…Magestad…" and a word like "Granada"? guessed, not read). A projecting tab from another leaf at the gutter
reads "1524 en henero" (I first misread "en Venecia"; corrected from trans_R9867.md) — the endorsement, agreeing with the date spelled in the cipher. A small "Sa" and a flourish at the edge belong to f.351.
**Sender/date from the cipher itself:** the last line spells out, letter by letter,
`zar 8 z 8 ʇʇ m | ε m ⊃ 8 3 φ ʇʇ b ß 9 m` = "de enero — Lope Hurtado", preceded by `zar tuf ß q? φ 7 b ʇʇ y`
= "de <Roma> a quatro". So: **Lope Hurtado, Rome, 4 January [1524]** (year from the mention of mussiur de Beure,
cf. R9846 Feb 1524; not stated). Addressee: the Emperor ("vuestra magestad" passim).

Transcription: `r9867_cipher.txt` (token by token, same symbols as r9846_cipher.txt).

## Mechanical decode (key_1524.tsv + key_1523_additions.tsv; `<>` = probable, `?tok` = unknown)
```
l01 m u/v s i/j u r de b e u/v r e de ?ʃ r al papa con
l02 t e n t o de lo que ?xil r dicho de <parte> de vuestra magestad
l03 y de la manera que a <t> e n i/j d o <en> ?ta a r
l04 y ?zur m i/j s m o lo que al n lo s que esta n c a
l05 r e Sad que ?zur d o ?xed ?zef ?ʃob esta u/v a n ?tul
l06 ?ʃr que da n con es n c a de ?tuʃʇʇ m e r c e d
l07 de vuestra magestad la que no t e n i/j a n si se ?xil s r
l08 de <hazer> a p r o u e c <h> a r a mas que se a
l09 ?zer que ?co e b r u/v e el arçobispo con el ?tol vuestra magestad no
l10 de u/v e <mo> s t a r <nec-> e s i/j d a d <por> que ?rub e m o s
l11 ?ʃug que ?zic ?ʃon p o c o para s a c a r dinero s y que esta
l12 r ?ʃub n ?yer a p r o u/v e c <h> a r a ?xer para que lo s
l13 b u s c a s e n lo s que ?zet ?yiz que no lo s t i/j e
l14 n e n si lo s ?yun e s que da n en Italia ?ʃec lo
l15 de <aca> esta r a con ?ʃ m o ?tel m u/v s i/j u r de r e
l16 u r e ?zad a p ?ʃ r mas ?xal r vuestra magestad ?zm <Roma> lo de
l17 ?zic es c u/v s a d o se r a al a r b a r ?xir ?tel de
l18 ?ʃal ?ʃon ?zef ?zad a d o y t i/j e n e mas ?ʒφ i/j d a
l19 d o r la s c o s a s de vuestra magestad que se p u/v e d e <dizi-> r
l20 de lo que su c e d i/j e r e ?zic r de la n t e <ha> ha-
l21 r e lo que su e lo ?zm vuestra magestad m e lo r m a n d a d o
l22 al a ?tol su p l i/j c o m a n d e p r o u/v e e r ?zm <ha> se a
l23 p a r a d o de lo que ?zub se m e d e u/v e <por> que ?zic no
l24 ?℮ e c i/j <t> a ?ʃφ r u/v e n c a y da n o de <Roma> a ?q? u/v a t r o
l25 de e n e r o l o p e <h> u/v r t a d o
coverage 418/467 = 90%
```
Coverage is token-level (a decoded token may still be a single letter of a word whose other letters are unknown);
18 distinct code groups remain unknown: xil(+c), zur, xed, zef, ʃob, tul, ʃr, tuʃʇʇ, co, tol, rub, ʃug, zic, ʃon, ʃub,
yer, xer, zet, yiz, ʃec, zad, xal, zm, xir, ʃal, ʒφ, zub, ʃφ, ℮, ʃ(+ʇʇ).
(xil = "le" in the 1522 key: `xil c` = les fits l07 "si se les", l02 "lo que le(s) ha dicho" — not added, 1522 value.)

## Best Spanish reading (gaps […])
Mussiur de Beure […] al papa contento de lo que le[s] ha dicho de parte de V. Md., y de la manera que ha tenido en […]
y […] mismo lo que […], los que estan […] Sad […] que […] estavan […] que dan con es[…] de […] merced de V. Md.
la que no tenian. Si se les […] de hazer, aprovechara mas que se a[…] que […] el arçobispo con el […] V. Md. no deve
mostrar necesidad, porque […]emos […] que […] poco para sacar dineros, y que esta[…] sin […] aprovechara […] para que
los buscasen los que […] que no los tienen. Si los fran[ceses?]… que dan en Italia […] lo de aca estara con […].
Pues mussiur de Beure […] mas […] V. Md. […] Roma lo de […] es escusado ser […]. […] tiene mas […] las cosas de
V. Md. que se puede dezir de lo que sucediere […] hare lo que […] V. Md. me lo [ha] mandado […] a[…] suplico mande
proveer […] de lo que se me deve, porque […] no […] y […]. De Roma a quatro de enero. Lope Hurtado.

## English gist
Monsieur de Beaurain [has left?] the Pope content with what he told him on the Emperor's behalf; the Emperor must not
show need [of money]; little can be raised; mention of the archbishop [of Capua?], of the French in Italy, and of
money being sought from those who do not have it. Closes asking the Emperor to provide for what is owed to the writer.
Read in part: the frame is clear but most clauses turn on unknown code groups.

## Coverage
418 / 467 tokens decoded (90 %), of which a large share are single letters; by words of plaintext perhaps ~60 %.

## Cross-check with trans_R9867.md (other session, read-only)
- They read the endorsement as "1524 en henero" and say the text has "no date line, paraph only". The cipher's last two
  lines in fact spell the date and signature letter by letter: "…de <Roma> a quatro de enero — Lope Hurtado"
  (ε m ⊃ 8 3 φ ʇʇ b ß 9 m: l-o-p-e-h-u-r-t-a-d-o, eleven signs, all but 3 = h already in the key). So: 4 Jan 1524.
- Their token count ~480 vs my 467; their frequent-group list (ton, zar, xul, rab, ɣof, ɣub, zil, teg, tef, zun, ʃub,
  ʃed, zic) matches mine. Line-by-line differences not audited beyond this.
