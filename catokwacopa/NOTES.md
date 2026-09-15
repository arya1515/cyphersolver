# The Catokwacopa advertisements (1875) — which readings the letters force, and which are guesses

Two personal advertisements signed *W.*, *The Standard*, p. 1 col. 2, 8 and 20 May 1875. The second
ends in clear: *"This will be intelligible if read in connection with my communication published in
this column on the 8th inst."* Number 8 on Schmeh's Top 50, republished on klausschmeh.net on
14 August 2026 with an active thread.

## State of play (September 2026)

The mechanism is agreed. Line *i* of the first ad and line *i* of the second are two order-preserving
halves of one plaintext phrase, from which W. also dropped letters. Nothing is substituted. Readings
have accumulated since 2018: Thomas Bosbach's DYING DECLARATION; Lance Estes and "Dave"'s Oxford
vocabulary (SUMMER TERM, 1853, CONINGTON, JOWETT, BALLIOL, SHIRLEY, I ADDED FIRST LINE SATIRS);
Thomas Ernst's diplomatic line numbering and BNA-checked text; Jozef Krajčovič's QUI FIT (Horace,
*Satires* 1.1) and his 2026 exact-cost audits. They disagree, above all over how much emendation is
allowed. Ernst has proposed SIGNED DECLARATION RELIGIONEM CONFIRMARE and MASTER PUPIL; Krajčovič
costs the former at 14 edits.

**The unanswered question is how much the omission rule lets you read into a line.** With three to
twelve letters freely inserted, plausible English can be made to fit almost anything. Readings are
worth something only where the letters force them. This attempt measures that.

Text: Ernst's BNA-verified transcription (`ads.py`), which corrects a dozen errors in the circulating
one (Hrsclam, 138 not 139, Etfdorshpxn, Tsvlysdinlge, Wtubtrfftrstendinhofsvmnr, …).

## 1. The line pairing is structural, not a reader's choice

Both ads have the same token skeleton, with numerals and dashes in the same slots (`Rep.–`/`Etd. –`,
`Ap. 138.–`/`A.P. 138.–`, `mistrl.–Ding`/`Oatvpu.–Y`). The letter totals are 222 and 219. Over the 24
letter lines, the summed length difference between paired halves is 33; **no random re-pairing in
100,000 comes that close** (`python mech.py`). So W. split each phrase roughly in half, and the pairing
is real.

## 2. The two halves are different in kind

For each word of the readings that fit exactly, I checked which ad supplies its first letter:

* **Consonant-initial words begin in the 8 May half, essentially always**: summer, term, cap, took,
  college, party, broke, left, repeated, conington, hertford, scholarship, motto, previously, second,
  first, line, satirs, qui, fit, told, shirley, dying, declaration. The one exception is *corner* in
  line 4.
* **Vowel-initial words mostly begin in the 20 May half**: away, at, attended (twice), us, is, in,
  instead.

The 8 May half carries onsets, and its line-initial letters are almost all consonants
(`scocsrimhcmciqcbhitimdde`). The 20 May half is vowel-heavy and rich in t, n, d, r, the letters of
inflections and endings. That gives a positional prior which discriminates between rival readings.
For example, I ADDED FIRST LINE **SATIRS** keeps the rule (**SAT**irs), while I ADDED FIRST LINE
**IS ARTS** breaks it (*i*s from the second half).

## 3. Exact costs of every published reading

`cost` = letters W. omitted / cipher letters that must be misprints (`python mech.py`):

| line | reading | omitted | misprints |
|---|---|---|---|
| 27 | DYING | 0 | **0** |
| 28 | DECLARATION | 0 | **0** |
| 16 | I ADDED FIRST LINE SATIRS | 1 | **0** |
| 17 | QUI FIT | 1 | **0** |
| 24 | TOLD SHIRLEY | 1 | **0** |
| 3 | CAP TOOK AWAY AT COLLEGE PARTY | 2 | **0** |
| 4 | OLD CAP BROKE AT CORNER LEFT INSTEAD | 2 | **0** |
| 7 | REPEATED | 2 | **0** |
| 1 | SUMMER TERM | 3 | **0** |
| 8 | I ATTENDED CONINGTON LECSURES | 4 | **0** |
| 25 | I ATTENDED JOWETT LECSURS | 4 | **0** |
| 15 | CONINGTON TOLD US TO ADD A SECOND MOTTO | 7 | **0** |
| 10 | HERTFORD SCHOLARSHIP EXAMINATION | 12 | **0** |
| 14 | MOTTO WAS PREVIOUSLY DISCLOSED IN COLLEGE | 14 | **0** |
| 5 | CONINGTON MET ME IN GARDEN | 5 | 1 |
| 27 | DOING | 0 | 1 |
| 17 | QUIT | 0 | 1 |
| 18 | COUNTED CAP / CONINGTON DEPARTED | 1 / 7 | 3 / 2 |
| 21 | HAD EXAMINATION | 6 | 3 |
| 9, 26 | MASTER PUPIL | 2 | 4 |
| 27 | SIGNED | 1 | 3 |
| 29 | RELIGIONEM CONFIRMARE | 4 | 7 |

