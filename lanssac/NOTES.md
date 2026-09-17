# Lanssac to Charles IX, Warsaw, 26 April 1573 — BnF fr. 4735 no. 51, f. 124 — NOTES

**Verdict: read.** Both cipher passages of the letter are recovered, 96 of the 100 signs. The key is a homophonic
letter cipher with two or three signs per common letter, a dozen syllable and word signs (*et, nt, st, de, ou,
car, Allemagne, pour, ns*), and the Court decipherer's marginal gloss, cut by the gutter on the microfilm, gives
fragments of both passages. Lanssac writes that, after the dangers French travellers now meet in Germany, the
obstacles in Thuringia, Meissen and the Mark of Brandenburg delayed him so much that he reached Poland
(Międzyrzecz) only on 25 February, and that without the escort of the King's pensioners Alexander von Miltitz and
Georg L(u)e(l)z he would "at the least have been detained or prevented from passing on". The rest of the letter
is in clear and refers to the *recueil* on the state of Polish affairs that follows it in the volume (no. 52,
ff. 126–127, "Deschiffrement du memoire"), which is why the catalogue lists a decipherment for the mémoire and
none for the letter.

Session 2026-09-17. Catalogue item 3 (class A). The catalogue entry gave f. 126; the BnF notice puts the folio
before the item number: no. 51 is f. 124 (canvas 242 of the Gallica scan btv1b9060724s), no. 52 (the mémoire in
clear, "Estat des affaires de Pollongne selon que le Sr de Lanssac y a peu aprendre") is ff. 126–127 (canvases
244–247). Confirmed on the images.

## 1. Prior art

- S. Tomokiyo, "French Ciphers during the Reigns of Charles IX and Henry III" (cryptiana, henryiii.htm), section
  "Ciphers of Monluc and Lansac, Sent to Poland (1573)": lists Lansac's cipher letters at ff. 124, 132, 138, 154,
  160, 164 and 331 and prints a reconstructed table (henryiii_Lansac.png, 689 × 285 px) with no transcription or
  reading of any letter. He notes that "a pair of symbols" seems "to delete symbols in-between" (ff. 154, 156).
  The letter is not on his unsolved page. His table is right for most of the first row and for the syllable
  signs, but its first row is **shifted by one letter from *m* onward** (his *ſ = m, L = n, ʒ = o, б = p, ⊨ = q,
  9 = r, ʓ = s, o+ = t* read here *ſ = n, L = o, б = qu, ⊨ = r, 9 = s, ʓ = t, o+ = u*), his row-3 *Γ = i* is *e*,
  his *‡ = h* is *d*, and his *pour* sign is the letter *h* in one of its two shapes. The differences are in
  key.tsv, column "Tomokiyo".
- Noailles, *Henri de Valois et la Pologne en 1572* (1867), vol. III (archive.org henridevaloisetl03noaiuoft):
  prints Monluc's and Lanssac's Polish correspondence selectively; the 26 April letter is not in it (OCR
  searched for "Lanssac", "26 avril", "Varsovie"). Monluc to Lanssac of 31 March 1573 and the "Avis de Varsovie"
  of 9 April are.
- DECODE: fr. 4735 does not appear in the French records harvested on 17 Sept 2026 (gallica_sweep/decode_France.html).

## 2. The documents

Gallica IIIF, `https://gallica.bnf.fr/iiif/ark:/12148/btv1b9060724s/f<N>/full/full/0/native.jpg`, 4417 × 6483 px
microfilm scans, all canvases labelled NP; canvas ≈ 1.76 × folio (rectos, and versos only when written). Fetched
with fetch_range.py one page at a time; Gallica answers 429 after some 25 requests and the script backs off.

| folio | canvas | item |
|---|---|---|
| 121 | 238 | no. 49 (Latin arrêt against Coligny) |
| 124 | 242 | **no. 51, Lanssac to Charles IX, 26 April 1573** — 4½ lines in cipher, gloss in the left margin |
| 126–127 | 244–247 | no. 52, "Deschiffrement du memoire … Estat des affaires de Pollongne", clear |
| 152 | 292 | no. 58, Noailles to the King |
| 154, 154v | 294 (dup. 296), 297 | no. 60, Lanssac to Anjou, 24 April — 20 + 17 lines of cipher, marginal decipherment |
| 156–157 | 300–303 | no. 61, Lanssac to Catherine, 24 April — cipher blocks, marginal decipherment |
| 160, 164 | c. 307, 314 | nos. 63, 65, Lanssac to the King and to Anjou, 1 May (fetched, not used) |

