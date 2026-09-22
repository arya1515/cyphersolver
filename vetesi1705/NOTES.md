# László Vetési Kökényesdi to Ferenc Rákóczi II, 9 January 1706 (Ráday Archives C64-4d2-10, 92-95; DECODE R473)

Status: no write-up. Read at the time: the letter carries a contemporary interlinear decipherment over its cipher
runs, and the archive's own note cites it to the printed edition *Ráday Pál iratai* I (1955). Nothing new was read
here beyond correcting the date.

Catalogue entry 52 (class B, scored by rule): "László Vetési Kökényesdi (alias Casimirius de Miloftzky) to Pál
Ráday, Ferenc Rákóczi II, 1 Jan 1705". Worked 21 Sept 2026. The images are not in the public domain (Ráday
Archives), so they are kept in the git-ignored `img/` and not reproduced.

## What the record is

DECODE R473 (`RAD_ARCH_Rakoczi_C64_4d2_10_92`) has three images (3612–3614) and a DECODE text transcription
(`DOC_R473_D3610_3610.txt`, by "MA", 21 Dec 2020). The letter is in Hungarian: clear text with numerical cipher
runs (one-part syllabic homophonic nomenclator, codes about 1–1190 plus dotted groups such as 2670, 6670, 2100).
It opens "Fejedelem … Nagyságod" (Prince, Your Highness), part in cipher, addresses him as "Kegyelmes Uram", names
"Ráday uram" in the third person, and is signed "Cassimirus Miloftzki". The addressee is therefore Rákóczi;
DECODE's receiver "Pál Ráday" reflects where the letter is kept (Ráday was Rákóczi's secretary).

A contemporary hand wrote the decipherment above almost every cipher group: "Francziaország", "Olaszországban",
"Spaniolországban", "Holandia és Anglia", "November", "December", "Ráday uram". This is the "partially decrypted"
of DECODE's status. The letter was read at the time.

## Date

DECODE's "1 Jan 1705 – 1706" is a placeholder span. The closing (image 3614) reads *Költ [2100.1560.500.670]
Kilencedik Januarii [357.1000.06]*, "given at [place, in cipher, unglossed] on the ninth of January", and the
archival endorsement at the head of image 3612 reads **1706 I. 9**. The letter is dated 9 January 1706.

## Prior publication

The pencil note at the head of image 3612, "H.ö. R.I. 102 a 1 jegyzet. 494. p.", refers to *Ráday Pál iratai I.
1703–1706* (ed. Benda Kálmán, Maksay Ferenc et al., Budapest: Akadémiai, 1955), item 102, footnote 1, p. 494.
The edition is on Szaktárs behind a paywall (403 here), so whether it prints this letter in full has not been
checked. The interlinear decipherment is enough on its own to make this "read at the time".

## What was tried

- `fetch_img.py 473`: record page, transcription and images.
- `align.py`: hard-EM alignment of each cipher run against DECODE's transcription of the interlinear gloss, to
  rebuild the key (`key_rebuilt.json`). The result is noisy: DECODE's transcription of the glosses is poor
  ("Fejedehd" for *Fejedelem*, "ttolendia" for *Hollandia*), and 154 of 373 groups sit in runs whose gloss count
  does not match. The key is not rebuilt. A clean rebuild would need a fresh hand transcription of the three
  pages. That would fill the few unglossed groups (the place in the date line, a handful of single groups), but
  the letter's content is already on the page.

## DECODE correction queued

Status Partially → Decrypted (interlinear, read at the time), date 9 Jan 1706, sender Vetési Kökényesdi (as
"Cassimirus Miloftzki"), receiver Ferenc Rákóczi II (kept in Ráday's papers), reference *Ráday Pál iratai* I (1955) p. 494 n. 1 (item 102).
