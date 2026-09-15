# Beale Paper No. 1 — book-cipher key search (started 2026-09-14)

## Data
- `b1.txt`, `b2.txt`, `b3.txt` — the three ciphers, extracted from the 1885 pamphlet (Wikisource transcription of
  *The Beale Papers*, pages 20–22). B1: 520 numbers, max 2906, 298 distinct. B2: 762 numbers, max 1005. B3: 618, max 975.
- `doi_words.txt` — the pamphlet's own numbered Declaration of Independence (1322 words, aligned to the pamphlet's
  every-10th-word markers). Decodes B2 to the known plaintext (with the known transcription errors).
- `doi_pg1.txt` — Gutenberg #1 Declaration (different word count; used as the "drifted edition" control).

## Harness (`bookcipher.py`)
- key modes: `first` (initial letter of word n), `last`, `second`, `letter` (nth letter of the text).
- `scan`: every start offset of a text at once via FFT cross-correlation of per-position letter log-likelihood
  ratio (English text letters vs. initial-letter background). Robust z over all offsets of the same text.
- Drift problem: a few word-count discrepancies between the encoder's edition and ours destroy a global
  alignment past that point (B2 vs Gutenberg #1 drops from z 7.4 to z 3.4). Fix = two stages:
  - `stage1`: numbers split into magnitude bands (1–100, 101–300, 301–700, >700); each band scanned at every offset;
    bands ≥2 allowed a sliding-max drift window (±10/20/40); top-3 offsets by mean LLR.
  - `stage2`: quadgram score of the decode with per-band shifts optimised by coordinate ascent.
  - Calibration: true key (B2 vs Gutenberg #1) → quad −12.1 with correct plaintext; false alignments in novels
    −15 to −17; a run of e's from last-letter streams can reach −13.0 (hence per-mode hit thresholds).
- A fully free per-band DP (`scan_drift`) over-fits (finds e-rich regions) — kept but not used.

## Corpus run (`scan_corpus.py`, `run_shards.sh`)
- All English Gutenberg (HF `sedthh/gutenberg_english`, 37 parquet shards, ~48k books), streamed: download →
  scan (10 processes) → delete. Combos: first×{b1,b2,b3}, last×b1, letter×b1.
- Output: `results_gutenberg.tsv` (top-1 per book/mode/cipher), `results_gutenberg.tsv.hits` (stage-2 hits).

## Results so far
- B2 positive control: detected as the only hit in the test shard (Gutenberg #1 DOI, quad −12.09).
- Pamphlet DOI vs B1: nothing (all modes, with drift). Gillogly's alphabetic strings reproduce
  (pos 187–206 = `abcdefghiijklmmnohpp`), i.e. the writer of B1 had the numbered DOI in hand.
- DOI-keyed decode of B1 as a second-layer simple substitution: hill-climb score −14.2 = same as a shuffled control.
- Pamphlet's own narrative as key: nothing.
- Repeated adjacent number pairs (language signature): B2 z=+6.8 vs shuffled; B1 z=−0.3; B3 z=−1.1
  (low power for B1 because of its many homophones, but no positive signal).
- DOI-initial histogram test: for numbers ≤1322 decoded through the pamphlet DOI, B1's letter histogram is
  indistinguishable from random picks jittered ±5 words (z=−1.0); B2 z=+16; B3 z=+1.8 (n.s.).
  Consistent with B1's numbers being chosen off the numbered DOI without encoding English through it.
- Internet Archive OCR candidates (`extra/`, `run_extra.py`, `extra_results.txt`): Pike 1810 (cihm_46872),
  Lewis & Clark 1814 (historyofexped01/02lewi), Jefferson's Notes 1787 & 1800, Webb's Freemason's Monitor
  1808 & 1818 — all modes, all three ciphers: no hits.
- Corpus positive controls seen so far: Gutenberg #300 (DOI) and #1866 (compilation containing the DOI at word
  ~141k) both flagged for B2 with the right plaintext → the scan finds a key buried mid-book.

## Conclusion (2026-09-14, stopped by user)
Called a fabrication. Corpus scan stopped after 3 of 37 English shards (4,254 books; results in
`results_gutenberg.tsv`, hits in `results_gutenberg.tsv.hits`). Only genuine hits were the B2 positive controls
(Gutenberg #300 Declaration; #1866 compilation containing the Declaration). Every B1 "hit" was an artifact
(index/TOC regions rich in the/and/of initials scoring for all three ciphers alike; e-runs from last-letter
keying). Basis for the verdict: Gillogly alphabet strings; DOI-initial histogram = random picks (z −1.0);
no repeated-pair language signature; no second-layer substitution; Nickell's anachronisms in the "1822" letters.
To resume the corpus scan: `./run_shards.sh` (skips shards marked in `done/`).
