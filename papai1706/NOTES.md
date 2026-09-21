# János Pápai (Constantinople) to Ferenc Rákóczi II, 1706–1710 — DECODE R731, R740, R741, R757, R765, R784, R805, R823

Status: read in part — seven of the eight letters read with the envoy's own key; R731 (graphic signs) not read.

Catalogue entry 46 (class B, scored by rule). Worked 21 Sept 2026. Archive images are not in the public domain
(DECODE: publishing only with the archive's permission); they are kept git-ignored in `img/`, and only derived text is
committed.

## The documents

| Record | Shelfmark (MNL OL G15) | Date, place | Cipher | Groups | In key |
|---|---|---|---|---|---|
| R805 | Caps. C Fasc. 33, pp. 34–37 | 1 May 1706, Constantinople (signed Pápai János, Horváth Ferenc) | numeric, R580 key | 336 | 336 (100%) |
| R823 | Caps. C Fasc. 33, pp. 140–143 | 19 Dec 1706, Constantinople (Pápai, Horváth) | numeric, R580 key | 1,632 | 1,609 (98.6%) |
| R765 | Caps. E Fasc. 80, pp. 2–11 | 5 Jan 1707 (DECODE origin "Balar") | numeric, R580 key | 4,864 | 4,787 (98.4%) |
| R784 | Caps. D Fasc. 80, pp. 110–111 | undated (DECODE 1707), unsigned; cover note in another hand | numeric, R580 key | 594 | 587 (98.8%) |
| R757 | Caps. E Fasc. 109, pp. 85–90 | 16 May 1708 (DECODE origin "Balar") | numeric, R580 key | 2,758 | 2,695 (97.7%) |
| R740 | Caps. H Fasc. 226, pp. 85–88 | 2 Jan 1710, Constantinople | numeric, R580 key (one passage, p. 2–3) | 168 | 168 (100%) |
| R741 | Caps. H Fasc. 226, pp. 89–96 | 8 May 1710, Constantinople | numeric, R580 key | 1,466 | 1,458 (99.5%) |
| R731 | Caps. H Fasc. 226, pp. 31–33 | 6 Mar 1710, Landor Fejérvár (Belgrade), signed *Pápai János* | graphic-sign substitution, six short passages | not transcribed | — |

Group counts are what `decode.py` parses from the DECODE transcriptions (R740: transcribed here from the images,
`R740_transcription.txt`). "In key" groups are those with a value in the key; the rest are digit slips in the
transcription, clear numerals (R823 opens with 400–1000 figures that are sums, not cipher) or joined groups.
Total: 11,640 of 11,818 groups (98.5%).

## The key: DECODE R580 / R581

DECODE R580 (MNL OL G15 Caps. C Fasc. 43/39) is headed *Nemzetes Vitézlő Pápai Jánosnak adott Clavis, mássa*
("key given to the noble and valiant János Pápai, copy"). R581 (Fasc. 43/40) and R452 (Ráday Archives
C64-4d2-25/11) are further copies of the same table. It is a Hungarian syllabic nomenclator, values 10–322:

- letters, two homophones each: A 219|229, B 209|239 … Z 60|312, plus ö, ü, ny, ly, gy, ty, cz, sz, nk, rt;
- vowel-consonant and consonant-vowel syllables (11 ab, 21 ad … 192 ge … 245 va … 236 üz), laid out in columns
  ending in 1, 2, 3 … 6;
- names: 246 Király, 256 Fejedelem, 257 Fényes Porta, 267 Török Császár, 277 Vezér, 287 Bassa, 297 Bécs;
  countries 17–207; places, rivers and months 18–298.

The key was never linked to these letters on DECODE (R805 is "partially decrypted": a few interlinear syllables).
The first test on R805 read 336 of 336 groups as continuous Hungarian. `decode.py` applies the table (R581's
transcription, which is the cleanest).

## What the letters say (gist; the reading files are `*_read.txt`)

- **R805, 1 May 1706.** The envoys urge that the Porte refuse the Germans (Imperial troops) free passage across
  Ottoman ground: *az németnek szabados általmenetelt ne engedgye … az Török Országon való általmenetelt … az végbeli
  Bassák … az Aradi Bassának ordere nélkül meg ne engedgye az németnek Szegedfelé való általmenetelt*. They have
  spoken to the Vezír about their affairs and also about Muscovy.
- **R823, 19 Dec 1706.** Report of an audience at the Porte in the presence of the Imperial internuncio, partly in
  Latin: *non libenter conversatur vobiscum … Fényes Porta in praesentia internuncii … praesentia autem vestra non est
  ingrata Portae*; the argument over hereditary kingship: *legibus imperatoris hereditarii regis sunt Angliae,
  Daniae, Sveciae, et tamen legibus subsunt*, and the envoys' reply that Hungary cannot give up its old laws.
- **R765, 5 Jan 1707.** Submission to the Prince's will, the Polish situation, and approaches to the French
  ambassador (*a Francia Ország oratorához elmentünk*) on the Prince's orders.
- **R784, 1707 (added 21 Sept 2026, catalogue entry "Unknown sender to Ferenc Rákóczi II").** Unsigned, undated
  report from Constantinople in the envoy's key: *A Francia Ország orátora jelentette … hogy semmi ratiókkal nem …
  a Fényes Portát az hadakozásra*: the French ambassador reported that no arguments could bring the Porte to war;
  the grandees who fought the last war have sworn to see it through (*egyátallyában effectuállyák hogy a Török
  Császárnak hadakozásra kell resolválni magát*); the whole Turkish nation is inclined to it; France means to turn
  Turkey wholly against the Germans (*ezt a Török Országot egészen a német ellen fordítsa*), from which Hungary would
  get harm, not profit; the ambassador has written the same to the Tatar Khan; if Muscovy and Poland do not second
  it, the Germans will overrun Hungary. It ends with the writer's wish to report quickly to *Nagyságod* (the Prince).
  The DECODE transcription splits five groups (`0 79`, `221 33`, `203 273`, `92 1`, `1 00`); read as the image
  shows them, all but one decode. On p. 2 a note in another hand, upside down, asks the Prince to keep it secret and
  decipher it himself: *Mivel ez titok, méltóztassék … titokban tartani s maga decifrálni …*. Grade H.
- **R757, 16 May 1708.** The Muscovite ambassador's message; the envoy cannot send money from Constantinople;
  Hentér.
- **R740, 2 Jan 1710.** The Kiaya's answer, in cipher: *legyen patientia, [ne] siessen, várakozzék … Bécs … a
  Vezérnek megírván … ha a Fényes Porta szívére nem veszi … ne kellyen illy haszontalan költeni s alkalmatlankodni
  Felségednek a Fényes Portán*: be patient, do not spend money and effort at the Porte in vain.
- **R741, 8 May 1710.** At the Defterdar's; the Pasha of Belgrade's letter concerned only the merchants' affairs.

The readings are run-on Hungarian as the cipher gives it (no word division); the word breaks above are editorial.
Grades: the numeric passages are H (direct table reading) except isolated groups shown as `[n]` in the reading files.

## R731: not read

R731 (6 March 1710, Belgrade, signed *Pápai János*) is written in clear except six short passages in a graphic
alphabet of perhaps 25 signs (∂, π, m-like, q, ÷, =, "11", with colons), about 350 signs in all, on p. 1 (three
passages) and pp. 2–3 (three). DECODE has no transcription. A secure sign-by-sign transcription could not be made
from the 2448-px camera images, and without one a monoalphabetic solve on ~350 signs is not reliable. Lead:
the top-left corner of the key copy R581 carries a line of signs of the same family (δ, ♀, ⊔, =, :), which the DECODE
transcriber noted as "symbols which do not occur in the key itself": probably a partial graphic alphabet.

## Prior work

- DECODE lists R805 as partially decrypted (interlinear syllables) and the others as not decrypted. No link to R580.
- Kálmán Benda edited *Pápai János törökországi naplói* (Budapest: Szépirodalmi, 1963, Magyar Századok). Whether
  it prints these ciphered despatches deciphered was not checked (not online). Contemporary decipherments may
  also exist in the Rákóczi chancery papers. Treat the readings here as new only in that they were not on DECODE.

## Files

`fetch.py` (DECODE pages, transcriptions, images via the project cookie), `decode.py` (the table decoder),
`DOC_*.txt` (DECODE transcriptions and keys), `*_read.txt` (decoded output), `R740_transcription.txt`.

## Remaining gaps
- R731 (6 Mar 1710, Belgrade), six graphic-sign passages, ~350 signs - blocker: not-attempted; not transcribed; 2448-px images judged too poor for a secure sign transcription; the graphic-sign line on R581 not tried
- ~178 numeric groups across R823, R765, R784, R757, R741 - blocker: open-codes; digit slips, joined groups or sums in the DECODE transcriptions; not re-checked on the images

## Escalation
- [x] siblings: eight Papai records plus key copies R580, R581, R452 opened
- [ ] clear-pages: not done — check the Rakoczi chancery papers (MNL OL G15) for contemporary decipherments of R731
- [x] known-keys: R580/R581/R452 applied to all seven numeric letters
- [ ] print: not done — Benda (ed.), Papai Janos torokorszagi naploi (1963) not checked
- [ ] key-rebuild: not done — use the sign line on R581's corner as a partial graphic alphabet and solve R731 monoalphabetically
- [ ] retry: not done — re-read the ~178 off-key groups on the images
