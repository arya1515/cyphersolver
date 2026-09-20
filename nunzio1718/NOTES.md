# Segreteria di Stato to the Nuncio in Spain, 1718-19 (ASV Segr. Stato Spagna 364D)

Status: read — found already solved (George Lasry, 2020); key extended here.

## The target

Twenty-four ciphered despatches from the papal Secretariat of State in Rome to the nuncio in Madrid,
4 January 1718 to 6 January 1720, in Archivio Segreto Vaticano, i. 1025, Segretario di Stato,
Spagna, dossier 364D. DECODE records **R154–R177**, one per item, 90 pages, status "partially
decrypted", homophonic nomenclator, numerical, images behind a login.

The catalogue entry listed this as a transcription job: DECODE's note says "(Partly) deciphered
within the letter", i.e. there are contemporary marginal decipherments on the leaves.

## Prior art — it is already read

The catalogue note was out of date. Each of the 24 DECODE records carries three attached documents:

1. the raw transcription of that item (a bare digit stream, plus the contemporary marginal glosses
   flagged `<PLAINTEXT ...>`), transcribed 2016-17 by EHum / KaJo;
2. `#KEY: reconstructed` — a **complete reconstructed key**, "TRANSCRIBER NAME: George Lasry,
   DATE OF TRANSCRIPTION: October 24, 2020", catalogued as "ASV - S364", covering 1717-01-01 to
   1720-12-31;
3. a 783 KB combined file holding Lasry's **segmented and deciphered** text of the whole S364 corpus —
   Spagna 364C items 1-32 and **364D items 1-24**, the ciphertext split into groups with the
   plaintext aligned underneath, line by line.

So the cipher was solved by Lasry in October 2020 and the whole of 364D was read then. Nothing about
the system was open when this session began. The DECODE status "partially decrypted" and the
catalogue's "noted" rating both understate what is on the records.

The contemporary marginal decipherment, by contrast, is thin and unreliable: on 364D/1 it gives a few
words per page and several are plainly wrong ("Ee", "Narzio/Nunzio?", "CvYeono"). It was not the basis
of Lasry's reading and it is not enough to read the letters from.

## The system (from Lasry's key)

Fixed-length homophonic substitution with a nomenclator, written as an undivided digit stream:

- regular elements are **two digits**; nomenclator elements are **four digits beginning with 4**;
- the digit **3 is a null**, and may also appear as one of the three digits after a `4` prefix, in
  which case it belongs to the nomenclator group and is not a null;
- no word division; homophones per letter run from one to six (`a` = 50; `.` = 303|323|343|363|373|393);
- the nomenclator is **alphabetically ordered in several separate runs**: 4001-4078 particles and
  endings, 4079-4296 nouns and names A-R, 4401-4479 S-V, 4485-4531 months and day numbers, 4535-4619
  a second alphabetical run A-T, then scattered later blocks (4681, 4706, 4870+).

Lasry's key as filed has **268** four-digit entries. The corpus uses **399** distinct four-digit
groups, so **131 were left without a value**, plus a tail of two-digit groups he left as `NN?`.

## What this session adds

Measured coverage of Lasry's reading over 364D: **34,243** cipher tokens, **33,408** given a value —
**97.6% read**. The residue is 835 tokens in 151 distinct groups, most of them two-digit groups the
transcribers could not read off the page rather than gaps in the key.

The real gap is in the nomenclator. Lasry's filed key has **268** four-digit entries; the S364 corpus
(364C + 364D, 84,961 tokens) uses **399** distinct four-digit groups, so **189 were left without a
value**, in **715 tokens — 11.0% of all nomenclator usage**.

Those are recoverable without any new cryptanalysis, because the key is alphabetical in runs: each
unknown group has a bracket fixed by its nearest valued neighbours, and the 85,000-token corpus
supplies contexts. **61 groups were recovered here** on the two together. Unknown nomenclator usage
falls from **11.0% to 3.4%** of nomenclator tokens corpus-wide (715 -> 221), and over 364D alone from
8.0% to 3.4% (198 -> 85 tokens, 97 -> 64 distinct groups). Whole-text reading of 364D goes from
97.56% to 97.89%.

Every value below is carried by at least two independent contexts, and in most cases by the
alphabetical bracket as well. They are in `key_extra.txt`.

