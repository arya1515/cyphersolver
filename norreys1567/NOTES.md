# Sir Henry Norreys to Cecil, 1567-68 — BL Add MS 4136 ff. 160-161 (DECODE R9251, part of R9250)

Status: in progress

## What the record is

DECODE R9251 ("Sr. Henry Norreys", 9 Mar 1567, 3 pp.) is three pages of Patrick Forbes's 1730s deciphering
file (Add MS 4136; see [smith1562](../smith1562/NOTES.md)). Only the top of p.1 (f.161) is Norreys's. The rest
is Throckmorton 27 Aug 1562, Middlemore 8 Apr 1563 and Smith 7 Mar 1562/3, all in other ciphers.

- The date is Old Style: "9 Mar. 1567/8" = **9 March 1568**.
- The Norreys series starts on f.160 (DECODE R9250 p.2 = smith1562/decode/IMG_R9250_I43261_P2.jpg):
  4 June 1567, 6 July 1567, 10 July 1567, 6 Feb 1567/8 (groups 1-11 on f.160, 12-23 on f.161),
  then 9 Feb, 24 Feb and 9 Mar 1567/8 on f.161.
- Forbes copied only the ciphered words, numbered. The target letter has three: (1) one name sign,
  (2) a five-sign word, (3) one name sign.
- Transcription with ad hoc token names: `transcription.txt`.

## The key

No key for Norreys is on DECODE. The volume's key records are Throckmorton's first and second ciphers (R9260),
Smith and Croft (R9261), Throckmorton's third (R9262) and Percy's key (R9257). None of their alphabets matches
Norreys's signs. The key leaves are ff.177-190; no Norreys cipher is among those imaged.

## Cribs (CSP Foreign viii, British History Online; saved in csp/)

| letter | CSP no. | ciphered content (from the calendar summary) |
|---|---|---|
| 4 June 1567 | 1265 | "the King of Spain, the Emperor, with the Duke of Savoy intend to overthrow the Protestants of France, Flanders, and England" |
| 6 July 1567 | 1405 | "Stewart's name in cipher" |
| 10 July 1567 | 1427 | "partly in cipher": the Earl of Murray stayed |
| 6 Feb 1568 | 1987 | Lesley, Earl of Rothes, Scotland, Calais, Gascony, Navarre … |
| 9 Feb 1568 | 1998 | Calais, the Protestants, the Prince of Condé, the Admiral, Marseilles, Strozzi … |
| 24 Feb 1568 | 2025 | Guise/Condé marriage, the Protestants, the Prince, the Admiral, money for the Almains |
| **9 Mar 1568** | **2054** | peace, Montmorency, the Pope/Emperor/King Catholic/Swiss, reiters, Bourbon, Longueville, Scotland, the Queen, Marseilles |

## Findings so far

- **Name signs recur across letters in the calendar's order.** #Xr, #Ec and #fk stand in the same sequence in
  9 Feb (6, 8, 9) and in 24 Feb (2, 3, 4). Both calendar entries run "the Protestants … the Prince [of Condé] …
  the Admiral". Provisional: Xr = Protestants, Ec = Prince of Condé, fk = Admiral.
- The letter signs are **homophonic**. "Lesley" = 6 Feb (1) `xi dash flat 3b oo 9` fits (l e s l e y, with
  the two l's on different signs). "Scotland" = 6 Feb (4) `4 T 4: 9 3b s: sqc 3u` fits (3b = l again).
- The June 1567 tail `… dash-a E Gam flat m pi oo T 3r dash-a` has the length of "and England", after two
  name signs (France, Flanders).
- The June "the Protestants" alignment (s: = e, 2 = t, cup = o, 7d = r, cap = s, lam = a) clashes with the
  6 Feb "Scotland" alignment (s: = a). One of the two is wrong. The copies are also sloppy
  (sqc / ⊏ and dash-a / ⊣ may each cover two signs).
- A crib-assignment search over the calendar vocabulary (work/csolve.py) finds no clear answer: the groups are
  too short and too varied, so many words fit.

## Target reading

Not read. (2) `+ rc o l inf` is five signs. Candidates from no. 2054: "Swiss", "Queen", "peace". The two name
signs are most likely among Montmorency / the Pope / the Emperor / the King Catholic / the Queen [of Scots].
There is no evidence yet to choose between them.

## What would move it

- The originals, TNA SP 70/96-97 (Norris to Cecil, Feb-Mar 1568). The Secretary's office usually wrote the
  decipherment between the lines. That gives the crib directly (State Papers Online, paywalled).
- A tokenised re-transcription of the 1567 passages at full resolution, then a homophonic solve on the longer
  4 June group (4) (about 50 signs) against the "that whereof he advertised him …" sentence.
