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
