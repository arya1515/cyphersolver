# Henri IV to Landgrave Maurice of Hesse-Kassel — the ciphered passages printed in Rommel 1840

**Status: read (17 Sept 2026).** Every passage that Henri IV's secretaries put in figures and that Rommel printed
undeciphered in *Correspondance inédite de Henri IV avec Maurice-le-Savant* (Paris, 1840) is decoded here with the key
Rommel himself published six years later ("La clef des chiffres…", *Allgemeine Zeitschrift für Geschichte* V, 1846,
pp. 402–403, from Groen van Prinsterer and van der Kemp). Seven letters of the King, 4095 groups: 22 Nov 1602, 12 Jan
1603, 27 Dec 1604, 28 Apr 1605, 22 Dec 1605, 20 May 1606 and 24 Jan 1609. The 22 Dec 1605 and 20 May 1606 letters are
the substance of the target: the King's programme of a common front of the German Protestant princes and the Dutch
against the Spanish-Habsburg design on the Imperial diet, two million livres a year for the States, "la liberté
germanique". The readings are in `letters/READINGS.md`; the raw decodes in `letters/*_decode.txt`.

Catalogue entry 24 (CATALOGUE.md) listed the target as "12 Jan 1603, 28 Dec 1603, 27 Dec 1604 (Rommel pp. 12, 148–189,
388–393)". That list came from Tomokiyo's page and is partly wrong about the pages: the 12 Jan 1603 letter is at
pp. 97–100 (p. 12 is the *Lettres missives* reference), the 28 Dec 1603 letter (pp. 148–160) is printed from a
contemporary decipherment with no figures at all, and pp. 388–393 (24 Jan 1609) hold a single line of figures. The
volume's other ciphered passages (pp. 84, 211–214, 230, 269–272, 307–314) were not on any list.

## 1. The documents

| Letter (Henri IV → Maurice) | Rommel pp. | IA leaves | Cipher | Read before |
|---|---|---|---|---|
| 22 Nov 1602 | 84 | 126 | 13 lines | no |
| 12 Jan 1603 | 99 | 141 | 12 lines | no (Lettres missives vi p. 12 prints it undeciphered) |
| 3 Apr 1604 | 170–175 | 212–217 | 5 pages | yes — Rommel 1846 pp. 403–404 (control, not redone) |
| 27 Dec 1604 | 211–214 | 253–256 | 3 pages | no |
| 28 Apr 1605 | 230 | 272 | 11 lines | no; Rommel's footnote regrets it |
| 22 Dec 1605 | 269–272 | 311–314 | 3 pages | no |
| 20 May 1606 | 307–314 | 349–356 | 6 pages | no |
| 24 Jan 1609 | 391 | 433 | 1 line | no |

Leaf = printed page + 42 in the Internet Archive copy `correspondancein00henr` (Paris, Renouard, 1840; the same scan
Google made). Full-resolution page images were fetched from the IA BookReader (`img/leaf_NNNN.jpg`, 2425 × 4098 px);
the IA hOCR (`src/correspondancein00henr_hocr.html`) was used only to find the pages with dense figures and to date the
letters from their headers. Rommel's key pages are `img/azg5_leaf_0407.jpg`, `0408.jpg` (IA `bub_gb_Zpc1AAAAMAAJ`,
Allg. Zeitschrift f. Geschichte V, 1846, leaves 407–408 = pp. 402–403); his deciphered sample of 3 Apr 1604 follows on
pp. 403–404. Tomokiyo's page (cryptiana …/henryiv.htm, "Cipher between Henry IV and Maurice of Hesse-Cassel") reproduces
the key as an image and notes the original cipher sheet in BnF Clairambault 360 f. 168 (October 1602); not consulted.

Rommel's own position, p. 170 n. 2: "Dans l'espoir qu'il est possible de retrouver la clef des chiffres suivans, nous
les reproduirons ici". By 1846 he had the key from van der Kemp, printed it with one sample letter, and never returned
to the others. The 1840 volume also carries a two-page glossary "Passages déchiffrés" (pp. 419–420) of phrases whose
sense he had guessed from the Landgrave's answers; it agrees with the key.

## 2. The cipher

Two-digit figures. Bare figures are letters (four homophones for the commonest, one for q; no k, w or z); a figure with
a comma after it is one word list (*le, la, leur, que, qui, qu'il, pour, pro, pre, ma, me, mon, ne, ny, nous, on, où, sa,
se, roy, pays/paix…*), with two dots above it a second (*con, ca, car, don, da, di, do, de, en, eulx, faire, faict,
point, elle, fa, forces, troupes, guerre, cour impériale, diète de l'Empire…*), with an overbar a third of names and
titles (*Bouillon, Comte, Conseil, Pape, Empereur, Roi d'Espagne, Roi d'Angleterre, l'Archiduc, Brandebourg,
Brunswick, provinces unies, Protestant, Allemagne, Angleterre, argent, armée, alliés, ambassadeur, au, aux, afin…*).
A dozen symbols stand for *te, tion, tant, tous, tout, tre/tra, grand, va, ville, votre, Hongrie*; one sign doubles the
preceding symbol; one cancels it; several flourishes are nulls.

Rommel's 1846 print is right in every letter value but leaves things the texts had to settle (`key.py` records
each with the passage that fixed it):

