# Prince Rupert / Royalist ciphers 1645-46 — cryptiana unsolved items #5 and #6

## #5 Maurice -> Rupert, Worcester, 7 July 1645 (Warburton, *Memoirs of Prince Rupert*, iii. 133)
Ciphertext (full, from the 1849 print; `maurice1645.py`): 93 groups, 63 distinct, max 398; 18 distinct groups < 100
(letters), 45 >= 100 (words). Repeats: 148 x5, 15 x4, 229 x4, 293 x4, 26/84/150 x3. Clear words interleaved:
"By your cipher, you may observe, that ... Garrison, ... Accordingly, ...". Context: the Scots army under Leven
was four miles from Worcester; Maurice is explaining why he cannot bring his regiments to Rupert at Bristol.

Known keys tested (ranges only, by Tomokiyo and here): Charles I-Rupert-Digby-Ormonde 1644-45 (has letter+digit codes
a1..p5, words to 421) and Nicholas-Rupert July 1645 (words 98-373 and 427-616) do not fit. "By your cipher" = a
cipher Rupert issued to his brother; no copy is known in print.

### Where the key would be — all located, none reachable online (2026-09-15)
- **BL Add MS 18980-18982** (Rupert Correspondence 1642-45, Warburton's source): all three volumes are digitised
  (ark:/81055/vdc_100163595876, vdc_100176984506, vdc_100165006764) but the catalogue says *"digital images
  currently unavailable"* — offline since the October 2023 BL cyber-attack; IIIF manifests return 403.
  The 18982 contents list (searcharchives.bl.uk/catalog/040-002095608) shows Maurice->Rupert 29 Jan 1645 at
  ff. 27-28 but no cipher-key item; the 7 July letter is not itemised there (Warburton may have used another volume).
- **DECODE** has 47 records from Add MS 18980-82 (R8429-R8454, mostly "Decrypted" 1645 letters with interlinear
  decipherment) and 81 from Add MS 72438 — images require an account and are flagged private (BL permission needed
  to publish). Public thumbnails are 200 px, unreadable.
- Cryptanalysis on 93 groups of a ~400-entry nomenclator: not feasible.
**Status: offline-only** (needs BL images back online, or a DECODE account + BL permission).

## #6 Intercepted royalist letters, BL Add MS 72438 ff. 9-10 (DECODE R8623, R8624), May 1646
Add MS 72438 = Trumbull Papers vol. 197, Weckherlin's cipher-keys and intercepts, incl. the 49 keys taken from
Digby's coach at Sherburn (Oct 1645). Catalogue (searcharchives.bl.uk/catalog/040-001967027): f. 9r "Intercepted
letter, addressed to 'My Lord' ... 21 May 1646. Largely in (undecoded) cipher"; f. 10r "Intercepted letter to King
Charles I, 13 May 1646. Largely in (undecoded) cipher". Also f. 104r and f. 171r undecoded.
- Full ciphertext is **not available anywhere online**: cryptiana prints only the first two lines of f. 9
  ("My lord your Lo^p being not a little beholding to 309 for y^e 500 44 66 24 21 107 195 155 212 well 32 66 25 155
  151 12 38 35 26 81 38 122 ..."; letters as 2-digit, words 107-500); DECODE records are "Private Ciphertext: True",
  authentication required; the BL digitisation (vdc_100162920089) is offline (403).
- The "cf. Biermann & Brown 2021" idea (their Isle-of-Wight key: letters 1-106, words 142-615) cannot even be
  tested on 40 groups of excerpt with the key table living in Cipherbrain comments; it is a 1648 key for a
  different correspondent in any case.
- The same volume holds 49+ keys (ff. 25-99, 100-109, 151-170) that would very likely read f. 9/f. 10 by simple
  trial once images are accessible — this is a "key in the same box" situation like Hamilton, not a cryptanalysis
  problem.
**Status: offline-only** (BL images offline; DECODE login + permission).

## Files
- `maurice1645.py` — the Warburton ciphertext and structure stats.
- `get_warburton.py`, `find_letter.py` — fetch/locate the letter in the archive.org OCR (`warburton3.txt`, not tracked).
- `thumbsize.py` — confirms DECODE public thumbnails are 200 px.

## If resumed
BL restores Add MS 72438 / 18982 images (check the catalogue "Digitised Content" field) -> pull IIIF manifests,
OCR-free eyeballing of the 49 Digby keys for one with words <= 398 and no letter-digit codes (Maurice), and run the
f. 9/f. 10 texts against every key in ff. 25-109.
