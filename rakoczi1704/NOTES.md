# "Ferenc Rákóczi II to unknown recipient, 4 ciphertexts" — DECODE R483, R852, R912, R922

Status: read. The three French letters (R852, R912, R922) are reports *to* Rákóczi. R912 and R922 read with the
preserved key DECODE R639 at about 97% of groups from a fresh transcription of the images. R852 has its own clear
copy. The Latin letter R483 is Rákóczi's own (Lwów, 27 June 1711). It carries an interlinear decipherment, and its
syllabic key has been rebuilt from that decipherment.

Catalogue item 44 (class B, scored by rule). All four records are MNL OL, and the images are not in the public
domain, so none is reproduced. Worked 21 Sept 2026. Pass 1 used DECODE's text transcriptions. Pass 2 fetched the
images (`fetch_img.py`, into the git-ignored `img/`) and re-transcribed every cipher page into `tr/`.

## Correction to the catalogue

DECODE gives Ferenc Rákóczi II as the author of all four. That holds only for R483. R852, R912 and R922 address
"Monseigneur" and "Votre Altesse" and report on Rákóczi's affairs at the Polish court, so Rákóczi is their
recipient, as with R902 (`../rakoczi1707/`). The catalogue's "1704–1711" is DECODE's span for the volume.

## The French letters and the Bonac–Groffey key (DECODE R639)

The key is a one-part numerical nomenclator, codes 10–560. The twelve odd numbers 97–119 are nulls. The groups of
500 and above that open a line (563, 564, 574, 589, 607, 609, 620 …) behave as nulls too.

Reading the key image (`img/IMG_R639_I3927_P1.png`) corrected DECODE's transcription of the table:

- S is 44, **45**, 100, 83 and T is 46, **47**, 102, 85. The 45 and 47 are overwritten on the sheet, and DECODE
  read them as 95 and 96. On the sheet, 95 belongs to *es* and 96 to Q.
- Z is 54, 55, 110. DECODE wrote "100/110?", which made the old decoder drop the whole Z line, and with it 55.
- The table's numbering jumps from 172 (Da) to 175 (de). The letters use **173 and 174 as "de"** throughout
  ("le Roy 173 Pologne", "Palatin 174 Belz"). Grade C.
- **561 and 562 = "nt"** (after *poi-*, *souve-*), beyond the end of the table. Grade C.

`decode_tr.py` applies the corrected table to the new transcriptions. The old `decode.py` output on DECODE's
transcription, `R*_key08_read.txt`, is kept for comparison.

| Record | Shelfmark (G15 Caps. C. Fasc. 39) | Date | Groups (image) | Keyed | Pass 1 (DECODE text) |
|---|---|---|---|---|---|
| R922 | pp. 346–347 | Dantzig, 28 Oct [1707] | 722 | 705 (97.6%) | 683/730 |
| R912 | pp. 312–314 | "au quartier", 5 Nov [1707] | 1,630 | 1,586 (97.3%) | 1,473/1,596 |
| R852 | pp. 115–117 | Dantzig, 22 Jan 1706 | 523 | clear copy on pp. 116–117 | 497/513 |

Unread in R912 and R922: 61 groups. They are line-opening fillers of 500 and above, the closing and signature
block of R912 p. 3 (`589 4 5 710 607 3 586 1000 …`, probably a date and a name in figures), and a handful of
values outside the table: 93 (×3), 89 (×3), 9 (×2), 3–8 and 699. The re-transcription corrected about 40% of
DECODE's lines. It found a line DECODE had dropped in each of R912 and R852, repeated runs, merged groups, and the
misreadings 350/380, 324/329, 489/459/497 and 687/607.

**R852 uses a different issue of the table.** Its letters and syllables agree with R639, but many of its word
codes, mostly those ending in 4 (144, 254, 194, 404, 294, 314, 424 …), mean something else: 144 = *de*, 254 = *la*
where R639 gives *beaucoup*, *jusque*. The letter's own clear copy (p. 116 and the top of p. 117, read from the
image into `R852_clear.txt`) supplies the text, so the variant table has not been rebuilt. The date is written
"22 janvier 1706". It speaks of "l'action", probably Zsibó (Nov 1705).

### What they say

- **R852** (Dantzig, 22 Jan 1706). The writer acknowledges Rákóczi's letter of 26 December and will pass letters on
  "au Sr. Groffey". He vouches for Groffey's loyalty and prudence. He waits for "le Sr. Roth." to join him. He asks
  for a weekly Latin paper like the *Mercurius hungaricus*, because every German and Dutch gazetteer "destroys the
  Kingdom of Hungary at his ease", and in Berlin people believed that no Hungarians were left after "l'action".
  Bercsényi ("Bertoti") could print the news and send it by way of Cracow. P. 117 adds a short clear note offering to
  register M. de Bonnac's letters and bills of exchange for Rákóczi.
