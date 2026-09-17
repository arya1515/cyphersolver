# Nicolas Raince, Rome, 1526 and 1529 (BnF fr. 2984, fr. 3040, fr. 3091)

Catalogue item 5 (the "gamble" of the five-item goal list). Session of 17 September 2026.
Everything below is unvalidated until Daniel reviews it; the evidence for each claim is named.

## Outcome in one paragraph

The item was never a blind-solving problem. Tomokiyo published the 1526 key in 2020 and the 1529
key with it; DECODE holds two Raince letters as decrypted; the one letter "entirely in cipher"
(9 June 1526) has its contemporary clear duplicate eight leaves earlier in the same volume, as
Mignet noted in 1886; and Bourrilly printed the cipher passages of the 17 June and 20 August
letters in 1901. What has never been read anywhere found is most of the **13 May 1526** letter
(about 85 lines of cipher on ff. 29r–31r) and the lower two thirds of the **20 November 1526**
letter (f. 105r). Both are in Tomokiyo's 1526 key, which this session verified on the leaf
against the clear text. A machine transcription of the unread 106 lines (5,629 glyph tokens,
connected-component segmentation and shape clustering on the Gallica microfilm) decoded with the
key reads in stretches ("pour perdre ... occasion", "qui estoit en la court de Savoye ... est
party pour venir icy", "vous faire tous services et plaisirs", "son royaume", "trois fois",
"vray monseigneur") but carries roughly a fifth of noise from fragments and merged glyphs, and
the blind sp53/fasthomo pipeline run on the same token stream collapsed into a degenerate map.
A clean reading needs a glyph-level hand transcription (a few hours) or better images than the
microfilm; the key and the tools for it are in this folder.

## Prior art (checked 17 Sept 2026)

* **Tomokiyo, "French Ciphers during the Reign of Francis I"**
  (cryptiana.web.fc2.com/code/francis.htm, first posted 2 Nov 2020, last modified 7 Dec 2023),
  section "BnF fr.2984 (1526)": key published as `francisRaince.png` (copy in `img/`).
  Monoalphabetic substitution with homophones for a (4), e (3), i (4), o (2), r (3), u/v (4);
  three nulls (λ, "ny", K); three word-signs: *con*, *l'empereur*, *le pape*. The same key
  serves fr. 3040 f. 21 (Raince to Montmorency, 7 Nov 1526). Section "Raince's Cipher (1529)":
  a second key for fr. 3091 f. 19 (12 Aug 1529), `francis_Raince1529.png`, with 16 word-signs
  (aux, bien, des, dit, de, en, et, il/je, la, le, les, leur, luy, pour, par, que). Tomokiyo
  credits Desenclos (HistoCrypt 2018) with locating the letters. He gives no plaintext.
* **DECODE** (de-crypt.org): records 4228 (fr. 3040 f. 21, 1526, "Decrypted", plaintext
  attached) and 3696 (fr. 3091 f. 19, 1529, "Decrypted", transcription and plaintext attached),
  both uploaded by user lehoanna 2022–23. Nothing from fr. 2984 is in DECODE.
* **Mignet, *Rivalité de François Ier et de Charles-Quint*, 2nd ed. 1886, t. II p. 211 n. 1**
  (archive.org `rivalitdefranois02mign`): "Lettre de Nicolas Raince à François Ier, écrite de
  Rome le 9 juin 1526 ... Mss. Béthune, vol. 8509 [= fr. 2984], l'original en chiffres f. 33,
  **le déchiffrement f. 17**." So no. 8 (ff. 33–37, wholly in cipher) has its contemporary clear
  duplicate at no. 5 (f. 17 ff., "Double de lettres ... des neufme et XIe juin"). Verified on
  the image: f. 17r begins "Sire, depuis les depesches envoyées du ... et une de moy ... adressée
  à monseigneur le grant maistre ... le comte de Venise ... le pape a depesché messire Francisque
  Guichardin, president de la Romaigne, qui partit vendredy matin pour commissaire general sur le
  faict de la guerre", and the same words are glossed above the first lines of f. 33r.
  Mignet also quotes the 12 June and 30 Jan 1527 letters (pp. 213–214, 272).
