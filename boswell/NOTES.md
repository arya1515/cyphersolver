# Charles I and Nicholas to Boswell, 2 November 1643 (TNA SP 84/157 ff. 217, 219) — NOTES

**Verdict: alphabet SOLVED (by Robert Pitt, September 2026; verified here against a permutation control),
text READ in substance; the residue is single-occurrence word codes and slips in a provisional transcription,
which only the manuscript can settle.** Not first: Pitt's repository (`robertpitt/charles-i-boswell-cipher`,
commit 609ebf4, 14 September 2026) had the alphabet, the supplementary homophones, most nulls and four word codes
before this session began. What is added here: the statistical control, the identification of the four graphic
signs and of the addressee, the TNA references, the historical frame (the Duke of Courland's envoy, the Dutch
embassy of 1644), a table of the transcription slips the reading implies, and a full connected reading of both
letters.

Session 2026-09-16. Target from Tomokiyo, *Unsolved Historical Ciphers*, "Charles I–Boswell Cipher (1643)";
transcription from his blog post of 17 September 2021 ([src/blog.txt](src/blog.txt), copied verbatim into
[charles.txt](charles.txt) and [nicholas.txt](nicholas.txt); Pitt's inputs are line-for-line the same text).

## 1. Sources

| Source | What it gives | Where |
|---|---|---|
| TNA Discovery | **SP 84/157/96, f. 217 "Charles I to Boswell - in cipher"** and **SP 84/157/97, f. 219 "Nicholas to Boswell - in cipher"**, both 2 Nov 1643, State Papers Foreign, Holland. Item-level catalogue only; no images online | Discovery API, browser User-Agent required (2026-09-16) |
| Tomokiyo, blog 17 Sept 2021 | Provisional transcription of both letters, asterisks where unsure; author not sure of the recipient's name | [src/blog.txt](src/blog.txt) |
| R. Pitt, `charles-i-boswell-cipher` (GitHub, MIT) | The periodic alphabet 20–115, 31 supplementary homophones 116–159, proposed nulls, 588 = of, 800 = to, 835 = un, 291 = Duke; decoder, tests, FINDINGS.md | cloned to scratch, commit 609ebf4 |
| H. F. Morland Simpson (ed.), *Civil War Papers*, in *Miscellany of the Scottish History Society* I (1893), pp. 143–170 | **Charles I to Duke James of Courland, Oxford, 2 Nov 1643 (duplicate)**: "Yor credentials of the 14th of August last for the gentleman by you designed to Vs in qualitij of yor Envoye were transmitted by him hither by the convoyance of 212, 364 … these Our Re-credentials"; cipher line `291, 588, 45, 135, 52, 25, 20, 50, 81` (= Duke of Curland). Memorial by the Duke's envoy (1645?): he was to cross to England but "the passage not being free … I treated with the ministers of their Majesties at the Hague, who dissuaded me from the voyage … to whom I delivered the letters for his Majesty"; the Duke offered men and ships, then munitions; 100 quintals of powder sent to Amsterdam. Firks, Major Georg von, the Duke's agent | IA `miscellanyofscot01scot`, OCR in [src/simpson_djvu.txt](src/simpson_djvu.txt) lines 11285–12800 |
| CSPD 1641–43 (Hamilton, 1887) | Nicholas to Roe, Dec 1643: "Arms and powder are arrived at Dartmouth for his Majesty" | IA `sim_great-britain-public-record-1625-1649-domestic-series_1641-1643` |

## 2. Structure (from [key.py](key.py); counts over both letters, 455 numeric groups, 171 distinct, 69 hapax)

| band | occ. | distinct | hapax | occ./distinct | what it is |
|---|---|---|---|---|---|
| 0–19 | 45 | 17 | 4 | 2.65 | **nulls** (never needed by any reading; sit inside and between words) |
| 20–115 | 276 | 80 | 17 | 3.45 | **alphabet**, 24 letters × 4 homophones (96 predicted, 80 seen; q and z unused) |
| 116–159 | 61 | 31 | 14 | 1.97 | **supplementary homophones** for a d e i m n o r s t u y, in alphabetical blocks |
| 160–399 | 25 | 22 | 19 | 1.14 | **nomenclator** (words), plus a null block 361–386 |
| 400–999 | 48 | 21 | 15 | 2.29 | nomenclator continued; 800 (to) ×14, 588 (of) ×7, 873 (you) ×6 |

The frequency separation the queue entry asked for is therefore clean: the alphabet is 20–115 and its usage is
even (per letter, the four homophones are used e.g. e 7/4/13/5, s 10/5/5/6, r 5/5/3/8).

### 2a. The alphabet (Pitt)

```
plain   a  b  c  d  e  f  g  h  i  k  l  m  n  o  p  q  r  s  t  u  w  x  y  z
1st     20 32 21 33 22 34 23 35 24 36 25 37 26 38 27 39 28 40 29 41 30 42 31 43
2nd     44 56 45 57 46 58 47 59 48 60 49 61 50 62 51 63 52 64 53 65 54 66 55 67
3rd     68 80 69 81 70 82 71 83 72 84 73 85 74 86 75 87 76 88 77 89 78 90 79 91
4th     92 104 93 105 94 106 95 107 96 108 97 109 98 110 99 111 100 112 101 113 102 114 103 115
```

i.e. `letter = row[(n-20) % 24]` with `row = acegilnprtwybdfhkmoqsuxz`, the odd then the even positions of the
24-letter alphabet (no j, no v). Each letter's four values are 24 apart. This is the same *type* as the regular
Stuart keys Tomokiyo describes for Scudamore 1636, Cave 1638 and Ormonde–Clanricarde 1643 ("three or six figures
to each letter in regular arrangement"), and as the Maltravers–Ormonde key read in `ormonde/`.

### 2b. Supplementary homophones 116–159 (values observed; Pitt's, one added)

```
116 a  117 d  118 e  119 ?  120 m  121 n  122 o  123 r  124 s  125 t  126 y     block 1: a d e (h/i) m n o r s t y
127 a  128 d  129 e  130 ?  131 n  132 o  133 ?  134 t  135 u  136 ?  137 ?     block 2: a d e (i) n o (r/s) t u ..
138 e  139 ?  140 ?  141 r  142 s  143 ?  144 ?                                block 3: e .. r s ..
145 a  146 e  147 i  148 o  149 r  150 s  151 u  152 ?                          block 4: a e i o r s u (y?)
153 a  154 e  155 ?  156 ?  157 ?  158 u  159 y                                 block 5: a e .. u y
```

Each block is alphabetical, so the unseen values are constrained (119 is h or i, 130 i, 133 r or s, 139–140 from
h i n o). `142 = s` is added here from Nicholas's opening `484 C O M 127 131 128 142` = "[His Majesty] comands".

### 2c. Nulls

0–19 (17 of the 20 values occur; 0 once, in `P 0 S S I B L E`, where it may be a plain "o" misread as a zero) and
361 362 364 374 376 377 380 381 386. No reading anywhere needs any of them. `6_` and `8_` in the date are digits
of the date, not nulls (see §4).

### 2d. The four graphic signs — the new finding

Tomokiyo renders four signs: △, 中, □ and +. Each occurs **once inside a spelled word and afterwards on its own**,
and the stand-alone occurrences come in exactly the combination the embedded ones predict:

| sign | embedded occurrence (Charles) | stand-alone occurrences | value |
|---|---|---|---|
| △ | `47 86 △ 110 33` = GO△OD | `back to OUR △ 中 873 □` | **good** |
| 中 | `93 122 中 41 112 in` = CO中US-in | `Our 中 873 □ S affeccons`, `our said 中 873 □`, `our △ 中 873 □` | **Cousin** |
| □ | `61 116 88 □ 77 70 28` = MAS□TER | same three places | **Master** |
| + | `158 ＋ 150` = U＋S ("inuiting us") | `acceptable to +`, `preiudiced +`, `to + to the port of`, `addres by 213 to +` | **us** |

So `△ 中 873 □` = "good Cousin your Master", and the three framed passages read "Our Cousin your Master's
affeccons & offers", "to assure our said Cousin your Master", "back to our good Cousin your Master, to whom we
herewith send your re-credentials". The clerk evidently wrote the sign beside the word the first time he spelled
it (compare "for whom 270 thus hereafter" in the Ormonde letter, where a code is introduced inline), and Tomokiyo
transcribed the sign in the middle of the spelled word. This is the explanation Pitt's notes said was missing
("repeated graphic-enclosed occurrences are NOT explained by this assignment"). With it, `873 = you / your`
(Pitt's guess) fits all six occurrences: "received your ciuill … letter", "the Duke of Curland's, your Master",
"pleasure to you[r]", and the three framed ones.

### 2e. Word codes

| code | occ. | reading | basis |
|---|---|---|---|
| 800 | 14 | to | every occurrence is prepositional or before an infinitive; both letters |
| 588 | 7 | of | both letters; "OF F E R S" = offers |
| 873 | 6 | you / your | §2d; Nicholas `873r` |
| 291 | 2 | Duke | external: Simpson's cipher line `291 588 C U R L A N D` on the letter *to the Duke* |
| 516 | 2 | letter | "received your ciuill … [516] of the 6th of 8ber", "any [514] [516] of Our good Cousin" |
| 591 | 2 | our? | "we acknowledge [591] [749] thereby highly obliged" wants "our selves"; second occurrence `A C 591 & E S 126` unresolved |
| 854 | 2 | will? | Nicholas "they [854] doe more hurt then good"; Charles "most [854]e-com-ly receiue" wants *wel*(comly): conflict, one of the two tokens is probably misread |
| 835 | 1 | un | "[835] D E R stand" = understand |
| 749 | 1 | selves | with 591 above |
| 750 | 1 | send | "herewith [750] your re-credentials" |
| 205 | 1 | assure | "to [205] our said Cousin your Master & to lett him understand" |
| 223 | 1 | by | "there[223] highly obliged" = thereby |
| 629 | 1 | pray / desire | "we [629] you therefore to present our princely thanks" |
| 640 | 1 | port(s) | "to the [640] of Weymouth, Dartmouth, Exeter, Falmouth or [228]" |
| 228 | 1 | Bristol? | fifth Royalist port; only a guess |
| 185, 755, 188, 539, 639 | 1 each | assistance; store?; armes?; musket(s); powder? | "receiue his [185] with in [755] [188] [539]s, match & [639]"; the Duke's memorial and his later shipments name muskets, powder, match and lead |
| 636 | 1 | pro- | "[636]por[tion]" |
| 406 | 1 | gener- | "[406]ous" |
| 484 | 1 | His Majesty | Nicholas's opening "[484] comands [me] to signify his pleasure" |
| 746 | 1 | secret- | "otherwise [746]ly to hinder" |
| 170, 181, 726 | 1 each | see §5 | Nicholas: "by your meanes of the [170] & otherwise secretly to hinder the coming ouer of the [181]s from the [726]" |
| 177, 213, 289, 514, 303 | 1 each | unresolved | 213 is the intermediary who carried the envoy's address to Oxford (Simpson's letter has `212, 364` for the conveyance of the credentials; not the same number, do not conflate) |

**The nomenclator looks alphabetical.** Sorting the codes with a reading: a 170–228 (assistance, assure, are, by,
Bristol), d 291 (Duke), g 406 (gener-), h 484 (His Majesty), l 514–516 (letter), m 539 (musket), o 588–591 (of,
our), p 629–640 (pray, pro-, powder, port), s 726–755 (secret-, selves, send), t 800 (to), u 835 (un), w 851–854
(which, will), y 873 (you). One clash: 190 "are" after 185 "assistance". Two of Pitt's exploratory guesses fall
outside their letter's range under this ordering (303 = "two", 376 = "both"; both sit where d/e-words and the null
block are), so they are not adopted here. The ordering is a hypothesis*; a second letter in the key would test it.

## 3. Verification

`permtest.py`: the 21 maximal runs of four or more alphabet groups (106 letters) scored with a 4-gram model built
from 2.7 million characters of 17th–19th-century English in the repo (`lm4.py`); the null permutes the 24 letter
identities over the same periodic structure.

| | score |
|---|---|
| Pitt's row | **−217.5** |
| 20,000 random rows: mean / sd / best | −333.7 / 12.1 / −271.1 |
| z, count ≥ real | **9.6, 0 of 20,000** |

`periodscan.py` (annealing a free 24-letter row for periods 20–32) is **not** decisive and is recorded as such: at
106 letters an unconstrained annealer over-fits, and periods 27–32 reach higher scores than the true key. The
argument for period 24 is structural (the odd/even construction of the row, the 24-apart homophones, the clean
alphabetical supplementary blocks), not the n-gram score. The readings against the clear text ("A C · · knowledge",
"[835] D E R stand", "X ^ E T E R", "Y O U R E 6* R E D E N T I A L S" beside Simpson's "Our Re-credentials") are
the confirmation.

## 4. Reading

Codes in [brackets], graphic signs and clear words as read, proposed transcription corrections in {braces} (§6).
Spelling as the cipher gives it.

**Charles I to [the Duke of Courland's envoy], Oxford, 2 November 1643 (SP 84/157 f. 217):**

> Sir, Wee have received your ciuill {&?} welcom letter of the {6th} of 8ber [= October] 1643. But never heard of
> any [514] letter of Our good△ Cousin中 the Duke of Curland's, your Master□, saue those inuiting us+ to send to
> the Funerals of the Late [303] Dukes his Father & Unkle [376] deceased of happy memory; to [which] we made an
> answer, but know not whether the same arriued [289] safe. The Difficulty of passage {we} feare {hath} preiudiced
> us [look*]. Our Cousin your Master's affeccons & offers are soe reall & acceptable to us, specially in this
> coniuncture of our Affaires, as we acknowledge [our] [selves] there[by] highly obliged. We [pray] you therefore
> to present our princely thanks [177] on this behalf, to [assure] our said Cousin your Master, & to lett him
> understand that we shall most [854]e-comly receiue his [assistance] with in [755] [188] [musket]s, match &
> [639], in {what} [pro]por[tion] it shall please him to transmit the same to us, to the [port] of Weymouth,
> Dartmouth, Exeter, Falmouth or [228]. Not doubting but God will shortly enable Us to recompence soe free & soe
> [gener]ous a c[591] & es[126]. Doe assure your self also of our fauour particular, & doe take your addres by
> [213] to us in very good part, as also that you haue taken care to avoyde the dangerousnes of the passage hither.
> And soe wishing you a safe returne back to our good Cousin your Master, to whom w[e] herewith [send] your
> re-credentials, Wee commit you to the Protection of the Almighty. Given at our court at Oxford the second day of
> Nouember in the Nineteenth yeare of Our Reigne 1643.

**Nicholas to Boswell, 2 November 1643 (SP 84/157 f. 219):**

> Sir, [His Majesty] comands [me] to signify his pleasure to you, that you use all possible diligence & industry
> by your meanes of the [170] & otherwise [secret]ly to hinder the coming ouer of the [181]s from the [726], for it
> is here apprehended that they [will] doe more hurt then good, for that they [are] understood here not to affect
> Monarchy. His Majesty's two letters herewith sent with flying Seales are put into your character, because most
> safe & ready; you are to decifer & interpret them. Monsieur F I R X S S appeares not here. …

## 5. What the letters are

* **The King's letter is not to Boswell.** It is to the Duke of Courland's envoy: it acknowledges *his* letter of
  6 October, calls the Duke "your Master" three times, sends "your re-credentials" (Simpson's letter to the Duke of
  the same day calls itself "these Our Re-credentials" and says the envoy's credentials "were transmitted by him
  hither"), and wishes him a safe return to his master. The envoy was at The Hague: the 1645 memorial says the
  passage was unsafe and "the ministers of their Majesties at the Hague" dissuaded him from crossing and took his
  letters. Nicholas's covering letter tells Boswell that the King's two letters (this one and the re-credentials,
  which also carries a cipher line) are "put into your character", i.e. Boswell's cipher, and that Boswell is to
  "decifer & interpret them" for the envoy. Hence the catalogue's "Charles I to Boswell".*
* **"Monsieur F I R X S S appeares not here."** Simpson names Major Georg von Firks as the Duke's agent (in Paris,
  1646–47) and attributes the 1645 memorial to him. Read as Firks/Fircks the group needs 42 → 45 (C) and 40 → 60
  (K)*; as it stands it is an X-spelling. Either way this is a man expected at Oxford who has not come, which is the
  envoy's own account of himself.
* **The arms.** "his assistance with in [store of?] [armes?], muskets, match & [powder], in what proportion it shall
  please him to transmit the same to us, to the ports of Weymouth, Dartmouth, Exeter, Falmouth or [Bristol?]": the
  Duke's memorial says he was told their Majesties needed "munitions de guerre" rather than men, and his later
  shipments were muskets, powder, match and lead. Nicholas to Roe in December 1643: "Arms and powder are arrived at
  Dartmouth for his Majesty" (CSPD).
* **The funerals.** Duke Friedrich of Courland (d. 1642) and his brother Wilhelm (d. 1640, remains brought home),
  buried with ceremony in February 1643: "the Funerals of the Late Dukes his Father & Unkle deceased of happy memory".
* **Nicholas's instruction** — hinder "the coming ouer of the [181]s from the [726]", people who "are understood
  here not to affect Monarchy", by Boswell's "meanes of the [170]" — fits the States General's embassy of mediation
  (Joachimi, Boreel, Renswoude), resolved on in late 1643 and received at Oxford early in 1644, which the King did
  not want: 181 + S = Ambassadors, 726 = States, 170 = the channel Boswell was to work (Prince of Orange? Admiralty?)*.
  The alphabetical ordering (§2e) puts 726 before "secret" (746), which "States" is not, so this is a historical
  reading, not a cryptographic one.

## 6. Transcription slips the reading implies (all unverified*, each a single-figure confusion)

| as transcribed | reading | needs | note |
|---|---|---|---|
| `40 24 23 n 48 44 31` | signify | 44 → 34 (F) | 3/4 |
| `107 41 76 101 14 27 he 50` | hurt then good | 27 → 29 (T) | 7/9 |
| `made an 1 4 40 30 69 28 3` | an-swer | 69 → 96 or 72 (E) | 6/9 inversion or 9/2 |
| `26 102 92 97 45 86 85` | & welcom | 26 → "&"?, 92 → 96 (E) | |
| `800 145 106 82 94 98* 53` | to affect | 98 → 93 (C) | Tomokiyo's own asterisk |
| `134 be*` | the | "be" → "he" | asterisked |
| `passage in* 34 22 are hash*` | passage we feare hath | "in" → "we", "hash" → "hath" | both asterisked |
| `not 78 59 it. 380 he 149` | not whether | "it" → "et" | |
| `C O 中 U S m.y^w` | Cousin the | "m." → "in" | |
| `the 21 62 61 47 110 113 70 52` | the coming ouer | a clear "in" dropped after M | |
| `82 48 52 42 40 64` | Fircks? | 42 → 45, 40 → 60 | or an X-spelling |
| `P 0 S S I B L E` | possible | 0 = plain o? | |
| `Y O U R E 6* R E D E N T I A L S` | your re-credentials | 6* → 21/45/69/93 (C) | asterisked |
| `Lave*` | Late | Tomokiyo's own suggestion | |

## 7. What remains, and what would settle it

Open: 514, 177, 213, 289, 303, 376 (or null), 170, 181, 726, 755, 188, 639, 228, the second 591, the 854
conflict, and the exact spelling of "Firxss". None of these is recoverable from two letters; each is a single
occurrence.

1. **Order the two folios.** SP 84/157 ff. 217 and 219 (items 96 and 97), TNA digital copying. The same volume
   should hold Boswell's letters of 8, 22 and 29 October 1643 that Nicholas acknowledges, and possibly the envoy's
   letter of 6 October and a decipher. That is Daniel's step (payment/account).
2. **Boswell's key.** Boswell's papers are BL Add MSS 6394–6395 (and Nicholas's in the Nicholas Papers, Egerton
   2533 ff.); a copy of "Sir W. Boswell's cipher" with Nicholas would close every word code at once.
3. **The Courland side.** Riga, Latvian State Historical Archives, fonds 554 (Duke's archive); Seraphim's Mitau
   copies are the source of Simpson's prints. The envoy's letter of 6 October 1643 and the Duke's letters of
   invitation to the funerals may survive there.
4. **Credit.** Pitt's repository should be cited as the solution of the alphabet; the findings here (§2d, §5) are
   to be offered to him and to Tomokiyo. That is an e-mail, Daniel's to send.

## 8. Files

`key.py` (alphabet, supplementary letters, nulls, word codes, signs; `decode()`), `lm4.py` (4-gram model; the
`.pkl` is regenerated), `permtest.py` and `permtest` output in §3, `periodscan.py` → `periodscan_out.txt`,
`charles.txt` / `nicholas.txt` (Tomokiyo's text), `decoded.txt` (mechanical output of `key.py`), `src/` (blog text,
Simpson and CSPD OCR; the two large OCR files are ignored by git and re-downloadable from the Internet Archive).

---
Checked: Pitt's inputs against the blog text (identical); the alphabet against a 20,000-row permutation control;
every reading above against the tokens; Simpson's re-credentials letter and memorial from the IA OCR; TNA references
from the Discovery API; CSPD Dartmouth line from the IA OCR. Not checked: the manuscripts (no images exist online);
the Latvian archive descriptions Pitt cites; Pitt's unit tests were not run. User must verify: the identity of the
envoy as Firks, the alphabetical-order hypothesis, and every entry in §6 before any of it is published or sent.
