# Acciaiuoli (nuncio in Lisbon) to the Secretariat of State, 1758–60 — READ

Catalogue: "Portuguese nuncio Acciaiuoli and the abbot Testa to The Secretariat", DECODE R25, R195–R201 (8 records).
ASV (AAV), Segreteria di Stato, Portogallo 117 ("Lettere di mons. Acciaiuoli, nunzio in Portugallo, e dell'abbate
Testa, 1757-1761", ff. 2–585). DECODE's date 18 Jan 1757 is the start of the volume; the cipher leaves date from
12 Sept 1758 to 1760.

**Result (19 Sept 2026): read.** Lasry's reconstructed key (DECODE, Oct 2020) had already turned all eight into a
letter stream, but DECODE posted no Italian text and left the 107 distinct four-digit code groups open. Here the stream is
split into words and 25 codes are fixed from the three contemporary decipherments on the leaves (R197–R199), plus
a few more from context. The full text is in `READING.md`. About 80 of the 107 distinct codes that occur once or twice stay open, and
a few passages in the long R200/R201 are broken by transcription slips.

## Key

Lasry, DECODE `DOC_R25_D3232` (reconstructed): fixed-length 2-digit homophones for letters and syllables (a 04 38 55,
e 84, i 08 53, o 81, s 88, il 43 91, che 39, non 14 …), `6` a null, 4-digit nomenclator codes beginning with `2`.
No 2-digit element begins with 2 or contains 6, so the parse is deterministic. Unassigned pairs that turn up
(82, 92, 42, 12, 32, 72, 02) are transcription slips.

## What the letters say

- **R25 (12 Sept 1758):** the nuncio's secret account of the attempt of 3 Sept 1758 on José I. The king, coming back
  from a lady "delle prime famiglie" (the young Marchioness of Távora), was fired on in his calesse; his valet
  and favourite Pedro Teixeira was badly wounded, and so were the postilion and the mule. The king was hit in the
  right arm and taken by the surgeon to the Real Barraca. The blow was thought to come from her relatives or from
  Teixeira's enemies. The Infante Don Manuel spoke of it to the nuncio "con il sospetto".
- **R195, R196 (Sept 1758):** the public version is illness. The arm is said to be broken and to stay impeded. The
  king is in bed all day. Fleets and ships are held back, to the merchants' loss.
- **R197–R199 (Oct 1758, deciphered on the leaf):** abscess and fever, not erysipelas. The arm will stay impaired.
  After the death of his sister, Queen Barbara of Spain, José says Ferdinand VI has promised to marry his daughter
  Maria Francisca, which the Spanish minister contradicts.
- **R200 (28 Nov 1758):** Carvalho (Pombal) is despotic and the king fears him. The court, the Infantes and the
  confessors. The expulsion of Jesuits and a lay brother of the Society. The nuncio is distrusted.
- **R201 (1760):** conferences of the Conde d'Oeiras (Carvalho). The Princess of Brazil's marriage to Infante Don Luis
  of Spain or to Don Pedro; London is alarmed at a Bourbon on the Portuguese throne; "il paese freme" for the
  union with the Infante Don Pedro. That marriage took place in June 1760.

## Sources and files

- `decode/` DECODE record pages, the digit transcriptions (`DOC_*_D165x-1663`), Lasry's key (`D3232`) and his
  decryption of all eight (`D3231`, one file attached to every record). The DOC_*.png files are key and work
  images. Images are in `img/` and are git-ignored (not public domain).
- `lasry_stream.txt`: Lasry's decryption flattened into one string per letter. `code_contexts.txt`: each code
  with the text around it.
- Literature: no edition of these ciphers found. The attempt of 3 Sept 1758 (the Távora affair) is well known.
  Acciaiuoli's reports are cited from the ASV but not printed in cipher or clear (web search 19 Sept 2026).

Contamination: Lasry's letter-level decryption was public on DECODE (logged-in attachments) and was used directly.
The word division, the code identifications and the historical reading are new here.
