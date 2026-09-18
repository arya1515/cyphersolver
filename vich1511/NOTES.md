# Ferdinand the Catholic → Jerónimo de Vich (Rome), AHN Estado 8714/8715

PARES search "Vich cifrada" lists the ciphered letters in the Vich family archive (AHN, Archivos privados):

| Signature | Date | PARES id | State |
|---|---|---|---|
| 8714 N.12 | 1508-09-30 | 12751356 | cipher + contemporary decipherment |
| 8714 N.26 | 1509-07-28 | 12751370 | cipher + decipherment |
| 8714 N.39 | 1510-05-13 | 12751383 | cipher + decipherment |
| 8715 N.41 | 1510-05-22 | 12751386 | cipher + decipherment |
| **8715 N.45** | **1511-04-04** | 12751390 | cipher only — **read here** (Seville) |
| 8715 N.46 | 1511-07-05 | 12751391 | cipher + decipherment (key source) |
| 8715 N.52BIS | 1512-03-01 | 12760824 | cipher + decipherment (key source) |
| **8715 N.57** | **1512-06-05** | 12751402 | cipher only — **read here** (Burgos) |
| **8715 N.60** | **1512-09-01** | 12751405 | cipher only — **read here** (Logroño) |
| 8715 N.73 | 1515-10-26 | 12751418 | cipher only — **different key, not read** (Pedrezuela) |
| 8715 N.74 | 1519-01-30 | 12751419 | Charles I, cipher + decipherment, another system |
| 8715 N.79 | "1500" | 12751424 | "Clave de cifra": a plain letter→sign table, not the key to any of these |

**Caveat on prior work.** The Barón de Terrateig, *Política en Italia del Rey Católico 1507–1516.
Correspondencia inédita con el embajador Vich* (CSIC, Madrid 1963, 2 vols.) edits this correspondence.
I could not consult it (the one online review returns HTTP 403), so whether he printed texts for
N.45/N.57/N.60 is unverified. PARES itself records no decipherment for them, and no text of them was
found online.

## The 1511–12 cipher

One key serves N.41, N.45, N.46, N.52BIS, N.57 and N.60. It is a nomenclator:

- **A homophonic alphabet** of figures and marked letters — `40` r, `4h`/`3` e, `ah`/`T` o,
  `to`/`7`/`b` a, `ch` c, `oo` d, `11`/`W` n, `X`/`g`/`9` t, `d`/`eh` s, `q` m, `o` g, `O` h,
  `mt`/`SS`/`P` p, `tt` r. Words not in the code are spelled out with these.
- **Code groups**, three letters, for words *and* for syllables: `pef` que, `diz` de, `dih` con,
  `fak` el, `hor` la, `has` lo, `raf` por, `rif` porque, `mix`/`mye` papa, `fef` emperador,
  `sap` venecianos, `fio` ferrara, `fuq` francia, `dur`/`dox` duque, `hib` guerra — and syllabic
  ones like `pob` si (in *si-t-io*), `flart` me (in *pri-me-ras*), `mik` no (in *me-no-r*).
- Full list: `key.md`; machine-readable in `decode.py`; ~130 groups recovered.

**How it was recovered.** N.46 and N.52BIS carry the clerk's decipherment on the following leaves.
Lining the two up word by word gives the alphabet and the common groups; the readings of N.45, N.57
and N.60 then supplied the rest. Two traps: `fug` (señor) and `fuq` (Francia) are near-identical, as
are `plart` (mi) and `plort` (al); and the barred q is m in most places but a in a few, so there are
probably two similar signs that this transcription merges.

## What the three letters say

**N.45 — Seville, 4 April 1511** (378 lines, ~5% still unread; `n45_pp*`). A long complaint against
Julius II and a set of instructions. Ferdinand is angry at the publication of the new cardinals, at the
Pope absolving the Venetians and treating with them "sin dezirme ni comunicarme", at the priory of San
Juan, and at the Pope's refusal to follow his counsel, from which followed *la rota* of the papal army.
Then the business: press the **Emperor–Venice concord** (with draft terms — Padua and Treviso to stay
with Venice in fief against tribute; Verona, Vicenza, Riva, Rovereto, Peschiera to the Emperor), settle
**Ferrara**, keep the Pope's army in a safe place, and deliver orders to **Fabrizio Colonna** under an
enclosed letter of credence. He warns that France is offering him a separate perpetual alliance without
the Emperor and that he will not take it, and that a rupture would wreck his crusade against the Moors.

