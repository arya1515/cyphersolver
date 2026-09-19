# Solved targets, ranked

Compiled 2026-09-16 from the Solved and Read rows of [README.md](README.md) and [TARGETS.md](TARGETS.md).
Where the tracker ranks open targets by *feasibility*, this list ranks the finished ones by what they were
worth: how hard the cipher was, how much research it took, what the text says, whether anyone had read it
before, how prominent the item was on the source lists, and how solid the reading is.

All scores are judgments on a 1–5 scale, not measurements. The composite is a weighted mean and the weights
are stated; change them and the order changes. Entries marked * carry an inference that the notes do not
verify (see the last section).

## Axes and weights

| Axis | Weight | 1 | 5 |
|---|---|---|---|
| **D** Cryptanalytic difficulty | 25 % | Key or table already in print; decoding only | Ciphertext-only recovery of an unknown system from images, no crib |
| **H** Historical weight of the content | 25 % | Private or trivial matter | Decision of state, or content that changes a known account |
| **N** Novelty | 20 % | Plaintext already in print before this work | No reading anywhere before this work* |
| **R** Research and archival effort | 10 % | Transcription supplied; one source | Images fetched and transcribed, siblings hunted across volumes, catalogues corrected |
| **F** Profile on the source lists | 10 % | Not on any list | Schmeh Top 50 entry with a live public dispute |
| **V** Completeness and verification | 10 % | Partial reading, controls weak | Read end to end, controls or a printed clear text agree |

## Composite ranking

| # | Target | Date | D | H | N | R | F | V | Score | Why it sits here |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Henry of Navarre → Ségur**, 500 Colbert 401 ff. 233, 239, 288v (+ f. 366, f. 333) | 1585–86 | 5 | 4 | 5 | 5 | 2 | 4 | **4.35** | The only target solved from the manuscript images with no transcription and no key family known in advance: 461 figures transcribed from Gallica, the syllabary found by the mod-5 test, a structured annealer at 97 % on a matched control, then the whole 440-canvas volume swept. Content is the German levy of 1585–86 and Casimir; the sender is corrected from Henry III to Navarre. Word-signs partly open |
| 2 | **Swatow telegram to Sun Yat-sen**, JACAR B03050738800 | 1916 | 4 | 4 | 5 | 3 | 2 | 4 | **3.90** | Code condenser over the Chinese telegraph code recovered by brute force over 57,600 keys with a character language model. Reports the Chaozhou rising and the fall of Swatow in the 1916 anti-Yuan campaign; 41 of 44 characters, the rest garbled by the operator |
| 3 | **Fra Giovanni di Lucca → Ferdinand III**, DECODE R2159 | 1644 | 4 | 4 | 5 | 2 | 2 | 4 | **3.80** | Polyphonic figure alphabet (17 = i/n, 19 = t/s) beaten ciphertext-only after Tomokiyo's crib proved self-contradictory. An offer to turn the Ottomans and Moldavia against Rákóczi and to supply 2,000 Cossacks, at the close of the Thirty Years' War. Three spellings and the speaker's name need the images |
| 4 | **Feuquières → Catinat**, Pignerol, 25 Jan 1691 (petit chiffre) | 1691 | 4 | 3 | 4 | 4 | 2 | 4 | **3.55** | Two-part code with no table in print, read by finding a second letter in the same code printed with its translation, and carrying alignment between them by hand (586/601 tokens). Fixes the plan for the Veillane surprise. Bazeries read it in 1893 but never published |
| 5 | **Maltravers → Ormonde** | 1634–35 | 3 | 3 | 5 | 4 | 2 | 4 | **3.50** | Block alphabet from 59 figures, then the nomenclator confirmed clause by clause against Wentworth's dispatches in Knowler 1739. The King's refusal of Kildare and the Crosby exchange for Ormonde's council seat. Two person-codes unidentified |
| 6 | **Louvois and Louis XIV → Catinat**, seven Grand Chiffre despatches | 1691 | 1 | 5 | 5 | 3 | 1 | 5 | **3.40** | No cryptanalysis: Bazeries' table applied to 12,362 groups from the MDZ hOCR. Ranks on content and volume alone: about 9,700 groups never in clear, including the King's 14 Sept decision to bring the army back over the Alps and abandon Piedmont. Controls 98–99 % against the two letters Bazeries printed |
| 7 | **Huang Xing → Lin Hu and Li Genyuan**, JACAR B03050731500 | 1916 | 3 | 3 | 5 | 3 | 1 | 4 | **3.30** | Kana-for-digit scheme identified and the telegram read from the frames. National Protection War correspondence; not on any list, a by-product of the Sun Yat-sen item |
| 8 | **Urquhart's Cyphral Octastich**, The Jewel 1652 | 1652 | 3 | 2 | 3 | 4 | 5 | 4 | **3.15** | A book cipher on the book itself, verified without the plaintext Vals AI published in Aug 2026: a new 285-number transcription from the 1983 photographs and 238/284 first-occurrence hits against 0.43 for controls. The highest-profile item solved (Schmeh Top 50 no. 28) but a royalist prayer, not news. Ten letters unread; the distich stays open |
| 9 | **Armstrong → Madison**, coded postscript | 1808 | 2 | 2 | 5 | 4 | 2 | 5 | **3.10** | Key rebuilt from pencil decodes on the NARA microfilm, found by scoring frames for faint pencil. 48 of 49 groups, the 49th a probable slip for *man*. The content is consular gossip. The separate 20 Feb 1808 letter is unsolved and the AFIO claim on it was rejected |
| 10 | **Warsaw, 24 Dec 1627**, DECODE R1408 | 1627 | 3 | 2 | 5 | 2 | 2 | 3 | **2.95** | Homophonic alphabet in plain order plus syllables, nulls and thirteen word codes, found by annealing from random starts. A promised canonry of Olmütz for a son of the Queen of Poland; addressee inferred. Word codes glossed from context only |
| 11 | **Richelieu → M. de Rancé**, BnF fr. 3829 ff. 87, 89 | 1629 | 4 | 3 | 1 | 2 | 2 | 5 | **2.85** | Clean ciphertext-only recovery of a homophonic alphabet and nomenclature, then found word for word in Avenel 1858. Cryptanalytically among the best pieces of work here; historically a verification of a 168-year-old reading the lists missed |
| 12 | **Charles I and Nicholas → Boswell**, TNA SP 84/157 | 1643 | 2 | 3 | 3 | 3 | 2 | 3 | **2.65** | Alphabet solved by R. Pitt (Sept 2026), verified here at z = 9.6. Added the four inline word-signs and the identification of the addressee as the Duke of Courland's envoy. A dozen word codes open |
| 13 | **Sir Richard Forster**, 13 May 1644 | 1644 | 3 | 2 | 1 | 2 | 2 | 4 | **2.25** | Found already read by Lasry, Biermann and Pitt. Value here is methodological: 31 of 34 symbols recovered blind from 207 tokens once word boundaries are used, six controls read |

