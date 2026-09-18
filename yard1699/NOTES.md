# Robert Yard to the Earl of Manchester, Whitehall 12 and 16 Oct 1699: NOTES

**Verdict: SOLVED (read in full, 18 Sept 2026).** The Beinecke catalogue calls both letters "almost
entirely in cipher, undeciphered". HMC 8th Rep. App. II p. 74 (xlix) adds that "No key to the ciphers
of the period is known to exist among the State Papers". The key has in fact been at Yale all along: the
Manchester papers' own "Diplomatic cipher, contemporary copy" (the THE=454 printed template). Both
letters read with it straight off, with no cryptanalysis. The key was validated first against the
interlinear decipherment on the sibling letter of 5 Oct 1699.

## 1. Sources

| Item | Yale OID (manifest `https://collections.library.yale.edu/manifests/<OID>`) | Box/folder |
|---|---|---|
| Yard → Manchester, 28 Sep/9 Oct 1699 (deciphered on the leaf) | 16601171 | 2/39 |
| Yard → Manchester, 5 Oct 1699 (deciphered on the leaf) | 16601172 | 2/45 |
| **Yard → Manchester, 12 Oct 1699** (target; pp. 1–2, p. 3 endorsement "Mr Yard 12/24") | **16601173** (IIIF 16601219–22) | 2/49 |
| **Yard → Manchester, 16 Oct 1699** (target; pp. 1–2) | **16601175** (IIIF 16601223–26) | 2/51 |
| **Key**: "Diplomatic cipher, contemporary copy", endorsed "Copy of the E. of Manchester's Cypher" | **2046948** (IIIF 1213691 recto, 1213692 verso) | 18/47 |

Tomokiyo (cryptiana `glorious.htm`, DECODE R2858–R2860) had already said that R2859/R2860 "can be
deciphered with THE=454", and he decoded the first few groups of each. No full reading had been
published: HMC calendars both as undeciphered. Cole's *Memoirs of Affairs of State* (1733) was not
re-checked for these two letters in this session.

## 2. The key (`key_raw.txt`, loader `key.py`)

It's a printed one-part template of 14 columns, each running A–Z: letters (3–162), two syllable columns
(163–482), then words and names up to 2342. The numbers are handwritten, one per slot, **skipping every
number ending in 5 or 9**, and 516–617 are skipped entirely. The marginal note says: "The numbers
under 3 and above 2342 and all numbers ending in 5 and 9 are Blanks. As are likewise the numbers
between 516 and 617". *Blanks* means nulls. In practice **every unassigned slot is also used as a
null**: 322, 482, 740, 742, 900, 902, 972, 1060, 1062, 1854, 2172, 2190, 2236, 2258, 2278, 2291, 2317, 2332,
2336, 2342. The 5 Oct letter's own decipherer skips 740, 900, 2172 and 2278 in the same way.
I transcribed all 1,456 assigned slots from the recto, in 25 tiles. Three entries sit in a fold and
can't be read (1584, 1744, 1904, the 3rd F-row entry of columns 10–12).

Differences between Yard's key and Manchester's copy (the handwritten numbering was not identical):
- the letter column: Yard uses **42 and 48 for *e*** ("sent th-r-e-e") and **21 for *d***
  ("Drummon-d-s"). This matches the HMC Addendum 141a reconstruction (48 = E, 21 = D), which
  Tomokiyo had flagged as "unmatching".
- 483 is printed "ard", but Yard uses it for *and* (so did Vernon, per Tomokiyo).

Yard's hand writes 2 in two ways, one looking like "V". So V3 = 23, V17 = 2317, V34 = 234, V36 = 236.

## 3. Plaintext

Deciphered words are in *italics*. The raw decode with syllable joins is in `oct12_decoded.txt` and
`oct16_decoded.txt`, and the transcriptions are in `oct12_ct.txt` and `oct16_ct.txt`.

