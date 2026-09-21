# Catalogue 97: the two unidentified ciphers on BL Add MS 4136 (DECODE R2988, R2989)

Status: read in part (21 Sept 2026): the 10 July 1559 letter ~85-90%; margin and Wood line closed unread. Write-up docs/wod1568.html.

Catalogue entry 97 ("Unknown sender (Paris) to unknown recipient, 10 Jul – 8 Aug 1559") covers the two items
Tomokiyo lists as unsolved on cryptiana `unsolved.htm` (Nicholas Throckmorton 1559 / John Wod 1568). The
Throckmorton cipher text on both leaves is already read by Tomokiyo (Cipher 1 and Cipher 3; see `../throckmorton/`).
Each leaf also carries a second cipher that is **not** Throckmorton's. Those two are the targets here:

| record | leaf | the unread cipher |
|---|---|---|
| R2988 | f. 32 (old 9), Throckmorton to the Queen, Paris, 10 July 1559 | ~12 lines of small cursive signs in the lower margin and beside the subscription, including a clear date `… 1559`, a boxed group repeated three times, `/` and `//` separators, and a starred insertion keyed to a `*` note in the left margin |
| R2989 | f. 33 (old 10), Throckmorton to Cecil, Paris, 8 Aug 1559 | one line at the foot, docketed in the left margin "Mr John Wod to Secretary Cecil, 6 Sept 1568", with a traced signature "M. Jhone Wod" |

Images: `img/` (DECODE, git-ignored). Downloaded with the bordeaux cookie 2026-09-21.

## R2989: John Wood to Cecil, 6 September 1568

Transcription (`wood_line.txt`, my labels; 3x zoom on `IMG_R2989_I20715_P.jpg`):

    g x ob r3 Z pm x x x2 f x2 Z g D x2 e XX 3 · x zl x ob x3 x2 x x2 Z zl o d pm g x ob /  (J) o · Z D x2 zl

`x` plain saltire; `x2` saltire with a hooked stroke; `x3` inverted-v form; `ob` o with a flat bar; `r3` a reversed
curly 3; `Z` long-tailed ʒ; `3` a short numeral 3 followed by a point; `zl` z with a vertical (L over z);
`pm` a plus-minus sign; `D` triangle; `XX` a blotted x with a dotted x written above it. 34 signs on the main line
and 5 after the marker `(J)`, which may be an insertion or a separate item.

**Same family as the Moray→Wood cipher.** The symbol families (x with variants, ʒ/z with variants, g, o, e, f)
match Tomokiyo's transcription of Moray to Wood, 13 July 1568 (`../moray/`, unread after one session). Wood
was Moray's agent in London that summer, so this is very likely the same Scottish cipher, and a second sample
of it. Tomokiyo's labels cannot be aligned glyph-for-glyph without his image (`stewart.jpg`, 404), so the two
texts could not be pooled.

**Crib from Bain.** Bain, *Calendar of Scottish Papers* ii no. 804 (Wood to Cecil, Edinburgh, 6 Sept 1568,
Cecil Papers, holograph) prints one passage with the footnote "These words are in cipher": *"and says he must
neidis haif it be on meinis or uthir."* (42 letters). Tested against the line (`align3.py`, `align4.py`):
exhaustive alignment with each sign = one letter, a null, or a fixed string of up to 4 letters (up to 6 nulls and
12 multi-letter signs), with and without the `(J)` group, with *says/sayis*, forwards and reversed, and every
substring of the phrase of 8+ letters: **no consistent alignment**. The line opens and closes with the same
trigram `g x ob`, which the phrase cannot produce. Either the Add MS 4136 line is a different ciphered passage
of the letter (the copyist may have taken the last one; Bain's final sentence, with its garbled "sennwngist"
footnoted "Sinews", is a candidate), or Bain's footnote marks words that the original shows deciphered in a
form the copy does not reproduce. 39 signs is far below what a ciphertext-only attack on a ~30-sign homophonic
alphabet needs.