The "déchiffrement" the catalogue notes for the siblings is not a separate leaf but a **decipherment written in
the outer margin**, line by line beside the cipher; the microfilm cuts it at the gutter so only the ends of its
lines survive (img/f154_margin*.png, img/f154v_margin*.png). f. 124 has the same kind of gloss beside its two
passages: "…es dangier", "…d'Allemagne", "…qui passent" beside ll. 1–3 and "moins esté retenu", "…ou oultre"
beside ll. 9–10.

## 3. The cipher

Signs are separate graphic symbols (crosses, bars, figures, letter-like forms), written continuously with commas,
points and short bars as word separators. Frequencies over the 741 tokens transcribed (f. 124, f. 154 block 1,
f. 156 block 1, f. 154v l. 1): e-signs 131 (17.6 %), r 65, a 54, s 50, n 49, u 44, t about 40, o 34 — a French
letter profile once the homophones are merged. Design, from the 47 signs met:

- **Letters:** a ⊤ π H · c 7 ⋔ · d ‡ · e ✕ ✱ Γ Δ · f o- · g ∞ · h + · i ⊢ ϙ · l 3 ⊥ · m 8 ᥙ · n ſ o-o · o ꞔ L ·
  p y N · qu ꞗ · r ϕ ⊨ · s 9 Lo IIII ттт · t ʓ ттт · u/v o+ ff o+o. (b, x, y, z not met with certainty; three
  signs — 4, ⊓, ʒ — occur 4–11 times in the siblings and are unread.)
- **Syllables and words:** *et* ♁ (a second form of it is *nt*; the transcription does not separate them), *nt* ꝸ,
  *st* 8 with a dot, *de* ᒐ and ꝛ, *ou* ᛏ, *ns* Λ, *car* Z, *Allemagne* Z with a lower curl, *pour* †.
- No nulls found in f. 124. The "deleting pair" Tomokiyo saw on f. 154 was not needed: the pairs of bars enclose
  single signs that read as letters (|ϕ| = *r* in *retenu*).

## 4. How the key was recovered

1. **Crib from the glossed sibling.** f. 154v l. 1 reads, beside the gloss "Car je n'ay pas cinquante escuz":
   Z ⊢✕ | ſπϙ | y⊤9 | 7⊢ſꞗπſʓ✕ = *car ie nai pas cinquante*. That fixed Z = car, ⊢ = i, ✕ = e, ſ = n, π ⊤ = a,
   ϙ = i, y = p, 9 = s, 7 = c, ꞗ = qu, ʓ = t, and showed that Tomokiyo's first row is off by one from *m*.
2. **Passage 2 of f. 124 by hand** against its gloss: † ⊥ ✕ . 8 ꞔ ⊢ o-o 9 . ✱ 8̣ Γ . ϕ ✕ ʓ ✱ ſ o+ = *pour le moins
   esté retenu* gave 8 = m, ꞔ = o, o-o = n, ✱ = e, 8̣ = st, Γ = e, ϕ = r, o+ = u; then ᛏ Γ ᥙ y ✕ 9 7 + ✱ . ᒐ =
   *ou empesché de*, y π 9 Lo ✕ ϕ ꞔ ff 3 ттт ⊨ Γ = *passer oultre*, ᥙ . π ꟿ Lo = *mais*.
