# BnF fr. 3621 no. 97 — the cipher read

**Charles III, duke of Lorraine, to his son the comte de Vaudémont, Nancy, 18 June 1592.**
Gallica `btv1b52524472n`, canvas f227, folio 109. "Coppie d'une lettre de Monsieur de
Lorraine a Monsieur de Vaudemont".

The cipher was catalogued as unsolved. DECODE record 9449 describes this exact piece and
gives its status as `Non-decrypted`; no key for it has ever been published.
<https://de-crypt.org/decrypt-web/RecordsView/9449>

## 1. What the letter physically is

Not a wholly ciphered despatch. Clear French and cipher **alternate inline on the same
lines**. The body runs to 21 written lines, of which lines 9 and 20 are wholly clear, line
21 is cipher then clear, and the rest are cipher with clear words embedded. Everything
below the subscription — the whole long postscript — is clear.

The baselines slope: the shear that sharpens the histogram of glyph y-centres is **−0.031**,
and deskewing at that value resolves the block into 21 line bands at about 87 px spacing in
the native 4046 × 5762 image.

## 2. The cipher

The cipher symbols are **ordinary cursive letterforms**, not the geometric signs of the
Nevers and Guise keys in fr. 3995. They can be read directly off the page. The by-eye
transcription in `no97_eye.txt` records 1,109 tokens: **1,071 letter symbols in 44 distinct
forms, and 38 nomenclator figures**.

Figures observed, with counts:

| figure | 139 | 145 | 31 | 57 | 141 | 98 | 88 | 13 | 103 | 121 | 122 | 123 | 137 | 146 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| count | 10 | 7 | 4 | 3 | 3 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

The letter-symbol frequencies match French rank for rank through the top fourteen places,
with the commonest symbol at 14.4%. The coincidence statistics place the cipher between a
purely monoalphabetic and a fully homophonic system, so it is a letter substitution with
**modest homophony**, plus the numeric nomenclator:

| | IC single | IC digraph | trigram repeat |
|---|---|---|---|
| this cipher | 0.0592 | 0.00595 | 39.8% |
| 44-symbol homophonic control | 0.0416 | 0.00257 | 19.3% |
| 22-symbol monoalphabetic control | 0.0834 | 0.01034 | 61.4% |
| plain French | 0.0795 | 0.00894 | 58.5% |

## 3. The key

Recovered by iterated local search against a character 4-gram model of Montaigne, the same
search having been calibrated first on controls with known keys (`control_*.txt`). The
mapping is stable: independent runs from different seeds, and a run with the crib locked,
converge on it.

The period folds u with v and i with j, and the model follows that.

```
A e   B p   C t   D s   E c   F o   G u   H h   J s   K u   L u
M e   N r   O d   P n   Q a   R o   S n   T e   U s   V c   W e
Y e   Z r   a i   b p   c t   d q   f c   g u   i a   j n   m y
n s   o r   p n   q d   r o   s n   t e   v r   x s   y l   z m
```

Transcription tokens are as defined at the head of `no97_eye.txt`: lower case is the plain
letterform, upper case its barred, dotted or capital variant, and `f H i n c t i G` are the
eight forms that spell *chasteau*.

## 4. Why the key is right

The eight-symbol group `f H i n c t i G` occurs at two separate places in the cipher, on
line 15 and on line 19, and the key renders it **chasteau** both times. **Chasteauvillain
stands in the clear on the same page**, twice: in the body at line 9, "aussi si dieu nous
fault la grace de prendre Chasteauvillain", and again in the postscript. The key was not
fitted to that word; the 4-gram search produced it, and locking it afterwards did not change
the rest of the solution.

Other words the key produces unprompted, none of them supplied to the search:

*munitions* (three times) · *promesses* · *prisonniers* · *resolution* · *secours* ·
*quartiers* · *clairement* · *commandement* · *conserver la plaine* · *ramener mon armée* ·
*aultres commoditez* · *il fauldra* · *recepvoir* · *de prudence*

## 4b. Tested against nulls

The objection to everything above is that the search maximises a French 4-gram score over 44
free parameters on ~1050 characters, so it has a standing incentive to produce French-looking
strings with or without plaintext underneath — and words picked out by eye are no defence,
because the chooser knows the subject. The pipeline was therefore run unchanged on nulls with
no plaintext: same symbols, same frequencies, same segment lengths, order shuffled. Scoring
blind: dictionary coverage and distinct French words of 6+ letters, from a corpus word list
with no names and nothing from this letter. Full output in `control_null.txt`.

| | 4-gram | coverage | distinct 6+ letter words |
|---|---|---|---|
| **manuscript** | **−2.10** | **83.0%** | **33** |
| null mean of 5 | −2.73 | 74.6% | 1.2 (range 0–3) |

Thirty-three against nought to three decides it: there is real French under this transcription.
Coverage barely separates the two and is a weak statistic here, since short function words can
be assembled out of anything. The blind list returned *clairement, resolution, paroistre,
quartiers, pourtant, secours* — the words found earlier by eye, now found without choosing them.

It also returned *uilains*, which in a u/v-folded model is *vilains*, sitting immediately after
*chasteau* and sharing its final u: the decode gives **chasteauilains** where the name wants
**chasteauuilains**. One symbol short. That is a transcription slip rather than a fault in the
key, but it is a slip, so the crib is eight letters secure and six more probable — not fifteen
letters proved.

## 5. What the ciphered passages say

Read with care. The decode scores −2.10 per character against −1.93 for real French and
−1.63 for a clean control. On the calibration in `control_merge.txt` that corresponds to a
transcription in which roughly six to twelve pairs of distinct glyphs have been read as the
same form, giving about 65–75% of letters correct. The limit is now the eye-transcription of
the glyphs, **not** the cryptanalysis. Individual words below are secure; the connective
tissue between them is not, and is left out rather than guessed.

The ciphered matter is military and concerns the same operation as the clear postscript:

* the promises made and not kept — *de tant de ... ses promesses ... qu'ils avoient fait*
* **prisonniers** and **munitions**, recurring; munitions again at the end of the letter,
  where the clear resumes with "si munitions"
* an order to **recepvoir mon commandement** and to **conserver la plaine**
* **Chasteauvillain**, and the intention **de ramener mon armée ... es quartiers de la
  Faulche** — La Fauche lies between Neufchâteau and Chaumont, in exactly the theatre the
  clear postscript describes
* a demand to be **préadverti**
* **resolution**, **le peu de moien** and **secours**
* Chasteauvillain again, with **l'on avoit ... promis**

The clear text around them, already transcribed in `clear_texts.md`, supplies the rest: the
grace of taking Chasteauvillain, Chaulmont, the sieur de Buzonville, la Glosiere, the
munitions promised, and the siege.

## 6. What is not done

The transcription is not yet clean. About a quarter of the glyph identifications are wrong,
which is why the reading is partial. Closing that gap means re-reading the 42 half-line
crops in `lc/` with the key in hand and correcting the barred, dotted and capital variants
one by one; the key will then read the letter through. The fourteen nomenclator figures are
unassigned: no key survives, so their values can only be got from context or from a second
letter in the same cipher.
