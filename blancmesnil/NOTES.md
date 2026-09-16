# Nicolas Potier de Blancmesnil → Duke of Nevers, "ce dernier juin" (BnF Français 3633, f. 24, no. 15)

Session 2026-09-16. Blocked at the ciphertext.

## Source

- Tomokiyo, *Catalogue of Ciphers (Mainly Related to Duke of Nevers)* (cryptiana `nevers.htm`), section "BnF fr.3633 (of which
  I have seen only some pages)": "Blancmesnil (f.24, no.15). A letter of Nicolas Potier de Blancmesnil to the Duke of Nevers,
  dated 'cer dernier juin', contains some phrases in cipher." No image, no transcription, no length.
- The same article gives a **Potier-Nevers Cipher** reconstructed from BnF fr. 3987 f. 1 (image `league9.png` in
  `../gallica_siblings/src/`): a letter-and-symbol homophonic alphabet a-z with codes for *que, qui, par, les*, used in
  Blancmesnil's letters of September 1589 (fr. 3987 ff. 45-48). If f. 24 of fr. 3633 is from 1589 it may well be in this key
  — that is the key-application hypothesis of the short list.

## Why it stops

**Français 3633 is not on Gallica.** Checked 2026-09-16 with the SRU API (`dc.title adj "Français 3633"` returns nothing;
`dc.title all "3633" and dc.type all "manuscrit"` returns only Arabe 3633 and Pelliot 3633). The link on Tomokiyo's unsolved
page next to this entry (`archivesetmanuscrits.bnf.fr/ark:/12148/cc57784f/cd0e3327`) resolves to Français 4736, the Danzay
volume, not 3633. The tracker's "Gallica IIIF" note for this item (row 5 of the 2026-09-16 short list) was an assumption
and is wrong. There is no ciphertext to measure, so nothing more can be done online.

What would move it: a reader's copy of fr. 3633 f. 24 (BnF Richelieu), then apply the Potier-Nevers key from fr. 3987 f. 1.

Checked: Gallica SRU for the shelfmark, the catalogue link on the source page. Not checked: the BnF Archives et manuscrits
notice for fr. 3633 itself (the search page needs a browser). User must verify: that no other digitisation exists.

## Second pass, 2026-09-16 evening: DECODE and catalogue cross-check — closed, not solvable online

- **fr. 3633 is not in DECODE** (`RecordsList?cmd=search&search=3633` returns nothing) and a second Gallica SRU sweep
  (`dc.title adj "Français 3633"`, `gallica all`, `dc.title all "3633"`) again returns only Arabe, Pelliot and unrelated items.
- **The Blancmesnil letters that are online as metadata are siblings, not the target.** DECODE holds fr. 3616 no. 11
  (R9433, anon., Bourges 24 Feb 1589), **no. 24 (R9434, Blancmesnil, Chaalons, 9 Dec)**, no. 45 (R9435, Chaalons, 11 Sept),
  no. 64 (R9436, anon., non-decrypted), no. 81 (R9437, Blancmesnil, 12 July) and fr. 3621 no. 79 f. 89 (R9448, Blancmesnil,
  30 May 1592), all entered 18 Jan 2025 by user 243 ("pabogi"), all but no. 64 marked *Decrypted* because the sheets carry
  a contemporary interlinear decipherment ("Letter, with cipher and decryption"). Tomokiyo's Nevers catalogue lists the same
  fr. 3616 items under "letters in cipher (which I have not seen)" and separately lists **fr. 3633 f. 24, no. 15, "ce dernier
  juin"** — so the "no. 24" coincidence is a different letter in a different volume, not a misprint. fr. 3616 and 3621 are not
  on Gallica either (SRU empty), and DECODE marks the images "not in the public domain … only with the permission of the
  Library" (login required in any case).
- Consequence for the key hypothesis: three Blancmesnil-Nevers letters of 1589-92 with their decipherments exist in fr. 3616
  and 3621, plus the four of September 1589 in fr. 3987 ff. 45-48 from which Tomokiyo reconstructed the Potier-Nevers cipher.
  If fr. 3633 f. 24 is in that key the job is a lookup; if not, the fr. 3616 decipherments are the next key to try. Neither
  step is possible without a reader's copy or DECODE image access.

**Verdict: not solvable online, 2026-09-16.** Blocked at the ciphertext; the key material is catalogued but not fetchable.

Checked: Gallica SRU (three query forms, fr. 3616/3621/3633/3987), DECODE metadata for the six Nevers-collection Blancmesnil
records and the search index for "3633". Not checked: the BnF Archives et manuscrits notice (the search page is
script-rendered and returned no text), DECODE images (login). User must verify: DECODE record numbers before citing them.
