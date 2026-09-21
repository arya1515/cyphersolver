# Charles V to the Empress Isabella (1536) and to Prince Philip (1543), AGS Estado (DECODE R9957, R9952) — NOTES

Status: no write-up

**Verdict: both letters were already read. R9952 was deciphered at the time. R9957 was deciphered and printed by
Wanruo Luo (2021) from its original key.** Catalogue entry 199 ("Charles V (Burgos) to Isabella of Portugal /
Prince Philip, 2 ciphertexts") is resolved and removed. Checked in one session on 2026-09-21.

## The two records are two unrelated letters

| record | shelfmark | what it is | DECODE status |
|---|---|---|---|
| R9957 | AGS Estado leg. 496, ff. 270–274 (18 images) | Charles V to the Empress Isabella; clear text with long cipher passages. Dated at the end "Del Burgo de Sādonyn a xvii de Mayo de MDxxxvi", signed "Yo el Rey". | Non-decrypted |
| R9952 | AGS Estado leg. 59, ff. 10–14 (20 images) | Charles V to Prince Philip, Cremona, 19 June 1543 (docket f. 10: "Cremona ... al Príncipe ... del Emp.or a xix de Junio 1543") | Partially decrypted |

- **Place and date of R9957.** "Burgo de Sādonyn" is **Borgo San Donnino** (now Fidenza, near Parma), on the
  Emperor's road north from Rome in May 1536. It is not Burgos. The date line reads xvii (17) May. DECODE gives
  8 May, and Tomokiyo gives 18 May. The catalogue's "Burgos, Spain" comes from DECODE's origin field.
- **R9952 was never an Isabella letter.** Its DECODE note ("Correspondence between the emperor and the empress
  … 1531 and 1532") was copied across the leg. 496 batch.
- **Image order.** R9957's DECODE images are out of archive order. The stamps give P4 = 0005, P5 = 0007,
  P6 = 0006, P7 = 0008, P8 = 0011 and P11 = 0004; scan 0010 is P10. The cipher runs on in stamp order.

## Prior solution (the contamination question)

- **R9957.** Tomokiyo, cryptiana "Spanish ciphers during the reign of Charles V", update section on Luo (2021)
  (copy in `vasto1527/prior/spanish2C_now.htm`): "Charles V to Isabelle de Portugal, Burgos, 18 May 1536,
  AGS,EST,LEG,496,270-274. DECODE R9957. Deciphered and printed in Luo (2021) p.287. The cipher used is AGS,
  Est. Leg. 1.1.1 doc. 169."
  - Source: Wanruo Luo, *El lenguaje cifrado de Isabel de Portugal (1530-1539)*, doctoral thesis, Universitat de
    València 2021 (dir. Júlia Benavent), RODERIC.
  - The key (AGS Estado leg. 1.1.1 doc. 169) was used between Isabella and Charles V in 1535–38. It combines a
    homophonic alphabet, double letters and syllables (base sign plus vowel stroke, or the numbers 32–91), code
    figures 92–211 and graphic signs. Dotted signs and numbers from 212 up are nulls.
  - Found here after a partial transcription and a failed alignment attempt (below). The existing reading was not
    used to solve anything here.
- **R9957 was also partly deciphered at the time, inside the letter.**
  - p. 16 (scan 0016) has two interlinear glosses: "quatrocientas o q[uinient]as lanças d'armas" and "los arneses
    y las cubiertas".
  - The lower half of p. 17 and the top of p. 18 hold a decipherment, in a rapid second hand, of the long cipher
    passages on pp. 16–17. It covers the German troops (25–30,000 men for Italy, more to be raised in Germany and
    Flanders), the Count of Nassau and "nuestro mayordomo" entering France from the Luxembourg side, and the
    diversion of the French King's forces. The clear phrases "que ninguna cosa puede ser mas provechosa que" and
    "juntamente con lo q", left in clear inside the cipher, recur in it.
  - The cipher on pp. 1–14 has no decipherment on the leaves.
- **R9952.** It is deciphered in the margins of ff. 10–12 and fully on ff. 13–14, "del Emperador a Su Al[teza]".
  Its subject is the Farnese offer through the Marqués del Vasto: two million ducats and a yearly census for the
  investiture of Milan for the Duke of Camerino (Ottavio Farnese). Tomokiyo, same page: "Deciphered in the margin.
  The cipher matches Charles V-Prince Philip Cipher (1545)", with additional code words.

## What was tried here before the prior reading was found

1. DECODE metadata and all 38 images fetched with the saved cookie (`img/`, git-ignored; not public domain).
2. Two transcription subagents (`trans_p1-9.txt`, `trans_p10-18.txt`). These are first passes: glyph naming was not
   unified between them, two "4" shapes were merged, and on pp. 3–9 and 13–14 they read from reduced views.
3. Crib alignment: the p. 16–17 cipher against the p. 17–18 decipherment and the two p. 16 glosses, with the hard-EM
   aligner from `balbases1677/align2.py` (`align.py`, `tx/`).
   - It did not converge: the sign tables came out random.
   - The ratio of about 1.5 plaintext letters per transcribed token fits the doc. 169 syllable system.
   - The token boundaries in the transcription did not match the system's signs (base sign plus vowel stroke;
     numbers 32–91 as syllables).
4. Literature check (`vasto1527/prior/spanish2C_now.htm`) found the Luo reading and the key's shelfmark.

## If anyone reopens it

Luo's key (AGS Estado leg. 1.1.1 doc. 169, her p. 603) and her edition (p. 287) are the starting point. The
transcriptions here are not good enough to check her reading sign by sign.
