# Colbert correspondence ciphers (Mélanges de Colbert, 1665 / 1673 / 1674) — cryptiana unsolved item #4

Three short undeciphered passages, all catalogued in DECODE by Tomokiyo (uploader), status Non-decrypted:

| item | MS | DECODE | Gallica ark | what |
|---|---|---|---|---|
| a | Mél. Colbert 127, f.349-350 | R2678 | btv1b10035540v | letter from Ratisbon, 29? Jan 1665, signature read "Estrauelse[?]" — almost certainly **Robert de Gravel**, French envoy at the Diet of Regensburg 1663-; "a few words" in figure cipher |
| b | Mél. Colbert 172, f.23-25 | R2734 | btv1b10034008j | **Louis de Béthune, duc de Charost**, governor of Calais, to Colbert, Calais 3 July 1673; one paragraph (~7 lines, ~120-150 three-digit groups, max 489); clear text around it mentions Douvres/marchands (Dover trade) |
| c | Mél. Colbert 168bis, f.553-554 | R2733 | btv1b100349564 | copy of abbé **Jacques de Gravel** to comte de **Maulevrier** (Colbert's brother, then commanding in Germany), 16 Aug 1674; short passages, max 474; sample: `433 168 75 232 284 415 75 481 141 481 79 141 112 474 141 287 327 99 481 415 199` |

Known keys in the same series that were already tried by Tomokiyo (all reconstructed on cryptiana louisxiv0.htm, DECODE
"Decrypted"): Nuchèze 1662, Fremont 1664, Schomberg/St-Romain 1665-68, Millet 1665 (DE=22), D'Estrades 1666 (DE=15),
De la Haye 1665-67 (DE=99), Pomponne/Vaubrun 1671 (DE=32), **abbé de Gravel 1672 (DE=23, Mél. 159 f.102)**, d'Estrées
1672 (DE=58), Condé 1673 (DE=91), Chaulnes 1674 (DE=64), Colbert de Croissy's ciphers (many). None fits a-c; in
particular Gravel's own 1672 cipher does not read his 1674 letter to Maulevrier (different correspondent → different key).

## Assessment (2026-09-15): STUCK — not solvable from what is online
- Cryptanalysis: (a) is a few groups; (c) is a handful of passages; only (b) has one continuous paragraph, and even that
  is ~150 groups of a 3-digit nomenclator with no repeats to speak of. George Lasry's syllable-cipher solver (which
  cracked the Mazarin-Bordeaux letter in this same series in 2025) has evidently not produced a reading; these items
  stayed on the list after his 2022-2025 sweep of BnF material.
- Key search online: DECODE has no Key records for Mél. Colbert 101-176. French ministerial keys of this period
  survive mainly at the Archives des Affaires étrangères (Ulbert, *Geheime Post* 2015, describes 1661/1675/1676 keys) —
  not digitised.
- Sibling-letter route (the one that worked for Armstrong): other Charost→Colbert letters (Calais, 1673-74, Mél. 165-176)
  or other Gravel/Maulevrier letters (Mél. 168-171) might carry the same cipher with an interlinear decipherment.
  Checking that means paging through Gallica volumes; **Gallica was down (connection reset / 500) throughout this
  session**, and the DECODE full images require a login (only ~200 px thumbnails are public: `decode/`).
- Not "offline-only" in the Hamilton sense (no located key), just no viable path. Park.

## Files
- `louisxiv0.htm/.txt` — cryptiana's survey of Colbert-era ciphers (source of the table above).
- `arks.txt` / `arks.py` — Gallica arks for Mél. Colbert volumes, harvested from that page.
- `gallica_iiif.py` — IIIF manifest/downloader (works when Gallica is up): `python gallica_iiif.py btv1b10034008j "^2[0-9]$" img172`.
- `decode_imgs.py`, `decode/` — DECODE public thumbnails of the three letters.
- `gallica_sru.py` — SRU title search (Gallica engine returned 500 today).

## If resumed
1. Gallica up → download f.23-25 of Mél. 172 and f.553-554 of 168bis at full resolution; transcribe (b) fully.
2. Scan Mél. 165-176 for other Charost letters from Calais with figures; Mél. 168-171 for Gravel/Maulevrier.
3. Only if a deciphered sibling turns up is there a solve here.
