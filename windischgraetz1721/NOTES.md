# Windischgrätz brothers, Brussels 18 Nov 1721 (DECODE R5029)

Status: read in part, 21 Sept 2026. Written up as `docs/windischgraetz1721.html`.

Ciphered letter, Brussels, 18 November 1721, catalogued on DECODE as Leopold Viktorin von Windischgrätz to his
brother Ernst Friedrich (DECODE R5029, "Non-decrypted", 8 pp., homophonic + nomenclator, numerical). Holder: SOA
Plzeň, pracoviště Klášter u Nepomuka, Rodinný archiv Windischgrätzů, inv. nr. 1433, karton nr. 202. Catalogue item 68,
class A (rule-scored). Five DECODE images: p2 = first page ("Brüssel den 18. 9bris 721", "Hochgebohrner Graf"),
p3 and p4 = two openings, p5 left = last page (signed "h. C."?), p1 = the same last page seen from the back.

## The key

The DECODE record carries a reconstructed key (`DOC_5029_…xlsx`) by **Jakub Mírka**, 19 June 2023, made from the
brothers' letters of the second half of 1721, most of which have interlinear decipherments. His code list includes codes found in this letter, but no reading of it is published; DECODE says non-decrypted.
Letters: two numbers each, A = 24/36, B = 12/48, C = 23/35 … Z = 1/37 (first column
counts down 24…1 through the alphabet in a fixed shuffle, second = first + 12 or + 36; table in `key.tsv`). Codes
above 48 are a small nomenclator; Mírka identifies 52 affaire, 54 Althann, 85 der/dem, 86 die, 121 geheim, 128 Graff,
135 hat, 145 ich, 152 Kayser, 197 Plan, 198 Prinz, and guesses 99 [Engländer?], 103 [Emp…?], 151 [K…?],
167 [Micosch?], 191 [Ostendische Compagnie], 195 [Pentenrieder], 213 [Starhemberg?]. Ernst Friedrich wrote on 27 Sept
1723 that he had received "the cipher key" with his brother's last letters.

## What was done

1. Images and the xlsx fetched with the project cookie (`decode/`, git-ignored).
2. The letter is German in clear with 13 enciphered passages. All numbers transcribed by eye from the full-resolution
   images: `ct.txt` (clear context in brackets). 181 groups: 122 letter groups, 59 code groups.
3. `dec.py` applies Mírka's table; output `dec.txt`. Every letter-spelled passage gives German at once, which checks
   the key: MIR · NICHT · EXCUSATION ZU MACHEN · HALTET · LIEBE · VERLIEHRET · DES · ZU · ZUSEHE · UNSER AN[…] ·
   VERLIEHRE · SUCCESSION · NIE[H]EMAHLEN ANZUNEHMEN · DIENSTE ZU · GETH[A]N.
4. No cryptanalysis was needed. 148 of 181 groups (82%) have a value; 33 code groups (23 distinct codes) stay open:
   78, 99?, 101, 102, 103?, 111, 130, 131, 139, 146, 149, 151?, 164, 167?, 168, 172, 181, 182, 204, 205, 206, 209, 225.

Slips: "1.39.4" is written with a 2-like flourish before the 4 (read ZUSEHE, not ZUAEHE); 45 (H) stands where A is
wanted in GETHHN and an extra H appears in NIEHEMAHLEN, either the writer's slip or a second value for A not in the key.

## The reading (gist)

The writer, who is at the Congress of Cambrai or close to it, replies to a letter of 1 November:

- The Emperor [103?] will not at all [130 209]; the Emperor himself advised [146] **to make an excuse** (*eine
  Excusation zu machen*). If "I" am supported from there, the advice is good; otherwise not, for [205] **holds**
  under hand, probably also [172] the Prince.
- [205] will surely tell no one, not even Althann. *Manus manum lavat* with [205].
- On the matter of [78] it is hard to believe how not only [151] but everyone **loses** the **love** for [103],
  even the Emperor himself, daily; after the courier finally, after so long, brought **the Prince's plan**.
- [225] has arrived, [103] for over two months [182 101]; the Emperor looks on quite calmly (**zusehe**). The
  [Engländer?] and [111] want to go home, and then **our** [139] and [204] would get little credit … "I" shall
  succumb, the Prince triumph, and the Emperor will rather [168] **lose** [78] and the …
- The Congress should open soon; the courier from Madrid brought Pozobueno the order to reserve, in exchanging the
  renunciations *ratione titulorum*, the article that Windischgrätz agreed with Beretti Landi at The Hague.
- To think of a limit to **the succession** [182] suits him, since he made it a point of honour **never to accept**
  it, so that [182] … "I have the Prince [206]" … for whose **services to** [131], which is shameful.
- Last page: only **to** [149] the Emperor **done** [131]; he asks for his brother's goodwill toward his services and
  his great expenses, and for the Congress to open.

The context (Cambrai, Pozobueno, Beretti Landi, renunciations, the Ostend Company code in the key) fits Ernst Friedrich
von Windischgrätz, imperial plenipotentiary at Cambrai, better than Leopold Viktorin; the direction in DECODE's metadata
is kept but should be checked against the hand of the brothers' other letters.

## Files

- `ct.txt`: the 181 groups by passage with clear context. `dec.py`, `dec.txt`: the reading.
- `key.tsv`: Mírka's letter table and code list, transcribed from the DECODE xlsx.
- `decode/`: images, record page and xlsx (git-ignored).
- Related: `windischgraetz1720/` (Charles VI's letters to L. V. Windischgrätz, keys R5017/R5018 — a different cipher).
