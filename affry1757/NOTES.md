# d'Affry (The Hague) to Rouillé / Bernis, 1757-58: intercepted code letters

Status: read in part (0.86 of groups measured 21 Sept 2026; R1071 unread, R1072 weak; write-up affry1757.html, 19 Sept 2026)

KHA The Hague, Prins Willem V, inv.nr. 192. DECODE R1052-R1076, R2067 (catalogue: d'Affry, 11 unsolved records).
Images (git-ignored, `img/`) and DECODE digit transcriptions (`decode/DOC_*.txt`) fetched 19 Sept 2026 with the
bordeaux cookie. `parse.py` reads the DOC files; `cipher_A.txt`, `cipher_B.txt`, `cipher_C.txt` hold the groups.

## Prior work

- DECODE marks R1052, R1053, R1062, R1063, R1066, R1069, R1075 "solved by Dutch codebreakers, solution on separate
  sheets". The sheets **are** among the DECODE images, as clear-text pages marked "gelcp[?] D'A. à R." with number
  and date (first missed here: they read like ordinary clear letters). Lyonet's decipherment pages: R1052 5506,
  R1053 5507-08, R1062 (see align/), R1063 (see align/), R1065 5566-68 + 5572 (cipher in numbered paragraphs P:1..),
  R1066 5578 (+5575), R1069 5589 + 5586, R1075 5604-05. Transcribed into `plain/R*.txt`.
- De Leeuw, *Cryptology and statecraft in the Dutch Republic* (thesis, UvA 2000), ch. on the Seven Years' War:
  Lyonet broke d'Affry's first code by June 1756, then "two more French ones, belonging to Bonnac and D'Affry";
  the French code used July 1757 - December 1758 "is not mentioned by Lyonet and Croiset, but was nevertheless
  solved"; d'Affry's code to Choiseul from Dec 1758 broken later.
- The contemporary decipherments survive as Nationaal Archief 1.01.50 (Stadhouderlijke Secretarie) inv. 221
  (d'Affry to R[ouillé], Dec 1755 - Jun 1757) and inv. 223 (d'Affry to B., Jul 1757 - Dec 1758), "grouped by the
  cipher used". Not digitised (empty scan ids, checked 19 Sept 2026).
- Bussemaker (ed.), 'Uittreksels uit de brieven van D'Affry aan de Fransche regeering (Dec 1755 - Mei 1762)',
  BMHG 27 (1906), DBNL `_bij005190601_01_0008`: Fruin's extracts from those decipherments, Dutch summaries with
  verbatim French sentences. Entries for 7 Jan, 1 Feb, 1 Apr, 19 Jul, 22 Jul 1757 match letters here.
  So the content of these letters was read in 1757 and summarised in print in 1906; the full text is not printed.

## Codes (group-frequency cosine between letters)

Revised: the Jan-Feb ("A") and Apr-Jul ("B") letters share their common values (de 219/1018/1138, la 583/382, que 197,
M 196, vous 569, il 1088, me 208, ne 134, faire 847, ma 6, ti 588, n 580...); the cosine split reflects homophone
habits, not two codes. `cipher_U.txt` holds both; `key_U.json` is the joint key. R1071 (C) is different.

Original split:

- **A** (Jan-Feb 1757, to Rouillé): R1052, 1053, 1062-1065, 1072, 1073, 1075, 1076. 5,011 groups, 777 distinct.
- **B** (17 Feb? / Apr 1757 - Jan 1758, to R. then "A à B" = Bernis): R1066, 1067, 1068, 1069, 1054, 1070, 1074
  (+ R2067, no transcription). 3,512 groups, 743 distinct. R1054's "to Bonnac" is DECODE reading "B"; the
  letter is Bussemaker's 19 July 1757 extract.
- **C**: R1071 (to Choiseul, 7 Aug 1757), 761 groups, unlike both.

Groups run 1-~1200; a word-and-syllable nomenclator (two-part or mostly unordered: frequent groups barely
cluster numerically).

## Code B: crib from Bussemaker's 19 July 1757 extract on R1054

The verbatim passage "Zoo het eerste het geval was, il me paroit qu'il seroit essentiel ... de la sagesse de leurs
règles" lies in R1054 positions ~200-370. Anchor: `800 698` (des précautions) at 264 and 277, 12 words apart in
the crib. See `key_B.json` for the growing key.

## Result (19 Sept 2026): key rebuilt from Lyonet's decipherments, the unread letters read

**Key.** Eight letters carry Lyonet's clear copy among the DECODE images (R1052, R1053, R1062, R1063, R1065, R1066,
R1069, R1075). Each clear copy was transcribed from the images (`plain/`) and aligned group by group with its
cipher (`align/*.tsv`, graded H/M/?; sub-agents, one letter each, cross-checked against each other). `merge.py`
votes `key_M.json` (651 groups; 56 left ambiguous in `amb_M.json`; `overrides.json` for corrections found in
reading). One code serves Jan 1757 - Jan 1758 (to Rouillé, then Bernis); only R1071 (to Stainville/Choiseul,
Vienna, 4/7 Aug 1757) is in a different code and stays unread.

