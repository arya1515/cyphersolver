# The Debosnys cryptograms (1882–83) — the cipher poem is rhyming couplets, and that fixes the unit

Henry Debosnys murdered his wife Elizabeth in Essex County, New York, and was hanged in April 1883.
He left four encrypted passages, written in jail. Number 3 on Schmeh's Top 50. Unsolved: nobody has
published a decryption of a single word (checked September 2026).

## Prior work this project had missed

An earlier version of these notes (15 September 2026) presented the systematic composition of the
glyphs as a new observation. **It is not new.** Brian of the *Sektu* blog made a full transcription in
2017 and got further:

* **1,188 glyph tokens of 425 types**, with 277 types occurring once
  ([transcription revision](https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html)).
* A second, **sub-glyph** transcription that decomposes each glyph into ordered components, e.g. the
  signature line `C2B2 XP NU ZOO OM2N SHI` → `<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`, with a
  small grammar for glyph construction. Sub-glyph frequencies follow Zipf's law.
* The **"N-glyphs"**: the tilde (N) never stands alone, only at the top of a glyph or under another N.
  He proposed it marks **nasalization**. The cipher poem averages 1.5 N-glyphs a line, against 2.05
  nasal syllables a line in Baudelaire's alexandrines.
* The working hypothesis that **glyphs are French syllables** and sub-glyphs are phonemes.

That transcription does not appear to have been released: the blog posts describe it without linking
a file, and none turns up in Nick Pelling's 2021 review of Sektu's work. So there is still no public
machine-readable text. Separately, Schmeh's page *Henry Debosnys was a
copyist* documents the plagiarism of his clear poems (Matthew Brown, 2021: Thomas Moore, *Peterson's
Magazine*).

## New here: the "monographe verse" is twenty lines of rhyming couplets

The passage headed *monographe verse* (`c4a.png`, 15 lines, continued on `c4b.png`, 5 lines, signed
*Hênêcos Debosnostys*) is the 20-line cipher poem. Read line by line at three times scale
(`crops/verse_a01`–`a15`, `verse_b01`–`b05`), **the last glyph of each line repeats in pairs**:

| lines | final glyph | lines | final glyph |
|---|---|---|---|
| 1–2 | tilde-curl | 11–12 | delta |
| 3–4 | dotted X | 13–14 | o + cross (lower right / above) |
| 5–6 | Y with ring | 15–16 | dark note with arrow, two dots below |
| 7–8 | barred o | 17–18 | tilde-curl |
| 9–10 | venus sign | 19–20 | curly X |

* Within couplets the final glyphs are **identical in 9 of 10**. The tenth pair shares its base (an o
  with a cross) and differs only in where the cross sits, which under the composition model is a
  near-rhyme.
* Across couplet boundaries (lines 2–3, 4–5, …) they match in **0 of 9**.
* Even if any two glyphs matched 20% of the time, 9 of 10 would arise by chance with probability
  4 × 10⁻⁶; at a more realistic 5–10%, 10⁻⁸ to 10⁻¹¹.
* The couplet-1 rhyme returns at couplet 9, as a recurring rhyme sound would.

That is ***rimes plates***, AABBCC…, the standard French couplet form. Three consequences:

1. **The line-final glyph encodes sound.** Identical final glyphs on rhyming lines mean a glyph stands
   for a phonetic unit carrying the rhyme, not an arbitrary word code. That supports Sektu's
   syllable hypothesis over a word-level or letter-level reading.
2. **The count fits syllables and nothing else.** Glyphs per line, excluding punctuation, run 11–17
   (mean 13.7, ±1 segmentation uncertainty; lines 11–13 lie under a stain). Debosnys's own clear French
   verse, poem No. 10 on `c3.png`, runs **6–11 words** and **24–42 letters** a line, with roughly
   **9–15 syllables**. The glyphs sit at syllable scale, slightly high, as a few pictograms and
   compound marks would make them.
3. **It turns the known-plaintext hunt into a shape search.** Given Brown's plagiarism finding, the
   natural candidate is a *copied* French poem, or a 20-line excerpt: alexandrine-scale rhyming couplets
   whose first and ninth couplets share a rhyme and whose other eight rhymes are distinct. The
   line-final punctuation adds a fingerprint (`, · - - , . , , , . , . · · · · · . · ·`, where · is
   none). The search needs no glyph identity decisions beyond the line endings.

`python verse.py` reproduces the counts and the chance figures.

## What remains open

* **The shape search itself.** It needs a corpus of French verse (Gutenberg, Wikisource), which is not
  in this repository. Candidates that pass the rhyme-and-punctuation fingerprint can then be checked
  against the internal glyph repeats, and at that point a transcription is needed.
* **A transcription.** The honest difficulty is still identity: whether two similar composites are the
  same symbol. The rhyme pairs help here too, since each pair gives one confirmed identity. Sektu's
  unreleased transcription would save most of the work, so asking for it is the obvious first move.

Images: `c1.png` (self-portrait page, 6 lines), `c2a`/`c2b` (No. 9, long prose passage with
pictograms), `c3.png` (No. 10: 4 cipher lines, then a clear French poem), `c4a`/`c4b` (the monographe
verse). Line crops: `c1_line*.png`, `crops/verse_*.png`.
