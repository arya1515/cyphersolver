# Target tracker — unsolved ciphers from cryptiana's list

Source list: https://cryptiana.web.fc2.com/code/unsolved.htm (S. Tomokiyo). Ranked 2026-09-14 by feasibility for
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
| 12 | Henry III → Segur | 1583–86 | Hard | todo | | BnF 500 Colbert 401; partial key |
| 13 | 1520s superscript-digit ciphers | 1526–29 | Hard | todo | | Latin syllabic; Worcester, Gilino, Garbino |
| 14 | D'Estaing → Gerard | 1779 | Hard | todo | | Clements Library, Clinton Papers |
| 15 | Le Tellier → Castelnau | 1657 | Hard | todo | | syllabic, short |
| 16 | Ferdinand III ↔ Cardinal-Infante | 1634–40 | Hard | todo | | Brussels; Latin/German |
| 17 | Switzerland telegram | 1937 | Hard | todo | | two short messages |
| 18 | Vatican Challenge Part 5 | 1542 | Hard | stuck | `vatican5/` | paused after serious attempt |
| 19 | Enigma message | 1945 | Very hard | todo | | single message; compute-bound |
| 20 | Lüderitz FO telegram | 1911 | Infeasible | infeasible | | five-figure codebook |

## Done elsewhere in this repo
| Target | Status | Dir |
|---|---|---|
| Beale Paper No. 1 | fabrication (evidence in notes) | `beale/` |
