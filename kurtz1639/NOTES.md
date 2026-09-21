# Kurz von Senftenau (Hamburg) to Trauttmansdorff, 1638-39

Status: read in part (key rebuilt in full; all nine letters deciphered; checked second transcription pass 21 Sept 2026)

Ferdinand Sigmund Kurz von Senftenau, imperial vice-chancellor, writing from Hamburg (one from Glückstadt) during the
preliminary peace talks with Sweden and France, to Maximilian von Trauttmansdorff (one to Ferdinand III, one a copy of a
letter to Schwarzenberg). SOA Plzeň, pracoviště Klášter u Nepomuka, RA Trauttmansdorffů, inv. č. 200, karton 9.

## Documents (DECODE, all public images, fetched to img/, git-ignored)

| DECODE | date | to | images |
|---|---|---|---|
| R3812 | 1639-02-03 (DECODE: 1638, wrong) | Trauttmansdorff | 14 |
| R3811 | 1639-01-17 | Trauttmansdorff | 6 (p.1 has interlinear decipherment) |
| R3813 | 1639-01-27 | Trauttmansdorff | 20 |
| R3814 | 1639? undated | Trauttmansdorff | 5 |
| R3815 | 1639-02-06 | Ferdinand III | 4 |
| R4625 | 1639-02-10 | Trauttmansdorff | 7 |
| R4645 | 1639-02-13 | Trauttmansdorff (with two Banér copies) | 9 |
| R4734 | 1639-04-08 | copy of letter to Schwarzenberg | 5 |
| R4736 | 1639-04-14 (Glückstadt) | Trauttmansdorff | 3 |

73 image files (many are two-page spreads). No DECODE key record, no DECODE transcription files.

## Prior work

- Contemporary interlinear decipherment on p.1 of the 17 Jan 1639 letter (R3811).
- Jakub Mírka, "Raně novověká šifrovaná korespondence ...", Západočeské archivy 2012, 44-72; reprinted in Crypto-World
  11-12/2012 (part I, pp. 23-25, lit/crypto1112_12.pdf). He rebuilt the key from the R3811 p.1 interlinear text
  (homophonic letters, one sign for each consonant+vowel bigram ba be bi bo bu ca ... , nulls, no codes) and deciphered
  only the 17 Jan 1639 letter, summarised in Czech (Swedish/French/Dutch pressure on the Polish king, supply problems,
  Saxe-Lauenburg and Denmark, long passage on Hans Georg von Arnim denying a part in Wallenstein's treason and seeking
  pardon). The key table and plaintext are not printed. The other letters were "dosud nedešifrované" (not yet deciphered).

## Method

tr/CONVENTION.md: token transcription of every image (agents, 2 at once). Key rebuilt from the R3811 glosses, then
extended by homophonic solving with a German LM and cleartext context.

## Result (19 Sept 2026)

