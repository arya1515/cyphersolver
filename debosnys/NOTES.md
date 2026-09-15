# The Debosnys cryptograms (1882–83) — the alphabet is systematic, and that changes the estimate

Henry Debosnys murdered his wife Elizabeth in Essex County, New York, and was hanged in April 1883.
He left four encrypted passages, written in jail. Number 3 on Schmeh's Top 50, and by his own account
almost nobody has worked on them.

## The stated bottleneck is real

There is no machine-readable transcription. Six scans circulate — one page with a self-portrait and
six lines of symbols signed *H. D. Debosnys*, plus five more — and every published description of the
alphabet is qualitative. Nothing can be computed without a symbol sequence, and producing one is a
vision job before it is a cipher job.

## What the scans show, which the descriptions do not

The alphabet is usually described as large and decorative. Read closely at three times scale, most of
it is not decorative at all: it is **systematic composition**.

A large share of the glyphs are a **small base carried under a diacritic**. The bases that recur are
plain `o`, `x` and `w`; the marks are a tilde, a dot above, a bar, a double bar, a triple stroke, a
slash and a small ring. So `õ`, `ẋ`, `x̄`, `x̃x`, `ō x`, `⇗o` and so on are not separate inventions but
one base plus one mark. Symbols repeat across lines — `õ` and `ẋ` both appear twice in the first line
alone, and `ẋ` again in the fifth.

Set against that are a handful of **pictograms**: a horse, a sun with a face, a tree, a human figure.
Those are not letters. In a cipher of this period and this kind they are nomenclator entries — a word
or a name apiece.

If that reading holds, the effective alphabet is far smaller than "large and decorative" implies: a
few bases times a few marks, plus a set of one-off pictograms for words. That is a much better
prospect than the descriptions suggest, and it is the kind of structure a self-taught cipher-maker
actually builds.

## The lead worth pairing with it

Matthew Brown showed in 2021 that Debosnys plagiarised his *unencrypted* poems and paintings — from
Thomas Moore and from *Peterson's Magazine*. If the encrypted passages hide copied published text
too, this stops being a cipher problem and becomes a known-plaintext hunt across a digitised corpus,
which is exactly the shape of the Beale work in this repository.

That lead only becomes usable once a transcription exists, because a crib search needs a symbol
sequence to search with.

## What was not done

A full transcription. Six images, several hundred glyphs, and the honest difficulty is not reading
them but deciding identity — whether two similar composites are the same symbol or two different ones.
Getting that wrong is invisible: it produces a plausible-looking failure rather than an obvious one,
and at a few percent error the index of coincidence and every frequency statistic become unreliable.

The right next step is a careful glyph-by-glyph inventory built from all six scans at once, so that
identity decisions are made against the whole corpus rather than line by line. That is a bounded
piece of work and it is the thing standing between this cryptogram and any analysis at all.

Images: `c1.png` (the self-portrait page) and `c2a`–`c4b`; line crops of the first at `c1_line*.png`.
