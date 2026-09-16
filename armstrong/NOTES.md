# Armstrong -> Madison, coded postscript of 30 Aug 1808 (THE=972 code) — tracker item #2

## Result: solved — 48 of 49 code groups determined, the 49th a probable slip (2026-09-15, two sessions)

    P.S. Ru-s-el ought to be the consul: he is a-n America-n by bir-th, and is much better
    qua-li-fi(ed) than any other can-di-da-te. In a word he is above men in general. Next to
    him in fit-ness is O-mea-ly, but he is like Ward-en an Ir-ish-[man].

> Russel ought to be the consul: he is an American by birth, and is much better qualified than any other
> candidate. In a word, he is above men in general. Next to him in fitness is O'Mealy, but he is, like Warden,
> an Irishman.

Reproduce: `python decode972.py ps` (grades: plain = H pencil or C known plaintext, `?` = M uncertain, `*` = inferred).
Full write-up with the group-by-group table: docs/armstrong.html (§4).

### Grades of the 49 groups

- **Pencil decodes on M34 roll 13 and/or the 4 May 1806 known plaintext (H/C), 27 distinct groups:** 1116 s, 1165 to,
  1405 be, 972 the, 1459 he, 1482 is, 1201 a, 821 n, 1429 by, 970 th, 1319 li, 584 than, 687 any, 249 other, 736 can,
  1013 di, 750 da, 967 te, 1561 men, 927 him, 1090 in, 832 ness, 934 o, 510 mea, 860 ly, 1280 en, 1216 an, 1481 ir.
  Frame 0190 (second session) also gives **1320 like** as an H reading, so it is no longer inference-only.
- **Inferred from context and checked against the alphabetical slot (I), all fit:** 1394 ru (opens a new run after
  1393 purp; reads ru in three independent places: ru-in and Dan-ish in the 22 Feb 1808 letter, Et-ru-ria on frame 0201,
  Y-ru-jo on frame 0194 — so effectively H, recorded in `pairs.txt` line 215), 1273 el (1272 eight < el < 1279 Emp),
  250 ought (249 other < ought < 252 own), 148 consul (146 confide < consul < 151 contrary), 130 America (new run after
  128 yesterday, before 137 between), 720 bir (719 Ba < bir < 723 bo), 992 qua (< 993 qui), 1048 fi(ed) (1046 fi … 1052
  fit), 1202 above (1201 a < above < 1209 Agent), 1052 fit (1050 fi < fit < 1062 fol), 384 Ward (383 w < ward < 385 was),
  1483 ish (1482 is < ish < 1484 it; Dan-ish).
- **The one doubt:** the last group is **555** in the manuscript and in Founders; 555 = re (frame 0195, sco-re), which makes
  no sense after Ir-ish, while **1555 = man** (frames 0195 and 0200, `pairs.txt` lines 119 and 457). Read as a dropped
  digit for *Irishman*; the alternative, that the postscript breaks off at "an Irish re…", is recorded for completeness.

### Corrections to the Founders Online transcription (from the LoC image, Madison Papers reel 10 frame 0521)

- Second line starts **972.** (the) in the manuscript, not Founders' "970." (th).
- Last line has **1216** (an) in the manuscript, not Founders' "1218".
- A pencil *s* under 1116 on the LoC copy: someone in Washington began and abandoned a decode.

### The people

- **Russel** = Ru-s-el: most probably Jonathan Russell of Providence, R.I. (1771–1832), whom Madison did appoint chargé
  d'affaires at Paris when Armstrong left in 1810. Inferential: no other document places him in France in 1808.
- **Warden**: David Bailie Warden (1772–1845), born in County Down, secretary of legation, got the Paris consulate;
  Armstrong removed him in 1810 and protested his reinstatement in 1811 ("without a single grain of attachment to the
  U.S.", 3 March 1811). The postscript shows the same animus three years earlier and gives its cause.
- **O'Mealy**: Michael O'Mealy, Baltimore merchant resident in France since 1793 (Papers of James Madison, Secretary of
  State Series 10:497 n. 2).

An earlier version of these notes read the subject as "S." = Skipwith and 1394 as a null; both were wrong. 1394 is *ru*
(the clerk's pencil dash over it marks a syllable continued from the word written over the preceding group), and the
subject is Ru-s-el.

## How: the codebook was reconstructed from NARA DUSMF microfilm M34 roll 13 (naId 188671172, `img13/`),
where the State Department clerk's pencil decode is written above each cipher number of Armstrong's 1806–07
despatches, above all the October 1806 political despatch on frames 0192–0201 (located by `pencil_score.py`, which
ranks frames by faint mid-grey pixels away from ink). Pairs were read frame by frame and recorded in `pairs.txt`
(584 lines, each with frame/line reference and H/M grade; about 352 read with confidence); `decode972.py` merges them
with Tomokiyo's partial table from the 4 May 1806 known-plaintext letter (`code972_partial.json`, 227 entries) and the
INFER dictionary of slot inferences, ranking H > C > M > I, into a table of ~580 distinct groups (`python decode972.py
table`; `export_key.py` writes it as `key972.js` for the site decoder). The 1808–10 roll 14 (naId 188671566) is NOT
decoded except a faint pencil line under the 22 Feb 1808 postscript.

**Control text:** the private letter of 22 February 1808 (Founders 99-01-02-2733), ~150 groups in the same code and
sharing no groups of interest with the known-plaintext letter, reads with gaps with the merged table ("The ruin of
Gustavus is at last resolved. Russia is to seize Finland, while France & Denmark take possession of Sweden…"), and
fixes ru, ish and Russia (305). Two probable single-digit slips there: Founders' 631 (wise) for 651 (plain) in
"com-plain-t-s", 916 (had) for 921 (have). One anomaly: 946 is *on* in the 4 May 1806 letter but must be *Gu* in
Gustavus (914 = gu elsewhere) — homophone or slip.

## Second session (2026-09-15): the roll-13 frames were re-fetched through the catalogue proxy
(`https://catalog.archives.gov/proxy/records/search?naId=188671172` lists the 393 object URLs, saved in `img13/objects.json`;
the images are `.../medialz/dc-metro/rg-059/603720/M34/M34-013/M34-013-NNNN.jpg`). Frame 0190 (Paris, 20 July 1806,
"A peace was signed last night between Russia and France ... this looks like peace between England and France also")
carries a full pencil decode and gives **1320 = like** (H), plus 1492 last, 835 night, 801 about, 679 look (H) and
512 media (M).

## What is left (not needed for the postscript)

- Frames downloaded but not yet read, which may turn the remaining I grades (1273, 250, 384, 1483, 992, 1048, 148, 130,
  720, 1052, 1202) into H: 0011-0012, 0016-0017, 0021, 0027, 0034-35, 0058-59, 0096-97, 0109-10, 0121-22, 0140-43,
  0150-51, 0160, 0188-89, 0191-92, 0223-25, 0232-38, 0289 (dense pages such as 0233 need 600 dpi crops line by line).
- The LoC image of the postscript (mjm015002) is still Cloudflare-blocked to scripts; it was collated by hand.
- The 20 Feb 1808 letter (different, unique code; cryptiana's other Armstrong item) was not attacked.
- The ~40 other coded Armstrong despatches of 1804–10 in rolls 13–14 can now be read with the table.
