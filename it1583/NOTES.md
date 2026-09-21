# BnF italien 1583 f. 68 — Sforza reply to Zorzo Maino, 4 May 1446 (DECODE R7898)

Status: attempted, closed unread (written up as `docs/it1583.html`, 21 Sept 2026)

## The document

- BnF italien 1583 (Archivio Sforzesco, documents 1433–1500, bought 1867), f. 68; DECODE R7898, 1 image,
  "Non-decrypted", no metadata. A slip pasted on a guard, numbered (21.) and 68/22.
- Dated at the head in clear: "M°cccc°xlvj die iiij° may" = **4 May 1446**.
- Mazzatinti's inventory (Archivio storico lombardo X, 1883, p. 230; OCR in `asl1883.txt`, line ~10470, from
  archive.org `archiviostoricol10cava`): "f. 68. Risposta a quanto ha riferito Zorzo Maino (4 maggio). In cifre."
  So it is a reply (almost certainly from Francesco Sforza's side, then condottiere in the Marche) to what his agent
  Giorgio (Zorzo) del Maino reported. Next entry: "f. 70. Lettera di Vincenzo Amidani a Fr. Sforza (Milano 4 maggio).
  In cifre."
- Mixed text: clear Lombard Italian with ciphered stretches. Clear phrases read:
  "cetera Che nuy no sapiamo [c] questi ne cerchamo ne domandamo [c] tocha ad nuy cerchare questo, ma solamente
  cerchamo con lo nome de dio [c] nostra raxone(?)"; "gli havemo rechiesto siano contenti fargli quello e dicto et
  ad quello se refferemo"; "[c] voglia essere contento mettere per scripto [c] se tra loro no gli sera noma uno
  che no habia [c] debitamente lo debiamo havere".

## Cipher

Graphic-sign cipher, 404 signs in 26 types after merging diacritic variants (draft transcription
`transcription.txt`, codes in its header; cipher-only `f68_signs.txt`). Two signs at 12 %, two at 7 %, flat tail.
The cross-circle sign (V) stands before clear clauses several times; in the related key below it is "de".
Repeats: FpBHcdSp (×2), 8zBprJFp (×2), xJpg (×4), FEpS (×3), FpBHc (×5).

## Attempts (21 Sept 2026)

1. Unconstrained homophonic annealing (it-cinquecento, clear text as context): collapses to "iiii".
2. Capped homophones, then nulls allowed: degenerate / nonsense.
3. One-to-one swap annealing (solver checked on a synthetic 400-letter Italian cipher: solved in 1 of 3 restarts):
   16 restarts, nonsense.
4. Word patterns: FpBHcdSp fits "uisconti", but the other repeats contradict that key.
5. **f. 70 found**: the slip at the top right of DECODE R7899 image P1 is f. 70 (pencil "1446 4 Mai"), Amidani's
   letter, all cipher, same sign family, a different hand. Draft transcription `transcription_f70.txt` (390 signs,
   31 types). Annealing on it alone: nonsense.
6. **Sforza keys on DECODE**: all 208 key records of ASMi Carteggio Sforzesco cart. 1591, 1597, 1598 downloaded
   (`fetch_keys.py`, `dl_keys.py`; images git-ignored) and scanned at thumbnail size; the 15th-c. copies at the
   head of cart. 1597 (nos. 2–36) read by heading and alphabet.
   - 1597 no. 14 (R-record name `Carteggio_Sforzesco_scat._n.1597_14`), an 18th-c. copy: "Angelus cum cifra
     Vincentij", used with "Johannes de Stavolis, Augustinus, Baptista, Matheus, et Vincentius". Same family as
     our signs: 2–5 homophones per letter, a sign for every vowel+consonant syllable (ab, ac, ad … uz), word signs
     (de = ♀, che, per, quale, con, ma, quello, perché, …), names (la S. V., lo Duca de Milano, Signoria Veneta),
     nulls. But its letter signs (a = o, ϙ …; e = ƅ, 5, ʒ; o = q …) are not the frequent signs of f. 68 or f. 70
     (⊧, ϕ, ƀ, barred ʒ). Not this key; it explains why simple-substitution solving failed.
   - 1597 no. 17: "M°cccc°xlvij … Zifra oratorum Ill. et Ex. Comitis … ad Ser.mum dnum Aragonum Regem"
     (1447, Sforza's envoys to Alfonso): different signs.
   - Nothing headed Maino or Amidani. cart. 1591 and 1598 are 16th–17th c.

## Why it is closed

The system has syllable and word signs over homophonic letters, and the only scan is binarized, so the diacritics
that may separate signs are unreliable. About 800 signs across two hands is not enough for a ciphertext-only
attack on a system like that. What would reopen it: the Maino/Amidani key of 1446 (look in ASMi Sforzesco
cart. 1597 at full size, and in Cerioni, *La diplomazia sforzesca*, 1970, vol. 2), or a colour scan of
ital. 1583 ff. 68–70 from the BnF for a sign-exact transcription.

## Related leads (not worked)

DECODE R7899–R7915 are seventeen more 1446 cipher records from BnF ital. 1583 (ff. 75–158): Nicodemo Tranchedini,
"Angelus" (Simonetta?), Stavoli and others. Some may be in the 1597 no. 14 key (Stavoli and Vincentius are
named on it). Worth a separate target.
