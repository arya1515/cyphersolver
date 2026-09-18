# The ten leaves are not one cipher: three keys, one solved

Measured, not assumed. Take the figure-frequency profile of each leaf's transcription. Two leaves
enciphered in the same key have the same profile; two leaves in different keys do not.

| leaf(s) | figures | most frequent figures |
|---|---|---|
| f. 173 | 1082 | `x` 7.9 · `t` 6.5 · `a` 5.9 · `.v.` 5.5 · `e` 5.3 · `7` 5.0 |
| f. 154 | 1061 | `t` 8.3 · `x` 7.6 · `a` 7.1 · `.v.` 6.2 · `7` 5.7 · `L` 5.1 |
| **f. 123r** | 1150 | `E` 7.7 · `d` 7.2 · `q` 7.1 · `U` 6.6 · `4+` 6.4 · `.v.` 5.2 |
| **f. 110** (sample) | 67 | `o` 11.9 · `n` 7.5 · `8` 6.0 · `h` 6.0 · `t` 6.0 · `BOX` 6.0 |

ff. 154 and 173 agree figure for figure; they are the same key, and that key is solved — applying it
gives running French on ff. 143, 150, 154, 173, 196 and 201, and ff. 196/201 independently share 23
runs of eight identical figures.

**ff. 123–124 are a second key.** Its common figures (`E`, `d`, `q`, `U`) are not the common figures
of the solved key, where `x`, `t`, `7` carry the load. Applying the solved key to f. 123r gives a
few French words in a page of noise — the residue you get from a wrong key of the same family, not
a transcription problem. f. 123r also uses **three-digit code groups** (`101`, `102`, `15`, `16`),
which the solved key does not.

**f. 110 is a third.** A smaller, denser hand, about a hundred figures to the line, and a different
profile again. The solved key yields nothing on it.

## What follows

The catalogue entry treated "Forget / Matignon / Mayenne, fr. 15572 + 15571" as one target. It is
three targets sharing a correspondence. One is solved and six leaves are read; two remain, and for
those the work is a cold homophonic solve, not transcription plus a known table.

`hillclimb.py` is the cold solver: simulated annealing over figure→letter maps, scored by the
character model with a penalty on the decoded letter distribution.

## A defect found in the language model, and fixed

The model was built from Berger de Xivrey's Henri IV letters with `v→u` and `j→i`, which turns every
Roman numeral (`viii`, `xxiiii`) into a run of `i`. Enough survived that **`iiiiii` scored better
than French** — real French −1.51 per character, a page of `i` −1.53. A cold solver maximising that
score collapses every figure onto `i`, which is exactly what the first run did.

Two changes fix it: drop Roman-numeral tokens when building the model, and require a context to be
attested at least 15 times before it is used (a stray eight occurrences of `iiiii` were doing the
damage). Now: French −1.51, a page of `i` −2.16, random letters −3.99.

## A crib for the second cipher: f. 79r's margin

f. 79r (canvas 85 right) is Mayenne's own letter — *"Du camp de Tonneins ce v.e mars 1586"*, signed
**Charles de Lorraine** — and it carries a seven-line cipher block inside the clear text with **its
decipherment written down the left margin**. The margin's line-openings are lost in the binding, but
what survives reads:

> … ne paroistra pour … campagne … avant … plustost que **Janvier** … **recouvrement** [des]
> **places** … aussy, et y **rafraischir** … **l'armée sur la fin de l'automne. Je pouray mettre en
> liberté** … **la Rouergue et la Quercy**, qui e[st] … **fruict** que je [pré]tends … **vous
> pourrez attendre** … ceste **année**.

**The anchor.** Of the crib words, *rouergue* has a distinctive repeat structure — r·o·u·e·r·g·u·e,
i.e. the pattern X Y Z W X V Z W. Searched against the block's 244 figures it has **exactly one
match**, at position 133:

```
4+  6  h  e  4+  B  h  e
r   o  u  e  r   g  u  e
```

So in this cipher `4+`=r, `6`=o, `h`=u, `f`=e, `B`=g — and none of those agree with the solved
Cipher-1, where `4+`=m and `h`=e. That is independent proof, from a crib rather than from
statistics, that the second cipher is a different key.

Five letters are not a solution. What they are is the start of one, and the method that produced
them — pattern-matching a rare word shape against the figure stream — is the method that will
produce the rest as more of the margin is recovered.
