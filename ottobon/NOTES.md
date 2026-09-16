# Marco Ottobon to Giovanni Mocenigo, 27 April 1589 (BNE Mss/994 ff. 34–38) — NOTES

**Verdict: blocked at the images, not attempted cryptanalytically.** The manuscript is digitised in full by the
Biblioteca Nacional de España (BDH record bdh0000174344, now BNE Digital oid 0000174344) and the letter is also
DECODE record R2252, nine openings. Neither image set can be reached by a script from this network: every bne.es host
that serves images sits behind a Cloudflare Turnstile check that curl, WebFetch and Playwright-driven Chromium, Chrome
and Edge (headless and headful) all fail, and the DECODE files need a login. A browser session by a person gets either
in minutes ([GET_IMAGES.md](GET_IMAGES.md)). What was established without the images is below, and the attack is
prepared so that the transcription can start the day the folios are in hand.

Session 2026-09-16.

## 1. What the item is

Tomokiyo, *Unsolved Historical Ciphers*, "Venetian Letter in Spanish Archives (ca.1589)": "Ms. 994 of National
Library, Madrid, contains an undeciphered letter from Venetian secretary Marco Otthobon to ambassador Juan Mocenigo,
dated 27 April 1589. Valle de la Cerda appears to have solved it, but his solution is lost. … The cipher symbols
consist of an alphabetical letter followed by Arabic figures." His Valle de la Cerda article adds that Catalina, Duchess
of Savoy, gave the letter to Valle at Turin on the Duke's orders, and cites Carnicer and Marcos p. 245 and Navarro
Bonilla et al. (2015) p. 115.

The printed catalogue (*Inventario general de manuscritos de la Biblioteca Nacional*, III (897–1100), Madrid 1957,
pp. 214–216; PDF at bne.es, `invgenmss03.pdf`) describes Mss/994, *Cartas orij. en cifra*, 191 folios, as Valle de la
Cerda's own dossier of his services as *Secretario de la Cifra*, and gives item 5 as:

> Carta en cifra de Venecia que dio en Turin la Señora Infanta Doña Catalina por orden del Duque de Saboya a Luis
> Valle de la Cerda que declaro y no tiene contracifra ni declaración por hauerse perdido. [La carta es del secretario
> Marco Otthobon al Embajador Juan Mocenigo, 27 abril 1589. Firma autógrafa] (fol. 34).

Item 6 begins at fol. 64 and fol. 39 is listed blank, so the letter is ff. 34–38; the volume's foliation runs ahead of
the image count because fols. 10–12, 14–21, 40–57, 61–63, 73–82 and 160–176 are missing (torn out by Tiran in 1842 for
the Affaires étrangères, or lost). The same volume holds Valle's other trophies: Alençon's letters with the
reconstructed alphabet (fol. 5), Rogers to Nicles 1585 (fol. 26), Longlée's letters (fol. 64), Sertori's cipher
(fol. 83), the Princess of Ascoli's booklet (fol. 92), Philip III's test cipher of 1599 (fol. 103), the *cifra de los
secretos de las minas* (fol. 113) and a hundred-year-old cipher (fol. 186).

The record on Europeana (`/2022717/bnesearch_detalle_bdh0000174344`) carries the BDH metadata: *Memorial de los
servicios prestados a los Reyes Felipe II y Felipe III por D. Luis Valle de la Zerda, correspondencia y documentos del
mismo*, "Originales y copias", "Varias h. en blanco", olim Mss/18724/5/1.

### The people

- **Giovanni Mocenigo** was the Republic's ambassador to Henry III, at Tours with the King in March–April 1589 (his
  dispatches of 14 March and 6 April 1589 are calendared in *CSP Venice* viii, nos. 823 and 825, both "Italian;
  deciphered"), and stayed on with Henry IV; Bonavoglia (2019, n. 22) records that in June 1595 the Council of Ten
  recommended Partenio's cipher after learning from Mocenigo, "the previous ambassador in France", that François Viète
  boasted he could read Venetian ciphers. Not the doge of that name (DBI 75).
- **Marco Ottobon** (Venice 1554 – 1649), *cittadino originario*, secretary of the Senate from 1584, on missions
  1588–97, later secretary of the Ten and *cancellier grande* in 1639 (A. Menniti Ippolito, DBI 79, 2013). Venetian
  Senate letters to ambassadors were subscribed by a secretary of the Senate, so a letter "from the secretary Marco
  Otthobon to the ambassador" with Ottobon's autograph signature is most likely a **Senate dispatch to the embassy in
  France**, whose register copy would be in ASVe, Senato, Deliberazioni Secreta, for April 1589.* The alternative is a
  private letter from a secretary on mission. The Venice–Paris courier road crossed Savoy, which is how it came to
  Turin and to Valle.

\* Inference from chancery practice, not verified against the register; the register, if it holds the letter, is a
complete crib and turns the problem into key reconstruction.