Score = 0.25 D + 0.25 H + 0.20 N + 0.10 R + 0.10 F + 0.10 V.

### Provisional additions, 17 Sept 2026

Seven items read after the ranking above was compiled. Scored on the same axes and formula by the assistant
alone, not worked out in the appendix and not folded into the by-axis lists; Daniel is to check the scores
before the tables are merged. Where they would fall: Lanssac between Feuquières and Ormonde, Raince between Huang Xing and Urquhart,
the other four between Warsaw and Boswell.

| # | Target | Date | D | H | N | R | F | V | Score | Why it sits here (provisional) |
|---|---|---|---|---|---|---|---|---|---|---|
| p1 | **Lanssac → Charles IX**, Warsaw, 26 Apr 1573, fr. 4735 f. 124, and ff. 160, 164, 174 | 1573 | 4 | 3 | 4 | 5 | 2 | 4 | **3.65** | Homophonic letter cipher with word signs, read from the Gallica images: key pinned from the glossed sibling f. 154v and the gutter-cut fragments, then confirmed by a pinned annealer against shuffled and blind controls; 96 of 100 signs; the same key reads three 1 and 9 May election letters. The Polish election bought by the Emperor and by France. Tomokiyo's table corrected |
| p2 | **Henri IV → Béthune**, Rome, 9, 10 and 22 Nov 1601, fr. 3484 nos. 7, 8, 12 | 1601 | 3 | 3 | 3 | 4 | 2 | 2 | **2.90** | 10 Nov read in full through its clear minute (f. 36), the key recovered by alignment and the 8 Nov and 10 Dec marginal decipherments; a Villeroy-office key of the design Bazeries printed for Béthune's brother. 9 Nov about six words in ten, 22 Nov open. Novelty limited because the minute already carried the 10 Nov text in clear |
| p3 | **Nevers → Pisany**, 8 Sept and 14 Oct 1593, fr. 3985 f. 209 and fr. 3986 f. 168 | 1593 | 2 | 3 | 4 | 4 | 2 | 2 | **2.85** | Tomokiyo's Nevers key no. 46 re-read at glyph level from fr. 3995 f. 87, checked against the office's decipherment of a Gondi letter, then applied: 8 Sept whole, 14 Oct in long stretches, both unread before. The five Revol letters are a separate key (no. 60) and stay open |
| p4 | **Philip II → Mendoza**, 7 Sept 1589, fr. 3641 ff. 10/14 and 12/76 | 1589 | 2 | 3 | 2 | 4 | 2 | 3 | **2.55** | Resolved rather than solved: f. 14 and f. 76 are the 1589 decipherer's fair copies of ff. 10 and 12, so the "second undeciphered letter" was never a cipher. Group-by-group alignment rebuilds part of Cg.13 (c. 70 syllables, c. 50 code groups), fills groups the decipherers left blank and corrects two readings. Fourteen groups open; needs Devos 1950 |
| p5 | **Jean du Bellay → Montmorency**, 16 June 1529, fr. 3078 no. 3 | 1529 | 2 | 3 | 3 | 3 | 2 | 2 | **2.55** | The residue of catalogue item 4, whose other letters proved to be in print (Le Grand 1688, Bourrilly 1905). Key re-derived on the leaf from the 22 June interlinear (B = o, the word signs *bien*, *fault*, *paix*), confirmed by reading the 17 Oct 1529 letter against Le Grand; about 60 % of the 16 June signs read in stretches. Divorce-negotiation news of 1529 |
| p7 | **BnF Espagnol 318**, nos. 92 and 95, the Catholic Monarchs' ciphered letters | 1497–1504 | 2 | 3 | 5 | 5 | 1 | 2 | **2.95** | Two keys found rather than broken: no. 92's is the *Cifra general* printed in 1994, proved against the glosses on its own leaf (eight hits, no misses) and transcribed; no. 95's is Lasry's 2022 alphabet, applied through segmentation and clustering to read about two thirds. High on novelty and research — five ciphered letters correctly mapped where the catalogue had four, one found already in print (Parisi 2020), and nos. 93–94 fingerprinted to the *Gran cifra* by the code-initial band of a one-part nomenclator. Low on difficulty and profile: nothing here was a cold break, and the volume is on no standard list. Held down on completeness — no. 92 is readable but not yet read out in full, and a third of no. 95 is beyond the scan |
| p6 | **Nicolas Raince → Montmorency**, Rome, 13 May and 20 Nov 1526, fr. 2984 pp. 29–31 and 105 | 1526 | 2 | 4 | 5 | 4 | 2 | 2 | **3.30** | The key was in print and useless, because reading which glyph sits under which letter in Tomokiyo's table image by eye slips a column: the first pass here had l, m and n each one place wrong. Re-measured off the image, the table resolves a control line glyph for glyph, and 86 of about 106 lines that exist in no edition were then read by hand off a microfilm. Low on difficulty (the system was published), high on novelty and content: the negotiation nine days before the League of Cognac, and the Medici pontificate as 'la totale ruine de sa maison' two months after the Colonna raid. Held down on completeness — 20 lines are machine-only and the read lines carry gaps |
| p7 | **Sormano and de Vaulx → François I**, Ferrara, Feb 1529, fr. 3096 nos. 63, 65, 66 | 1529 | 2 | 4 | 5 | 5 | 2 | 4 | **3.70** | Key in print (Lasry 2023) but never applied; the work was reading 18,000 signs from the scans by segmentation, clustering and a classifier with every line checked by eye, and finding the null and the nomenclator the table lacks. Two of three letters end to end, the third in stretches; the duplicate pair verifies the reading. Content: the duke of Ferrara refusing the crown of Naples and the French command before Cambrai, unread since 1529 |
| — | **Henri IV → Landgrave Maurice of Hesse-Kassel**, seven passages, 1602–09 | 1602–09 | 1 | 4 | 5 | 3 | 2 | 4 | **3.10** | Provisional. No cryptanalysis: Rommel's 1846 key applied to his 1840 figures, about 4,100 groups transcribed by eye. Never in clear before (Tomokiyo and the Lettres missives list them undeciphered). Content: the King's plan of a Protestant-German and Dutch front against the Spanish design on the Diet, 20 May 1606, and the two-million-livres subsidy, 22 Dec 1605 |

