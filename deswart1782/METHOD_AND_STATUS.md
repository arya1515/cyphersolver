# De Swart cipher despatches: method and working results

## Sources acquired

- DECODE R1036, `NA_3.01.25_P._van_Bleiswijk_inr610_by_J.I._de_Swart_1782-03-08`: all nine scans and the authenticated manual ciphertext transcription.
- DECODE R1040, `NA_1.01.02_SG_inr7408_by_J.I.__de_Swart_1787-11-29`: all 23 scans and the complete authenticated TXT transcription (`R1040_transcription.txt`, DECODE images 5453–5475).
- DECODE R1038, the original 1765 Croiset Russia codebook: all scans and its authenticated partial key transcription (`R1038_key_transcription.txt`).
- DECODE R2045 and R2195: scans of later de Swart ciphertext/plaintext pairs used as cribs and as checks on the 1765 nomenclator.
- DECODE R2032, R2051, and R2052: separate ciphertext/plaintext copies from the same St Petersburg legation (1784 and 1786), acquired to reconstruct the otherwise missing Rechteren-family nomenclator. Their diplomatic transcriptions and provisional group alignments are preserved in `R2032_known_pair.txt`, `R2051_known_pair.txt`, and `R2052_known_pair.txt`.
- Karl de Leeuw, *Cryptology and Statecraft in the Dutch Republic* (2000). Its note on the 29 November 1787 letter says that it is coded, presumably by accident, with two different codebooks.
- Bartoloni et al., “The Oterleek Codes” (HistoCrypt 2026) and its GitLab repository. These document the Croiset codebook family and provide a later machine-readable relative, but not the exact 1765 key.

No published prior decipherment of either R1036 or R1040 was found. Searches by record number, correspondent, date, archive description, and distinctive subject matter led only to DECODE/catalogue records and contextual historical sources.

## R1036 result

The authenticated R1038 transcription yields 5,961 usable code-to-plaintext entries. Marks are part of the code and were normalized as follows:

| Manuscript/transcription mark | Internal suffix |
| --- | --- |
| no mark | none |
| two short strokes / `^{''}` | `^"` |
| underline | `^_` |
| caret | `^^` |
| small circle | `^o` |
| circle crossed by a bar / `^+` | `^CircleWithHorizontalBar` |

R1036 contains 1,719 code groups after removing the duplicated copy leaves. Images 5419/5421 and 5420/5422 independently transcribe the same ciphertext passages; their token sequences agree at 96.7% and 99.6%, respectively. They were aligned and merged, preferring a reading that exists in the key.

The literal key resolves 1,448 groups (84.2%). Thirty-four high-confidence values recovered from repeated grammatical contexts raise this to 1,613 groups (93.8%); the second pass (2026-09-21) added `2` = *een*, `3^o` = *stel*, `39` = *hun*, `176^^` = *mpli* (*pure et simpliciter*), `363^o` = *tusschen*, `410^_` = *zij*, `681^_` = *mogendheden*, `724` = *welgeval* and `741` = *haar* (the Empress, 12 occurrences). These inferred values remain explicitly labelled in `R1038_key_parsed.tsv`; examples include:

- `881` = `nje`, completing *Spanje* repeatedly;
- `340^_` = `mar`, completing *Denemarken* repeatedly;
- `311^_` = `land`, completing *Engeland* repeatedly;
- `404^_` = `lijk`, in *mogelijke*, *onveranderlijke*, and *duidelijke*;
- `114^_` = `ing(en)`, in *bevordering*, *bijvoeging*, *bepaling*, and *betrekkingen*;
- `737^o` = *bewuste*;
- `673^"` = *propositie*;
- `462^"` = *acte*;
- `924` = *het*;
- `7` = *te* (also supplied by a conflicting but legible R1038 entry).

A third pass read the key entries DECODE had left illegible straight from the R1038 scans (the word stands to the left of its code, and parallel columns of homophones confirm faint words). Of 50 entries read, 41 fit their R1036 contexts and were kept, for example `781` = *geheel* (*het Griekse project geheel stil*), `748^"` = *commercie* (*de vrijheid van de commercie der neutralen*), `488^_` = *Zijne Keizerlijke Majesteit*, `515^o` = *twaalf* (twelve Greek boys), `640` with a barred circle = *Russisch*. They are labelled "read from R1038 scan" in `R1038_key_parsed.tsv`, and every reading, kept or not, is in `R1038_scan_readings.tsv`. R1036 now reads 1,663 of 1,719 groups (96.7%). The 56 open groups (51 codes) are entries lost in the scan's binding shadow, blank in the book, or read with too little confidence to use.