3. **Annealer over the whole transcription** (solve.py: French 5-gram model sp53/fr5.npy, 24-letter alphabet,
   symbol → letter or short code, the crib letters pinned). Seeds agree on the free signs to within 2–8 rare ones
   and return ‡ = d, Lo = s, ⊥ = l, L = o, ᥙ = m, 3 = l, ттт = t, which read gloss words never used as cribs in
   the siblings: *les dangiers*, *l'autre* (gloss "causé l'autre"), *causé*, *beaucoup*, *grant seigniur*
   (gloss "grand seigneur"), *du monde* (gloss "que du monde"), *changement*, *sur la teste* (gloss "sur la
   teste"), *recommandé*, *doubte ou vous mettre*. The transcription of the siblings (tokens.txt) is a first pass
   with known glyph conflations (plain 3 vs hooked ʓ, three vs four strokes, the two cross forms, the two *et*
   forms) and is not offered as a reading of ff. 154–156.
4. **Lattice decode of f. 124** (lattice.py): each sign given its candidate values, beam search on the 5-gram
   score; the two passages come out as in reading.txt, with the choices listed there sign by sign.
5. **Controls** (controls.py, controls.log, 741 tokens). Pinned run, real order: −2193 to −2198 over three seeds.
   Pinned run on three shufflings of the same tokens: −2924, −2973, −3009. Blind run (nothing pinned): one seed
   reaches −2033, a *better* score than the pinned key, but recovers only 6 of the 21 crib letters; the other two
   seeds recover 0 and 4. So the language model alone does not find this key from a transcription this noisy;
   the cribs and the glosses do, and the model then fills the remaining signs consistently with words the cribs
   never touched.

## 5. Reading

reading.txt has the full letter with the clear text. The two passages:

> Sire, [despuis? les dangiers qu'encontrent en Allemagne les françois qui passent, et vostre ser{o r h e}] Les
> empeschementz et les plus grandes causes qui ayent esté depuis deux {ans} … toute la Turinge, Misnie et Marche
> de Brandebourg m'ont tellement retardé que je n'arrivay en Polongne à Mezeritz que le vingt-cinquiesme de
> febvrier. Et sans la faveur que j'ay receue d'aulcuns des serviteurs et pensionnaires de vostre Majesté,
> principalement des Sieurs Alexandre de Militiz et George Luelz(?), qui me y ont accompagné avec bonne et forte
> troupe de leurs amis et assisté de leurs moyens, j'eusse sans doubte [pour le moins esté retenu ou empesché de
> passer oultre. Mais], la grace à Dieu, je me suis rendu il y a desjà long temps avec Monsieur de Valence …

The Miltitz were Saxon nobles in French pay; Mezeritz (Międzyrzecz) is the first Polish town on the road from
Frankfurt an der Oder to Poznań. The "dangers" are the hostility to Frenchmen in Protestant Germany after
St Bartholomew's Day, which is why this passage is in cipher and the itinerary is not. Lanssac reached Monluc
in Warsaw in time for the election Diet (opened 5 April); Anjou was elected on 11 May.

## 6. What remains uncertain

- Passage 1, first word: ꝛ 9 N ff ϙ IIII is read *despuis* (ꝛ = *de* and N = *p* on this one occurrence each);
  the gloss end "…es dangier" is compatible with "…uis les dangiers" but the gutter takes the start.
- *françois*: o- ⊨ ⊤ ſ ⋔ ꞔ ϕ 9 gives *fran-c-o-r-s*; the seventh sign must be the *i* sign ϙ (P with a loop),
  which this hand writes close to the *r* sign ϕ, or the word is not *françois*. *qui* rests on the gloss; the
  cipher has ꟿ Γ, and ꟿ reads *i* in *mais*.
- Passage 1, end: *et vostre ser* + four signs ꞔ ϕ + ✱ (*o r h e* under the key), probably *service* with a
  misread sign; left in braces.
- The two forms of the *et* sign (*et* / *nt*) and of the cross (*h* / *pour*) are told apart by context here,
  not by the transcription.
- Passage 2 is read in full and agrees with both gloss fragments.
- Not done: reading ff. 154–164 in full (they carry their own decipherments in the margin, so nothing new is
  locked in them), and the f. 331 letter Tomokiyo lists in the same cipher, which has no decipherment noted.

## 7. Files

fetch_range.py (Gallica IIIF fetch with back-off) · strips.py (deskew a block, cut one strip per line) ·
tokens.txt (741 tokens: f. 124, f. 154, f. 154v l. 1, f. 156) · f124_tokens.txt · solve.py (annealer) ·
lattice.py (candidate-set beam decode) · controls.py, controls.log · key.tsv · reading.txt ·
Tomokiyo’s table at cryptiana.web.fc2.com/code/henryiii_Lansac.png (not copied here). Page images and crops (img/, 177 MB) are not committed;
docs/lanssac_f124.jpg is the cipher block of f. 124.
