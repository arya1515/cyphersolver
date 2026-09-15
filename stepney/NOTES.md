# George Stepney to the Earl of Manchester, Vienna 23 March 1702 — NOTES

**Verdict: OFFLINE-ONLY** (manuscript located and fully transcribed; the key is not the
THE=454 Manchester cypher; 24 groups of an unknown two-part nomenclator cannot be broken;
the key / plaintext should exist in TNA or BL material that is not online).

## 1. Sources (identifiers)

| Item | Where | Status |
|---|---|---|
| The letter itself (autograph, 1 leaf + endorsement leaf) | Yale Beinecke, James Marshall & Marie-Louise Osborn Coll., **OSB MSS fc37 (Manchester papers), Box 8 folder 40**; Yale digital OID 16601200; IIIF image ids 16601263–16601270 (`https://collections.library.yale.edu/iiif/2/<id>/full/full/0/default.jpg`) | downloaded: `img/stepney_01..08.jpg` (full), `img/small_*.jpg`, `img/crop_01_12_47_68_72.jpg` (cipher lines) |
| DECODE / DECRYPT database | record **R2864** "George Stepney to Manchester, Vienna, 23 March 1702 (Non-decrypted)" | listed by Tomokiyo; DECODE images login-only |
| Tomokiyo's article | cryptiana.web.fc2.com/code/glorious.htm ("Diplomatic Codes after the Glorious Revolution and Use of Printed Templates") | saved `cryptiana/glorious.htm`, `.txt` |
| HMC 8th Report, App. II (1881), Duke of Manchester's MSS, p. 86 no. (xl) | archive.org `EighthReportHistoricalMSS` (`ia/EighthReportHistoricalMSS_djvu.txt` l. 234093) | calendar only: "*March 23.—G. Stepney to the Earl of Manchester, announcing the ratification of the article against the Pretender, and expressing some anxiety respecting the position of Prince Eugene in Italy although the expedition to Naples had been deferred. (Partly in cipher.)—Vienna.* March 23—Attached is a memorandum giving the news [that] had reached Vienna of the progress of events in Europe (pp. 5)." **No decipherment printed** (other entries in the same calendar say "Partly in cipher, deciphered" when a decipher exists). |
| *Court and Society from Elizabeth to Anne* (1864) vols 1–2 | archive.org `courtsocietyfrom01mancuoft`, `courtsocietyfrom02mancuoft` | do **not** print this letter |
| THE=454 key ("Duke of Manchester's Cypher") | Yale OSB MSS fc37 (catalogued "1701 July"); DECODE **R2858**; reconstructed in HMC 8th Rep. *Addendum* 141a (not in the IA scan we have) | described on cryptiana; letter tested against it below |

## 2. Full text of the letter (from the images; see `ciphertext.txt`)

> Vienna. 23d. March 1702
> My Lord,
> I am hon'd with yr letter of ye 10th past. This will come to ye Hague by a Courier of
> Count Wratislaw's; who will carry the Emp'rs Ratification of our article agst ye P.P. of W.
> **836. 468. 445. 242. 233. 55. 44. 370. 30. 325. 576. 246. 388. 380.** but it is no fault of
> mine who both by word of Mouth & by Memorial have remonstrated of what Consequence it would
> be to have **418. 847. 398. 370. 360. 731. 102. 271. 632. 413.**
> Our project may lye by, for yr Lp will have heard our expedition of Naples is layd aside
> for a fitter season; It will be well if Pr. Eugene can secure himself upon a good defensive,
> considering how much the French are likely to be superiour in Numbers: Wee have been late
> with our Recruits, & our Reinforcement cannot be in Italy in less than two months.
> The E. of Bavaria continues surly. I am with respect My Lord, Yr Lordship's most humble &
> most obedt servant G Stepney.
> To the E. of Manchester. [endorsed:] Vienna March 23 1702 Mr Stepny

Corrections to the published excerpt: Tomokiyo's last group **412** is **413** in the MS
(clear in the crop). Everything else agrees. There is **no interlinear, marginal or fly-leaf
decipherment** anywhere on the 8 images; the endorsement is only date + sender.

Same folder (images 3–7): an unsigned Vienna news-sheet of 22 March 1702 (Polish treaty
for 8000 men, Warsaw reports, Cardinal Lamberg, Gen. Thüngen, Venetian complaint about
Prince Eugene at Ponte Vico, King of Prussia) — the "memorandum, pp. 5" of the HMC entry;
entirely en clair, no cipher.

## 3. Sibling material / keys found (previous session + this one)

- **Yale search.** The Yale `catalog.json` API returned empty bodies (`yale_out.txt`), but
  the IIIF ids were resolved and all 8 canvases downloaded (`iiif_out.txt`). No other
  Stepney/Manchester items were fetched; the digitised Manchester papers at Yale are
  the source of DECODE R2854–R2872 (keys THE=452, THE=454, Yard/Jersey/Vernon letters
  1699–1700, an Italian cipher 1700, this letter). No image of a key for 1702 and no
  deciphered Stepney letter was found.
