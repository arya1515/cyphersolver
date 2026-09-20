# Throckmorton, BL Add MS 4136: surviving key and published plaintext

**Result (20 September 2026): prior solution located and key verified on two samples.**
This is an archival verification, not a new cryptanalytic solution or a complete
transcription of all twenty DECODE records.

## Verified reading

The first complete numbered extract on **R9220, f.110, no.(6)** reads:

> all be it i be revoked or the warr breake

Normalized: **“albeit I be recalled, or war break out.”** Throckmorton asks Cecil
to obtain the Queen's permission for Mr Jones to stay abroad and gain experience
even if Throckmorton himself is recalled or war begins. The passage is printed in
Patrick Forbes, *A Full View of the Public Transactions in the Reign of Q. Elizabeth*,
I (1740), p.355, within the 7 March 1559/60 despatch. The leaf also includes the
8 March continuation and the separate 9 March letter to the Queen.

The archived **“Sr Nicholas Throckmorton's Third Cipher,” R9262, ff.180–185**,
provides the alphabet, nulls and word signs. The sequence has **27 cipher tokens,
including two nulls**, not 27 plaintext letters. Dotted 4, 5 and 6 all mean *r*;
plain 4 means *o*; colon-marked 6 means *u/v*. Marked A and b supply *all* and *be*,
a curved T supplies *the/to*, and *bo* supplies *-ed*. The final double *r* in
*warr* is real; an earlier reading as *wars* was corrected in the existing dossier.

The second test, **R9230, f.133, extract (1)**, reads **“orleans or burges”**
from 15 alphabet tokens. Forbes II (1741), p.12 gives the same words, and
[CSP Foreign V, no.425, paragraph 11](https://www.british-history.ac.uk/cal-state-papers/foreign/vol5/pp197-215)
summarizes the passage: the apparent preparations against Orleans or Bourges may
conceal an attack on Rouen, Newhaven (Le Havre), and Dieppe. CSP no.426 records
a separate decipher of the ciphered passages. The sentence beyond the sampled
words has **not** been transcribed token by token here.

Both readings are **H** under this repository's convention: glyph values read
from the archived key. The Forbes facsimiles were also checked visually: I p.355
and II p.12 (Internet Archive leaves 386 and 44). The inherited dossier incorrectly
cited II p.31 / pp.28–35 for the second sample; that reference is corrected here.
Word spacing, capitalization and expansion into modern
English are editorial. The published texts were available during these checks;
neither is a blind decipherment. The archive key is an archived reconstruction;
its proximity and catalogue date do not establish that it is the original
sixteenth-century operational key.

Replay with `python decode_control.py` and `python decode_control.py control_9230`.
The JSON files contain the glyph labels, every token, key sources and limitations.
Replay verifies application of the transcribed key; visual comparison supplies
the evidence for the glyph identification.

## What was retrieved

The existing authorized-cookie downloads include all **54 image references** for
the twenty target records. Hashing shows **39 unique images**, because adjacent
records often overlap on a leaf. R9220 and R9221 are the same image under different
file names. The four nearby key records add **17 images**. All 71 referenced files
were checked for JPEG signatures and hashed in `verified_inventory.json`.

| Key record | Actual scope | Relevance |
|---|---|---|
| R9257, f.172 | Percy extracts above a separate alphabet and nomenclator | Not evidence of a Throckmorton key merely because it is nearby |
| R9260, ff.177–178 | A preceding cipher fragment and Throckmorton's first/second keys | Earlier Throckmorton systems; not the tested key |
| R9261, f.179 | Heading: Sir Thomas Smith's cipher | Different alphabet; potentially relevant to Smith material in composite R9255 |
| R9262, ff.180–185 | Throckmorton's third cipher, eleven images | Direct match to both samples |

Images are retained in the git-ignored research directory. DECODE's notices
restrict republication; the public write-up links to the records without copying
the manuscript photographs. The session cookie is neither copied nor printed.

## The twenty records and their published counterparts

See **[CONCORDANCE.md](CONCORDANCE.md)** for every record, folio, normalized date,
recipient, CSP entry and Forbes reference. **[PUBLISHED_REFERENCE_TEXTS.md](PUBLISHED_REFERENCE_TEXTS.md)**
contains the cached historical Calendar entries, explicitly labeled as edition
text, not as a new decipherment. These entries often summarize rather than
transcribe the dispatches.

The exact records are R9220–R9234, R9242–R9245 and R9255. They are not every record
in the numerical range R9220–R9255. Dates in the concordance are January-start
years: March 1559 in the manuscripts corresponds to March 1560; January 1562 to
January 1563. This does not change the calendar day. R9234 is dated 1 November
1563, and should not be changed to 1562 to fit its neighbours.

R9232 is matched provisionally to CSP V no.597 by its 9 September dispatch of
Francisco. Nos.599–600 are other same-day Cecil material and remain comparison
candidates. **R9255 is composite**: its Throckmorton portion is 22 November 1562,
CSP V nos.1099–1100 / Forbes II p.208. Smith, Somer and Randolph material on the
same record is not solved by merely citing that Throckmorton letter.

## Correcting the proposed target

[Tomokiyo's Elizabethan cipher study](https://cryptiana.web.fc2.com/code/elizabeth.htm)
already explains that these are largely extracts of ciphered passages, cites
Forbes, reconstructs three Throckmorton ciphers, and notes the surviving archive
keys (November 2024 update). Credit for that identification belongs to Tomokiyo.
The DECODE status “Non-decrypted” does not establish that no plaintext exists.

The meaningful two-digit superscript remark was copied from the preceding
Serno Gilino/Bishop of Worcester discussion on the unsolved list. It is not a
description of the Throckmorton third cipher. The two specifically unresolved
cases Tomokiyo identifies are the marginal material on **R2988** and John Wod's
1568 material on **R2989**; neither belongs to the twenty-record target here.
This investigation does not solve either of those cases.

## Limits and next work

The verified extent is **42 transcribed tokens in two passages**. No fraction of
the entire corpus has been measured. Most of the twenty correspondences are
date/addressee and source-heading matches; they have not been checked glyph by
glyph. A complete diplomatic edition would require transcribing the 39 unique
leaves, separating letter boundaries and other writers, and aligning each
numbered extract with Forbes/CSP. Nothing in this result establishes a newly
recovered historical secret or a first decipherment.

For the proposed “unknown cipher” target, the useful conclusion is that the
archived key works and published plaintext already exists. The remaining work is
an edition and completeness audit, not an evidence-based claim of twenty new solves.
