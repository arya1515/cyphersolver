# Target tracker — unsolved ciphers from cryptiana's list

Source list: https://cryptiana.web.fc2.com/code/unsolved.htm (S. Tomokiyo), re-checked 2026-09-15 against the
source as last modified 6 September 2026. Ranked 2026-09-14 by feasibility for
model-driven work (multilingual reading, historical cribs, cross-referencing digitised editions, fast solver
building), not by the repo's existing tooling. Status: `todo` · `active` · `solved` · `found-solved` (already in
print, catalogue wrong) · `stuck` · `offline-only` (needs archive access or copies; nothing more can be done online) · `infeasible`.

| # | Target | Date | Difficulty | Status | Dir | Notes |
|---|---|---|---|---|---|---|
| 1 | Richelieu → M. de Rancé (BnF fr. 3829 ff. 87, 89) | 1629 | Medium | solved | `richelieu/` | Ciphertext-only reconstruction of the homophonic alphabet + nomenclature; agrees word for word with Avenel 1858 (found afterwards); DECODE R9461-2 should be marked deciphered |
| 2 | Armstrong → Madison postscript (30 Aug 1808, THE=972 code) | 1808 | Medium | solved | `armstrong/` | 2026-09-14: "Russel ought to be the consul: he is an American by birth, and is much better qualified than any other candidate. In a word, he is above men in general. Next to him in fitness is O'Mealy, but he is, like Warden, an Irishman." Key = pencil interlinear decodes on DUSMF M34 roll 13 + alphabetical-slot inference; 49/49 groups (555 read as slip for 1555 *man*). 22 Feb 1808 letter (99-01-02-2733) also largely read |
| 3 | Charles II → Duke of Hamilton | 1650 | Medium | offline-only | `hamilton/` | Not solvable online: 102 groups, no redundancy, no printed key (Camden 1880 has none). Key located in the archive: NRS **GD406/1/2197** "Keys for ciphers used in the correspondence of the Duke of Hamilton", 5 items, open; letters = GD406/1/10573-10576 (Hamilton Red Book ii 156-159, microfilm on site). Needs a copy order to Edinburgh |
| 4 | Colbert passages (Mélanges Colbert) | 1665–74 | Medium | stuck | `colbert/` | Three short passages (Gravel? 1665 · Charost 1673 · Gravel→Maulevrier 1674); no key online, too short for cryptanalysis, all 12 known Colbert-series keys already fail; sibling-letter search needs Gallica paging (Gallica down during session). See colbert/NOTES.md |
| 5 | Prince Rupert → Maurice | 1645 | Medium | offline-only | `rupert/` | Full ciphertext from Warburton iii.133 (93 groups, max 398); known Rupert keys don't fit; the key would be in BL Add MS 18980-82 / 72438 — digitised but offline since the BL cyber-attack (IIIF 403); DECODE images need login + BL permission |
| 6 | Royalist intercepts, BL Add MS 72438 ff. 9-10 | 1646 | Medium | offline-only | `rupert/` | Ciphertexts themselves not online (DECODE R8623-4 private; BL images offline); the same volume holds 49 captured Digby keys (ff. 25-99) that would almost certainly read them once images are accessible |
| 7 | Maltravers → Ormonde | 1634–35 | Medium | partial (alphabet solved) | `ormonde/` | Nulls 91-111; regular block alphabet (consonants x3 from 7, vowels from 64) recovered via consecutive-figure doublets; angry / letters / Crosby / a councellor read; 186=Lord Deputy, 174=Ormonde, 221=Parliament inferred; 9 codes contextual. Write-up: docs/ormonde.html |
| 8 | Hyde superscriptions | 1659–60 | Easy | found-solved (explained) | `hyde/` | Hyde→Barwick letters in Vita Barwick 1721 with full key (THE=370, 1-692); superscriptions decode to nothing / exceed the key; 1724 editor: dummy numbers "only to puzzle the Enemy". Not a cipher. docs/hyde.html |
| 9 | Thurloe intercepts (Dutch, French, English) | 1653–56 | Medium-Hard | stuck | `thurloe/` | 4 pieces (136 / 22 / 16 / 50 groups); all cryptiana 1653-60 keys fail; Dutch/French hill-climb on 1653 letter gives fragments only; Rawlinson A originals not online |
| 10 | Stepney → Earl of Manchester | 1702 | Medium-Hard | offline-only | `stepney/` | MS located & transcribed (Yale OSB MSS fc37 box 8 f.40, IIIF; 24 groups, 413 not 412); THE=454 Manchester key rejected; key = "Mr. Stepney's cipher" (asked for Aug 1701) in TNA SP 105/106 or BL Add MSS 7058-78. 2026-09-15: Schmeh's Top 50 entry 34 cites a **Manchester cryptogram of Sept 1783**, 4th Duke of Manchester to **Sir John Stepney**, at the Clements Library - same two families a generation on. The library told a reader in 2017 that one letter is not enough and a corpus would be needed, which is the conclusion we reached independently here |
| 11 | Telegram to Sun Yat-sen, Swatow 3 Apr 1916 (JACAR B03050738800) | 1916 | Hard | solved | `sunyatsen/` | Systematic 20×5 code condenser (consonants alphabetical from l, vowels e a i o u, column-major 01–00, no additive) found by brute force over the family (57 600 keys) scored with a Chinese char LM; standard telegraph code. 41 chars: 潮城由莫擎宇獨立。我軍亦光復汕頭。後莫率大隊來，令我退出鎮守府。我軍力薄，暫由翼□支持。文慧返… (3 codes garbled). Huang Xing telegram (B03050731500) not attempted. docs/sunyatsen.html |
| 12 | Henry III → Segur | 1583–86 | Hard | blocked (Gallica access) | | BnF 500 Colbert 401; partial key |
| 13 | 1520s superscript-digit ciphers | 1526–29 | Hard | blocked (DECODE/BL images need login) | | Latin syllabic; Worcester, Gilino, Garbino |
| 14 | D'Estaing → Gerard | 1779 | Hard | skipped | `destaing/` | Clements Library, Clinton Papers |
| 15 | Le Tellier → Castelnau | 1657 | Hard | skipped | `letellier/` | syllabic, short |
| 16 | Ferdinand III ↔ Cardinal-Infante | 1634–40 | Hard | **found-solved** | `ferdinand3/` | 2026-09-15: this entry was stale. Solved by **Thomas Ernst in October 2017**, in the comment thread of Schmeh's own Top 50 post — a digit-pair code on the Habsburg AEIOU motto (01/02=A, 02/12=E, 03/13=I, 04/14=O), with each non-numeric sign encoding its count of strokes or semicircles. Nine years published. Second time a target has proved already solved in the open literature, after the Barney dictionary code |
| 17 | Switzerland telegram | 1937 | Hard | todo | | two short messages |
| 18 | Vatican Challenge Part 5 | 1542 | Hard | model class excluded | `vatican5/` | NEW: vowel-bearing digits identified as {7,0,3,1} (word-final enrichment + frequency mass, two independent signals agreeing with Italian to 3 dp). Constrained search still fails to converge (0.86 vs 0.80 chance) while a MATCHED synthetic of the same design, length and polyphony recovers its key at 0.93-0.97 -> the cipher is provably not a polyphonic single-digit substitution of Italian. Reading: mixed letters + unmarked multi-digit nomenclature; needs the key, not analysis |
| 19 | Enigma message | 1945 | Very hard | todo | | single message; compute-bound |
| 20 | Lüderitz FO telegram | 1911 | Infeasible | infeasible | | five-figure codebook |