| group | value | evidence |
|---|---|---|
| 4007 | stesso | "in questo **stesso** dispaccio"; "lo **stesso** Sig. Card. Alberoni" |
| 4008 | ciò | "è vero che **ciò** seguirebbe"; "spero che **ciò** sia per succedere" |
| 4013 | già | "**già** è abbastanza risposto"; "non sarebbe **già** che un deplorabile effetto" |
| 4030 | quel | "diverso da **quel** prescrittomi negli indulti" |
| 4033 | ogni | "superare **ogni** renitenza"; "per togliere **ogni** equivoco" |
| 4082 | articoli | "i due consaputi **articoli**"; bracket Armi(4081)-Auditore(4084) |
| 4086 | avvis | "divulgato ne' pubblici **avvisi**"; "si contenti di **avvis**armi" |
| 4101 | cifra | "con la sua **cifra** de 12"; "l'altra **cifra** unita a questo dispaccio" |
| 4110 | Congregazion | "la **Congregazion**e Concistoriale"; "i padri della **Congregazion**e di San Filippo Neri" |
| 4113 | Card.le | "il Sig.e **Card.** Alberoni" (25x) |
| 4114 | corriere | "col ritorno del **corriere**"; "la spedizione fatta costì del **corriere**" |
| 4172 | general | "il Capitolo **general**e"; "il vicario **general**e di quella Chiesa" |
| 4174 | giurisdizion | "nel libero esercizio della sua **giurisdizion**e"; "l'autorità e la **giurisdizion**e Ecclesiastica" |
| 4176 | governo | "per sua regola et **governo**"; "al buon **governo** di coteste Chiese" |
| 4191 | istruzion | "le precise **istruzion**i che N.S. le diede" |
| 4193 | leg | "il Sig. Card. **Leg**ato di Ferrara"; "una **leg**a da Valenza" |
| 4198 | maniera | "nella **maniera** già detta"; bracket maggior(4197)-necessari(4200) |
| 4210 | Monsignor | "si sono espressi con **Mons.** Nunzio" (against the parallel plain copy) |
| 4216 | negoziat | "tutti i suoi **negoziat**i conclusi in questa Corte"; bracket necessaria-notizie |
| 4230 | obblig | "l'**obblig**azione che gliene avrà a N.S."; "divotissimo et **obblig**atissimo servitore" |
| 4233 | offici | "il tribunale et **offici**ali della Nunziatura"; bracket occasione(4231)-opportun(4236) |
| 4236 | opportun | "gli **opportun**i provvedimenti"; "valersene **opportun**amente" |
| 4238 | ordin | "in **ordin**e alla reintegrazione"; "dis**ordin**i et inconvenienti" |
| 4239 | pace | "turbare la **pace** della Christianità"; "**pace** o tregua" |
| 4262 | particolar | "una giunta **particolar**e deputata dal Re" |
| 4270 | port | "**port**arsi alla Corte"; "seco **port**ati da Roma"; "im**port**antissimo affare" |
| 4279 | promozione | "in proposito della **promozione** del Sig. Card. Alberoni" (45x) |
| 4403 | risoluzion | "prenderà quelle **risoluzion**i che saranno più proprie" |
| 4408 | scriv | "mi ha fatto l'onore di **scriv**ermi"; "**scriv**ercene subito" |
| 4437 | subito | "**subito** che si fosse concluso"; "risolversi **subito**, altrimenti" |
| 4462 | tratt | "avesse potuto ivi **tratt**are gli affari secondo le sue istruzioni" |
| 4463 | Trattato | "la conclusione del **Trattato**"; "il **Trattato** della neutralità d'Italia" |
| 4465 | tribunal | "il **tribunal**e della Nunziatura di Spagna"; "registrata in quel **tribunal**e" |
| 4467 | truppe | "le numerose **truppe** già incamminate"; bracket troppo(4466)-Turco(4468) |
| 4469 | vascelli | "li **vascelli** di Spagna hanno preso camino"; bracket Turco(4468)-Vescovo(4470) |
| 4474 | Vicerè | "il Sig. **Vicerè** di Sardegna al Sig. **Vicerè** di Napoli" |
| 4482 | corrente | "li 31 del **corrente**" (probable; day-of-month formulae) |
| 4491 | quattro | "li **quattro** motivi addotti"; adjacent to cinque(4492) |
| 4499 | 12 | "in data delli **12** Luglio passato, qual appunto fu il giorno della promozione" |
| 4564 | aggiustamento | "il bramato **aggiustamento** delle note pendenze" |
| 4565 | accennat | "la seconda parte sopra **accennat**a"; "gli **accennat**i due indulti" |
| 4569 | bisogn | "di non averne **bisogn**o, et quando ve ne fosse **bisogn**o" |
| 4573 | contrari | "furono sì **contrari** alla risoluzione presa dall'Imp.re" |
| 4583 | giust | "niun Re potrebbe **giust**amente pretendere"; bracket giustizia(4582) |

Month block (two parallel Gennaio–Dicembre runs; Lasry's own 4535 Aprile, 4539 Agosto and
4562 Novembre fix both offsets, and 4538 Luglio is confirmed independently by "delli 12 Luglio
passato, qual appunto fu il giorno della promozione" — Alberoni was created cardinal 12 July 1717):

| | Gen | Feb | Mar | Apr | Mag | Giu | Lug | Ago | Set | Ott | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| run A | 4532 | 4533 | 4534 | *4535* | 4536 | 4537 | 4538 | *4539* | 4540 | 4541 | 4542 | 4543 |
| run B | 4552 | 4553 | 4554 | 4555 | 4556 | 4557 | 4558 | 4559 | 4560 | 4561 | *4562* | 4563 |

The by-products are two corrections to Lasry's own sheet. His 4470-4477 (`Veso`, `Vesconi`,
`Vescoua`, `Viscon`, `Vesconi|Vienna`, `Viscoui`) are garbled placeholders for a Vescovo/Vescovi
group; 4474 inside that run is not a bishop at all but **Vicerè**. And `4535 - Apte` is `Aprile`,
the fourth slot of a plain calendar run.

## Content

The despatches are Clement XI's Secretariat to the nuncio in Madrid at the opening of the War of the
Quadruple Alliance. The recurring business is the **promozione** of Cardinal Alberoni and the
**aggiustamento** of the "note pendenze" between Rome and Spain — the nuncio's jurisdiction, the
abolition of the Nunziatura in Naples, the *espulsione* of the nuncio, the Spanish *vascelli* bound
for the Levante, the Emperor, the Turk and the Trattato di Pace.

## Files

- `decode/rec15*.htm`, `rec16*.htm`, `rec17*.htm` — the 24 DECODE record pages
- `decode/txt/` — the 72 attached documents (per-item transcriptions, Lasry's key, the corpus dump)
- `lasry/364D-*.txt` — the 24 items cut out of the corpus dump
- `corpus.py`, `ctx.py`, `measure.py` — parser, context viewer, coverage measurement
- `key_extra.txt` — groups recovered here, beyond Lasry's filed key