**N.57 — Burgos, 5 June 1512** (35 lines, ~7% unread; `n57_*`). The aftermath of **Ravenna**
(11 April 1512). Ferdinand reconstructs how his army was pushed into battle: Vich's own letters, and
the papal side, pressed the viceroy Ramón de Cardona, saying that **if they did not fight, the Pope
would not meet the pay and would come to terms with France** — against Ferdinand's repeated written
orders not to risk a battle. "Las cosas de guerra es muy peligroso [para] los que están ausentes
dellas; siempre se ha de remitir a los que las tienen presentes." Do not do it again, he says, or it
would be *echar la soga tras el caldero*. Then: get the Pope and the Venetians to pay their share, push
the Emperor's business to a conclusion, and **treat the Ferrara business secretly, "sin que la sienta
el Papa"**, reporting back so he can give orders.

**N.60 — Logroño, 1 September 1512** (432 lines, ~14% unread; `n60_pp*`). Written from the Navarre
campaign, and the sharpest of the three. It opens on **the bulls for Navarre** that Vich had sent, and on
the Pope acting "en quebrantamiento de lo que tiene asentado" with him. Then:

- **The Emperor–Venice peace**, again, and urgently: give way over Vicenza if Venice raises the tribute;
  "que se abrevie la conclusión"; if it drags, the Emperor will despair of the League and tie himself to
  France for good, since everything the Emperor has done "ha sido por las promesas que yo le he hecho".
- **Spiritual war on Louis XII.** Ferdinand wants the Pope to use "las armas espirituales": to deprive
  the king of his crown, of **Guyenne and Normandy** — assigning them to England — as a "príncipe fautor
  y receptador de cismáticos y heréticos", to absolve his provinces and subjects from obedience, and to
  grant crusade bulls against him; citing precedents against the Emperor Frederick and King Pedro. He
  asks for the bull of Guyenne and Normandy to be sent to him.
- **Money and Milan.** Pensions to hold an Italian power steady: twenty thousand ducats a year from the
  Pope and Venice, twenty thousand more from another party, as much again from Ferdinand — fifty
  thousand in all, "y no se olvide de aqueste artículo, que es muy sustancial".
- **Ferrara after Milan.** If the Pope insists on starting with Ferrara, Vich is to insist on finishing
  the French in the state of Milan first, "que esto es lo que cumple a su bien y a Italia"; and on a
  mutual-defence arrangement so that each member of the League is secured in its Italian state.

**Checks.** The key was built from N.46 and N.52BIS alone and then read three letters it was not built
from. Each letter's place and date come out of the clear-text subscription and match the catalogue
(Seville, Burgos, Logroño). The contents fit their dates independently: the March 1511 cardinal
promotion, Ravenna, the Navarre bulls. In N.57 the proverb *echar la soga tras el caldero* is spelled
out letter by letter, not taken from code groups.

## N.73 (1515) — not read

`n73_transcription.txt` (124 lines, 3,177 tokens, 197 distinct) and `n73_freq.txt`. It is a different
system: mostly three-letter code groups (`sin` 151, `sud` 97, `no` 93, `zre` 89, `xed` 68) with a
smaller set of signs (`X` 171, `TH` 170, `PHI` 163, `RH` 151). No deciphered sibling exists for it:
the nearest, N.74 of 1519, is Charles I's and is a third system (its `sex` = papa, `mod` = tiene,
`sin` = de). Attacks tried and failed (`solve73.py`, `solve73g.py`): annealing against the repo's
Spanish 5-gram model with the lowercase groups split into letters, as whole units, and as context
breaks around symbol runs. All gave ~-2.7 to -3.5 per character with seeds disagreeing — no solution.
Symbol runs are short (median 3), so there is little for an n-gram model to hold onto; this one needs a
crib or a sibling. Its clear text: docket "a 26 de octubre 1515", opening "videlicet iterum", ending
"en Pedrezuela a xxvj de otubre de dxv".

## Files

- `pares.py` search/image client; `lines.py`, `half.py` page-to-strip cutters.
- `n45_pp03-09.txt`, `n45_pp10-15.txt`, `n57_transcription.txt`, `n60_pp03-09.txt`,
  `n60_pp10-15.txt` — transcriptions in ASCII glyph labels (legend at the head of each).
- `*_decoded.txt`, `n57_decode_v3.txt` — decodes; unread groups print in [brackets].
- `decode.py` the key, `key.md` the human-readable key.
- Images are not committed; re-fetch with `python pares.py img <pares-id> <prefix>`.

## Open

- ~5–15% of groups per letter still unread; the untouched decipherments (N.41 and the three in 8714)
  would close most of them.
- The q = m/a sign split, and `plart`/`plort`, want a careful re-reading against the images.
- N.73 (1515) needs a different approach.
- Whether Terrateig 1963 already printed any of this.
