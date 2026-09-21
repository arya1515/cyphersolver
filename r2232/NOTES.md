# R2232: Wolff to Princess Wilhelmina of Prussia, The Hague, 25 July 1801

Status: read (21 Sept 2026)

- **Record.** DECODE R2232, KHA The Hague, Wilhelmina Prinses van Pruisen (A32), inv. 192. Catalogue 222 (class A,
  rule-scored). DECODE: "Non-decrypted", 3 pp., homophonic, numerical, French. Pencil on the leaf: "A32 399".
  The three DECODE images are out of order: the letter runs P2 (opening "Madame!"), P3, P1 (closing, date, signature).
- **Key.** DECODE R2233, the same inventory number: Wolff's covering letter of 8 September 1801 ("La Haye ce VIII
  Septembre"), which sends "la clef ci-jointe" because his letter of 25 July had crossed a courier. The key is
  45 numbered rows, each with four consecutive values of one running sequence:
  `0 1/8 1/4 1/2 1 2 … 8 9 à a b c … n ô o p q r s t û u v w x y z a e i o u a`
  (row 15 = a b c d, row 44 = e i o u). A group is a row number with a superscript 1–4 (bare = 1) choosing the
  value in that row, so each letter has up to four homophones (a = 15, 14², 13³, 12⁴ …). DECODE's own note on R2233
  describes it exactly ("consecutive numbers not exceeding 45, each added with index numbers from 1 to 4"). Decoder:
  `decrypt.py` (value = S[N+k−2]).
- **Transcription.** Claude, from the DECODE scans (IMG_R2232_I15506–15508, rotated, cut into bands), `ct.txt`:
  1,065 cipher groups, 119 distinct, in words separated by the writer's commas and spaces. Clear-text passages
  (the openings, "Votre Altesse Royale", the formulas) are in the letter itself and kept in capitals in `ct.txt`.
- **How found.** The key record was the next DECODE number; the first test ("15, 15² 17³ 31³ 24³ 20⁴ 27²" =
  "à Berlin", signature 38² 45² 25³ 19² 18³ = W O [L] F F) worked, and the rest decoded on the first pass.
- **Slips.** A few groups decode one place off (superscript misread or miswritten): the signature's 25³ gives m for
  l, "bienfaisante" comes out "bie?gck" (27³ 19³ 15³ 22⁴ for n f a i), "subsistance" comes out "subsiston…", and
  "voué" is "vov". Readings are corrected in `reading.txt`; `decrypt_raw.txt` is the mechanical output.

## Reading

See `reading.txt`. A royalist named Wolff at The Hague writes to the exiled Princess of Orange in London, in cipher
"because of the importance of the matter". He is, he says, the author of a plan sent to her and to the King of
Prussia at Berlin in March or April 1798, when he was in the Hanseatic towns: a gathering of forces for a landing at
Le Havre and a bombardment of Paris, another landing in Holland, a corps attacking the IJssel while the rest operates
on the continent, the pacification of the country, a new way of commanding combined armies, "finishing with the wish
to be able to do as Coriolanus". Since the plan was made after the peace of Campo Formio and circumstances are alike
again (1801, the Lunéville peace), he offers his services to carry it out. He had offered the late Prince Frederick
(d. 1799) to bring several thousand men of the Swiss brigade with the best officers, by a letter sent the morning
of 14 September 1795, the day he was arrested; otherwise he would have entered British pay, and would not have
spent 39 months and 5 days in prison. He asks her to obtain for him the British government's half-pay from the day
of his arrest (he had 50 florins a month as quartermaster), or another relief, recalling her intercession for him
at Berlin in 1791. Her orders can reach him by the same channel "sans adresse, avec 3 marques ▽".

Unread or doubtful: two short passages in clear text were not transcribed word for word (marked "…" in `ct.txt`),
a few words after "proportionné" and "si j'ai le [c…]", and the end of the final group ("# 19 28", "en"). Wolff is
not identified further; the 1795 arrest and 39-month imprisonment would date his release to about December 1798.

## Prior work

DECODE status "Non-decrypted"; the key record R2233 is filed next to it with a correct description of the system,
but no reading was given on either record. No printed decipherment found. Key from the archive; read on the first
attempt.
