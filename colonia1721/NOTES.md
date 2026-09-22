# Cipher slip from Brussels, 9 Oct 1721 (ASV Arch. Nunz. Colonia 5, f. 26r) — FOUND ALREADY READ

Catalogue item 238 (class B), "Unknown sender (Colonia) to unknown recipient, 1 Jan 1721". DECODE R24
(`ASV_ARCH_Nunz_Colonia_5-1`). The DECODE date 1 Jan 1721 is only the year: the slip is headed in clear
**"Brusselles 9 ott.re 1721"**. It is a single leaf (f. 26r) of nine lines of comma-separated figures, no
address or signature, filed in the archive of the Cologne nunciature. Italian.

**Result (21 Sept 2026): found already read.** The record carries George Lasry's reconstructed key "ASV - C15"
(Nov 2020, `DOC_R24_D3446`), his segmented decryption (`DOC_R24_D3445`), and a running reading with an English
translation by Paolo Bonavoglia "based on key obtained with simulated annealing" (`DOC_R24_D3443`). About 96% of the
tokens have a value. Added here: three values from context, the date and place, and a check of the transcription
against the image (it agrees). Seven tokens stay open.

## System

Fixed-length homophones of 1–3 digits separated by commas (no parsing problem), 4-digit nomenclator codes
(9336, 9356, 9441, 9485), nulls 2 / 22 / 222 used as word spacers. Lasry's key in `decrypt.py`.

## Changes to Lasry's key

- **18 = qu, not que**: qu-a-l-che (qualche), a qu-e-l che (quel), in qu-e-st-o (questo). With "que" every one
  of the three has a doubled e.
- **55 = gli**: "ma e-55 a quel che vedo ne è informato" = *ma egli, a quel che vedo, ne è informato*. Grade C.
- **67 = g?** : "67 r a t s di sapere" = *grat(o) … di sapere*, "[I should be] glad to know"; the s is odd (a slip
  for o?). Grade M.
- Lasry's queried 81 ne, 86 se, 88 st all fit (ne è informato, se stima a proposito, questo). Kept.

## Reading (`READING.md`)

> Sopra il curato [45 9441 43]te divinis, g(rat)s di sapere qualche cosa di [9336] [9485] di Tournai. Sopra
> l'affare di Colonia, ma egli, a quel che vedo, ne è informato. Se stima a proposito che io [76] scriva in [9356]
> ad un suo corrispondente, lo farò volentieri, ma attendo i suoi ordini in questo.

"About the parish priest [… a] divinis [= suspended from his office?], [I would be] glad to know something of
[9336 9485] of Tournai. About the Cologne affair, he is, as far as I see, informed of it. If you think fit that I
[76] write in [9356] to a correspondent of yours, I will gladly do so, but I await your orders on this."

Brussels in 1721 is the Austrian Netherlands; the writer is probably the internuncio at Brussels (or his
agent) writing to the nuncio at Cologne, under whom Brussels fell. Not identified further: no sender/recipient on
the leaf.

## Open

- 45, 9441, 43 in "curato 45 9441 43-te divinis": the phrase is plainly "[sospeso/interdetto] a divinis"
  or "curato di [place] …", but no value is supported by a second occurrence.
- 9336 9485 ("di [9336] [9485] di Tournai": probably a title and name, e.g. the bishop), 9356 (a place or
  "cifra"?), 76 (ne/le/gli?).

## Prior art / contamination

Reading and key were on the DECODE record (Lasry Nov 2020; Bonavoglia undated) before this session; found before
any attempt. No print edition searched beyond that (the slip has no sender to search by).

Images: `decode/IMG_R24_I142_P1.jpg` (git-ignored, AAV copyright).
