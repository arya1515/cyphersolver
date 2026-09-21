# De Swart 1782: Dutch legation cipher from St Petersburg (DECODE R1036)

Status: read (R1036, 96.7% of groups); R1040 (1787) read in part

## Target

Johan Isaac de Swart, Dutch resident at St Petersburg, to Pieter van Bleiswijk (Grand Pensionary), despatch of
8 March 1782. DECODE R1036, `NA_3.01.25_P._van_Bleiswijk_inr610_by_J.I._de_Swart_1782-03-08`, nine scans, with
DECODE's authenticated manual transcription of the ciphertext. Sister record R1040 (Nationaal Archief 1.01.02
Staten-Generaal inv. 7408, de Swart, 29 November 1787, 23 scans) was worked alongside.

## System

A Dutch code-nomenclator of three-digit groups in which a mark on one digit (two short strokes, underline, caret,
small circle, circle with a bar) makes a different group: `340` and `340^_` are unrelated values. Entries are
words, syllables and letters, so words are often built from pieces (*Spa + nje*, *Dene + mar + ken*). This is the
Croiset codebook of 1765 for the Russia legation, which survives with its key as DECODE R1038.

## Result

The key comes from the archive: DECODE R1038's authenticated partial transcription of the 1765 codebook, parsed
to 5,961 code-to-plaintext entries (`decode_1765.py`, `R1038_key_parsed.tsv`). It reads 1,448 of the 1,719
groups (84.2%). Thirty-four more values were recovered from repeated contexts, each checked against every
occurrence, which brings the reading to 1,613 groups (93.8%). They are labelled "contextual inference" in
`R1038_key_parsed.tsv`. Examples: `881` = *nje* (Spanje), `340^_` = *mar* (Denemarken), `176^^` = *mpli* (*pure et
simpliciter*, twice), `741` = *haar* (the Empress, 12 times), `681^_` = *mogendheden*.

A third pass read the key entries DECODE had left illegible straight from the R1038 scans (the word stands to the left of its code, and parallel columns of homophones confirm faint words). Of 50 entries read, 41 fit their R1036 contexts and were kept, for example `781` = *geheel* (*het Griekse project geheel stil*), `748^"` = *commercie* (*de vrijheid van de commercie der neutralen*), `488^_` = *Zijne Keizerlijke Majesteit*, `515^o` = *twaalf* (twelve Greek boys), `640` with a barred circle = *Russisch*. They are labelled "read from R1038 scan" in `R1038_key_parsed.tsv`, and every reading, kept or not, is in `R1038_scan_readings.tsv`. R1036 now reads 1,663 of 1,719 groups (96.7%). The 56 open groups (51 codes) are entries lost in the scan's binding shadow, blank in the book, or read with too little confidence to use.

The despatch covers three matters:

1. the French and Spanish answers to the Austro-Russian mediation proposal, and Britain's position on the American
   colonies and Gibraltar;
2. Catherine II's Greek project: Grand Duke Constantine is being taught Greek and given Greek attendants;
3. Prussia's accession to the Armed Neutrality, and the Vice-Chancellor's talks with the Swedish and Danish
   ministers about the accession act and its secret articles.

The token-level reading is `R1036_machine_decipherment.txt`, with the audit trail in `R1036_tokens.tsv`. The 56
unread groups are all rare codes, and 51 distinct codes remain (`R1036_unknowns.txt`). A normalised opening and
the method are in `METHOD_AND_STATUS.md`.

## R1040 (1787)

Leeuw (2000) says this letter was coded "presumably by accident" with two codebooks. The switch point is at
group 180 of image 5459. After it the 1765 key reads the text at 84–90% a page (`R1040_second_key_*`). The first
1,928 groups use a missing Rechteren-family nomenclator. Crib alignments with R2032, R2051 and R2052 (known
plain/cipher pairs from 1784–86) cover only 2–3% and do not yield prose. The key is probably Nationaal Archief
inv. 158, which is not online. That segment is open.

## Prior work

No published decipherment of R1036 or R1040 was found. The search covered record numbers, correspondent, dates
and subject. The Oterleek-codes paper (HistoCrypt 2026) documents the codebook family but not these letters.
