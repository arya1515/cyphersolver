# Pallotto to Barberini, 1629 — ciphered despatches of the nuncio at Vienna

Status: read (content recovered from the printed decipherment); key not recovered

BAV, Barb.lat. 6960 — 28 ciphered passages in the register of Monsignor Giovanni Battista Pallotto,
archbishop of Thessalonica, nuncio to the Emperor, 4 August – 29 November 1629.
DECODE records R286–R313 (28 ciphertexts) plus R315 (the whole volume), all "Non-decrypted".

The catalogue entry said "what the cipher hides is not known". It is known, and has been in print since 1897.

## What the target actually is

The manuscript is free on DigiVatLib: <https://digi.vatlib.it/view/MSS_Barb.lat.6960>, 194 pages,
IIIF manifest at `/iiif/MSS_Barb.lat.6960/manifest.json`. Those images are small — the IIIF `info.json`
gives a maximum of **748 × 1088 px** per page, an old bitonal microfilm scan, and anything larger the server
returns is an upscale. **DECODE has better scans of the same leaves**: `IMG_R286_I2489_P1.png` and
`IMG_R286_I2490_P2.png` are **1491 × 2066**, four times the pixel area, behind the login (cookie recipe in the
`decode-access` memory). Use DECODE's images, not DigiVatLib's, for any transcription work here.

DECODE's `additional_information` gives each record's page range in that same DigiVatLib pagination,
so DECODE page *n* = canvas *n*. Ranges are in `decode_records.txt`.

The volume interleaves **ciphered sheets** (full-width, dense numerals, e.g. pp. 5–6) with **clear text**
(written in a narrow right-hand column with a wide left margin, e.g. pp. 3–4, 7–9, 13). The clear pages are
not decipherments written against the cipher; they are the register's fair copies and the enclosures.

## The content is already published

Hans Kiewning (ed.), *Nuntiaturberichte aus Deutschland nebst ergänzenden Aktenstücken. Vierte Abteilung:
17. Jahrhundert, Band 2: Nuntiatur des Pallotto 1628–1630, 2: 1629* (Berlin 1897).
Full text on archive.org, item `4-2_20200807` (`4,2_djvu.txt`), saved here as `ed/pallotto_bd2_1629.txt`.

Kiewning prints Pallotto's despatches from the Rome-received copies in **ASV, Nunz. di Germania 119**, and
heads each ciphered one "**dechiffr.**" with the date the Roman office deciphered it — i.e. he prints the
*contemporary decipherment*. The Italian is given verbatim for the substantive passages, with German
regesta for the rest. Some forty Pallotto "dechiffr." despatches of 1629 are printed.

Two independent confirmations that Barb.lat. 6960 carries the same texts:

* **R286 = pp. 5–6 = 4 August 1629 = Kiewning Nr. 153** (*Arch. Vatic. Nunz. di Germ. 119 fol. 11–19*).
  The cipher sheet is headed, in clear, `Di Vienna 4 di Agosto / Ill.mo et R.mo Sig.r Card.le P.rone`
  followed by a struck-out opening line. The clear pages around it run continuously *through* the cipher
  sheet — p. 4 ends `...non haver facoltà di accettar altro partito, che'l proposto in` and p. 7 resumes
  `nome del suo Rè` — and that sentence is Kiewning Nr. 153 word for word.
* **p. 13** is the enclosure Kiewning prints as Nr. 153 *Beilage II, Propositione P. Valeriano per Sabran*
  (`Bibl. Barber. LXIX 60 fol. 122`), again verbatim: `...il quale aggiunse di più, che fatta la pace,
  quando S. Sta ... proponga una lega et unione di questi eserciti, affine di abbatter il Turco commune
  nemico del nome christiano, che S. Mtà mandaria plenipotentiarii in Italia, acciò N. Sre potesse
  concludere così gran negotio, con che il demonio resteria ingannato e burlato.`

So the despatches are about the Mantuan succession crisis in the summer and autumn of 1629: Pallotto's
attempts, through P. Valeriano Magno and the imperial minister Eggenberg (Echembergh), to mediate between
the Emperor and the French envoy Sabran over Casale, Susa and the Grisons passes.

## The cipher