- **R922** (Dantzig, 28 Oct [1707]). The writer reports a sale carried out for Madame la Palatine de Belz (Elżbieta
  Sieniawska), with an authentic copy sent to the sieur Kray. He has kept out of the business "as far as possible, by
  my credit and my advice". There are orders for carbines. He is leaving to join the King of Poland and asks that
  Kray be given orders so that he can continue "mes services à la Cour de Pologne". P. 2 covers money matters and a
  prisoner.
- **R912** (5 Nov [1707]). A survey of Polish and Swedish politics: King Stanisław, the Palatine of Belz and the
  Grand Hetman, the Muscovites under the Field Hetman, the King of Sweden's pacification and a new election, the
  Tsar, and Rákóczi's letter to Rehnskiöld (the affair of R902). The Palatine of Ruthenia and a regiment asked of
  Rákóczi, which Stanisław and the Germans hold against him, also come up, as do Tököly and his siege.

Writer: unsigned. R852's writer names Groffey in the third person and was at Danzig. R922 is also from Danzig and
may be the same man. Grade M. The key heading *De Monsieur de Bonac et Graffei* suggests that the key served the
whole Bonac–Groffey correspondence.

## R483: Rákóczi, Lwów, 27 June 1711 (Latin)

P237 Festetics 10. d. 2. 42–44, 6 pp., 2,531 cipher groups in 180 lines (transcribed from the images, `tr/R483_p*.txt`,
with the clerk's interlinear on the `P:` lines). The letter is signed in autograph "Franciscus Princeps" and dated in
clear "Leopoli die 27. Junii Anno 1711". DECODE's "7 June" is wrong. It is addressed to "Fidelis nobis sincere
dilecte", an envoy on his way to Holland who is in poor health and handles money and the mathematical instruments
ordered from Mangold. A clear postscript deals with those instruments.

**Key rebuilt.** `align483.py` aligns every cipher line with the interlinear by hard EM, with each code taking
0–4 letters. It gives 224 codes (`R483_key_rebuilt.json`), 156 of them seen at least twice. It is a syllabic cipher
with homophones: single letters (190/430 s, 140/380 n, 60/300 e, 20/260 a, 130/370 m), open syllables (257 re,
428 ti, 68 se, 362 de, 96 no, 457 ri, 148 si, 92 ce, 152 co, 59 tu, 378 ta) and a few words and names.
Decoding with the rebuilt key (`check483.py`, output `R483_key_read.txt`) reproduces 70% of the clerk's letters.
The mismatches are rare codes, homophones seen once, and the clerk's own abbreviations. Where the clerk's words
are doubtful, the key often settles them: "nos Regem extra dietam promulgatum non deposito [juramento] agnoscere
non posse sine … ruina [libertatum nostrarum]", and "ne fors etiam".

Content. P. 1: Rákóczi sends a copy of the "Tractatus sic dictae Pacis Carolianae" (Szatmár), which he calls a
fraud engineered in Vienna, and reports that Archduke Charles was proclaimed king in every Hungarian county,
contrary to the 1687 article of the Pozsony diet. P. 2: he will not recognise a king proclaimed outside a free diet.
He appeals to the Tsar and the Polish Republic to mediate. He offers to come to a free diet in person or by
plenipotentiaries and to recognise a lawfully crowned king, provided the confederates are restored to their
estates. P. 3: the Allies' assurances about Hungarian liberties were a "diversio armorum" for Austria, and the war
must go on. P. 4: Pálffy's artillery against "arcem nostram Munkatsiensem", and the restitution of Transylvanian
liberty. P. 5: the general confederation in Poland, letters to go "per Saxoniam", the Muscovite advance, a warning
to trust only news sent directly from Rákóczi, complaints about the Grand Chancellor's "indiscretum procedendi
modum" and about Ráday, and letters from the Chancellor at Dukla. P. 6: receipts left with a Jew, and a member of
the Economic Council who took treasury money for his own use.

Open: an edited Latin text line by line. The material for it is here (clerk plus key reading). The key's
single-occurrence codes (68 of 224) are grade C.

## Files

- `fetch_decode.py`, `fetch_img.py`: fetch the DOC transcriptions and the images (cookie from `../bordeaux/decode/`).
- `tr/`: new transcriptions from the images (R922 p1–2, R912 p1–3, R852 p1–3, R483 p1–6).
- `decode_tr.py`: the corrected R639 table. `R922_image_read.txt`, `R912_image_read.txt`: readings.
- `R852_clear.txt`: the contemporary clear copy of R852.
- `align483.py`, `check483.py`, `R483_key_rebuilt.json`, `R483_key_read.txt`: the R483 key and reading.
- `decode.py`, `R*_key08_read.txt`: pass 1 on DECODE's transcriptions.
