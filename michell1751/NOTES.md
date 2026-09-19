# Frederick II to Louis Michell, Berlin, 28 December 1751 (KHA, Prins Willem V inv. 198; DECODE R1957)

Catalogue item 215 (class C, scored by rule). Worked 19 Sept 2026.

**Outcome: found in print.** The text this cipher hides is printed in the *Politische Correspondenz Friedrichs des Grossen*,
vol. 8 (Berlin 1882), no. 5263, pp. 576–577, "Au secrétaire Michell à Londres, Berlin, 28 décembre 1751", edited from the
minute ("Nach dem Concept"). The copy at The Hague is the Dutch interceptors' copy of the letter as sent, in the Prussian
numerical nomenclator; nobody had matched the two until now. The code itself is not rebuilt here beyond the anchors below.

## The document

Two pages (DECODE images P2 = first page, P1 = second page; the DECODE order is reversed). A clear heading and opening, 550
code groups, a clear date line and a copied signature:

- *Au S<sup>r</sup> Michel à Londres.* / *J'ai reçu votre dépêche du 14<sup>e</sup> de ce mois,* 1555 1550 15 144 66 6203 …
- … 6472 403 2179 4004 1437. *A Berlin ce 28 décembre 1751.* *(signé) Féderic.*

Groups run from 2 to 6472, written with a point between them. A few groups are underlined (single, double or triple
strokes: 533, 2102, 206, 211, 362, 4013 …); two corrections are written above the line (759 over a struck group, 5760 over
a struck 5760-like group). Full transcription in `transcription.txt` (ciphertext only in `ct.txt`).

## Why it is PC 5263

1. The clear opening "J'ai reçu votre dépêche du 14 de ce mois" is word for word the opening of no. 5263. The other letter
   to Michell of the same date at The Hague (DECODE R1955, "(1)") opens "Toutes vos dépêches m'ont été bien rendues et la
   dernière est du 14e de ce mois" and uses a different code (fractional groups like 1½, 150½, 660½); it is the letter
   DECODE's note calls "a letter of the same date with different length". R1955 is not this target and is not read here.
2. Length: 550 groups against 438 words of print after the opening, a ratio of 1.26, usual for a nomenclator that spells
   rarer words in syllables.
3. Repeated groups fall in the same order and at the same relative places as repeated words of the print (`anchors.py`,
   the largest positional gap across all occurrences shown):

   | group | word | occurrences | max gap |
   |---|---|---|---|
   | 1064 | Vienne | 4 | 0.022 |
   | 545 | avec | 3 | 0.024 |
   | 4364 | faire | 6 | 0.039 |
   | 4310 | Sardaigne | 3 | 0.039 |
   | 3042 | dessein | 3 | 0.043 |
   | 87 | encore | 3 | 0.017 |

   Other probable equivalents from local context: 169 = *de* (11×), 47 = *roi* (in *le roi de Sardaigne* = 16 140 47 169
   4310, and 3279 47 twice for *le roi* before *d'Angleterre*), 1555 1550 = *et suis*. 1900 fits *Pologne* by position
   (3×, gap 0.046) but 4366 (4×) also sits near *Pologne*; not settled.

## What the letter says (from the print)

Frederick agrees with Michell that the King of Sardinia will join the Austro-Spanish treaty being negotiated at Madrid.
He has learned in secret that Vienna and St Petersburg plan to make Prince Charles of Lorraine the next King of Poland,
and reads Austria's Italian neutrality treaty as freeing its hands for that. Michell is to find out whether London knows
of the plan, or whether Vienna settled it with Russia alone; Frederick suspects the Empress-Queen's new cessions to
Sardinia were made on George II's advice, with Poland as her compensation. Michell is to say how long the present
pacific system of the English ministry will last if George II lives some years more, to report to the King alone,
without copies to the foreign department, and to say whether George II grieved for the Queen of Denmark (d. 19 Dec)
and for the Duke of Cumberland's dangerous illness.

The instruction "report to me alone, without doubles to the department" is why two letters went to Michell that day: the
ministerial one (R1955) and this immediate one, both intercepted and copied in The Hague.

## Open

- The code is not reconstructed; a full alignment of the 550 groups to the print would give most of a Prussian 1751
  nomenclator (numbers up to ~6500, homophones for common words). Worth doing if other Prussian ciphers of 1750–52
  come up.
- R1955 (the ministerial letter) is in a different code; the ministerial rescripts are not in the *Politische
  Correspondenz*, so its plaintext is not in print. Not a catalogue target of its own.

## Sources

- DECODE R1957 (images `IMG_R1957_I13456_P1.png`, `IMG_R1957_I13457_P2.png`) and R1955, fetched with the DECODE cookie;
  images git-ignored.
- *Politische Correspondenz Friedrich's des Grossen*, Bd. 8 (1882), no. 5263, pp. 576–577:
  https://archive.org/details/politischecorres08freduoft

## R1955, the other letter of 28 December 1751: attempted, open

Worked 19 Sept 2026 (catalogue entry for DECODE R1955). Transcribed in full in `transcription_r1955.txt`.

- The Dutch copy is headed *Lettre du Roi de Prusse au Secrétaire Michell du 28 Decemb. 1751* and signed *Féderic*, but
  the *Politische Correspondenz* prints only one letter to Michell of that date (no. 5263 = R1957). This one is the
  ministerial rescript, issued in the King's name and not printed.
- The clear opening is *Toutes vos dépêches m'ont été bien rendues et la dernière est du 14e de ce mois*. Then come 362
  code groups (2 to 5346, most under 3600, with half-groups 1½, 10½, 40½, 150½, 180½, 660½) and the date.
- It shares no code with R1957: only 19 of their distinct groups coincide, and those are chance collisions.
- 295 of the 362 groups are distinct, and the commonest (2, 230) occurs 5 times. That is a large two-part code with
  homophones even for *de* and *que*, so ciphertext-only analysis has nothing to work with. The pair 1487 50 recurs 3×.
- No printed or online decipherment was found. What could open it: the Prussian ministerial code of 1751 (GStA PK, I. HA
  Rep. 96 / Rep. 9 Chiffres), Pierre Lyonet's decipherments for the States General (see K. de Leeuw, *Diplomacy &
  Statecraft* 10, 1999), British decyphers of Michell's correspondence (BL Add MS Newcastle papers; TNA SP 107), or
  other rescripts to Michell in the same code with known content. DECODE R1953 (von der Hellen to the King, 4 Jan 1752,
  KHA inv. 196) was checked the same day and is in a different, smaller code (groups under ~1650, frequent repeats), so it is no sibling of R1955.
