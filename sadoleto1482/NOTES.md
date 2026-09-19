# Nicolò Sadoleto, Ferrarese envoy to Matthias Corvinus, Pozsony 1482 (ASMo Ambasciatori Ungheria b. 1/9)

Outcome: read in part (19 Sep 2026). R1102's cipher block read in gist; R1101 and R1106 have contemporary clear
copies on Vestigia (7a; 26a/26b), so were read at the time; R1103's faded block yields fragments only.

Session of 19 September 2026. Target: catalogue entry "Sadoleto (Pozsony) to Ercole I / Ferrante, 4 ciphertexts",
DECODE R1101, R1102, R1103, R1106 ("partially decrypted", graphic signs). Pre-1497: a reading beats the 1497 record.

## Prior art
- Never printed. Magyar diplomácziai emlékek (Nagy & Nyáry 1875–78) skipped Sadoleto's letters; MDE IV p. 77 has one
  passing mention. Mátyus Norbert, "Nicolò Sadoleto követjárása Magyarországon (1482–1483)", *Vestigia* 3 (2020)
  150–163 (https://real.mtak.hu/119767/9/Vestigia3.pdf): the letters "were not copied, so not published"; prints the
  20 June 1482 letter in full and quotes short clear passages of 15 July, 11 Sept, 12 Dec 1482. Nothing on cipher.
- W. Somogyi, *Vestigia* 3, 216–230, n. 25: the letter of 24 June 1482 (Vestigia 1280) has a marginal decipherment.
- Cremonini, *RSU* 16 (2017) n. 39: ASMo Cifrario b. 4 fasc. 1 = a key "per corrispondere con Nicolò Sadoletti a
  Napoli tra 1479 e 1480", reconstructed in the 19th century; unpublished, not digitised. No 1482 key known.
- Tomokiyo (cryptiana): nothing.

## Sources in hand (images git-ignored in `img/`)
DECODE (cookie `bordeaux/decode/cookie.txt`), all 4320×3240 two-page spreads, record JSON in `decode/views.jsonl`:

| DECODE | ASMo b.1/9 no. | Vestigia | date | to | what it is |
|---|---|---|---|---|---|
| R1101 | 7 | 1284 (clear copy **1283 = no. 7a**) | 15 Jul 1482 | Ercole | long cipher passages; 7a is the full contemporary clear copy |
| R1102 | 8 | 1286 | 16 Jul 1482 | Ercole | clear letter, cipher block of 7 lines on p. 2 — **no clear copy** |
| R1103 | 11 | 1294 (copy) | 17 Aug 1482 | Ferrante (copy sent to Ercole with no. 12 = V1296) | clear copy with a 4-line faint cipher block on p. 2 — **no clear copy** |
| R1104 | 13 | 1298 (decipherments **1295 = 13a**, **1297 = 13b**) | 31 Aug 1482 | Ercole | "Decrypted" |
| R1105 | 16 | 1302 | 11 Sep 1482 | Ercole | "Decrypted" |
| R1106 | 26 | 1318 (decipherments **1319 = 26a**, **4004 = 26b**) | 27 Nov 1482 | Ercole | partly cipher; 26a/26b give the clear |

Vestigia record JSONs in `vestigia/`; originals downloaded to `img/v/` (no login).

## The cipher
Monoalphabetic substitution with some homophones, graphic signs, word divisions kept, mixed with clear words.
Working key in `key_working.md`. Confirmed by aligning R1101 p. 2 ll. 1–3 with 7a: "…pigliare questa impresa, et
non lassasse pretermittere questa opportunità laquale mai più fo, né forse sera, e che lo facesse per lo amore…".

## 7a clear copy, p. 3 (Vestigia 1283 image 2, right page), as read
1 che io havea da la M.tà del S. Re Ferdinando su questa, et anche dal S. Conte de …
2 …che per nessuno modo io dovesse domandare questo Re per utilità sua, attento
3 la sua natura, et anche … dove el Florentino voleva che io anche ricordasse
4 per questo …, io non volse, et gli dixi la casone, e lo San(?) de' Francesco, el quale
5 anche fo per parte al ambassata che pregasse la M.tà del S. Re de Hungaria cum ogni
6 … volesse unirse e pigliare questa impresa, e non lassasse pretermittere questa
7 opportunità laquale mai più fo, né forse sera, e che lo facesse per lo amore e
8 benivolentia e per la affinità strectissima che l'ha cum tuta la liga, e per honore e glo[ria]
9 de sua M.tà et abassare una volta Venetiani per modo che l'imparasse de stare
10 fra li suoi fine. Bene è vero che poi neli parlamenti che facemo cul Secretario
11 e quelli altri dove tractavamo de tante gente …, io dixi in bono proposito che an[che]
12 minor gente poteria mo la M.tà sua pigliare de quello de la Sig.ria de Venetia
13 in pocho tempo fino a Treviso inclusive, havendo da la liga tanto contento
14 … e che non doveva credere de' … la costa per modo che …

## Log
- 19 Sep: DECODE metadata for R1100–R1118 fetched; images downloaded (cookie works); Vestigia search "Sadoleto" =
  85 items, found the clear copies 7a, 13a/13b, 26a/26b. Key being built from R1101/7a and R1104/13a.

## Results (19 Sep 2026)
- **Key recovered** (`key_working.md`): a monoalphabetic cipher of graphic signs with a few homophones (e, n, o, r, a),
  word divisions kept, clear words mixed in, "quid" (in clear letters) = "perchè". Verified against 7a on R1101 p. 2
  ll. 1–3 ("pigliare questa impresa, et non lassasse pretermittere questa opportunità laquale mai più fo, né forse
  sera, e che lo facesse per lo amore…") and against 13a on R1104 ("epsa me dice che è certa che la liga non…";
  "perchè Millano et Fiorenza non voriano…").
- **R1101 (15 Jul 1482)**: read at the time; its clear copy is 7a (Vestigia 1283). Not a new reading.
- **R1106 (27 Nov 1482)**: read at the time; decipherments 26a (Vestigia 1319, "Quanto sia per le gratiose…") and
  26b (Vestigia 4004). Not aligned sign by sign here.
- **R1102 (16 Jul 1482)**: no clear copy known; **read in gist** (`reading_r1102.md`): Sadoleto learnt in great secret,
  while leaving Buda for Pozsony, what had been written to Francesco Quirino at court: [the Venetians] wanted Matthias's
  friendship, offered him **Veglia** (Krk, seized by Venice from Count Giovanni Frankopan in 1480), to make his natural
  son ("e bastardo", i.e. János Corvin) captain of their fleet, and to pay him **100,000 [ducats] a year**, the same
  sum Sadoleto says in 13a would buy Matthias's entry into the war for the League. Syntax "como [X] haveva scripto ad Francesco Quirino"; gaps: the informant's title (494),
  the code group 3ί2ии (probably "Venetiani"), a few words in ll. 2–4.
- **R1103 (17 Aug 1482, copy to Ferrante)**: the 4-line block is badly faded; fragments only ("… se tener che … lo
  credo … suoi … vostro … meco … che …"). Better images (UV/multispectral) or the ASMo original would be needed.

## Open
- The informant "da 494 Francesco" and the group 3ί2ии; check against the other Sadoleto letters (nos. 18–28) for
  repeats. Ercole's replies (Minute nos. 1–3, Vestigia 1252/1250/1251) may paraphrase the Venetian offer.
- R1103: Vestigia 1294 is the same Ferrante copy; no second exemplar found. Only better imaging would help.
- The 1479–80 Sadoleto–Naples key (ASMo Cifrario b. 4 fasc. 1, Cremonini n. 39) should be compared with this key.