**Readings** (`read/R*.md`, inferred values with evidence in `read/R*_new.tsv`, {braces} = inferred, [n] = open):

| Record | Date, no. | Read | Content |
|---|---|---|---|
| R1072 | 6 Jan 1757, 123 | ~65% in sense | "the Italian", a spy, offers to go to England and report on forces, cabinet, campaign plans; wants pay and a pension |
| R1076 | 7 Jan 1757, 124 | ~90% | convoy and escort after the storm; navy without land increase; herring; talk in Amsterdam |
| R1073 | 25 Jan 1757, 133 | ~90% | false rumour of a memorial on the augmentation; talk with the Grand Pensionary |
| R1064 | 1 Feb 1757, 136 | ~95% | States of Holland adjourned to the 20th; taxes for the augmentation; herring favour; spies (Quintin, La Combe) |
| R1067 | 1 Apr 1757, 161 | ~88% | Steyn embarrassed; the Gouvernante: "faut-il que ce soit moi qui favorise les moyens de faire du mal à mon père?"; Maastricht convoy; Wassenaer |
| R1068 | 26 Apr 1757, 172 | 56/60 groups | courier Vienna-London; Colloredo to d'Arenberg |
| R1054 | 19 Jul 1757 (to B.) | ~92% | Gouvernante's journey; ask for a declaration of the States-General; précautions of d'Estrées |
| R1070 | 22 Jul 1757, 210 (to B.) | ~95% | Gouvernante to speak to the States of Holland; Ostend and Nieuport; trade to Amsterdam and Rotterdam |
| R1074 | 17 Jan 1758, 283 | ~90% | French loan attempted in London; Macdonald (Bulkeley regiment) suspected |
| R2067 | 17 Jan 1758, 283 (to B.) | ~91% | cover letter to the loan extract: money operations in England useless; Englishmen and Spaniards passing; transcribed from the images here |
| R1071 | 4/7 Aug 1757 (to Stainville) | not read | different code |

**Checks.** Bussemaker's verbatim sentences recur group for group: 19 Jul (R1054, groups 145-351, four small
differences where Fruin abridged), 22 Jul (R1070), 1 Apr Wassenaer sentence (R1067 piece 7); Coquelle (1904)
quotes the Gouvernante's words to d'Affry from the Paris original, found in R1067. Bussemaker's Dutch summaries
of 7 Jan, 1 Feb, 1 Apr, 19 Jul and 22 Jul agree point by point.

**DECODE transcription slips** found on the way: in two hands a looped 8 was read as 0 (R1072, R1075, also R1064,
R1067: 056=856, 099=899 ...); groups run together (58291 = 582 91) or dropped; superscript corrections (8^578).
`view.py` splits merged groups; the reading agents re-parsed from the DOC files where needed.

**Open:** ~5-12% of groups per letter (listed as [n] in each reading), the weak stretches of R1072, R1071 entirely.

## Remaining gaps

- R1071 (to Stainville/Choiseul, 4/7 Aug 1757), 761 groups - blocker: no-key-material; a different code; no decipherment among the images and the Nationaal Archief 1.01.50 inv. 221/223 decipherments are not digitised
- R1072 weak stretches (~65-78% in sense) - blocker: open-codes; groups not in key_M and unresolved by context; listed as [n] in read/R1072.md
- ~5-12% of groups per undeciphered letter - blocker: open-codes; single groups with no Lyonet alignment and no context value, listed as [n] in each reading

## Escalation

- [x] siblings: all R1052-R1076 and R2067 opened; eight Lyonet decipherments found among the images
- [x] clear-pages: the "clear" pages are Lyonet's decipherments, transcribed into plain/
- [ ] known-keys: other d'Affry codes (1755-56, and to Choiseul from Dec 1758) not sought for R1071
- [x] print: De Leeuw 2000, Bussemaker 1906, Coquelle 1904 checked
- [x] key-rebuild: key_M.json voted from the alignments, inferred values in read/R*_new.tsv
- [ ] retry: not recorded - no second pass over the [n] groups with the extended key
