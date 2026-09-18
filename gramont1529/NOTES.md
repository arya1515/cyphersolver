# Gramont, Mâcon and Langeac to Montmorency, 1529-1537 (catalogue item 6)

BnF fr. 3091 no. 23; fr. 3071 nos. 4, 7; fr. 3083 no. 8. Session of 18 Sept 2026.

## Verify-first answer: four letters, four keys, all broken by Lasry in 2023

The catalogue guessed "three hands, probably three keys". In fact each letter has its own key, and all four
keys were reconstructed by George Lasry in 2023 (tables dated 05/11/2023 on Tomokiyo's page
cryptiana.web.fc2.com/code/GL.htm, copies in `img/`). Tomokiyo's own page (code/francis.htm) has partial tables
for three of them from sister letters. **Neither site gives any plaintext** ("only the decipherment keys are
displayed"), so the task here was reading the letters, not breaking the ciphers.

| item | Gallica | leaf / canvas | writer, place, date | key (Lasry name) | cipher extent |
|---|---|---|---|---|---|
| fr. 3083 no. 8 | btv1b90601328 | f. 20-21, c35-36 | Jean de Langeac, bp of Avranches, Venice, 14 Jan [1529] | "Avranches' cipher 1" (= Tomokiyo fr. 3005 f. 107) | 11 lines |
| fr. 3071 no. 7 | btv1b9060315f | f. 17, c30 | Gabriel de Gramont, cardinal, Rome, 21 July [1530] | "Gramont's cipher (1530)" (= fr. 3019 f. 20, fr. 3040 ff. 12, 18) | 14 lines |
| fr. 3091 no. 23 | btv1b9060253s | ff. 45r-47v, c49-52 | Gramont, bp of Tarbes, Rome, 11 Oct [1529] | "Gramont's cipher (1529)" (= fr. 3040 f. 16, Clair. 330 f. 53) | ~175 lines, wholly cipher |
| fr. 3071 no. 4 | btv1b9060315f | ff. 9-10, c16-19 | Charles Hémard de Denonville, cardinal de Mâcon, Rome, 11 Apr 1537 | "Mascon's cipher" (= fr. 3053) | ~45 lines mixed |

The catalogue's ark "btv1b9060315f" is fr. 3071 and "btv1b90601328" is fr. 3083; fr. 3091 is btv1b9060253s
(the Raince volume). fr. 3091 is filmed as two-page openings, so canvas numbers do not follow folios.

## Results

* `fr3083_no8_langeac.md`: read in full apart from two short groups. Saint-Pol asks Langeac to seek his
  leave (congé) from the Signoria; Venice refuses and protests it would ruin the enterprises (Milan, Spanish
  money arriving, spring coming); Langeac has written to dissuade him. January 1529, five months before
  Landriano.
* `fr3071_no7_gramont.md`: ~85 % read. Dated by content to 21 July 1530. The Pope keeps "Francisque" on
  the mission rather than Gramont, for fear of Imperial suspicion; Rodolfo Pio, bishop of Faenza and nephew of
  Carpi, is to leave in 3-4 days to congratulate the King on the return of the Queen and the princes.
  Three of Lasry's "unknown" signs identified: 8Δ = PAPE, key-ring sign = ROY, ʃʃ-on-stem null.
* `fr3091_no23_gramont.md`: **read in full**. The letter runs to 171 cipher lines (ff. 45r-47v), each page 90-95 %
  confident, with per-page line tables in `f45r_transcription.md` … `f47v_transcription.md`. Year 1529 fixed by
  Clement VII's departure from Rome for Bologna, the bull of the four décimes, and Orange before Florence. Gramont
  vouches for the Pope's secret alignment with France. Clement dreads the general council and plans to grant it in
  principle and then stall it; he offers to feign illness on the road to wait for the Admiral Chabot; he fears
  soothsayers who foretell his deposition or death "du costé de" the Emperor, and had a dream before leaving Rome
  (enclosed). Orange is dealing to restore the Medici in Florence against Pisa and Livorno going to the Emperor.
  Code signs: heart = the King; several unlisted signs = the Emperor, the Florentines, the Pope/Medici (from
  context). `#` is A as often as M; the ♀-on-foot sign is a null.
* `fr3071_no4_macon.md` (+ `macon_key.md`, `macon_9r_26-34.md`, `macon_9v.md`): **read**, apart from two short
  spots on f. 9r and loosely read clear text. Codes 20 = Empereur, 30 = pape, 40 = roy (not in the published tables).
  The Farnese marriage offer (Vittoria Farnese to Cosimo de' Medici) and Paul III's threat, relayed through Latino
  Giovenale, to declare for the Emperor if it is refused; Pier Luigi Farnese and Novara; the King's Turkish alliance
  "se verifie clerement"; Venice expected to follow the Pope; the King "s'amuse en Picardie". The Venice ambassadors
  are trying to win over Alessandro Vitelli. **The slip f. 9bis is a contemporary decipherment of the f. 9v
  passage**, and our reading, made first, matches it.

Summary: all four items are now read (Langeac and Gramont 1529 in full, Gramont 1530 ~85 %, Mâcon ~90 % of the
cipher). No new cryptanalysis was needed. Three code signs of Lasry's "unknown" rows and three Mâcon code numbers
are identified.

Prior art still to look at: B. Wirtz-Daviau's edition of Chabot's 1529 embassy (may quote Gramont's letters
from a contemporary decipherment).

## Tools

`thumbs.py` (Gallica thumbnails), `sheet.py` (contact sheet), `full.py` (full-res canvases, 8 s spacing,
back-off on 429), `crop.py` (fractional crop + autocontrast), `decode.py` (Gramont 1529 alias decoder; `python decode.py < aliases/f45r.txt`), `macon_decode.py`
(Mâcon decoder, aliases in `macon_key.md`). `aliases/` holds every page's glyph transcription (f46r uses a few
extra alias characters of its own, explained in `f46r_transcription.md`).
Raw images in `full/` are not tracked.
