# Charles of Egmond to the grand master of France

Status: in progress — full candidate reading; final consistency review and site write-up pending.

Source: BnF français 3015, no. 8, folio 16. [Body, Gallica view 27](https://gallica.bnf.fr/ark:/12148/btv1b9060086g/f27.item); [address, view 28](https://gallica.bnf.fr/ark:/12148/btv1b9060086g/f28.item).

## Diplomatic working reading

All values are inferred (I), not taken from an archived key or known plaintext.
Doubtful glyph identifications are M as detailed below. Spaces and capitalization
are editorial. Braces contain raised insertions. Square brackets mark the
ink-heavy sign interpreted as u. Peculiar spellings and repetitions are retained.
The word-divided lines are checked automatically against the token replay.

01. Mon cousin pource que sueis aduerti que donnes faueur
02. a uous possible au bien de mes affaires uous ai bien
03. uouellu faire la presente pour uous prier uoulloir
04. continuer pour laduenir cosidere lextreme necessite
05. la ou pour le present me trouue pour auir obei aulc
06. commandemens du roi lequel est cause que suis entre en
07. ceste guerre comme plus amplement {entenderes} par le commandeur
08. de sainct Iehan mon ambassadeur auquel ai donne charge
09. uous communiquer le tout il uous plaira lui
10. donner assistence telle quil lui sera besoing
11. et le croire en ce quil uous dira de par moi en ce
12. ce faisant me obligeres de plus en plus a uous
13. ce scet nostre seigneur auquel apres
14. mestre recommande a uostre bonne grace prie
15. uous auoir en {sa} garde darnhem ce dih[u]itieme de
16. iuillet

Clear closing, with the abbreviation expanded: “Le tout v[ost]re bon cousin”.
Signature: CHARLES.

Address: “A mon bon cousin / Monsieur le grant maistre / de France”.

## Meaning in modern English

My cousin, having been informed that you give all possible support to my affairs,
I wished to write and ask you to continue in the future, considering the extreme
need in which I now find myself after obeying certain commands of the king,
which caused me to enter this war. You will learn more fully from the commander
of Saint John, my ambassador, whom I have instructed to communicate everything
to you. Please give him such assistance as he needs and believe what he tells
you on my behalf. By doing this you will oblige me increasingly to you, as our
Lord knows. Having commended myself to your good grace, I pray that he keep you
in his protection. From Arnhem, this eighteenth day of July [year absent].

This translates the apparent sense; it is not a replacement for the literal
reading above. “Certain” interprets the unexpanded `aulc`; 18 July interprets
`dih[u]itieme`. No recipient's personal name or year is supplied in the cipher.

## Residual uncertainties and limits

- **M, line 4:** the small cross assigned EX/x in `lextreme` is supported by
  context; its visual distinction from plain plus/g needs a final inventory check.
- **M, line 15:** the u in `dih[u]itieme` is ink-heavy, with its stem visible.
  The apparent date is 18 July. No year is present in the recovered date clause.
- **M, insertion 7:** the small e after t overlaps a descender from the line above.
  The ten-sign sequence reads `entenderes` and the caret places it after `amplement`.
- **I/M, throughout:** several m/n zigzags are distinguished partly by context;
  the early provisional labels conflated them. Their occurrence audit is recorded
  in `body_audit.json`, but this does not constitute an independent decipherment.
- The raw forms `sueis`, `uouellu`, `cosidere`, `auir`, `aulc` and the repetition
  `en ce / ce faisant` have not been silently repaired. They may reflect spelling,
  enciphering slips, abbreviations, or residual glyph errors. Re-inspection is
  required before choosing between those explanations.
- The title identifies the recipient as grand master of France. The actual person
  and the ambassador's personal name remain unestablished. “Commander of Saint
  John” is a title in the letter, not a recovered personal name.
- The separate clear letter at folio 24, dated 3 April 1537, is contextual evidence
  only. It is not a matching clear copy and cannot supply this letter's year.

## Reproduction

Run `python egmond/decode_audited.py`. It reads explicit shape labels and the
inferred key, replays both raised insertions at checked token anchors, and writes
`complete_raw_reading.txt`. The original failed probes and earlier drafts remain
available as the research trail; they are not alternate accepted plaintexts.

The corrected body plus insertions measures 726 labelled signs, 27 label names.
These are transcription statistics: A and + are variants, A_blotted is an
uncertain instance, and DD/CE each denote one compound sign. Do not equate the
27 labels with 27 historically distinct cipher characters.
