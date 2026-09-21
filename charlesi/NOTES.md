# Charles I in the Isle of Wight — the two unread letters (1648)

Four of the King's ciphered letters from his captivity were solved in 2021 by Norbert Biermann,
Thomas Bosbach and Matthew Brown, working in the comments of Klaus Schmeh's Cipherbrain blog, and
their reconstructed nomenclator is published. Two letters remain unread:

* **22 May 1648, to Edward Worsley** ("Z"), 112 code groups, printed in Albin's *History of the Isle
  of Wight* (1795) p.237
* **1 August 1648, to Prince Charles**, 88 code groups, printed in *Original Letters*

The task here was the cheapest decisive test on the whole target list: does the published key open
them? It does not, and this note establishes that with numbers rather than by eye, then goes on to
kill the most promising alternative key as well.

**Result: both letters remain unread. Two candidate keys are now excluded, one of them for the first
time.**

---

## 1. The published key, made machine-readable

`key.py` transcribes the Biermann/Bosbach/Brown nomenclator from the solvers' own published table
(`img/Nomenclator-Charles-I.png`). It is a homophonic substitution with a word list:

* **a–h** take descending runs: 9 8 7 6 5 4 3 2, again 19 18 17 16 15 14 13 12, and again 90 80 70 60 50
* **i–s** take ascending runs: 21–30, 31–40, 41–49 (s displaced to 51 because 50 is already e)
* **t–z** take 52–57, 62–67, 72–77; s picks up 61 and 71 as well; h picks up 20
* **nulls** 1, 10, 58, 68, 69, 78, 100–107
* **words** 142–615, roughly alphabetical, from 142 (*Argyll*) to 615 (*you*)

The period alphabet has 24 letters: no j, no v.

`test_key.py` validates it on the two solved letters, which decode cleanly:

> you-could-be-con-t-e-n-t-to-m-a-r-r-y-**m-a-d-a-m-o-is-e-l-l-e**-in-regard-of-her-p-e-r-s-on-I-find-ing-her-in-(**o-the-r-r-e-s-p-e-c-t-s**)-a-good-match-for-you

> of-send-ing-the-fleet-to-help-be-ing-yet-of-the-**s-a-m-e**-opinion … concerning-my-**o-w-e-n**-request-to-**e-s-c-a-p-e**-of-which-now-I-have-great-hope

## 2. The decisive test

Three measurements, with the two solved letters as positive controls.

**Coverage** — how much of each message the key can interpret at all:

| letter | code groups | uninterpretable |
|---|---|---|
| 3 Oct 1648 (solved) | 61 | **0%** |
| 7 Nov 1648 (solved) | 39 | **0%** |
| 22 May 1648 (unread) | 112 | **43%** |
| 1 Aug 1648 (unread) | 88 | **48%** |

**Range** — the key is letters 1–107, a dead gap 108–141, words 142–615. Neither solved letter puts
a single code in the gap. The 1 August letter puts two there (126 and 140).

**Language** — take the maximal runs of single-letter codes, map them through the key, score them
with an English bigram model built from 12.9 million characters. The null randomly permutes the 24
letter identities across the homophone classes, which preserves every structural fact about the key
and destroys only the identity, so it tests exactly the claim at issue.

| letter | runs | chars | score | z | p |
|---|---|---|---|---|---|
| 3 Oct 1648 (solved) | 5 | 33 | −2.52 | **+3.17** | **<0.00025** |
| 7 Nov 1648 (solved) | 3 | 14 | −2.53 | **+2.34** | **<0.00025** |
| 22 May 1648 (unread) | 10 | 43 | −4.68 | +0.09 | 0.47 |
| 1 Aug 1648 (unread) | 3 | 15 | −3.99 | +1.11 | 0.14 |

The solved letters sit outside 4000 random relabellings. The unread letters sit in the middle of
them. The published key does not open either.

This agrees with what the solvers said at the time — "The letters of August 1 and May 22 were
written with a different nomenclator" — and with the 1 August letter's own postscript: *"This Cypher
which now I write in, is that which was sent you by the noble frend who conveis this Letter to you
from me."* Charles is telling his son he has switched keys. What is new here is that the exclusion
is now measured rather than asserted.

Reproduce: `python test_key.py`.

## 3. A corrected and extended source

Tomokiyo cites "History of the Isle of Wight (1795) p.237" without naming the author. It is **John
Albin**, *A new, correct, and much-improved history of the Isle of Wight* — not Richard Worsley's
1781 history, which the Cipherbrain thread cited instead. Internet Archive item
`bim_eighteenth-century_a-new-correct-and-much_albin-john_1795`, leaf 258.

