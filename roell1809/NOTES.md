# Roell (Amsterdam) to Van Dedem (Constantinople), 9 Feb 1809 — DECODE R1469, R1470

Status: attempted, open (no key, no decipherment, no crib; closed from the evidence 21 Sept 2026)

- **Source.** Nationaal Archief 1.02.04 legatie Turkije, inv. 804, two items. DECODE R1469 (7 images, 6681–6687,
  dated 1809-02-09) and R1470 (6 images, 6688–6693, undated). Catalogue entry "Willem Frederik Roell … to Frederik
  Gijsbert van Dedem tot de Gelder", scored by rule, class C.
- **Attribution** is DECODE's: the letters are neither addressed nor signed. The DECODE note already doubts it,
  since Van Dedem was on his way home when the letter was sent.

## What the records hold

The scans were checked page by page (`contact.png`, git-ignored). All 13 pages are code throughout. There is no
interlinear, margin or separate decipherment. The only clear words are an opening "Monsieur" (R1469) and a docket
on R1470 p.1 read by DECODE as "? 69 Fermer? no? 9?". Line numbers 5, 10, 15 are written in the margin. R1469 ends
on p.7 with a paraph.

## The code

Transcriptions: DECODE (SofPe, 2 Feb 2020), parsed by `parse.py` into `R1469_groups.txt` and `R1470_groups.txt`
(dots separate the groups; a few marks and uncertain digits are dropped).

| | groups | distinct | highest | most frequent |
|---|---|---|---|---|
| R1469 | 1,297 | 622 | ~3000 (one 7205, a misread) | 1390, 460 ×12 |
| R1470 | 1,288 | 707 | 3264 | 804, 75, 357, 296, 394 ×10 |
| both | 2,585 | 931 | | |

The language is French per DECODE; no plaintext confirms it. No group exceeds about 1% of the text, where French
*de* alone should be 4–5%. The code is therefore **heavily homophonic**. The frequent groups are spread from 35 to
2920, so it is not a one-part (alphabetical) code whose ranges could be predicted.

## What was tried

1. **DECODE keys.** The metadata dump (`catalogue_harvest/decode/views*.jsonl`) has no key record for the Turkish
   legation or for Roell's ministry. Only these two and the older Dedem letters match.
2. **Same code as Dedem 1788–93?** (`dedem1788/`, which has French cribs R1947 and R2053 and Dutch R2121.) No. Only
   30–33% of each crib's distinct groups occur here, against a 28% chance baseline, and just 0–5 of each crib's 30
   commonest groups are among the 200 commonest here.
3. **Van Spaen 1808 / Fagel 1804** (the ministry's other open codes of the period, `spaen1808/`, `fagel1804/`) use
   different systems: groups to 1339 unmarked, and syllabic groups with clear endings.
4. **Print and archives.** Colenbrander, *Gedenkstukken* V (1806–1810), turned up nothing by web search. Roell's own
   papers (NA 2.21.008.78, inventory PDF searched) hold letters *from* Van Dedem 1808–09 and from **S. F. Croiset,
   1808–09**, the Foreign Ministry's code-maker, but list no codebook.

A ciphertext-only attack on 2,600 groups of a homophonic word code with about 3,000 values is not realistic.
Compare Dedem 1788, where even ~1,300 groups of aligned crib gave no consistent key.


## Archive check, Nationaal Archief 1.02.20 legatie Turkije (online scans, 21 Sept 2026)

DECODE's "1.02.04 legatie Turkije" is the wrong archive number: 1.02.04 is Schonenberg's Portugal legation; the Turkish
legation is **1.02.20** (inventory `turk_inv.txt`). Its scanned items were checked page by page (scans git-ignored):

- **inv. 804** (174 scans): clear Dutch *copies* of the legation's letters to the States General, 1785–93. The cipher
  pages are not there; DECODE's "inv. 804" is probably an old number.
- **inv. 988** (123 scans), "Dépêches de S.E. W.F. Röell … à Monsieur Gaspard Testa, Chargé d'affaires … près la
  Sublime Porte", 1809–10: numbered, all in clear Dutch ("Mynheer"). No. 1 is 10 Jan 1809 (to Van Dedem), No. 2 is 14
  March, No. 3 is 17 March. **Röell sent no despatch of 9 Feb 1809 in this series, and he wrote in Dutch**, so R1469/R1470
  (French, "Monsieur") are probably not his.
- **inv. 990** (83 scans), Van Dedem's letters to Testa from Bucharest, Vienna and Holland, 1809–11: in clear French,
  "Monsieur" (Bucharest 17, 25, 29 Jan 1809…). No cipher and no decipherment seen.
- **inv. 980** (143 scans), copies of Testa's letters to Van Dedem, 1808–11: clear French, "Excellence"; copies of 10 and
  26 Feb 1809 but none of 9 Feb.

The "Monsieur" salutation and the French fit Van Dedem writing to Testa better than Röell, but no clear counterpart
of either cipher letter was found in these four files. The Croiset letters in NA 2.21.008.78 and Boon (2012) are
not online.

## What would move it

- The codebook: legation papers (NA 1.02.04 legatie Turkije, around inv. 804) or Croiset's 1808–09 letters in
  NA 2.21.008.78.
- Van Dedem's replies of 1809 in the same code with a clear copy, which would give a crib.
- Henk Boon, *Onze man in Constantinopel* (2012), cited by DECODE, was not checked.
