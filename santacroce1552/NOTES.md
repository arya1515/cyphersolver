# Prospero Santa Croce (nuncio in France) to Cardinal Innocenzo del Monte, 1553 (ASV Segr. Stato, Francia 3; DECODE R6–R10) — NOTES

Status: no write-up

**Verdict: closed, already solved and in print.** All five DECODE records are ciphered passages of letters from
Santa Croce's first French nunciature. Each was deciphered on arrival, and the decifrati are bound with the
originals in Nunziatura di Francia 3. All five letters are printed with the cipher passages already deciphered in
J. Lestocquoy (ed.), *Correspondance du nonce en France Prospero Santa Croce (1552–1554)*, Acta Nuntiaturae
Gallicae 9 (Rome/Paris 1972). George Lasry put a scan of that volume and his reconstruction of the letter key on
all five records on 24 Oct 2020. This session adds nothing new, so catalogue entry 245 is removed and there is no
site page. Session 2026-09-21 (Claude Opus 5).

## Sources (DECODE, fetched with the shared cookie; images and PDF stay in the git-ignored main-checkout folder)

- Images: R6 ff. 117r–117v, R7 ff. 128r–128v, R8 f. 230r, R9 f. 248r, R10 f. 263r.
- Volunteer transcriptions from 2016 (`decode/DOC_R{6,7,8,10}_D162x.txt`). R9 has none.
- Lasry's reconstructed key, the same file on every record (`decode/DOC_R*_D320x.txt`): a homophonic alphabet of
  1-digit and 2-digit elements (A = 28|38|8, E = 24|34|4, I = 2|22|32, O = 26|36|6, T = 07|76|86, U = 02|04|06|08,
  and so on). **1** is a null or word separator. The code groups (nomenclator) start with a dotted digit.
- DOC_R*_D319x.pdf: a 288-page Google Books scan of Lestocquoy 1972. The page number is the PDF index minus 13.

## Identification in Lestocquoy 1972

| DECODE | folio | letter | printed |
|---|---|---|---|
| R6 | 117r–v | no. 67, Poissy, 26 Mar 1553 ("fol. 117-120v; déchiffrement, fol. 118v") | pp. 157 ff. |
| R7 | 128r–v | no. 71, Poissy, 5 Apr 1553 ("fol. 128-129v; déchiffrement, fol. 129-130v"), cipher marked "En chiffre" | pp. 162–163 |
| R8 | 230r | no. 112, Abbaye d'Ourscamp, 28 Sept 1553 (fol. 229-231); starred cipher passage "Il Re Chr.mo resta mal contento dell'impresa di Corsica…" | p. 218 |
| R9 | 248r (stamped 256) | no. 124, Paris, 14 Dec 1553 (edition gives fol. 254-258v, a different foliation); P.S. "Si dice che ci è l'avviso della giunta del sig. Pietro Strozzi in Corsicha…" | p. 240 |
| R10 | 263r | second letter of 23 Dec 1553 ("ibid., fol. 263-264"); cipher "Molti persuadeno S.M. di havere a far guerra in Italia…" | pp. 243–244 |

DECODE's date "28 Jul 1552" is the start of the volume (the archive comment says "dal 28 Luglio 1552 al 13 gennaio
1554"). It is not the date of any of these letters, which run from 26 Mar to 23 Dec 1553.

## Check of the key against the print

`decode.py` applies Lasry's key to the 2016 transcriptions. The split into 1- and 2-digit elements is ambiguous, so
it is resolved by beam search under `it-cinquecento`, and dotted groups are left as [codes]. The decrypts agree with
the printed text wherever the transcription is clean. Examples:
- R6: "ci è maneggio stretto col [duca] … non so se sia per haver denari con promesse di mercanti et avvantaggio
  … o pur per qualche lega o per haver artigliaria con la scusa che ha usato il [duca di Firenze] a Siena",
  word for word with p. 157.
- R8: "resta mal contento [dell']impresa di Corsica parendole … stata impertinente … lauda molto … si risoluerà di
  mantenerla … parte con provisione di [quaranta mila] scudi per le cose di [Parma]", which agrees with the
  interlinear clear and with p. 218.
- R7 and R10 agree with pp. 162–163 and 244 ("generale supremo di Italia con vinti mila scudi…", "Molti … a far
  guerra in Italia…").

The code groups ([57], [43], [63], [99], and undotted "3 3") were not worked out against the print. They are not
needed, because the print gives the whole text.

**R9, the three cancelled lines.** Under the letter of 14 Dec 1553, three lines of cipher are struck through with
crosses. The edition does not print them. The secretary then wrote the postscript out in clear below: "L'armata
regia che partì per Corsicha ha havuto fortuna et non si sa come né dove sia et non credo che ci sia aviso del
Strozzi". I read the struck digits through the strokes (`r9_cancelled.txt`) and decrypted them. The reading is
poor, but fragments fit that same sentence: line 1 begins "l'ar[mata]…" and line 3 has "…aviso…". So the cancelled
cipher is the postscript, enciphered and then abandoned in favour of clear text. Nothing unprinted is hidden there.

## Files
- `decode/` — the DECODE text files (transcriptions, Lasry's key). The images and the PDF are not committed.
- `decode.py` — decrypts with Lasry's key plus an LM segmenter.
- `r9_cancelled.txt` — my reading of the R9 cancelled lines (uncertain).