The full token-level plaintext is in `R1036_machine_decipherment.txt`, with unresolved groups retained as `[code]`; `R1036_tokens.tsv` preserves the one-to-one ciphertext/plaintext audit trail. The decrypted despatch reports three connected diplomatic subjects:

1. French and Spanish answers to the Austro-Russian preliminary peace proposal and the uncertain British response, including American independence/colonies and Gibraltar.
2. Catherine II's “Greek project,” including the education of the young Grand Duke Constantine in Greek and preparations for Greek attendants.
3. Prussian accession to the Armed Neutrality and Russian discussions with the Swedish and Danish ministers about the accession instrument and its secret articles.

The opening, normalized conservatively, reads:

> Waarbij ingesloten waren de antwoorden van de hoven van Frankrijk en Spanje op de propositie, welke de beide oorlogende hoven dezelve hadden laten volgen op de bewuste preliminaire propositie, [door graaf Cobenzl], welke de Oostenrijkse minister zondag van zijn hof ontvangen heeft, en waarvan in de mijne aan U HoogEdelGestrenge [...] te veronderstellen is dat [...] depeche overgebracht heeft. Betrekkelijk zowel op de bewuste antwoorden als op dat van Engeland [...] bleef evenzo min als tevoren enig middel over waardoor de voornoemde oorlogende hoven de mediatie van enige verdere werkzaamheid zouden kunnen geven.

This is an editorial reconstruction, not a claim that the surviving partial key makes every inflection certain. The machine file is the authoritative auditable plaintext.

## R1040 result and remaining first-key problem

The two-codebook switch is now located exactly. Images 5453–5458 and the first 179 groups on image 5459 use the missing Rechteren-family nomenclator (1,928 groups total). Group 180 on image 5459 begins `dit alles` and switches to the surviving 1765/R1038 key. The 1765-key portion then continues through image 5474; image 5475 has no cipher groups.

`R1040_second_key_machine_decipherment.txt` contains the decoded second segment only (the decoder no longer contaminates it with the first 179 wrong-key groups from image 5459). Direct/key-assisted coverage is generally 84–90% per full page, with lower coverage on the abbreviated final page. The segment reports:

1. evidence for an effective or nearly completed alliance between Austria and France;
2. close attention by the Prussian and British representatives in St Petersburg to the Austrian-French negotiations;
3. information and suspicions relayed from Berlin;
4. Prince Kaunitz, the Bavarian exchange project, and its relationship to the German princes/Fürstenbund;
5. the likely positions of Russia, Prussia, Austria, and France.

Its secure opening reads:

> Dit alles, gepaard met vele andere omstandigheden, schijnen als indicien te zijn welke de hiervoor gedetailleerde [berichten] wegens de effectief, zo niet reeds gesloten, ten minste op het tapijt zijnde alliantie tussen de oorlogende hoven van Frankrijk [en Oostenrijk] zeer waarschijnlijk maken. Ik ben ook van het zekere [onderricht] dat de ministers van Pruissen zowel als de chargé d’affaires van Engeland op de tegenwoordige handelingen alhier van Oostenrijk en Frankrijk een bijzondere oplettendheid hebben gesteld ...

The first 1,928 groups are not yet responsibly claimed as solved. Direct tests show that neither the 1765 key nor the 1803 Croiset relative is the key; apparent 1803 hits produce nonsense. R2052 (24 December 1786) is the strongest known crib. Its clear copy begins “De minister van Pruissen heeft voor eenige dagen demarches gedaan ...” and aligns to 186 cipher groups. R2051 (3 December 1784) yields another clean 245-group alignment. These establish plaintext-unit boundaries and vocabulary, but the digit-level placement/type of marks must be preserved: collapsing marks to the three-digit base creates impossible homographs. Diagnostic marked transfers currently cover only about 2–3% of R1040 and do not form coherent prose, so they are retained as probes, not presented as a decipherment.

Next work on the first segment is therefore narrowly defined: produce exact digit-and-mark transcriptions for R2032/R2052, solve their repeated-symbol alignment globally, and transfer only exact marked groups into R1040 before contextual expansion. The archived Rechteren cipher listed as Nationaal Archief inventory 158 remains a likely physical key source but is not available online.

## Reproducibility

Run `python decode_1765.py` in this directory. It regenerates:

- `R1038_key_parsed.tsv`
- `R1036_tokens.tsv`
- `R1036_unknowns.txt`
- `R1036_machine_decipherment.txt`
- `R1040_second_key_machine_decipherment.txt`
- `R1040_second_key_tokens.tsv`
- `R1040_1765_page_stats.tsv`
