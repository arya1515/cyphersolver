# "BLUME SALAMANCA" telegrams, Zurich → London, 8 January 1937 — in progress

Two telegrams sent from Zurich via London (one annotated *via Angleterre Eastern*) to Spain on 8 January
1937. Both begin *BLUME SALAMANCA*, then five-letter groups. They were found by the historian Regula Bochsler in
the Swiss Federal Police files on Werner Oswald, founder of the Emser Werke (Bochsler, *Nylon und Napalm*,
2022), and posted by Klaus Schmeh on Facebook. Oswald told the police they concerned "wool business" in Spain;
Bochsler doubts it, given his ties to Franco's side. Salamanca was Franco's headquarters in January 1937.
Tomokiyo's catalogue notes that the index of coincidence is English-like, suggesting a transposition.

## Transcription

Only the first telegram is reachable. The photograph embedded in Schmeh's Facebook post was retrieved at
1,134 × 1,012 px; the second telegram is not in the public preview. `tg.py` holds **123 groups, 615 letters**.
The transcription checks against the form: 123 groups + BLUME + SALAMANCA = **125 words**, the figure written in
the *Wörter* box, and the pencilled (50) and (100) fall at the right groups. Group 121 (`RBEEP`) has a red
line through it on the original, but it is counted in the 125.

## What is established

**It is a transposition, and the language is Spanish.** The index of coincidence is **0.0699**, a natural
language rather than a code or a polyalphabetic cipher. Letter frequencies in place fit Spanish best
(chi-squared 102, against French 150, English 207, Italian 217, German 582), with e 11.9, o 11.2 and a 9.4 at
the top. A transposition keeps every letter as itself, so the plaintext is Spanish with some padding: `x` is 6
of 615 (e.g. `ANANX`, `REFLX`), which suggests telegraphic stops or fillers, and `p` runs high.

**It is not a single columnar transposition.** A simulated-annealing search over column orders at every width
from 4 to 20, scored with Spanish quadgrams (`trans.py`), tops out at −6.03 per quadgram. Real Spanish scores
−4.1 and shuffled letters −6.3. The same search, run on planted Spanish transpositions of the same length,
reaches −4.8 at widths 9, 14 and 19. So a single columnar key would have been found.

## What is not yet excluded

**Double columnar transposition**, the standard hand system of the period. `double.py` alternately
hill-climbs two column orders. On planted double transpositions it recovers widths 8/11 and 7/11 but misses
6/9, 10/12, 12/5 and 13/17, about **1 in 4** at these settings. A negative sweep with this tool therefore
excludes nothing. Solving double transposition at 615 letters is within reach of specialised solvers such as
Lasry's, not of this one.

## What would move it

* A stronger double-transposition solver (Lasry-style, with segment-based moves and restarts at scale), run
  over widths up to about 20.
* **The second telegram**, from Bochsler or Schmeh. Two messages of the same day very likely share keys, and
  equal-length messages under the same double transposition can be attacked jointly (multiple anagramming).
* Context cribs: Spanish commercial or military vocabulary of January 1937 (lana, envío, pesetas, Salamanca,
  Burgos, and names from Oswald's circle).
