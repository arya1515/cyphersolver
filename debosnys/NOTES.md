# The Debosnys cryptograms (1882–83) — the cipher poem is rhyming couplets; still unsolved

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

## Solve attempt, 15 September 2026 (later): not solved — what was built, tested and excluded

### The sources he copied are English, and there is a clean initials crib

Brown's plagiarism PDF (`brown_plagiarism.pdf`, from Schmeh's 2021 post) traces nearly every clear
"poem" in the papers to **English** sources: Thomas Moore above all (*Lalla Rookh*, *Irish Melodies*,
*Odes of Anacreon*, *Elegiac Stanzas*), plus Thomas Tod Stoddart, Thomas Holley Chivers and
D. C. Colesworthy. Several of the copies are stitched from lines of different poems, and several are in
rhyming couplets. Nick Pelling's 2015 post adds a crib: in No. 9 the clear initials **H. D. D. L. M. F.**
carry dots under each letter giving the number of letters left (H+4 Henry, D+8 Deletnack, D+7
Debosnys), so L, M and F stand for words or names of 7, 7 and 6 letters.

### Two passages transcribed

* `verse_transcription.py` holds the **monographe verse**, all 20 lines: 279 glyph tokens, 111 types,
  52 hapax. It uses a descriptive code (e.g. `N_OX` = tilde over o and x, `SL(o,d)` = slash with circle
  and dot). The 4× half-line crops it was read from are in `glyphs/`. Line 12 lies under a stain and is
  the least reliable. Dotted X is the commonest glyph at 9%.
* `n10_transcription.py` holds the **4 cipher lines on page No. 10**: 99 glyphs, 72 types, 6 pictograms.

Identity decisions are the weak point (tick versus dot over X, variants of the lying S-curl). The type
count is probably too low, not too high.

### What the unit is

`unitstats.py` compares the verse with 279-unit samples of real verse:

| unit | per line | types | top unit | adjacent doubles |
|---|---|---|---|---|
| **cipher glyphs** | **13.9** | **111** | **9.0%** | **7** |
| French syllables | 13.5 | 166 | 3.8% | 0.2 |
| English syllables | 10.2 | 172 | 4.5% | 0.3 |
| English letter pairs | 15.3 | 146 | 4.3% | 0.5 |
| French / English words | 8.6 / 7.3 | 174 / 180 | ~5% | 0.1–0.3 |
| French / English letters | 37.4 / 29.8 | 26 / 23 | 14.7% / 12.7% | 9 |

Only French syllables fit the line length. The rhymes decide between the languages. In real rhyming
pairs the *final syllable* is identical in **61%** of Boileau's couplets but only **31%** of Moore's.
The cipher shows 9 of 10, which has probability about 3 × 10⁻⁴ for English syllables and about 0.05 for
French (higher still for a phonetic rather than orthographic syllabary). So the best-supported reading
is a **French syllabary**, even though his copying habits point to English.

Two things still do not fit cleanly. The top glyph is too frequent for one syllable, and there are too
many adjacent doubles: dotted X is doubled five times, perhaps a single two-part sign. Repeated glyph
bigrams occur at twice the shuffle rate (15 types against 7.3, 95th percentile 11), so the sequence is
language-like and not decoration.

### Cribs and searches tried — all negative

| test | result |
|---|---|
| **No. 10 cipher = lines 1–8 of the clear poem below it** (~93 glyphs, ~91–95 syllables, both end in "?") | Isomorph alignment scores **58**, level with random French verse (median 59, max 66). A planted encoding of the same poem scores 86–88 against a control maximum of 74–80, so the test would have seen it. **Not an encoding of that poem**; most likely the tail of No. 9 |
| **Verse = any 20-line window of 28 French verse volumes** (Racine, Corneille, Molière, Hugo, Chénier, Musset, Gautier, Baudelaire, Verlaine, Boileau, Voltaire; 7,821 couplet windows) | No outlier. A planted encoding of a real window ranks **1st of 7,821** (158 against 127 next), so the search works; the verse's best alexandrine windows are a smooth tail (56, 55, 54…) |
| **Verse = Delille's verse *Aeneid* V**, prompted by the *Aeneid* 5.437 lines copied under the verse | 1,170 windows: max 46, 95th percentile 35, no outlier |
| **Verse = Moore / Stoddart / his own clear English poems**, by line-length profile and couplets | Best correlations 0.6–0.7, at the chance level for 7,000 windows; Moore's couplets also run 3–4 syllables short |
| **"Monograph" reading**: each glyph a stack of letter-marks | Constrained hill-climb over mark→letter keys: real order does not beat the same glyphs shuffled, in French or English |
| **Source of his French poem No. 10** | Not found; its grammar suggests his own composition |

### What remains open

* **Transcribe the rest of the corpus** (No. 9, about 400 glyphs, and the self-portrait page) in the
  same code. A syllabary of ~150 signs cannot be solved from 380 tokens. All ~1,200 give repeated
  sequences a chance, and No. 9 has the H.D.D.L.M.F. crib inside it.
* **Wider French source search**, above all 19th-century popular verse and song (Béranger, romances,
  prison and death poems), the kind he would have copied. The machinery (`versesearch.py`) is ready and
  validated by its planted control.
* **Sektu's full transcription**, if he can be reached: it would settle the identity decisions that
  weaken every test above.

Reproduce: `python verse_transcription.py`, `python unitstats.py`, `python isomorph.py 40`,
`python versesearch.py`, `python shape.py en corpus/debosnys_clear.txt`, `python monogram.py fr 8`.

Images: `c1.png` (self-portrait page, 6 lines), `c2a`/`c2b` (No. 9, long prose passage with
pictograms), `c3.png` (No. 10: 4 cipher lines, then a clear French poem), `c4a`/`c4b` (the monographe
verse). Line crops: `c1_line*.png`, `crops/verse_*.png`.
