# Robert Fagel to William V, The Hague, 18 June 1804 (DECODE R2238)

Status: in progress

Koninklijk Huisarchief, The Hague, A31 Prins Willem V, inv. nr. 337. DECODE R2238 (non-decrypted, nomenclator,
numerical, 3 pp., login). Robert Fagel (1771-1856), William V's adjutant in 1793-94, writes from The Hague to the
exiled Stadholder. Outcome so far: **attempted, open**. The key has not been found.

## The letter

DECODE numbers the pages back to front: P2 is the first page, P3 the second (the cipher), P1 the closing page with
"Je suis avec respect, Monseigneur, de Votre Altesse Sérénissime le très humble et très obéissant serviteur,
R. Fagel", dated "La Haye 18 Juin 1804".

Clear context (P2): a letter from the Hereditary Prince dated the 6th of this month announces V.A.S.'s departure
"as fixed" (destination read as Brunswick or Berlin, uncertain) at the end of next week. Gaebel arrived here on the
9th and could leave only on Monday the 13th. After conferring with Monsieur de Cesar, the Commissaires kept him
so that Monsieur d'Yvoy could be briefed. "Messrs les Commissaires de la maison" sent a note to Monsieur Hubrecht
(name uncertain) on Monday, hoping for a meeting. He replied by word of mouth that he hoped to speak with
Monsieur Damen within a couple of days. P3 opens in clear: "Dès lors il n'a plus fait entendre parler de lui, et
l'on ne tardera pas à connaître la déclaration, sur laquelle les instructions de V. A. S. et celles du ministre du
Roi sont parfaitement d'accord." The cipher follows. The subject is the 1804 settlement of the House of Orange's
property with the Batavian Republic.

## The cipher

`ciphertext.txt`: 128 figure groups (99 distinct), 2 to 4 digits, the highest 2510. Commas separate words. Dots
join groups inside one word, which points to syllable groups. Clear endings are appended to some groups (503t, 788e,
281s, 1241t, 687e, 248e). The words "&", "car" and "que" are in clear, and there is one boxed interlinear insertion.
Small superscript marks (c, 3, 6, 9, fractions) follow some groups, and their reading is uncertain. The arcs over
groups containing 6 or 8 are the looped digit tops, not marks.

## Keys tried (19 Sept 2026), all ruled out

- **Grand Chiffre du Stadhouder** (DECODE R1024, KHA A29 PWIV 301 B, 1782, J. F. Euler; de Leeuw, Cryptologia 25,
  2001). The DECODE key transcription (DOC_R1024_D2881, 4,732 entries, 51-5000; the 1-50 and 1201-1250 blocks are
  not transcribed) gives nonsense on direct lookup ("presque, dio, savoir, presenter, accession.?.cla.cahos ...").
  The optional additive Tableau (rows T-Dd, 17 values each, from de Leeuw's DOC_R1024_D1785) was tried from all
  187 row starts and 187 column starts. None gives French. The letter also carries no start letter at its head,
  which the Grand Chiffre instructions require when the Tableau is used.
- **R2240** (KHA PWV inv. 339, "cipherkey 1793 or later"). This key has letter homophones 1-100 and names and
  places 100-6006. Our dot-joined words are not runs of small numbers, so it does not fit.
- **R1035** (1803 Russia legation codebook) and **R1891** (1798 Schimmelpenninck codebook) are Dutch-language
  codes. The letter's plaintext is French.
- **Siblings in inv. 337**: R2236, R2237 (decrypted) and R2239 (the Hereditary Prince to William V, 1795-96). These
  use a small-number system with fraction marks, a different system from Fagel's.

## Next

The code has about 2,500 groups, and a 128-group text cannot yield it without a key. The key is most likely among
the KHA papers of William V's exile or the Fagel family papers (NA 1.10.29, which DECODE indexes for keys of
1680-1793: R2792-R2852; the first pages of the eleven undated sets R2842-R2852 were sampled on 19 Sept and are covers or indexes, the contents not yet examined). Checking those key records for a French code of 1795-1806 whose range
covers 2510 is the next step.

DECODE images are git-ignored (`img/`, `key*/`, `decode/`, `lines/`). Only derived text is committed.
