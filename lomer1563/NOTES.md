# "Mr. Lomer" (John Somer) to Secretary Cecil, Paris, 9 December 1563 (BL Add MS 4136 ff. 138-139, DECODE R9235) — NOTES

Status: no write-up

**Verdict: closed. It was deciphered at the time and the decipherment is calendared.** Session 2026-09-21. "Mr. Lomer"
is a misreading of **John Somer** (Sir Thomas Smith's secretary, sent to Paris in the autumn of 1563). The letter is
*Calendar of State Papers, Foreign, Elizabeth* vi (1869), no. 1471, "Somer to Cecil … Paris, 9 Dec. 1563. Signed.
Orig. Portions in cipher, deciphered." The calendar summary is saved in `csp_vi_1471.txt`
([british-history.ac.uk, pp. 604-615](https://www.british-history.ac.uk/cal-state-papers/foreign/vol6/pp604-615)).
Nothing new is added here beyond identifying the writer and the key, so catalogue entry 95 is removed and there is
no site page.

## The record (2 images = ff. 138-139, Forbes's copy of the ciphered passages)

Add MS 4136 is Patrick Forbes's deciphering file (see `smith1562/NOTES.md`, `throckmorton/NOTES.md`). Like R9255 it
is composite:

- f.138 top: passages (41)-(54) and the signature "N. Throkmorton" at the end of a Throckmorton despatch. These
  belong to the Throckmorton series (third cipher, clear null words *quant, apres, car, hault, pour, yea, because*).
- f.138 foot to f.139 top: **Somer to Cecil**, passages (1)-(10), margin "Mr Somer Secretary Cecill Dec. 1563",
  signed "J. Somer". This is the DECODE target.
- f.139 rest: passages (11)-(17), endorsed at the foot "Sr Tho: Smith", in the same sign set. Probably Smith's
  letter of the same packet. Not matched to a CSP number here.

DECODE's "London" is wrong (Paris); day 9; language English.

## The key: Throckmorton's third cipher (R9262, f.180)

Somer did not use Smith's own cipher (R9261); his signs and his clear nulls are those of "Sir Nicholas Throckmorton's
third Cipher" (R9262 p.1). Somer was working in Paris alongside Throckmorton (then under arrest) and Smith, so this fits.
Checked on passage (1), lines 2-3 (`transcription_p1.txt`):

| cipher | key values | reading |
|---|---|---|
| `+4.2te` | f r o m | from |
| `τ` | the (word sign) | the |
| `+6.8‡⅃ɦ` | f r e n c h | French |
| `‡te⊔‡ss‡γ325.` | a m b a ss a d o r | ambassador |
| `‡γ6:857:∩7.vγ` | a d v e r t i s e d | advertised |
| `τ 9.‡te8` | the s a m e | the same |

CSP §3: "the French Ambassador, De Foix, advertised the same, and much more, hither". Line 1 opens `γ8 ‡+3:γ …
‡ss6:6.vγ te8` = "… assured me". `bab`, `car`, `hault` are the key's nulls. The fit is exact on every value tried.
The whole letter was not transcribed: CSP gives its content and Cecil's office had the decipherment.

## DECODE corrections to queue

Author John Somer (not "Lomer"); place Paris; date 9 Dec 1563; English; status Decrypted (deciphered at the time,
CSP Foreign vi no. 1471); key = R9262 (Throckmorton's third cipher); f.138 top is the end of a Throckmorton letter,
f.139 lower half (11)-(17) is marked "Sr Tho: Smith".