**The key.** KEY.md / key.json. Numbers 41-100 are consonant+vowel signs in a regular table: each ten is split into two
halves, one consonant each, in reverse alphabetical order from 41 (r p n m l k h g d c b); units 1-4 of a half run o i e a
(41 ro, 42 ri, 43 re, 44 ra); the fifth place of each half is a separate consonant+u series (45 pu, 50 lu, 55 mu, 60 hu,
65 ku, 70 du, 75 gu, 80 bu, 85 cu, 95 us, 100 ru; 97 is, 98 es). Numbers 1-40 and the letter and graphic signs are
homophones for single letters, a few for pairs (9 te, 6 se, c si, n ve, d so, k ti, #l-loop tu); ψ/φ z, π/α m, 29 qu.
#s-loop, #dot, p and a few rare signs are treated as nulls (or flourishes). This is Mírka's "homophonic substitution with
bigrams and nulls", now written out.

**The reading.** read/<record>.txt (clear text in braces, decipherment in brackets); read/SUMMARIES.md in English.
22,913 cipher tokens transcribed; 98.3% get a value. The decipherment is fluent in stretches and garbled in others:
by-eye coherence 55-80% per letter (R4645 best, R4736 and R3814 weakest). The garble is mostly transcription (one pass by
agents; 1/7, 6/0/c, 9/ψ/φ, 93 vs 9 3 confusions) and Latin passages, not the key. α reads "Salv-" before l (Salvius,
salvus conductus): probably a second sign merged with α in transcription.

**Content.** Kurz's reports from Hamburg (and Glückstadt) Jan-Apr 1639: Banér's winter invasion of Lower Saxony and
Halberstadt, Duke Georg of Lüneburg's passivity and the Lower Saxon Circle's neutrality, Arnim's escape and his plea for
a protectorium, the Danish mediation of Christian IV and its expiry, distrust of Salvius and of "universal" treaties
("ein teufflisch inventum"), France's aims (Lorraine, Alsace, the imperial crown), Rákóczi and French money.

**Corrections to DECODE.** R3812 is 3 Feb 1639, not 1638 (it answers R3813 of 27 Jan 1639; postscript dated 1639).

**Open (updated 21 Sept).** The second pass is done (below). The Banér copies in R4645 (to Lüneburg, 10 Jan 1639; to the
Lower Saxon envoys, 29 Jan 1639) and the R4734 endorsement ("Copia deß Herrn Reichs Vice Canzlers schreiben Ahn Herrn
Graven von Schwartzenberg abgangen. 8. April 1639") are transcribed in read/. See Remaining gaps.

## Second pass (21 Sept 2026)

Every tr/ file was checked line by line against crops of the images (tr/PASS2.md rules, tr/PASS2_LOG.md per-file log;
check.py prints each line with its token values). About 360 tokens corrected, no lines added or removed. The recurring
misreads: `c` for `#l-loop` (tu, 27 cases, mostly R3812/R3811), bold `9` for `#sect` (w, about 30), `6`/`61` for `φ`
(z, dozens in R3813), wrong splits of two-digit groups (`63 1` = `6 31`, `9 3` = `93`, `4+ 2?` = `42`), `62`/`93` for
`6`/`9`. In R3813 a crossed ƒ-like sign had been merged with `x` (i); split out as `#f-cross` = ta (114 tokens; LM
confirms: R3813 -2.968 -> -2.935, while x = ta makes R3812 worse, so it is R3813's own sign).

A script bug was also fixed: decode.py, parse.py and check.py treated any line starting with `#` as a comment, so 56
cipher lines opening with a sign (`#4-hook`, `#z-tail` ...) had been left out of the reading and the solver.

Effect (German 5-gram, mean log-prob per char, before -> after; deciphered chars):
R3812 -3.071 -> -3.015 (6888 -> 7008); R3811 -3.036 -> -2.966; R3813 -3.084 -> -2.935 (10189 -> 10514);
R3814 -3.352 -> -3.324; R3815 -3.108 -> -2.981; R4625 -3.270 -> -3.219; R4645 -3.312 -> -3.306 (Latin-heavy);
R4734 -3.089 -> -2.989; R4736 -3.099 -> -3.113 (2060 -> 2200 chars: restored lines, e.g. "dimittiren, mal disfatti
et mal disfatti ist"). 23,699 cipher tokens, 99.9% with a value. read/*.txt regenerated.

Alpha split (21 Sept): α re-valued m -> sa (LM better on 7 of 9 letters), 28 looped tokens renamed #a-loop = m after
image check. Scores after all changes: R3812 -2.969, R3811 -2.906, R3813 -2.881, R3814 -3.260, R3815 -2.945,
R4625 -3.191, R4645 -3.306, R4734 -2.902, R4736 -3.089 (every letter better than the 19 Sept baseline).

## Log

- 2026-09-19: records, images, literature fetched; transcription started.
- 2026-09-19: all 73 images transcribed (tr/); structured solver; key rebuilt (KEY.md); all nine letters deciphered.
- 2026-09-21: checked second transcription pass on all 73 images; comment-line bug fixed (56 lines restored); #f-cross = ta split from x in R3813; read/ regenerated; α = sa and #a-loop = m split; R4645 Banér copies and R4734 endorsement transcribed (addressee Schwarzenberg).

## Remaining gaps

- All nine letters, residual garbled lines (listed per file in tr/PASS2_LOG.md; R3814 and R4645 Latin worst) - blocker: illegible; the checked second pass (21 Sept) fixed about 360 tokens; what remains is mostly ambiguous digit groupings, blots and overwritten digits where the image does not decide, and Latin/Italian passages
- Latin passages - blocker: illegible; checked on the images in the second pass; the residual garble sits in run-together digit groups and blots. The alpha question is settled (21 Sept): the small upright α = sa (Salvius, salvus, caesaris, universal-, sachsen), a larger looped ℒ-form = m (#a-loop, 28 tokens split out on the images); in R3813's hand the two shapes are hard to separate
- R4645 P6 closing and postscript in Kurz's fast hand (about half the words unread; the Banér copies P7+P5 and P3+P8 and the R4734 endorsement are now transcribed, read/R4645_clear.md, read/R4734_endorsement.md) - blocker: illegible; cursive personal hand at DECODE image resolution

## Escalation

- [x] siblings: all nine DECODE records (73 images) transcribed; no key record or transcription files on DECODE
- [x] clear-pages: R3811 p. 1 interlinear decipherment used to seed the key
- [n/a] known-keys: the key is rebuilt in full from the glosses and the regular CV table; Mirka's 2012 key is not printed
- [x] print: Mirka, Zapadoceske archivy 2012 and Crypto-World 11-12/2012: only the 17 Jan letter, summarised
- [x] key-rebuild: structured homophonic solver with a German LM; table 41-100 written out (KEY.md, key.json)
- [x] retry: checked second transcription pass on all 73 images (21 Sept 2026), decode.py rerun on all nine letters; LM score better on 8 of 9