Arithmetic: p7 0.50 + 1.00 + 1.00 + 0.50 + 0.20 + 0.40; p6 0.50 + 1.00 + 1.00 + 0.40 + 0.20 + 0.20; p1 1.00 + 0.75 + 0.80 + 0.50 + 0.20 + 0.40; p2 0.75 + 0.75 + 0.60 + 0.40 + 0.20 + 0.20; p3 0.50 + 0.75 + 0.80 + 0.40 + 0.20 + 0.20;
p4 0.50 + 0.75 + 0.40 + 0.40 + 0.20 + 0.30; p5 0.50 + 0.75 + 0.60 + 0.30 + 0.20 + 0.20.

### Provisional additions, 18 Sept 2026

Ten more items, scored the same way and with the same caveat: the assistant's scores, for Daniel to check before merging.
Where they would fall: the Sun Yat-sen intercepts beside Lanssac, Toledo 1565 and Soglia 1848 beside Feuquières, Adams No. 88
just above Warsaw, Yard 1699 and Vich 1511–12 beside Béthune, Mary to Norfolk just above Adrian 1521, Adrian level with
Mendoza, and Erving 1807 below Forster. Bordeaux 1653 (p17, added later the same day) sits just below Huang Xing, Pelissier 1592 (p18, rescored after the calibrated re-reading) level with Louvois and Louis XIV, and Gramont 1529–37 (p19) just below Feuquières. Herbault 1626 (p20, contributed by Arya Sanketbhai Patel) sits just above Erving 1807; Conti 1649 (p21) beside Bordeaux 1653. Sadoleto 1482 (p26, added 19 Sept) sits just below Adams No. 88 and just above Warsaw. Ricasoli 1425 (p22) sits with Armstrong, just above Warsaw. Sessa 1524 (p23) sits among the lower partial reads, just above Herbault 1626. Charles VI to Windischgrätz 1720–22 (p24) sits beside Yard 1699, whose case it repeats: the key in the same papers, read straight off.