**Whitehall 12 Oct 1699.** "I have the favor of your Lordp's letter of the 7/17 of this month, and am
sorry I could not effect what your Lordp desired in your letter of the 3d Oct. I hope at an other time
your Lordp will be able to give me earlier notice, and I assure you nothing shall be omitted on my part.
The *messengers stay yet at Dover* looking *for Mills*. I hope wee shall *meet with him at last*. Wee
have an account from the Lords *Justices of Ireland that they* have *received private information that
many disaffected persons return* dayly into that *Kingdom*, and that there *is some ill design against
the Government*. The *like intimations* come from *the north* that some*thing is designed in Scotland*,
and there *the same intimations* likewise with relation *to England*. And all is said to be carryed
*on very privately at Saint Germains*, which I take the liberty *to mention* that your Lordp *may
endeavour all you can to get light* into *what* they are *doing at Saint Germains*.
By the last *post from France* wee *found* at the *post house a letter* from one *Lebrun at Paris to
Dunster at the* three Lyons in *Bedford Court*, with an *enclosed for Mr. Gray*; but upon *reading it*
could find *nothing therein* but *private concerns*, and so *sealed again and* delivered. Your Lordp may
please to be informed *of your correspondent* who this *Gray is*.
Wee shall now expect the King with the first fair wind; for wee conclude his Majesty would be ready to
embarke to morrow or Saturday. …"

**Whitehall 16 Oct 1699.** "I received by the post yesterday the favor of your Lordp's letter of the
11/21 instant, and as soon as I understood the contents of it, and that *Mills* [1276 = *have not*,
sic; a slip] was *gone* by the *way of Rouen*, I gott *warrants* prepared, and *sent three* severall
*messengers* to *watch his landing* all along *the coast where* it may be thought *he* may *land*; and
*at London too* he is *watched* where *he lives*; and besides wee still *keep a messen[ge]r at Dover*
*to watch him* and *Lord Drummond's priest* [enciphered pre-su-t] these, for I think nothing would be
*more usefull* then to *take them and their letters*.
I have given directions *likewise concerning Fowles*, and will endeavor to have *him met with*. Tho I
must acquaint your Lordp that there is no *goldsmith lives* in *Round Court*, nor any body *named
Cockburne*; but there is *one* of that *name, a thread* man in Bedford *Court*, whom I have ordered
*enquiry* to be made.
I suppose your Lordp has heard of *Clance the periwig maker*; *he is* gone lately *to France*. Your
Lordp will please to have *him observed* and to give *notice* of *his return*.
Wee are now looking out very impatiently for an Easterly wind to bring the King over. …"

## 4. Checks

- **Key validation on a letter deciphered at the time (5 Oct 1699).** `454 1322 120 306` = *the
  person s we* (interlined "the Persons we"). `622 [740 900 2172] 327 347 1038` = *for at Dover*.
  `328 261 323 [2278]` = *appear*. `241 120 128 356 211 112` = *messenger*. `293 304 130 340 [438] 502
  804` = *to watch … coming*. All of these match the contemporary interlinear decipherment.
- **The readings are self-consistent.** Every non-null group in both letters decodes to a word or a
  syllable joining into a word, apart from Yard's slips: 1276 (*have not*) after "Mills"; 266 for 286 in "coa-st";
  "pre-su-t" for "priest"; 20 (*c*) for *s* in "gold-s-mith"; *messen[ge]r* missing a syllable. The proper names (Mills, Lebrun, Dunster, Gray, Fowles,
  Cockburne, Clance, Lord Drummond's priest) agree with the Beinecke summaries of the neighbouring
  letters ("Mills and Lord Drummond's priest", "persons expected at Dover").
- Reading doubts: the 12 Oct opening group `656` (*like*) and the 2 digits shaped like "V" were checked
  on the enlarged crops (`crop.py`).

## 5. Files

`key_raw.txt` (key transcription; `python key.py` expands and checks it), `dec.py` (decoder: `python
dec.py oct12_ct.txt`), `oct1{2,6}_ct.txt`, `oct1{2,6}_decoded.txt`, `crop.py` / `kcrop.py` (crop
helpers), `manifest.json` (12 Oct manifest). The images are not committed (`.gitignore`). Refetch them
with the IIIF ids in §1.