- **THE=454 key (R2858).** Printed template, numbers 3–2342; nulls = numbers <3, >2343,
  all ending in 5 or 9, and 516–617. Structure recovered from Tomokiyo's decipherments
  (`analyze.py` KEY454): letters 3–c.160 alphabetical (a=4,6,7,10; d=28,33; e=36–40;
  f=42,48; k=72; l=73,74; n=87,88; o=93; r=112–117; s=120–128; t=130; w=146); syllables
  c.164–515 in two alphabetical series (as164 … ye316; an326 … con500, the=454);
  words 618–2342 in several alphabetical series (for622 … you736; but751 … writ888; any908
  … the King1128 … equal1900). Used by Yard/Jersey/Vernon → Manchester at Paris 1699–1700.
- **HMC 8th Rep. App. II p. 85 (clxi), 13 Aug 1701 n.s.:** Manchester (Paris) "wished to
  have **Mr. Stepney's cipher**, as there was a suspicion that letters from Vienna were
  opened." So Stepney's own cipher (his cipher with the Secretary's office) was
  requested for Manchester in Aug 1701 — this is almost certainly the key used here.
- **HMC 8th Rep. App. II p. 86 (xxxii), Stepney 8 Mar 1702:** Stepney asks Manchester that
  their correspondence "may not interfere with Mr. Secretary [Hedges, Northern Dept.]
  in what relates to his province" — Vienna belonged to the Northern Department, so these
  letters are semi-private; Stepney's *official* dispatches of the same week (TNA SP 80)
  and his letter-book copies would carry the plaintext.
- HMC note on Yard's undeciphered letter of 12 Oct 1699 (p. 74, xlix): "No key to the
  ciphers of the period is known to exist among the State Papers" — refers to the 1699
  Paris cipher, not to Stepney's.

## 4. Structure (`analyze.py` → `analyze_out.txt`)

- 24 groups: 21 three-digit, 3 two-digit (55, 44, 30); range 30–847; only repeat 370
  (once in each passage). Last digits fairly flat; 3 groups end in 5 (445, 55, 325), none in 9.
- Tiers: 30/44/55/102 (letters), 233–468 (15 groups, syllables), 576, 632/731/836/847 (words).
  Same letters/syllables/words architecture as the Secretaries' printed templates, but
  nothing above 847 (THE=454 traffic uses 1000–1900 freely) → probably a smaller key.
- **THE=454 test fails**: under its null rule P1 has 4/14 nulls (445, 55, 325, 576) and
  P2 0/10; the non-null groups read "[836≈move..prize] way mi la f [370≈en..gr] d …" —
  not English (44 sits in the e/f block, so "Mila-n" is excluded). Tomokiyo reached the
  same conclusion implicitly (R2864 is his only Manchester letter not marked "can be
  deciphered with THE=454").
- Sequence 55 44 370 30 (letter-letter-syllable-letter) looks like a spelled name/word.
- Context cribs (unverifiable): P1 qualifies the Emperor's ratification of the anti-Pretender
  article ("which comes very late / ought to have been done long since / with an alteration");
  P2 completes "of what consequence it would be to have [it dispatched in time / a squadron
  in the Mediterranean / the fleet in Italy]" before "Our project may lye by … expedition of
  Naples is layd aside". With one repeat and no key, ~all 24 groups remain unbroken.

## 5. Where the key / plaintext is (offline)

1. **Stepney's letter-books**, TNA SP 105 (Archives of British Legations; Stepney's Vienna
   volumes c. SP 105/60–66) — copies of his out-letters normally give the plaintext.
2. **Stepney Papers, BL Add MSS 7058–7078** — his own copies of letters and (reportedly) his
   cipher keys.
3. **TNA SP 106** (State Papers Foreign, Ciphers) — the office's cipher templates of this
   type (SP 106/6 etc. hold the Charles II / William III printed-template keys per Tomokiyo).
4. Any copy of "Mr. Stepney's cipher" sent to Manchester in Aug–Sept 1701 would be in the
   Manchester papers (Yale OSB MSS fc37, or the portion at Huntingdonshire Archives), but it
   is not among the two keys Yale has digitised (THE=452, THE=454).

## 6. Files

- `ciphertext.txt` — full transcription with the 24 groups (MS reading 413, not 412).
- `analyze.py` / `analyze_out.txt` — structure, THE=454 partial key + null-rule test, cribs.
- `img/stepney_01..08.jpg`, `img/small_*.jpg`, `img/crop_01_12_47_68_72.jpg` — Yale IIIF images.
- `ia/*_djvu.txt` — HMC 8th Report and Court & Society OCR; `cryptiana/` — Tomokiyo pages.
