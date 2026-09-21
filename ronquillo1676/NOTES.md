# Salinas (London) and Ronquillo (Nijmegen) to Fuenmayor, 1676–78 — DECODE R966–R984, R1001

Status: read

The remaining ciphered letters in Baltasar de Fuenmayor's volume, Archives générales du Royaume, Brussels,
Secrétairerie d'État et de Guerre, inv. nr. 2559 (see [hernannunez1674](../hernannunez1674/NOTES.md),
[balbases1677](../balbases1677/NOTES.md), [carpio1677](../carpio1677/NOTES.md)):

- **Bernardo de Salinas, Spanish envoy in London**, eight letters, 21 Aug 1676 – 2 Mar 1677 (R966–R973)
- **Pedro Ronquillo, Spanish plenipotentiary at Nijmegen**, twelve letters, 21 Dec 1676 – 19 Mar 1678 (R974–R984,
  R1001)

DECODE's transcriptions were fetched 21 Sept 2026 (`img/`, git-ignored). R1000 in the same volume is French and
already decrypted on DECODE, so it was not taken.

**Result.** All twenty are in **the Balbases 1677 key** (`../balbases1677/key.json`, plus the four values added in
hernannunez1674). No changes were needed. Across the twenty the key reads 88.4% of 23,463 groups. Sixteen letters
carry a contemporary marginal decipherment, and the key output agrees with it. **Four have none in DECODE's
transcription, and these are new readings:**

| rec | letter | groups | read | DECODE status |
|---|---|---|---|---|
| R970 | Salinas, 15 Sept 1676 | 663 | 77% | partially decrypted |
| R973 | Salinas, 2 Mar 1677 | 199 | 86% | partially decrypted |
| R982 | Ronquillo, 19 Mar 1678 | 813 | 71% | non-decrypted |
| R984 | Ronquillo, 26 Feb 1678 | 1,144 | 86% | non-decrypted |

The images of R970 and R973 were not checked for a margin that DECODE's transcriber left out. If one is there, it
is a check on these readings, not a prior reading of them.

So one cipher served Fuenmayor's correspondence with at least three Spanish envoys: Salinas in London, Hernán
Núñez in Stockholm, and Ronquillo and Balbases at Nijmegen. Carpio in Rome used a different one.

Per-letter coverage (from `read.py`): R966 88%, R967 87%, R968 83%, R969 87%, R970 77%, R971 94%, R972 89%, R973 86%,
R974 93%, R975 89%, R976 70%, R977 88%, R978 93%, R979 92%, R980 89%, R981 89%, R982 71%, R983 89%, R984 86%, R1001 93%.

## Transcription formats (the only real work)

DECODE's transcribers used three conventions:

1. Groups are separated by double spaces and characters by single spaces (most records).
2. Every character is single-spaced, with no group boundaries (R971, R974, R978, R979, R983, R1001). The key first
   read these at 0%. They were rejoined and segmented with a dynamic programme over the key's vocabulary (`seg.py`:
   fewest groups, one-character groups penalised).
3. R970 and R973 write a sign as "Infinity" (∞), which is c before a vowel (∞o co, ∞i ci). R970's transcriber also
   writes 5 where the key has *a* and b for *que*, which accounts for most of its unread groups.

Unread groups are almost all transcription noise ("?", "*", split groups). R982's transcription is the worst (full
of "?"), and its reading is gist only.

## What the four new readings say (gist)

- **R970, Salinas, 15 Sept 1676.** "ya se habrá [sabido] el fatal suceso…". Salinas fears the blow will close
  "esta puerta". The discourses at the English court turn to a peace; the "progresos" on Fuenmayor's side move
  minds there; the minister has tolerated the event; the Danish fleet.
- **R973, Salinas, 2 Mar 1677.** The English princes are "no siendo tan malos" when it comes to withdrawing the
  troops from France, "en que me prometo persistirán". The preparations of the last months show that everything is
  in earnest. The discourses treat the peace as good as made.
- **R982, Ronquillo, 19 Mar 1678** (ten days after the fall of Ghent). The congress; Flanders surprised; "nos
  falta"; two months; the Brunswick princes; "estamos muy mal"; "melancólicas reflexiones".
- **R984, Ronquillo, 26 Feb 1678.** On Fuenmayor's reports of the assembly of the northern allies. Everything hangs
  on the resolutions of the English parliament and on whether the King really breaks with France. The Danes
  complain about subsidy remittances. Brandenburg is in Pomerania. The Duke of Hanover's intrigue ("esta trama")
  runs through his kinship with Madame.

## Files

`try.py` (the key plus additions), `seg.py` (segmenter), `read.py` (all twenty letters → `read/R*.txt`, each with
DECODE's margin transcription where there is one).
