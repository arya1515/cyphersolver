# No. 43: the unglossed opening, read (BnF fr. 3854 no. 43, f. 117r ll. 0–11)

No. 43 is Conti's mémoire *pour Monsieur de Legue*: Geoffroy, marquis de Laigue, Conti's envoy to Archduke
Leopold Wilhelm. It runs to seven pages, ff. 117r–120r (Gallica canvases 245–251).

- It is written in a numerical code of letters and syllables, with clear words mixed in.
- A contemporary hand deciphered it between the lines from f. 117r l. 12 onward.
- **The first twelve lines, 264 groups, were never deciphered.** They are the address and the purpose of the
  mémoire. This file reads them.

## How the code works (rebuilt here)

The key was rebuilt from the glossed groups that agents transcribed from ff. 118r, 118v
and 117v (`n43/pairs_c246.txt`, `pairs_c247.txt`, `pairs_c248.txt`: 1,485 glossed groups). `n43/buildkey.py` tallies them into
`n43/key43.txt`.

- **Single letters: four interleaved alphabets.**

  | Numbers | Direction | Examples |
  |---|---|---|
  | 3–25 | a→z | a 3, b 4, … l 13, … z 25 |
  | 28–50 | z→a | o 37, n 38, i 42, e 46, a 50 |
  | 51–73 | a→z | e 55, i 59, s 68, u 70, x 71 |
  | about 80–98 | z→a | t 80, s 81, n 86, i 90, c 96 |

- **Syllables: consonant blocks of five, in vowel order a e i o u.** For example b 251–255, c 256–260,
  d 261–265, f 291–295, g 296–300, h 301–305, l 336–340, m 341–345, n 346–350, p 375–379, q 380–384,
  r 385–389, s 410–414, t 415–419, v 420–424.
  - A second, homophonic series fills the gaps: do 277, de 279, je 314, gu 321, ne 354, me 358, la 364, ru 390,
    pu 400, se 439, ti 442, te 443, su 445.
- **An underlined number reverses its syllable.** 385 = ra, 385̲ = ar; 416 = te, 416̲ = et; 347̲ = en.
- **Nulls:** numbers roughly 99–250, never glossed anywhere (99, 119, 129, 150, 199, 200, 206, 207, 210, 219,
  222, 225, 229, 230, 237, 240, 250).
- **Code words:** 457 = cardinal, 458 = parlement, 472 = l'archiduc.

## Where the 264 values come from (`n43/decode_opening.py`)

- **220 groups:** the majority gloss the same number carries on the glossed pages.
- **24 groups:** fixed by the alphabet structure (37, 38, 46, 59, 80, 81, 86) or are nulls.
- **20 groups:** second-series syllables fixed by context in the opening itself.
  - They agree with one another and with the block layout: do 277 and de 279 share a block, as do me 358 and
    la 364.
  - These are the least certain values. None changes the sense of a sentence.

## Text

Clear words in the manuscript are in roman; the deciphered text is in *italics*.

> *Pour Monsieur de Legue. Parce que nous ne doutons que le cardinal ne donne une mauvaise interprétation à toutes
> ses actions, et* qu'il *ne face* principalement *ses effors pour mettre l'archiduc dans la défiance de nos*
> bonnes intentions *sur le sujet de la conférence que [le] parlement a accordée,* j'ay jugé à propos de vous en
> *faire instruire, afin* que vous puissiés *destourner les mauvais effets des artifices du cardinal, et faire
> comprendre à l'archiduc que ce pourparler n'a esté causé et résolu que* par les *retardemens que l'archiduc
> apporte à nous secourir, et que* nous sommes tousiours dans *nos mesmes desseins, sans que rien puisse altérer
> les paroles que nous a[vons données] …*

The glossed text continues from here, on the same subject. f. 118r: Saint-Germain lets a hundred muids of corn
a day come in from Corbeil during the conference. The deputies of the parlement and the sovereign courts are
"tous gens de bien dans le zèle de la paix générale et dans une haine irréconciliable pour le ministériat du
cardinal". f. 118v: the Mazarin article, and the Archduke "aura tout sujet de se louer … pour le rétablissement
de la paix des deux couronnes".

## Notes

- **Why the opening was left undeciphered.** The second-series syllables (277, 279, 314, 321, 354, 358, 364, 390,
  400, 439–445) and the alphabet values 37, 80, 81 and 86 never occur in the glossed text of ff. 117v–118v
  (1,485 glossed groups): no pair confirms them and none contradicts them. The opening leans on a part of the key
  the body hardly uses, which may be why the contemporary decipherer did not gloss it.
  - Checks against the complete f. 117v pairs: 46 = e, 59 = i and 38 = n agree with the alphabet layout.

- The mémoire is undated. The opening says the conference (Rueil, from 4 March 1649) has already been granted
  and that the Archduke's slowness in sending help provoked it. That places it in early or mid March 1649,
  before nos. 41–42 (26–27 March).
- Slips in the original:
  - *effors* is enciphered with an extra `s` (effor-s-s).
  - *mauvais effets* lacks the *fe* (ef-[229 null]-t-s).
- My transcription of the opening is in `n43/opening_c245.txt`, the decoded text in `n43/opening_decoded.txt`.
