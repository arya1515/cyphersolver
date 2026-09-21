# Dinteville (Langres) to the Duke of Nevers, 3 July 1592 (BnF Français 3621 no. 116, f. 130; DECODE R9451)

Status: attempted, open. Catalogue item 183. Session 2026-09-21. Not read.

## What the leaf is

- DECODE R9451 has one image (`IMG_R9451_I44642_P.png`, 2020 × 2881), fetched with the project cookie. The volume is
  also on **Gallica, `btv1b52524472n`**, full resolution, where the canvas is 2 × folio + 9 (from `lorraine1592/NOTES.md`):
  f. 130r = **view 269**, f. 128r = view 265. So fr. 3621 *is* digitised. The blancmesnil note of 16 Sept says
  otherwise; that note is wrong.
- f. 130r is a clear French letter signed by Dinteville, dated "de Langres le iij^e Juillet 1592". It has **two cipher
  passages set inline in the clear text**: about 3 lines near the top (lines 4-7, after "du reste de Strasbourg"), and
  about 7 full lines in the middle (lines 11-17, after "Comme Leur Roy …"). Roughly 400-450 signs in all. The signs are
  letters, digits and marks: `# 4 1 0 o v w m ψ α Δ □ ¢ ∇ π ƒ z +`, some with a bar or dot, and dots after some signs.
- **There is no decipherment on f. 130.** DECODE's "with cipher and decryption" does not hold for this leaf. The
  paragraph after the date, "Monseigneur ce matin j'ay sceu … l'armee lorraine …", is an autograph postscript in
  clear French in a poor hand. It is not cipher and not a decipherment. f. 130v (view 270) carries only the address.

## The sibling that has a decipherment

- **f. 128r (view 265)** is another Dinteville letter to Nevers, "[?] Juillet 1592", in the **same sign set**, with a
  contemporary decipherment written **above** each cipher line: "… m'a dict / avoir veu d'as[ce]nder a Geneve deux
  millions d'or d'Espaigne / … quarante cinq + mulets chargez qui doibt aussi passer dans trois / jours et prendre le
  chemin de Besançon qu'un chemin de Fl[andres] …". This is probably no. 114, which the lorraine1592 notes list as
  "avec chiffre et déchiffrement". About 150 signs, three and a half lines.
- The alignment test (`align.py`) takes the 50 signs I transcribed of the second cipher line and the interlinear
  "avoir veu descendre a Geneve deux millions d'or d'Espaigne" (48 letters). It looks for a one-sign-one-letter mapping,
  homophones allowed, with up to three sign types as nulls. **No consistent mapping exists.** "auoir" sits cleanly over
  `II Δ α ψ p`, but then the same `α` has to be `d` in "d'ascendre". The decipherer also writes `+` and `|` for signs
  they left unexpanded (after "cinq"), which points to nomenclator codes for words (cens, Geneve, Espaigne). So the
  system is a letter cipher with code signs, possibly polyphonic, and my eye transcription of the glyphs is not
  reliable enough to separate these readings from ~150 aligned signs.

## Why it stops

A key would have to be rebuilt from the short f. 128 crib and then pushed onto 400+ unglossed signs of f. 130,
and that rests on a glyph transcription I could not make consistent even on the crib. It is solvable in principle,
by a careful hand transcription of f. 128 and f. 130 (and any other Dinteville letters of 1590-92 in fr. 3621 /
fr. 4716 no. 31) followed by the nomenclator-plus-LM method of pelissier1592 and lorraine1592. It was not done this
session.

What would move it: a verified sign-by-sign transcription of f. 128's three cipher lines against the interlinear,
then of f. 130. Next leaf to check for more crib: the rest of fr. 3621 for other Dinteville letters (nos. 100-120).

Checked: DECODE image of f. 130; Gallica views 263-272 (ff. 127-131); the f. 130 postscript (clear); the f. 128
interlinear; Tomokiyo's Nevers catalogue (no Dinteville key). Not checked: the other Dinteville letters in fr. 3621,
fr. 4716 no. 31 (1590). The images stay git-ignored (BnF; DECODE says publication needs the library's permission).
The site crops are from Gallica, where BnF images are free for non-commercial use.
