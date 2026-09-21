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

Four letters in the same cipher, each read from its own image with values calibrated on
contemporary glossed letters in the same hand (21 Sept 2026). Share of cipher signs in
secure + probable French:

| Item | Date | Reading file | Read |
|---|---|---|---|
| fr. 3181 f. 55, Catherine | 31 July 1563 | `f55_v2_reading.md` | ~91% (80 secure, 11 probable) |
| 500 Colbert 390 p. 357 | late summer 1564 | `c390_p357_reading.md` | ~94% |
| 500 Colbert 392 p. 231, Bourdin | Dec 1562 | `c392_p231_reading.md` | ~80% |
| 500 Colbert 390 p. 139, "Deschiffrez vous mesmes" | 1562-63 | `c390_p139_v3_reading.md` | ~63% (36 secure, 27 probable) |

Token-weighted, about 82% of the 2,035 transcribed signs.

- **f. 55**: Council of Trent and the Habsburg marriage; "avancer le concile", "pour le bien
  de la Chrestienté", "ce qui se promect des sessions de Decembre, desquelz vous avez oy
  parler, vous estant dernierement à … Trante".
- **p. 357**: the precedence dispute at the imperial court (1564, after Ferdinand I's
  death): "il fauldra prandre autre pretexte que celuy porté par la depesche du s[ieu]r
  Charon… laisser là quelque secretaire ou aucun des vostres, advisés soubz couleur d'aucuns
  voz affaires particuliers".
- **Colbert 392 p. 231**: Bourdin encloses Catherine's letter of 15 Dec 1562 (La Ferrière I
  448-451) on the secret marriage overture; its leak to Spain ("sçavoit incontinant en
  Espaigne"), "[s]a femme … triumphe de la premiere ouverture que vous luy feistes de ce
  mariage", closing "d'amitié et alliance… à l'honneur de Dieu et au repos de la
  chrestienté". Clear end with date on p. 232.
- **p. 139**: a secret note, "decipher it yourself, trust no clerk, burn it": "que je vous
  tienne pour trop advisé et affectionné et loyal serviteur du roy mon fils… les yeux ouverts
  pour observer… mon cousin… ses actions… beau frère".

Method: `lattice.py` (beam decoder, fr-1530-despatches model) over per-glyph candidate sets;
per-hand values from the glossed siblings in `fr3181_glossed.md` (f. 57-58) and
`colbert390_glossed.md` (p. 138, pp. 189/199, 221-231). Crib material from La Ferrière in
`cribs.md`. Crops are git-ignored and rebuilt from Gallica.

## Setup (earlier session)
This is setup and key calibration, not a completed decipherment. No continuous reading of any of the four target letters has been established.

- Images fetched locally (img/): fr3181 v33-v42 (ff. 52-61), c390 v70-73 + v179-181, c392 v112-115.
- c390 v70 = pp. 138-139 spread: p.139 is the "Deschiffrez vous mesmes" note, ~20 lines cipher,
  plus a cipher paragraph on p. 138 with interlinear gloss visible (left page, partly deciphered).
- c390 v180 = p. 357: Catherine (?) letter, lower two thirds in cipher, ~25 lines, no gloss.
- c392 v112 = p. 231: Bourdin letter, ~30 lines cipher, no gloss.
- f. 55 = fr3181 v36: 17 lines of cipher then clear text (Havre de Grace / Queen of England passage in clear).

## Remaining gaps
- fr. 3181 f. 55, about 9% of signs (ꝥ, ɼ, εʃ, ɾ, 'h Ə'; runs on lines 4, 8, 9) - blocker: no-key-material; the signs occur in no glossed passage in this hand (f. 57-58 aligned in full; the Colbert 390 glosses are in another hand)
- 500 Colbert 390 p. 357, about 16 signs at the end of line 3 / start of line 4, one sign in line 10 - blocker: no-key-material; the run fits "l'Empereur" by pattern only; no gloss or print
- 500 Colbert 392 p. 231, about 20% (runs on lines 4, 5, 7, 8-9, 11-17, 22) - blocker: no-key-material; W, ss, tt, πꝫ, t7 and "maue" occur once or twice and in no glossed passage of Colbert 390 pp. 189-231
- 500 Colbert 390 p. 139, about 37% (lines 3-4, 7, 8-10, 12-14) - blocker: illegible; faint ink and heavy nulls; ẟ, ẟao, ẟar, ℛ, ℞, aʓ, Ꝫ unglossed anywhere found

## Escalation
- [x] siblings: fr. 3181 f. 52, f. 57, f. 58 and Colbert 390 pp. 138, 189/199, 221-231, 241 opened; f. 57-58 and p. 138 give the hands' values; Colbert 392 p. 232 is the clear end of the Bourdin letter
- [x] clear-pages: clear parts of all four letters used for context; Colbert 392 p. 232 dates the Bourdin letter
- [x] known-keys: Tomokiyo's Bishop of Rennes key; the Rennes2 (Lorraine) key checked, not this cipher
- [x] print: La Ferrière I-II (cribs.md): none of the four passages printed; Bourdin's enclosure is Catherine 15 Dec 1562; Tomokiyo lists all four as undeciphered
- [x] key-rebuild: per-hand values from glossed siblings, LM lattice decoding
- [x] retry: every letter re-run after each new value set; p. 139 control re-run withdrew four readings
