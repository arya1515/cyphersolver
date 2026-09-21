# Giuliano Caprile (catalogue 157) and Alfonso Cistarelli (catalogue 158), Ferrarese agents in Hungary 1519–1521 — NOTES

Status: written up (docs/caprile1519.html)

**Verdict.** Catalogue 157 (Caprile, 7 records) and 158 (Cistarelli, R1137). Of Caprile's records, R1129–R1135 were
read at the time or in 1882 (clear copies filed as "b"/"c", or interlinear glosses), and R1138 was deciphered by W. Somogyi
(2025). **New here: R1139 (6 Apr 1521) and R1136 (8 Mar 1520) read in part**, with a homophonic key rebuilt from
Somogyi's two printed decipherments. R1128 (9 Mar 1519, a different "two-tier" cipher, about Caprile's own lawsuit)
is not read. Cistarelli's R1137 (numeric) is read only in fragments by ciphertext-only annealing.

ASMo, Ambasciatori, Ungheria b. 4 (Caprile 1519–20 file = "b. 4/23"; 1520–21 file = "b. 4/28"; Cistarelli = "b. 4/26").
DECODE R1128–R1139 (R1137 is Cistarelli). Images fetched with the shared cookie into `img/` (git-ignored). Vestigia
(public) search results in `vestigia/search_*.json`; record JSONs `vestigia/v*.json`; images `img/v/`.

## Record map

| DECODE | ASMo no. | Vestigia | date | DECODE status | clear copy / gloss | cipher system |
|---|---|---|---|---|---|---|
| R1128 | 1519–20 no. 1 | 1853 | 9 Mar 1519 | partial | none found; 7 cipher lines + clear postscript | 1519 two-tier |
| R1129 | no. 3a | 1855 | 20 Apr 1519 | decrypted | 3b, 3c (V1856–1857) | 1519 two-tier |
| R1130 | no. 4a | 1858 | 1 May 1519 | decrypted | 4b, 4c (V1859–1860) | 1519 two-tier |
| R1131 | no. 5a | 1861 | 12 May 1519 | partial | 5b, 5c (V1862–1863) | 1519 two-tier |
| R1132 | no. 6a | 1864 | May 1519 | decrypted | 6b, 6c (V1865–1866) | 1519 two-tier |
| R1133 | no. 7a | 1867 | May 1519 | decrypted | 7b, 7c (V1868–1869) | 1519 two-tier |
| R1134 | no. 8a | 1870 | 12/15 Jun 1519 | partial | 8b, 8c (V1871–1872); interlinear on pp. 4–5 | 1519 two-tier |
| R1135 | no. 10a | 1874 | 1519 | partial | 10b (V1875, 19th-c. copy, gaps); interlinear gloss on the leaf | 1519 two-tier |
| R1136 | no. 11 | 1876 | 8 Mar 1520 | partial | none found | 1520–21 sign cipher |
| R1137 | Cistarelli no. 3 | 1904 | 25 Jul 1520 | partial | none found | two-digit numeric |
| R1138 | 1520–21 no. 10 | 1919 | 16 Feb 1521 (DECODE 6 Feb) | partial | none found; slip | 1520–21 sign cipher |
| R1139 | 1520–21 no. 13 | 1922 | 6 Apr 1521 | partial | none found; slip | 1520–21 sign cipher |

The same 1520–21 sign cipher also occurs, not on DECODE, in 1520–21 no. 11 (V1920 p. 3, a 9-line postscript) and
no. 12 (V1921, 25 Feb 1521, cipher phrases inside clear sentences).

## Systems

- **1519 two-tier cipher**: each cipher unit is a base glyph (7, m, n, L, t, 4, a …) with a small letter written
  above it. R1135's clear lines between the cipher lines are an interlinear gloss ("questa cavalcata respondere che in
  vero è cosa che mo[lto]" = the 10b copy's text). Not yet analysed.
- **1520–21 sign cipher**: continuous invented signs (φ, ψ, ÷, ss, ff, o, q, y, λ, T, ⊥, 8, *, …), no word
  division, no decipherment found anywhere in the file.
- **Cistarelli**: two-digit groups, mostly ending in 5 or 0 (25 95 70 15 80 55 …), with a few other signs (f, k, u),
  mixed with clear text. No gloss.

## Prior work

- ASMo inventory (`lit/asmo_ungheria.pdf`), Caprili 1519–20: "mancano quasi tutte le decifrature di dispacci, le qual
  sono state cavate solo nel 1882". The "b"/"c" items of nos. 3–8 and 10 are those 1882 decipherments (7b is a pencil
  copy beginning "Sire, quantunque io tenga per certo…"). No. 1 (R1128) has none.