Numeric, written as an unbroken stream of digits with decorative spacing. Transcriptions of all 28
ciphertexts were made for DECODE in 2019–20 by volunteers and are downloadable as `DOC_R*.txt`
(saved in `decode/`, fetched with the cookie recipe in the `decode-access` memory).
112,805 digits in total; R286 alone has 3,573 (measured with `docs/_check_profile.py --measure`).

Digit frequencies are strongly uneven (0 = 16.1 %, 4 = 4.8 %), and adjacent digits carry ~0.18 bits of
mutual information — so the stream is structured, not random.

**What was ruled out.**

* *Fixed two-digit codes.* No phase preference at all: index of coincidence 0.01462 at phase 0 versus
  0.01466 at phase 1; the even-position and odd-position digit distributions agree to within 0.2 %.
  Same for three-digit codes at all three phases. Under a genuine fixed-length code the correct phase
  should stand out.
* *Crib-free homophonic solve.* Fixed-multiset simulated annealing over the 100 two-digit codes,
  5,000 codes of text, scored by a space-free Italian 5-gram model built here from
  `lang/corpora/it-renaissance.txt` + `it-gutenberg.txt` (12.0 M characters, `it_clean5.npy`),
  reaches −3.54 log-prob per character against −1.5 for real Italian. Not a solution.
  (Note for reuse: the shared `lang/` corpus `it-nunziature.txt` is OCR garbage — it scores a string of
  twenty-four `i` better than real Italian. Do not build models from it.)
* *Syllabic two-digit nomenclator.* Aligning two-digit codes to plaintext spans of 1–4 letters against the
  known plaintext collapses back to single letters for every well-attested code, so there is no evidence
  for a syllable table.

**What looked like evidence, and is not.** The opening of R286 does align letter-for-letter with the known
opening of Nr. 153:

```
55 70 83 65 03 29 00 69 38 73 11 36 50 23 22 07 92 20 86 72 52 06 38 97 12 33 23
H  O  R  I  C  E  V  U  T  A  L  A  R  I  S  P  O  S  T  A  D  A  T  A  M  I  I
```

27 letters with two independent repeat confirmations (38 = T twice, 23 = I twice). I first read that as roughly
a 1-in-180 coincidence. **It is not: 27 is below chance.** See the run-length test below — random controls on this
material reach consistent runs of 36 to 39 letters. The opening match is unremarkable and should never have been
presented as support. Re-read on DECODE's better scan the line is essentially the same (two substitutions, no
length change), so the break at letter 28 is not a transcription artefact either. Iterating a banded DP aligner
over the whole of R286 reaches about 55 % code→letter consistency, which the held-out test below shows is worthless.

## Why the key is not recovered — measured, with controls

Two experiments were run after the first pass, and they change the earlier conclusion.

**1. Held-out test. The "key" recovered from R286 carries no information.**
Learn a table on the first 55 % of R286 against the crib, freeze it, then align the remaining digits to the
remaining crib and count confirmations (a confirmation = the code was already in the table and agrees).
Against eight controls that keep the same table but shuffle the letters among the codes:

| | confirmations per letter | DP score |
|---|---|---|
| learned key | 0.355 | −3266 |
| shuffled controls (mean of 8) | 0.359 | −3313 |

No separation. The same test for a "2-digit codes + nulls, no digit slips" model gives 0.440 against a control
mean of 0.431 — again nothing. **The ~55 % consistency reported in the first pass was the aligner fitting the
crib, not a key.** Any claim of a partial key here would have been wrong.

**2. Positive control. The pipeline works; this material defeats it.**
Encipher the same crib with a random two-digit homophonic key, damage the digit stream with single-digit
insertions and deletions at a given rate, and run the identical learner. Fraction of the true key recovered:

| digit error rate | key recovered |
|---|---|
| 0 % | 100 / 100 |
| 0.5 % | 87 / 100 |
| 1.7 % | 7 / 100 |
| 4 % | 19 / 100 |

So the method is sound, and it needs a transcription accurate to better than about **0.5 % of digits**. Above
roughly 1 %, a two-digit key cannot be recovered from this much text even when the plaintext is known, because
each inserted or dropped digit flips the code phase for everything after it.