* **Bourrilly, "La première défection de Clément VII à la ligue de Cognac (août–septembre
  1526)", *Bulletin italien* 1 (1901) pp. 213–229** (archive.org `bulletinitalien01borduoft`):
  appendix II prints "simplement les parties chiffrées et qui n'avaient pas été déchiffrées
  encore" of the **17 June 1526** letter to the King (ff. 41–43, no. 10) and of the **20 August
  1526** letter to Montmorency (ff. 47–50, no. 11). He read them himself in 1901 (the
  interlinear decipherment on f. 41 is contemporary and partial). He also cites the 1, 20 and 27
  Aug letters and the Carpi letters of the volume.
* **Grethen, *Die politischen Beziehungen Clemens VII. zu Karl V.* (1887) pp. 108–115** used the
  9 and 17 June reports (per Pastor, *History of the Popes* IX pp. 308–311, notes). Not online
  in full text; not checked.
* **Pastor IX appendix XXXVIII** prints one Raince letter to Montmorency (1526). Not seen.
* Friedmann's cipher keys (NAF 4206) do not include Raince (Tomokiyo, "Further sources").

## The ciphered letters on the image

Gallica ark btv1b90598430 is a black-and-white microfilm of fr. 2984, 85 openings, all canvases
labelled "NP". Canvas n shows the opening whose recto is foliated 2n−3 (checked on ff. 17, 23,
25, 27, 29, 31, 33, 35, 37, 39, 41, 103, 105, 119, 121, 123); each canvas is 7,984 × 5,525 px
via `/full/full/0/native.jpg`.

| no. | folio | date 1526 | to | cipher on the leaf | read where |
|---|---|---|---|---|---|
| 6 | 25 | 1 Aug | Montmorency | last 7 lines of f. 25r | contemporary interlinear decipherment on the leaf |
| 7 | 29–31 | 13 May | Montmorency | f. 29r whole (36 lines), f. 30v whole (35), f. 31r upper half (25); clear close | later gloss on lines 1–c. 13 of f. 29r only; **rest unread anywhere found** |
| 8 | 33–37 | 9 June | the King | whole letter, 9 pages | clear duplicate f. 17 ff. (Mignet 1886); gloss on f. 33r top |
| 10 | 41–46 | 17 June | the King | most of the letter | interlinear decipherment; cipher parts printed by Bourrilly 1901 |
| 11 | 47–50 | 20 Aug | Montmorency | parts | cipher parts printed by Bourrilly 1901 |
| 24 | 105 | 20 Nov | Montmorency | 40 lines after 4 clear lines | gloss on the first c. 12 lines; **lower 21–28 lines unread anywhere found** |
| 28 | 121–123 | 7 Dec | Montmorency | c. 18 lines on f. 123r | dense interlinear decipherment on the leaf |
| fr. 3091 no. 11 | 19 | 12 Aug 1529 | Montmorency | — | DECODE 3696 decrypted; Tomokiyo's 1529 key |

Token count of the unread residue: 106 lines of about 50 glyphs, 5,629 segmented tokens.

## Key check on the leaf (the "control")

* f. 33r line 1 against f. 17r line 1 ("Sire depuis les depesches envoyées"): with ∧ = s,
  ✕✕ = i, ρ (o with a straight tail) = d, ψ / 7 / ⊥o = e, T = p, Ƶ = u, I = i, ⊡ = c, ε = h,
  "ny" / K / λ nulls, the glyphs read s-i-[ny]-r-e, d-e-p-u-i-s, [ny]-l-e-s,
  d-e-p-[λ]-e-s-c-h-e-s, [K]. Crops `img/f33r_a.png`, `img/f17r_top.png`.
