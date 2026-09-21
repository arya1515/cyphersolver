# R2234: an Orangist correspondent at Basle to William V, 17 August 1796

Status: read (21 Sept 2026)

- **Record.** DECODE R2234, KHA The Hague, Prins Willem V, inv. 339. Catalogue 221 (class A, rule-scored).
  DECODE: "Non-decrypted", 1 p., homophonic, alphabet, French. Pencil on the leaf: "9360", "Tollius".
- **Key.** DECODE R2235 in the same inventory number: two printed-form sheets, a *Schrijf Tafel* (encipher) and a
  *Translateur Tafel* (decipher), each with five monoalphabetic alphabets labelled D, G, L, N, R over the
  25-letter alphabet a–z without j. D and R are inverses of each other, G and N likewise, and L is its own
  inverse; the Translateur sheet is the Schrijf sheet with those pairs swapped. Transcribed in `decrypt.py`.
- **System.** Not homophonic. The letter is written in seven sections, each opened with a capital (D, G, L, N, R,
  D, G) at the left margin. The capital sets the alphabet of the first line; each following line (marked with a
  dash) steps to the next alphabet in the cycle D→G→L→N→R→D. Word division, digits and punctuation are left in
  clear. The date line ("30 thermidor an 4 de la Rép. franç. / 17 août vieux style") and the closing
  "Salut et fraternité" are in clear.
- **How found.** "gasoez ma 12" of line 1 gave "depuis le 12" with alphabet D. Line 2 read with G, line 3 with L,
  and so on: the per-line cycle was found by trying all five alphabets on lines 2–5.
- **Transcription.** Claude, from the single DECODE scan (IMG_R2234_I15510_P1, rotated 90°), `ct.txt`,
  1,321 cipher letters. The residual garble in `decrypt_raw.txt` comes from transcription slips (n/r/v/u,
  c/e, i/y), not from the key; `reading.txt` is the corrected French.

## Reading

See `reading.txt`. A correspondent in Basle, writing in Republican dating, to the Stadholder in exile:
no letter since 12 July; asks for a decision by 4 September on keeping his lodging (lease ends 4 October) and for
a bill of exchange of 50 louis every three months, Basle being very dear. News: an officer says the Prince of
Salm is raising a hussar regiment for the King of Prussia on condition that it return to the Prince of Orange's
service when he goes back to Holland; the report that "the prince" will have Hamburg(?) and the land around
Osnabrück; fear that the Prussian ministers are lulled by the French, who want only to hold both banks of the
Rhine. Barthélemy (the French envoy at Basle) no longer invites him since he was named in the Hamburg gazette of
5 July; Barthélemy's secretary expects the Army of Italy to join the Army of the Rhine through the Tyrol within a
month, "which does not look like peace"; Degelmann (the Imperial envoy) does not believe it. A French courier
from Italy arrived and nothing transpired, so bad news for them. If a congress were held he could do nothing
there without being seen.

Unread or doubtful: the end of line 5 / start of line 6 ("j'en suis aux derniers …"), a place name in line 10–11,
two words before "et Barthélemy" in line 13, and the verb in line 20. Signature in clear not read. The writer is
unidentified; the archival pencil "Tollius" (Herman Tollius, the princes' former tutor, named in the DECODE note)
is an attribution, not tested here.

## Prior work

DECODE status "Non-decrypted"; the record's note already pointed to R2235 as the likely key but gave no reading.
No printed decipherment found. Key from the archive; ciphertext read with it on the first attempt.
