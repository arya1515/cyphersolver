# The WW2 censorship-manual steganograms — attempted 15 September 2026, blocked on image resolution

Schmeh's Top 50 No. 33. A British postal-censorship training manual, The National Archives **KV 2/2424**
(scan on Schmeh's blog as `Censor-Manual-WW2.pdf`, 18 page-spread images), gives worked examples of hidden
messages. Two examples state their plaintext but not the mechanics, and nobody has published the readings:

* **Illustration No. 13 (p. 14), a fashion drawing** signed *Mary Helen Shaw*. The manual: *"Message.— (In
  figures 1, 2 and 3). Heavy reinforcements for the enemy expected hourly. (In signature in French
  shorthand)— Before Arras."*
* **Illustration No. 14 (p. 17), part of a map of Amsterdam.** *"The morse letters had to be transposed 11
  positions forward. The message in German when translated read:— Oil has arrived, everything is ready.
  Gustav available for the appointed day."* The facing text names the carrier: *"Morse can be introduced into
  the heavy lining in the print such as tram lines, etc."*

## What was established

**The map's shift runs the way the manual says, and the one published fragment fixes its direction.** In
October 2016 a commenter ("m") read pen marks under the Raadhuisstraat tram band as `AATHUT`; `+11` gives
`LLESFE`, from *ALLES FERTIG*, "everything is ready". So the map carries the German plaintext shifted
**−11**, written as Morse, and a reader shifts **+11** after decoding. `crib.py` checks this and prints the
exact mark sequence that candidate German wordings would put on the map. The stretch around the fragment
should read `.--. .- .- - .... ..- - --. .. -..- ...-` (`paathutgixv`), 29 marks. A full wording such as
*Öl angekommen, alles fertig, Gustav am bestimmten Tage bereit* is about 150–190 marks. Any future reading
of the original can be tested against these mark by mark, not eyeballed.

**The tram bands themselves are not the Morse.** Four bands were unrolled into straight strips
(`bands.py`: Rokin inner and outer, Kalverstraat, Raadhuisstraat) and their inked and blank runs measured.
The segments run 30–90 px with no two-length structure: the ordinary alternating fill of a tram line on a
printed map. The Morse is the much smaller **pen marks added beside a band**, as the 2016 reader described:
thin strokes and small filled blocks hanging off the lower edge of the Raadhuisstraat band east of
Keizersgracht. The manual's "introduced into the heavy lining" means added *to* the lining, not written *as*
it.

**"French shorthand" in the fashion drawing points to Duployé.** Duployé was the dominant French system of the
period. That supports the 2020 blog comment that reads *Arras* in the Duployan strokes of the *H* of *Helen*
(circle *a*, oblique stroke *r*, circle *a*, short curve *s*). It tells against the 2017 reading of *von aras*
in German Stolze-Schrey, which the manual's own caption excludes. Neither reading could be verified at this
resolution.

## Why it stops: the marks are at the resolution limit of every public image

| image | map width | px per mm (map ≈146 mm) |
|---|---|---|
| Schmeh's 2017 photograph, `Censor-Manual-map.png` | 2,437 px | ~17 |
| TNA scan in the manual PDF, page spread | ~1,215 px | ~8 |

The pen marks are 0.1–0.3 mm, so **2–5 px** in the better image, and they touch the band's dark fill. At
native-pixel zoom (`nat_*.png`) strokes and blocks merge. A column-by-column detector (`marks_raad.py`) finds
24 candidate marks along the street, but their widths (1–38 px) do not separate into dots and dashes, and
several are band texture or map lettering. Reading dot against dash reliably needs a direct scan of the
original at 1,200 dpi or better, about 47 px/mm. The fashion drawing's candidate carriers have the same
problem: the dash-and-block trims on the hems, cape and cuffs of figures 1–3, which two blog readers
independently suspected.

**The official download does not help.** The National Archives' free digital copy of KV 2/2424 (115
images, downloaded 15 Sept 2026) is the same digitised scan: the map spread, image 44, is pixel-identical to
the copy on Schmeh's blog (3,491 × 2,809 px), and no image in the file is larger than 3,504 px. The rest of the
file is MI5 correspondence on letter codes. Page 34 is the covering note from the Chief Postal Censor to MI5
(Mr Grogan), 25 November 1943, sending a copy of the "Procedure for use of Overseas Censorships (Code
Section)", which dates this copy of the manual. A sharper image needs new photography of the original at Kew,
either a record-copying order or Schmeh's 2017 photographs at full resolution.

## What would finish it

* **A high-resolution scan of KV 2/2424, pp. 14 and 17** (TNA image ordering, or a researcher at Kew). With
  one, `crib.py`'s predicted sequences turn the map into a mechanical check, and the ALLES FERTIG stretch
  alone confirms the reading.
* For the drawing, the same scan plus a Duployé manual for the signature; the Morse carrier is probably the
  trims of figures 1–3.

Reproduce: `python crib.py` (shift direction and predicted mark sequences), `python bands.py`
(tram-band unrolling and run lengths), `python marks_raad.py` (the resolution-limited mark detector).
Images: `Censor-Manual-map.png`, `Fashion-Drawing-hires.jpg` (Schmeh's photographs), `manual.pdf`.