* **70** is a fourth homophone for *p*, missing from the table's third row (*presse, perdra, principalement*).
* **83** and **85** in the fourth row sit under the wrong columns in the print: 85 = *m* (*maison, ensemble,
  embrasse*), 83 = *o* (*favorisé*).
* The word lists are typeset with fewer words than figures; the texts give 17, = *la*, 18, and 19, = *le*, 24, =
  *lettre*, 25, = *leur*, 59, = *pays*, 60, = *pour*, 65, = *pro*, 66, = *pre*, 68, = *que*, 83, = *rompre*
  (*cor-rompre*), 86, = *se*; 42: = *don*, 45: = *da*, 46: = *di*, 48: = *do*, 62: = *en*, 64: = *point*, 68: =
  *elle*, 69: = *faire*, 70: = *faict*, 84: = *forces*, 85: = *fa*; 26_ = *Comte*, 28_ = *Conseil*, 31_ = *Pape*,
  33_ = *Empereur*, 35_ = *Roi d'Espagne*, 37_ = *Roi d'Angleterre*, 55_ = *l'administrateur* [de Strasbourg],
  63_ = *duc*.
* **59_** is *le Turc* ("la paix avec [59_]", Dec 1605), not part of *l'administrateur de Strasbourg* as the 1846
  layout suggests; **98_** (blank in 1846) is a prince whose friendship the duke of Lorraine mediated in 1604, not
  identified.
* Glyphs: the tall 4 is *te* or *tion* (the print does not separate them reliably; read by context), the hooked 4 is
  *tant*, 8 with a tail *tous*, 9 with a stroke *tout*, the hatted glyph *va*, ♯ is *tre* far more often than *tra*,
  the "9 +" of the 1840 typesetter is Rommel's doubling sign 94, the three-dot ∵ and the 𝒴-like sign cancel, and the
  ♀-, Ψ- and tt-like flourishes are nulls ("ayant ♀ tt sceu que").

Controls: (a) Rommel's 1846 clear text of 3 Apr 1604 against our decode of the first lines of p. 171 (word for word);
(b) his footnotes on pp. 102–103 (*diète de l'Empire, l'Archiduc, Protestants, ambassadeurs, Empereur, cour impériale*),
his p. 211 note (*le duc de Bouillon*) and the "Passages déchiffrés" glossary; (c) the internal test that every
passage comes out as continuous early-seventeenth-century French with the clear text it interrupts.

## 3. Method

