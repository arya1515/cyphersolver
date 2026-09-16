# cyphersolver

An exercise in benchmarking AI on historically "unsolved" ciphers, and in having some fun with them. The targets
are drawn from three standard lists: S. Tomokiyo's
[Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm), Klaus Schmeh's
[Top 50 unsolved encrypted messages](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/),
and Elonka Dunin's [famous unsolved codes](https://elonka.com/UnsolvedCodes.html). Each one is a test of how far an AI
assistant, working with a human, can get on a problem that has resisted people for decades or centuries: how much is
archival research, how much is cryptanalysis, and where it stops. Method: archival research, historical cribs,
19th-century printed editions, and small purpose-built solvers, always run against matched controls so that a
negative result says something.

- **Website:** https://dbourdeau.github.io/cyphersolver/ — hub, priority queue, and formal write-ups (source in [`docs/`](docs/)).
- **Tracker:** [TARGETS.md](TARGETS.md) — every list entry ranked by feasibility, with status, evidence and next step.
- **Per-target record:** each working directory has a `NOTES.md` with sources, dead ends, what is established and what is inferred.

## Results

### Solved

| Target | Date | Result | Where |
|---|---|---|---|
| Richelieu → M. de Rancé, BnF Français 3829 ff. 87 & 89 | 1629 | Homophonic alphabet and nomenclature recovered ciphertext-only; later matched word for word to Avenel (1858), which the catalogues missed | [`richelieu/`](richelieu/) · [write-up](https://dbourdeau.github.io/cyphersolver/richelieu.html) |
| Armstrong → Madison, coded postscript ("THE = 972" code) | 1808 | 49/49 groups read; 580-group code table reconstructed from NARA pencil decodes | [`armstrong/`](armstrong/) · [write-up](https://dbourdeau.github.io/cyphersolver/armstrong.html) |
| Swatow telegram to Sun Yat-sen (JACAR B03050738800) | 1916 | Systematic code condenser over the standard telegraph code recovered by brute force; 41 of ~44 characters read | [`sunyatsen/`](sunyatsen/) · [write-up](https://dbourdeau.github.io/cyphersolver/sunyatsen.html) |
| Huang Xing → Lin Hu and Li Genyuan (JACAR B03050731500) | 1916 | Scheme identified: three kana per character, consonant row carries the digit, vowel free; plaintext read from the JACAR frames | [`sunyatsen/HUANG_NOTES.md`](sunyatsen/HUANG_NOTES.md) · [write-up](https://dbourdeau.github.io/cyphersolver/huangxing.html) |
| Maltravers → Ormonde | 1634–35 | Regular block alphabet and nulls recovered from 59 figures; every spelled word reads; the nomenclator then confirmed clause for clause against Wentworth's dispatches in Knowler's *Strafforde's Letters* (1739). Two person-codes in one clause remain unidentified | [`ormonde/`](ormonde/) · [write-up](https://dbourdeau.github.io/cyphersolver/ormonde.html) |

### Explained: not a cipher, or nothing to read

| Target | Date | Finding | Where |
|---|---|---|---|
| Hyde's ciphered superscriptions | 1659–60 | Dummy numbers "only to puzzle the Enemy", per the 1724 editor and the full Hyde–Barwick key of 1721 | [`hyde/`](hyde/) · [write-up](https://dbourdeau.github.io/cyphersolver/hyde.html) |
| Chinese gold bar cryptograms, Shanghai | 1933 | Almost exactly ten of every letter; flatter than any cipher of a real text can be. No message | [`goldbar/`](goldbar/) · [write-up](https://dbourdeau.github.io/cyphersolver/goldbar.html) |
| D'Agapeyeff challenge cipher | 1939 | The ciphertext is not enciphered English | [`dagapeyeff/`](dagapeyeff/) |
| Beale Paper no. 1 | 1885 | Fabrication; evidence in notes, book-cipher scan over Gutenberg negative | [`beale/`](beale/) |

### Partly read or adjudicated

| Target | Date | Result | Where |
|---|---|---|---|
| Voynich manuscript (Beinecke MS 408) | c.1404–38 | Plain or simply enciphered European language excluded on transliteration-robust entropy; verbose encoding vs structured meaningless text left roughly even, with the separating tests named | [`voynich/`](voynich/) · [write-up](https://dbourdeau.github.io/cyphersolver/voynich.html) |

### Found already solved by others (the lists are stale)

| Target | Date | Solved by | Where |
|---|---|---|---|
| Perwich → Arlington, Paris | 1670 | Matthew Brown; Lasry, Biermann and Tomokiyo (TNA blog, Oct 2025). 20-column transposition with nulls, reproduced here | [`perwich/`](perwich/) |
| Ferdinand III ↔ Cardinal-Infante | 1634–40 | Thomas Ernst, Oct 2017, in the comments of Schmeh's own post | [`ferdinand3/`](ferdinand3/) |
| Milroy telegrams (Union ciphers) | 1861–62 | Richard Bean, 2026; source list has since caught up | [`milroy/`](milroy/) |
| Feynman ciphers #2 and #3 | 1987 | 2023 solution, verified here | [`feynman/`](feynman/) |
| Confederate Navy dictionary code | 1863 | Webster's 1850 dictionary, found solved Aug 2026 | [`barney/`](barney/) |
| ADFGVX messages, Eastern Front | 1918 | Keys published by Lasry, Niebel, Kopal and Wacker; the 22 "unsolved" residue is garbled in transmission. The 2017 thread consolidated: 9 solved, 3 partial, 10 open; Lasry's sixteenth key rebuilt; Norbert's method reimplemented and re-derives 7 pages blind; the 10 open ones resist 15 keys and a key-free attack that fails its own control | [`adfgvx/`](adfgvx/) · [write-up](https://dbourdeau.github.io/cyphersolver/adfgvx.html) |

### Attempted and closed from the evidence

Each of these was attacked with solvers validated on matched controls of the same length and design. The controls solve;
the target does not, and the notes say why.

| Target | Date | Why it stops | Where |
|---|---|---|---|
| SP 53/16 nos. 78-79 and SP 53/22 f. 52 (Mary Queen of Scots papers residue) | 1585 | Numeric ciphers of the Paris-Rheims exile network, 507 and 644 groups. Alphabetical-block design excluded in three languages with a solved English control; a generic homophonic attack fails its own matched control, and f. 52 (84 tokens) is below unicity. Needs the images and SP 53/22 f. 53 as a candidate key | [`sp53/`](sp53/) |
| Louis XIV → duc de Chaulnes, Rome (300-group one-part code) | 1690 | Ciphertext verified from the page images and the code's ten-column Croissy design established, but 300 groups do not determine a 116-entry nomenclator: the annealer recovers 4-12% of a matched control and wrong keys score within noise of the true one. No printed plaintext found. Needs the minute in AE Rome Corr. 331-332 | [`chaulnes/`](chaulnes/) |
| Vatican Challenge Part 5 (Farnese → Poggio) | 1542 | Identified as an Antonio Elio polyphonic-syllabic cipher; Meister key 176/2 verified from the scan and excluded; letter-, lattice- and unit-level attacks fail against controls. Needs the DECODE images or the key | [`vatican5/`](vatican5/) · [write-up](https://dbourdeau.github.io/cyphersolver/vatican.html) |
| Debosnys cryptograms | 1882–83 | Cipher poem is rhyming couplets in a French syllabary, too short for any crib-free attack | [`debosnys/`](debosnys/) · [write-up](https://dbourdeau.github.io/cyphersolver/debosnys.html) |
| Copenhagen cryptogram | c.1950s | Two transcriptions, ten languages, six reading conventions; not a simple substitution of any language tested | [`copenhagen/`](copenhagen/) · [write-up](https://dbourdeau.github.io/cyphersolver/copenhagen.html) |
| Scorpion letters S1 and S5 | 1991 | Below the unicity distance for a homophonic key; controls produce fluent false solutions. The 2018 claim tested | [`scorpion/`](scorpion/) · [write-up](https://dbourdeau.github.io/cyphersolver/scorpion.html) |
| Charles I, Isle of Wight letters | 1648 | Two letters still unread; two candidate keys newly excluded | [`charlesi/`](charlesi/) |
| Berthier → Napoleon; letter to Marmont | 1807–12 | Neither attackable from the single printed source (Vilcoq 1969) | [`napoleon/`](napoleon/) |
| Catokwacopa advertisements | 1875 | Readings audited: which the letters force, which are guesses | [`catokwacopa/`](catokwacopa/) |
| Kaliningrad bottle post | found 2015 | Blocker is transcription from two photographs, not cryptanalysis | [`kaliningrad/`](kaliningrad/) |
| Thomas Urquhart's encrypted poems | 17th c. | Provenance objection to the Aug 2026 claim checked independently | [`urquhart/`](urquhart/) |
| Zhongshan telegrams | c.1938 | No corpus exists online; the premise of the list entry was wrong | [`zhongshan/`](zhongshan/) |
| Koehler cryptograms (Abwehr) | 1944 | Five short letter-cipher messages; skipped as intractable | [`abwehr/`](abwehr/) |
| WW2 censorship-manual steganograms | 1940s | Blocked on image resolution; TNA's digital copy is the same scan | [`censorship/`](censorship/) |
| Colbert passages (Mélanges Colbert) | 1665–74 | Three short passages, no key online, all known series keys fail | [`colbert/`](colbert/) |
| Thurloe State Papers intercepts | 1653–56 | Four short pieces, all period keys fail | [`thurloe/`](thurloe/) |
| D'Estaing → Gérard | 1779 | 217 tokens of a 600-code with no key material; needs the archive copy | [`destaing/`](destaing/) |
| Le Tellier → Castelnau | 1657 | Too short for an unconstrained syllabic solve | [`letellier/`](letellier/) |
| Henry III → Ségur | 1583–86 | Blocked on Gallica access; the sibling cipher's design is known | [`segur/`](segur/) |
| 1520s superscript-digit ciphers | 1526–29 | Blocked: DECODE and BL images need login | [`superscript/`](superscript/) |

### Offline only

Nothing more can be done online; the key or the text is located in an archive.

| Target | Date | What is needed | Where |
|---|---|---|---|
| Charles II → Duke of Hamilton | 1650 | Copy order for NRS GD406/1/2197 (open) | [`hamilton/`](hamilton/) |
| Maurice → Rupert; royalist intercepts, BL Add MS 72438 | 1645–46 | BL volumes digitised but offline since the 2023 cyber-attack | [`rupert/`](rupert/) |
| Stepney → Manchester, Vienna | 1702 | Stepney's office cipher in TNA SP 105/106 or BL Add MSS 7058–78 | [`stepney/`](stepney/) |
| Torcy → Geertruidenberg plenipotentiaries; Villars → Polignac (BL Add MS 61575) | 1710 | The ciphertext itself: Tomokiyo's transcription files are dead links, DECODE R8755/R8756 need a login, the BL volume is not digitised | [`geertruidenberg/`](geertruidenberg/) |

### In progress

| Target | Date | State | Where |
|---|---|---|---|
| "BLUME SALAMANCA" telegrams, Zurich → London | 1937 | Identified as a Spanish transposition; single columnar excluded; double-transposition solvers built and validated. Paused | [`blume/`](blume/) |

### Surveys

- [`top50/`](top50/) — Schmeh's Top 50 cross-referenced entry by entry and re-checked against what has been solved since each post.
- [Why the famous ciphers resist](https://dbourdeau.github.io/cyphersolver/famous.html) — Kryptos, Voynich, Dorabella, Beale, Linear A, Phaistos, the pigeon message, sorted by the actual reason each holds out.

## Repository layout

```
README.md          this file
TARGETS.md         ranked tracker of every list entry
unsolved.htm       snapshot of Tomokiyo's source page, for diffing against later revisions
docs/              the website (GitHub Pages), see below
<target>/          one directory per target: NOTES.md, ciphertext, scripts, small derived data
```

Every target directory except `barney/` has a `NOTES.md`. Large downloads (microfilm, corpora, OCR, run logs, images)
are excluded by [`.gitignore`](.gitignore) and regenerated by the scripts named in each directory's notes.

### The website

`docs/` is served by GitHub Pages. One manifest in [`docs/_build_site.py`](docs/_build_site.py) drives the navigation,
footers with previous/next links, "On this page" strips and the index cards. After editing any page:

```bash
cd docs && python _build_site.py
```

The builder is idempotent. The priority queue on the index page is generated separately from
[`docs/_queue.json`](docs/_queue.json) by `python _build_queue.py`.

## Reproducing the two flagship results

### Armstrong → Madison, 30 August 1808

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
| `armstrong/decode972.py` | merges the three layers and renders any coded passage: `python decode972.py ps\|feb\|all\|table` |
| `armstrong/export_key.py` → `key972.js` | exports the merged 580-group table for the website decoder |
| `armstrong/pencil_score.py` | ranks microfilm frames by amount of faint pencil (finds the annotated despatches) |
| `armstrong/crawl_wb.py` | follows Founders Online correspondent links via the Wayback Machine to list coded letters |

Not in the repo: the 393 roll-13 frames (2.5 GB, from [NARA catalog 188671172](https://catalog.archives.gov/id/188671172)),
roll 14, crops, and the downloaded Founders/LOC pages. The decode reproduces from tracked files alone:

```bash
cd armstrong && python decode972.py all
```

### Richelieu → M. de Rancé, July 1629

Homophonic substitution recovered by ciphertext-only analysis from a published transcription, then found to agree
word for word with the decipherment printed by Avenel in 1858 (*Lettres … du cardinal de Richelieu*, t. III,
pp. 368–369, 381–383). The letters are listed as undeciphered in current catalogues (cryptiana; DECODE R9461–R9462)
and should be marked solved. Full write-up: [richelieu/SOLUTION.md](richelieu/SOLUTION.md).

| file | purpose |
|---|---|
| `richelieu/richelieu1629.txt` | S. Tomokiyo's transcription (source) |
| `richelieu/parse.py` | tokenise transcription, frequency / n-gram stats |
| `richelieu/build_ngrams.py` | build French quadgram model from Gutenberg texts |
| `richelieu/solve.py` | simulated-annealing homophonic solver (`--fix`, `--core`, `--weight`) |
| `richelieu/render.py`, `final.py` | render letters with a hand-built / final key |
| `richelieu/avenel.py`, `avenel_ctx.py` | fetch and search Avenel vol. III OCR (Internet Archive) |

```bash
cd richelieu && pip install requests && python build_ngrams.py && python solve.py --restarts 8 && python final.py
```

## Conventions

- Every claimed reading is graded: **H** read from a primary key source, **C** from a known-plaintext letter, **M** uncertain,
  **I** inferred from context or alphabetical position. The website decoders show the grade per group.
- A negative result is only reported alongside a matched control: a synthetic text of the same length, alphabet and cipher
  design that the same solver does recover.
- Before treating a catalogue item as unsolved, check the 19th-century printed editions (Avenel, Camden Society,
  Nuntiaturberichte) and the comment threads of the list posts. Six items so far were already solved in the open.
- Dates in notes are absolute. Sessions are dated so that "since" claims can be checked against the source lists' last-modified dates.

## Publication drafts

[`papers/`](papers/) holds anonymised HistoCrypt-format drafts of the solved results (two regular papers, one short paper), the
official style files, a shared bibliography, and a README with the verified format rules and the pre-submission checklist.
Unvalidated drafts, not submitted.

## Contact

Daniel Bourdeau, [dnbourdeau@gmail.com](mailto:dnbourdeau@gmail.com). Corrections, prior solutions I have missed,
archive copies, or pointers to key material are all welcome. Issues and pull requests on this repository work too.

## Licence

Text and notes CC BY 4.0; code MIT. Manuscript images are from the Library of Congress, National Archives, BnF, JACAR and
the IACR and remain subject to those institutions' terms.
