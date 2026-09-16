# "KR Blitz" Enigma message, OB Oberrhein IIa → OKW, 10 January 1945 (TARGETS.md no. 19)

Session started 16 Sept 2026. Status: **attempt in progress** (exhaustive ciphertext-only run launched).

## Source

- Klaus Schmeh, *An unsolved Enigma message from the Second World War*, Klausis Krypto Kolumne / Cipherbrain,
  7 Jan 2019 (scienceblogs.de/klausis-krypto-kolumne/2019/01/07/…). Photo of the Funkspruch form supplied by
  Hauptmann Wolfgang Schmidt (Bundeswehr museum, Feldafing). Image: `files/2019/01/Enigma-Himmler.jpg` (1200 × 1683).
- Listed again in Schmeh's *Ungelöste Verschlüsselungen aus dem Zweiten Weltkrieg (2)*, 4 Feb 2021 (item 7; comments
  discuss authenticity: Fraktur form, "HOKW" = Hauptquartier OKW; Michael Hörenberg: "the source is reliable").
- Tomokiyo, unsolved.htm, section "Another Enigma Message (1945)".
- **Fränz Friederes, *Breaking Enigma Ciphertext in 2023* (bachelor thesis, ciphereditor.com archive), §5.3 "Attacking
  a hard nut"**: attacked this message with his open-source tool *bomm* (github.com/ffraenz/bomm). Searched Enigma I
  with UKW-B (60 wheel orders × 26³ positions × 26 right-ring settings = 27,418,560 locations, "E-Stecker" 26 starts,
  IC then Sinkov trigram at 7 plugs), and also UKW-A, UKW-C, "Zagreb Delta", "Spanish Enigma", Enigma S
  "Sondermaschine", B 207. Best scores all lie together (−8.46 … −8.58 per trigram), i.e. **nothing found**. He did
  not enumerate the middle ring (left-wheel step, ~15 % chance) and treated all 97 letters as ciphertext.

## The form (read from the photo at glyph level, 16 Sept 2026)

Header (form 209, Hugo Hönicke Berlin): Fernspruch / Fernschreiben / Funkspruch / Blinkspruch (Fernspruch struck).
Nachr. Stelle "Karpathen" / Nafü; Nr. 110 struck → 86; Vermerke: Geh. Kdos; Befördert an HOKW 10.1.45 2306 durch Ro.,
Rolle 2783; "Ang. 22.30 von Abt. Karp. Lehr(?)"; "Verschlüsselt 10.1 / 22.45 Schlüsselstelle Karpathen: No 86 gKdos",
signature. Abgang Tag 10.1.45 Zeit 2003; Dringlichkeit **KR-Blitz**. An: Oberkdo. der Wehrmacht Abt. P I / Nafü / So.St.
Absendende Stelle: O.B. Oberrhein IIa.

Text line 1: `2003 - 97 - hiq rst -` = time, letter count, **Grundstellung HIQ, enciphered message key RST**
(Heer/Luftwaffe indicator procedure from 1940). The first letter of the indicator is h, not b (same glyph as in
hitlu, aheef); Dan Girard's "BIQ" is a misreading.

Ciphertext (97 letters, 19 groups + 2):

```
HITLU TSUNQ RTLIA BFTQR
NUWLQ VNITR SETNQ IPKLM
AHEEF DCABC UWORU BSWYA
BGGFD TXCBX DVDUC EZGFB
KYILX OWNPQ RTUVS WM
```