This confirms Krajčovič's audit: DYING is exact and SIGNED is not, so DYING DECLARATION stands and
SIGNED DECLARATION is an emendation. MASTER PUPIL needs four misprints in a six-letter half, so it is
not a reading of these letters.

## 4. Which lines the letters decide: an open-vocabulary search

`search.py` enumerates **every** word sequence that fits a line exactly, with no misprints. The
vocabulary is about 30,000 words from 24 nineteenth-century novels, ranked by word frequency, omission
count and the positional prior from §2. It is not given the published readings. It is run twice: once
with a list of the Oxford names the readings use, once without (`search_all.txt`,
`search_all_nonames.txt`).

**Forced by the letters and ordinary vocabulary**, where the search's top reading is the published one
or close to it without any name list:

* 27 DYING · 28 DECLARATION · 7 REPEATED
* 4 OLD CAP BROKE AT CORNER LEFT INSTEAD (top of 30,000-word search)
* 3 CAP TOOK AWAY … PARTY (the middle word contested: *at college* against *catalogue*)
* 16 I ADDED FIRST LINE(S) …
* 1 SUM TERM (SUMMER TERM also fits; the search prefers the abbreviation)

**Exact alternatives the published readings missed:**

* **18 `cagap / ndted` → CHANGE ADOPTED / ADAPTED**, exact. The published COUNTED CAP and CONINGTON
  DEPARTED need 3 and 2 misprints.
* **21 `hodsam / yxn` → HOLIDAYS EXAMINE(D)**, exact. HAD EXAMINATION needs 3.
* **14 `mopredisco / tsvlysdinlge` → MONTHS PREVIOUSLY (or PRIVATELY) DISCLOSED …**, sharing its core
  with Krajčovič's MOTTO WAS PREVIOUSLY DISCLOSED IN COLLEGE but with far fewer omissions.

**Not decided by the letters at all:** 9 and 26 (`mistrl / otenpu`, `mistrl / oatvpu`), 12, 23, 29.
Many unrelated readings fit within a nat or two of each other (*omit stern pull*, *moist relative
put*, *retire followed both mare*). Any reading of these lines is a conjecture, including the author's
own here.

## 5. The name cribs are specific — this is the strongest evidence for the Oxford reading

CONINGTON, JOWETT, SHIRLEY and HERTFORD were introduced as guesses, and without them the search cannot
find those lines. So each frame gets the reverse test (`python names.py`): substitute every one of
**1,645** names and proper nouns from the corpus, and count those that fit exactly with no more
omissions than the published name:

| line | frame | names that fit |
|---|---|---|
| 8 | I ATTENDED ___ LECSURS | **CONINGTON only** |
| 25 | I ATTENDED ___ LECSURS | **JOWETT only** |
| 24 | TOLD ___ | **SHIRLEY only** |
| 15 | ___ TOLD US TO ADD A SECOND MOTTO | **CONINGTON only** |
| 10 | ___ SCHOLARSHIP EXAMINATION | **HERTFORD only** |

A frame that lets a thousand names through would prove nothing. These let exactly one through, and
the parallel lines 8 and 25 each admit a different Oxford classics lecturer of the 1850s. So the frame
readings carry real evidential weight. **The Oxford reading is right in outline**: an 1850s Oxford
undergraduate recalling Conington's and Jowett's lectures, the Hertford scholarship, and a motto
disclosed or used before, closing with a DYING DECLARATION. The frames themselves are partly the
readers' choice, though, and lines 9/26, 12, 23 and 29 remain unread.

## What would finish it

* **Line 29** (`ereflodbr / rileohmae`) completes DYING DECLARATION. It is short enough for an
  exhaustive search over a Latin vocabulary (Ernst's RELIGIONEM CONFIRMARE is 11 edits away) and over
  English phrases, with the positional prior.
* **Line 23** (48 letters) needs a phrase-level language model, not unigrams.
* **Identity**: Ernst's candidate (a W-initial Balliol commoner of 1856) against Krajčovič's
  Jex-Blake, who won the Hertford in 1853. The £138 in line 20 and the DYING DECLARATION of line 27
  are the checkable facts.

Reproduce: `python mech.py` (pairing test, exact costs), `python -c "import mech; mech.rule_report()"`
(positional rule), `python search.py all [--no-names]`, `python search.py 23`, `python names.py`.
