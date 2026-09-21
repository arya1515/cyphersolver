# BayHStA Kurbayern Äußeres Archiv 4591 — fourteen ciphertexts in the Bavarian key volume

Status: in progress

Catalogue entry 161 ("Unknown sender to unknown recipient, 14 ciphertexts"). DECODE R9291, R9319, R9322, R9323,
R9325, R9367, R9408, R9409, R9410, R9413, R9416, R9417, R9424, R9427. Images: DECODE, login (cookie in
`bordeaux/decode/cookie.txt`); not public domain, kept in `img/` (git-ignored).

## What the volume is

KAA 4591 is the ducal chancery's collection of cipher keys, 1530s–1620 (DECODE lists 102 key records R9277–R9423
from it), with ciphertexts bound in among the keys. The fourteen catalogue records are not one correspondence:
they are separate letters in at least six systems, several with their key a few folios away.

| Record | Folio | What it is | System | Key | State |
|---|---|---|---|---|---|
| R9291 | 36 | a strip of cipher signs (alphabet row + second row), not a letter | graphic alphabet | itself a key fragment | reclassify |
| R9319 | 96–114 | "Post Scripta": 17 pp. of squared paper with dots and crosses | grid/dot cipher | ? | |
| R9322 | 121–122 | f.121 Hieronymus Łaski, Buda 24 Nov 1529, copy of his letter to Count Palatine Frederick; f.122 King John of Hungary to Duke Ludwig of Bavaria, Buda 1529 | System B | rebuilt from glosses | **read** |
| R9323 | 123 | Latin note to the Bavarian secretary (Łaski circle) | System B | rebuilt from glosses | 3 of 13 lines, rest in hand |
| R9325 | 129 | Latin note, Fulda affair (1576) | letter substitution + nomenclator | **R9324 (f.124–127)** | **read** |
| R9367 | 169 | German letter, son to father, 22 March 1535, names/phrases in cipher | signs | ? | |
| R9408 | 236–239 | long unseparated text, some clear words | System A | Augurelio R9369? | |
| R9409 | 240–243 | long unseparated text | other | ? | |
| R9410 | 244–247 | German, 1535, clear words mixed in | System A | ? | |
| R9413 | 252–256 | long unseparated text, partial interlinear notes | System A | ? | |
| R9416 | 262–263 | pp.1–2 a Bavarian servant to his duke, "eritags nach Jacobi" (Tuesday after 25 July): troops in Austria/Styria, asks for 7 years' pension and the Oberrichter post at Straubing; pp.3–4 another sign set | homophonic signs | interlinear | pp.1–2 **read at the time**; pp.3–4 **broken ciphertext-only** (de-1500s model), report on the Pressburg talks between the two kings and the Turk |
| R9417 | 264 | Łaski at Kraków, 16 June [1530], to the Bavarian secretary "Waisenfelder": Buda siege, Nicolaus Min… sent to France, meeting at Coburg | System B | rebuilt from glosses | **read** |
| R9424 | 274–277 | German letter, cipher in Latin-letter substitution | letters | margin notes | |
| R9427 | 287 | long unseparated text, faint interlinear decipherment at foot | System A-like | glosses | |

System A (signs ↓ ω π 4 8 ÿ …) is also the system of R9368, R9407 (Augurelio), R9411–R9412 (Cornelio Sperantio):
the Bavarian agents in Rome/Italy, 1530s. Key R9369 (f.172) is "Dno Aurelio Augurelio".

## R9325 (f.129) — read

Key R9324 (f.124–127): alphabet A x, b t, c o, d þ, e 2, f k, g y, h n, i a, k (looped b), l (barred b), m d, n i,
o c, p δ, q (looped δ), r ɓ, s Λ, t Z, u w, x ɣ, y 7, z ⊙; doubles bb v, cc ꝸ, dd XX, ee (crossed x), ff ß, gg,
ll, mm, nn 4, pp, rr, ss (m with tail), tt 3; sch st sp ch signs; nulls g, -o-, stemmed square, ⊟, W-like, 8
underlined. Nomenclator (f.126–127): Pontifex, Card. Comensis, Card. Matutius(?), Nuncius Ap., Electores
ecclesiastici, Cologne, Trier, Mainz, Würzburg (bishop, chapter, dean), Abbas / Capitulum / Decanus Fuldensis,
Imperator, Archdukes Matthias and Ernst, Landsberg league, Ferdinand of Austria, Dux Bavariae, Philip of Bavaria,
Nobilitas Fuldensis, Conradus til (?) dux nobilium, Nobilitas Franconiae, Landgrave Wilhelm, Elector of Saxony,
Augsburg-Confession princes, the Emperor's vice-chancellor and councillors. That is the 1576 deposition of Abbot
Balthasar von Dernbach of Fulda by his chapter and knights with Julius Echter of Würzburg.

