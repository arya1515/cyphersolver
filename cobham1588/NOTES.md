# Lord Cobham to Walsingham, May–June 1588 (BL Harley MS 287, DECODE R8490/R8492/R8495/R8496): key partly rebuilt, not read

Catalogue item: "Cobham (Belgia) to Walsingham, 4 ciphertexts" (DECODE R8490, R8492, R8495, R8496; rule-scored).
Outcome: **attempted, open.** The cipher system has been identified and most of its alphabet has been rebuilt from
the decrypted sibling letters in the same volume. Only fragments of the four letters read with confidence.

## The documents

William Brooke, 10th Lord Cobham, was one of Elizabeth's commissioners at the Bourbourg peace talks with Parma's
deputies (spring–summer 1588). His letters to Walsingham are in clear English. Short passages and single words are
in cipher, set into the running text.

| DECODE | Harley 287 | date, place | pages with cipher | notes |
|---|---|---|---|---|
| R8490 | ff. 80–81 | Ostend, 5 May 1588 | f. 80r (about 12 cipher groups), f. 81 (2 lines) | "Julio Romeo, Cristophero Mondragon" and "Doctor Dale" in clear |
| R8492 | f. 88 | undated, 1588 | f. 88r: the densest cipher (about 14 lines) | "captain Montgomery ... of late gone into Scotland ... with 40 men of ..." |
| R8495 | ff. 92–93 | 27 May 1588 ("Belgia") | f. 92r, about 8 lines | news: the Armada still at Lisbon, Gonzaga, 200 mariners at Sluys |
| R8496 | ff. 96–97 | Bourbourg ("Binborow"), 9 June 1588 | ff. 96r–97r, scattered | |

Images: DECODE, fetched with the session cookie (see memory decode-access). They are BL images, not in the public
domain: kept in `tmp/cobham/` (git-ignored). Nothing from them is committed except derived text.

DECODE R8497 (Harley 287 f. 187, "The Cowler Cipher for Mr Bodley ... in the Low Countries", December 1590) is the
key record the catalogue pointed at. It is **Bodley's** cipher of 1590, a different alphabet, and does not
apply to these letters.

## Prior art

- CSP Foreign vol. 21 pt 4 (Jan–June 1588) calendars the Cobham letters in SP 77 (Flanders), for example 1 May,
  3 June, 6 June and 10 June. It does not calendar these Harley 287 letters. No printed decipherment was found.
- DECODE marks the sibling Cobham letters in the same volume as **Decrypted**: R8481 (f. 63, Mar 1587/8),
  R8488 (ff. 75–76, Ostend 9 Apr 1588), R8489 (ff. 78–79, Apr 1588), R8493 (f. 89). Their cipher passages carry
  a contemporary **interlinear decipherment**. They are the source of the key below.
- A second session (cypher-7e, folder `harley287`) is working the same system on R8477–R8487 (Ostend, March
  1587/8). Key notes were exchanged on 21 Sept 2026.

## The system

A **monoalphabetic substitution with homophones** in Greek-like letters, arbitrary signs and a few Latin letter
shapes. Nulls are dots, dashes and ".." marks, though ".." also stands for u/v. A few signs are **code signs**; a
square (◻) is one. Word division is mostly kept. It is the same system as the glossed March–April letters.

Key rebuilt from the glosses of f. 75 (R8488: "upon our arrival", "willing to harken", "by the clergy they made
means", "discours", "sent from", "their great desir of", "cardinal is coming", "the pope's legate", "the Duke of
Parma his bastard son") and f. 89 (R8493: "what may be", "further hoped for at their hands", "our abode in this
towne is so advantagious"). The sign names are descriptive:

| plain | signs |
|---|---|
| a | U / ∪ |
| b | + |
| c | 8 |
| d | ∞ |
| e | 7 |
| f | H |
| g | crossed X (Ж) |
| h | ϸ (loop on a long stem) |
| i | ⊥, X (undotted) |
| k | ω |
| l | ϕ (small loop), L, and ".." after a letter (cypher-7e) |
| m | ∝ (loop with tail) |
| n | ǂǂ (double-barred cross) |
| o | Z (z-shape), c, d |
| p | ϑ |
| r | V, γ |
| s, t | Λ (two near-identical forms; not separated) |
| u / v | "..", ":" |
| w | ẋ (dotted x) |
| y | γ |

Doubtful or missing: j, q, x, z. There are unidentified signs on f. 88 (K, υ, ρ, W) and unnamed code signs. Because
the s/t and r/y signs are shared, a letter-by-letter reading needs a clean sign-level transcription. This session
did not make one.

## What reads

Fragments only, grade M (probable) unless marked:

- f. 80r: "hoping them in the ◻ [code] …ances for what chaunces so ever" (the cipher word ends -ances); "it will
  not be … the ho-v-en [haven?] is …" (uncertain); "in all ΛVZΛTΛ in numbers, that at the ΛVZΛT …, which was
  the 20" — the word could not be resolved: ARMADA does not fit the key (V = r, Z = o).
- f. 92r: "imprisoned in …", "it is reported that they have … of letters" (ϕ7ΛΛ..⊥VΛ, l-e-t-t-[e]-r-s, H).
- f. 88r: the clear frame reads "There is captain Montgomery of late gone into Scotland" [cipher] "with 40 men of"
  [cipher] "which have promised the" [cipher] "15 of late there is" …. The cipher words contain signs not in the
  table.

## What would finish it

1. A sign-level transcription of the cipher passages on ff. 80r, 81, 88r, 92r and 96r–97r, from full-resolution
   crops (the images are 7200×10200 px, so each passage can be cut at about 4× reading size).
2. Separate the two Λ forms (s/t) and the r/y signs from the glossed siblings, if they differ at all.
3. Merge with cypher-7e's `harley287` key for R8477–R8487.
4. Read the passages. The letters are in plain English and the context is known (Bourbourg talks, Armada news).

Status: attempted, key partly rebuilt, open.
- Cross-link: cypher-7e read R8482-R8487 (docs/harley287.html, harley287/key.tsv); its key has narrow ∧ = s, wide ∧ = t.
