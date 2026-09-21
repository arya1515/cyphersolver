# Toulon to Van Hogendorp, 30 July 1803 — DECODE R2034

Status: in progress (blocked on the physical key; 9 of 67 words fixed from same-key known plaintext).

## Source

- Ciphertext: DECODE R2034, Nationaal Archief, The Hague, 1.02.13 (Legatie Rusland), inventory 208.
- The authenticated DECODE image was acquired as `IMG_R2034_I14728_P1.png`; `R2034_upright.png` is the lossless upright rotation.
- Clear text: “Den Haag 30 July 1803”, “Burger Minister!”, and the closing “Heil en Hoogachting! L. van Toulon”.
- The numerical body is transcribed in `ciphertext.txt` (110 groups).

## Key identification

The exact key survives. Nationaal Archief 2.21.227, item 335, describes a *Correspondentiecijffer* annotated:

> eerst voor den minister van Grasveld in anno 1799, nu in anno 1801 voor den Minister van Dedem, met de Ministers der Bataafse Republiek te Parijs en in Spanje … voor den Minister van Hogendorp te Petersburg 1803

The same object is described in the Croiset family archive, Nationaal Archief 2.21.045, inventory 34313 (old number 5187): a ten-page booklet with six written pages, instructions, and six loose sheets of code notes. The physical original was deposited with the Nederlands Postmuseum / Museum voor Communicatie (registration B1 392); the Nationaal Archief holds a photocopy. The catalogue currently marks it **PHYSICAL**, with no online scans.

The six written codebook pages explain the six series in the letter: unmarked numbers and numbers marked by a wave, caret, double stroke, overbar, or plus. Values range from 1 to 992. This is therefore an ordered dictionary code: the mark identifies the codebook page/series and the number identifies an entry.

## Same-key traffic

DECODE R1942 is a two-page dispatch from Dirk van Hogendorp in St Petersburg to Maarten van der Goes, 5 July 1803 (NA 2.01.08, inventory 318). Its numerical groups use the identical six marks and range, so it is almost certainly traffic under item 34313. Its scans and prepared crops are in `../R1942/`. It supplies several hundred additional tokens for joint analysis.

DECODE R1944 (Etienne Bourdeaux, Berlin, 31 January 1801) is another strong candidate: its date and correspondents match the 1801 Dedem/Paris/Spain phase of item 34313, and DECODE notes that its nomenclator was probably devised by S. E. Croiset. Its two authenticated scans use the same six superposed marks as R2034.

More importantly, the immediately following Bourdeaux dispatches R1945 (3 February 1801) and R1946 (7 February 1801) are marked **decrypted** and include contemporary plaintext solution sheets. Their authenticated scans are now downloaded and rotated. They are same-key ciphertext/plaintext pairs for reconstructing item 34313. R1946 is now aligned across all 158 plaintext words, and R1944's misplaced solution is also aligned far enough to recover exact target entries. See `related_plaintext_pairs.md`.

The meaningful part of R2034 ends at group 69, `763~ = Einde des briefs`; groups 70–110 are deliberate random padding.  Directly verified target readings are currently:

`51~ = van` (groups 10, 39, and 62), `279 = en` (24),
`153 = Paul` (30), `222= = niet` (52), `43~ = zyne`
(53), `304~ = wegens` (58), and `380~ = de` (59).

These readings account for the start control which precedes the plaintext in
R1944–R1946.  Omitting that control shifts every apparent mapping by one and
produces false readings such as `51~ = men` and the impossible target sequence
“het Heer”; those provisional values have been withdrawn.

The target transcription was also corrected from `120` to `120~` after
reinspection of the authenticated image.

## Related but different key

DECODE R1891 is Croiset's small (under 500 entries) codebook for R. J.
Schimmelpenninck, Museum voor Communicatie inventory 34312. Its catalogue note
mentions later temporary reuse, but the photographed table cannot be R2034's
1–999, six-mark key. It remains a constructional analogue, not the target
table. R1925 is a decrypted 1799 letter using that related codebook; the
separate contemporary solution survives.