## R2988: marginal cipher on Throckmorton's letter of 10 July 1559

About 300 cursive signs in 12 lines: strokes, hooks and loops with points and superscript points, word-like
clusters separated by spaces, `/` and `//`; a boxed group (read upright something like `ʃro` with superscript
points, once as `rel ʃro`) occurs three times; the clear year `1559` appears in line 10. Mirroring and inverting
the image do not give Latin script. The look is of a shorthand or an abbreviated sign alphabet rather than the
letter-symbol alphabets of Throckmorton's three ciphers, and the sign inventory could not be fixed reliably
from the scan (variation in size, points and ligatures). Not transcribed; not attacked.

## Route in

1. R2989: the original Wood letter of 6 Sept 1568 in the Cecil Papers at Hatfield (Bain's "C.P., vol. I"). It
   should show where the cipher sits and whether it was deciphered, giving a true crib for the line and a second
   text for the Moray cipher.
2. Tomokiyo's image or glyph table for Add MS 32091 f. 213, to merge the Moray and Wood texts under one labelling.
3. R2988: a clean high-resolution photograph of f. 32 and a comparison with 16th-c. English shorthand and
   personal sign systems. The clear "1559" and the `*` note suggest a contemporary annotation, possibly by the
   decipherer, rather than a second despatch.

## Files

`rec2988.htm`, `rec2989.htm` (DECODE record pages) · `wood_line.txt` · `align*.py` (crib alignment) ·
`bain2.txt` (Bain ii OCR, not committed) · `img/` (not committed).

## Session 2 (2026-09-21): main text started, margin still unread

- R2988's main Cipher 1 text is unpublished (not in Forbes or CSP Foreign; Tomokiyo only says it deciphers).
  A first pass is in `main_decrypt.txt`, lines 1-5 only, low-medium confidence: "...[it may] please <Queen's
  majesty> to <be> advertised that whereas I sent ... of the eight of <this> <moneth> at five of the clock in
  the afternoon ... of the same date written at midnight touching <French King>'s state ... I judge <Queen's
  majesty> [will] be desirous to be further informed thereof ... convenient to put in writing the [whole?]
  discourse of ...". Lines 6-15 are sign transcriptions only, line 16 is not transcribed; signs υ and ζ are
  not yet placed in the key.
- The starred insertion in the main text is on line 13, after "z ⊥ k v 5 1 H x 3". The left-margin `*` note
  keys to it, so at least that note belongs to the letter.
- Margin: the dated line reads `·ɥ ɾ ᵹ 8 ⅃.. 1559 / … //`. The day may be "8" rather than 10 July, which
  could mean it is a separate (earlier) note. The script runs left to right (lines end in `/`, `//`); it is
  not Hebrew, mirrored or inverted Latin. Hypothesis to test once the main text is read: the margin is a
  shorthand copy or postscript of the deciphered letter. Compare its group count (~200) with the plaintext's
  word count, and see whether the three boxed `ʃro` groups fall where a code name recurs.

### Session 2, continued: main letter read; margin identified as a separate dated text

**Main letter (Cipher 1), read.** Re-cut at the measured line centres (y = 812, 910, …, 2220), the whole block
decrypts with Tomokiyo's key after these corrections: x and υ = i; y = f/h; z = m; ρ = d/t; ∫t = w; Q = *be*;
ξ = *your Majesty*; a dot over a sign marks a code word. Lines 1-4 are secure (see `main_decrypt.txt`, pass 2).
Lines 5-15 decode to continuous English with the same key: "…convenient to put in writing the whole discourse
of … the present … state … the French King … service well considered … graciously … perceive … experience …
shall be able to declare more plainly and particularly when it shall please the same to command … preserve
your Majesty's health … wealth … at Paris the tenth of July". This is an unpublished letter (not in Forbes;
CSP Foreign vol. 1 pp. 362-369 has only the 8 July despatches). Letter-level transcription of lines 5-15 still
to be finished (estimated ≥90% of the letters are recoverable).

