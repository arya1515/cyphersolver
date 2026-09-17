# Jean du Bellay (London) to Montmorency, 1529 — BnF fr. 3077 and fr. 3078 (catalogue item 4)

Working notes, 17 Sept 2026. Images: Gallica IIIF `btv1b90599292` (fr. 3077, 200 canvases) and `btv1b9060311s`
(fr. 3078, 177 canvases); in fr. 3078 canvas = page number (the volume is paginated, not foliated: p. 21 = canvas 21).
Downloads in `img/` (gitignored; `fetch_thumbs.py`, `fetch_pages.py`). Gallica dropped connections for most of the
session and returned 429 after ~30 requests; only fr. 3078 pp. 21–27, 31–32 were obtained at full size, no fr. 3077 page.

## 1. What the catalogue item is

The BnF notice (OAI record, `ref/oai_*.xml`) gives day and month only; the volumes are bound by day-month across
years. Identification from Le Grand's *Histoire du divorce* t. III (1688, Preuves, MDZ bsb10280117, OCR in
`ref/legrand3_*.txt`), Brewer's *Letters and Papers* IV (BHO, `ref/lp4_1529_dubellay_full.txt`) and the leaves:

| notice | date | L&P IV | Le Grand III | leaf | cipher state |
|---|---|---|---|---|---|
| fr. 3078 no. 3 "lettre chiffrée, XVIe de juing" | **16 June 1529** | not calendared | not printed | p. 21 (one page, 8 lines of cipher) | **never read**: DECODE R3688 "Non-decrypted"; not in Bourrilly 1905, Le Grand, L&P |
| fr. 3078 no. 4 "lettre chiffrée, XXIIe de juing" | 22 June 1529 | not calendared | pp. 327–332 (Béthune 8603 f. 25) | pp. 25–27 | contemporary **interlinear decipherment** on the leaf, word by word |
| fr. 3078 no. 5 "avec chiffre, XVe de juing" | 15 June 1529 | 5679 | pp. 323–326 | p. 31–33? (DECODE R3690 "partially decrypted") | printed in clear |
| fr. 3077 no. 18 "avec chiffre, XVIIIe de septembre" | 18 Sept 1529 | 5945 | pp. 354–359 | f. 113 (DECODE R4252 "Decrypted"; Friedmann's key NAF 4206 no. 5 "refers to fr. 3077 fol. 114") | printed in clear |
| fr. 3077 no. 20 "lettre chiffrée, IIIIe d'octobre" | 4 Oct 1529 | 5983 (+ BL Add. 28579 f. 178) | pp. 359–363 | f. 125? (DECODE R4253 "Decrypted") | printed in clear |
| fr. 3077 no. 23 "avec chiffre, XXVIIIe d'octobre" | 28 Oct **1528** | 4879 | (Le Grand III 188–192) | pp. 145–147 = canvases 143–145 (read on the leaf: "Monseigneur, je croy que me pensez si peu paresseux…") | Bourrilly 1905 no. 156 prints the 15 cipher lines in clear with the key they recovered ("la royne a dict à quelqung … l'Empereur ne cessera jamais qu'il n'ayt ruiné le roy d'Angleterre"); Lasry 2022 re-solved the key; DECODE R4254 "Non-decrypted" is stale |
| — (not in the catalogue item) | **22 Oct 1529** | 6019: "the beginning of the letter is in cipher, undeciphered" | pp. 377–379: "le commencement de cette lettre est en chiffre non déchiffré" | original not in fr. 3077 (Le Grand cites Béthune 8530, a different volume); copy fr. 3005 f. 165 | **opening unread since 1529**; Tomokiyo: "unsolved, in Bayonne's cipher (1529)" |
| fr. 3078 no. 17 "avec chiffre, XVIIe d'octobre" | 17 Oct 1529 (Wolsey's fall) | 6011 | pp. 369–375 (Béthune 8603 f. 113) | pp. 113–117 (DECODE R3691 "partially") | printed in clear; L&P's abstract includes the cipher passages |
| fr. 3078 no. 19 "avec chiffre, XXVIIe d'octobre" | 27 Oct 1529 | 6030 | pp. 379–381 (f. 133) | pp. 133–134 (DECODE R3692 "Decrypted") | printed in clear |

So the catalogue's "no decipherment noted" is Omont's inventory language. **All five letters of the catalogue item
are in print in clear**: fr. 3078 nos. 5, 17, 19 and fr. 3077 no. 18 (15 June, 17 Oct, 27 Oct, 18 Sept 1529) in
Le Grand 1688, from the Court's decipherments (Brewer 1875 abstracts them), and fr. 3077 no. 23 (28 Oct 1528) in
Bourrilly 1905, whose editors recovered its key. The item is therefore closed as *found already solved*. What the
sweep of the two volumes turned up beyond it: the whole cipher block of **16 June 1529** (fr. 3078 p. 21) has never
been read, and the opening of **22 October 1529** (not in these volumes; copy fr. 3005 f. 165) is marked undeciphered
by Le Grand, Brewer and Tomokiyo.

The 1528 letters are a different matter: Bourrilly and de Vaissière, *Ambassades en Angleterre de Jean du Bellay*
(1905, archive.org `ambassadesenangl00dube`, OCR in `ref/bourrilly1905.txt`) print the whole first embassy
(Sept 1527 – Feb 1529) in clear, recovered the lost key of du Bellay's *first* cipher themselves (letter of 28 Oct 1528,
fr. 3077 pp. 145–147, their no. 156 n. 6: "nous en avons retrouvé la clef qui était perdue"), and note that the
ciphered stretch of 21 Oct 1528 is "en chiffre dans le texte" (printed in clear). George Lasry re-solved the 1528
cipher in 2022 (Tomokiyo, GL.htm, "Bayonne's Cipher (1528–1529)", Clair. 328 f. 291 = the same 28 Oct letter).

Scheurer, *Correspondance du cardinal Jean du Bellay* t. I (1969) covers 1529–1535 and must print these letters; it
is on archive.org only as a lending copy (`correspondancedu0000remy`, text and search-inside blocked, HTTP 401/403)
and Google Books returned 429 all session. **Not checked.** If Scheurer read p. 21 or the 22 Oct opening, the
"never read" claims above fall.

## 2. The cipher and its key

"Bayonne's Cipher (1529)" (Tomokiyo, francis.htm, reconstructed from Clair. 333 ff. 24, 27 of June 1530; image
`ref/tomokiyo_francisBayonne.png`): a homophonic symbol alphabet (2–4 signs per letter, no k/v/w; u = v), a few
nulls, word signs for *roy* and *madame*. Paul Friedmann's 19th-century reconstruction is BnF NAF 4206 no. 5
(DECODE R9467, image not public). Tomokiyo lists the same cipher in Clair. 329 f. 139 (30 June 1529), Clair. 330
ff. 16, 71, 85 (18 Sept, 17 Oct, 27 Oct 1529, the copies with decipherment), fr. 3040 f. 68 (30 June, "undeciphered"),
Clair. 312 f. 325, Clair. 313 ff. 339, 343, fr. 3005 f. 165 (22 Oct, "unsolved").

The key was re-derived here from the leaf itself: the 22 June letter (pp. 25–27) carries the Court decipherer's
interlinear reading over every cipher sign, and Le Grand prints the clear text, so glyph and letter align one to one
(`img/c025_*`, `img/c027_*` windows). Readings confirmed on p. 25–27 (glyph → letter; T = Tomokiyo's table):

| letter | signs seen | notes |
|---|---|---|
| a | c, ∪, ⊔, ∩, ɔ | T has ɔ c ∪ ⊔; ∩ new ("desia", "de la") |
| b | * | T also ⊓ |
| c | Y (y-shaped, hooked), ⊐ | "icy", "rechercher" |
| d | ℘ (curled p), ⊏ | "desia", "viendra", "de" |
| e | ω, ✝ (cross with top serif), ✗ (x with descender) | "viendra", "et", "desia" |
| f | ═, ⫽ | "fin", "faire" |
| h | ρ (9-shaped), L | "rechercher" (both) |
| i | —o, o— (bar and small o, either order) | "faire", "qu'il", "fin", "desia" |
| l | △, ⧋ | |
| m | ◇, ◇ with small cross at lower right | "me", "ma part", "mon" |
| n | +◇, ◇+— (cross and diamond, cross left or bar right), —ᴜ | "fin", "viendra", "sont", "honestes" |
| o | 3, ε, **B** | B is not in T; "mon", "roy", "ont", "pou-oir" fix it |
| p | Λ, λ, H | "partie", "pour", "aporter" |
| q | ⊤ | "qu'il", "que" |
| r | ⊡ (dotted square), □ | |
| s | ᴜ—, —e (bar and e-loop), ᒐ (hook), cross with bottom curl | "desia", "assez", "honestes", "se" |
| t | ✧̂ (diamond with cross on top), ⚲ (circle on cross), cross with top hook | "partie", "et", "sont", "semblant" |
| u/v | 8, ℓ, y, ξ | "pour", "que", "trouvez", "vous" |
| x | ϖ | T; not confirmed here |
| y | π | "icy", "envoyé" |
| z | ¨j (j with two dots) | "assez", "qu'ilz" |
| words | V = bien; R = fault; —ʔ = paix; ᛏ = madame; ee = roy; ○ = les? ; ⊞ (boxed cross) = a name | V, R, paix new to T |

## 3. Reading of 16 June 1529 (fr. 3078 p. 21) — partial

Clear text (first reading) in `p21_transcription.md`: du Bellay writes about "l'evesché" he hopes for, "la menée
qu'on me veult f[aire], que je sçay depuys le retour de mon homme", and asks Montmorency "en renouveller quelque
mot" to the King and to send his decision by the next despatch. Eight lines (c. 190 signs) are in cipher.
With the key above the block reads in stretches:

- l. 0: … *(c|v)ous et(?) trouvez … la ou* (the sign after "trouvez" is ═ = f, giving "fon la ou"; "bon" expected)
- l. 1: *…ptez a vous, [j']ay en…e de faire*
- l. 2: *semblant [que] madame ne fust a … pour con-*
- l. 3: *-clure … la [⊞] luy ayt par-* (⊞, a boxed cross, is a person; "luy ayt parlé" likely)
- l. 4: *… importun(?) … [il] fault envoyé querir pou-*
- l. 5: *-voir; il ne fauldroit oublyer a le*
- l. 6: *faire …*
- l. 7: … then clear *toutesfois, messire, vous ne …*

About 60 % of the signs resolve to a letter that yields French; the rest are the diamond-cross family (m/n/t),
the two cross-with-hook signs (s/t) and three signs not seen on pp. 25–27 (ℒ, ⊞, ⊏ with an overbar). Glyph reading
at 4 262 px width is the limit; the per-glyph windows are in `img/c021_Q*`, `img/c021_Z*`.

## 5. Independent check on a catalogue letter: 17 Oct 1529 (fr. 3078 pp. 113–117) read on the leaf

Fetched at full size in a third pass. The letter is four pages almost entirely in cipher with no interlinear
decipherment (one word, *n'empesche*, glossed on p. 116); Le Grand's clear text therefore came from a deciphered copy
(Clair. 330 f. 71). The first cipher lines (p. 113, from "Au demourant") read with the key above, sign by sign:

    —o ∪ π | ω ◇₊ ✚̂ | 8 ✗ 3 o— □ | ⊞ | en ses | ω …          → j'ay est[é] veoir [le Cardinal] en ses e[nnuis]
    3 8 | ⊤ ℓ ω | △ o— ∪ π | ✧̂ □ ε ξ ω | △ ω | λ ⧋ ℓ o— | ρ □ ∪ ◇+ ✧̂ | exemple
                                                            → ou que l'y ay trouvé le plus grant exemple

Le Grand III 370: "Au demourant, j'ay esté voir le Cardinal en ses ennuis, où que j'y ay trouvé le plus grand exemple
de fortune". So the key reads the catalogue's 17 Oct letter directly from the leaf, independently of the 1688 print,
and fixes two more signs: the boxed cross ⊞ = *le Cardinal* (Wolsey), and ρ (open loop) = g beside the closed-loop
9-shape = h. With ⊞ = le Cardinal, p. 21 l. 3 reads *… le Cardinal luy ayt par[lé]*, i.e. the 16 June letter already
concerns Wolsey's intervention over the bishopric du Bellay hoped for. The 27 Oct letter (pp. 133–134) carries the
decipherer's interlinear reading over some twenty cipher lines (`img/c133_L*` windows cut, not yet read): the crib to
finish the p. 21 variants.

## 4. What is checked, not checked, and next

Checked: BnF notice items against Le Grand, L&P and the leaves for fr. 3078 pp. 21–27, 113–117, 133–134 and fr. 3077 canvases 128–150 (dates 16, 22 June 1529 read
on the leaf); Bourrilly 1905 for every 1528 date (all printed in clear); DECODE records R3688–3693, R4252–4254,
R9467, R2287; Tomokiyo francis.htm and GL.htm; Le Grand III pp. 318–400; L&P IV May 1528 – Nov 1529 du Bellay entries.
Not checked: Scheurer 1969 (lending copy); fr. 3077 leaves (Gallica down); Clair. 330 copies with decipherment;
fr. 3005 f. 165; NAF 4206 (restricted).
User must verify: the partial reading of p. 21 word by word against the leaf, and whether Scheurer prints p. 21.

fr. 3077 canvases 128–150 were fetched at 2000 px in a second pass (`img/p3077_2000`): 131–133 = 12 Oct 1529 in
clear, 135–138 = 16 Oct 1529 in clear, 143–145 = 28 Oct 1528 (pp. 145–147, the first-cipher letter, 15 lines of
cipher, Bourrilly no. 156), 149–150 = 1 Nov 1528. No 22 Oct 1529 leaf is in this stretch, consistent with Le Grand's
Béthune 8530 reference pointing to another volume.

Next: (1) finish p. 21 with the pp. 26–27 windows (`img/c027_L*`) to pin the diamond-cross and hooked-cross variants;
(2) the 22 Oct 1529 opening from fr. 3005 f. 165 (Gallica ark to find) with this key; (3) Scheurer t. I for both.
