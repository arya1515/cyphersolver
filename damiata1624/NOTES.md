# Paris nunciature to the Secretariat, 1625 (ASV Segr. Stato Francia 64; DECODE R59–R61) — NOTES

Status: no write-up

**Verdict: read at the time. Both cipher passages carry the Roman office's decipherment on the leaf, and the
reconstructed key already on the DECODE records fits them.** Catalogue entry 256 ("Nuncio Damiata (France) to The
Secretariat, 22 Dec 1624") is resolved and removed. One session, 2026-09-21.

## What the records are

The catalogue title is DECODE's archive comment, not the documents. "Damiata" is the see *in partibus* of the
nuncio, Bernardino Spada, archbishop of Damiata (Tamiathis), nuncio in France 1623–27; "22 Dec 1624" is the
start date of Naro's run in the volume, not a letter date. The two records are:

- **R60** (ff. 137–138, stamped 137/138): the nuncio's letter, Paris, **15 August 1625**, signed by the archbishop.
  Clear Italian news (Fontainebleau, Richelieu, Mansfeld's officer Montespina, the English fleet, Vaudémont,
  Verdun). On f. 138r three short cipher runs, each with the decipherment written above it:
  *Il fratello dell'Arcivescovo [di Livorno?] … mi ha mostrato e lasciato copia dell'annesso capitolo di lettera
  che gli scrive il detto Monsignore …*
- **R61** (ff. 186–187): **Bernardino Naro**, Paris, **last day of February 1625**, signed, with a *Copia* of a
  Brussels letter of 21 Feb 1625 (Mirabello, the Savoy ambassador). One line of letter-sign cipher (marked +)
  and two lines of figures at the foot of f. 186r, with the decipherment written above the figures:
  *A cenar l'occasione di rispettar i Francesi sospettosissimi e gelosi di loro natura.* A faded offset of the same
  line shows on f. 186v.

So DECODE's "Non-decrypted" is wrong for both: they were read at the time.

- **R59** (ff. 126–127, stamped 126/127; catalogue 255, "Naro, 3 Jan 1625"): **Bernardino Naro, Paris,
  14 April 1625** (Richelieu, the Aldobrandini precedent, lodging for the coming legate). Three cipher passages,
  each glossed above: *il Generale delle galere* (f.126r); *di procurare l'Ambasceria ordinaria di Roma* (f.127r);
  *Il card. di Lione lo contrarià* (f.127v). Decoded with the key: `14 18 17 08 41 40 33 18 [2] 89 [25] 33 18 [55]
  14 40 33 18 41 08` = *generale de le galere*; `33 [5] 40 34 47 40 37 48 49 40 41 …` = *l'ambasciar…*;
  `… 74 93 41 40 41 49 40 [25]` = *contraria*. Catalogue 255 resolved and removed the same day.

## The key

The DECODE DOC_ files on both records (D3246, D3247) hold George Lasry's transcription (24 Oct 2020) of the key
reconstructed by Norbert Biermann and Thomas Bosbach for ASV F64, 1625: two-digit homophones, nulls 2 and 5,
three-digit nomenclator codes each followed by a null digit (`key_R60_biermann_bosbach.txt`). It fits:

- R60: `04 [5 5] 13 41 40 93 18 33 16 [2 5] 98 [5] 40 41 48 39 03 18 37 48 16 30 06` = *a fratelo del
  arcivescovo*; the run under "Monsignore" contains `14 17 16 41` = *gnor*.
- R61: the end of the figures decodes as *… di loro natura*.

My digit reading from the DECODE scans confuses 8/0 and 9/4, so the passages do not decode clean end to end
(`decode_with_key.py` marks the gaps); the contemporary glosses are the reading. The letter-sign line in R61 is not
in this key and was not attacked: whether the + gloss belongs to it or to the figures is not settled.

## Files

`ciphertext.txt` (R60, R61, with the page), `r59_digits.txt`, `r60_digits.txt`, `r61_digits.txt`, the key, `decode_with_key.py`.
Images: DECODE, fetched with the shared cookie into the git-ignored `damiata1624/decode/` of the main checkout.

## Open

- DECODE corrections: status Non-decrypted → decrypted on the leaf; dates 15 Aug 1625 (R60), 28 Feb 1625 (R61).
