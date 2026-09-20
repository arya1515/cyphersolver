# Pallotto to Barberini, 1629 — ciphered despatches of the nuncio at Vienna

Status: read (content recovered from the printed decipherment); key not recovered

BAV, Barb.lat. 6960 — 28 ciphered passages in the register of Monsignor Giovanni Battista Pallotto,
archbishop of Thessalonica, nuncio to the Emperor, 4 August – 29 November 1629.
DECODE records R286–R313 (28 ciphertexts) plus R315 (the whole volume), all "Non-decrypted".

The catalogue entry said "what the cipher hides is not known". It is known, and has been in print since 1897.

## What the target actually is

The manuscript is free on DigiVatLib: <https://digi.vatlib.it/view/MSS_Barb.lat.6960>, 194 pages,
IIIF manifest at `/iiif/MSS_Barb.lat.6960/manifest.json`. The images are small — the IIIF `info.json`
gives a maximum of **748 × 1088 px** per page, an old bitonal microfilm scan. Everything larger that the
server returns is an upscale. This matters: see "Why the key is not recovered" below.

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
112,805 digits in total; R286 alone has 3,570.

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

**What survives.** The opening of R286 does align letter-for-letter with the known opening of Nr. 153:

```
55 70 83 65 03 29 00 69 38 73 11 36 50 23 22 07 92 20 86 72 52 06 38 97 12 33 23
H  O  R  I  C  E  V  U  T  A  L  A  R  I  S  P  O  S  T  A  D  A  T  A  M  I  I
```

27 letters with two independent repeat confirmations (38 = T twice, 23 = I twice; p ≈ 0.006 by chance).
The 28th code conflicts and the alignment never recovers. Iterating a banded DP aligner (2-digit codes plus
1-/3-digit resync ops for transcription slips) over the whole of R286 against a hand-corrected crib of
Nr. 153 tops out at about **55 % code→letter consistency** — far above the 20 % baseline, far below the
~95 % that would mean the key is in hand.

## Why the key is not recovered

Most likely the transcriptions, not the cipher. Checking DECODE's line 1 of p. 5 against my own reading of
the image, the two agree on the first 22 digits and then differ by about six digits, including a
±2-digit difference in length, over a 74-digit line. A single inserted or dropped digit flips the phase for
the rest of the line, which is exactly what would erase the phase signal in the statistics above and break
a letter-level alignment every ~27 letters. Line 2 by contrast matched almost exactly, so the error rate is
uneven rather than uniform.

At 748 px per page the digits are roughly ten pixels wide and individual strokes are genuinely ambiguous.
A key recovery needs a fresh, accurate transcription, and that needs better images than the BAV serves
publicly — a new capture of ff. 2–3, 5–6 and the other cipher leaves would probably be enough, since the
plaintext of every passage is already known from Kiewning and can be used as a crib.

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
