# "French marshals to the King", BnF fr. 3081 f. 41 (DECODE R2322): Cardinal Campeggio's conclave articles, c. 1534 — NOTES

Status: read in part

**Verdict: f. 41r was already READ by George Lasry (key and overlay dated 24 May 2022, on Tomokiyo's cryptiana
pages). f. 41v, a second full page of cipher, had no published reading; it is read here with Lasry's key
(about 90–95% of letters secure).** The letter is not from 1520 and not from marshals: it is a copy of the articles
that Cardinal Lorenzo Campeggio swore into the hands of the French cardinals Bourbon, Lorraine and Tournon,
promising what he would do for Francis I if elected pope. Tournon was made cardinal in 1530 and Campeggio died in
1539, so the only conclave that fits is **October 1534** (death of Clement VII, election of Paul III). Catalogue
entry 195 is resolved and removed. Session 2026-09-21.

## Sources

- DECODE R2322 (Non-decrypted, "1 Jan 1520", "French marshals → French King"): four images fetched with the
  shared cookie into the git-ignored `decode/` — P1 = f. 41r (cipher), P2 = f. 41v (cipher), P3 = f. 42r
  (blank), P4 = f. 42v (endorsement "Dupplicata des articles envoyez par messrs les marechaulx françoys au roy").
- S. Tomokiyo, "French Ciphers during the Reign of Francis I", cryptiana `code/francis.htm`, section "BnF fr.3081":
  "George Lasry solved it in 2022". Lasry's key table and three overlay crops (`GL/GL_BnFfr3081_f41*.png`, on
  the page `GL.htm`) cover **f. 41r only**. Lasry also found the same key reads BnF Dupuy 265 f. 132 (Mâcon to
  the King, 29 May 1535). Copies in the git-ignored `prior/`.

## The system

Homophonic substitution with graphic signs, no word division: 20 letters with 1–4 signs each, and two code signs
(CON, ET). It is the cipher of the bishop of Mâcon's Roman embassy. Adjustments found on f. 41v:

- The three-stroke sign that Lasry lists third under H reads **Y** throughout (roy, iceluy, quoy, veoyant, moyennant).
- The "Rg" sign is **P**, not T (penser, pourveoir, pouvoir, partie, persuasion).
- A looped "4" acts as **R** (pour, pourveoir).
- Lasry's first "Unknown" sign (a bold ʃ) is probably **S**: "par [s]es dictes persuasions", "vers le[s] detenteurs".
- His second "Unknown" (the ɱɱɓ cluster) appears once, in "devers [UNK] et ses successeurs". It is probably a code for a person, likely the Emperor (grade M, from context only).

## The reading of f. 41v

Line-by-line transcriptions: `f41v_lines01-19.md`, `f41v_lines20-38.md`. Read from the images by two Claude
subagents with Lasry's table and his f. 41r overlays as a training sheet. Running text, normalised:

> … [tres chre]stien et serenissime seigneur Francois roy de France, la Maieste duquel a esté souventefois
> recherchée de contribuer a l'entreprinse de l'expedition contre iceluy grant Turc, qu'il a tousiours niée,
> le pouvant faire sinon que premier sa Maieste feust reintegrée et restituée en la duché de Milan, conté d'Ast
> et seigneurie de Gennes, desquels en avoit esté spoliée violentement et par force. Et pendant que sa
> Maieste n'estoit reintegrée en ses seigneuries, ne povoit pencer a une expedition si loingtaine ne aux chouses
> [?] d'iceluy grant Thurc. Par quoy, veoyant la volunté et grande envie dudit treschrestien roy … qu'il ne les
> puisse reprendre, en maniere que la paix, qui n'a aucun lien ferme, … soit pour engendrer bien toust et
> prestement en Italie aultre plus grande fla[m]e de guerre que devant; si moyennant l[e]s … l'on ne vient a
> penser d'y pourveoir, ce que par grande experience se cognoist ne pouvoir faire sans contenter en quelque
> partie le dit tres crestien roi. Et pour ce, s'il plaist a Dieu me donner grace d'estre pape, suis venu
> avecques les negotiateurs de Sa Maieste aux articles ci souscripts et aux conventions par moy iurees.
>
> Et premierement ie [s]aierai avecques toute demonstration, persuasion et exhortation que l'on pourroit user,
> ainsi devers [code: the Emperor?] et ses successeurs comme vers les detenteurs du duche de Milan et tout
> l'estat du dit duche, conte d'Ast et seigneurie de Gennes, que les dicts estatz et seigneuries soient rendus et
> restitues es mains du dit seigneur roi tres crestien ou des illustrissimes seigneurs ses enfans et
> successeurs. Et quant par ses dictes persuasions et voie …

f. 41v breaks off mid-sentence with no signature. The rest of the articles were on a leaf that is not in the
volume, or is filed elsewhere.

## Second pass

A retry of every doubtful place at 3–4x zoom (table in `f41v_lines20-38.md`, "Second pass") settled: l. 2 "a este"
(C), l. 5 "niee" (H), l. 8 "desquels en avoit" (C), l. 16 the scribe wrote A twice (H), l. 27 "moy" (H), l. 31
"successeurs" and "vers les detenteurs du duche" (H: the bold ʃ is S, confirmed in l. 37), l. 35 "restitues es"
(C), l. 36 "illustrissimes" (C), l. 37 "par ses dictes" (C).

## Remaining gaps

- l. 12 "SORVOEES" after "chouses", letters clear, word not understood - blocker: illegible; in sense, not ink: not a French word in this form, possibly a scribal slip.
- l. 15 "de SAREES", letters clear, word not understood - blocker: illegible; in sense, not ink: perhaps a proper name or slip.
- l. 19 sign 4 of "fla?e" - blocker: no-key-material; sign absent from Lasry's table, "flame" from context only (M).
- l. 30 the code cluster (Lasry's Unknown 2) before "et ses successeurs" - blocker: open-codes; the Emperor from context (M).
- The rest of the articles after f. 41v - blocker: needs-physical-access; fr. 3081 unseen beyond ff. 41-42, the text breaks off, f. 42 blank.

## Escalation

- [x] siblings: DECODE neighbours R2319–R2325 opened (fr. 2988 and Dresden, unrelated); Lasry's sibling for the same key, Dupuy 265 f. 132, already read by him. fr. 3081 ff. 40/43 not opened (no Gallica ark found this session).
- [x] clear-pages: f. 42r (blank) and f. 42v (endorsement only) checked; no decipherment.
- [x] known-keys: Lasry's fr. 3081 key (the Mâcon-embassy key) applied; the gramont1529 Mâcon key is a different sign set.
- [x] print: Tomokiyo francis.htm and Lasry GL.htm read; no printed reading of f. 41v found. Du Bellay correspondence and Pastor not searched.
- [x] key-rebuild: four signs re-valued from repeated words (Y, P, R, S).
- [x] retry: second pass on every doubtful place, regraded H/C/M/I (above).
- Next: find fr. 3081 on Gallica for ff. 40 and 43; check the 1534 conclave in Pastor for Campeggio's articles.