- W. Somogyi Judit, "Estei Hippolit püspöki hagyatéka Giuliano Caprili magyarországi leveleinek tükrében",
  *Scriptorium* VI (2025) 247–264 (`lit/somogyi2025.pdf`), n. 50: prints decipherments of the 16 Feb 1521
  postscript in both versions: the slip of no. 10 (V1919 = **DECODE R1138**) and the postscript of no. 11 (V1920).
  She calls the system homophonic. Texts in `crib_somogyi.md`. So R1138 is already read (2025).

## 1520–21 key (R1136, R1138, R1139, V1920, V1921)

Built by monotone EM alignment (`em21.py`, `key21.py`) of the transcription (`caprile1521_transcription.txt`, labels in
`seg21/signs.md`, ligatures m+ → MT, n+ → NT in `c21_merged.txt`) against Somogyi's plaintexts of V1920 and the
capitals of V1919 (= R1138), seeded by a ciphertext-only anneal (`fastanneal.py`, `f21_o4.txt`). 714 letters
aligned, 89.6 % of alignments agree with the majority value of their sign. Counts per sign in `key21_counts.json`,
majority key in `key21.json`:

a = q, T, UT · c = PHI, TH · d = PSI, r · e = y, ss, 12?, 8? · g = w, U · i = B, RC, L · l = ff, n, A? · m = z, HH ·
n = DIV, p · o = CE, QB, o-SL-o · p = EL, AMP · r = AST, x · s = MT (m+), NT (n+) · t = h, f, K? · u = LAM, a.
The lone o is mostly a null (filler between letters); 8 appears as a null after "il" in R1139 L01.
Homophonic, as Somogyi says; no word division; no nomenclator codes seen.

## Readings (gist; raw decrypt in `decrypt21_raw.txt`)

Grades as in README: C = likely, M = possible. Transcription errors leave many letters wrong; only the phrases below
are claimed.

**R1139, slip of 6 Apr 1521 (1520–21 no. 13), 9 cipher lines, read in part.** "Post: il custode … io scrissi … è
tornato governator de[l] … ogni cosa … è tenuto Agria … in castello … la venuta … in Italia … li scritti … vedendo io …
deli danari del suo … come mi disse … lui m'ha resposto dice de voler andar in Italia quando al dare … Milan … parlaremo a
longo sopra ciò … per andar … el mi dirà …" (C for the quoted phrases). Subject: the castellan/custode of Eger, the
governor's return, money of the late bishop, and someone's wish to go to Italy — the Hippolito estate business of
Somogyi's article.

**R1136, 8 Mar 1520 (1519–20 no. 11), 12 cipher lines, read in part.** "e la susseguente matina … il custode … questo
episcopato … il custode … governator … Lactantio … tesoro … in gran … conclusi … congrega[tione] … ogni episcopa[to] …
in questo modo … poco spensi … Excellentia … al custode … de Ungaria sopra il suo … secondo … tornato … intendere …
[s]pensier suo … tal debito" (C/M). Subject: Eger see, its custode and governor, money and debts, the day after a
meeting ("la susseguente matina"), written as Ippolito was leaving Hungary (he crossed the border 7 Mar 1520).

**R1137 (Cistarelli, 25 Jul 1520), 584 numeric groups + 83 signs, fragments only.** Ciphertext-only anneal
(`fastanneal.py`, `refine37*.py`, outputs `f37_*.txt`, `r37*.txt`) gives a partly consistent key (e = 0, 25; a = 86,
80; o = 70, 10; i = 45; t = 95; r = 85, 84; s = 90, 15; n = 65, y; l = 55; p = 75; u = 96; m = 60; d = 20; c = 30) and
phrases such as "lettere per", "sempre", "presto", "saria meglio", "non se poteria", "dua milla", "questi altri",
"Antonio" (M). Not a reading; the transcription (`r1137_transcription.txt`, one reader) needs checking.

**R1128 (9 Mar 1519), not read.** Two-tier sign cipher of 1519 (7 lines). Its clear part and no. 2 (V1854,
"In un'altra mia ve mandai in zifra…") show the subject is Caprile's own lawsuit at Rome ("le ragioni mie …
l'adversario"). The 1882 decipherments of nos. 3–8 and 10 would give the key; not attempted.

## Log

- 2026-09-21: DECODE R1126–R1140 metadata and images; Vestigia searches "Caprile" (52) and "Cistarelli" (20);
  contact sheets of every page. Transcriptions of R1137 and of the 1520–21 cipher by two agents. Literature: ASMo
  inventory (1882 decipherments), Somogyi 2025 (R1138 read). Key from Somogyi cribs by EM; R1139 and R1136 read in part;
  R1137 ciphertext-only anneal gives fragments.
