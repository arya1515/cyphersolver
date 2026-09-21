# Riksarkivet 1628–1646 group (catalogue #207, DECODE R4282–R4341)

Outcome (21 Sept 2026): **read in part.** The two Bremen letters of 1631 are read in full; R4282, R4284 and R4306
were attempted and stay open; the Rusdorff (1628) and E 708 (June 1633) letters were surveyed, not worked.
Write-up: docs/riksarkivet1628.html.

Catalogue entry 207 bundled 14 DECODE records from Riksarkivet Stockholm under "Unknown sender → unknown recipient,
Stockholm, Latin, 1628–1646". Viewed here on 21 Sept 2026, they turn out to be four unrelated groups. None of them is
"unknown → unknown", and only two are in Latin.

| records | what it is | system | state |
|---|---|---|---|
| R4282 (Chifferklaver låda II:113) | Latin letter, ~2 pp., sender/recipient not given | letter cipher of ~40 signs (Latin letters, digits 3 4 5 7 8, λ Δ φ ε α ⊡), with Latin words in clear | open |
| R4284 (låda II:114) | Latin letter, 1628, archival note "Legat … till L. Camerarius bref för 1628" | homophonic numbers (108 values) with Latin words in clear; plus a key-test leaf (effusorem sanguinis / pestem patriae / praeter naturalem / disturbatorem religionis) | open |
| R4306 (låda II:133, wrapper II:104) | letter to "Mr ?ilick" in Amsterdam, "1632?" | numbers 5–203, colon-separated; IoC 0.078 | open |
| R4330–R4331 | Johann Friedrich, archbishop of Bremen, to Johan Adler Salvius at Hamburg (not Åke Tott), 27 Nov. and 2? Dec. 1631 (German) | two-digit numbers inside clear German: homophonic, four consecutive numbers per letter; one-/two-number nomenclator (4 = wir, 5 = H. Christian, 7 = H. Georg, 32 = Bistum Minden, 59 = Salvius) | **read** (≈80% glossed at the time; all groups read here) |
| R4333–R4337 | J. J. von Rusdorff to Axel Oxenstierna, The Hague 1628 (German/Latin) | two- and three-digit numbers inside clear text; archive: "in many cases annotated as unsolved cipher" | open |
| R4338–R4341 (Oxenstiernska saml. E 708) | Swedish letters to Oxenstierna, June 1633 (DECODE's 1646 is wrong; the leaves are dated 8/18 and 27 June 1633) | two-digit letter code, four-digit nomenclator (1564, 3143, 3319 …) and letter-pair codes (rr, mm, aa, tt); interlinear decipherments at the time on some groups | read in part at the time |

## Images and access
`decode/` holds the record pages and images (DECODE public records; cookie from `bordeaux/decode/cookie.txt`).
Images are git-ignored. `decode/keys/` holds the images of 70 Chifferklaver låda II key records (R4259–R4329).

## Work so far (21 Sept 2026)
- R4306 transcribed by agent (463 numbers), then re-transcribed keeping the scribe's variant forms (34/74, 40/4o/9o,
  30/3o/70/7o: 55 tokens). Monoalphabetic by IoC (0.078), "34 42" ×31. Annealing with quadgram models in nl, de, la,
  fr, sv, en, it, es, pt, da, as simple substitution, with low/high numbers as word breaks, and as homophonic: no
  language converged (best ≈ −4.3/char against ≈ −2.5 for real text). Not read.
- R4284 transcribed by agent (754 numbers, 108 distinct; ~20 doubtful multi-digit readings). Homophonic Latin
  annealing (8 × 250k): Latin-sounding nonsense only. Not read.
- Key sweep: the Siebenbürgen "Schauis" key (R4310, a = 9 50 71 86) and the 1632 word-end-30 key (R4296) tested
  against R4306 and R4284: neither fits.

## Bremen 1631 (R4330, R4331): read
Transcribed with the interlinear glosses (`bremen_transcription.txt`). Aligning glossed words to their numbers gave a
band key: each letter has four consecutive numbers, the bands in a scrambled order:

8–11 a · 12–15 g · 16–19 n · 20–23 t · 24–27 b · 28–31 h · 32–35 o · 36–39 u · 40–43 c · 44–47 i · 48–51 p ·
52–55 w · 56–59 d · 60–63 k · 64–67 [q] · 68–71 [x] · 72–75 e · 76–79 l · 80–83 r · 84–87 y · 88–91 f · 92–95 m ·
96–99 s · 100–103 z.

The band order is the alphabet written in a six-column grid (a b c d e f / g h i k l m / n o p q r s / t u w x y z)
and read down the columns; that places the unseen q and x and makes 84–87 y (weyter, Reuterey).

k, z, m, w and y were not glossed; they were fixed from the unglossed groups (sinken, schantze,
kommen / dem accord mitbegriffen / umbgriffen, etwas / wir / westphälisch, weiter / Reuterei). Every group then reads
(`bremen_decoded.txt`); the residue is transcription slips (e.g. `occupireh`, `feldlsihen`).

Content: the archbishop (Johann Friedrich of Holstein-Gottorp) presses Salvius, Swedish resident at Hamburg, for
Swedish succour — foot, dragoons, "etliche tausend" — against the imperial/League troops of Gronsfeld and
Bönninghausen in Westphalia; his men have taken the Burg and are attacking the schantze; he fears the enemy will
ravage the Lüneburg country and asks that the Stift be included in the accord if the Neuenburg garrison marches out.

## What stays open
- R4282 (Latin letter cipher, ~33 signs, ~1,000 letters): homophonic and substitution annealing over the written word
  divisions and without them gave no Latin (best −2.77/char with breaks). Either the transcription merges signs
  (u/n/μ, q/g, b/h, o/8) or the system is not a plain substitution. The clear words (et qualis sit eius futurus
  status dubitatur; sed tamen ut res; tractatus magnas admodum; Mittatur nobis responsum) are the cribs to try next.
- R4284 (Latin, 108 numbers): not broken. The leaf with effusorem sanguinis / pestem patriae / praeter naturalem /
  disturbatorem religionis written over their letter-cipher equivalents is a key test for a *letter* cipher, maybe
  R4282's, and was not used yet.
- R4306 (1632, to Amsterdam): monoalphabetic by IoC but no language fits; the digit-variant question is open.
- R4333–R4337 (Rusdorff 1628) and R4338–R4341 (E 708, June 1633, Swedish): not worked. E 708 carries interlinear
  decipherments of the time and mixes two-digit letters with four-digit nomenclator codes and letter pairs; the key
  collection lists a key "Oxenstierna and Lars Nilsson Tungel (1633)" that was not identified among the 70 key
  records fetched. The band-grid idea from Bremen was not tested on them.
