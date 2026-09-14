# cyphersolver

Attempts on historically "unsolved" ciphers, using statistical cryptanalysis plus archival research.

## Richelieu → M. de Rancé, July 1629 (BnF Français 3829, ff. 87 & 89)

**Website:** https://dbourdeau.github.io/cyphersolver/

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
| `docs/index.html` | the website (self-contained) |

Reproduce: `pip install requests` · `python build_ngrams.py` · `python solve.py --restarts 8` · `python final.py`

## Barney → Mallory dictionary code (CSS Harriet Lane, 1863)

Started, then found already solved (Aug 2026, Webster's Primary School Dictionary 1850). Notes in `barney/`.
