# Kauderbach (The Hague) to Friedrich August II, 1754-58 — KHA Prins Willem V inv. 201

Status: read (19 Sept 2026); written up as docs/kauderbach1754.html

Catalogue target: Johann Heinrich Kauderbach, Saxon-Polish resident at The Hague, despatches to Dresden intercepted
by the Dutch (copies in the Stadtholder's archive, KHA Prins Willem V inv. 201). DECODE R1043, R1044, R1954, R1958,
R1959, R2078-R2082 (10 records, 32 pp.). DECODE: "None of the encrypted messages by Kauderbach intercepted in The
Hague were ever solved"; "codegroups are not separated".

## Material

- `decode/rec*.htm` record pages; `decode/DOC_R1043/R1044/R2078_*.txt` DECODE manual transcriptions (only three).
- `img/` full-resolution PNGs (git-ignored, DECODE login images). `sm/` previews (git-ignored).
- `trans/R*.txt` new transcriptions of the other seven records (this project, 2026-09-19).

## Prior work

- Web search (2026-09-19): Sächsische Biografie entry; no printed decipherment of Kauderbach's cipher found.
  Originals in Hauptstaatsarchiv Dresden (Geheimes Kabinett, Gesandtschaften) — not online here.

## The copies

Intercept copies, clear French with cipher passages. Cipher = continuous digit runs, no separators, with clear
abbreviations inside the runs (`E.M.`, `C./.`, `Q./.`, `M./.`, `S./.`, `J./.`, `T./.`).

## Analysis log

1. Digit counts over the three DECODE transcriptions (6,096 digits): 2 1012, 1 964, 9 910, 4 825, 6 696, 3 664,
   7 411, 0 401, 5 135, 8 78. Strongly skewed successor table (6→3/9, 1→6/9/4, 0 never →0/5/8).
2. No 2- or 3-digit phase preference from segment starts (IC 1.98/1.96 and 3.61/3.59/3.61): groups are of
   variable length. Transcribers' spacing does not mark groups.
3. Long exact repeats (e.g. `02 69143116921929144424` ×4, `7969 4716419474792 13` ×4, `11696324` ×8): a fixed
   code, not a running key.
4. Digits 5 and 8 are never inside a code group: dropping them (single-digit nulls) gives a clean 2-digit phase
   (IC 2.72 vs 2.10; 4-phase 0.155/0.161 vs 0.103/0.103). Code table after re-alignment (`align.py`, Viterbi
   pair model with skip penalty): first digit in {0,1,2,3,4,6,7,9}, second in {1,2,3,4,6,7,9}; ~50 codes in real use.
   The same pair profile in every letter: one key for 1754-58.
5. Letter-homophonic solves (quadgram coordinate ascent, validated on synthetic French at 98% with 2% noise and
   through the full digit pipeline) fail on the real stream (-4.7 to -5.1 per token vs -3.9 synthetic); German,
   Dutch, Italian, word-reversed French, null codes, merged look-alike digits (4/7, 1/7, 1/4, 6/0): all fail.
6. **Sibling key found: DECODE R936**, "Kauderbach in Den Haag - Saxony 1761" (HStAD 10024 Loc. 08236/11 Bl. 5),
   transcribed on DECODE. One code per letter or syllable (a ai an au b be ... que qui ... vous), capital letters for
   names (S = la Hollande, Q = la Russie, T = l'Angleterre, U = la France, W = la Reine, Z = l'Empereur, ...),
   and "6 est faux chiffre" (a declared null). Explains our 5/8 nulls and the `S./.`, `Q./.` markers. The 1761
   numbers themselves are a different table (they use 5 and 8). Next: solve the 1754 table as a one-to-one
   assignment onto the 1761 vocabulary (`perm.py`).
7. **Solved (19 Sept 2026).** `perm.py`: simulated annealing over a one-to-one assignment of the 61 codes onto the
   1761 vocabulary (letters + syllables, `m` added after checking the R936 image, where DECODE's "30 - ni?" is m),
   char-4-gram score. Seeds 22 and 24 converged independently to the same key (-3.847/letter, synthetic French
   -3.95). Refined with an extended vocabulary (`perm2.py`, then by reading): 27 = in, 91 = ou, 33 = qu, 79 = st,
   17 = par, 22 = pas, 46 = qui, 60 = ent, 77 = nt. Key in `key.json`; decoder `decode.py`; machine readings
   `read/machine_R*.txt`; code-level lookup `codes.py`.
   First readings: R2078 (24 Dec 1754) "il n'y a pas eu depuis longtems une assemblée des etats de Hollande dont
   les objets de deliberation soient eté plus importans ... les ouvertures faites par le comte d'Affry ... le
   colonel Yorck ne s'endort pas dans ces circonstances"; R2080 (22 Jul 1755) the debate in the Estates on the
   30,000-man augmentation ("le lord Holderness l'a fait connaitre ici"); R1959 (5 Aug 1758) "le bruit que [E.M.]
   est en negociation avec [P.] ne parait pas etre entierement sans fondement".
8. Lengths (measured, `cipher/R*.txt`, pairs after null removal): R1043 1054, R1044 628, R1954 1621, R1958 542,
   R1959 391, R2078 1231, R2079 558, R2080 1260, R2081 802, R2082 425; all 8,512 groups, 62 distinct, IC 0.036.
   The capital-letter names (E.M., P., J./C., Q., S., Y., M.) are clear sigla whose 1754 meanings are not those
   of the 1761 table; read from context only.