| # | Target | Date | D | H | N | R | F | V | Score | Why it sits here (provisional) |
|---|---|---|---|---|---|---|---|---|---|---|
| p8 | **Sun Yat-sen's circle, intercepted telegrams**, JACAR B03050088300–B03050090200 | 1916–17 | 3 | 4 | 5 | 5 | 1 | 3 | **3.65** | The Swatow family applied across the Ministry of Communications' copies: keys found by search over a family already known, so 3 not 4, but each accepted on a telegram it was not fitted to, and rhyme-day dates check. About sixty telegrams from six files transcribed by hand from the forms. Content: the end of Yuan's monarchy seen from Sun's side, Chen Qimei's murder, and the Foreign Ministry's own advice relayed on a wire it could not read. On no list. Held down on completeness: most long telegrams keep [?] groups, two keys are tentative, and 文密 is open |
| p9 | **García de Toledo → Philip II**, Messina, 16 July 1565, AGS Estado leg. 1394 no. 247 (duplicado) | 1565 | 3 | 4 | 5 | 3 | 1 | 4 | **3.55** | No key in print and no decipherment on the leaf or in PARES, but an easy system once seen: two clear-text cribs (*seiscientos soldados*, *en tiera*) and the alphabetical order of the figures 12–43 gave the whole table, confirmed on predicted letters and on *Mosiur de Lenni*, a name not in the clear text. High on content: the viceroy's own account of the Piccolo Soccorso and of a second relief run waved off by La Valette's signals, plus the Sicilian finances. On no list (own PARES sweep). Held down on verification: the checks are internal; the original despatch has not been found |
| p10 | **J. Q. Adams → Secretary of State**, St Petersburg, No. 88, 25 June 1812, M35 reel 3 | 1812 | 2 | 3 | 5 | 4 | 2 | 2 | **3.05** | Code rebuilt from the clerk's interlinear decodes, not broken cold, after refuting the editorial premise that it was Armstrong's THE = 972. The nine lines Ford printed as not decyphered read, 124 of 134 groups with 27 by slot inference. Content: the Chancellor's strokes at Wilna on the eve of 1812, dated earlier than the standard accounts. Held down on completeness: one passage, ten groups unread, the rest of the despatch in threads |
| p11 | **Robert Yard → the Earl of Manchester**, Whitehall, 12 and 16 Oct 1699, Beinecke OSB MSS fc37 box 2/49, 2/51 | 1699 | 1 | 3 | 4 | 4 | 2 | 5 | **2.90** | No cryptanalysis: the key was a printed code sheet in the same Manchester papers at Yale, transcribed (1,456 slots) and validated on the 5 Oct sibling's contemporary decipherment. Both letters read end to end, 368 groups, five slips marked. Novelty held to 4 because Tomokiyo had named the code and decoded the first groups, and Cole's *Memoirs* (1733) was not re-checked. Content: intelligence traffic, the Dover watch for Mills and Lord Drummond's priest and reports of a design at Saint-Germain; no decision of state |
| p12 | **Adrian of Utrecht, the Admiral and the Constable → Charles V**, Vitoria, 30 Dec 1521, AGS Estado leg. 8 no. 150 | 1521 | 2 | 3 | 2 | 4 | 1 | 4 | **2.55** | Found in print (Pérez Gredilla's decipherment in Danvila, MHE 38, 1899), then used as a crib: ciphertext transcribed from PARES and aligned on `xif` = V. M., the nomenclator rebuilt with its alphabet-block code initials. Corrects the dead king from England to Manuel I of Portugal and reads or corrects about 17 of c. 25 unread groups. Low on difficulty and novelty (plaintext in print), on no list; held on completeness by about ten open groups and a rough sign alphabet at PARES resolution |
| p13 | **G. W. Erving → Madison**, Madrid, 24 Mar 1807, Pinckney's code | 1807 | 1 | 2 | 2 | 4 | 1 | 5 | **2.15** | Holes in a decode already in print closed from the two received copies and Pinckney's decoded despatches; the only loss is Erving's own. Low on difficulty (Madison had the key), novelty (the editors had suggested two of the corrections) and profile (on no list); high on verification and research (three microfilm and LoC sources collated) |
| p14 | **Ferdinand the Catholic → Jerónimo de Vich**, AHN Estado 8715 N.45, N.57, N.60, Apr 1511 – Sept 1512 | 1511–12 | 2 | 4 | 3 | 4 | 1 | 3 | **2.90** | Key rebuilt from two deciphered siblings, not broken cold, then read three letters it was not built from; about 22,500 signs and groups transcribed from PARES. High on content: Ferdinand's own account of how his army was pushed into Ravenna, the Sforza restoration and the call for spiritual war on Louis XII. Novelty held to 3 because Terrateig 1963 (not seen) prints Ferdinand's letters from this legajo and may include these. On no list. Held down on verification and completeness: the checks are internal, some groups unread, and the siblings N.41 and 8714 were not used |
| p15 | **Mary Queen of Scots → the Duke of Norfolk**, "the 20th" [Feb or Mar 1570], Cotton MS Caligula C II f. 74r | 1570 | 2 | 3 | 3 | 3 | 2 | 3 | **2.65** | Key in print (Tomokiyo, rebuilt from the deciphered siblings) and checked on f. 66r; no cryptanalysis beyond reading signs. Novelty is limited: Tomokiyo's overlay already had most of the letters, and what is new is the continuous reading, the gap fills, the names and the date. Content: the Norfolk marriage intrigue after Moray's murder, with Elizabeth blaming Mary for it. Five unkeyed signs and a few words open |
| p16 | **Cardinal Soglia → the nuncio Viale Prelà**, Rome 15 June 1848 (*L'Italia del Popolo*, 30 June 1848) | 1848 | 4 | 3 | 5 | 3 | 2 | 3 | **3.55** | Ciphertext-only recovery of a system nobody had described for this text: word separator, 64-cell table with syllables, alphabetical 8XXX code, and a synthetic control behind the negative. Never read before, and the paper offered a prize for it in 1848. Content: a papal counter-order to the nuncio that came a day late. Transcription supplied, one digit restored. On no list, only a Cipherbrain post. Ten code words read from context and checked by rank, eleven open |
| p17 | **Bordeaux → Brienne**, London, 30 May 1653, BL Add MS 4200 f. 88 | 1653 | 2 | 3 | 5 | 4 | 2 | 4 | **3.25** | Read with the Deciphering Branch's own key sheet (DECODE R7537), so 2 not higher, although the design had been identified and a solver built for it beforehand. Never read before: the English worksheets stop at frequency counts. Research: the DECODE key found, the transcription re-checked on the images and 21 faults fixed, the duplicates collated. Content: the envoy's precedence complaint after the Bordeaux deputies' reception and the advice to hold back French mediation, during the Fronde's last months. On Tomokiyo's list only. Held on completeness by six nomenclature codes and a dozen rare tokens |
| p18 | **A. Pelissier → Pierre Jeannin**, Burgos, 13 Sept 1592, BnF fr. 3982 no. 22 | 1592 | 2 | 4 | 4 | 5 | 2 | 4 | **3.40** | Key in print (Tomokiyo, from Pelissier's later letters) and confirmed by the decipherer's glosses, so 2; the work was ~18,400 signs transcribed from the Gallica scans and beam-decoded. Never read before and weighty: Spanish policy toward the League and the Estates in the autumn of 1592, the two-army plan and its cost, the case for Navarre as argued in France. Research 5: the key calibrated on 1,764 signs of the sibling letters aligned with their decipherment. Completeness 4: 94% of the ciphered words read, 256 gaps marked |
| p19 | **Gramont, Mâcon and Langeac → Montmorency**, Venice and Rome, 1529–37, fr. 3083 no. 8, fr. 3091 no. 23, fr. 3071 nos. 4, 7 | 1529–37 | 2 | 4 | 5 | 4 | 2 | 4 | **3.50** | Keys in print (Lasry 2023) but never applied, so 2; the work was reading ~9,000 signs from the scans, six unlisted code signs, and dating. Content is the French line to Clement VII before Bologna (council, Florence, the Admiral's mission) and Paul III's Farnese marriage threat of 1537. Verification: a contemporary decipherment slip for the Mâcon f. 9v passage |
| p20 | **Phelipeaux d'Herbault → Philippe de Béthune**, Paris, 13 Feb 1626, BnF fr. 3669 no. 25 | 1626 | 1 | 3 | 2 | 3 | 1 | 4 | **2.20** | Resolved rather than solved, like Mendoza: the catalogue's one undeciphered letter is a copy of no. 26, which carries the 1626 decipherer's interlinear plaintext, so 1 on difficulty and 2 on novelty (read in 1626, never printed). The ciphered passages matter (the Valtelline, the reason for the Huguenot peace, Savoy pressing France towards war with Spain six weeks before Monzón); identity checked on the clear text, the run boundaries and matching groups. Only on the BnF harvest list. |
| p21 | **Prince de Conti → Laigue and Noirmoutier**, Paris, March 1649, BnF fr. 3854 nos. 41–43 | 1649 | 2 | 4 | 4 | 4 | 1 | 4 | **3.20** | Nos. 41–42 already read (Lasry 2023), so their share adds only corrections. No. 43's key was rebuilt from the clerk's glosses, not broken cold, hence D 2; but its opening had never been read and the body, though glossed in 1649, is unpublished. Content: the Frondeurs' secret line to the Archduke during Rueil, the conference as a stalling device and the promise to break it when Spain enters France. Not on any list (catalogue only). Four blotted places open |
| p22 | **Galeotto Fibindacci da Ricasoli → the Signoria of Florence**, Urbino, early 1425, ASF Dieci di Balìa, Responsive 2 no. 171 | 1425 | 3 | 3 | 4 | 4 | 1 | 3 | **3.10** | The oldest letter read in this repository. Gabbrielli's 1863 key and glosses did a third of the work; the three long runs he left unread were aligned sign by sign and his null list corrected. Never printed, so the text is new, though the key has been in print since 1902. Two word signs from context and five letter values on this letter only keep V at 3 |
| p23 | **Duke of Sessa (Luis Fernández de Córdoba) → Charles V**, Rome, 18 Apr 1524, RAH Salazar A-31 ff. 128–131 | 1524 | 2 | 2 | 4 | 5 | 1 | 3 | **2.70** | Key rebuilt from the court's decipherments of sibling letters, so 2. Routine embassy news, though never read: Bergenroth skipped the letter. Research 5: a century typo corrected, eight siblings aligned across three volumes, template matching over ~110 pages. Completeness 3: word-level reading, four groups open |
| p24 | **Charles VI → Count Windischgrätz**, Vienna, 1720–22, SOA Plzeň RA Windischgrätz (DECODE R5019–R5024) | 1720–22 | 1 | 4 | 4 | 4 | 1 | 4 | **2.95** | Both keys on DECODE beside the letters, so 1: the work was transcribing a 977-entry nomenclator and a sign key and reading 35 passages. Content weighs: the Emperor's own secret line on the peace after Alberoni's fall (France and Philip V, Sardinia, Montferrat, Portugal) and the first Spanish marriage feelers for his children. Novelty 4 because Mírka 2012 described the letters and keys without a plaintext. V 4: every passage reads, two cells uncertain |
| p25 | **Maffeo da Treviglio → Ludovico Sforza**, Buda, 22 Nov 1489 and 12 Jan 1490, ASMi Sforzesco 650 and 642/1, 4 | 1489–90 | 3 | 4 | 5 | 5 | 1 | 4 | **3.70** | The oldest text read in this repository, and the oldest previously unread ciphertext read here by any route. D 3: the key existed in print but only as numbers with no sign images, so it had to be re-anchored to the shapes through a cipher-and-clear pair, and about twenty signs were then recovered from the letters themselves. N 5: of the 1489 letter only its first two lines had ever been deciphered, and the 1490 letter not at all. H 4: Matthias Corvinus's peace with Frederick III and the Diet, the two rival marriages for John Corvinus, the queen's opposition, and a warning that intercepted cipher letters had been read. R 5: three archives' catalogues reconciled, three sibling records shown to be already deciphered and set aside. V 4: pp. 1–2 of 1489 read nearly throughout, p. 3 in patches |
| p26 | **Nicolò Sadoleto → Ercole I d'Este**, Pozsony, 16 July 1482, ASMo Ambasciatori Ungheria b. 1/9 no. 8 (DECODE R1102) | 1482 | 2 | 4 | 4 | 3 | 1 | 3 | **3.00** | Alphabet rebuilt from two sibling letters with contemporary clear copies, so D 2. The seven lines had no decipherment and carry real news: the Venetian counter-offer to Matthias at the start of the War of Ferrara (Veglia, a fleet command for János Corvin, 100,000 a year), the same sum Sadoleto later quotes as Matthias's price. Read in gist only, with a nomenclator group and a dozen signs open, so R 3; two of the four catalogue items were read at the time |
| p27 | **Marqués del Carpio (Rome) → Baltasar de Fuenmayor**, 1677, AGR Brussels SEG 2559 (DECODE R1002–R1011) | 1677 | 2 | 3 | 3 | 3 | 1 | 4 | **2.55** | The key was rebuilt from the cipher, but eight letters had marginal decipherments to align against, so D is 2. Two letters were catalogued as unread, though each proved to carry a faint margin, and no key had been published, so N is 3. Content: the Spanish ambassador's quarrel with Innocent XI, and the 1677 campaign seen from Rome (Messina, Charleroi, Freiburg, d'Estrées at Turin). V 4: the whole file reads, with three code words conjectural |
| p28 | **Unknown writer → "Monsieur"**, 17th c., TNA SP 106/10 ff. 241–243 (DECODE R927) | 17th c. | 4 | 4 | 1 | 2 | 1 | 3 | **2.80** | D 4: no key, no crib, no clear sibling; the pencil key on the flap was a false lead, and the homophonic system was recovered from a hand transcription by quadgram annealing. N 4: catalogued as undeciphered. H 1: a private client-to-patron letter, unnamed. R 2: writer and date unknown. V 3: last page nearly throughout, first page in fragments |

Arithmetic: p8 0.75 + 1.00 + 1.00 + 0.50 + 0.10 + 0.30; p9 0.75 + 1.00 + 1.00 + 0.30 + 0.10 + 0.40; p10 0.50 + 0.75 + 1.00 + 0.40 + 0.20 + 0.20;
p11 0.25 + 0.75 + 0.80 + 0.40 + 0.20 + 0.50; p12 0.50 + 0.75 + 0.40 + 0.40 + 0.10 + 0.40; p13 0.25 + 0.50 + 0.40 + 0.40 + 0.10 + 0.50;
p14 0.50 + 1.00 + 0.60 + 0.40 + 0.10 + 0.30; p15 0.50 + 0.75 + 0.60 + 0.30 + 0.20 + 0.30; p16 1.00 + 0.75 + 1.00 + 0.30 + 0.20 + 0.30;
p17 0.50 + 0.75 + 1.00 + 0.40 + 0.20 + 0.40;
p18 0.50 + 1.00 + 0.80 + 0.50 + 0.20 + 0.40;
p19 0.50 + 1.00 + 1.00 + 0.40 + 0.20 + 0.40;
p20 0.25 + 0.75 + 0.40 + 0.30 + 0.10 + 0.40;
p21 0.50 + 1.00 + 0.80 + 0.40 + 0.10 + 0.40;
p26 0.50 + 1.00 + 0.80 + 0.30 + 0.10 + 0.30;
p22 0.75 + 0.75 + 0.80 + 0.40 + 0.10 + 0.30; p23 0.50 + 0.50 + 0.80 + 0.50 + 0.10 + 0.30;
p24 0.25 + 1.00 + 0.80 + 0.40 + 0.10 + 0.40;
p27 0.50 + 0.75 + 0.60 + 0.30 + 0.10 + 0.40;
p28 1.00 + 1.00 + 0.20 + 0.20 + 0.10 + 0.30.

## By single axis

**Hardest cryptanalysis (D):** Ségur · Sun Yat-sen · Lucca · Feuquières · Richelieu. Ségur alone combined an
unknown system, transcription from images and a syllabary; the other four were known families attacked
ciphertext-only or with a partial crib. Catinat 1691 is last: the table was printed in 1893.

**Most important content (H):** Catinat 1691 · Ségur · Lucca · Sun Yat-sen · Ormonde, Feuquières, Huang Xing,
Boswell, Richelieu. Only Catinat 1691 records a decision of state (Louis XIV giving up Piedmont for 1692).
Ségur and Lucca are diplomacy at the level of armies and alliances. Urquhart and Armstrong are the weakest
here despite their prominence.

**First reading ever (N):** Ségur, Sun Yat-sen, Huang Xing, Lucca, Warsaw, Ormonde, Armstrong and Catinat's
five letters have no earlier reading that the notes could find*. Feuquières had an unpublished 1893 reading.
Urquhart and Boswell had readings weeks old. Richelieu and Forster were already in print.

**Most research (R):** Ségur · Feuquières · Ormonde · Urquhart · Armstrong. The Feuquières sibling letter was
found by searching the OCR of three volumes; the Ormonde nomenclator was confirmed from a 1739 edition; the
Urquhart numbers were re-transcribed from photographs on the HCPortal record.

**Highest profile (F):** Urquhart is the only Schmeh Top 50 entry among the solved. Everything else is from
Tomokiyo's list, and Catinat 1691 and Huang Xing are on no list at all.

## Second tier: explained, nothing to read

Ranked by how firmly the negative is established and how prominent the item was.

| # | Target | Date | Finding | Standing |
|---|---|---|---|---|
| 1 | Roosevelt cryptogram, number block | 1935 | A permutation of 1–52 written by hand; ordered-key readings fail while controls succeed. Ernst's doodle claim confirmed | Schmeh Top 50 no. 17. Reopen only with the original sheet |
| 2 | Chinese gold bar cryptograms | 1933 | Letter counts flatter than any cipher of a real text; no message | Schmeh Top 50; the top50 survey records independent corroboration |
| 3 | Hyde's ciphered superscriptions | 1659–60 | Dummy numbers, per the 1724 editor and the 1721 key | Tomokiyo entry; settled from print |
| 4 | D'Agapeyeff challenge | 1939 | Not enciphered English | Famous; the negative is a language test, not a full explanation |
| 5 | Beale Paper no. 1 | 1885 | Fabrication argued in the notes; book-cipher scan negative | Famous; the fabrication case is an argument, not a proof |

## Third tier: found already solved by others

Ordered by how much this repo added.

1. **ADFGVX, Eastern Front 1918.** The 2017 thread consolidated, Lasry's sixteenth key rebuilt, Biermann's
   method reimplemented and re-deriving seven pages blind; the ten open messages shown to be garbles.
2. **Matthias Corvinus to Ercole I d'Este, Pozsony, 1 June 1482 (DECODE R1156).** Printed in 1877 and by Fraknói
   in 1895. The cipher runs re-read from the image and a working key rebuilt; four garbled passages of the print
   corrected (*valent*, *gentibus*, the closing *Speramus cito nos res nostras ita disposituros…*, and the "regest"
   shown to be the letter's own last sentence).
3. **Alchymey teuczsch, Heidelberg Cod. Pal. germ. 597, 1426.** Read by Wattenbach in 1869. The compiler's struck
   24-sign alphabet (f. 1r) and the invocation alphabet (ff. 6v, 91v) recovered from the images and checked on his
   plaintexts; a third set fixed for eleven letters from the 2014 catalogue's reading of f. 93r; the "ff. 70–71"
   pointer shown to be Bischoff's item numbers. Ruled out as a record candidate.
4. **Letter to the King of Aragon, ACA Reserva 12, [1413–16].** Printed by Salas in 1931; the column-transposition
   rule checked on the archive's image.

Perwich, the Feynman ciphers, Ferdinand III, Milroy, the Confederate dictionary code and Mazarin–Bordeaux 1654 were found
solved by others with nothing added here and are no longer listed (removed 17 September 2026).

## Appendix: the scores worked out

Weights: D 0.25, H 0.25, N 0.20, R 0.10, F 0.10, V 0.10 (sum 1.00). Each entry below gives the reason for
every axis score, then the six weighted terms in that order and their sum. Scale anchors: 1 = the low
description in the axis table, 5 = the high one, 3 = a typical entry on Tomokiyo's list.

**1. Navarre → Ségur, 1585–86**
- D 5: no transcription existed; 461 figures and 25 letter-glyphs read from the Gallica images; the system (letters plus a 70-syllable table) was unknown until the mod-5 test exposed it; the key came from a structured annealer scored on a matched control at 96.6 %.
- H 4: instructions to the envoy raising a German army in the Wars of Religion, naming Casimir, Clervant's reiters and the invasion road; corrects the sender from Henry III to Navarre. Not a decision of state in itself, hence not 5.
- N 5: no reading anywhere before this work*; the letters were miscatalogued and unread.
- R 5: IIIF fetch, glyph-level transcription, whole-volume sweep of 440 canvases, an unlisted cipher leaf found (f. 366), Tomokiyo's sibling key shown to be this key shifted by eight.
- F 2: Tomokiyo list entry, no wider fame.
- V 4: 97 % on control, three letters read in substance; a dozen word-signs and f. 143 open.
- 0.25×5 + 0.25×4 + 0.20×5 + 0.10×5 + 0.10×2 + 0.10×4 = 1.25 + 1.00 + 1.00 + 0.50 + 0.20 + 0.40 = **4.35**

**2. Swatow telegram to Sun Yat-sen, 1916**
- D 4: the family (a code condenser over the standard telegraph code) was hypothesised, then 57,600 keys brute-forced with a Chinese character model. A known family narrowed by search, so 4 not 5.
- H 4: a field report of the Chaozhou rising and the fall of Swatow in the 1916 campaign against Yuan Shikai, addressed to Sun himself.
- N 5: no reading found before this work*.
- R 3: JACAR frames fetched; the tail re-checked on the sheet at 600 dpi.
- F 2: Tomokiyo entry.
- V 4: 41 of about 44 characters; the three lost codes are the operator's garble.
- 1.00 + 1.00 + 1.00 + 0.30 + 0.20 + 0.40 = **3.90**

**3. Fra Giovanni di Lucca → Ferdinand III, 1644**
- D 4: a polyphonic alphabet (two figures each standing for two letters) is harder than plain homophony; solved ciphertext-only after the supplied crib proved self-contradictory, with all seeds agreeing and shuffled controls failing. Not 5 because the transcription was supplied and the text is short.
- H 4: an offer to turn the Porte and Moldavia against Rákóczi and to supply 2,000 Cossacks, in the last year of the Thirty Years' War.
- N 5: DECODE still marks it non-decrypted; no reading found*.
- R 2: worked from Tomokiyo's transcription only.
- F 2: Tomokiyo entry.
- V 4: 231 groups read end to end; three spellings and the speaker's name need the images.
- 1.00 + 1.00 + 1.00 + 0.20 + 0.20 + 0.40 = **3.80**

**4. Feuquières → Catinat, 25 Jan 1691**
- D 4: a two-part code with no table in print cannot be annealed at 418 groups; it was read by aligning a second letter in the same code against its contemporary translation, by hand, after every automatic aligner failed. Heavy but partly known-plaintext, so 4.
- H 3: the tactical plan for the Veillane surprise; operational, not strategic.
- N 4: Bazeries read it in 1893 but never printed the reading.
- R 4: the Grand Chiffre table transcribed from Gallica and verified on four despatches; the sibling letter found by searching the OCR of three volumes.
- F 2: Tomokiyo entry.
- V 4: 586 of 601 tokens across the two letters; twelve singleton groups unread.
- 1.00 + 0.75 + 0.80 + 0.40 + 0.20 + 0.40 = **3.55**

**5. Maltravers → Ormonde, 1634–35**
- D 3: a regular block alphabet recovered from 59 figures through consecutive-figure doublets; short, and the alphabet is of a standard Stuart design.
- H 3: Wentworth's Irish administration, the King's refusal of Kildare, Ormonde's council seat in exchange for Crosby.
- N 5: no reading found before this work*.
- R 4: the nomenclator confirmed clause by clause against Knowler's 1739 edition of Wentworth's dispatches.
- F 2: Tomokiyo entry.
- V 4: every spelled word reads; two person-codes in one clause unidentified.
- 0.75 + 0.75 + 1.00 + 0.40 + 0.20 + 0.40 = **3.50**

**6. Louvois and Louis XIV → Catinat, seven despatches, 1691**
- D 1: Bazeries' 1893 table applied; no cryptanalysis.
- H 5: the King's 14 Sept decision to bring the army back over the Alps, fight defensively in 1692, hold and then burn Carmagnole, take Coni in winter. The only decision of state among the solved items.
- N 5: about 9,700 groups in five letters never before in clear*.
- R 3: MDZ hOCR of the volume, 137 doubtful stretches checked on the page images, seven OCR fixes.
- F 1: on no list; the by-product of the Feuquières item.
- V 5: 98.1 % and 99.1 % against the two letters Bazeries printed in clear.
- 0.25 + 1.25 + 1.00 + 0.30 + 0.10 + 0.50 = **3.40**

**7. Huang Xing → Lin Hu and Li Genyuan, 1916**
- D 3: the scheme (three kana per character, consonant row carrying the digit) identified by inspection and confirmed by reading.
- H 3: National Protection War correspondence between named commanders.
- N 5: no reading found before this work*.
- R 3: JACAR frames fetched and read.
- F 1: on no list; found beside the Sun Yat-sen telegram.
- V 4: read from the frames; not independently controlled beyond the reading itself.
- 0.75 + 0.75 + 1.00 + 0.30 + 0.10 + 0.40 = **3.30**

**8. Urquhart's Cyphral Octastich, 1652**
- D 3: a book cipher whose rule (number k → first word of the needed initial on physical page k) is simple once stated; the work was verifying it with a first-occurrence test, 238/284 against 0.43 for controls.
- H 2: a royalist prayer for Charles II in ottava rima; literary, not documentary.
- N 3: Vals AI published a plaintext in Aug 2026; this reading was made without it and extends the transcription, but is not first.
- R 4: 285 numbers re-transcribed from the 1983 edition's photographs on the HCPortal record (Schmeh's public 272 were 13 short); EEBO-TCP text aligned to physical pages.
- F 5: Schmeh Top 50 no. 28, with a live public dispute over the distich.
- V 4: ten letters of line 5 unread at a TCP text defect; the distich claim fails and stays open.
- 0.75 + 0.50 + 0.60 + 0.40 + 0.50 + 0.40 = **3.15**

**9. Armstrong → Madison, coded postscript, 1808**
- D 2: the key was read off pencil decodes on other despatches and completed by alphabetical-slot inference; little cryptanalysis.
- H 2: who should be consul; diplomatic gossip.
- N 5: no reading found before this work*.
- R 4: NARA microfilm frames fetched through the catalogue proxy and ranked by a script scoring faint pencil; 580-group table rebuilt.
- F 2: Tomokiyo entry.
- V 5: 48 of 49 groups determined, the 49th a probable slip for *man*; the reading is not in doubt.
- 0.50 + 0.50 + 1.00 + 0.40 + 0.20 + 0.50 = **3.10**

**10. Warsaw, 24 Dec 1627**
- D 3: a 5-gram plus dictionary annealer converged from random starts; the alphabet turned out to be in plain order, which made the problem easier than it looked but was not given to the solver.
- H 2: a promised canonry of Olmütz for a son of the Queen of Poland.
- N 5: DECODE still non-decrypted; no reading found*.
- R 2: Tomokiyo's transcription only.
- F 2: Tomokiyo entry.
- V 3: every spelled word reads; ten word codes and three groups glossed from context; addressee inferred.
- 0.75 + 0.50 + 1.00 + 0.20 + 0.20 + 0.30 = **2.95**

**11. Richelieu → M. de Rancé, 1629**
- D 4: homophonic alphabet plus nomenclature recovered ciphertext-only from a short text; clean cryptanalysis.
- H 3: Richelieu's own instructions in 1629; of interest, already used by historians since Avenel.
- N 1: printed word for word by Avenel in 1858.
- R 2: Tomokiyo's transcription; the Avenel match found afterwards.
- F 2: Tomokiyo entry.
- V 5: agrees word for word with the 1858 print.
- 1.00 + 0.75 + 0.20 + 0.20 + 0.20 + 0.50 = **2.85**

**12. Charles I and Nicholas → Boswell, 1643**
- D 2: the alphabet was solved by R. Pitt; this repo verified it (z = 9.6) and added the four word-signs.
- H 3: the King's letter to the Duke of Courland's envoy; Nicholas on the Dutch embassy of 1644.
- N 3: Pitt's reading is weeks old; the word-signs and addressee are new here.
- R 3: re-credentials traced to Simpson's 1893 print; the addressee identified.
- F 2: Tomokiyo entry.
- V 3: read in substance; a dozen single-occurrence codes open and the transcription needs the folios.
- 0.50 + 0.75 + 0.60 + 0.30 + 0.20 + 0.30 = **2.65**

**13. Sir Richard Forster, 13 May 1644**
- D 3: a mixed homophonic alphabet recovered blind, 31 of 34 symbols from 207 tokens, six controls read; good method on a small text.
- H 2: the content is not remarkable.
- N 1: already read by Lasry, Biermann and Pitt before this work.
- R 2: transcription only; four slips need the manuscript.
- F 2: Tomokiyo entry.
- V 4: permutation control z = 8.8; three symbols short of the full alphabet.
- 0.75 + 0.50 + 0.20 + 0.20 + 0.20 + 0.40 = **2.25**

**Sensitivity.** Three other weightings, same scores. With novelty dropped and its weight given to D and H (0.35 each): Ségur 4.25, Sun Yat-sen 3.70, Lucca 3.60, Feuquières 3.45, Richelieu 3.35, Ormonde 3.10, Urquhart 3.05, Catinat 1691 3.00, Huang Xing 2.90, Forster and Boswell 2.55, Armstrong 2.50, Warsaw 2.45. Richelieu climbs to fifth and Catinat 1691 falls to eighth, because both are carried by novelty in opposite directions. With list profile raised to 0.30 at the expense of D and H (0.15 each): Ségur 3.85, Urquhart 3.65, Sun Yat-sen 3.50, Lucca 3.40, Ormonde 3.30, Feuquières 3.25, Armstrong 3.10, Catinat 1691 3.00, Huang Xing 2.90, Warsaw 2.85, Richelieu and Boswell 2.55, Forster 2.15. Urquhart is the only item fame moves far. With all six axes equal (1/6 each): Ségur 4.17, Sun Yat-sen 3.67, then Urquhart, Ormonde, Lucca and Feuquières tied at 3.50, Catinat 1691 and Armstrong 3.33, Huang Xing 3.17, Warsaw and Richelieu 2.83, Boswell 2.67, Forster 2.33. Ségur is first and Forster last under every weighting tried; Sun Yat-sen is second in three of four; the middle six reorder freely.

## What this ranking does not settle

- **Novelty marked *:** "no earlier reading" means none was found in the printed editions, catalogues and
  DECODE records the notes cite. An archive decipherment sheet could exist for any of them, as it did for
  Richelieu. Confirming it would take the DECODE record and the archive's own finding aid for each.
- **Historical weight** is judged from the plaintext as read. For Ségur, Warsaw and Lucca the word-signs
  and names still open could raise or lower it.
- **Difficulty** compares finished work. Items closed as unsolved (SP 53, Ottobon, BLUME) were
  harder than anything here and are ranked in the tracker, not on this page.

Checked: every row against the Solved, Explained and Found-solved tables of README.md and the tracker rows of
TARGETS.md as of commit d1abee8; the five provisional rows against SOLVED_CATALOGUE.md and the per-target NOTES on 17 Sept 2026. Not checked: the per-target NOTES.md for facts beyond those tables; whether any
"first reading" has a prior in an archive finding aid. User must verify: the axis scores and weights, which are
editorial.