Every code group of the 22 May letter was checked against that page image
(`img/albin_leaf258.jpg`). **Tomokiyo's transcription is exact.** This matters because the strongest
structural result below turns on three digits, and because the OCR of the same page disagrees with
him in four places — all OCR error, none real.

Albin also prints, on the facing page 236, a **letter of 16 May 1648 to the same man** which
cryptiana does not carry. It is almost entirely in clear and contains exactly one cipher group:

> …it is that you would goe to Southampton to one Mrs. Pit's House, where you will finde **W:** and
> deliver to him the enclosed … and also advise with him, where I shall take the Boat and where land
> and the Watch Word as soone as you can: the other is to **395** wch. I desyre you send safely and
> speedely to him…
>
> *Least you should not understand The Cypher; … If I knew certainely that you had the Cypher out of
> wch. I have written this Name, I would wryte more freely than I now care.*

So **395 is a man's name**, stated as such by the King, and 395 occurs twice in the 22 May letter.
By Peter Barwick's contemporary letter-code, **W: is Captain Silius Titus** and **Z is Edward
Worsley**. Albin's surrounding narrative supplies the context: this is the escape plot of late May
1648, with Worsley, Richard Osborne and John Newland of Newport as the King's agents, and Albin's
own verdict on the cipher — *"totally unintelligible to them, as well as to us."*

## 4. The Worsley cipher is not the Titus cipher

This is the part that is new.

On 22 May 1648 Charles wrote to Titus *and* to Worsley, about the same escape, on the same day. The
Titus cipher is effectively published: George Hillier, *Narrative of the Attempted Escapes of
Charles the First from Carisbrook Castle* (1852), prints fifteen of those letters with the
decipherment set in italics beside the code groups. In 2021 Thomas Ernst proposed on Cipherbrain
that the Worsley cipher "comes closest to the Titus-cipher" and said he was reconstructing the
latter from Hillier. He never published it, and nobody ran the comparison.

`hillier.py` harvests the aligned passages out of the 1852 text; `titus_vs_worsley.py` compares the
two repertoires. No key reconstruction is needed for this — it only asks which numbers each cipher
uses.

| band | Titus (660 groups) | Worsley (112 groups) |
|---|---|---|
| 1–97 | 30.0% | 65.2% |
| **98–203** | **18.3%** | **0%** |
| 204–416 | 40.2% | 34.8% |
| **417–739** | **11.5%** | **0%** |

* Expected Worsley codes in 98–203 if drawn from the Titus repertoire: **20.5**. Observed: **0**.
  P = 1.4 × 10⁻¹⁰.
* Titus uses 48 distinct codes above 416. Worsley uses none.
* Permutation test, 200,000 draws of 112 codes from the observed Titus usage distribution:
  **0** reproduce the empty 98–203 band, **0** stay under 416, **0** do both.

The two ciphers are different keys. The high overlap in the low numbers (42 shared codes, nearly all
under 100) is just both ciphers using the letter range densely, and is not evidence of identity.

A by-product worth keeping: `python hillier.py pairs` recovers 35 aligned cipher/plaintext passages
from Hillier, and several align one-to-one and cross-confirm — 251 = *my* (×4), 680 = *wife* (×2),
169 = *from* (×2), 647 = *twenty* (×2), 686 = *escape*, 457 = *Lady Carlisle*, 715 = *Mrs Whorwood*,
659 = *Monday*, 662 = *Wednesday*, 665 = *Sunday*, 672 = *May*. One passage aligns exactly and gives
letter values: *Mrs Whorwood that I s-t-a-y not for the ship* = 715 363 209 **63 78 20 46** 270 158
360 356. This is a start on the Titus key, not a finished one.

## 5. Why neither letter yields to analysis

`structure.py` and `nearrepeat.py`.

| | 22 May | 1 Aug |
|---|---|---|
| code groups | 112 | 88 |
| distinct | 76 | 66 |
| **hapax** | **43%** | **59%** |
| longest exact repeat | 2 | 1 |
| longest near-repeat (±1) | **7** | 2 |

A code group that occurs once carries no statistical information whatever, so the hapax rate is a
ceiling on what any analysis can recover. At 43% and 59%, with 30 and 42 distinct word codes
standing for unknown words, there is nothing to climb. George Lasry made the same point on
Cipherbrain in 2021: the runs of consecutive two-digit codes are far shorter than automated solvers
need.

