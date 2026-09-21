# Ormanetto / Clementino, Spain nunciature 1576-77 (ASV Segr. Stato Spagna 10; DECODE R117, R118)

Catalogue no. 239 (DECODE refill, rule-scored class A, "noted"). Worked 21 Sept 2026.

Outcome: **attempted and closed.** R117 contains no cipher. R118 is a short numeric cipher with no key and no
decipherment; not read.

## What the two records are

**R117** (`ASV_i1025_SdS_Spain_10-1`, 2 images, ff. 245-246, stamped 247): a clear Spanish memorial, *Copia del
Memorial dado por parte del obispo de Pamplona*: an account of the fruits of the see of Pamplona during the vacancy
after Diego Ramírez (d. 27 Jan 1573) until Antonio Manrique's bulls (1575), and the claim that the nine months'
fruits held back by the Pope be paid to the bishop. The only "numerical" matter is sums of ducats in Roman numerals
with the Spanish thousands sign (e.g. `xbnUdn L-ix`, `xxxbjUdn - m`), repeated in the right-hand margin. There is
no cipher. DECODE's "Ciphers within cleartext" tag was triggered by the Roman-numeral sums.

**R118** (`ASV_i1025_SdS_Spain_10-2`, 1 image, f. 365, stamped 350): six lines of contiguous figures (389 digits
measured on `r118_cipher.txt`, plus the barred-4 sign `X` and dots over some digits), then in another hand and
ink a clear Italian note:

> Il Nuntio ha trattato col Sig.r Perez tutto quello che V.S. Ill.ma scrive con la cifra di 19 di sett.re, il qual
> Sig.r ha promesso di buoni uffici al Re, et di procurare risposta, de la quale V.S. Ill.ma sarà poi sabbato
> avvisata.

The letter is undated on the leaf. The note refers to a cipher from Rome of 19 September, and Perez is Antonio
Pérez, Philip II's secretary. The letter therefore dates from autumn 1576 or 1577. The DECODE record's range is
9 Jan 1576 to 2 Nov 1577; the catalogue's "9 Jan 1576" is only the start of that range.

## Is the note the decipherment? (DECODE: "possibly already deciphered on the same page")

The note is about the same length as the cipher (about 200 letters expanded; about 190 digit pairs), and it opens
the way the figures do: `20 70 53` recurs at the start of line 1 and the end of line 2. It was tested as a crib.
`crib_align.py` beam-searches a tokenisation of lines 1-2 into 1-3-symbol tokens aligned letter by letter with
the note, keeping the token→letter map functional and minimising distinct tokens:

- the note: 43 distinct tokens for 60 letters;
- three shuffles of the same letters (control): 47, 51, 48.

The gain is small and the best alignment is incoherent (tokens of mixed lengths, no stable pair structure). The
note does not fit as a crib. It reads as the nuncio's (or his secretary's) clear message in the third person,
added below the cipher, not a decifrato. Line 1 also breaks two structural keys: Lasry's key for the Como→Dandini
cipher of 1580 (DECODE R72; two-digit letter codes with an even second digit, 3 digits + mark for nomenclator
words) cannot apply, because this text has odd second digits throughout (53, 07, 03, 05).

## Keys and printed sources looked for

- DECODE: no key record for the Spain nunciature 1570-80. The only 1570-80 Spain records are R116 (Ormanetto 1573,
  non-decrypted, still in the catalogue as no. 259) and R5624 (Sega 1579, N/A).
- The Spain nunciature correspondence of these years is calendared by J. Olarra Garmendia and M. L. Larramendi,
  *Correspondencia entre la Nunciatura en España y la Santa Sede durante el reinado de Felipe II* (Rome, from
  1948; citation from memory, not checked here). Not found online. If this letter's decifrato survives in the registers, it
  is there. This is the lead for anyone continuing.

## Transcription

`r118_cipher.txt`: lines 1-2 read at 3x zoom, lines 3-6 at 2x and less secure. Dots over digits are not recorded.
The page images are git-ignored (`decode/`, DECODE login).

## What would move it

The Olarra-Larramendi volume (to date the letter and find its decifrato) or a Spain nunciature key of 1572-77.
Ciphertext-only: 389 digits in a homophonic two-digit system with marks is short for a blind attack.
