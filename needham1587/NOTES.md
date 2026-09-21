# Francis Needham to Walsingham, 28 July 1587: BL Harley MS 287 ff. 39–40 (DECODE R8479)

Status: read (every cipher run of f. 39v deciphered; one word of about six letters on line G unsure; the f. 39r
and f. 40r runs were already read at the time in interlinear glosses and a margin note)

Catalogue item 133 ("Needham to unknown recipient, 28 Jul 1587", scored by rule).

## The document

Four DECODE images of Harley MS 287 ff. 39–40:

| image | folio | what |
|---|---|---|
| 1 | f. 39r | Letter opens "It may please your honour. The sudden departure of the bark ... before Sluce". Clear English with short cipher runs. Interlinear glosses and a margin note in another hand give their meaning: "aboute my L. of Lecester", "as by Burgrave said", "my lord of Lecester and Mr Norris", "is the L. North". |
| 2 | f. 40r | End of the letter, clear with two glossed cipher words ("Sr William", "Burgrave"); signed and dated 1587. |
| 3 | f. 40v | Address leaf; endorsed "28 July 1587. From Needham". |
| 4 | f. 39v | The densest page: six cipher runs (lines A, C, D, F, G, H below), **not glossed** except for four words ("advise", "enemyes", "campe nor the towne") and three lower down ("Mr Burley", "the Spaniard", "were removed hence"). |

The writer is **Francis Needham**, Walsingham's servant, who went with Leicester to relieve Sluys in July 1587. CSP
Foreign vol. 21 pt 3 (1929) calendars his letter of the same day from Flushing (SP 84/16 f. 216, pp. 206–8: the
council aboard Leicester's ship before the haven of Sluys, the firework ship, the want of boats, "this commission
must come from the States", the surrender of Sluys). The Harley letter tells the same story (its f. 39r ends on the
boats and "the commission from the States") and is either a second letter of the same day or Needham's own
fuller version. The Harley leaves are not calendared. The calendar notes (p. 237 n.) that Needham used with
Walsingham the cipher of Thomas Wilkes, whose key is at the front of BL Add MS 5935 (not online; p. 35 n. 4).

## The cipher

A three-grid pigpen. Nine box shapes, each in three forms: plain, with a dot below, with a dot inside. Order of
the shapes and letter values (the shapes are described as drawn; how they sit in the grid was not checked against
the key):

| order | shape | plain | dot below | dot inside |
|---|---|---|---|---|
| 1 | ⌟ (J) | a | k | t |
| 2 | ⊔ (U) | b | l | u/v |
| 3 | ⌞ (L) | c | m | w |
| 4 | ⊏ (C) | d | n | x |
| 5 | □ (O) | e | o | y |
| 6 | ⌜ (F) | f | p | z |
| 7 | ⊓ (N) | g | q | — |
| 8 | ⌝ (7) | h | r | — |
| 9 | ⊐ (D) | i | s | — |

So the alphabet a–i, k–s, t–z runs straight through the three grids (no j; u = v). Words are divided. No
homophones, nulls or code names were met on f. 39v.

**How it was found.** The glosses "advise", "enemyes" and "campe nor the towne" gave e, n, o, r, s, t, h, w, m;
"Burgrave" gave b, u, g. Line A then read "want of intelligence" and line D "whether there was any bridge or not",
after which the alphabetical layout of the grids was evident and fixed the remaining cells. A quadgram annealer
(`solve.py`) was built but not needed.

The first transcription pass had two recurring slips, which the grid layout corrects: the dot of ⌟ (t) was read
below instead of inside (giving k), and dots below were sometimes attached to the neighbouring sign. Dots sit
under the lower-left of their sign; the script slants right.

## Reading of f. 39v (cipher in italics; clear text paraphrased where not transcribed)

- **A**: "... we had *want of intelligence* these five days last past ..." — the gloss "advise" above the next
  cipher word: "we could have no *advise* out of the *enemyes campe nor the towne*".
- **C–D**: "and we were so far from knowing what was meet to be done at that time [that] we *knewe not whether
  there was any bridge or not, or whether there were any at the chanel*".
- **F–G–H**: "... *and that the chanel was b[…]ed with hoyes and flyboates fastened wyth chaynes, strengthned
  behind wyth flatt bootes*."

The rest of f. 39v is clear: Sir Roger Williams' sally, the storm, the enemy's hundred files at the walls, the
state of the town, Count Maurice, Colonel Morgan and Russell; the lower glosses ("Mr Burley", "the Spaniard",
"were removed hence") were read at the time.

The reading agrees with the calendared despatch of the same day, which says the fireship could hardly be brought
up to "the bridge" across the haven: Parma had closed the channel with a boom of boats.

## What remains open

- Line G, word 3: b + four signs + "ed" (`U ? ? ? ? O C`), a verb for how the channel was closed. The four signs
  are cramped and one is blotted; "barred" fits the sense but not the count. Grade M.
- The clear text of ff. 39r–40r has not been transcribed in full here; only the cipher mattered.
- Add MS 5935 (the Wilkes key) was not consulted; the rebuilt key would be checked against it.

Files: `cipher.txt` (sign transcription), `decode.py` (key and decoder), `solve.py` (annealer, unused),
`trans_*.txt` (first-pass transcriptions by agents, with the slips noted above). Images in `img/` are DECODE
scans, git-ignored.
