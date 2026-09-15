# The Kaliningrad bottle post — the blocker is transcription, not cryptanalysis

Found in 2015 by roadworkers at Baltiysk, the former Pillau, in a brown Soviet-era bottle: two sheets
of lined notebook paper in blue ink, roughly a thousand characters in seven sections. It is number 19
on Schmeh's Top 50, and it is the only entry on that list with enough ciphertext for statistics.

## Why it was worth attacking

Two things put it near the top of the queue. It has more text than anything else still open there.
And it carries an unfinished lead: a commenter said in February 2021 that the plaintext comes from
the **1876 Russian Synodal Bible** and promised the method, then never posted it, and the blog closed
twenty-two months later. A named crib against a digitised text is a testable proposition.

## What stopped it

**There is no transcription.** The cryptogram exists only as two photographs. Everything published
about it — the index of coincidence of 0.054, the 37-character alphabet, the frequency count — was
derived by readers from those images, and none of them published the character string they worked
from.

Transcribing it here was attempted and abandoned on honest grounds. The ink is faint, the hand is
cursive, and the reverse side bleeds through badly enough that contrast enhancement makes some lines
worse rather than better. The fatal problem is that cursive `n`, `u`, `v` and `w` are barely
separable in this hand, and the published alphabet contains all four plus primed variants of several.
An error rate of even a few percent over a thousand characters would wreck any substitution analysis,
and would do so invisibly — producing a plausible-looking failure rather than an obvious one.

## What is observable, and one thing that seems unremarked

From the images at full resolution:

* The alphabet is **a b c d e f g h i k l m n o r s t u v w z** plus **d' f' h' l' m' n' n" r' s' t'
  z'**, plus **ö ü ê**, and an underlined e and n. **No j, p, q, x or y.**
* The primed consonants are worth noting: **d' l' n' s' t' z'** is exactly the set that carries the
  apostrophe when Russian palatalised consonants are transliterated into Latin. That is independent
  support for the Russian hypothesis, and it suggests the apostrophes are part of the plaintext
  transliteration scheme rather than cipher decoration.
* Running through the text are **dotted initialism groups**: `z.s.f.d.`, `c.f.`, `z.f.b.`, `s.n.c.`,
  `z.b.n.`, `n.t.d.` Short, full-stopped letter groups of two to four, scattered through running
  text. I did not find these discussed in any of the published commentary. In a Bible-derived text
  they would be a natural place for book-chapter-verse references, which would make them the best
  available crib — a Synodal Bible citation has a rigid shape.

## Status

Not attempted beyond this, because the input does not exist in a usable form. The productive first
step is not cryptanalysis but a careful transcription from the originals or from higher-resolution
photographs than the two published ones, ideally by someone who can handle the hand. Until that
exists, the 0.054 coincidence index and the 37-character alphabet are the only numbers anyone has,
and they are not enough to work with.

Images: `Kaliningrad-Cryptogram1.png`, `Kaliningrad-Cryptogram-2.png`, and a reader's frequency count
in `Kalinigrad-Frequencies.png`.
