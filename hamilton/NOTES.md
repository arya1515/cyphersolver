# Charles II -> Duke of Hamilton, 1650 — cryptiana unsolved item #3

Four letters (6, 14, 31 Aug; 27 Sept 1650) with passages in a small **numeric nomenclator** (numbers <= ~384).
Printed (cipher groups left undeciphered) in *An Account of the Preservation of King Charles II* (1766), p.86ff;
also HMC *Manuscripts of the Duke of Hamilton* (1887), items 393-396 ("printed, partly in cipher, not deciphered").

## Ciphertext (from the 1766 print, verified against cryptiana)
- 6 Aug 1650:  ...I have commanded **163** to give you a particular account... ask your opinion in two things;
  the first is **281 192 258 91 308 100 379 3 108 327 13**, whether it were not **6 70 199 65 330 153 237 56
  190 329 290 38 3**. The other is, what should be done **302 192 353 308 100 108 17 120**.
- 14 Aug 1650: I have sent this bearer **270 16 135 9 190 10** to acquaint you with my condition.
- 31 Aug 1650: Concerning **331 288 198 196 6 190 22 58 135 256 58 256 380 55** ... send to **122** about it.
- 27 Sept 1650: I have at last resolved that **85 237 70 9 50 40 384 4 10 308 290 304** by the **174 261 82 15
  347 8 3** ... receive particulars from **122** and **223** ... preparing yourself **281 329 165 244 9 42 65
  56 324**, to get you **20 174 36 9 40 13 15 38 61 195 289 4 5 384 380 10**.
- Bare code words used in clear: 163, 122, 132(=Dumfermline, per cryptiana), 223.

## Key source (the route to a solve)
The related **Lanark (Lanerick) correspondence, 1647-48** in the same Hamilton archive was deciphered and printed
by the **Camden Society, 1880** (= *The Hamilton Papers*, `hamiltonpapersbe00hamirich.txt` here; deciphered
portions set in italics). Checked 2026-09-14: Gardiner prints only the *decipherments* (no cipher figures) and
says explicitly (p. xxi) that the letters came "without any key being appended"; the 1650 letters are his
nos. 174-177 (pp. 255-256), printed with the figures and *not* deciphered. So the 1880 volume cannot yield the key.
Burnet's *Memoirs of the Dukes of Hamilton* (1677; 1852 ed. `burnet1852.txt`) narrates 1650 without printing them.

### THE KEY EXISTS — National Records of Scotland, GD406/1/2197 (found 2026-09-14)
NRS online catalogue, Hamilton muniments GD406/1 (Correspondence of the Dukes of Hamilton):
- **GD406/1/2197 — "Keys for ciphers used in the correspondence of the Duke of Hamilton." c 1645. 5 items.
  Access: Open, on site.** Description: "These cipher keys can be used to decipher the encoded parts of some of
  the letters sent to the duke of Hamilton." (The "c 1645" is a cataloguer's guess for undated sheets; the
  2nd Duke's 1650 key may or may not be among the five.)
- The four letters themselves: **GD406/1/10573** (6 Aug), **10574** (14 Aug), **10575** (31 Aug), **10576**
  (27 Sep) — originals bound in the *Hamilton Red Book*, vol. ii, nos. 156-159; not produced to readers, but a
  **microfilm is available in the Historical Search Room**. 10576 catalogued "[Partly in cipher]".
- Related: GD406/1/2496, Patrick Maxwell, Paris, June 1650, to the Duke, "asking for the duke's cipher" (closed,
  unfit for production) — shows Hamilton was issuing a cipher of his own in 1650.
- Other undeciphered cipher items c.1648 in the same series: 2181, 2189, 2191, 2194-2196, 2206, 2232, 2288.
Gardiner (1880) evidently never saw 2197. **Next step: order digital copies of GD406/1/2197 (5 items) from NRS
(lsrhe@scotlandspeople.gov.uk / copying service) and, if the Charles II key is not among them, of the microfilm
frames of Red Book ii nos. 156-159 to collate the figures.** Nothing further can be done from published sources.

## Collation of the two printed witnesses (`collate.py`)
A = 1766 *Account* (via Tomokiyo); C = Camden 1880 (Gardiner, from the MSS). Differences:
| place | A | C |
|---|---|---|
| 6 Aug "done" | 302 192 353 308 **100** 108 17 120 | ... 308 **106** 108 ... |
| 14 Aug bearer | 270 16 135 9 190 **10** | 270 16 135 9 190 (no 10) |
| 31 Aug "send to" | **122** | **22** (22 also occurs inside the run 190 **22** 58 135) |
| 27 Sep "by the" | 174 **261** 82 15 **347** 8 3 | 174 **26** 82 15 **30** 8 3 |
| 27 Sep "yourself" | 281 329 165 244 9 **42** 65 56 324 | ... 9 **4** 65 ... |
Camden's 2o8 = 258 (OCR). 102 groups, 67 distinct, range 3-384. Repeats: 9 (x4); 3, 10, 190, 308 (x3);
4, 6, 13, 15, 38, 40, 56, 58, 65, 70, 100, 108, 122, 135, 163, 174, 192, 237, 256, 281, 290, 329, 380, 384 (x2).
Structure guess (cf. Charles II's 1648 Swan cipher: letters 10-78 with 3 homophones each, words 79+; and the
Nicholas 1650 letter: letters <50, words 100-300s, names 300+): groups <=~90 are letters/nulls, >=100 words and
names. 3 and 10 sit at the ends of runs three times each -> probably nulls or a terminal letter. 132 = the
dateline (Dunfermline, where Charles was in early Aug 1650); 163, 122, 223 are persons (agents/bearers); 22 is
"the proper person" to send to. Runs with many small numbers (270 16 135 9 190 10; 20 174 36 9 40 13 15 38 61
195 289 4 5 384 380 10) are names or rare words spelt out. Shared pairs across letters: 237 70 (6 Aug, 27 Sep),
192 ... 308 100 (twice, 6 Aug), 308 290 (27 Sep), 58 135 256 58 256 (31 Aug).

## Historical frame for cribs (when the key comes)
Hamilton was confined to the Isle of Arran from the King's landing (June 1650) until Jan 1651 ("I hope your stay
where you are will not be long"). 6 Aug: the Kirk had just removed Charles from the army at Leith (c. 2 Aug) and
was pressing the Dunfermline Declaration (signed 16 Aug); the "two things" are probably the declaration and what
to do about the army/Cromwell. 31 Aug (3 days before Dunbar): Hamilton had offered to come to him or act;
"concerning ... which is the best and safest way ... who to imploy" = sending a message/agent to someone. 27 Sep:
"I have at last resolved that ... by the ..." is the decision that became **the Start** (4 Oct 1650, Charles's
flight from Perth to the Highland royalists); "preparing yourself ... to get you [out of Arran / a pass]".

## Status: OFFLINE-ONLY (2026-09-15)
Ciphertext collated from both witnesses; cryptanalysis impossible (102 groups, no redundancy); **key located in
the archive (NRS GD406/1/2197, open)** — solution depends on obtaining copies from Edinburgh. Nothing further
can be done online; parked. To resume: order digital copies of GD406/1/2197 (5 items) and, if needed, the
microfilm frames of Hamilton Red Book ii nos. 156-159 (GD406/1/10573-10576); then apply the key with a
10-line script over `collate.py`'s RUNS.