Doubtful glyphs (zoomed crops in the session scratch): group 4 ends in **r** (Michael BGNC read s; the r matches the r
of rtlia/vnitr, the s of setnq is a tall cursive s); group 7 is set**n**q (BGNC: v; the n has two arches like vnitr);
group 12 ends in **a** (Girard x, Friederes r; the x's of txcbx/kyilx are open crosses, this is a closed a-bowl);
group 18 begins **ow** (Bean/Michael "a", Michael "h", Friederes "ah": the first glyph is an o with a hook, the second
a w with a leading loop; genuinely ambiguous). Readings differ from Friederes' (`sctnq`, `bswyr`, `ahnpq`) in 4 letters;
1-3 garbles do not stop the trigram method (Ostwald & Weierud 2017).

**Kenngruppe question.** Ostwald & Weierud (2017, citing Rijmenants 2010 p. 331): the Army dropped the discriminant
group on 1 Sept 1943. Verified here on the Huppenkothen message of 9 Apr 1945 (KL-Maschinenschlüssel, key published
by Sullivan & Weierud): with UKW B, wheels I II III, rings XJE, stecker AM BF CD EK HQ IO LV NT SY WZ, start GLB
(= KHR deciphered at UFC), decrypting from the **first** group BUQVG gives `XGEHEIMXSSXGRUFXGLUECKSX…`. So in 1945 SS/Army
traffic the first group is ciphertext: **all 97 letters are ciphertext**, as Friederes assumed. The 92-letter reading
(HITLU as Kenngruppe) is kept only as a low-prior variant.

## Method (enigma/ directory)

- `enigma_core.py` reference machine (verified on the Huppenkothen key, indicator KHR@UFC → GLB).
- `solver.py` scrambler tables T[l,m,r] per wheel order (rings at A, core positions), stepping model with i0 = index of
  the first middle-wheel step (1..26 ≡ right ring) and optional left-wheel double step at the k-th middle step;
  IC / bigram / trigram scoring; hill climb over plugboard moves (add, remove, re-pair; Sullivan-Weierud cases).
- `climb2.py` configurable climb (phase schedule); `sa.py` simulated annealing; `run_all.py` production driver
  (numba, 20 threads, per-order top-K saved to `results/<tag>/`).
- `lm_build.py`: trigram/bigram/monogram log-probabilities = Sullivan & Weierud's raw 1941 Enigma-decrypt trigram counts
  (17,694, from bomm) + the 1945 KL plaintexts, blended 2:1 with 2.7 M trigrams of Gutenberg German converted to Enigma
  conventions (ae oe ue sz, ch/ck → q, punctuation → x, digits spelled).

### Calibration (real 1945 ciphertext, first 97 letters of Huppenkothen parts 1-3, known key)

- At the true location the 26 E-Stecker climbs (IC → bigram at 4 plugs → trigram at 8) recover the full plugboard
  from 15, 2 and 9 of the 26 starts; score −752 / −703 / −729 against a best wrong location of −899 over a whole
  wheel order (17,576 locations): the true key stands out clearly **if** a climb reaches it.
- Broader control set (3 real + 40 synthetic 97-letter texts, random 10-plug keys): 26 E-starts solve 29/43 (67 %);
  + 25 N-starts 32/43; + 10 perturbation restarts (ILS) 35/43 (81 %); + X-starts and 20 ILS 37/43 (86 %).
  Steepest ascent, monogram or bigram first phases, trigram-only, and SA (20k–100k steps) are no better and
  correlate in their failures. Cost: 0.73 ms per climb; 26 E-starts ≈ 19 ms, E+N+ILS10 ≈ 43 ms per location.
- **The failures are informational, not algorithmic**: the six controls that resist everything have plaintext IC
  0.051–0.064 (easy ones 0.08–0.09); given 3–4 of their 10 true plugs the trigram climb still fails most of the time,
  given 6 it succeeds 50–90 %. At 97 letters a low-IC plaintext sits at the edge of the unicity region for this
  attack, which is presumably why Ostwald/Weierud, Hörenberg/Girard and Friederes all came back empty.
- Wrong middle-step index: with i0 off by ±1 the true position still yields the full plugboard in ~70 % of controls,
  off by ±2 much less; so all 26 i0 values are enumerated (no thinning).

## Runs

| tag | hypothesis | locations | pipeline | status |
|---|---|---|---|---|
| main97 | Enigma I, UKW B, 97 letters, no left step | 60 × 17,576 × 26 = 27.4 M | E+N starts (51 climbs) + ILS 10 | launched 16 Sept 2026 |

## Indicator check (`analyze.py`)

A candidate (order, cores l m r at letter 0, i0) fixes the right ring: the window before keypress i0 shows the notch
letter, so ring_r = notch − i0 + 1 − r. The message key P is (l + ring_l, m + ring_m, window_r − 1). Requirement:
deciphering RST at Grundstellung HIQ with the candidate's plugboard and rings gives P, for some of the 676
(ring_l, ring_m). Validated on Huppenkothen parts 1–3: each returns exactly the published rings XJE and message keys
GLB / XSP / BHO. A random candidate passes with probability ≈ 1/26.

## Context

"Karpathen" (Nachrichtenstelle / F.S.T. Karpathen on the form) was a train standing next to Himmler's special train
"Steiermark" at Triberg, used as his command post as OB Oberrhein; on 3 Jan 1945 Fernschreiben Nr. 244 went from
"F.S.T. Karpathen" to the Fernschreibstelle H.Gr. Oberrhein (Die Ortenau 79, 1999, p. 660, footnotes). The message
therefore left Himmler's own headquarters train and was relayed by teleprinter (Rolle 2783) to the OKW headquarters.

## Open / to do
- Left-wheel step variants (kleft 0..3), the 92-letter variant, UKW C: later passes if main97 is empty.
- Historical: the recipient's copy (OKW) or the sender's file (BA-MA RH 19 XIV, OB Oberrhein) could hold the clear text;
  "Karpathen" was the cover name of the signals station of Himmler's headquarters (his command train / Triberg).
