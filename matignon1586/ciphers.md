# One cipher, not three: a wrong turn and how it was caught

**This file previously argued that the ten leaves use three different ciphers. That was wrong, and
the argument is retracted.** What follows is the retraction, the evidence that overturned it, and
the lesson, because the mistake is more instructive than the correction.

## What I claimed, and why it was wrong

I compared figure-frequency profiles across leaves. ff. 154 and 173 agreed (`x`, `t`, `a`, `.v.`,
`7` carrying the load); f. 123r looked quite different (`E`, `d`, `q`, `U`); f. 110 different again.
Applying the solved key to f. 123r gave a few French words in a page of noise. I concluded: three
keys, one solved.

The flaw: **I was comparing my own transcriptions, not the manuscript.** I transcribed those pages
in different sittings and my names for the glyph shapes drifted — the same figure written `x` on one
page became `E` or `d` on another. A frequency profile computed over inconsistent labels says
nothing about the cipher. The "evidence" was an artifact of my bookkeeping.

## What overturned it

**The control that should have been run first.** Seed the solver with the *true* Cipher-1 key, then
with scrambled versions of that same key — same symbols, same letter multiset, values shuffled — and
compare. A key that is right will beat its own scrambles; a key that is irrelevant will not.

| seeded with | ff. 123–124 (4,278 figures) |
|---|---|
| **the solved Cipher-1 key** | **−2.35 per figure** |
| scrambled #0 / #1 / #2 | −2.53 / −2.50 / −2.52 |

−2.35 is *better than the −2.40 per figure that a known-correct solution scores* on the solved
leaves. And decoding f. 124r with the solved key, with no search at all, gives:

> **Sire, quelque bo[nne] resolution de les secourir** … **en [R]ouergue** … **province** …
> **que lesdits** … **il luy pla[i]t** …

ff. 123–124 are in Cipher-1. They read badly at first because **f. 123r was the first page I
transcribed in that hand and my figure-reading was poor**, not because the key differed.

## The independent confirmation: a contemporary decipherment

f. 78v (canvas 85 left) carries a cipher block *with its decipherment written down the margin* —
a check on the key that owes nothing to my language model:

> De sorte que je presupose que nous puissions … descharger **la Garonne**, de quatre places qu'ils
> y tiennent, qui sont **Castets, Ste Bazeille, Caumont et le Mas** … **Clerac, Monflanquin** …
> **Montségur** …

`cribem.py` aligns a decode to that plaintext and re-estimates the key from what aligns, repeating.
Seeded with the solved key it reaches **alignment score 106**; six scrambled versions of the same
key reach 3–41, a random start 30. Decoding the block with the solved key directly gives
*"de sorte que je …"*, *"tiennent qui sont …"*, *"pour trois mois …"* — its own margin, recovered.

**So f. 78v and f. 79r are Cipher-1 too**, and the five figure values I reported from a "rouergue"
pattern-match on f. 79r (`4+`=r, `6`=o, `h`=u, `f`=e, `B`=g) are **withdrawn**: they contradict the
solved key, which reads the leaf, so the single pattern hit was chance. One hit in 244 positions is
not evidence; I treated it as evidence because I had already decided the cipher was different.

## Where f. 110 stands

Weakly positive and not settled. Seeded with the solved key a sample scores −2.25 against −2.31 to
−2.35 for scrambles — the right direction but a thin margin — and the decode yields *volontiers*,
*de nostre*, *ce jour*, *attendront* among noise. The hand is tiny and dense, about a hundred
figures to the line, and my transcription of it is the worst in the corpus. The likeliest reading is
the same key and a bad transcription; that is a claim to test, not to assert.

## The lesson worth keeping

Two habits would have caught this on the first day. **Compare against a scrambled control**, not
against your intuition: the scrambled-key test took two minutes and settled in one table what days
of frequency-staring got wrong. And **never compute statistics across transcriptions made in
different sittings** without checking that the labels mean the same thing — the drift is invisible
and it looks exactly like a signal.
