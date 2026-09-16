# Regent Moray to John Wood, Edinburgh, 13 July 1568 (BL Add MS 32091 f. 213) — attempted 2026-09-15, not solved

Cryptiana "Moray-Wood Cipher — A Scotch Diplomatic Cipher (1568)" (unsolved list; Tomokiyo's article `elizabeth.htm`,
section "Moray-Wood Cipher (1568)"): "Although the cipher seems simple, the short ciphertext is not deciphered."
Transcription `elizabeth_moray.txt` (fetched 2026-09-15, saved here). The image `stewart.jpg` named in its header
returns 404 on cryptiana; the BL viewer is still offline after the 2023 cyber-attack; DECODE has no record for the
letter (public RecordsList searched for "Moray"). So the ciphertext is Tomokiyo's transcription and cannot be
checked against the page.

## The letter

*Catalogue of Additions to the Manuscripts in the British Museum 1882-1887* (archive.org
`CatalogueOfAdditionsToTheMSS188287`), Add MS 32091 (Malet collection, "State papers and documents 1087-1575"),
item 56: "James [Stewart, Earl of Moray], Regent [of Scotland], to John Wod, his ambassador in England,
**refusing to recall him and sending Border news**; Edinburgh, 13 July, 1568. Partly in cipher. Signed. f. 213."
Neighbours: Privy Council to the Archbishop of York 15 July 1567 (f. 211), Cecil to Parker 15 July 1568 (f. 215),
Morton's declaration on the casket 29 Dec 1568 (f. 216), Leicester to Moray 17 May 1569 (f. 218). The only
other cipher item in the volume is Throckmorton to Dudley 22 May 1560 (f. 180, "deciphered"; Tomokiyo has it).

Context from Bain, *Calendar of Scottish Papers* ii (1900; archive.org `CalendarStatePapersMaryQueenOfScotsVol2`):
Wood had gone to London in June with the Scots translations of the casket letters; Mary intercepted his letters
and sent them to Elizabeth (no. 715, 22 June), which is presumably why he asked to be recalled. Moray wrote to
Elizabeth the same day, 13 July (no. 730, from Edinburgh, in Hay's hand: thanks for hearing the cause, offers to
come in person or send noblemen, "the les tyme be drevin it salbe the mair proffitable for the haill Ile"), and
to Cecil on 31 July (no. 751) and 12 August (nos. 760-761), each time "credit Mr Wood". Bain did not calendar
Add MS 32091; his British Museum items are all Add MS 33531 and Cotton Caligula, so **the Wood letter is not in
print**, and no clear text of it is available online. Border news of that fortnight (nos. 712-729): Moray's
raid on Herries' West March from Hoddom, Lochinvar, Huntly out in the north, Argyll's convention, Dumbarton
still held for the Queen.

Related Scottish ciphers, all checked and none matching this symbol set:
- HMC *Sixth Report* (1877) pp. 634 ff., Moray papers at Donibristle: "seven in cipher, of which two are
  entitled 'The Quein's Cipher'", two facsimiled (Tomokiyo's `mary_Moray1.png`, `mary_Moray2.png`). These are
  Mary's ciphers with the Commendator of Inchcolm (her letter of 23 July 1568 asks him for one: "y dar nocht
  vreit les y heuu a sipher, therfor send mi en"). The Queins Cipher has a 26-letter alphabet of symbols and
  digits, eight "Nulles", and a word list (and, that, the, so, als, nor, nocht, yless, allow, thair, of, plus
  names: the Quene of Scotland, the Prince, the Quene of Ingland, the Duke, Ergill, Huntly, Murray, Mortoun,
  Lethingtoun, Grange...). It shows what a Scottish court cipher of 1568 looked like: alphabet + nulls + a
  short nomenclator.
- Throckmorton to the Regent, 20 July 1569, Add MS 33531 f. 79 (Bain no. 1103, "in cipher deciphered"):
  Tomokiyo's reconstruction is letter-like glyphs (q, r, B, α, ∂, ʃ, 7, k, Δ...), not this set.
- Mary-Hamilton 1569 and Chisholm-Grange 1571 (same volume): different symbol sets.

## The ciphertext

134 groups, 32 distinct, 9 hapax, IC 0.0496 (Scots letters ≈ 0.066; homophones bring it down).
Tomokiyo's labels (his SP53 files use the same convention: numbers for glyphs, a letter suffix for a variant):

