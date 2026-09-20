# BnF fr. 3181 f. 55 — Catherine de Médicis to the bishop of Rennes, 31 July 1563

## Status of the passage

La Ferrière printed this letter (*Lettres de Catherine de Médicis*, II, pp. 79–81,
from "Orig. Bibl. nat. fonds français, n° 3181, f° 55 r° et v°"). He set the whole
ciphered block as `[ ]` with the footnote **"Partie chiffrée"** — he could not read it.
Tomokiyo likewise lists f. 55 as undeciphered. The thirteen ciphered lines below have
therefore never been read.

The clear text around them, as printed by La Ferrière, is:

> Monsieur de Rennes, je n'ay receu vostre lettre du xviii<sup>e</sup> de juing que
> depuis sept ou huit jours, c'est pour **[ — thirteen lines in cipher — ]**
> Au demeurant, je veulx bien vous advertir que, après avoir essayé tous moyens de
> faire départir la royne d'Angleterre de la place du Havre-de-Grâce …

So the cipher fills the gap between "c'est pour" and "Au demeurant".

## Key

The cipher is the Bishop of Rennes' cipher (1561–64), reconstructed by S. Tomokiyo
(`images/CharlesIX_Rennes.png`). It is a homophonic alphabet (2–8 shapes per letter),
about thirty word-signs, and a set of nulls that includes ordinary French words written
in clear (`que`, `est`, `pour`, `plus`, `xix`, `vre`, `do`, `fo`). The key was calibrated
on this hand against the margin decipherment of the sibling letter f. 57 (13 Aug 1563),
whose first ciphered line reads `que les princes` — fixing p=b, r, i, n, c=m, e, s.

Shapes confirmed in this hand (my ASCII names, see `decode.py`):
a = z, η, ſ, ff-lig · c = 3, m · d = Ⱡa("ſa") · e = d, xy, xi, "ᶌ" · f = 4, φ
i = 10, 1̄0̄, #, m̨, k · l = 6, ơ · m = Ə, Ṅ · n = 9, ɑɲ, ᵹʒ · o = ᴄ, Ʒ, ʌ
p = b · q = ſſ · r = ɟ, ee, ~ · s = ʒ, ȼ · t = Ꙅ, ᴄ~ · u/v = λ, µ, ɑʃ · x = ✷
y = ✦, T · z = θ
Word-signs seen: que = q̄q̄ · vous = < · nous = > · vostre = + · qui = V̄ · mais = A
par = at · la = m̄n̄ · lettre = ᴄʃ · bien = ᴘʟ · faire = ᴄa · faict = ᴛᴜ

## Decoding

`decode.py` holds the glyph-by-glyph transcription of all thirteen lines and prints the
letter stream. Word division is mine; the cipher has none.

## Reading (first pass)

Secure stretches are in plain type; `…` marks glyphs I could not resolve and `[ ]`
marks restoration.

 1. … par … a vostre / **sceu ce que vous avez descouvert**
 2. … par … **du mariage** … **vostre advis** … [con]**duict**
 3. … **d'iceulx en mon intention**, et b[ien] **que tou**[s] …
 4. … fort … [qu'il] **ayt tenu ce chemin** d[e] …
 5. **ce qui pourra** … ayant aussi **entendu ce que le** …
 6. **vous mist en avant, qui l'avoit** … dél[ibéré] … **faire** … **la lettre bien**
 7. **de la** … bien tost … **l'avancement du concile, à ce que** ju[sques] …
 8. … **chacun faict** … de … **sa part** … monstre …
 9. … **fructueuse** … **de ce concile, mais nous** …
10. … **avoir l'utilité qui en sortira** … mes …
11. **mes** … **ce qui** … **mect des se**[ss]**ions** *Descembre* **des** …
12. **que** … **vous avez oy** … **par lettres** … vous …
13. … [tou]**chante** … [nulls: // ʌ vre est que xix 8ᵝ]

## Substance

The passage is about the Council of Trent and the Habsburg marriage negotiation, not
about the Havre — which is why Catherine put it in cipher and left the Havre news in
clear. She acknowledges what Rennes has *descouvert*, refers to *du mariage* and to his
*advis*, states her own *intention*, discusses what "le Sr …" *mist en avant*, and twice
returns to the *concile*: *l'avancement du concile*, the hope that it be *fructueuse*,
and *l'utilité qui en sortira*. Line 11's *sessions* and the clear word *Descembre* point
to the closing sessions, which in fact ended on 4 December 1563.

## What is left

Lines 2, 4, 8, 12 and 13 are the weakest: several homophones of r/s, e/o and l/t are near
identical in this hand and I could not always separate them at 8720-px resolution. A
second transcription pass, and the same treatment of the three sibling letters
(500 Colbert 390 pp. 139 and 357; 500 Colbert 392 p. 231), would close most of the gaps.