**Correction to the first pass.** It said the images top out at 748 × 1088 px and that DECODE's transcription of
p. 5 line 1 differs from a fresh reading by about six digits in seventy-four including a length difference. Both
statements were wrong, and the error was mine:

* 748 × 1088 is DigiVatLib's maximum, but **DECODE serves its own scans of the same leaves at 1491 × 2066** —
  four times the pixel area (`IMG_R286_I2489_P1.png`, `IMG_R286_I2490_P2.png`, behind the login).
* Re-read on that better scan, line 1 differs from DECODE's transcription in **two digits out of seventy-four,
  both substitutions, with no length difference** (they read 93 where the scan shows 73, and 30 where it shows
  38). My earlier six-digit discrepancy was my own misreading of the low-resolution image. On line 2 the two
  readings differ by a digit or two and possibly in length, so the transcription still cannot be assumed exact —
  but DECODE's is better than the first pass credited, and no length error is demonstrated.

**3. Run-length test: there is no alignment signal at all.**
A crib aligner can fake a fit, but a long *consistent* run cannot be faked easily: inside one window a repeated
code must carry the same letter and the map must stay a function, so a false run dies at its first repeat
conflict. Scan every (digit offset, crib offset) pair in a band, extend each run while it stays consistent under
two-digit codes, and take the longest:

| | longest consistent run |
|---|---|
| real R286 against the plaintext of Nr. 153 | **39 letters** |
| control: crib letters shuffled (5 runs) | 39, 39, 36, 38, 36 |
| control: cipher reversed | 39 |
| synthetic two-digit cipher, same text, 1.7 % digit noise | **207 letters** |
| synthetic two-digit cipher, clean transcription | 2705 letters |

The real material sits exactly on its own chance baseline. The synthetic cipher at the *same* noise level as the
real transcription is five times longer. This method also recovers 81 of 100 key codes from the noisy synthetic
text, where the earlier DP learner managed 7 — so it is not that the tool is too weak.

**Where that leaves it.** Transcription noise is no longer a sufficient explanation. On this evidence
**R286 is not a two-digit homophonic encipherment of the text Kiewning prints as Nr. 153.** What remains open:
the code width may not be two (though no phase structure shows at width three either); the cipher sheet
pp. 5–6 may encode a different despatch, or a version of it whose wording differs materially from the
Rome-received copy Kiewning used; or the system may be nomenclator-heavy or variable-length, in which case no
fixed-width alignment can ever match. The contents of the despatches are unaffected by any of this — they rest
on Kiewning and on the register's own clear pages, not on any decipherment made here.

**The concrete next step**, and the reason this is worth returning to: DECODE's 1491 × 2066 scans are good enough
for a careful transcription, and the plaintext of every passage is already known from Kiewning. A transcription
of one sheet at better than 0.5 % digit error would settle it either way. Doing that by eye is slow and my own
attempt was not clearly better than DECODE's; the repository's existing approach for this — glyph segmentation
and clustering, as used for the Sormano and Gramont leaves — is the tool to build.

## Files

* `decode/R286.txt` … `R313.txt` — DECODE's 2019–20 digit transcriptions (28 ciphertexts).
* `decode_records.txt` — DECODE record → DigiVatLib page range, date, length.
* `ed/pallotto_bd2_1629.txt` — Kiewning 1897, Band 2 (1629), full OCR text from archive.org.
* `crib153.txt` — hand-corrected Italian text of Nr. 153 (4 Aug 1629), 3,359 letters, used as the crib.
* `solve.py`, `align2.py`, `align3.py`, `align4.py`, `soft.py`, `walk.py`, `syll.py` — the aligners tried.
* `hill2.py`, `it_clean5.npy/.json` — the space-free Italian 5-gram model and the annealing solver.
* `manifest.json` — the DigiVatLib IIIF manifest. Images are git-ignored (`img/`).

## Next

The sibling volume, **BAV Barb.lat. 6956** (catalogue entry 236, DECODE R215-R318, seventy ciphered
sheets of the same nunciature for 1628), is still open. Kiewning's **Band 1, Nuntiatur des Pallotto 1628**
(Berlin 1895) covers exactly those months and is the first place to look. Not checked here.
