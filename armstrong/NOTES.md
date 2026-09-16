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
- The 20 Feb 1808 letter: see the adjudication section below (2026-09-16). Not readable with this table.
- The ~40 other coded Armstrong despatches of 1804–10 in rolls 13–14 can now be read with the table.

## The 20 February 1808 letter and the AFIO contest solution (adjudication, 2026-09-16)

**Verdict: the published solution does not hold.** It is a set of 56 word labels hung on 51 of the letter's 216 distinct
groups, and it fits its own sentence no better than a key fitted by the same procedure to a shuffled ciphertext.

The item: Armstrong to Madison, Paris, 20 Feb 1808 (Founders 99-01-02-2728; NARA M34 roll 14 images 29-32). Founders
prints 369 groups, 216 distinct, values 1 to 1900, with 35 passages in graphic symbols (shorthand-like) that no
transcription renders. Ciphertext saved as `feb20_ciphertext.txt` (Founders is now behind a CloudFront challenge for
scripts; the Wayback copy `web.archive.org/web/2025id_/https://founders.archives.gov/documents/Madison/99-01-02-2728`
works). The Association of Former Intelligence Officers announced on 27 May 2025 that Yaacov Apelbaum had decrypted it and
published a 60-word plaintext and a 56-entry key (saved as `afio_key.txt`; machine-readable form from Tomokiyo's
`madison_AFIO.txt`). Tomokiyo's article "An Outlier Code in Armstrong-Madison Correspondence (1808)" (cryptiana
`madison_armstrong.htm`, Oct 2025, rev. June 2026) already judged it unconvincing; this is the quantitative version.

### What the frames say

- Every coded despatch on the roll-13 frames read here (0034 = 18 Mar 1805 copy, 0097 = 10 Sept 1805, 0122 = 1806,
  0190-0201 = 1806, and the pencil-annotated pages generally) is in the THE=972 code, values below about 1600. No group
  in the 1700-1900 range, which the 20 Feb letter uses 49 times, was seen on any frame. The State Department clerk's
  pencil decodes therefore give the THE=972 key only; there is no pencil decode of the 20 Feb letter (Kreider: "we've
  found no evidence that it ever was decoded"), and Madison wrote to Jefferson on 15 May 1808: "The undecyphered letter
  from A. ... No such Cypher is in the office, and must be one concerted with another correspondent" (Founders
  99-01-02-3082, Kreider's identification). So "rebuild the claimed key from the frames" has a definite answer: the
  frames cannot yield it, because the key was never in Washington.
- Paired check with our table (`python decode972.py feb15` / the 20 Feb groups): the **15 Feb 1808** despatch, five days
  earlier, is in THE=972 and reads at once (176 of 243 groups H/C-known, 72 %: "with one [hand] they offer us the
  Floridas ... they do not accept this ... it is however merely an experiment; yet if it succeeds you will [see] a
  second ... In either case, do not suspend a moment the seizure of the Floridas"). The 20 Feb letter with the same
  table: 92 of 369 groups (25 %) hit, and the hits are noise ("roc de ion ... ward the native pos native like ct
  Monarch temp ..."). Two letters, one table, one reads and one does not: the 20 Feb code is a different code, as
  Kreider's team and Tomokiyo said.

### Scoring the AFIO key (`python adjudicate_feb20.py`)

| test | AFIO key | control |
|---|---|---|
| groups of the letter covered by the key | 133 of 369 (36 %); 51 of 216 distinct | |
| key numbers that never occur in the letter | 5 of 56: 6 *i*, 39 *written*, 131 *to*, 432 *its*, 1358 *that* | |
| plaintext words with no code group at all | 6 of 60: *seamen, examined, not, we, shall, receive* | |
| published text aligned in order against the key's rendering | 40 of 60 words, over groups 12-102 (page 1) | shuffled key: 18.9 mean, max 26 (passes, but trivially: the key was read off this page) |
| mapped occurrences inside that span the text does not use | 28 of 68 dropped (consistency 0.59) | key built by the same walk on a **shuffled** ciphertext: 0.70 +/- 0.18 |
| mapped occurrences over the whole letter the text does not use | 93 of 133 (share used 0.30) | same control: 0.41 +/- 0.02, min 0.36 |
| the 13 occurrences of 17 = "of", 12 of 18 = "the", 10 of 38 = "and", 8 of 14 = "this" | used 0, 1, 0, 0 times | |

Reading the first sentence with their own key gives *you the petitions your [1628] have concerning their your treatment
[symbols] have commerce been*, which they print as "The petitions of your seamen concerning their treatment have been
examined": *you*, *the*, the second *your*, one *have* and *commerce* are dropped, *of*, *seamen* and *examined* are
supplied. "I have written to you ... its ports ... that" rests on five key numbers absent from the letter. The 35
symbol passages, including two full lines, are not mentioned. The "verification methodology" on the AFIO page (grammar,
style, thematic parallels with the 1804 and 1806 letters, frequency of "the/this/have") tests the English sentence,
not the key; the frequency claim is false on its face, since the text uses the letter's commonest group once in
thirteen occurrences.

The controls: (A) shuffling the 45 words among the 56 numbers drops the in-order match from 40 to about 19, which
shows only that the key encodes the order of page 1, as any key read off page 1 must. (B) The informative control is
to build a key the same way (walk the plaintext, give each word the next free group) on a *shuffled* copy of the
ciphertext: 500 such keys fit the AFIO sentence with 60 of 60 words in order, account for 70 % of the mapped
occurrences in their span and 41 % over the letter, both better than the AFIO key's 59 % and 30 %. A key that fits
random noise better than it fits the real text carries no information about the code.

### What would settle it

A reading must render every occurrence of every mapped group, say what the symbol passages are, and be checked against
an independent source: a second letter in the same code, or the key itself. The candidates for the "other
correspondent" (Tomokiyo, from Kreider): Pinkney, Monroe, Erving, Livingston, or Armstrong's New York circle. The
Founders page for 20 Feb 1808 also opens with a clear "The", which any solution has to continue.

Not checked: the roll-14 images of the letter itself (naId 188671566, objects 29-32; not fetched), so the Founders
group list stands unverified against the manuscript; the frames 0011-0289 were skimmed for value range and pencil, not
read group by group.
