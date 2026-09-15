# D'Agapeyeff cipher (1939) — the ciphertext is not enciphered English

Challenge cipher from the first edition of Alexander D'Agapeyeff's *Codes and Ciphers* (OUP, 1939, p.158),
dropped from later editions; the author is said to have admitted he had forgotten how he enciphered it.

## Structure (confirms the standard reading)

395 digits in 79 groups of five. Dropping the trailing `000` of the final group `92000` leaves **392 digits
= 196 pairs**, and the pairs are perfectly regular:

* first digit of every pair is from **{6, 7, 8, 9, 0}** — counts 56, 41, 80, 18, 1
* second digit of every pair is from **{1, 2, 3, 4, 5}** — counts 33, 46, 29, 43, 45

That is a 5 × 5 Polybius square, the method D'Agapeyeff works through in his own book. 18 of the 25 cells
occur; the unused ones are 61, 73, 95, 01, 02, 03, 05. Cell counts:

```
81:20  75:17  62:17  82:17  85:17  64:16  83:15  74:14  91:12
63:12  84:11  65:11  72:9   92:3   93:2   04:1   94:1   71:1
```

## Positive control

The same book contains a **worked Polybius example with its plaintext given** — 178 letters of A–E
enciphering "THE NEW PLAN OF ATTACK INCLUDES OPERATIONS BY THREE BOMBER SQUADRONS…". Same author, same
book, same method, known answer. Running identical tests on both is the cleanest possible comparison.

| test | control (known English) | challenge |
|---|---|---|
| cells | 89 | 196 |
| distinct cells | 22 | **18** |
| best-case chi-squared vs English frequencies | **4.2** | **34.1** |
| repeated digrams vs random shuffle of own symbols | **z = +3.60** | z = −0.73 |
| repeated digrams vs English of same length | z = −0.01 | z = −1.74 |

The control behaves exactly like enciphered English on both tests. The challenge behaves like a random
sequence on both.

## The frequency result, calibrated

"Best-case chi-squared" sorts the observed cell counts against sorted English expectations, so it is a
*lower bound* over every possible substitution key, and it does not depend on the order of the text — it
therefore holds **whatever transposition may or may not have been applied**. Calibrated on 3000 real
English samples of 196 letters:

* English best-case chi-squared: median 7.3, 95th percentile 13.0. Challenge: **34.1**.
  **0 of 3000** English samples were this bad.
* Distinct letters used: English median 22. Challenge: **18**. **0 of 3000** English samples used 18 or fewer.

So a simple Polybius substitution of 196 letters of English is excluded at better than 1 in 3000 on two
independent statistics.

## No transposition is detectable

Repeated digrams are invariant to the substitution key, so a keyed columnar transposition can be attacked
without ever guessing the square: hill-climb the column order to maximise digram repeats. Done for 4, 7, 14
and 28 columns — and then repeated on *random shuffles of the same symbols* as a control:

| columns | challenge | random shuffles |
|---|---|---|
| 4 | 78 | 75, 76, 74 |
| 7 | 83 | 82, 83, 80 |
| 14 | 89 | 86, 86, 85 |
| 28 | 98 | 97, 97, 97 |

The scores rise with the number of columns on random data exactly as they do on the cipher: this is
overfitting, not a key. There is no transposition signal. The book's own null rule ("every third, fourth or
fifth letter … is a dummy", p.111) was also swept at every offset and every period, and no offset produces
readable text or a better score.

## Reading

The ciphertext does not carry the statistical signature of English enciphered by the method the book
teaches. This is consistent with the long-standing suspicion, and with the author's own admission, that the
encipherment was botched.

**Honest limits.** This is evidence about what the ciphertext is *not*, not a proof that nothing is there.
Heavy null insertion (well above the book's stated rate) would also flatten frequencies and break digram
structure. And the tests assume an English plaintext, which the book's context makes very likely but does
not guarantee.

Reproduce: `python control.py` (control vs challenge), `python keyed.py` (calibration and transposition
search), `python solve.py --nulls` (null sweep).

## Dropping the bijection (free.py) — degenerate, adds nothing

The flat cell distribution suggests the square may not be one-to-one: either homophonic (common letters
hold several cells, which flattens counts) or polyphonic (one cell covers several letters, which explains
why only 18 distinct cells appear where English of this length uses about 22). `free.py` allows any
cell-to-letter mapping and anneals on quadgrams.

It fails in the classic way: the search collapses onto a two-letter mapping and emits
`sseeeseeseesesessessss…`, scoring **-4.64**, which *beats* real English (-4.8) while being obvious
nonsense — an unconstrained many-to-one map can always cheat by sending every symbol to common letters and
harvesting quadgrams like `eses`. Control shuffles of the same symbols score -4.48 to -4.62, i.e. the same
or better than the real text.

So the result is uninformative about the cipher and only shows the method needs a constraint (a fixed
letter-count profile, or a near-bijection). It does, however, repeat the earlier finding: the real
ciphertext scores no better than shuffles of its own symbols.

## Final diagnostics (diag.py): language, periodicity, repetition

Three more hypotheses tested, all negative, and together they close off the natural-language reading from
every direction.

**Plaintext language.** Best-case chi-squared against each candidate's letter frequencies (lower is
better; English 196-letter samples have a median of 7.3):

| plaintext model | fit |
|---|---|
| uniform over 10 symbols | **10.6** |
| Latin | 18.8 |
| French / Spanish | 20.9 |
| Italian | 25.8 |
| Russian transliterated | 33.9 |
| English | 34.2 |
| German | 37.9 |

The distribution fits *a uniform draw over ten symbols* better than any natural language, and English is
among the worst fits. Changing the assumed language does not rescue the cipher.

**Periodicity.** Index of coincidence taken on every n-th cell, for periods 2 to 15, stays flat
(0.054 to 0.086) with no peak. There is no periodic key, so a Vigenere-style or rotating-square
construction is excluded.

**Repetition.** Natural language of this length repeats itself; this text does not.

| | challenge | English, 196 letters |
|---|---|---|
| repeated 3-grams | **5** | 16.8 |
| repeated 4-grams | **0** | 6.6 |

## Overall

Five independent lines now agree: the frequency profile (order-independent, so it survives any
transposition), the absence of a transposition signal, the absence of periodicity, repetition far below
natural language at every n-gram length, and the failure of the book's own null rule at every period and
offset. The cell sequence behaves like a near-uniform random sequence.

For an elementary 1939 textbook cipher whose author admitted he could no longer decipher it and quietly
dropped it from later editions, the economical conclusion is that the encipherment was botched and there is
no recoverable plaintext. That is not a proof, and it cannot be one; but every test that would show a
signal shows none.
