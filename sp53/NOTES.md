# SP 53/16 nos. 78 and 79 (1585?) and SP 53/22 f. 52 — attempted 2026-09-16 and 2026-09-15 (second session), not solved

The unsolved residue of the Mary Queen of Scots cipher papers on Tomokiyo's list ("More Undeciphered Letters
Related to Mary, Queen of Scots"). All three ciphertexts are Tomokiyo's transcriptions (`SP53_16_78.txt`,
`SP53_16_79.txt`, and f. 52 inline in `mary.htm`), downloaded 2026-09-16 and live. No images are available:
SP 53 is on State Papers Online (paywalled), the cryptiana image files named in the transcriptions are not served,
and TNA Discovery blocks scripts. So the attack rests on the transcriptions as given.

| item | what it is | tokens | distinct | IC |
|---|---|---|---|---|
| SP 53/16 no. 78 | anonymous letter in cipher to Mr Tempest, English priest at Paris; clear lines in French; endorsed by Phelippes | 507 | 132 (numbers 1-141) | 0.0106 |
| SP 53/16 no. 79 | anonymous letter in the same hand to Dr Barret, president of the English College at Rheims; endorsed by Phelippes | 644 (+27 illegible) | 102 (85 base numbers 1-138, 21 of them with letter variants a-f) | 0.0151 |
| SP 53/22 f. 52 | "Cifer with Spanish spy", short | 84 | 22 (0-13 with b-variants) | 0.050 |

## Why the premise was half wrong

The tracker note said "run the published keys". The 2023 Lasry-Biermann-Tomokiyo keys are for Mary's
symbol cipher with Castelnau (BnF fr. 2988 etc.); nos. 78 and 79 are numeric ciphers of the English Catholic
exile network, and Tomokiyo already tried the neighbouring keys (SP 53/22 f. 27/28/49 "Emilio", the Mary-Fontenay
cipher) on the sibling items without success. Nothing published applies mechanically. So the work became
ciphertext-only cryptanalysis with matched controls, and the numbers below are the result.

## Statistics

No. 78 is flat: the top group 92 is 4.5% of tokens, 34 groups occur once, and the IC (0.0106) sits between a
letters-only homophonic cipher with the same symbol count (matched control: 0.0080, 14 singletons) and a
syllable/word code. Repeats are thin: 128 92 (x4), 69 71, 135 01 (x3), one trigram 05 128 92 (x2). No. 79 is
less flat (IC 0.0151); its top base numbers are 01 (41 with variants a/b/d), 08 (33; b/c), 29 (27), 12, 76,
128 (20). The two letters share the range and many frequent groups (128, 20, 10, 15, 12, 03, 05, 68, 92, 102,
101) but 29 (27x in 79) never occurs in 78 and 92 (23x in 78) is 11x in 79, so a common key is possible but
not demonstrated; they were also attacked as one text (`SP53_16_7879.txt`).

## Attacks and controls

Language models: spaceless character 6-grams trained on period text after stripping Roman numerals and
letter runs (an earlier French model had a degenerate attractor, scoring "iiii..." as fluent French, from the
numerals in footnote apparatus). English 1.44 M letters (Poulet's letter-books 1586, Strickland's *Letters of
Mary*); French 6.9 M (Labanoff vols 5-6 plus the Chaulnes corpus); Latin 2.3 M (Petrarch, Nadal's Jesuit
letters); Spanish 6.0 M and Italian 5.5 M from the repo's existing corpora.

**Hypothesis A — alphabetical blocks** (letters in order, each with a run of consecutive numbers, the design of
the 1584-89 Croissy-office keys and of several SP 53/23 "alphabets"): `blocks2.py`, coordinate descent over the
23 block boundaries with 12 restarts. Controls are period text encoded with a random 141-number block key with
the same token count (`make_control2.py`).

| text | English | French | Latin |
|---|---|---|---|
| control (507 tokens, 128-129 symbols) | **96-98% of letters recovered**, -1.9 nats/letter | 81% recovered (e/i confusion), -3.5 | 89.3% recovered, -2.7 |
| no. 78 | -4.79 | -4.55 | -4.26 |
| no. 79 (base numbers) | -5.22 | -4.79 | -4.73 |
| 78+79 together | -4.99 | -4.65 | -4.31 |

Random text under these models scores about -4.6 to -5.0 per letter. The real texts never leave that level
while the English control is solved outright, so **nos. 78 and 79 are not alphabetical-block letter ciphers in
English, French or Latin** as transcribed.

**Hypothesis B — unstructured homophonic letter cipher** (every number a letter, no order): `homo2.py`,
simulated annealing with incremental scoring, 1.5 M iterations per restart. The matched control (507 tokens,
127 symbols) is **not solved**: English -1317 after a restart against -776 for the true plaintext (10.5% letters
right with the earlier solver; the stronger one no better); French -1159 against -694. The real texts land in
the same band (78: -1256 en, -1202 fr; 79: -1729 fr). With four tokens per symbol this is below what a
ciphertext-only homophonic attack can do, which matches Lasry's experience on d'Avaux 1684. Nothing to report.

**f. 52**: 84 tokens over 22 symbols. Homophonic annealing in Spanish, French, English and Italian gives fluent
nonsense at -2.1 to -2.4 nats/letter; matched 84-token controls in the same four languages are **not solved**
either (-2.0 to -2.3 against -1.26 to -1.32 for the truth). Below unicity; no reading claimed.