1. Locate: digit density per page in the IA hOCR marks leaves 126, 141, 212–217, 253–256, 272, 311–314, 349–356, 433
   (and the Landgrave's 131, 144–145).
2. Transcribe by eye from 900-px strips of the full-resolution page images (`strips.sh`, `crops/`), recording the
   diacritics the OCR loses: comma, two dots, overbar, and the glyphs. Notation in `ct/*.txt`: `NN` bare, `NN,`
   comma, `NN:` dots, `NN_` overbar, `D` doubling, `X` cancel, `{te} {4} {4c} {8} {9} {tra} {hat} {grand}
   {ville} {votre}` glyphs, `[[…]]` the printed clear text. About 4095 groups.
3. Decode with `key.py` (`python3 run.py ct/pNNN.txt`); read the concatenated output by hand into
   `letters/READINGS.md`. No solver, no segmenter: the passages are short enough to read directly, and the reading
   is what fixed the list alignments above.
4. Not done: the 3 Apr 1604 letter (already in clear in 1846), the Landgrave's own ciphered phrases beyond the two
   used as controls, and the footnote ciphers Rommel printed beside their clear text (pp. 187, 216, 224, 329).

## 4. What the King wrote (summary)

**22 Nov 1602.** He holds back his despatch for the Landgrave's promised advice on the Diet: whether it will meet,
what will be treated, what proposal he should make "pour le public et le particulier de mes alliés", and whether to
send his ambassador on to Saxony and Denmark, with Maurice's counsel on the instruction to give him.

**12 Jan 1603.** Since the Emperor will not appear at the Diet nothing of weight will be treated there, "et
principallement de l'élection d'un roy des Romains". Bouillon has not written a word about the Administrator of
Strasbourg's coming to France nor about the Strasbourg bishopric; the King wants to know how he took the journey and
how far he has embraced the Administrator's cause.

**27 Dec 1604.** Why he has not sent the embassy to the German princes Maurice advised: the "mauvaise intelligence"
he has found among the Protestant princes, and the disgust some of them have given him by believing Bouillon and
favouring his cause "avec moins de respect et considération à ma personne que je n'espérois d'eulx". The Hungarian
revolt is put out but its consequences will spread. He doubts James I's policy of friendship with Spain will wear.
The Dutch have as much courage as ever, are provided for, send deputies to England; a newly-visited prince has given
them hope of arming for them next year, and Maurice should encourage him. The Spaniards forge new plots against him
daily; the comte d'Auvergne, his father-in-law and his sister are in justice for treating with them.

**28 Apr 1605.** The aid he continues to give the United Provinces and Geneva proves his conduct towards those of the
religion inside and outside his kingdom, "pour les notables intérests que j'ay à leur conservation et de la cause
publicque". (Rommel: "Il est à regretter que ces lignes ne soient pas encore déchiffrées.")

**22 Dec 1605.** Mérargues' treason and the attempt on his person came "quasi au mesme temps de la conspiration
d'Angleterre. Il semble aussy qu'ils ayent esté forgés sur mesme enclume"; Spanish ministers everywhere corrupt the
subjects of the princes they reside with; James I has as much cause to complain "toutesfois il le couvre et
dissimule mieulx". The States need to be reinforced by their allies to restore the reputation of their arms; Maurice
and the German princes should send money and troops as some have promised; the King will continue next year the same
assistance as this, "non moindre de deux millions de livres", but without other help the States cannot resist, the
enemy massing money and forces to attack them harder than ever; get the help to them before spring, "car celuy qui
pourra prévenir sa partie en cela en sera grandement avantagé". What does the Emperor intend at the Diet he has
summoned, the Turkish peace, the Hungarian accord, the siege of Brunswick?

**20 May 1606.** The Emperor changes nothing and is ill served, above all in Hungary. The Spaniards will do all they
can to have a King of the Romans elected of the house of Austria wholly at their devotion (Feria sent to the Diet, in
clear); two propositions of great consequence in which all Christendom has no less interest than Germany itself. All
kings and princes jealous of Spain's growth must take counsel together in time to keep the Spaniards from shaping the
Diet's resolutions to their wish; he will contribute whatever depends on him and is fitting, above all when he sees
the others do the like, as his predecessors favoured the ancient allies of the crown "pour la conservation de la
liberté germanique", seeking no advantage but the common cause; Maurice is to tell those he judges worthy and to
advise the King what he can and should do now. James I will not break with Spain over Owen and Baldwin, so much he
wants peace, and the Spaniards ply him with specious offers to make him forget it; their aim is the Netherlands, where
they mean a great effort this year on the Rhine and Frisian side, their army doubled, waiting only for Spinola. The
States, weaker, will be forced onto the defensive, a miserable condition for a republic governed by many heads; all
whose interest is joined to theirs must put their hand to it before their weakness grows, otherwise the remedies come
too late. His earlier request that Maurice favour their suit with the German princes has had little effect. Their
East Indies and Portuguese enterprises prosper, but he doubts that fortune lasts if the land war goes against them and
their people tire of the burden. The Spaniards will exploit the Pope–Venice quarrel; he will try to compose it.

**24 Jan 1609.** The ministers of the Pope and of the King of Spain will do everything to reconcile Matthias with the
Emperor.

## 5. What remains

* Nine groups on p. 213 (the name of the prince who visited the States, "d'un nouveau …"), seven at the top of p. 307,
  the name behind 98_ (p. 211), the run of letters and signs at the top of p. 311 that the 1840 typesetter could not
  set in figures, and single garbled groups here and there (`[?]` in the readings). The 1840 print is itself a
  transcription of the Marburg originals (Hessisches Staatsarchiv Marburg, 4 f Frankreich); only they would settle
  these and confirm 98_ and 19_.
* 55, and 56, are both used where *paix* or *pays* is wanted; the clerk or the print confuses them.
* The tall-4 glyph (*te* / *tion*) is read by context.
* Whether the letters exist in clear anywhere (the Landgrave's chancery decipherments, if kept, would be at Marburg;
  *Lettres missives* prints 12 Jan 1603 and 28 Dec 1603 from Rommel without reading the figures) is not checked
  beyond Tomokiyo's note.

## 6. Files

`key.py` (key with the corrections and their evidence), `run.py` (decode a transcription), `strips.sh` (page
strips), `ct/` (transcriptions with page and line breaks), `letters/*_decode.txt` (raw decodes),
`letters/READINGS.md` (hand readings), `img/` (page images and the 1846 key), `crops/` (strips), `src/` (IA hOCR,
page map, Tomokiyo's page and key image, AZG OCR texts).

Checked: every King's passage transcribed from the page images and decoded; key against Rommel 1846 and his sample; list
alignments against the texts. Not checked: the Marburg originals; the BnF Clairambault 360 key sheet; the Landgrave's
ciphered phrases beyond two pages. User must verify: the historical identifications proposed for 98_ and the unresolved
name on p. 213 are guesses and are marked so.
