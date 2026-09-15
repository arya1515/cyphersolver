# Ormonde–Maltravers Cipher (1634–1635) — NOTES

**Verdict: PARTIAL (alphabet recovered, all spelled words read; nomenclator codes only inferred from context).**

Target: S. Tomokiyo, *Unsolved Historical Ciphers* → "Ormonde-Maltravers Cipher (1634-1635)"
(https://cryptiana.web.fc2.com/code/unsolved.htm).

## 1. Sources

| Source | What it gives | Where |
|---|---|---|
| HMC, *Calendar of the manuscripts of the Marquess of Ormonde, K.P., preserved at Kilkenny Castle*, vol. I (1895), pp. 28–29 | The two letters (Maltravers → Ormond, 13 Sept 1634 Dorking; 22 Jan 1634/5 Whitehall), cipher figures printed in the text | IA `calmarqormonde01greauoft`; OCR in [ormonde1_djvu.txt](ormonde1_djvu.txt) lines 2101–2156; page scans [p28.jpg](p28.jpg), [p29.jpg](p29.jpg) (IA `page/n43`, `page/n44`) |
| Same volume, index "Cypher, letters in. 28, 75, 118, 209, 214" | Other cipher letters in the volume: p.75 Sir Edward Nicholas → Ormond 18 Apr 1644 (with interlinear decipher, a *different* key, figures 4–211); pp.209–214 letters of the 1650s (another key, figures up to 523). **Nothing else from 1634–36, no key, no decipherment of the Maltravers letters.** | [cipher_runs.txt](cipher_runs.txt) (output of [find_cipher_runs.py](find_cipher_runs.py)) |
| HMC Ormonde New Series vols. 1–3 (1902–04; bundled in the same IA djvu file) | No Maltravers letters, no 1630s cipher | grep of the same file |
| Tomokiyo, "Ciphers in Early Stuart England before the Civil War" (strafford.htm) | Wentworth–Charles I, Wentworth–Laud (nulls < 30, codes 85–202), Wentworth–Windebank ciphers (images only); Scudamore 1636 and Cave 1638 ciphers "assign three (or six) figures to each letter in regular arrangement"; Ormonde–Clanricarde 1643 also regular. None is the Maltravers key (different null/code ranges), but they show the *type*: regular alphabet blocks + nulls + numbered nomenclator. | fetched 2026-09-15 |
| Wedgwood, *Thomas Wentworth* (1961) p.159; Wikipedia "James Butler, 1st Duke of Ormond" | "In January 1635 Ormonde was sworn of the Council" — confirms the reading of letter 2 | — |

The printed figures were checked against the page scans: **every figure below is exactly as printed** (in particular
"26" in the first run is printed, not an OCR slip).

## 2. Ciphertext (as printed; full letters in [ciphertext.txt](ciphertext.txt))

Letter 1, 13 Sept 1634:
> My lord of Kildare is long ago in England though I have not seen him, it is said he came over because he was
> **65, 35, 21, 26, 59, 98, 113, 186, 108, 143,** refused to see him because he brought no
> **28, 69, 49, 50, 70, 44, 89,** from **186, 99.**

Letter 2, 22 Jan 1634/5:
> You desire to know what **93, 185, 95,** hath written unto **99, 149,** concerning **98, 10, 44, 79, 47, 8, 59,** for whom
> **270** thus hereafter of which I can give you no account of at all, only by what I hear it is like to go worser with
> him, rather than better, **95, 186, 98** hath written unto **98, 218, 97** much in praise of **100, 174, 103** in general,
> and particularly for his good carriage in **111, 95, 221,** and upon his motion **93, 31, 174 99** is to be
> **64, 99, 11, 79, 85, 35, 12, 69, 28, 29, 79, 44,** in which courses **174** shall do well to continue.

59 figures, 39 distinct, max 270. Repeated: 98 ×4, 99 ×4, 44/79/95/186 ×3, 28/35/59/69/93/174 ×2.

## 3. Structure (from [analyze.py](analyze.py), output in [analyze_out.txt](analyze_out.txt))

* **91–111 are nulls.** Nine distinct values (93 95 97 98 99 100 103 108 111), each used 1–4 times, and 17 of 18
  occurrences sit at the edge of a cipher run or immediately beside a ≥112 code (`93 185 95`, `99 149`, `95 186 98`,
  `98 218 97`, `100 174 103`, `111 95 221`, `186 99`). Tomokiyo's guess is confirmed.
* **≥112 are nomenclator codes** (113 143 149 174 185 186 218 221 270): each stands alone between nulls or clear
  text, and 270 is explicitly *introduced* ("for whom 270 thus hereafter").
* **< 91 are letters**, and the letters are the key to the whole thing: the four spelled runs contain doubled letters
  written with *consecutive* figures — `49 50`, `69 70`, `28 29`, `11 12` — i.e. each letter owns a block of
  consecutive figures. Cribs:

  | figures | reading | context |
  |---|---|---|
  | 28 69 49 50 70 44 (89) | l e t t e r (s) | "brought no letters from [the Lord Deputy]" |
  | 11 79 85 35 12 69 28 29 79 44 | c o u n c e l l o r | "upon his motion [Ormonde] is to be a councellor" (Ormonde sworn PC Jan 1635) |
  | 10 44 79 47 8 59 | C r o s b y | Sir Piers Crosby, who fell out with Wentworth in the 1634 Parliament and was put out of the Irish Council early in 1635 ("like to go worser with him") |
  | 64 | a | "is to be **a** [null] councellor" |
  | 65 35 21 26 59 | a n g [k] y | "he was angry [with] the Lord Deputy" — see §5 |

  All of these are consistent with **one regular key**: the 19 consonants of the 24-letter alphabet
  (b c d f g h k l m n p q r s t w x y z; i=j, u=v) in alphabetical order, **three figures each, starting at 7**,
  followed by the vowels from 64:

  ```
  b 7-9   c 10-12  d 13-15  f 16-18  g 19-21  h 22-24  k 25-27  l 28-30  m 31-33  n 34-36
  p 37-39 q 40-42  r 43-45  s 46-48  t 49-51  w 52-54  x 55-57  y 58-60  z 61-63
  a 64-..  e ..69,70..  i ..  o 79-..  u 85-..      (vowel block sizes not fixable: 5 each = 64-88, or a=3/others 6 = 64-90)
  91-111 nulls        112+ nomenclator (names/words)      1-6 unknown (nulls or "&"/"the"?)
  ```
  Every letter-figure in the text falls where this grid predicts (b8 c10-12 g21 l28-29 m31 n35 r44 s47 t49-50 y59
  a64-65 e69-70 o79 u85); the only misfit is 26 (see §5). An exhaustive scan of regular grids (start 1–11, block
  2–4, uniform vowel blocks 2–6; 42 grids) ranks start=7/size=3 first by English quadgram score.
* Tomokiyo's "44 79" / "79 44" are simply **r-o** (C**ro**sby) and **o-r** (councell**or**).

## 4. Reading

Letter 1 (13 Sept 1634):
> ...it is said he [Kildare] came over because he was **ANGRY** [null] **113**=*with?* **186**=*the Lord Deputy* [null]
> **143**=*the King?* refused to see him because he brought no **LETTER[S]** from **186**=*the Lord Deputy* [null].

Letter 2 (22 Jan 1634/5):
> You desire to know what [null] **185** [null] hath written unto [null] **149**, concerning [null] **CROSBY**, for whom
> **270** thus hereafter, of which I can give you no account... it is like to go worser with him rather than better.
> [null] **186**=*the Lord Deputy* [null] hath written unto [null] **218** [null] much in praise of [null] **174**=*Ormonde*
> [null] in general, and particularly for his good carriage in [null][null] **221**=*Parliament*, and upon his motion
> [null] **31**=m(?) **174**=*Ormonde* [null] is to be **A** [null] **COUNCELLOR**, in which courses **174**=*Ormonde* shall
> do well to continue.

Nomenclator values (contextual, unverified): 186 = Lord Deputy (Wentworth) — near certain (three consistent uses);
174 = Ormonde/"your lordship" — near certain; 221 = Parliament (the 1634 Irish Parliament, in which Ormonde backed
Wentworth) — very likely; 270 = new code assigned to Crosby; 143 = the King (or another great person who refused
Kildare) — likely; 113 = a preposition ("with"/"against") — guess; 185, 149, 218 = persons (185 probably also
Wentworth or the King; 218 the King/Secretary Coke/Arundel) — unknown. 31 (= m in the grid) before 174 is
unexplained (perhaps "m[y lord]" begun and abandoned, or an error).

## 5. Residual problems (honest list)

1. **26 in "angry".** The grid gives 26 = k, so the printed run reads a-n-g-k-y; r is 43–45. Since "angry" is the
   only sensible word, either Maltravers mis-enciphered or the HMC transcriber misread the MS (44/45 → 26). The
   figure is printed as 26 (scan checked), so this cannot be resolved without the manuscript.
2. **89 at the end of "letter".** Either u (if vowels are a=64-66, e=67-72, i=73-78, o=79-84, u=85-90 — then a slip
   for s) or a null/plural sign (if vowels are 5 each, 64–88, and 89–111 are nulls). Sense is unaffected.
3. Exact vowel block sizes, the meaning of 1–6, and the nomenclator entries cannot be fixed from 59 figures.
4. The historical claim "the King refused to see Kildare because he brought no letters from the Lord Deputy" fits
   Kildare's 1634 quarrel with Wentworth (he crossed to England that summer) but I did not find an explicit
   confirmation online (Knowler's *Strafforde's Letters* vol. I would be the place to check).

## 6. What was tried

* Downloaded OCR of HMC Ormonde vol. I; extracted both letters; regex scan of the whole bundled file for figure runs
  ([find_cipher_runs.py](find_cipher_runs.py)) — no other 1630s cipher, no key, no interlinear decipher.
* archive.org advancedsearch for all "manuscripts of the Marquess of Ormonde" volumes (17 items; old series I–II,
  new series I–VIII) — the 1634–35 letters appear only in old-series vol. I.
* Compared with the Wentworth-circle ciphers described on cryptiana (Wentworth–Laud: nulls < 30, codes 85–202;
  Scudamore/Cave/Ormonde–Clanricarde regular-block alphabets): same *design family*, different key.
* [analyze.py](analyze.py): frequencies, range distribution, null-position test, bigrams, crib-derived regular grid,
  exhaustive regular-grid scan with quadgram scoring, and an unconstrained homophonic hill-climb (simulated annealing,
  quadgram score, 40 restarts) on the 28 letter-figures. **The hill-climb yields nothing** ("thath erethet hereth
  erthereare", q=-76 vs. -137 for the true key) — with 28 symbols and 28 letters it just fits common quadgrams; the
  solution comes from the consecutive-doubled-letter structure plus historical cribs, not from statistics.

## 7. Where the rest is

* The originals (Kilkenny Castle Ormonde papers) are now in the **National Library of Ireland, Ormonde Papers**
  (MSS 2300 ff.); a key sheet, if it survives, would be there or among Maltravers/Arundel papers (Arundel Castle).
  Not online.
* Bodleian **Carte MSS** (vol. 1, 1630s letters to Ormonde) may hold copies; the early Carte volumes are not
  calendared online.

## 8. Files

`ciphertext.txt`, `analyze.py`, `analyze_out.txt`, `find_cipher_runs.py`, `cipher_runs.txt`, `ormonde1_djvu.txt`
(OCR, 4.4 MB), `p28.jpg`, `p29.jpg`, `NOTES.md`.
