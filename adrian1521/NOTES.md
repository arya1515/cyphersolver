# Adrian of Utrecht, the Admiral and the Constable of Castile → Charles V, Vitoria, 30 Dec 1521

AGS **Estado leg. 8 no. 150** (PARES description 13002542, 2 ff., 4 images; "Cifrada prácticamente en su
totalidad"). Written ten days before Adrian was elected pope (9 Jan 1522), signed by all three governors.

## Result (2026-09-18)

**Read in full. The letter had already been deciphered in the 19th century, and that reading has now been
checked and corrected.** Claudio Pérez Gredilla, head of the Simancas archive, deciphered it. Danvila printed his
text in *Historia crítica y documentada de las Comunidades de Castilla* t. V = **Memorial Histórico Español
t. XXXVIII (1899), pp. 703-705** ("Esta traducción se debe á D. Claudio Pérez Gredilla… sin que… haya podido
descifrar algunas palabras, que se trasladan tal como resultan en el original"). Danvila cites "Estado leg. 8,
fol. 150" (the foliation stamped on the leaf; OCR gives "460", the page scan reads 150); the text is the same letter. Found by OCR search of the
archive.org scan (`memorialhistri38realuoft`), after PARES gave the date and place.
[gredilla_1880s.txt](gredilla_1880s.txt) is a transcription of his text from the page scans. Code groups he
could not read are printed in italics, about 25 of them.

What this session added:

1. **Ciphertext transcribed** from the PARES images ([transcription.txt](transcription.txt); PARES serves
   nothing larger than ~1000 px, so this is from crop-and-upscale; several sign readings are still rough) and
   **aligned with Gredilla's text chunk by chunk** ([chunks.py](chunks.py), anchored on the 19 `xif` = V. M.
   groups against his 21 "V. M."). His reading holds throughout; the key below comes from that alignment.
2. **A wrong king.** Gredilla prints "el fallecimiento del **Rey de Inglaterra**". No King of England died
   in 1521 (Henry VIII died in 1547). The cipher has `Len top suz`, and the rest of the letter concerns
   **Manuel I of Portugal**, who died on 13 Dec 1521: "la Reina de Portugal y hermana de V. M." is Leonor, his
   widow and Charles's sister; "este moço el Rey que sucede" is João III; "los Reyes de Portugal tienen
   [alianza] antigua con los de Francia". On f. 1r l. 6 *Portugal* is spelled letter by letter after
   `top` (= Reina), with the same signs (`C` = g, `roc` = al) as the other spelled *Portugal* on l. 16.
3. **About 17 of Gredilla's unread groups read, or corrected as misreadings,** by cross-reference inside the
   letter itself: a group he left blank in one place is often spelled out, or read by him, in another. See
   [plaintext_corrected.txt](plaintext_corrected.txt), where every change is marked with a confidence level.
   The certain ones:
   - `rol` = *agora/ahora*: he read it himself in "porque ahora no hay recaudo" but left it blank at "que está [rol]".
   - `xep` = *ya*: "cu+xep" is his own "cuya copia"; so "para [xep] detención" = "para **cuya** detención".
   - `dopca=` = *urcas*: `dop` = ur- is certain from six occurrences of *urca(s)*.
   - `top` = Rey/Reina, `suz` = Portugal, `te` = de: "[top te] que tiene" = "a la Reina, de que tiene…".
   - `for` = *como*: "así por lo que pierde… **como** porque nos parece…"; Gredilla drops it twice.
   - Misprints in the 1899 edition, checked on the manuscript: "[xiu]" is `xim`, "[itb]" is `tib`, "[xap]" is
     `xac`, and the numeral "40" after "urcas [xub]" is the code group `yo`, not a number. The letter itself
     counts three hulks: one at San Sebastián and "los otros dos" at Laredo.
   Probable readings, from context plus the code's initial-letter ranges (next section): `ral` agora, `rip`
   alianza (twice), `pah xim` mucha voluntad, `xin` voluntad, `fir` contra, `pij` (por) manera, `lag=` ellas,
   `sig` procurar, `fun` coyuntura(?), `nag` Italia(?), `fac` Consejo(?).
4. **The shared-cipher hypothesis is negative.** The premise was that Adrian's own letters with decipherments
   would supply the key. They do not share this code:
   - Estado 8/112 (28 Jul 1520; transcription 8/113) uses a sign/figure cipher (`s ʓ ɦ x ω 8 g 3 7 ff β…`).
   - PTR 2/1/94 (24 Oct 1521; transcription 2/1/92), PTR 2/1/99, 2/1/100 (with a fully ciphered enclosure,
     pp. 3-5) and 2/1/101 (7 Dec 1521) all use Adrian's **dotted trigraph code** (`leb. nud. sa. cab. sih.
     gig. mef. vuh…`). That is a different nomenclator: V. M., *que*, *de* and *en* have other groups.
   - PTR 1/96/5, 9, 12, 13, 44 and 45 are clear-text transcriptions of the Admiral's 1521 cipher letters, with no
     ciphertext beside them. Their originals were not found on PARES.
   The joint letter uses a third code, probably the Admiral's or the Constable's with the court. A sibling in
   the same code is the way to settle the remaining groups (see "Open").

## The code (reconstructed from the alignment)

Mixed nomenclator: three-letter (sometimes two-letter) code groups for words and for syllables inside words
(`log` = *en* both as a word and in *s-en-tira*, *fallecimi-en-to*; `lan` = *de* in *pier-de*, *de-udo*), plus a
homophonic alphabet of letters, figures and signs. A code group takes a sign suffix for inflection (`mix` la /
`mix=` las; `fom` cosa / `fom=` cosas). `≡` (triple-barred staff) and `P4` open and close paragraphs.

The initial letter of a code group follows the plaintext alphabet in blocks, although the order inside a
block is not recoverable from this letter:
`r` a-words (aca, agora, al, alianza, amistad, antes, allá) · `f` c-words (con, Consejo, cosa, contra, como) ·
`l/L` d–f (de, del, dicho, el, en, es-, ella, Francia, franceses) · `n` h–l (ha, lo) · `m` la ·
`p` m–n (mar, mucha, manera, men-, negocios, no/nos) · `s` o–r (otra, para, parece, por, Portugal, qual, que,
que es) · `t` r–t (Rey/Reina, razón, remedio, salvo, si, su, esta/este, tan, tiene, todavía) · `d` u- (urca) ·
`x` v–y (V. M., voluntad, ya, yo).

| code | reading | | code | reading | | code | reading |
|---|---|---|---|---|---|---|---|
| xif | V. M. | | sur | que | | lan / Lan | de |
| Len | del | | Loc | el | | log / Log | en |
| Leg / leg | es- | | fer | con | | fap | Consejo |
| fom | cosa | | for | como | | fir | contra* |
| mix | la | | nex | lo | | nam | ha- |
| pri | no (pri= nos) | | pex | negocios | | pag | men- |
| pah | mucha* | | pit | mar | | pij | manera* |
| som | por | | sum | para | | sot | qual |
| sem | parece | | sex | que es | | so / sac | otra |
| suz | Portugal* | | sig | procurar* | | top | Rey / Reina |
| tah | su | | tao | esta/este | | tiz | tiene |
| tup | salvo | | toc | razón | | tul | si |
| tix | todavía* | | rac | aca- | | roc | al |
| ral / rol | agora | | rip | alianza* | | rum | amistad |
| rib | antes | | ril | allá | | lum | dicho |
| lix | Francia | | lux | franceses | | lag | ella(s)* |
| dop | ur- (urca) | | xep | ya | | xap | yo |
| xim / xin | voluntad* | | da | hacer | | te | de |
| puo | mi | | mun | tenido | | fun | coyuntura? |

Alphabet (partial; homophones): a = α, e4, Δ · c = a, 6, σ · d = q, z · e = ℓℓ, ℓℓ:, E · g = C · h/l = y ·
i = io, ⊥ · m = p · n = rto · o = + · p = R, ff · r = nt, G · s = `=`, P4 · t = g, d · u/v = ≠T · y = δ.
The alphabet values are good enough to follow every spelled word against Gredilla's text, but I have not
separated each homophone at this resolution. Treat this table as a reading aid, not a finished key.

## Open

`[suf]`, `[xub]` + `yo`, `[ren] [nod]`, `[xac]` (a people: "que [xac] y franceses son a unirse", "si [xac]
están neutrales"; the Scots fit the context, since Albany landed in Scotland with French backing in Nov
1521 and "marcas represalias" were a Scots–Flemish grievance, but the x-block should hold v–z words), `[sif]`,
`[tib]`, `[xit]`, `[Lag]` (one of the belligerents with France), `[ne]` (*la* or *mala* fortuna). Route: a sibling in
the same code, meaning another letter of the governors or of the Admiral or Constable to Charles in 1521-22 with a
decipherment. PTR 1/96 and 1/105 hold the Admiral's and Constable's correspondence. The originals of the PTR
1/96 transcriptions would be the first thing to look for.

## Files

- `pares.py` — PARES search and image download (the `ViewImage.do?accion=42&txt_descarga=1` route; only
  `txt_zoom=10` gives the ~1000 px image, all other values give 343 px). `probe.py` scans description IDs.
- `img/` — est8_150 (target); est8_112/113, ptr2_1_81/83/92/94/99/100/101, est7_234/236, ptr1_96_* (comparison).
- `danvila/` — MHE 38 OCR text and page scans n708-n710 (pp. 703-705).
- `transcription.txt`, `chunks.py`, `gredilla_1880s.txt`, `plaintext_corrected.txt`, `key_working.md` (first draft).
- `strips/`, `ln/`, `crops/` — upscaled line crops used for transcription.
