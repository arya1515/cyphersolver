# Segreteria di Stato to the Nunciature in Spain, 1736 (ASV Segr. Stato Spagna 423)

Status: read — found already solved (George Lasry, 2020); nomenclator recovered here.

## The target

Catalogue entry: "The Secretariat (Spain) to The Nunciature, 10 ciphertexts". These are ciphered despatches from the papal
Secretariat of State in Rome to the nunciature in Madrid, 14 July to 22 December 1736, in the Archivio Segreto Vaticano,
Segretario di Stato, Spagna 423 (index i. 1025: "Lett. originale e ciffre della Segretaria alla nunziatura, dal 7 gennaio
1736 al 29 dicembre 1736", ff. 9-522). They are DECODE records **R179-R188**, one per item: 21 pages, status "partially
decrypted", homophonic nomenclator, numerical, images behind a login. The corpus actually has 11 items (423/1-11). The
catalogue's "7 Jan 1736" is the start of the volume, not the date of a letter. The addressee on the clear dockets is
"Sig. Ab. Guiccioli, Madrid", who ran the nunciature after the rupture of 1736.

## Prior art: it is already read

Every record carries the same pattern of attachments as Spagna 364D ([[nunzio1718]]):

1. the item's raw transcription (EHum/Matt F/NiLan, 2015-17), a bare digit stream;
2. `#KEY: reconstructed`, "ASV - S423", **George Lasry, 24 October 2020**;
3. a 68 KB file with Lasry's **segmented and deciphered** text of all eleven items.

So the cipher system was solved and the letters read in October 2020. The DECODE status and the catalogue's "what the
cipher hides is not known" were both out of date. Copies are in `decode/keep/`.

## The system (from Lasry's key)

- Fixed-length homophones, written as an undivided digit stream. Regular elements have **two digits**: letters, plus
  syllables such as `quel`, `per`, `non`, `gli`.
- **7 is a null**, except inside a nomenclator group.
- Nomenclator elements have **four digits beginning with 1** (1130-1985).

Lasry's filed key has **no nomenclator values at all**: every 4-digit group in his decipherment is printed as `<1222>`.
The corpus uses **166 distinct groups in 708 tokens**, 7.9% of the text.

## What this session adds

The 1736 nomenclator is **not alphabetical** (1222 = -mente, 1245 = -zione, 1882 = Spagna, 1935 = V.S.), so the bracketing
method used on 364D does not apply. Values were fixed from context alone. A value was accepted only when **every**
occurrence of the group reads with it, and most groups carry three to twenty occurrences. `key_extra.txt` has 48 lines
(47 groups). The measurement below was run before the last two were added, so it counts 46.

| | before | after |
|---|---|---|
| nomenclator tokens given a value | 0 / 708 | 424 / 708 (46 groups) |
| whole text read (9,001 tokens, nulls counted) | 90.6% | 95.3% |

(`python measure.py`. The 136 unread two-digit tokens are transcription gaps, "?" in the source.)

Selected values, each with the contexts that carry it:

| group | value | evidence |
|---|---|---|
| 1222 | -mente | somma-, diffusa-, pari-, facil-, destra-, sicura-, minuta-mente (44x) |
| 1245 | -zione | na-, situa-, esecu-, considera-, disapprova-, precipita-zione |
| 1655 | N.S. | "N.S. è rimasto sommamente amareggiato"; "ha N.S. lodato"; "le giuste istanze di N.S." |
| 1935 | V.S. | "scritte da V.S. in data dei ..."; "si manda a V.S. copia"; "non manchi V.S. di" |
| 1849 | S. Sede | "tumulti contro la S. Sede"; "i diritti alla S. Sede" |
| 1388 | Cort- | "illuminare codesta Corte"; "alle Corti di Spagna e di Napoli" |
| 1882 / 1606 | Spagna / Napoli | "alle Corti di Spagna e di Napoli"; "pensioni alla Corte di Napoli" |
| 1392 / 1240 | codest- / quest- | "codesta Corte" (Madrid) vs "questa S. Sede", "questa sera" (Rome) |
| 1242 | tutt- | "con tutta la sicurezza"; "di tutto ciò"; "impieghi tutta la sua destrezza" |
| 1241 | molt- | "con molta violenza"; "in molte guise"; "di molta conseguenza"; "dopo molti attentati" |
| 1259 | altr- | "degli altri"; "uno per la ... e l'altro per il"; "degli uni e altri" |
| 1320 | Brev- | "Brevi, uno per la [1828] e l'altro per il Sig. [...]"; "il Breve arrivi sicuramente" |
| 1863 / 1329 | Sig. / Card. | "Sig. Card. Acquaviva"; "il Sig. [1429] di Montemar"; "creando un Card." |
| 1234 / 1594 | Nunzi- / Ministr- | "i nostri Ministri, i Nunzi"; "attual Ministero di una Corte" |
| 1803 | princip- | "contro ogni principio di pietà"; "sul bel principio troncato"; "il cuore de' Principi" |
| 1885 / 1802 | stat- / prim- | "la Corte è stata sorpresa"; "il primo tumulto"; "arrivar prima gli originali" |
| 1692 | port- | "rapporti" (5x), "importante", "in Portogallo" |
| 1423 | dovre- | "non dovrebbero mai servire di esempio"; "non si dovrebbe mai temere" |
| 1908 | temp- | "da lungo tempo"; "da tempo immemorabile" |
| 1614 | notizi- | "se ne dà la notizia a V.S."; "una tal notizia può servire" |
| 1865 | grazi- | "alle grazie accordate"; "alle richieste grazie" |
| 1511 | giust- | "per giustificar poscia"; "le giuste istanze"; "più ingiuste cedole" |
| 1820 | Re | "cedola Reale"; "padronato Reale"; "Regalista" |

Less certain, carried by fewer contexts: 1208 cos-, 1210 restar, 1635 obblig-, 1925 Vescov-, 1239 ecclesiastic-,
1219 ancora, 1889 stess-, 1229 affinché, 1690 mi-, 1943 passat-, 1612 nomin-, 1608 maggior, 1238 quant-, 1231 anch-,
1693 poss-, 1818 inform-.

Open: 120 groups, most seen once or twice. Among them 1591 (16x; "la Maestà"? It fails in "gli arrolamenti [1591]i"),
1596 (11x; before "Molina" and the unread 1513-a-1382: probably "Mons." with a title of Gaspar de Molina, Bishop of
Málaga and Governor of the Council of Castile), 1236 (9x, a conjunction), and the date numerals 1953/1957/1960/1964/1985.

## Content

The letters are Clement XII's Secretariat to the nunciature during the **1736 rupture with Spain**. Spanish recruiting
officers ("arrolamenti", "ingaggiature") in Rome and the Papal State set off riots in Trastevere and at Velletri. The
letters cover the tumults "contro la S. Sede", Cardinal **Acquaviva** (Spain's protector), the Duke of **Montemar**, the
Bishop **Molina** "scordatosi degli obblighi di Vescovo", the Corti di Spagna e di Napoli, and the Dataria and pensions.
From October on they turn to the *padronato reale*, the "Regalista" doctrines of the Madrid junta, Briefs to the King and
Queen, and the nomination to cardinals' hats ("col maggior numero di cappelli").

## Files

- `decode/rec179-188.htm`: the DECODE record pages. `decode/DOC_*`: all attachments and page images (git-ignored).
- `decode/keep/`: Lasry's key and decipherment and the per-item transcriptions (kept).
- `corpus.py`: parses Lasry's aligned decipherment into `seq.json`. `ctx.py`: context viewer. `measure.py`: coverage.
- `key_extra.txt`: the groups valued here. `reading.txt`: the running text with those values applied.