| family | symbols (count) | total |
|---|---|---|
| x | x 14, x2 9, x3 1 | 24 |
| z | z1 8, z4 4, z 3, z3 3, z2 2, z5 1 | 21 |
| numbers | 10 14, 17 10, 19 9, 13 5, 14 3, 12 2, 16 2, 18 2, 11 1, 15 1 | 49 |
| letters | a 9, o 8 + o2 1, r 5, e 4, s 3, f 2, p 2, c 1, g 1 | 36 |
| others | 4 2, 4b 1, Eb 1 | 4 |

Repeats: `10 x2 13 r` twice; trigrams `x2 s 10`, `o x 10`, `r 17 10`, `17 10 o` twice each; bigrams `o x`,
`r 17`, `10 z1` four times; `r` is followed by `17` in four of its five occurrences (t-h? q-u?). Doubles: `x x`,
`z z`, `a a`. The obvious reading `r 17 10` = *the* (t, h, e) was tried as a fixed crib and is not preferred by
the models (constrained best -1200 vs -1157 unconstrained, quadgram).

## What was done

**Language models** (`lm.py`, `qg.py`, `ng5.py`). Scots corpus of 3.49 M letters: *Diurnal of Occurrents*,
*Register of the Privy Council* i, Pitscottie's *Historie and Cronicles* i and iii, and the Scots quotations in
Bain ii. Held out for controls: *Historie and Life of King James the Sext*. Two OCR traps cost the first hour and
are worth recording: Roman numerals (`iiij`, `xviij`) and the OCR habit of reading *n* as `ii` make runs of *i*
cheap, so the solver converged on `iiiwiiiaiii…` until such tokens were filtered (also tokens with `j`, tripled
letters, 4 vowels or 5 consonants in a row). Quadgram table with additive smoothing; 5-gram with interpolated
absolute-discount backoff. Comparison tables in English (Bain's calendar prose), French (Labanoff vii) and
Latin (Buchanan, *Rerum Scoticarum Historia*).

**Solver** (`solve2.py` quadgram, `solve3.py` 5-gram): simulated annealing over the 32-symbol → 26-letter map,
250 000 steps, geometric cooling 8 → 0.2, single-symbol and swap moves, 24-60 restarts.

**Matched controls** (`control2.py`, `control3.py`): 134-letter windows of the held-out Scots text, 32 symbols
(one per letter present, the remaining symbols as homophones of the eight commonest letters, main symbol used
60 % of the time), same solver.

| model | control recovery (fraction of letters) | target best | target reading |
|---|---|---|---|
| quadgram | 0.85, 0.46, 0.73, 0.31 (mean 0.5) | -1157.2 (4 of 24 restarts identical) | `tnesenantairneteneandertationentinthe…` |
| 5-gram Scots | **0.93, 0.98, 0.97, 0.96, 0.97**, 0.11 (5 of 6 ≥ 0.93; scores -191 to -260) | **-269.5** (60 restarts; top four within 3 nats) | `tsederunttagreteneundersasabsendinthemtoatstratserinthesatnetreiteeistittodartisheattheirsettisneteirtosdistheisseetareareindisthemais` |
| 5-gram + word segmentation polish (`solve4.py`) | 1.00, 0.35, 0.10, 0.00 — the polish hurts, abandoned | -620.7 (solved control: -433) | fragments only (*in them that*, *at their*) |
| 5-gram English | — | -273.8 | gibberish |
| 5-gram French | — | -252.3 | `ietatepearlbetitetpertuerelleterre…` |
| 5-gram Latin | — | -268.1 | gibberish |

Calibration of the one 5-gram control failure: its true plaintext scored -319 under the model, worse than the
solver's wrong answer (-279). Over 400 random 134-letter windows of held-out Scots the true text scores
mean -235.7, sd 32.5; **12.75 % of genuine Scots passages score below the target's optimum of -269.5**. So a
passage of ordinary Scots prose would very probably have been read (5 of 6 controls), but a passage that is
atypical for the model — Border news is names and places: Herries, Lochmaben, Hoddom, Lochinvar, Annandale —
can sit below the solver's false optimum, exactly as the failed control did.

**Nulls and homophones** (`nulltest.py`, `famtest.py`). Dropping any one of the 13 symbols with ≥ 3 occurrences
moves the per-letter quadgram optimum by at most 0.16 nats (base -8.84; range -8.68 for `19` to -8.95 for
`10`): no symbol behaves as a null. Dropping the whole z family (-8.68 on 113 letters) or x family (-8.91 on
110) is no better; merging the x variants (-9.13), the z variants (-9.30) or all families (-9.29) is worse, so
Tomokiyo's variants are distinct symbols, as his notation implies. Neither family is a word separator: taken as
spaces they give word lengths of 0, 1 and 21 or 28.

**Nomenclator** (`solve5.py`): treating the 9 hapax or the 16 symbols with ≤ 2 occurrences as word codes and
scoring only the 5-gram windows between them gives -2.03 and -1.90 per window and still no reading; but the
matched control with 26 word-code positions planted fails too (0.09, 0.05, 0.19), so this test has no power at
this length and the nomenclator question is open. Number symbols as word codes, letter symbols as word codes,
x and z families as word codes: same outcome (`nomen_custom.txt`).

**Crib dragging** (`cribdrag.py`, `crib2.txt`): twenty words and names (the quene, hir majestie, Lethingtoun,
secretare, the lettres, the Duke, Argyle, Huntlie, Herreis, Ingland, France, quhilk, thairfoir, Hamiltoun,
Elizabeth, the quene of Ingland, your grace, my lord, the lordis, nobilmen) placed at every consistent position
and the rest annealed under the constraint (80 000 steps, 4 restarts per placement; 730 placements in all,
`crib2.txt`). Best placement -280.4 (*Ingland* at 74), then *Argyle* at 43 (-286.7), *Huntlie* at 73 (-289.9),
*secretare* at 37 (-290.2), *Herreis* at 73 (-291.4); *thequene* at best -304. Every placement sits 11 nats or
more below the unconstrained optimum of -269.5 and the decrypts round the cribs stay gibberish, so no crib is
supported.

## Where it stands

Undetermined, not excluded. The ciphertext as transcribed is not read by a homophonic-substitution attack that
reads five of six matched Scots controls, nor under English, French or Latin models, and no symbol behaves as a
null or separator. Two explanations remain open and cannot be separated at 134 groups: an atypical, name-heavy
plaintext (13 % of genuine Scots windows score below the false optimum), or word codes among the symbols, as
the Queins Cipher of the same year has. Tomokiyo's "seems simple" is right about the symbol count, but 134
groups over 32 symbols is at the unicity edge for this class once the text departs from ordinary prose.

**Route in.** (1) The page: Add MS 32091 f. 213, for the clear text round the cipher (which fixes the subject
and gives running cribs) and to confirm the symbol set; BL images are offline, so a reader's photograph or the
BL reprographics service. (2) A second letter in the same cipher: Moray-Wood correspondence June-September
1568 (Sussex forwarded "a packet from Murray to Mr John Wood" on 6 Sept 1568, Bain no. 805; Wood's letters to
Cecil have cipher words, no. 804) — the Cecil Papers at Hatfield and TNA SP 52/15-16 are where they would be.
(3) The Moray papers (NRS GD... / Darnaway): the seven Donibristle ciphers of the HMC report, five never
reproduced, one "partly composed of Arabic numerals" — the nearest thing to a candidate key.

## Files

`elizabeth_moray.txt` (Tomokiyo's transcription) · `lm.py`, `qg.py`, `ng5.py`, `wordscore.py` (models) ·
`solve2.py`-`solve5.py`, `cribdrag.py`, `nulltest.py`, `famtest.py`, `control2.py`-`control4.py` (attacks and
controls) · `run*.txt`, `control*.txt`, `famtest3.txt`, `nulltest3.txt`, `nomen_*.txt`, `crib2.txt` (outputs).
Downloaded editions, n-gram tables and Tomokiyo's images are not committed (`.gitignore`); rebuild with
`python ng5.py <corpus files>` and `python -c "import qg; qg.build([...])"`.

## Checked / not checked / user must verify

Checked: Tomokiyo's transcription fetched and counted; Catalogue of Additions entry; Bain ii for July-August
1568 and for any Add MS 32091 item; HMC 6th Report Moray section; Tomokiyo's Mary article for the 1569-71
Scottish keys; DECODE public list; all runs above with their controls.
Not checked: the manuscript itself (offline); the Cecil Papers (HMC Salisbury i) and TNA SP 52 for a sibling
letter; Claire Webb's St Andrews thesis on Moray's diplomacy (repository returned 503 twice).
User must verify: the conclusion "undetermined" rests on Tomokiyo's symbol identities; one misread variant
would change the frequency profile the controls were matched to.