## 2. What the pages look like

DECODE R2252, "BNE_ms.994_LuisValledelaZerda_5_34r_63v", symbol sets *Alphabet, Numerical*, origin Venice, 9 images,
status N/A, cleartext language given as Latin (probably an error for Italian). The nine 200-px thumbnails are public
([decode/](decode/), montage in `decode/montage.png`):

| image | left page | right page |
|---|---|---|
| 1 | f. 33v blank | f. 34r: Valle's cartouche heading and a ten-line description in clear |
| 2 | f. 34v blank | f. 35r: cipher, full page, ~25 lines |
| 3 | f. 35v: cipher, full | f. 36r: cipher, full |
| 4 | f. 36v: cipher, full | f. 37r: cipher, full |
| 5 | f. 37v: cipher, full | f. 38r: cipher, half page, signature block, seal |
| 6 | f. 38v: address side (a few lines) | f. 39r blank |
| 7–9 | blank openings | |

So the ciphertext is about six and a half pages of dense script, on the order of 150 lines. At the density of
Bonavoglia's specimens (15–25 letter-plus-figure groups per line) that is 2,500–4,000 tokens, more than five times the
Ségur letters and the longest Venetian text on any of the lists. Length is what decided Ségur, Lucca and Warsaw.

## 3. Access: everything tried

| route | result |
|---|---|
| `bdh.bne.es/bnesearch/…`, `bdh-rd.bne.es/viewer.vm`, `pdf.raw`, `high.raw`, `low.raw` | all 308 to `bnedigital.bne.es/bd/card?oid=0000174344&site=bdh` (server: cloudflare) |
| `bnedigital.bne.es/bd/card`, `/bd/medium`, `/bd/viewer`, `/iiif/…` with Chrome headers, es-ES | HTTP 403, 1.3 MB Cloudflare "Un momento…" page with a Turnstile widget |
| WebFetch of the same | 403 |
| Playwright: bundled Chromium headless; Edge headless; Edge headful | Turnstile never clears in 60 s, title stays "Un momento…" |
| Wayback Machine CDX for object 174344 | captures exist only of page 1 (`pdf.raw … page=1`, 2024 and 2025, the binding) and `low.raw` pages 1–5 (2025-07-28); nothing of ff. 34–38 |
| Europeana record | metadata only; `edmIsShownBy` absent |
| Hispana, datos.bne.es, catalogo.bne.es, archive.org search | metadata or nothing |
| DECODE R2252 | RecordsView public; `IMG_R2252_I160NN_PM.png` without login returns a 986×568 "Insufficient permissions to see the full image" placeholder; thumbnails `TH_IMG_…` 200 px |
| Google Books / print | the letter is not reproduced in Carnicer and Marcos (2005) or Navarro Bonilla (2015) as far as their online descriptions show; Lohmann Villena 1954 concerns item 11 |

Not tried, by policy: registering a DECODE account, or any method that pretends the client is not a script. Daniel's
browser session is the way in, and it is quick.

## 4. What the cipher family is, and what to expect

Tomokiyo files the letter with the **Venetian ciphers with superscripts**: a base letter followed by one or two
figures, often written as exponents, for letters, syllables and words. The Council of Ten's cipher book of 1578–87
(ASVe, CX, Cifre, chiavi e scontri di cifra, b. 4, r. 16) holds the *zifra granda* used by ambassadors in European
capitals, described by Bonavoglia (HistoCrypt 2019, §4, Figs. 1–2):

- an alphabet with three homophones per letter (a polywog sign, a turned-T sign and *u* with a figure; his example for
  A is o18 t8 u15);
- an abacus for the ten digits;
- a **syllabary of 27 consonant rows × 5 vowels** whose figures end in 1 2 3 4 5 for -a -e -i -o -u, the base letters
  being f, r and a: ba–bu = f1–f5, ca–cu = f11–f15, da–du = r1–r5, pa–pu = a1–a5, ta–tu = a41–a45 and so on
  (transcribed from his Fig. 2 into [refs/zifra_granda_syllabary.json](refs/zifra_granda_syllabary.json));
- a dictionary of some 500 words (L54 = *Guerra*).

