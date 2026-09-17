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
| 9 | **Armstrong → Madison**, coded postscript | 1808 | 2 | 2 | 5 | 4 | 2 | 5 | **3.10** | Key rebuilt from pencil decodes on the NARA microfilm, found by scoring frames for faint pencil. 49 of 49 groups. The content is consular gossip. The separate 20 Feb 1808 letter is unsolved and the AFIO claim on it was rejected |
| 10 | **Warsaw, 24 Dec 1627**, DECODE R1408 | 1627 | 3 | 2 | 5 | 2 | 2 | 3 | **2.95** | Homophonic alphabet in plain order plus syllables, nulls and thirteen word codes, found by annealing from random starts. A promised canonry of Olmütz for a son of the Queen of Poland; addressee inferred. Word codes glossed from context only |
| 11 | **Richelieu → M. de Rancé**, BnF fr. 3829 ff. 87, 89 | 1629 | 4 | 3 | 1 | 2 | 2 | 5 | **2.85** | Clean ciphertext-only recovery of a homophonic alphabet and nomenclature, then found word for word in Avenel 1858. Cryptanalytically among the best pieces of work here; historically a verification of a 168-year-old reading the lists missed |
| 12 | **Charles I and Nicholas → Boswell**, TNA SP 84/157 | 1643 | 2 | 3 | 3 | 3 | 2 | 3 | **2.65** | Alphabet solved by R. Pitt (Sept 2026), verified here at z = 9.6. Added the four inline word-signs and the identification of the addressee as the Duke of Courland's envoy. A dozen word codes open |
| 13 | **Sir Richard Forster**, 13 May 1644 | 1644 | 3 | 2 | 1 | 2 | 2 | 4 | **2.25** | Found already read by Lasry, Biermann and Pitt. Value here is methodological: 31 of 34 symbols recovered blind from 207 tokens once word boundaries are used, six controls read |

Score = 0.25 D + 0.25 H + 0.20 N + 0.10 R + 0.10 F + 0.10 V.

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
2. **Perwich → Arlington 1670.** Transposition reproduced from the TNA blog solution.
3. **Feynman ciphers 2 and 3.** The 2023 solution verified.
4. **Ferdinand III ↔ Cardinal-Infante.** Ernst's 2017 solution located in Schmeh's own comment thread.
5. **Milroy telegrams; Confederate Navy dictionary code.** Located in print; nothing added.

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
- V 5: 49 of 49 groups.
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
- **Difficulty** compares finished work. Items closed as unsolved (Bordeaux, SP 53, Ottobon, BLUME) were
  harder than anything here and are ranked in the tracker, not on this page.

Checked: every row against the Solved, Explained and Found-solved tables of README.md and the tracker rows of
TARGETS.md as of commit d1abee8. Not checked: the per-target NOTES.md for facts beyond those tables; whether any
"first reading" has a prior in an archive finding aid. User must verify: the axis scores and weights, which are
editorial.
