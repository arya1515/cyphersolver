# Sauli and Riario (Portugal) to the Secretariat, 1579–81 — READ (contemporary decipherments, checked with Lasry's key)

Catalogue item 260 (class A). ASV, Segreteria di Stato, Portogallo 8 (DECODE R190–R194; index i. 1025, doss. 8).
The volume holds Antonio Sauli's letters as nuncio (23 Jan – 9 Dec 1579, ff. 2–74) and Cardinal Alessandro Riario's
as legate a latere to Philip II (6 Mar 1580 – 23 Jul 1581, ff. 107–323). The catalogue date "23 Jan 1579" is the
volume's first date, not a letter's.

**Result (21 Sept 2026): read.** The ciphers were deciphered on arrival: nearly every cipher passage carries the
secretariat's decipherment written interlinearly. The work was a transcription job. Each passage's digits were
decrypted with George Lasry's reconstructed key (DECODE, Oct 2020) and compared with the contemporary gloss. They
agree everywhere the digits were legible, and the comparison adds five code words to Lasry's key.
Found solved: in part, by Lasry (key and a decryption of R190–R191). R192–R194 had no posted decryption.

## Records

| DECODE | ASV folios | pp. | What | Date |
|---|---|---|---|---|
| R190 | 92r–95r | 5 | letter incl. passage "Al conte di Desmon[d]", soldiers of S.S.tà in Ireland | undated here; ff. 92–101 lie between the Sauli (2–74) and Riario (107–323) runs |
| R191 | 98r–101r | 6 | Ortiz, the "distruttione di quelli poveri Italiani" (Smerwick, Nov 1580?), Anselmo, soldiers' pay | author and date not established |
| R192 | 195–197 (old 200–202, 118–123) | 6 | Riario, audience with Idiáquez "li 4"; pp. 5–6 a "Copia" dated 29 Nov 1580 | Nov–Dec 1580 |
| R193 | 236–238 | 3 | Riario to Card. di Como (Gallio), Badajoz 2 [Oct?] 1580; p. 3 a clear decifrato, Elvas 1?0 Dec 1580, signed A. Card.le Riario | Oct–Dec 1580 |
| R194 | 281 (st. 296) | 2 | Riario (hand, subject); undated, unsigned: Irish captains, money, Flanders first, the truce | 1580–81 |

R190/R191 decryption: Lasry's DECODE file DOC_R190_D3249 (same file on all five records) covers only ff. 92–101,
from Midas's 2017 transcription (474 of 2392 groups marked ?; the ? are transcription slips, not key gaps).

## Key

Lasry's reconstruction (DOC_R190_D3258): fixed two-digit homophones, 9 = null used as word separator, so parsing is
deterministic (no group begins with 9). a 00 81, b 71, c 61, d 51, e 07 83, f 73, g 63, h 53, i 05 85, l 25 75,
m 65, n 55, o 03 87, p 77, q 67, r 57, s 47, t 37, u/v 01 27, z 17; che 78, per 84, quell 24, quest 14,
ancora 44, dura 68, M.ta 28, 82 "Hune". Numbers are written in plain numerals between 9s ("4 mesi", "1300").

Added here from the glosses (R192–R194):
- 16 = Inghilterra (6×, firm)
- 30 = S.S.tà (3×, firm)
- 36 = Francia (1×)
- 40 = cattolici (2×; once glossed "guerra", then struck out)
- 10 = Italia (3×); glossed "V.S. Ill.ma" once (R192 p.6, may be 18) — doubtful
- 20/28: S.M.tà in some places, "Italiani" in others; in this hand 20 and 28 are hard to separate. Probably two
  codes, 28 M.tà (Lasry) and 20 Italiani, not settled.
- 72: "denari" (R192 p.6, R194 p.1); R192 p.4 "la 72 82" glossed "la Reg.a d'Inghilt.a navi" — 72/82 not settled.
- Unresolved: 4-digit prefixes 6371/7771/7361/7761 + 9 before several phrases in R193–R194 (null flourish or code);
  "religione cattolica" in R194 p.2 enciphered short (unread code group); tail "0?9 32 0 9 75 71 63" after
  "dubbio che ha S.S.tà" on R192 p.1 (unglossed, not decrypted).

## Content (from glosses and clear text)

- Riario reports the Pope's warning about a plot "sopra il negotio di Piamonte": the Marquis of Ayamonte (former
  governor of Milan), the Anselmi, Huguenots of the Dauphiné to help them in Italy. Philip II thanks the Pope and
  promises nothing will disturb Italy (R192).
- The Italian troops (the papal contingent for Ireland/England): to be sent with munitions and 4 months' pay under
  S.S.tà's name; the Queen of England's ships make it a clear danger; the "impresa d'Inghilterra" must wait until
  Flanders is subdued; the Italians embarked on the Lisbon river, to be sent back toward Italy (R192–R194).
- Aid to the Catholics of Ireland, the Irish captains, the Earl of Desmond (R190, R194); the President "è pietra
  scandali et mal sodisfatto della Corte romana" (R193 p.3).

## Files

- `decrypt.py` — Lasry's key as a decoder.
- `transcription_R192.md`, `transcription_R193_R194.md` — per-passage digits, decrypt, gloss, agreement.
- `decode/DOC_*.txt` — DECODE transcriptions and Lasry's key. Images in `img/` are git-ignored (ASV).

Prior art: no edition of Riario's legation letters found (web search 21 Sept 2026); Lasry's key and partial
decryption on DECODE (2020) are the prior solution.
