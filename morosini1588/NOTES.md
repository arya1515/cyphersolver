# Morosini (legate in France) to Cardinal Montalto, 1588–89 — READ

Catalogue item 243 (class B). ASV, Segreteria di Stato, Francia 22 ("Francia, card. Morosino, 1588 e 1589",
ff. 10–583, letters 25 July 1588 – 20 Sept 1589). DECODE R18–R22, R27–R49, R51–R58: 36 cipher enclosures,
items 22/1–37 (22/29 has no DECODE record; R23–R26 and R50 in the numeric run are other material:
R23 a key book, R24 Cologne 1721, R25 Portugal, R26 Spain 1736).

**Result (19 Sept 2026): read.** 34 of 36 read end to end with the key printed by Meister; 2 (R53, R54, items
22/32–33, Tours and Moulins, spring 1589) are in a second key reconstructed only in part by Lasry and read in part.

## Key

Meister, *Die Geheimschrift im Dienste der päpstlichen Kurie* (Paderborn 1906), pp. 393–394, no. 40:
"Con monsig. Moresino nuntio in Francia. 8 Giugno 1587", signed for by Francesco Sini, secretary of the
Bishop of Brescia (Morosini). DECODE attaches the scan (R18 DOC_3174.pdf) and Lasry's partial reconstruction
(DOC_3175.txt, Oct 2020); Lasry noted "full key in Meister" but no plaintext was posted, and DECODE lists the
records as "partially decrypted".

- Letters, homophones of 1–3 digits: a 21 212 2, b 24 42, c 25 52, d 26 62, e 35 153 5, f 30 03, g 40 04,
  h 41 14, i 17 171 7, k 60 06, l 50 05, m 20 02, n 10 01 0, o 91 191 9, p 70 07, qu 90 09, r 00 13 1,
  s 54 45 4, t 51 15 6, u 37 173 3, x 11, z 12, et 16 69 75, con 19 76 55; clusters cr 22 … tr 49.
- Words: non 61 71, che 56, chi 63, per 64, perche 65, percioche 66, accio 67, acchioche 72, nondimeno 77,
  come 79, ancora 92, ancorche 93, benche 94, qua 95, que 96, qui 97, quando 99.
- Nomenclator, three digits with a dot on the middle one (DECODE transcription `X Y^. Z`): 111 Papa,
  113 Re di Francia / S. M.tà Christ.ma, 116 Regina Madre, 129 Duca di, 131 Cardinale di, 133 Arcivescovo,
  161 quanto, 165 quello, 166 questo, 167 V. S. Ill.ma … 232 il già Re di Navarra (full list in decrypt.py).
- Nulls: 8 with any following digit (80–89).

Because the digits run on with no separators and homophones are 1, 2 or 3 digits long, the text is decoded by
a Viterbi/beam search over segmentations scored by the shared Italian 5-gram model (`lang/`, it-cinquecento,
no spaces): `python decrypt.py` → `decrypt_raw.txt` (per page) and `plaintext_by_record.txt` (per item).

Second key (F22b, R53/R54 only): syllabic, 1–2 digits, no nulls, dot on the first digit of nomenclator codes;
Lasry's reconstruction has ~70 elements and gaps, so these two read in part (content: the vice-legate of Avignon at
Tours, lodged near Plessis; heretics and Catholics mixing at court; Mayenne). R35 (22/14) is a Spanish copy of
Philip II's letter to the Queen Mother in the same key; the Italian model still segments it.

## Grades

- Nomenclator glosses 113, 161, 165, 166 are H (Meister prints 113 as "Il Re di Francia, S. Mtà Christma";
  165/166 as "quelli/questi", which the text uses as quello/questo).
- Undotted-code reading: H in bulk; single-letter slips (transcription errors, homophone choice) are left as the
  decoder gives them, typically 1–3 %.
- Dotted codes not in Meister's list (e.g. 162, 191, 250, 516, 617, 716, 770): open, most are transcription
  slips of a dotted digit.

## Content

Per-item summaries: `summaries_a.md`, `summaries_b.md`. Highlights: the Council of Trent's publication and the
Gallican objections (Aug 1588); Estates of Blois; the murder of the Duke of Guise in the King's chamber on
23 Dec 1588 and the arrest of the Cardinal de Guise, Nemours, Elbeuf, Joinville, the Archbishop of Lyon and the
prévôt des marchands (R43); Tours and the royalist–Navarre rapprochement (1589); Moulins, June–July 1589.

## Prior art

No edition of Morosini's legation found (no Acta Nuntiaturae Gallicae volume; searched 19 Sept 2026). The
clear duplicates of the covering letters are transcribed on DECODE (R18/R19 DOC_1806/1807).
Images: DECODE, login; kept git-ignored (`img/`, `decode/*.png|pdf|htm`).
