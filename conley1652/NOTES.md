# "Mr. Conleys Hand" (Paris) 1652–53: two royalist letters in Abraham Cowley's hand (BL Harley MS 7003; DECODE R7768, R7769; catalogue 137)

The clear text of both letters is read (`transcription.txt`). The cipher is 23 numbers in five short runs: one
three-group name, three spelled-out runs and one single group (`codes.txt`). They are not read. That is too
little text to break the code without a key, no key is on DECODE or in print, and the Hyde–Barwick key does not
fit. One hypothesis is graded M below. The catalogue entry stays, as "attempted, open".

## Source

- British Library, Harley MS 7003 ff. 314r–315r. DECODE R7768 (images f.314r and f.314v) and R7769 (f.314v and f.315r).
  DECODE images the same leaf, f.314v, on both records (byte-identical files). The images are BL copyright and git-ignored.
- The docket after letter 1 reads "mr Cowleys Hand". DECODE misread it as "Conleys" and made it the author.
  Abraham Cowley was cipher secretary to Lord Jermyn and Queen Henrietta Maria in Paris, and "cypher'd and
  decypher'd with his own hand" most of their letters (Sprat, 1668; CELM, *Cowley*). The copy is a clean
  later-looking fair copy. The docket says whose hand the original was in, so the sender is Jermyn's office at
  the Queen's court. Cowley or Jermyn himself are both possible: "she [the Queen] intends to write to you" and
  "the money for which I engaged myselfe to you".
- The recipient is a royalist in Holland. He writes on the Dutch war and the King's journey into Holland, he has
  a son, and he is short of money. It is not Nicholas, who is named in the third person, and not Hyde ("Mr
  Chanchellour"). He is not identified.
- Letter 1: Paris, 28 Dec 1652. Letter 2: Paris, 3 May 1653. The lower half of f.315r begins a third,
  unrelated letter ("My Lo:", writer at the Hague). It has no cipher on the imaged part.

## The cipher

Numbers separated by colons, set into clear English. In letter order:

| where | groups | context |
|---|---|---|
| L1 | 228:196:188 | "the present estate of ___ … assistance to be sent thither against next spring" |
| L1 | 102:43:97:133:52:180 | "you will not be informed of by ___" (a person) |
| L1 | 57:102:58:20:30 | "concerning ___ dispatch back" (a person) |
| L1 | 248:88:46:47:96:52:7:57 | "the person that came lately from ___" (a place) |
| L2 | 203 | "write a word to Mr ___" (a person) |

Values run from 7 to 248. The runs of five, six and eight numbers look like names spelled letter by letter, with
the higher numbers probably homophones or syllables. 228:196:188 and 203 look like code words. Repeats: 102 (twice),
52 (twice), 57 (twice).

**Hypothesis (M).** The place is "Scotland": s c o t l a n d = 248 88 46 47 96 52 7 57. The Glencairn rising
was being raised in the Highlands that winter, and the royalists at Paris were looking for "assistance … against
next spring". If so, 52 = a and 57 = d, and the third run begins with d. Nothing else checks it: no other run
shares enough letters. 228:196:188 would then be Scotland or the Highlands as a code word. Not verified; grade M.

## What was tried (21 Sept 2026)

1. **Access.** Downloaded the four DECODE images with the saved cookie. Found the duplicate f.314v.
2. **Transcription.** Transcribed both letters in full (`transcription.txt`), 23 code numbers.
3. **Print.** *Miscellanea Aulica* (1702), which prints Cowley's fifteen letters to Henry Bennet
   (30 Apr 1650 – 13 Sep 1653), was searched in the archive.org full text (miscellaneaauli00browgoog). Neither
   letter is there. Web searches of distinctive clear phrases found nothing.
   Not checked: the Clarendon State Papers calendar, and Nethercot, "The Letters of Abraham Cowley" (MLN 43, 1928).
4. **Sibling key.** The Hyde–Barwick key (`hyde/barwick_key.py`, 1659) gives gibberish ("much at vi",
   "ma p ka ar s ru"). Ruled out.
5. **Ciphertext-only.** Not attempted: 23 numbers in five runs cannot fix a key.

## What would move it

A Jermyn/Queen cipher of 1652–53 (Clarendon MSS, Bodleian; Nicholas papers), or the original letters, which may
carry interlinear decipherment. The recipient could be identified from the son and the promised money.