Reading in `r9325/reading.txt`. Normalised:

> Protestatus [est] abbas secreto coactum [se] ad litem acceptare Pontificis inhibitionem. Rogatus Pontifex ut
> contradicendo se interponat, declaret sive sponte sive vi contra canones esse. Si id fiat, Abbas agere cessat et
> cum Pontifice litigabit; ad [quod] cum non possit, Consiliarii Caesaris iudicabunt, aut Pontifex tum facit quod
> iam voluit. Rogatus Dux Bavariae auxilio sit; Nuncius suadeat Pontifici ita ad protectionem via[m].

All signs resolve; slips: "secreto" written without its second e, "auxilio" begins with the i-sign, "voluit" ends
in the d-sign.

## System B (R9322, R9323, R9417) — Hieronymus Łaski, 1529–30

Monoalphabetic graphic substitution with a few word signs; key rebuilt from the interlinear glosses (153 aligned
word pairs; `sysB/key_from_glosses.tsv`): 3 i, X e, ⊕ s, U2 u/v, ⊙ a, N n, O m, M o, ⋇ r, HH t, W c/t, D d, ≡ p,
9 l, B b, Z g, Q q, ≐ f, † f, H h, XH x. Word signs from context: DAG = King John (Zápolya) ("non alio loco vult
habere [DAG] quam loco fratris sui", said of the Sultan), BIGX = Ferdinand ("concordia inter [DAG] et [BIGX]";
"ad oppugnandum dominia [BIGX]"), FLW = probably King John's title. Decoded text in `sysB/decoded.txt`.

- R9322 f.121: Łaski to a Bavarian duke, Buda 24 Nov 1529 (with a copy "ad illustrissimum dominum Fredericum imperii
  capitaneum"): King John followed the dukes' counsel; the Sultan, forced home by plague in his army, left John the
  kingdom of Hungary without tribute, fifty guns and a thousand hundredweight of powder, and will return next summer
  against Ferdinand's lands unless there is a concord; Łaski commends himself as the duke's servant.
- R9322 f.122: "Joannes Dei gratia rex Ungarie" to Duke Ludwig of Bavaria, Buda 1529: sends Lazarus the Jew as envoy.
- R9417 f.264: Łaski, Kraków 16 June [1530], to the dukes' secretary: letters of 12 June received; the siege army
  before Buda; concord best made through imperial princes; Nicolaus Min… sent to the King of France; the Sultan
  willing to receive in friendship whom King John names; asks for envoys to meet at Coburg in Saxony by (date) July.

## R9416 pp.3–4 (f.263) — broken from ciphertext only

3,150 signs, 661 words, word-separated, ~23 frequent signs; 'io' always together (treated as one sign). The
constrained annealer (`anneal.py`, homophone caps) with the new `de-1500s` model (Deutsches Textarchiv prints
1472–1609, added to `lang/` for this target) gave running German on the first run: "…uon beden kunigen zu entlicher
handlung gen Pressburg gesetzt… der tag zu Pressburg erfolgt ist… mit grossem pomp… dem turkischen kaiser… tribut…
zu geben…". The faint interlinear gloss on the first lines of f.263 ("nunmen bag uon beden kunigen zu entlicher /
handlung gen bresburg gesetzt") agrees with the solver's text word for word, which confirms the break independently.

## Steps

- 2026-09-21: record list from the DECODE dump (141 records in KAA 4591: 102 keys, 39 ciphertexts); images of the
  14 targets and 30 neighbouring keys fetched with the cookie.
- Matched R9325 to key R9324 by the null signs (identical set); applied key, all words Latin; read.