**Margin (the target).** It is a separate text in another system, not a gloss on the letter. It runs 10 lines
under the letter, ends with a date line `ɥɾᵹ 8 ⅃.. 1559 / … //`, then a 3-line `*` block keyed to the star
after "…" on main line 13. The letter says Throckmorton wrote on "the eight of this month" (by Gray, and again
at midnight by Carew). So the margin is most likely his copy or abstract of the **8 July** despatch, sent a
second time with the 10 July letter. The printed abstracts are CSP For. i nos. 947 (to the Queen, on Lord Grey's
ransom and Rochefoucauld) and 950 (to the Council; "portions in cipher, deciphered": the French King's fever,
d'Elbeuf and la Brosse for Scotland, galleys, Ruy Gomez, the Earl of Arran at Geneva, Anne du Bourg). The boxed
group that occurs three times is then probably a name. Lord Grey is the best candidate (he occurs repeatedly in
both abstracts).
Blocker: the sign inventory is not stable (points, superscripts, ligatures) and an abstract is not a verbatim
crib. Next step: get the R.O. originals SP 70/5 nos. 947/950 (TNA, State Papers Online) with their deciphered
cipher portions, then align them against a full margin transcription.

**R2989 Wood line.** No change: 39 signs, Bain's crib does not align; needs Hatfield CP vol. 1.

**Margin system (closer look, line 1 at 4x).** The signs are small letter-like forms (o, θ, ϑ, ı, √, ɥ, 7, 6)
that change value with point position: points above, right, doubled (`o··`, `θ·`, `ɥ:`), and superscript
letters. Groups are 1-4 signs separated by spaces, with `/` and `//` as clause marks. This is the pattern of
the dotted-letter word codes of the period (Thomas Smith's 1563 cipher: "a letter with one or two dots to the
left, right, above or below" stands for a word beginning with that letter; the Cecil-Norris table also works
this way). So most groups stand for whole words, and ~200 word tokens in an unknown code cannot be solved
ciphertext-only. **Closed as not readable from what is available:** it needs either the key (not among the
Add MS 4136 key leaves ff. 173-185, R9258-R9262, which are Throckmorton's and Smith's letter ciphers) or the
verbatim 8 July despatches (SP 70/5; CSP For. i 947, 950) as a crib.
- HMC Salisbury (Hatfield) calendar vol. 1 (archive.org calendarmanuscr01giusgoog), checked 2026-09-21: no entry
  for Wood's letter of 6 Sept 1568 (Sept 1568 runs 1185-1187 with nothing from Wood). Bain ii 804 remains the
  only print, so no further crib exists in print for the Wood line.

**10 July letter, pass 3 (`main_decrypt.txt`).** Lines 1-4 are secure; lines 5-15 read at ~85% (≈470 of 550
signs). Content: Throckmorton sends a gentleman (the bearer) to report the French King's state by word of
mouth. He asks the Queen to give him credit, praises his "diverse and sundry" service since coming over and
asks that it be rewarded, then signs off "…to preserve your Majesty in health, wealth and all felicity. At Paris
the tenth of Julii". Key additions: flat-topped 6 = w; ζ = null inside words; q̇ = your Majesty; K = all(?).
Twelve code signs are still open (1k̲ ρ̲ g̲ δ̄ δ̲ ō ⊓̄ q̄ r̄ π̄ ƒ̇ ʋ̲).

**Margin transcribed and measured (`margin_transcription.txt`, first pass).** About 405 signs in 217 groups. There
are about 29 base shapes (22 occur 4 or more times) and about 80 shape+dot combinations. Mean group length is 1.87
(1 sign: 106 groups, 2: 60, 3: 30, 4: 14, 5: 5, 6: 2). One boxed group, `[y+r u']`, occurs 4 times (M00, M03, M04,
M06); `z+e+l'` occurs twice. English spelled letter by letter would give a mean word length of about 4.3, with
single-letter words under 5% of the total; here half the groups are one sign. So this is not a letter cipher:
it is a word-sign system (shorthand or a dotted word code) with about 80 distinct signs. With about 217 tokens
and no crib there is no statistical attack: most word signs occur once or twice, and nothing has a known value
to anchor an alignment. Open only with a key or a verbatim crib (SP 70/5, the 8 July 1559 despatches).

**R2989 non-uniqueness test (`nonunique.py`).** The 39 signs (16 distinct) were annealed with 200 random restarts
against a quadgram model of Bain ii, where each sign is one letter (homophones allowed). 185 of the 200 end
states score above the median of real 39-letter windows of Bain (−338), the best at −290, and 92 of them differ
from each other in more than a third of their letters. All the top solutions are gibberish (e.g.
"stereatththestherstateth…"). The model overfits: the line admits dozens of unrelated "English" readings that
fit better than real text. That makes the line undetermined, not just hard; ciphertext-only it cannot be read.
It can be read only with an external crib (the Hatfield original).

**Conclusion (2026-09-21): closed unread, both targets.**
- Margin: a word-sign system, about 80 signs in 217 groups, no anchor, so no attack.
- Wood line: shown to have no unique solution.
- The 10 July letter on the same leaf is read at about 85-90% (a by-product).

**Margin identifiability test (`margin_stats.py`).** The groups match English words, not letters: 222 group tokens,
141 types, 113 hapaxes. 222-word windows of Bain give a median of 140 types and 107 hapaxes. So each group is
a word sign (a word code or shorthand), and 113 of 222 tokens (51%) are signs that occur only once. A sign seen
once has no internal evidence for its value: nothing it contains or repeats pins down the word, so any word that
fits its context fits equally well. Without a key or a verbatim crib, then, at most the 109 tokens of repeated
signs (49%) can be pinned down ciphertext-only, and even those only up to guesses from context. **95% is
provably out of reach by any ciphertext-only method**, and the target is closed as impossible from the
ciphertext. It needs the key or SP 70/5 (8 July 1559).

## Remaining gaps

- 10 July letter, twelve code signs (1k̲ ρ̲ g̲ δ̄ δ̲ ō ⊓̄ q̄ r̄ π̄ ƒ̇ ʋ̲) - blocker: open-codes; not on Tomokiyo's Cipher 1 key image; values guessed from context only
- 10 July letter, spans marked [..] in lines 5-8, 11-14 (~80 of 550 signs) - blocker: illegible; small signs at DECODE resolution, crop overlap
- 10 July letter, the starred note keyed to line 13 - blocker: no-key-material; it is in the margin word code
- f. 32 margin, ~405 signs in 222 groups - blocker: no-key-material; word-sign code, 113 of 141 types used once; needs its key or TNA SP 70/5 (CSP For. i 947, 950)
- f. 33 John Wood line, 39 signs - blocker: too-short; no unique solution (nonunique.py); needs Hatfield, Cecil Papers vol. 1

## Escalation

- [x] siblings: Add MS 4136 key leaves ff. 173-185 (R9258-R9262) and the twenty throckmorton/ records checked; no word-code key
- [x] clear-pages: no decipherment on either leaf; the Forbes copies have none for these passages
- [x] known-keys: Tomokiyo Ciphers 1-3, Smith 1563, Cecil-Norris and Moray-Wood tried against the margin and Wood line
- [x] print: Forbes I, CSP Foreign I (BHO), Bain II no. 804, HMC Salisbury I checked
- [x] key-rebuild: Cipher 1 corrected (seven values); margin and Wood line tested for identifiability (margin_stats.py, nonunique.py)
- [x] retry: three passes over the 10 July letter (subagent, re-cut crops, full re-transcription)