## Where we are ahead of the source (2026-09-15)

The source page (last modified 6 Sept 2026) still lists these as unsolved. Results here are not yet reported to
Tomokiyo, who solicits contributions on the page.

| Source entry | Our status | Evidence |
|---|---|---|
| Richelieu (1629) | solved | `richelieu/`, docs/richelieu.html — agrees word for word with Avenel 1858 |
| Postscript in Code from Armstrong to Madison (1808) | solved, 49/49 groups | `armstrong/`, docs/armstrong.html |
| Ormonde-Maltravers Cipher (1634-1635) | alphabet recovered, partial read | `ormonde/`, docs/ormonde.html |
| Undeciphered Superscription by Hyde (1659-1660) | not a cipher — dummy numbers (1724 editor) | `hyde/`, docs/hyde.html |
| Telegram to Sun Yat-sen (1916) | solved | `sunyatsen/`, docs/sunyatsen.html |
| A Dictionary Code Used by Confederate Navy (1863) | found already solved by others, Aug 2026 (Webster's 1850) | `barney/` |

The source has caught up on one item since our ranking: **Union Ciphers during the Civil War (1862)** is now marked
Solved (Richard Bean with Claude Opus 5, 2026), matching our `milroy/` finding.

## Source entries not yet ranked here

The source carries roughly 60 unsolved entries; the 20 ranked above are a subset chosen for feasibility. The
remainder, for completeness, grouped by how promising they look with this repo's methods:

**Worth attacking next (tooling already exists or sources are printed/online)**
| Source entry | Date | Why |
|---|---|---|
| ~~Telegram from Huang Xing to Lin Hu and Li Genyuan~~ **DONE 2026-09-15** | 1916 | Scheme identified: 3 kana per character, each kana = one digit via its gojuon consonant row, vowel a free homophone (5 ways to write each digit) -> a private 3-digit codebook. Consonant-row triples collide 7x vs 1.03 expected (permutation p=0.006); vowels collide at exactly chance (p=0.70). Plaintext read off JACAR frames 0247-0248. See `sunyatsen/HUANG_NOTES.md` |
| Telegrams Found in a Sunken Ship Zhongshan | ca.1938 | Chinese telegraph code + condenser; same toolkit as Sun Yat-sen |
| William Perwich | 1670 | likely transposition; despatches printed by Camden Society 1903 (online) |
| ~~Charles I in the Isle of Wight~~ **ATTEMPTED 2026-09-15, still unread** | 1648 | Premise refuted: the two unread letters are NOT the same family. Published Biermann/Bosbach/Brown key excluded on both - coverage 43%/48% uninterpretable vs 0% on the solved controls; language z=+0.09 (p 0.47) and +1.11 (p 0.14) vs +3.17/+2.34 on controls. The Titus key (Hillier 1852) also excluded: Titus puts 18.3% of groups in 98-203 and 11.5% above 416, the Worsley letter none in either; 0 of 200,000 draws reproduce it. 43%/59% hapax means no analytic route. Needs the key itself. See `charlesi/NOTES.md` |
| ~~Encoded Letter from Berthier to Napoleon~~ **ATTEMPTED 2026-09-15, blocked on one article** | 1812 | Premise half-right. Napoleon's printed correspondence holds his OUTGOING letters, so a staff letter to him is not in it - but Chuquet, *1812, la guerre de Russie*, 3e serie (1912) pp.165-219 prints Berthier's December 1812 letters to Napoleon in clear, from AF/IV/1643, the same carton as the cryptogram; two are dated 22 December. Archive pinned to AF/IV/1643 plaquette 1/VI. Cipher is ~1200 entries, 64% hapax - not attackable. Blocker: full ciphertext exists only in Vilcoq, *Revue Historique de l'Armee* no.4 (1969), not digitised. Also found: cryptiana's two pages disagree on one group (356 vs 656). See `napoleon/NOTES.md` |
| ~~Encoded Letter to Marshal Marmont~~ **ATTEMPTED 2026-09-15, no ciphertext exists online** | 1807 | Dead until the source is obtained: cryptiana prints only the opening clear line and NO code groups, and Vilcoq 1969 is the sole source. Likely tractable once in hand (Marmont's 1811 code had ~150 entries, two-digit figures mixed with plain letters). Papers are at SHD, not the Archives nationales - the Dalmatia/Illyria series left AF/IV for the depot de la Guerre in 1830. See `napoleon/NOTES.md` |
| Japanese Coded Telegram Decoded by Yardley | c.1920 | Yardley printed the plaintext; scheme recoverable |

**Ranked lower (short, key-dependent, or archive-bound)**
English: Throckmorton (1559) / Wool (1568) · Moray-Wood (1568) · SP53/16 no.78 · SP53/16 no.79 · SP53/22 f.52 ·
Walsingham-related ciphers.
Spanish: postscript to Ferdinand's letter (1498) · Charles V letter (1521?) · Simancas EST,LEG,1381,180 · 1381,143.
French to 1610: Catherine de Medicis to du Croc (1567) · Birago to Nevers (1571) · Blancmesnil to Nevers ·
Marie de Medici (1610).
French/Italian/Spanish: Venetian letter in Spanish archives (ca.1589) · Cocquet (1616) · Fra Guglielmo Vizani (1637).
German: King of Hungary and Bohemia (1634) · "More ciphers of Ferdinand III?" · variable-length figure code,
Austrian archives (1627, 1644) · Starhemberg (1758).
French 17th: Prince of Conde (1654).
English Civil War: Ormond-Arran (1678) · Charles I-Boswell (1643) · Richard Forster (1644) · Charles I and
Henrietta-Maria private cipher (1645) · letter to Prince Rupert (1648) · intercepted letter of Hyde (1659) ·
"An Intercepted Letter".
French 1690-1710: ambassador in Rome (1690) · Catinat (1691) · Geertruidenberg (1710) · Villars and Polignac (1710) ·
Catinat (1702).
American: Armstrong to Madison, 20 Feb 1808 (the outlier code — different from the postscript we solved; a 2025 AFIO
contest solution is disputed by Tomokiyo).

## Famous unsolved ciphers (Elonka Dunin's list), ranked on the same scale

Source: https://elonka.com/UnsolvedCodes.html. Added 2026-09-15. Most rank low, and the reason is worth stating:
the famous ones are famous either because they resist every method, or because they are undeciphered *writing
systems* rather than concealed messages, which is a problem for linguistics and not for cryptanalysis.

| Item | Date | Odds | Why |
|---|---|---|---|
| Chinese gold bar ciphers, Shanghai | 1933 | low | The one that suits this project: mixed Chinese/Latin script, banking context, Chinese telegraph code and a reader of the language are what is wanted. Short inscriptions, poor photographs, disputed provenance |
| D'Agapeyeff cipher | 1939 | low | 196 digit pairs; the author forgot his own method, so a real cipher exists. Likely Polybius plus transposition. Eighty years of attack; may be too short for a provable solution |
| Dorabella cipher | 1897 | very low | 87 symbols; many readings fit, none provable |
| Kryptos K4 | 1990 | very low | The most worked-over 97 characters in existence; Sanborn sold the solution privately in 2025 |
| WWII pigeon cipher | 1942? | none | GCHQ assesses one-time pad, i.e. information-theoretically secure |
| Voynich manuscript | c.1420 | not a cipher? | Six centuries and a whole field have found no key; evidence now favours a constructed or glossolalic text |
| Phaistos disc | c.1800 BC | not a cipher | Undeciphered script with a corpus of one object |
| Linear A | c.1800 BC | not a cipher | Unknown language; Linear B fell only because the language was Greek |
| Indus script | c.2600 BC | not a cipher | ~400 signs, inscriptions average five characters, no bilingual, may not encode language |
| Rongorongo, Etruscan, Proto-Elamite, Meroitic | various | not ciphers | Undeciphered writing systems; Meroitic can be read aloud without being understood |
| Beale papers | 1885 | fabrication | Concluded here: see `beale/` |

Already closed from that list: Feynman ciphers 2 and 3 (Vierra 2023, verified here), Zodiac Z408/Z340,
Poe's challenge ciphers, the Chaocipher, the Smithy code, the Cyrillic Projector.

## Klaus Schmeh's "Top 50 unsolved encrypted messages", scored on the same scale

Source: https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/
Cross-referenced and re-checked 2026-09-15; full working in `top50/NOTES.md`.

The list ran as a post series, one article per entry, **8 Feb 2017 to 12 Apr 2020**, so solve status
has to be measured per entry. Cipherbrain closed 31 Dec 2022 and **the index page was never
retro-annotated** — it still calls Rivest's timelock unbroken though Schmeh posted the solution
himself in 2019. The index cannot be used as a status source.

**Nine of the fifty are closed and the list does not say so**: 48 Rivest timelock (Fabrot and
Cryptophage, 2019), 42 Bonus 22 M-209 (Lasry, Jan 2018), 35 Thouless (Richard Bean, Aug 2019, book
cipher on *The Hound of Heaven*), 32 silk dress (Wayne Chan, 2023 — US Army Signal Service weather
code, 27 May 1888), 27 Ferdinand III (Thomas Ernst, Oct 2017), 15 Rilke (not a cipher — QWERTZ
typewriter keys), 14 Codex Seraphinianus (asemic, per the author), 21 YOG'TZE (case closed Apr 2025),
and **39 Riverbanks Ripper, which is an April Fools' joke** — posted 1 April 2017, ciphertext one
character, transcriber credited as "George Fabyan", first murder set in Geneva, Illinois, home of
Riverbank Laboratories. It has sat unmarked for nine years.

Sixteen more are open but not settleable by cryptanalysis (Voynich, Kryptos K4, Zodiac Z13/Z32,
Somerton, Rohonc, Dorabella, pigeon, McCormick, Shugborough, Blitz, Cylob, Untersberg, Fair Game,
Powers, and the two compute challenges). Those are listed in `top50/NOTES.md`, not scored here.

### Worth attacking

| # | Target | Odds | Why |
|---|---|---|---|
| 46 | ADFGVX residue, 1918 | **high** | The sleeper. Lasry, Niebel, Kopal and Wacker broke the Childs corpus and published the keys, so these 22 are not unbroken ciphers but *mutilated transmissions against known keys*. 12-13 were read in the 2017 comment thread by Biermann, Armin, Baertl and Lasry; Schmeh promised a consolidating article and never wrote it, so **no clean table of which are solved has ever been published** and ~9-10 were never touched. ~3,964 letters available |
| 28 | Thomas Urquhart's poems | **high** | Numeric book-cipher shape (distich 64 numbers to 70; octastich ~272 to 201), Urquhart's printed corpus finite and digitised. **A live dispute to settle**: Vals AI announced 31 Aug 2026 that Claude Fable 5.1 solved the distich against the *Proquiritations*; Reticuli Labs rebutted on 1 Sept 2026 (rule fails at 10 of 64 positions, scores at chance, and the distich is absent from the verified 1653 text). No expert has adjudicated. The octastich is untouched |
| 19 | Kaliningrad bottle post | **high** | ~1,000+ characters over seven sections, far the most text of any open entry and the only one with enough for statistics. 37 symbols, IC ~0.054, consistent with Russian. **An unpublished crib claim is outstanding** — a 2021 commenter said the plaintext is from the 1876 Synodal Bible and never showed the method. Directly testable |
| 3 | Debosnys, 1882-83 | **high** | Four cryptograms, few hundred symbols, and almost nobody has worked on it. **No complete machine-readable transcription exists** - that is the stated bottleneck and it is a vision task on six public scans. And Debosnys was shown in 2021 to have plagiarised his unencrypted poems and paintings, so the ciphertexts may conceal copied published text: a known-plaintext hunt of the `beale/` kind |
| 47 | Köhler, Abwehr 1944 | medium | 921 letters over five messages, a decent corpus here. System unknown; Enigma variants exhaustively excluded. Published as an image only, so transcription comes first |
| 8 | Catokwacopa, 1875 | medium | Two *Evening Standard* ads, the second intelligible only with the first; full transcriptions published. Live thread on klausschmeh.net since Aug 2026. Interleaving of two streams with omitted letters, not substitution; partial readings disputed |
| 33 | Censorship manual steganograms | medium | Already partly solved in 2017 (Morse in pen strokes on the Amsterdam map, matched to the manual's own gloss). Residue is well specified: the fashion drawing's Morse, and the exact German plaintext. Originals TNA KV 2/2424 |
| 12 | Scorpion letters, 1991 | medium | ~250 symbols over two homophonic ciphers; S2-S4 withheld by police. The Z340 break shows what searching transposition as well as substitution can do |
| 23 | Copenhagen cryptogram | medium-low | 107 characters, 25 symbols, four apparent sentences. Simple substitution and almost certainly **not English** - Danish is the obvious candidate, which makes it a multilingual language-model problem. The ACA never even wrote it up |
| 18 | Moustier altar inscriptions | medium-low | ~100 characters. Huylebrouck's 2022 Trithemius *Ave Maria* hypothesis is testable, but Ernst's caution is serious: letter extenders and four distinct L-shapes mean the standard transcriptions may conflate symbols |
| 17 | Roosevelt cryptogram, 1935 | medium-low | Letter part fell in 2015 ("DID YOU EVER BITE A LEMON?"); the open residue is ~115 digits. Ernst's 2017 claim that it is a doodle, because the joined pairs give 43 numbers covering 10-52 exactly once, is a blog comment and is checkable |

### Ranked lower

| # | Target | Odds | Why |
|---|---|---|---|
| 29, 30 | Pollaky; Harry-Caroline and Tissie-Jabber | low | Victorian agony-column ads, scans public, ten words each. Tissie-Jabber's groups over {a,b,c,d,n,o} may not be letters at all. Pollaky destroyed his records |
| 16 | Lima, Ohio robbery, 1916 | low | ~110 letters, and variant transcriptions are a genuine obstacle; the 2025 partial readings are mutually inconsistent |
| 9 | Rubin, 1953 | low | One typewritten slip; contains the plaintext names "Dulles" and "Conant". No claimed solution of standing |
| 7, 31, 44 | Cigarette case 1909; MLH 1974; bullet 1944 | low | Four engraved lines; four lines of symbols; 44 letters. All far too short |
| 43 | Rayburn, 2004 | low | ~80 mixed characters, all underlined or struck through; plausibly a handwritten **password list**, not a cipher |
| 25 | SS radio message, 1944 | low | Six lines, and probably a **forgery** - wrong typography, wrong SS rank abbreviations, anachronistic stamp |
| 24 | Erba murder, 2006 | low | Blocker is sourcing: only a press photograph, no authoritative transcription |
| 38 | Sufi Fiddle | low | Seven lines of unidentified script, **no transcription ever published**, and provenance rests on a novel's afterword. Palaeography before cryptanalysis |

## Done elsewhere in this repo
| Target | Status | Dir |
|---|---|---|
| Beale Paper No. 1 | fabrication (evidence in notes) | `beale/` |
