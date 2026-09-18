# Cardinal Soglia → nuncio Viale Prelà, Rome 15 June 1848 — **read**

Source: broadsheet reprint (Rome, Tip. Puccinelli, 1848) of *L'Italia del Popolo* (Mazzini, Milan) no. 40, 30 June
1848, "Dispaccio del Card. Soglia". Posted by Klaus Schmeh (Cipherbrain, 13 Dec 2014) as unsolved; image
`soglia-cryptogram.png` (1325×2061). Transcription: Joe's (blog comment #4) checked line by line against the scan
(`strips/`); **one correction** on line 12: `…2251242496774740906…` (Joe dropped a `4`). Corrected text: `ct2.txt`
(955 digits). The dispatch was addressed to the nuncio at Innsbruck, where the Emperor had fled on 17 May.

No earlier solution exists. Spada, *Storia della rivoluzione di Roma* II ch. XIV, prints only the clear covering
letter and a paraphrase from an "authoritative person" (approval of the nuncio's conduct). *Il Labaro* of 7 July
1848 printed only a guess.

## The system (`decode.py`)

| element | finding | evidence |
|---|---|---|
| `5` | word separator (not at every boundary) | between 5s, 92 of 102 runs have even length; the odd runs are the punctuation digits below plus one print error |
| 2-digit groups | 64-cell table, digits {0,1,2,3,4,6,7,9} × same; letters with homophones + syllables (`con`,`che`,`per`,`gli`,`chi`,`mi`,`te`,`ta`,`to`…) | `8` never appears in the second digit position (0 of 404); every one of the 64 possible groups is identified or accounted for |
| `8XXX` | 4-digit one-part code for words and stems, **in alphabetical order** | Imperatore 8319 < istruzione 8340 < Monsignor 8374 < opportuno 8422 < ordin- 8424 < Padre 8429 < parte 8433 < port- 8446 < Roma 8620 |
| stems | code + letters: `(ordin)i`, `passa(port)i`, `le (parte)cipo`, `(cotest)a`, `(lontan)a` | |
| lone `1 2 3 4` | , ; : . | `4` sits right before the clear "A risparmio di tempo…" |
| `70` | u/v; `70 70` = w (`Lutzovv`) | vie, diverse, nuove, arrivo |
| print error | `19 09 0[5] 99 09 8446 67`: 4 printed as 5 | the second "passaporti" reads `19 09 04 99 09 8446 67` |

Same design as the 1814 Vienna nunciature cipher described by Kent Ramliden (blog comment #7), except that there
7 marked the word codes and dinomes excluded 5/7. Here 8 marks them and dinomes exclude 5/8.

How it was broken: `runpar.py` (5 as separator) → one-letter-per-group SA fails in It/Fr/La (−3.4 nats/char;
the synthetic control solves exactly, `synth.py`) → an injective letters+syllables nomenclator annealer
(`native/isa.cs`, `run_i.py`) produced "circostanze", "intendendosi", "indirizzata". Pinned those (`run_f.py`)
and read the rest by hand. Then the 8XXX parse and the alphabetical code order.

## Plaintext (normalised; `(…)` = code word, `[8xxx]` = code group not read)

> Con mio (foglio) del [8734][8760][8904][8739][8413] si le commetteva che in seguito degli ordini dati a Sua
> Eccellenza il (Signor), [8227] di Lützow di abbandonare Roma, Ella si facesse del pari a richiedere i passaporti
> per restituirsi alla Dominante, o per condursi in (Colonia), che (è) (lontan)a della (guerra), (com)e [8704]e,
> lo avesse creduto opportuno. (Tuttavia) per nuove sopraggiunte circostanze Le partecipo [8093][8102] del (Padre)
> che Ella rimanga in Inspruck presso l'Imperatore e ovunque egli fosse per recarsi; intendendosi sospesa la
> indicata delibera [8136] relativa alla domanda de' passaporti: interessa [8131] a (Padre) (cotest)a nuova
> istruzione, che Le viene indirizzata per tre diverse vie, (col fine di) assicurarne l'arrivo.
>
> *(clear:)* A risparmio di tempo dovrà con ogni sollecitudine rendere ostensibile il presente dispaccio
> *(cipher:)* a Monsignor Morichini per di lui norma alle pratiche affidategli.

**English.** "By my letter of […] you were instructed that, after the orders given to His Excellency the Signor
[…] Lützow to leave Rome, you should likewise ask for your passports in order to return to the capital, or to go
to Cologne, which is far from the war, [as …] you thought fit. However, because of new circumstances, I inform you
[…] of the Holy Father that you remain at Innsbruck with the Emperor and wherever he may go; the decision […]
about asking for the passports is to be considered suspended. It matters […] to the Holy Father [that] this new
instruction, which is sent to you by three different routes so as to ensure it arrives… To save time you must
at once show this dispatch to Mgr Morichini, for his guidance in the negotiations entrusted to him."

History: Lützow received his passports around 6–9 May 1848 and left Rome on 16 May (Chigi diary). The
Dizionario Biografico (Treccani, "Viale Prelà") says that on **14 June the nuncio left Innsbruck for Frankfurt and
Cologne**. So this 15 June counter-order, telling him to stay with the Emperor, came a day late. Morichini
(titular archbishop of Nisibis) was the papal envoy to the Emperor in June 1848.

### Code-word readings and their check
The code is alphabetical. A linear rank model (`rankfit2.py`: code ≈ a + b·rank in a sorted 1,500-word 19th-c.
vocabulary), fitted only on the 9 firm anchors (Imperatore, istruzione, Monsignor, opportuno, ordin-, Padre,
parte, port-, Roma), predicts the context readings (within 4 codes for col, Colonia, come, foglio; 7–23 for the rest; the firm anchors themselves scatter −41 to +60): col(-) 8114/8110, Colonia 8117/8116,
come 8122/8120, foglio 8245/8247, lontano 8339/8346, è 8199/8211, guerra 8289/8310. After Roma the code runs
denser than predicted (Roma +60, Signor +36, Tuttavia +72), which is consistent. This rules out
"dispaccio" (8247) and "Conte" (8227): both would have to sort before è/Colonia.

## Open: 11 code groups (unrecoverable from this message alone)
Windows from `windows2.py` (piecewise interpolation on all anchors, roughly ±15 words):

| code | window | context |
|---|---|---|
| 8734 8760 8904 8739 8413 | tr–tu / venti–vo(lgente) / after v (Z or appendix) / tu–u / N–O | date block "del …"; probably an early-June date such as "tre volgente" plus a reference |
| 8227 | ess–eta–ex–fa | "il Signor, […] di Lützow" (Chigi calls him "ex-ambasciatore") |
| 8704 | te–ti | "(com)e […]e lo avesse creduto opportuno" |
| 8093 8102 | ch–ci / ci–co | "le partecipo [..][..] del Padre" |
| 8131 8136 | cr–da / da–dar | "interessa [..] a(l) Padre", "delibera [..] relativa" |

The char-LM choice inside these windows (`codefill2.py`) only picks function words (ciò, da, esse). Reading
these needs the 1848 papal codebook or other traffic in the same code (Vatican archives, Arch. Nunz. Vienna;
HHStA intercepts). `{8}` after "si" (line 1) is an unexplained stray digit.