Two years before the letter, on 26 August 1587, the Ten approved Franceschi's ciphers; the *Ziffra N.11* of 1587 (same
book, c. 74) encodes single letters as base letter a/c/d/f/g/h plus 1–20 with a modulo-20 structure (Bonavoglia 2022,
Fig. 7–8; Tomokiyo's table). Bonavoglia's overview (Cryptologia 46, 2021) says the letter-plus-two-figure design was in
use for almost a century, so the 1589 letter may use the zifra granda itself, a re-keyed table on the same plan, or the
1587 generation. Tomokiyo notes there is no evidence either way. Valle read it in 1589 without a key.

Consequences for the attack:

1. **The vowel-slot test decides the design in a minute.** If the figures' last digit is confined to 1–5 within a
   base letter and the mod-5 histogram is far from flat, the syllabary is on the zifra granda plan, and the annealer
   from `segur/` (structured syllabary with vowel slots, clear-text context) applies directly; that solver read a
   97 % control at 460 tokens and here there would be 2,500+.
2. **A direct key-reuse test** against the 1578–87 syllabary: fraction of tokens that are table entries, and the
   Italian 5-gram score of the resulting syllable string against random relabellings ([structure.py](structure.py)).
   If the key is the zifra granda, the letter reads at once, apart from the word list, which the text's own repeats
   will gloss.
3. If neither, it is a homophonic nomenclator with letters, syllables and words mixed; at 2,500–4,000 tokens the
   Lucca/Warsaw 5-gram-plus-dictionary annealer has more than ten times the text it needed, and the Ségur mod-5
   machinery covers any regular syllabary. Repeated formulae (*Serenissimo Principe*, *Vostra Serenità*, *Illustrissimo
   Signor Ambasciatore*, the dateline) are cribs. The crib to look for first: the Senate register copy in ASVe, or
   the calendared substance of Mocenigo's April–May 1589 dispatches (*CSP Venice* viii, nos. 823–828) for the
   subject matter (Henry III at Tours, the treaty with Navarre of 3 April, the levy in Germany, England's fleet).

## 5. Plan once the images are in hand

1. `python render.py ms994_full.pdf` (or `--decode`), then `--crop` each page into strips at 2×.
2. Glyph-level transcription into `ct.txt` with the grammar in [parse.py](parse.py): base letter, figure, whether the
   figure is superscript or inline, one- vs two-digit figures written where two would fit, capitals, the polywog and
   turned-T signs, clear-text words, line ends. Record divergences and doubtful glyphs in `ct2.txt`, as the Birago
   experience requires (his transcriptions normalise marks; here there is none to trust, which is better).
3. `python structure.py ct.txt`: profiles, IC, vowel-slot test per base letter, zifra granda key-reuse test, repeats.
4. Branch on the result as in §4; controls first (a matched synthetic text enciphered with the zifra granda plan and
   with a random nomenclator of the same size), then the target; write up only when the control reads and the target
   either reads or provably does not.

## 6. Files

- `GET_IMAGES.md` — the browser step, both routes, with the file names to save under.
- `parse.py`, `structure.py`, `render.py` — token grammar, structural tests, page rendering and cropping.
- `refs/zifra_granda_syllabary.json` — Bonavoglia 2019 Fig. 2 transcribed; `refs/zifra_granda_fig2.png` — the figure
  (ASVe b. 4 r. 16, reproduced by Bonavoglia "for no profit use only").
- `decode/th_R2252_P1-9.png`, `decode/montage.png` — the public DECODE thumbnails.
- `refs/` does not keep the Bonavoglia PDFs: HistoCrypt 2019 (ep.liu.se/ecp/158/001/ecp19158001.pdf) and 2022
  (ecp.ep.liu.se/index.php/histocrypt/article/download/410/369/312) are open access.

## Sources

- S. Tomokiyo, *Unsolved Historical Ciphers* (cryptiana.web.fc2.com/code/unsolved.htm), *Luis Valle de la Cerda*
  (valle.htm), *Venetian Ciphers with Superscripts* (venetian.htm, last modified 23 Oct 2025).
- *Inventario general de manuscritos de la Biblioteca Nacional*, III, 1957, pp. 214–216 (Mss/994).
- Europeana record 2022717/bnesearch_detalle_bdh0000174344; BNE Digital oid 0000174344.
- DECODE R1940 (biography of Valle, 7 pp.), R2248–R2262 (Mss/994 items 1–15), R2252 (this letter).
- P. Bonavoglia, "Hieronimo di Franceschi and Pietro Partenio: Two Unknown Venetian Cryptologists", HistoCrypt 2019,
  pp. 3–11; "The Enigma of Franceschi's Falso Scontro", HistoCrypt 2022; "The ciphers of the Republic of Venice: an
  overview", Cryptologia 46 (2022) 4.
- *CSP Venice* viii (1581–1591), ed. H. F. Brown, 1894, nos. 823–827 (British History Online).
- A. Menniti Ippolito, "Ottoboni, Marco", DBI 79 (2013).
- D. Navarro Bonilla et al., "Cryptanalysis Skills and Secret Information Practices under Two Monarchs: Secretary Luis
  Valle de la Cerda", in *Geheime Post* (2015); C. Carnicer and J. Marcos, *Espías de Felipe II* (2005) — cited through
  Tomokiyo, not seen.

Checked: catalogue entry, DECODE record and thumbnails, Europeana metadata, all listed access routes, Bonavoglia's
figures. Not checked: the page images themselves, the ASVe register, the 2005 and 2015 monographs. User must verify:
nothing here is a reading; the item stays open.
