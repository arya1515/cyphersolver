# Kurz von Senftenau (Hamburg) to Trauttmansdorff, 1638-39

Status: read in part (key rebuilt in full; all nine letters deciphered, first-pass transcription; 19 Sept 2026)

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

**Open.** A checked re-transcription (second pass against the images) would lift the reading to near-complete; the clear
postscripts and the Banér copies in R4645 are not transcribed; R4734's endorsement (addressee) needs checking.

## Log

- 2026-09-19: records, images, literature fetched; transcription started.
- 2026-09-19: all 73 images transcribed (tr/); structured solver; key rebuilt (KEY.md); all nine letters deciphered.

## Remaining gaps

- All nine letters, the garbled stretches (20-45% per letter; R4736 and R3814 worst) - blocker: not-attempted; single agent transcription pass with 1/7, 6/0/c, 9/psi/phi, 93 vs 9 3 confusions; the checked second pass the notes call for was not made
- Latin passages and the alpha sign before l ('Salv-') - blocker: not-attempted; probably a second sign merged with alpha in transcription; not re-checked on the images
- R4645 clear postscripts and the two Baner copies; R4734 endorsement - blocker: not-attempted; clear text, not transcribed

## Escalation

- [x] siblings: all nine DECODE records (73 images) transcribed; no key record or transcription files on DECODE
- [x] clear-pages: R3811 p. 1 interlinear decipherment used to seed the key
- [n/a] known-keys: the key is rebuilt in full from the glosses and the regular CV table; Mirka's 2012 key is not printed
- [x] print: Mirka, Zapadoceske archivy 2012 and Crypto-World 11-12/2012: only the 17 Jan letter, summarised
- [x] key-rebuild: structured homophonic solver with a German LM; table 41-100 written out (KEY.md, key.json)
- [ ] retry: not done — a checked second transcription pass against the images for the confusable signs, then rerun decode.py on all nine letters
