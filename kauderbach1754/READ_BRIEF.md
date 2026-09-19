# Reading brief (Kauderbach 1754-58)

Key: `key.json` (2-digit code -> letter/syllable), solved 2026-09-19. System: one code per letter or syllable
(like the 1761 Kauderbach key DECODE R936, `key/DOC_R936_D2668_2668.txt`), digits 5 and 8 are nulls, capital
letters with ./. are names in clear (meaning differs from 1761; leave as [S./.] etc.).
Machine decryptions: `read/machine_R<rec>.txt` (clear passages in [brackets], {n} = dropped stray digit).
Tool: `PYTHONUTF8=1 python codes.py key.json '<regex on decoded text>' 20` shows the codes behind a decoded string.
Transcriptions: decode/DOC_R*.txt and trans/R*.txt; images img/ (crop small, <=1600 px, if you must look).

Task for each assigned letter: write `read/R<rec>.txt` containing
1. the cipher passages as clean, word-divided French (18th-c. spelling kept), clear passages summarised in one line
   each in [brackets]; mark doubtful words with [?] and unread stretches with [...];
2. a short "Notes" list: key corrections you are confident of, with the evidence (code, >=2 contexts), and
   transcription slips you suspect.
Known uncertain codes: 10, 20, 30, 40, 66, 90, 13 (also 're'?), 76, 23, 39. Do not change key.json yourself.
Report: per letter, share of the cipher you could read, and your proposed key corrections.