DECODE R1035, Nationaal Archief 1.02.13 inventory 228, is also **not** the target key. It is the much larger, seven-series codebook signed at The Hague on 5 August 1803, six days after R2034. Direct manuscript lookup was tested rather than inferred from metadata. It turns the opening groups into the disconnected sequence `ing | beh | hoe | voor | plus | ...`, and the following groups remain random Dutch/French dictionary entries. Several spot checks are unambiguous in the photographed number columns (for example `430~ = ing`, `336~ = beh`, `501 = hoe`, `1+ = voor`). This is a decisive negative control, not a partial reading. The apparent match `763~ = Einde des briefs` is a retained conventional control group shared by the related system; it does not make the vocabulary tables identical.

The R1035 instructions explain the random material before a `Begin des briefs` control and after an `Einde des briefs` control, but none of its six start controls (`404~`, `27"`, `847"`, `713^`, `325`, `17+`) occurs in R2034. That independently rules out R1035 for this letter.

## Prior-art checks

- Exact-name and exact-date web searches found no published decipherment.
- Searches of Satoshi Tomokiyo's Cryptiana index/domain found no Toulon, Hogendorp, or Batavian match.
- The printed 1943 *Correspondentie van Dirk van Hogendorp met zijn broeder Gijsbert Karel* concerns his brother and does not surface this official letter.
- J. A. Sillem's 1890 biography identifies several numbered ciphered dispatches by Hogendorp, but contains no 30 July letter from Toulon and no decipherment of R2034.
- Florentijn van Kampen's HistoCrypt 2026 reconstruction and repository concern the later inventory-228 codebook and its 1806-1810 traffic. They were checked in full and provide the decisive ruled-out comparison above, not the plaintext of R2034.

## Present result and next attack

R2034 is now securely transcribed and its key is identified archivally, but the plaintext is **not yet read**. A claimed plaintext based on R1035 would be false. The physical key remains offline, but the discovery of R1945 and R1946 provides a new recovery route from same-key known plaintext.

DECODE's authenticated record API adds a useful subject constraint: its
cataloguer notes that a private letter sent by the cipher clerk in his own
name is highly unusual and that the short message "can only pertain to matters
of encryption."  This also fits the replacement St Petersburg nomenclator
dated 5 August 1803, six days after this letter, but it is not itself a
plaintext recovery.

### Ruled-out digitized-key candidates