* f. 29r line 1–2 (gloss "monseigneur ... je vous ay dernierement ... depesche du ... de ce
  moys"): m-[ny]-o-n-s-e-i-[K]-g-n-e-[λ]-u-r; [ny]-i-e; v-o-u-s (v = the R-shaped u variant);
  a-y; d-e-r-n-i-e-r-[K]-e-m-e-n-t; e-p-e-s-c-h-e (depesche); d-u; q-u-a-t-r-i-e-s-[ny]-m-e
  (*quatriesme*; q is the "ni"-shaped glyph, m the s-shaped one); d-e-c-e-m-o-y-s (*de ce moys*).
  Crops `img/L1_0.png` … `L1_2.png`.
* Two corrections to read Tomokiyo's table on this microfilm: the glyph he draws as a barred b
  (third e) appears here as a small circle at the base of a stem with a bar on top (the most
  frequent single glyph, 188 of 5,629 tokens), and the E-shaped glyph he lists under x reads y
  in *moys*, *Savoye*, *voye*, *icy*; ω is also y. The 4-like glyph is r as in his table; the
  "-o" and H shapes are its variants.

## Machine transcription of the unread residue (`seg2.py`)

Connected components on a background-normalised binarisation (threshold bg − 45, ≥ 60 px,
height ≥ 14, mean darkness ≥ 55, which drops most verso show-through and the fainter gloss ink),
assigned to text lines by a y-histogram (pitch 104–112 px), x-overlapping components merged
(dots, broken strokes), then Ward clustering of 24 × 24 shape rasters plus baseline geometry
into 70 clusters (`raince_tokens.json`, `raince_cipher.txt`, cluster sheets `img/raince_sheet_*`)
and into 140 (`raince140_*`). Regions: f. 29r lines 11–36 (c16 right, y 0.230–0.746), f. 30v
whole (c17 left), f. 31r cipher part (c17 right, y 0.03–0.535), f. 105r lower part (c54 right,
y 0.345–0.80). Lines 1–c. 13 of f. 29r and 1–12 of f. 105r carry a gloss that the darkness
filter does not separate cleanly, so they were left out; their content is in the gloss anyway.

Cluster labelling by eye against the key (`handmap.json`): 45 of 70 clusters are clean single
glyphs (a, b, c, d, e, f, g, h, i, l, m, n, o, p, q, r, s, t, u/v, y, nulls); 25 clusters,
holding 12.6 % of tokens, are fragments, merged pairs, or the three word-signs mixed together.
The decode (`hand_decode2.txt`, `draft3.txt` with uncertain clusters in capitals) reads in
stretches, for instance (f. 29r, lines 11 ff., cluster errors left as they are):

    ... etgauictegsiviepoUrperdreIabeSIeoccasionIqUiLavoi ...   pour perdre [la be]lle occasion [qu'il] avoi[t]
    ... acestefinetq..dy.nevo...                                à ceste fin et qu'il y ne vo...
    squiestoiterIacoUrtdesavoyesestpartypourvenirScy           ...s qui estoit en la court de Savoye s'est party pour venir icy
    egcoreseg?eeautreschosesbiendong                            encores en ... autres choses bien don[né]
    ?onseig?uracddie?d?et?acharge?ousfairecto?s                 monseigneur ... et la charge ... vous faire tous
    ctiotevahousfairetoussnruiceset?daisirs (f. 30v l. 1)        ... vous faire tous services et plaisirs
    oeretoeensonuu?royaumeetmeeapnrdep?usinursfois              ... en son royaume et me ... plusieurs fois
    u?iutroisfoisquiau?e?eniera?rome                            ... trois fois qui ... venir à Rome
    c?eaisantpeenaretoutpoue?emieud??bienest?vraymonsei/gneur   ... prenant tout pour le mieulx ... bien est vray monseigneur
    aayeregsqu?enseraperpetue?ememoire                          ... en sera perpetuelle memoire
    tasdn?trespropey??ainsdevertetmensong                       ... nostre propre ... ains de ... et mensonges

f. 31r and f. 105r decode worse (the f. 31r hand is more compressed and the f. 105r region is
another day's ink); their draft lines are in the same files. The French 5-gram score of the
hand-map decode is −4.1 per letter (clean French −1.4 to −1.7), which measures the segmentation
noise, not the key.

**Blind pipeline.** `sp53/fasthomo.py` (French, 10 M moves, 7 × 3 restarts) on the 70- and
140-cluster streams reached −3.08 to −3.4 per letter but with a degenerate map (almost every
cluster to e, n, i, s, t; `blind140_render.txt`), which outscores the true key on this stream:
so on a token stream with about 20 % segmentation noise the LM-only solver is not a usable
reader, and the greedy coordinate descent from the hand map (`greedy70map.json`) only relabels
the junk clusters. The hand map from Tomokiyo's key is the reading; the solver result is a
negative control on the transcription quality, not on the cipher.

## What would finish it

1. A glyph-level hand transcription of the 106 lines at 2–3× zoom with the key at hand (the
   `band_*` crops are generated by the last block of `draft3` in `seg2.py`'s companion code;
   about 75 three-line crops), correcting the machine draft word by word. Two to four hours.
2. Or better images: the BnF has no colour digitisation of fr. 2984 online (the Gallica item is
   the microfilm); a reader's photograph of ff. 29–31 and 105 would let the segmentation run
   clean.
3. The word-signs *con*, *l'empereur*, *le pape* occur in the residue (L-shaped, C-with-loop and
   y-shaped glyphs in clusters 13, 40, 43) and need to be tagged by hand.
4. Registration in DECODE of the eight fr. 2984 letters (none is there) is Daniel's step, with
   the key image credited to Tomokiyo.

## Hand-transcription progress

The committed `trans/` files are a partial hand review, not a finished reading. `f29r.txt` covers lines 1–25 of the machine-draft region (manuscript lines 11–35); the four `*_gloss_*.txt` files record the faint contemporary glosses on f. 29r and f. 105r. Unread stretches remain marked with `?` or `[...]`; no uncertain wording is silently promoted to plaintext. `CALIBRATION.md` records the glyph distinctions and the worked f. 29r line-20 control used to make the partial reading reproducible. `score_trans.py` reports coverage and a French 6-gram score; its output is not directly comparable with the older 5-gram figure above.

## Files

`NOTES.md`; `CALIBRATION.md`; `bands.py`, `bands_gloss.py`, and `score_trans.py`; the
partial readings in `trans/`; `seg2.py` (segmentation + clustering, regions hard-coded),
`render.py` (solver map to lines); `raince_tokens.json`, `raince_cipher.txt` (70 clusters),
`raince140_tokens.json`, `raince140_cipher.txt`, `raince140n_cipher.txt` (nulls removed),
`hinit140.txt` (warm start), `handmap.json` (cluster → letter from the key),
`greedy70map.json`, `hand_decode2.txt`, `draft3.txt`, `blind140_render.txt`; `img/` holds
Tomokiyo's two key images, the key-check crops and the 70-cluster montage sheets. The page
images (`img/c*.jpg`, 23 MB, canvases 10–28, 53–54, 61–63 at 1600 px and full size) are kept
locally and not tracked; re-fetch with
`https://gallica.bnf.fr/iiif/ark:/12148/btv1b90598430/f<n>/full/full/0/native.jpg`.
The `bands_gloss.py` source images are the local `f2984/c16_full.jpg` and `c54_full.jpg`
canvases and are likewise not tracked. Solver outputs are in
`sp53/par_raince*_*.txt`, `sp53/parw_raince140n_warm_*.txt`.