## Second session, 2026-09-15: same key, glyph labels, pooled control

**The numbers are labels, not figures.** Tomokiyo's transcription convention for symbol ciphers (his SP 53/16
no. 29(2) file `SP53_16_29c.txt`, whose key image `mary_SP53_16_29_2.png` is a table of glyphs, and his Moray-Wood
file) numbers each distinct glyph and marks variants with a letter suffix. Nos. 78 and 79 are written the same
way (78 as `01`-`141`, 79 with variants `01a`-`01d`, `84f`, `16e`), and the letters are of the Paris-Rheims
network whose surviving keys in SP 53/22 are all symbol tables. So these are almost certainly **symbol ciphers of
the Mary-Castelnau class** (homophonic alphabet plus a nomenclator of glyphs), not numeric ciphers.* The
alphabetical-block test of the first session (Hypothesis A) therefore tested a design the cipher cannot have; its
negative result stands but says nothing. Hypothesis B (unstructured homophonic) is the right frame, and it fails
its own 507-token control. *Inference from the notation; the page images would settle it.

**One key for both letters.** Frequency profiles over the shared label set: Pearson 0.35 (Spearman 0.38) against
0.00 ± 0.09 for 200 random relabellings of no. 79 (max 0.345). Ten of the twenty commonest labels are common to
both letters (`01 03 10 12 15 20 68 92 101 128`), against 2.9 ± 1.5 expected by chance (P < 0.0002). The one
strong exception, `29` (27 times in no. 79, never in no. 78), behaves like a nomenclator element proper to the
Barret letter. Only one repeated bigram is shared (`71 15`), as expected when most letters have several
homophones. So pooling the letters (1151 tokens, 159 labels with variants, 132 base labels) is legitimate, and
the first session's pooled run (`run5_homo_*_7879.txt`: English -3.13, French -2.81 per letter, i.e. random
level) is the real test.

**Does doubling the text help?** Matched controls at the pooled length: 1151 tokens of period English (Poulet)
and French (Labanoff) under a random homophonic key of 132 symbols (130 and 127 used), same annealer, 1.5 M
iterations, two restarts (`control_*_homo1151*.txt`, `run7_ctrl_homo1151_*.txt`).

| control | true plaintext | solver best | letters recovered |
|---|---|---|---|
| English 1151 | -1888.1 (-1.640/letter) | -3427.0 (-2.977/letter) | 31.8 % |
| French 1151 | -1586.4 (-1.378/letter) | -3307.0 (-2.873/letter) | 7.5 % |

Doubling the text does not cross the threshold: the solver lands 1.3-1.5 nats per letter below the true key, in the
same band as its 507-token failures (-2.6 en, -2.3 fr per letter) and as the real pooled text (-3.13 en, -2.81 fr).
The English control keeps a third of its letters only because the frequency-ranked initialisation seeds the
commonest symbols with e, t, a. With four tokens per symbol and no cleartext context this class is not attackable
ciphertext-only by an n-gram annealer, which is what Lasry found for d'Avaux 1684 and what the 2023 Mary letters
needed 50 letters and 150 000 symbols to overcome. Closed from the evidence; the route in is images and keys.

**Calendar entries.** Boyd's *Calendar of Scottish Papers* viii (1585-86), which would give the archivist's
description of nos. 78 and 79, is premium content on British History Online and a restricted (lending) item on
archive.org (HTTP 401 for the OCR text); the page images Tomokiyo names (`sp53-16-f78*.jpg`, `sp53-16-no79*.jpg`)
are 404 on cryptiana. Neither the clear French lines nor the endorsements are available. The 1585 Rheims
president was Dr Richard Barret; "Mr Tempest" is presumably Robert Tempest, the Durham recusant priest in Paris.

## What would move this

1. Images of SP 53/16 nos. 78-79 (State Papers Online, or a TNA copy order): the transcription's leading-zero
   two-digit groups, the 79 letter variants and the 27 illegible slots need checking, and the clear French
   lines (not transcribed) are the crib.
2. A key: the 1585 Paris-Rheims correspondence keys would sit in SP 53/22 (f. 53 is a French-nomenclature
   numeric key naming Paget 83, Arundel 84, Morgan 85, Fontenay 86, range compatible with 1-141) or in
   SP 12/193. Tomokiyo has not reported trying f. 53 on 78/79; that is the first thing to do with images.
3. Identification of the writer (Morgan, Paget, Gifford or Cordaillot's circle, 1585) and of the letters'
   calendar entries (CSP Scotland vol. 8, not online as text) for content cribs.

## Files

`SP53_16_78.txt`, `SP53_16_79.txt`, `SP53_16_7879.txt`, `SP53_22_52.txt` (ciphertexts); `homo.py` (LM, first
homophonic and blocks solvers), `homo2.py` (incremental homophonic annealer), `blocks2.py` (coordinate-descent
blocks solver), `make_control2.py`, `eval2.py`; `control_*.txt`, `control52_*.txt` (controls with keys and
plaintexts); `run5_*.txt`, `run6_*.txt` (outputs). Corpora and models are rebuilt with the commands in
`homo.py` from the archive.org identifiers named above (not tracked).
