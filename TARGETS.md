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
| 10 | Stepney → Earl of Manchester | 1702 | Medium-Hard | offline-only | `stepney/` | MS located & transcribed (Yale OSB MSS fc37 box 8 f.40, IIIF; 24 groups, 413 not 412); THE=454 Manchester key rejected; key = "Mr. Stepney's cipher" (asked for Aug 1701) in TNA SP 105/106 or BL Add MSS 7058-78 |
| 11 | Telegram to Sun Yat-sen, Swatow 3 Apr 1916 (JACAR B03050738800) | 1916 | Hard | solved | `sunyatsen/` | Systematic 20×5 code condenser (consonants alphabetical from l, vowels e a i o u, column-major 01–00, no additive) found by brute force over the family (57 600 keys) scored with a Chinese char LM; standard telegraph code. 41 chars: 潮城由莫擎宇獨立。我軍亦光復汕頭。後莫率大隊來，令我退出鎮守府。我軍力薄，暫由翼□支持。文慧返… (3 codes garbled). Huang Xing telegram (B03050731500) not attempted. docs/sunyatsen.html |
| 12 | Henry III → Segur | 1583–86 | Hard | blocked (Gallica access) | | BnF 500 Colbert 401; partial key |
| 13 | 1520s superscript-digit ciphers | 1526–29 | Hard | blocked (DECODE/BL images need login) | | Latin syllabic; Worcester, Gilino, Garbino |
| 14 | D'Estaing → Gerard | 1779 | Hard | skipped | `destaing/` | Clements Library, Clinton Papers |
| 15 | Le Tellier → Castelnau | 1657 | Hard | skipped | `letellier/` | syllabic, short |
| 16 | Ferdinand III ↔ Cardinal-Infante | 1634–40 | Hard | skipped (DECODE login) | `ferdinand3/` | Brussels; Latin/German |
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
| Charles I in the Isle of Wight | 1648 | two of four solved by Biermann & Brown 2021; remaining two likely same family |
| Encoded Letter from Berthier to Napoleon | 1812 | Napoleonic petit chiffre; Napoleon correspondence fully printed |
| Encoded Letter to Marshal Marmont | 1807 | same family as above |
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

## Done elsewhere in this repo
| Target | Status | Dir |
|---|---|---|
| Beale Paper No. 1 | fabrication (evidence in notes) | `beale/` |
