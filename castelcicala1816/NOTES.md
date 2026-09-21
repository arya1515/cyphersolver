# Castelcicala (Paris/London) to the Marchese di Circello, 1816–1819 — catalogue 167

Attempted 21 Sept 2026 and closed open: no key, no decipherment, no crib. Catalogue entry 167 stays with
outcome "attempted, open".

## What the records are

DECODE R9553, R9555–R9557, R9582–R9586 (ASNa, Ministero degli affari esteri 2337_4…2337_37), 13 images, fetched
with the shared DECODE cookie (images git-ignored in `img/`, metadata in `decode/`).

- Sender: Fabrizio Ruffo, principe di Castelcicala, Neapolitan ambassador (London in 1816, Paris 1815–1832);
  signed "Il Principe di Castelcicala".
- Recipient: **not unknown**. R9553 is addressed "Ecc.mo Sig. Marchese di Circello, S. S. S., Napoli"
  (Tommaso di Somma, Secretary of State for foreign affairs). DECODE leaves the receiver blank.
- R9553 is headed "Cifra della Segreteria di Stato" and numbered 2314: the ministry's general code, not a
  personal one.
- Dates on DECODE: 1 Apr, 3 Jun, 6 Sep, 30 Oct 1816 (London/Paris), 14 Nov 1817, 3 Apr, 13 Jul, 28 Oct 1819; R9586
  undated. The 1819 letters end in clear with "Parigi li …".

## The cipher

A numerical code, groups 14–2460, dots between groups, no word division visible. Almost all groups lie in
1350–2460; low groups (14, 40, 86, 97, 154, 222…) are rare. Some groups in R9585 carry a trailing 0 (15680,
18300, 22321?, 23530, 5810), probably a mark on the base group. Repeated phrases inside one letter (R9553:
"1901 2445 1652 1633" twice, "2358 1726 1454" twice, "1999 1531" four times) show a codebook of words or
syllables, not a letter cipher. 331 groups transcribed from three pages (`transcription.txt`), 208 distinct:
far too few for a ~2,500-entry code to be broken ciphertext-only.

## Where a key could come from, and what was checked

- **Box 2317 plaintexts** (DECODE's note). The only box-2317 record on DECODE is R9549 (2317_1). Its cipher pages
  (a 1798 "Cifra di Vienna" despatch with a clear version, and a letter signed "de Baptiste") use a different
  code: their frequent groups are 441, 486, 563, 1144, 1951, none of which is frequent here, and they stop at
  ~1999. So the box-2317 plaintexts on DECODE do not belong to these ciphertexts.
- **Decrypted siblings in box 2337** (R9550–R9552, R9568–R9581, R9589–R9590) are 1850s–60s telegrams and letters
  (e.g. R9550 Massone, Washington 28 Oct 1859, syllabic code with interlinear reading). Different period, different
  code; not tested further.
- **Print.** Web search (Castelcicala + Circello + cifra/dispacci 1816–1819) found biographies (Treccani DBI) but
  no edition of the ciphered despatches. Not in Tomokiyo's Cryptiana index as far as searched.

## What would move it

The 1816–19 "Cifra della Segreteria di Stato" codebook, or Circello's deciphered copies, in ASNa (Esteri, the
Paris legation series or the Segreteria's cipher office papers). Failing that, a full transcription of catalogue
166 (15 more records, 51 pp., same box, same sender, probably the same code) would roughly quadruple the text,
still short of what a ciphertext-only attack on this code size needs.
