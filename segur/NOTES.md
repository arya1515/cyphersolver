# Henry of Navarre to Ségur, BnF 500 de Colbert 401 ff. 233, 239, 288v (1585–86) — SOLVED 2026-09-16

**Status: the key is recovered and the three ciphered letters of 1585–86 are read in substance.** The alphabet, the
syllabary and the double-letter signs are fixed; a dozen word-signs written in letters (*pi*, *na*, *gne*, *H*, *L* …) and
three nomenclature numbers (180, 215?, 900) are glossed from context or left open. The 1583 letter at f. 143 is in a different
cipher and is not read. Tracker item #12; short-list candidate 4 of 2026-09-16.

## Corrections to the catalogue entry

- **Sender.** Tomokiyo's page lists these as letters of *Henry III*. They are signed *Henry* at Montauban (f. 239, 1586) and
  La Rochelle (f. 321, 11 June 1586), close "vostre affectionné maistre et parfait amy", and speak of "mon frere Mons.r le
  Prince" (Condé), "mon cousin le duc de Montmorency", the levy of reiters by the duke Casimir and Clervant: they are letters of
  **Henry of Navarre**, whose envoy to the German princes Ségur-Pardaillan was (the volume is titled *Négociation de M. de Ségur
  … pour le roi de Navarre avec les Princes protestans d'Allemagne, 1584–1588*). The f. 321 key Tomokiyo reconstructed is
  therefore also a Navarre cipher.
- **f. 143** (Beaupréau, July 1583) is not from the king either: it is *to* Ségur from a correspondent signing "vostre tres
  humble et tres … serviteur", and its clear text is about the cipher itself: *"Il me semble qu'il n'est point besoin d'autre
  alphabet, vous y avez toutes choses tellement dispersées en lettres, syllabes, doubles, nulles et tout le reste qu'il est
  impossible de le descouvrir … Les noms sont en lettres et syllabes."* That sentence is a description of the design found
  below (letters, syllables, doubles, nulls; names written with letter-signs), in a different key.

## Sources and access

- Gallica, ark:/12148/btv1b10035574w, 440 canvases, labels all "NP". IIIF manifest and images answer a script with a browser
  User-Agent (`fetch_gallica.py`; the 15 Sept block was transient). Canvas ≈ folio + 11 at f. 139, + 23 at f. 227, + 38 at f. 294.
  Cipher folios: f. 143 = canvas 154; f. 233 = 257; f. 239 = 263; f. 288v = 325 (left page); f. 321 = 359; f. 333 ≈ 370.
  Full-resolution images are 7749 × 6057 px; not committed (`img/`, `probe/`, `crops/` are git-ignored).
- Transcriptions: `ct_233.txt` (220 tokens), `ct_239.txt` (70), `ct_288.txt` (196), `ct_143.txt` (63, different key). Clear text
  in brackets. Re-read at 2× zoom for every digit the reading disputed (`crops/`).

## The design (recovered)

The numbers 1–53 are letters, doubles and a null in **alphabetical order with two or three homophones per letter**; 54–123 are
**seventy syllables, fourteen consonants × five vowels in alphabetical order**; word-signs written in letters and a few numbers
above 123 are names and words.

| numbers | value | evidence (words read) |
|---|---|---|
| 1 | *ee* / *ée* (double) | la lev**ée**, fortifi**ée**s |
| 2 | *ll* (double) | mi**ll**e |
| 3 | unread double (not in the 1585–86 letters) | — |
| 4 5 6 | a | **a**vec, **a**ucun, c**a**s |
| 7 8 | b | o**b**ligé |
| 9 10 | c | con**c**lure, **c**eux, du**c**, **c**hemin |
| 11 12 | d | **d**ix, gran**d**e |
| 13 14 15 | e | passim |
| 16 17 | f | (no plain *f* occurs; the syllables carry it) |
| 18 | g | **g**rande |
| 19 20 21 | h | mar**ch**er, **ch**emin, Daul**ph**iné |
| 22 23 24 | i / j | d**i**x, **j**e ne sçay, fa**i**re |
| 25 26 | l | mi**l**, qu'i**l**, **l**a |
| 27 28 | m | pro**m**ptement |
| 29 30 | n | passim |
| 31 32 33 | o | **o**bligé, **o**u |
| 34 35 | p | **p**romptement, **p**lus |
| 36 37 | q | (none in clear; *que/qui* are syllables 100/101) |
| 38 39 | r | passim |
| 40 41 42 | s | passim |
| 43 44 | t | passim |
| 45 46 47 | u / v | a**v**ec, **v**ous, Vi**v**arès |
| 48 (49) | x | di**x**, ceu**x**, deu**x** (49 once, else 49 = y) |
| 49 50 | y | mo**y**en, sça**y**, a**y**t |
| 51 | z | advisere**z**, oblige**z** |
| 52 | *et* | capituler **et** conclure, consentement **et** faire |
| 53 | null / word end | after *adviserez*, *obligé*, *Eglises*; between *H* and *L* |
| 54–58 | ba be bi bo bu | **bi**en, o**b**ligé (7), **bu**? |
| 59–63 | ca ce ci co cu | **Ca**simir, **ce**ux, en **ce** **ca**s, **co**nclure, se**co**urs |
| 64–68 | da de di do du | **Da**ulphiné, **de**ux, **di**ligence, a**du**iserez |
| 69–73 | fa fe fi fo fu | **fa**ite, **fe**i-re (faire), forti**fi**ées, **fo**urnir |
| 74–78 | ga ge gi go gu | obli**gé** |
| 79–83 | la le li lo lu | **la**, **le**, ob**li**gé, p**lu**s |
| 84–88 | ma me mi mo mu | **ma**rcher, prompte**me**nt, **mi**lle, **mo**yen, re**mu**ez |
| 89–93 | na ne ni no nu | **ne**cessaire, four**ni**r, **no**s |
| 94–98 | pa pe pi po pu | **pa**r, **pi**eces, **po**ssible, de**pu**is |
| 99–103 | qua que qui quo quu | **que**, **qui** |
| 104–108 | ra re ri ro ru | cont**ra**cte, **re**istres, esc**ri**re, p**ro**mptement |
| 109–113 | sa se si so su | **se**cours, Ca**si**mir, **so**nt, **su**is |
| 114–118 | ta te ti to tu | consen**te**ment, for**ti**fiées, **to**ut, capi**tu**ler |
| 119–123 | va ve vi vo vu | Cler**va**nt, le**ve**e, **vo**s |
| □ (square glyph) | *ss* (double) | nece**ss**aire (twice) |
| pi | *est* | s'il vous **est** possible, qui ayt **est**é faite, Clervant **est** obligé |
| Ra | *faictes* / *faire* | **Faictes** s'il vous est possible la plus grande levée |
| qu | *vous* | s'il **vous** est possible |
| na | *affaires* or *nouvelles* | de vos **na** depuis …; en quel estat sont nos **na** |
| gne (f. 288v) | *Je* | **Je** suis en extreme peine |
| gne gna (f. 239), pe pu, e, X, gla, H, L, Ne, qua, 180, 900 | word-signs, unread | see `reading.md` |

Alphabetical homophone counts (3 for a e h i o u, 2 for b c d f l m n p q r s t, 1 for g x z) are exactly the design of the
f. 321 key that Tomokiyo reconstructed (a 12–14, e 20–23, i 30–32, …, syllables ba–vu 63–142 consecutively, nomenclature from
162): the same chancery pattern with different offsets. In this key the syllable table starts at 54 and has fourteen
consonants (b c d f g l m n p q r s t v; no h, j, x, z rows), and the doubles and the null sit at 1–3 and 53.

## How it was solved

1. **Statistics.** 461 numeric tokens over 102 distinct values, 25 letter-written glyphs. Values 1–53: 311 tokens; 54–123:
   146; above 123: 3. The frequencies of 64–123 taken mod 5 are 60 / 30 / 22 / 20 / 14 for one alignment and nearly flat for
   the other four: **blocks of five with one dominant slot**, the a-e-i-o-u signature of an alphabetical syllabary (e most
   frequent). That fixed the syllable structure before any letter was known. (The alignment is right; the start was first
   put at 64 and corrected to 54 from the reading, see step 4.)
2. **Structured annealer** (`solve.py`): numbers below the block start are free homophones (22 letters + null, null capped at
   8 symbols with a 3-nat penalty per dropped letter); each block of five is one consonant plus the fixed vowel; letter-glyphs
   and numbers above the table are skipped; the surrounding **clear French is kept as fixed context** for a 5-gram model
   (du Croc corpus: Catherine de Médicis, Teulet, Labanoff, 9.4 M letters, u=v, i=j, no spaces). Moves: reassign or swap a
   letter symbol, reassign or swap a block consonant. 300 000 steps, 12 seeds: 5 of 12 converge on one key at −6223.3.
3. **Controls** (`control.py`, `eval_control.py`): Catherine de Médicis' letters enciphered with random keys of the same
   shape, same token counts and the same clear-text interleaving. With the 64-start model: control 1 recovered 47 % of letter
   tokens and 4/12 blocks, control 2 90 % and 10/12. With the 54-start, 14-block model (control 3): **96.6 % of letter tokens
   and 12 of 14 blocks** (the two missed are *x* and *f*, one token each). So the method reads a text of this size when the
   structure is right, and not always when it is not.
4. **Reading.** The blind key already gave *capituler et conclure promptement avec ceux que vous adviserez … le duc Casimir …
   faire la levée … la faire marcher le plus tost, quelque prompt secours, deux mille reistres, dix mil escus, chemin, Vivarès,
   Daulphiné, n'espargner aucun moyen … secourir en toute diligence, la plus grande levée qui ayt esté faite, Monsieur de
   Clervant est obligé fournir, nos places sont bien fortifiées*. Against the final key it had **86 % of the letter tokens
   right (241/280) and 77 % of the syllable tokens (127/165)** despite the wrong block start; the letter part came out
   alphabetical on its own (a 4–6, b 7, c 9–10, d 11–12, e 13–15, g 18, h 20–21, i 22–24, l 26, m 27–28, n 29–30, o 31,
   p 34–35, r 38–39, s 40–42, t 43–44, u 45–47), which is the independent check. Reading *et conclure* (52 62 29 9 83 105),
   *secours* (110 62 46 39 42) and *le duc Casimir* (80 68 9 59 111 86 38) forced 62 = *co*, 59 = *ca*, 65 = *de*, 56 = *bi*
   → the table starts at 54 with b c d …; *que vous* (100 47 …) and *qu'il* (101 25) fixed 99 = *qu*; *Clervant* fixed
   119 = *va*. Rerun blind with the corrected structure (start 54, 14 blocks; `run_target14.log`), 6 of 8 seeds agree at −6201.9 and the key has **88.9 % of the letter tokens (249/280), 90.9 % of the syllable tokens (150/165) and 11 of 14 blocks** right against the final key; its only null is 52 (*et*), and the three blocks it misses are *b*, *qu* and *v* (the model writes *v* as *u*, and *qu* is a two-letter consonant it cannot represent).
5. **Digits disputed by the French were re-read at 2× zoom.** Confirmed as written: 20 in *a-v-i-h* (avec), *contra-h-te*
   and *Valen-h* (20 = h everywhere else; the encipherer's slip for 10 = c, or the key really doubles c at 20 — the three
   *ch* words read with 9/10 + 20 exclude that); 46 in *e-v-c-ri-re*. Corrected by re-reading: line 5 of f. 288v ends
   `80 40 65 45` (*les deux*, not 90); the interlinear insertion is `… 65 9 80 38 119 29 44` (*de Clervant*, not 63) and its
   caret sits after 111 in line 6, so *mon-si-[eur de Clervant]-est obligé*; `1579` at line 9 of f. 233 is *15 79* or the year.

## What the letters say

Navarre, October 1585 (a month after the bull of excommunication and the loss of his Guyenne places to Mayenne's army), tells
Ségur in Germany to conclude promptly with whoever he judges fit, if possible with Duke [John] Casimir or with his consent, to
raise the largest levy he can and to march it at once; he is writing to Clervant to raise the two thousand reiters he is
bound to furnish under the contract with the Churches, or part of them, using the ten thousand écus from [180] if he has no
other means; and he wants to know the route the army will take — the Vivarais or Dauphiné roads would suit. In February 1586
from Montauban: spare no means, succour us in all diligence, set every piece in motion, commit everything to it. On 1 April
1586 (slip): he is in extreme anxiety at having no news since [e], does not know where or to whom to write nor how their
affairs stand; make, if you can, the greatest levy ever made; the two thousand reiters Clervant is bound to furnish are very
necessary to us, and even more [H] [L]; assistance and succour are very necessary; our places are well fortified; we have
sent [someone] to … of whom we have long had no news. The postscript hand *D.* on f. 239 adds Drake's "very great prize" (the
sack of Santo Domingo, January 1586) — *le premier homme de marine … qui soit au monde*. All consistent with the German levy
of 1586–87 that Ségur, Clervant and Casimir were negotiating (Segesser, *Ludwig Pfyffer*; de Thou; the Ségur négociation
volumes themselves), which marched in 1587 to the disaster of Auneau. *Inferences, not readings: 180 = the Queen of England
(Elizabeth's subsidy for the levy); H, L = Hollande, Lorraine or similar.*

## Not done / open

- The word-signs (X, gla, gne, gna, pe, pu, e, H, L, Ne, qua, Ra) and numbers 180, 215?, 900: a fourth letter in the same
  key, or the key sheet itself (not in this volume — checked ff. 321/333 are the other key), would gloss them.
- f. 143 (1583): 58 numeric tokens (max 156, code numbers 134/136/156 in the clear text) in a different key of the same
  design, from a correspondent at Beaupréau to Ségur. Not attackable at this length; its clear text is the useful part.
- f. 321 and f. 333 (Tomokiyo's reconstruction): not re-derived here.
- Misreadings I may have made: 93 (*nuine* for *peine*, 95), 66 (*pie-bes* for *pieces*, 60/61), 28 (*emlises* for *Eglises*,
  18), the 20/10 question. All flagged in `reading.md`.

## Files

- `ct_233.txt`, `ct_239.txt`, `ct_288.txt`, `ct_143.txt` — transcriptions with clear text in brackets.
- `key_v4.json` — the key (letters, blocks, glossed glyphs); `key_v1.json` the blind annealer's key; `decode.py key_v4.json`
  renders the letters; `decode_v4.txt` its output; `reading.md` the edited reading with token notes.
- `solve.py` (structured annealer; `BLOCK0`, `NBLK`, `NULLPEN`, `MAXNULL` env), `control.py`, `eval_control.py`, `load.py`,
  `crop.py`, `fetch_gallica.py`; logs `run_target.log`, `run_control1..3.log`, `run_target14.log`; `henryiii.htm/.txt` the
  cryptiana article as fetched.

Checked: transcription of the three letters at full resolution and 2× re-reads of disputed digits; mod-5 structure; three
matched controls; convergence over seeds; alphabetical order of the recovered key; word-level French of every cipher span.
Not checked: the f. 321 key against Tomokiyo's table token by token; the identity of the word-signs; the historical glosses
(Casimir, Clervant, the 1579 contract, Drake). User must verify: the sender attribution before it is reported to Tomokiyo,
and the readings marked ? before they are quoted.
