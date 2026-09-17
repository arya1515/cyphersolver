# Thomas Urquhart's encrypted poems — the octastich rule verified independently, the distich claim not reproduced

Two numeric cryptograms of Sir Thomas Urquhart (1611–1660). The **distich**: 64 numbers in two lines of 32, values to 70,
printed under the heading "THE CYPHRAL DISTICH" at the end of *Logopandecteision* (1653) as reprinted in the Maitland
Club *Works* (1834), p. 417 (`src/Urquhart-Cryptogram.png`, the 1834 page; `src/maitland1834.txt` has the OCR). The
**octastich**: eight lines plus a ten-number "Decagram", printed at the end of *Ekskybalauron* / *The Jewel* (1652) on
a final leaf that the EEBO/TCP copy lacks; the public transcription is Schmeh's (Cipherbrain 2015, 2017, 2019), 272 + 10
numbers, values to 201, from a scan supplied by Kent Ramliden; the HCPortal record (cryptograms.hcportal.eu, cipher 8)
carries a scan with the verse beneath it. Number 28 on Schmeh's Top 50.

**Status (16 Sept 2026).** The octastich is a book cipher on *The Jewel* itself: the k-th number, counting straight
through the poem, is a word index into page k of the 1652 edition, the letter being the word's initial; and Urquhart
took the *first* word on the page beginning with the letter he needed. That rule was published by Vals AI on 31 Aug
2026 as a Claude Fable 5.1 result. It is verified here independently, from the EEBO-TCP text of *The Jewel* and Schmeh's
public transcription, without using the claimed plaintext: 231 of 267 aligned numbers are first-occurrence hits
against a shuffled-sequence control of 69 % (max 74 % in 30 trials) and a random-page control of 43 %, and lines 1, 3,
4, 5 and 8 read as English (*Great Lord, mantaine that regal familie … Our Emperour, King, Monarch and Protector*).
Lines 2, 6, 7 and the Decagram do not read from Schmeh's transcription because it is short by about thirteen numbers in
those lines; the reading of those lines rests on Vals' transcription (285 numbers), which is not published. The
**distich** claim (i-th number → i-th Proquiritation, first letter) does *not* reproduce: 34 of 64 first-occurrence hits,
chance level for texts of 30–100 words, and no English; page-index variants on either book are at chance too. The
distich stays unread.

## 1. What the poem says about its own key

The verse printed under the octastich (quoted in full by "Davidsch", Cipherbrain, 1 Aug 2019, from the HCPortal scan):

> To this Octastick if you will subjoyn / A Decagram of this same stuff of mine, / All gather'd out of my Exskybalorum, /
> You'll find a Rule by which, with great decorum, / You may most comfortably regulate / Your actions, thoughts and
> speeches; and know that / I love an aphaeresified treason / Better then any prosthesized reason.

"Gather'd out of my Exskybalorum" names the key text. *Aphaeresis* is the loss of a word's initial; *prosthesis* the
addition of one. The two coined words say what the cipher does: it takes initials.

## 2. The rule, and the property that makes it checkable without the plaintext

Vals' rule: *The Jewel* has 284 numbered pages; the octastich and Decagram have 285 numbers; number k indexes a word on
page k; take its initial. They also noticed that "Urquhart almost always picked the first word on the page starting
with the letter he needed" (231 of 275 positions in their run).

That habit is the lever used here. Whether number n on page k points at the first word of its own initial on that
page is a property of the number and the page alone. If the cipher were anything else, the rate of such coincidences
would sit at the base rate for that page's word list (about 43 % for a random page and index in this book, because
small indices are frequent and early words are first occurrences by construction). If it is this cipher, the rate
should approach 1, short of transcription noise. That gives a test that never looks at the claimed plaintext.

## 3. The text, and the printer's misnumbering

`pages.py` reads the EEBO-TCP XML (`src/tcp_A95749.xml`, from the textcreationpartnership GitHub mirror) into word
lists per page, dropping marginal notes, running heads and catchwords, joining end-of-line hyphens, and tokenising on
letters. Two numberings are provided, because the 1652 printer misnumbered: the pages numbered 34–35, 38–39, 42–43
and 46–47 each occur twice, 60 and 110 do not occur (the TCP `<pb n=…>` follow the print). `numbering='physical'`
counts leaves in order from p. 1, which is what a man turning pages does, and it is the numbering that aligns.

## 4. Alignment of Schmeh's transcription (`align.py`, output `alignment_schmeh.tsv`, `reading_octastich.txt`)

Schmeh's 272 numbers cannot be laid one-per-page onto 284 pages without gaps, and where the transcription drops a
number every later letter would land on the wrong page. So the alignment is a dynamic programme over (token, page)
with three moves: match token j to page p (scored +1 for a first-occurrence hit, −0.6 for a word that is not the first
of its initial, −0.3 when the index exceeds the TCP page's word count), skip a page (a number the transcription lost,
cost 1), drop a token (a number it invented, cost 1.5). The path found has 267 matches, 17 skipped pages and 5 dropped
tokens; 231 of the 267 matches are first-occurrence hits.

