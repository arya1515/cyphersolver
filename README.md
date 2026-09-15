# cyphersolver

Attempts on historically "unsolved" ciphers — the items in S. Tomokiyo's
[Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm) list — using archival research,
historical cribs and small purpose-built solvers.

**Website:** https://dbourdeau.github.io/cyphersolver/ — hub with the status of every target and formal write-ups of the
solved items. **Tracker:** [TARGETS.md](TARGETS.md) — all 20 targets ranked by feasibility, with status and notes.

| Target | Date | Result | Where |
|---|---|---|---|
| Armstrong → Madison, coded postscript ("THE = 972" code) | 1808 | **solved** — 49/49 groups; 580-group code table reconstructed | [`armstrong/`](armstrong/) · [write-up](https://dbourdeau.github.io/cyphersolver/armstrong.html) |
| Richelieu → M. de Rancé, BnF Français 3829 ff. 87 & 89 | 1629 | **solved** — ciphertext-only reconstruction; later matched word for word to Avenel (1858) | [`richelieu/`](richelieu/) · [write-up](https://dbourdeau.github.io/cyphersolver/richelieu.html) |
| Maltravers → Ormonde | 1634–35 | **alphabet solved** — regular block key + nulls recovered from 59 figures; spelled words read, nomenclator inferred | [`ormonde/`](ormonde/) · [write-up](https://dbourdeau.github.io/cyphersolver/ormonde.html) |
| Hyde's ciphered superscriptions | 1659–60 | **explained** — dummy numbers, per the 1724 editor and the full Hyde–Barwick key | [`hyde/`](hyde/) · [write-up](https://dbourdeau.github.io/cyphersolver/hyde.html) |
| Charles II → Duke of Hamilton | 1650 | offline only — key located at NRS GD406/1/2197 (open); needs a copy order, nothing more to do online | [`hamilton/`](hamilton/) |
| Prince Maurice → Rupert (1645) and royalist intercepts, BL Add MS 72438 (1646) | 1645–46 | offline only — keys/texts are in BL volumes digitised but offline since the 2023 cyber-attack | [`rupert/`](rupert/) |
| Vatican Challenge Part 5 (Farnese → Poggio) | 1542 | stuck — polyphonic digit cipher; solvers built, paused | [`vatican5/`](vatican5/) |
| Colbert passages (Mélanges Colbert) | 1665–74 | stuck — three short passages, no key online, known series keys fail | [`colbert/`](colbert/) |
| Thurloe State Papers intercepts | 1653–56 | stuck — four short pieces, all period keys fail | [`thurloe/`](thurloe/) |
| Stepney → Manchester, Vienna 1702 | 1702 | offline only — MS transcribed from Yale IIIF; key (Stepney's office cipher) in TNA/BL | [`stepney/`](stepney/) |
| Beale Paper no. 1 | 1885 | fabrication — evidence in notes | [`beale/`](beale/) |

Every working directory except `barney/` has a `NOTES.md` with the record of the attempt (sources, dead ends, what is
established and what is inferred).

---

## Armstrong → Madison, 30 August 1808 — coded postscript

John Armstrong (U.S. Minister to France) ended a private letter to Madison with 49 groups of the diplomatic code he used
1804–1810, in which 972 = *the*. The code was never published. It was reconstructed from the State Department's own
pencil interlinear decodes on NARA microfilm M34 roll 13 (frames 0192–0201, a despatch of October 1806), merged with
Tomokiyo's known-plaintext values from the letter of 4 May 1806, and completed by alphabetical-slot inference. Reading:

> Russel ought to be the consul: he is an American by birth, and is much better qualified than any other candidate. In a
> word, he is above men in general. Next to him in fitness is O'Mealy, but he is, like Warden, an Irishman.

| file | purpose |
|---|---|
| `armstrong/NOTES.md` | group-by-group evidence, corrections to the Founders transcription, residual doubts |
| `armstrong/pairs.txt` | ~500 number → syllable pairs read from the pencil decodes, with frame/line reference and H/M grade |
| `armstrong/code972_partial.json` | Tomokiyo's table from the 4 May 1806 known plaintext (base layer) |
| `armstrong/decode972.py` | merges the three layers and renders any coded passage — `python decode972.py ps\|feb\|all\|table` |
| `armstrong/export_key.py` → `key972.js` | exports the merged 580-group table for the website decoder |
| `armstrong/pencil_score.py` | ranks microfilm frames by amount of faint pencil (finds the annotated despatches) |
| `armstrong/crawl_wb.py` | follows Founders Online correspondent links via the Wayback Machine to list coded letters |

Not in the repo (see `.gitignore`): the 393 roll-13 frames (`img13/`, 2.5 GB, from
[NARA catalog 188671172](https://catalog.archives.gov/id/188671172)), roll 14, crops, and the downloaded Founders/LOC pages.
Reproduce the decode from tracked files alone: `cd armstrong && python decode972.py all`.

## Richelieu → M. de Rancé, July 1629 (BnF Français 3829, ff. 87 & 89)

Homophonic substitution cipher recovered by ciphertext-only analysis from a published transcription, then found to
agree word-for-word with the decipherment printed by Avenel in 1858 (*Lettres … du cardinal de Richelieu*, t. III,
pp. 368–369, 381–383). The letters are listed as undeciphered in current catalogues (cryptiana; DECODE R9461–R9462);
they should be marked solved. Full write-up: [richelieu/SOLUTION.md](richelieu/SOLUTION.md).

| file | purpose |
|---|---|
| `richelieu/richelieu1629.txt` | S. Tomokiyo's transcription (source) |
| `richelieu/parse.py` | tokenise transcription, frequency / n-gram stats |
| `richelieu/build_ngrams.py` | build French quadgram model from Gutenberg texts |
| `richelieu/solve.py` | simulated-annealing homophonic solver (`--fix`, `--core`, `--weight`) |
| `richelieu/render.py`, `final.py` | render letters with a hand-built / final key |
| `richelieu/avenel.py`, `avenel_ctx.py` | fetch and search Avenel vol. III OCR (Internet Archive) |

Reproduce: `pip install requests` · `python build_ngrams.py` · `python solve.py --restarts 8` · `python final.py`

## Vatican Challenge Part 5 (ASV Segr. di Stato, Spagna 1A; Farnese → Poggio, 15 April 1542)

Digit cipher with dotted digits, apparently variable-length polyphonic (cf. Lasry, Megyesi & Kopal, *Cryptologia* 2021,
§5.5, where the same collection is left unsolved). Work in `vatican5/`: unit/statistics tools (`units.py`, `mi*.py`,
`dots*.py`, `partition.py`), an Italian character LM built from Nuntiaturberichte OCR (`build_it_lm.py`, `ngrams5.py`),
Python solvers (`solver5–7.py`), a C# lattice solver (`native/Program5.cs`, compile with `csc.exe`; ~180 it/s), and a
synthetic-key harness (`make_syn.py`, `syn_fix.py`, `lmscore.py`, `wordscore.py`) used to show the solver recovers a
known key of the same design. Findings and negative results in `vatican5/NOTES.md`. Paused.

## Other directories

- `hamilton/` — Charles II → Hamilton 1650: collation of the two printed witnesses (`collate.py`), structure notes, and the
  archive reference for the surviving cipher keys (NRS GD406/1/2197). Blocked on a copy order; see `hamilton/NOTES.md`.
- `rupert/` — Maurice → Rupert 1645 ciphertext (`maurice1645.py`) and the Add MS 72438 intercepts: key locations mapped
  (BL Add MS 18980–82, 72438), all offline; see `rupert/NOTES.md`.
- `colbert/` — Mélanges Colbert passages: assessment, Gallica/DECODE tooling; stuck.
- `ormonde/` — Maltravers–Ormonde 1634–35: ciphertext, `analyze.py` (null test, grid scan, hill-climb), page scans, notes.
- `hyde/` — Hyde–Barwick 1659–60: `barwick_key.py` (full 1721 key, 643 entries) + the four superscriptions decoded; notes.
- `thurloe/` — Thurloe intercepts: extracted texts, `apply_keys.py` (all cryptiana period keys), Dutch/French LM solvers; notes.
- `stepney/` — Stepney–Manchester 1702: transcription from Yale IIIF images, THE=454 test, notes.
- `beale/` — book-cipher scanner over Gutenberg (`scan_corpus.py`, `bookcipher.py`); notes arguing fabrication.
- `milroy/`, `feynman/`, `barney/` — items that turned out to be already solved by others; tooling and notes kept for reference, not tracked.
- `docs/` — the website: `index.html` (hub), `armstrong.html`, `richelieu.html`, `ormonde.html`, `hyde.html`, shared `style.css` / `site.js`.

## Conventions

- Large downloads (microfilm, corpora, OCR, run logs) are excluded by `.gitignore` and regenerated by the scripts noted above.
- Every claimed reading is graded: **H** read from a primary key source, **C** from a known-plaintext letter, **M** uncertain,
  **I** inferred from context/alphabetical position. The website decoders show the grade per group.
- Before treating a catalogue item as unsolved, check the 19th-century printed editions (Avenel, Camden Society, Nuntiaturberichte).

## Licence

Text and notes CC BY 4.0; code MIT. Manuscript images are from the Library of Congress, National Archives and BnF and remain
subject to those institutions' terms.
