# Rennes 1563 — Catherine de Médicis / Court → Bernardin Bochetel, bishop of Rennes

Catalogue item 11 (class B). Goal: read the undeciphered letters
- BnF fr. 3181 f. 55 (Catherine, 31 July 1563) — ark btv1b9059845t, view 36 (folio = view + 19)
- 500 Colbert 390 p. 139 (ark btv1b10033942k, view 70; "Deschiffrez vous mesmes" note) and p. 357 (view 180)
- 500 Colbert 392 p. 231 (ark btv1b100339594, view 112; Bourdin, ~30 lines all cipher)

## Prior art
Tomokiyo, "French Ciphers during the Reigns of Charles IX and Henry III"
(https://cryptiana.web.fc2.com/code/henryiii.htm): reconstructed the Bishop of Rennes'
cipher 1561-1564 (`images/CharlesIX_Rennes.png`) from the deciphered letters in Colbert 390
and fr. 3158 f. 1 (Francis II, 3 Sept 1560, read with the key). fr. 3181 f. 52 (28 Feb 1563)
and f. 57 (10 Aug 1563) use the same cipher and carry marginal decipher glosses (views 33, 38);
f. 55 (31 July 1563) undeciphered. A second cipher (Cardinal de Lorraine → Rennes 1563,
Colbert 392 p. 27) = `images/CharlesIX_Rennes2.png`.
Short function words (est, plus, pour, que) double as NULLS in this key.

## Key (Tomokiyo reconstruction, images/CharlesIX_Rennes.png)
Letters (homophones separated by spaces; descriptions of glyphs):
- a: z / eta / long-s / ff-lig
- b: h / y-loop (8-like with tail)
- c: 3 / m-like / * / E
- d: La-lig / gamma-loop / x / script-v-dot
- e: d / xy / xi / backslash
- f: 4 / phi
- g: a / a-tilde / beta (circled)
- h: pi / pi-macron / c-hook
- i/j: 10 / 10-macron / m-hook / k / lz
- l: 6 / sigma / beta2
- m: 9-left / J-hook / N / d3
- n: 9 (circled) / u-hook / u-flourish / ff-tall / tt (circled)
- o: curl-C / 3-like / u-4 / lf
- p: b / Z / N-cap / my
- q: ss-double
- r: 2-like / s-swash / ee / U-cup
- s: 3-swash / phi-cross / V
- t: G-spiral(circled x2) / e-curl / c-tilde / T-bar / 6 / f-cross
- u/v: lambda / mu / w-flourish / w-3 / uv / gl-lig
- x: star4 / star6
- y: 7-hook / T / r-small
- z: theta / theta-slash
Nulls: // , double-dagger, =, r-hook, do, fo, eps3, g3, G-swash(circled), L-swash(circled); plus, pour, que, est, xix, vre (word-lookalikes as nulls)
Word signs: bien=pl, com=delta, con=croc, dit=delta-circ, ent=G-circ, est=#, et=g-tail/tp, faict=tu, faire=ca, la=mn-bar, le=vp, lettre=sc, luy=8
mais=A, nous=>, ont=delta2, par=at, plus=quote2, puis=tz, quant=Omega, que=qq-bar, qui=V-bar, si=z-swash, vous=<, vostre=+
l'Empereur=e-grave-like, Roy de Boheme=V-dot

## State

Status: read in part.

**fr. 3181 f. 55 (Catherine de Médicis to Rennes, 31 July 1563) is read in part** — see
`READING.md` and `decode.py`. The thirteen ciphered lines were never deciphered: La
Ferrière printed the letter in *Lettres de Catherine de Médicis* II, pp. 79-81 and set the
whole block as `[ ]` with the footnote "Partie chiffrée"; Tomokiyo lists f. 55 as
undeciphered. Tomokiyo's reconstructed key works on it once calibrated on this scribe's
shapes, which was done against the line-by-line margin decipherment of the sibling letter
f. 57 (13 Aug 1563, view 38), whose first ciphered line reads `que les princes`.

Continuous stretches recovered include: *sceu ce que vous avez descouvert*, *du mariage*,
*vostre advis*, *d'iceulx en mon intention*, *ayt tenu ce chemin*, *ce qui pourra*,
*entendu ce que le*, *vous mist en avant, qui l'avoit*, *l'avancement du concile, à ce
que*, *chacun faict*, *de ce concile, mais nous*, *avoir l'utilité qui en sortira*,
*mect des se[ss]ions*, *que vous avez oy*, *par lettres*. The subject is the Council of
Trent and the Habsburg marriage negotiation — which is why it was enciphered, while the
Havre-de-Grâce news in the same letter was left in clear.

Not yet attempted: 500 Colbert 390 p. 139 and p. 357, and 500 Colbert 392 p. 231 (same
cipher; images fetched to `img/`, which is git-ignored — `fetch.py` and `fetch3181.py`
rebuild it; note fr. 3181 folio = Gallica view + 19, so f. 55 = view 36).

## Setup (earlier session)
This is setup and key calibration, not a completed decipherment. No continuous reading of any of the four target letters has been established.

- Images fetched locally (img/): fr3181 v33-v42 (ff. 52-61), c390 v70-73 + v179-181, c392 v112-115.
- c390 v70 = pp. 138-139 spread: p.139 is the "Deschiffrez vous mesmes" note, ~20 lines cipher,
  plus a cipher paragraph on p. 138 with interlinear gloss visible (left page, partly deciphered).
- c390 v180 = p. 357: Catherine (?) letter, lower two thirds in cipher, ~25 lines, no gloss.
- c392 v112 = p. 231: Bourdin letter, ~30 lines cipher, no gloss.
- f. 55 = fr3181 v36: 17 lines of cipher then clear text (Havre de Grace / Queen of England passage in clear).