Reading, capital = first-occurrence hit, lower case = word not first of its initial (one to three words off, which is
what TCP tokenisation differences produce), `?` = page with no number in the transcription, `_` = index beyond the TCP
page, `(n)` = dropped:

```
1 wREATLORDMApTAInETHATREGtaFAMILIE      Great Lord, mantaine that regal familie
2 WtEREOFKINGCHARLStHaS?KK???U????Rwb    Whereof King Charls the S[econd is the head]   (transcription short by ~7)
3 ATDGRAnTTHatHEDAYBEARETHEFUPaEMESgEIGS And grant that he may beare the supreme sweigh
4 WHERDENGLIsHSCoTSANDIOSoAREBORNEANDBRED Where English, Scots and Ir[i]sh are borne and bred
5 AaDCOnERTHTO__?IttSUaPDApTHORIEIE      And [conerthto …] this usurp'd authoritie
6 REIG??_EINMISnOtALPREDEC???IWP?P?WM    Reigne in his royal predec[essors stead]       (transcription short by ~6)
7 SETHpLBEOURSOLtCES?HUWwA(17)RHECBOR    Let him be our sole Cesar, Artur, Hector       (partly; transcription defective)
8 OeREMPoRPUwJINGMONARCHANDPROTECTOR     Our Emperour, King, Monarch and Protector
9 AM(95)fAF(33)(51)(50)S                 [Amen, so be it]                               (Decagram; not reproducible here)
```

Line 1, position by position (`k n word letter first-occurrence`): 28 of 33 numbers are exactly the first word of
that initial on physical page k; the five others are one word off (25 vs 26, 18 vs 17, 23 vs 22, 75 vs 74) or a TCP
variant (58 vs 31), i.e. differences between the TCP tokenisation and the 1652 page, not between rule and text. The
right-hand column above is the reading; it agrees with Vals' plaintext wherever Schmeh's transcription is intact,
including the unreadable stretch in line 5 (Vals: C-O-N-E-R-T-H-T-O at pages 149–157; here CONERTHTO at the same place),
which is therefore a defect of the cipher or of the 1652 print and not of either decoder.

**Controls.** (a) The number sequence shuffled and re-aligned by the same programme, 30 trials: hit rate mean 0.686,
max 0.738, against 0.865 real; the programme is free to seek the best alignment for the shuffle too, so this is the
fair comparison. (b) Numbers kept in order, pages randomly permuted: 0.433 mean, 0.474 max. (c) Printed page numbers
instead of physical: lower hit rate through the misnumbered stretch (not tabulated; the DP prefers physical).

## 5. The distich

Reticuli Labs' rebuttal of 1 Sept 2026 (`src/reticuli_*`) says the Proquiritation rule fails at ten of the 64
positions because the required letter begins no word in the target section, and that the distich is not in the 1653
edition at all but in the 1834 reprint. The second point is confirmed here on the 1834 OCR (heading, numbers, and the
six-line verse *Of carping Zoil and despightful Momus …* follow the 32nd Proquiritation on p. 417; the 1834 reading of
line 2 has `5.38.5` where Schmeh has `5.33.5`). The first-occurrence test, applied to Reticuli's tokenised
Proquiritations, gives 34 of 64 hits and the string `NTMAMNDN_OHTISEABRPTTSGSNTAATVTD / ASOTHDOSTTTBHPBTHBIPFSWTLVWTABV_`,
which is not English and not the claimed prayer. Page-index variants (k → page k or k + 1…3 of *The Jewel* or of
*Logopandecteision*, printed or physical numbering, lines restarting at page 1) all sit within the shuffled control
(mean 0.50, max 0.62 of 64). The distich is a different cipher, or the same cipher on a text not tried (the six-line
verse itself, the Latin *Parva peto* couplet that commenters have tried, the 1653 sheets in their original order), and
it stays open.

## 6. What is needed

* **The 285-number ciphertext of the octastich.** Schmeh's transcription is short in lines 2, 6, 7 and the Decagram.
  The HCPortal record has the scan but refuses non-browser clients; the Wayback Machine was offline during this
  session; Vals' `verify_octastick.py` and transcription are unpublished; the 1983 Jack & Lyall edition prints the leaf.
  With it, `align.py` becomes a straight one-per-page decode and the remaining lines can be read and controlled the
  same way. Anyone with the HCPortal page open in a browser can copy the numbers.
* The 1652 leaf itself, to settle the ±1 positions and the nine letters of line 5.

## 7. Files

`ct.py` (both ciphertexts as published), `pages.py` (TCP page parser, two numberings), `align.py` (DP alignment and
reading), `alignment_schmeh.tsv` (per-token table), `reading_octastich.txt`, `src/` (TCP XML of A95749 and A64608,
1834 *Works* OCR, Schmeh's post HTML and images, Vals' page, Reticuli's files, the 1653 and Wilcock 1899 OCR from the
first session).

## Earlier sessions

*15 Sept 2026*: provenance objection checked on the EEB 1653 scan and Wilcock 1899 (no numeric runs in either);
octastich measured (272 numbers, 82 distinct, IC 0.021, skewed to small values, 31 of the distich's 32 values shared),
called a book cipher by shape and left as not attackable without the key text. The key text was the book it is printed in.