The one real handle is the near-repeat in the Worsley letter, **found by Matthew Brown in April
2021**:

```
position 14   2 20 3 230 388 45 36
position 79   1 20 2 230 388 46 36
```

Four positions match exactly; three differ by exactly 1. Brown's inference was that the low numbers
are homophones and that a letter's homophones are consecutive — which is how the contemporary
Bramhall-to-Ormond cipher of 1653 is built, and unlike the September–November key, where codes
differing by 1 are different letters.

What is added here is that the pattern is not chance. Shuffling the observed multiset of 112 codes
200,000 times, holding length, alphabet and every code frequency fixed:

| | longest near-repeat (±1) | p |
|---|---|---|
| 22 May 1648 | **7** | **0.00000** (0 of 20,000) |
| 1 Aug 1648 | 2 | 0.50 |
| 3 Oct 1648 (solved) | 1 | 1.00 |
| 7 Nov 1648 (solved) | 1 | 1.00 |

The null distribution of the longest near-repeat peaks at 2. A 7 does not occur. So the repeat is
a real repeated phrase and the adjacency structure is real, and 1, 2, 3 are interchangeable, as are
45 and 46.

That is one phrase in a 112-group message. It is not enough to solve a nomenclator.

## 6. Where this leaves the two letters

**Excluded:** the published September–November nomenclator (§2), and the Titus nomenclator (§4).

**Established:** the Worsley cipher assigns consecutive numbers as homophones of one letter (§5); it
occupies 1–97 and 204–416 with nothing between (§4); 395 is a man's name (§3); the transcription is
sound (§3).

**Honest limit.** These two letters are short, almost entirely non-repeating, and use keys of which
no copy is known. They will be read when someone finds the key itself — in the Titus and Firebrace
papers in the British Library, in Barwick, or among Worsley family papers — not by analysis of 112
and 88 code groups. The 2021 thread reached the same conclusion from the other direction and stopped
in May 2021 with several mutually incompatible partial readings on the table and no way to choose
between them.

The originals of the two Worsley letters are on display at Carisbrooke Castle Museum.

---

### Files

| file | what it does |
|---|---|
| `key.py` | the published nomenclator, machine-readable, with the grey (inferred) entries marked |
| `letters.py` | the four ciphertexts plus the 16 May crib, verified against the 1795 page |
| `test_key.py` | the decisive test: coverage, range, language fit with a structure-preserving null |
| `structure.py` | inventory, hapax rate, repeated n-grams, adjacency |
| `nearrepeat.py` | permutation test on the near-repeat |
| `hillier.py` | harvests aligned cipher/plaintext from Hillier 1852 |
| `titus_vs_worsley.py` | repertoire comparison excluding the Titus key |

### Sources

* Nomenclator and solved letters: Klaus Schmeh, *Solved: The encrypted letters from Charles I to his
  son*, Cipherbrain, 5 May 2021, and the comment threads under it and under the 11 April 2021 article
* Ciphertexts: Satoshi Tomokiyo, cryptiana, *Charles II and the Royalists*, §4
* 22 May and 16 May letters: John Albin, *A new, correct, and much-improved history of the Isle of
  Wight* (1795), pp. 236–237
* Titus letters: George Hillier, *Narrative of the Attempted Escapes of Charles the First from
  Carisbrook Castle* (1852)
* Letter-code identifying Z as Worsley and W as Titus: Peter Barwick, *The Life of the Reverend Dr.
  John Barwick* (English edition 1724), p. 395

## 7. The original leaf (21 Sept 2026)

The 1 August letter is DECODE **R8342** (BL Harley MS 6988 f. 208; old foliation 127), which the
catalogue listed as "Charles R. to unknown recipient" (entry 135). The recipient is the Prince of
Wales. The leaf was checked against `letters.py`, and the transcription holds. The superscript groups
(379, 126, 329 165, 77, 5 20, 381) are the King's own insertions, most of them over struck groups
that cannot be read. The group before 107 could be 69 rather than 60. Halliwell, *Letters of the
Kings of England* ii (1846) 449–450, prints the clear text and notes only that "part of the original
is written in cipher". The "key" record R8341 (Harley 6988 f. 194, 1646) is a graphic-sign
substitution and cannot be the key for a numeric nomenclator. Nothing new opens the letter. **Outcome: skipped as impossible without the key**; it
stays unread. The "noble Frend" who brought the cipher to the Prince in August 1648 is most likely
Lauderdale, which points the key search at the Lauderdale papers as well as the Clarendon and
Nicholas papers.
