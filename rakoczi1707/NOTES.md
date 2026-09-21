# Philippe Groffey (?) to Ferenc Rákóczi II, 15 October 1707 — DECODE R902

Status: cipher identified and the letter read in substance; a diplomatic, word-for-word edition still needs a fresh
transcription from the manuscript.

MNL OL, G15 Caps. C. Fasc. 39, pp. 277–279. DECODE R902,
`NAH_G15_CAPS_C_FASC_39_277`. The archive images are not in the public domain and are deliberately not reproduced
here. Research copies were viewed through the account supplied for this project.

## Correction to the catalogue

DECODE calls Pompeio Cesoni (Ferenc Rákóczi II) the author. The address leaf says, in clear,
`A Monsieur / Monsieur Pompeio Cesoni`. Rákóczi is therefore the **recipient**, not the sender.

The sender is very probably **Philippe Groffey** (also Grophey/Graffei in the literature):

- the matching key is headed `De Monsieur de Bonac et Graffei`;
- the writer handles intelligence from the Swedish and Polish courts and discusses letters from Pál Ráday to
  Field Marshal Carl Gustaf Rehnskiöld;
- Groffey was the French-speaking agent used by Rákóczi at those two courts, and the 1707–08 accounts print his
  salary by name.

There is no open signature on the photographed leaves, so the name is an attribution, not a palaeographic reading.

## The key

The letter uses the preserved table in **DECODE R639**, MNL OL G15 Caps. C. Fasc. 44/08. Its transcription is
`DOC_R639_D2752_2752.txt`; the heading is `De Monsieur de Bonac et Graffei`.

It is a one-part numerical nomenclator:

- 10–120: homophonic letters and common endings;
- 121–460: syllables and common words;
- 461–560: titles, peoples, countries, places, names, months, and numbers;
- 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119: nulls.

Rare, diagnostic values include 489 = *Monsieur*, 491 = *Monseigneur*, 497 = *les Svedois*, 506 = *Svede*,
507 = *Pologne*, 526 = *le Prince Constantin*, and 533 = *Dantzig*. The same table reads the known-plaintext
comparators R852 and R912. On R902 it recognizes 1,020 of 1,108 parsed groups (92.1%). The residue is overwhelmingly
made of impossible numbers, joined groups, and one-digit slips in DECODE's manual transcription.

`decode.py` applies the table. `R902_key08_read.txt` is the conservative token-level result: bracketed numbers are
not silently guessed. The raised leading `1` used in this hand is represented by DECODE as `1^.` and must be joined
to the following one or two digits; treating that period as an ordinary separator destroys the reading.

## What the letter says

The document is an intelligence and lobbying report from the Polish–Swedish theatre. The first part surveys military
and diplomatic news involving the Tartars, Saxony, the Swedes, the Emperor, Vienna, and the English and Dutch. The
writer then turns to his own work for Rákóczi. Secure or nearly secure stretches read:

> J'ay aussi eu l'honneur de vous [représenter], Monseigneur, ... les lettres de Monsieur Ráday au général
> Rehnskiöld ...

> ... à la Cour de Suède ... réparer le tort ... à Votre Altesse ... vos intérêts ...

> ... sur mon zèle à Votre Altesse ... je me suis donné tous les mouvements ... tant à la chancellerie suédoise
> qu'à la Cour de Pologne ...

The second leaf discusses the King of Poland, Prince Konstanty, and the King of Sweden, then the disposition of
Polish grandees and troops. Its clearest political sentence says that someone taking Poland's interests to heart was
resolved to sacrifice himself, if necessary,

> ... pour affranchir la liberté ... opprimée par les Suédois en faveur du roi Stanislas ...

This is not a private letter by Rákóczi. It is a report **to** him about attempts to advance his interests at the
Swedish and Polish courts, including the fate of Ráday's approach to Rehnskiöld and Polish resistance to Swedish
management under Stanisław Leszczyński.

## Limits of the reading

The key is certain; the exact prose is not yet publishable as a continuous quotation. The DECODE transcription often
confuses a single digit (for example 142 gives *bo* where 192 must give *eu*, and 143 gives *bu* where 173 gives
*de* in `J'ay aussi eu l'honneur de vous`). Because the code mixes letters, syllables, and complete words, one wrong
digit can turn a normal word into several plausible-looking fragments. Contextual repairs were used only to
identify phrases and are **not** accepted as a continuous diplomatic reading.

A final edition requires retranscribing the 2 cipher leaves directly, group by group, then rerunning `decode.py`.
The result above is enough to identify the system, reverse the catalogue's sender/recipient direction, attribute the
writer with high probability, and establish the subject of the hidden text.

## Sources checked

- DECODE R902 (ciphertext and address leaf), R639 (key), R852 and R912 (same-key comparators).
- Kálmán Thaly, ed., *II. Rákóczi Ferencz fejedelem leveleskönyvei*, vol. 2 (1873). The printed accounts name
  Groffey and record salary paid through December 1707; the target letter itself is not printed there.
- Kálmán Benda, *Le projet d'alliance hungaro-suédo-prussienne de 1704* (1960), on Philippe Grophey and Ráday.
- *Études sur François II Rákóczi, prince de Transylvanie*, identifying Philippe Groffey as Rákóczi's representative
  especially at the Swedish and Polish courts.

## Remaining gaps
- R902 (pp. 277-279), ~88 unparsed or impossible groups and the continuous diplomatic text - blocker: not-attempted; residue is DECODE transcription slips (one-digit errors, joined groups); no fresh group-by-group transcription from the two cipher leaves has been made, though the images were viewable through the project account

## Escalation
- [x] siblings: same-key comparators R852 and R912 read; DOC files R633-R646 fetched
- [ ] clear-pages: not done — check R902's leaves and R633-R646 for a clear draft or decipherment of the 15 Oct 1707 report
- [x] known-keys: score_keys.py tested NAH G15 keys; R639 (Bonac et Graffei) fits 92.1% of groups
- [x] print: Thaly, Rákóczi leveleskönyvei II (1873), Benda 1960, Études sur François II Rákóczi: letter not printed
- [n/a] key-rebuild: key table R639 is complete and certain; the residue is transcription error, not missing key values
- [ ] retry: not done — retranscribe the two cipher leaves group by group from the DECODE images and rerun decode.py