- DECODE's catalogue contains only three plausibly relevant Dutch key records for this period: R1891 (the much smaller 1798 Schimmelpenninck key), R1035 (the replacement St Petersburg nomenclator signed 5 August 1803), and R1038 (a 1765 St Petersburg nomenclator). There is no separate hidden catalogue entry for Croiset item 34313 / old number 5187. DECODE R5187 is an unrelated 1640--1669 Uppsala key.
- The complete downloadable R1038 transcription was tested against the seven secure R2034 anchors. It is not a reused assignment table: no R1038 variant of numeric base `51` means *van*, whereas the 1801 same-key solution fixes `51~ = van`. Other anchors also disagree (for example R1038's base-380 variants include *van* and *de Keizer*, not the exact target assignment `380~ = de`). R1038 is therefore useful only as a structural analogue, not as a decoding source.
- Web searches for the old inventory number `5187`, current Croiset inventory `34313`, the title *Correspondentie Cijffer*, and museum loan number `B1 392` found only the two official Nationaal Archief descriptions. Neither surviving copy has online scans.
- DECODE R1891 is indeed the immediately preceding museum item 34312, but its four image IDs are followed directly by the two images of unrelated R1892; there is no unattached 34313 scan hidden in that upload sequence. DECODE record R5187 is likewise unrelated (a 1640--1669 Uppsala key).
- DECODE R1943 (Valckenaer, 1799) has a surviving French plaintext and was
  tested as another possible known-plaintext source.  It is a different
  assignment table: repetition in its solution independently fixes its
  `907^` group as *sera*, whereas the exact 1803 R1942 quotation fixes the
  target table's `907^` as *zoo*.  Numerical and mark similarity therefore
  reflects the shared Croiset construction, not reuse of the same key.

### Additional same-key quotation recovery

Sillem's biography explicitly cites R1942, dispatch no. 12 of 5 July 1803, for the passage in which Hogendorp calls Vorontsov's attitude *zoo wonderlijk*. The R1942 ciphertext contains the unique adjacent pair `907^ 934"` at that point. This gives high-confidence (not clerk-solution-level) assignments `907^ = zoo` and `934" = wonderlijk`. They fill R2034 plaintext words 50 and 18 respectively.

1. Transcribe and align the contemporary plaintext/ciphertext pairs R1945 and R1946, then apply every recovered group directly to R2034.
2. Finish and independently verify transcriptions of R1942 and R1944 for additional repeated groups.
3. Test all 720 possible orders of the six marked pages under the assumption that the vocabulary is alphabetically ordered.
4. Solve the resulting monotone word-substitution problem jointly across the messages with an early-19th-century Dutch word/phrase language model.
5. If known plaintext and statistics still leave gaps, request digitization of NA 2.21.045/34313 (or 2.21.227/335 / Museum B1 392); the surviving key would make the reading mechanical.

## Files produced in this pass

- `transcription.txt`: 110 code groups with all six superscript marks and the one grammatical trailing dash.
- `R2034_upright.png` and `cipher_crop_2x.png`: inspection derivatives of the authenticated DECODE image.
- `decode_r2034.py` / `decoded_tokens.json`: partial-codebook comparison harness and output.
- `extract_key_cells.py` / `key_context_line*.jpg`: reproducible manuscript lookups used to reject R1035.
- `prepare_related_images.py` / `R1944_*`, `R1945_*`, and `R1946_*`: upright derivatives of authenticated same-key traffic and plaintext sheets.
- `related_plaintext_pairs.md`: provisional transcription and group alignment from the newly found known-plaintext records.

## Session of 21 September 2026: same-key known plaintext exhausted

- **R1945 read in full** (`R1945_transcription.txt`): 187 groups against a 152-word contemporary solution. The opening
  is `871` (start control) `914+ Caraman`, `803+ verzekert`. The earlier table in `related_plaintext_pairs.md`
  (`814+`, `303+`, `719`) misread these. A one-to-one alignment drifts: `273~`, `733~`, `916=` and `977=` each
  recur on different words. So the solution sheet is not a word-for-word match of the cipher (phrase entries,
  omitted words or re-wording). Only one R2034 group recurs with the same mark, `222=`, and it lands near
  "observatie, dat". That is not proof against `222= = niet` (R1946), but the value should be re-checked if
  the key is ever seen. Bases shared with a *different* mark (670, 37, 394, 202, 145, 44, 410, 99) are
  different entries and give nothing.
- **R1946 cipher page 4** (words 1–40) re-read: homophones are in use (Heer = `453=` and `370~`), and none of these
  groups occurs in R2034's meaningful part.
- **The series are not alphabetical** (~ series: 297 Men, 370 Heer, 500 dat, 580 de, 733 zeer, 884 waar), so
  plan items 3–4 (page-order/monotone alphabet solving) cannot work. With 58 of 67 words appearing nowhere in
  the surviving same-key traffic, a language model has nothing to anchor them to.

**Status: in progress. Blocked (offline key).** R2034 stands at 9/67 words. The only way forward is the
physical key, NA 2.21.045 inv. 34313 (duplicate description NA 2.21.227/335, Museum voor Communicatie B1 392):
request a scan.
