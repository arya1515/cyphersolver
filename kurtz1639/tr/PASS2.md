# Second transcription pass (checked), kurtz1639

Goal: correct misread cipher tokens in the first-pass files tr/IMG_*.txt by checking every line against the image.
Images: C:/Users/dbour/cypher/kurtz1639/img/<same stem>.jpg (large; crop with PIL to about 6-8 lines at full resolution,
e.g. save crops to your scratch dir and Read them; for two-page spreads the left page is the left half).

Tool: `cd C:/Users/dbour/cypher/.worktrees/kurtz2/kurtz1639 && PYTHONPATH=.. PYTHONUTF8=1 python check.py tr/<file>.txt`
prints each line's decipherment (German, some Latin/Italian/French, 17th-c. spelling, no word breaks) and token:value
pairs. The key is fixed and correct (KEY.md). Garbled stretches in otherwise fluent German point to misread tokens.

Rules
- Edit the tr/ file in place. Change a token ONLY when the image shows it differently. Never change a token just to make
  the German read better; a correction must be visible. If the image is genuinely ambiguous, keep the reading that makes
  sense and add nothing else.
- Known first-pass confusions: 1/7, 6/0/c, 9/ψ/φ, 93 vs `9 3`, 3/5, 4/9, dropped or doubled tokens, skipped or repeated
  lines, line order on spreads. Check every line, not only garbled ones.
- Keep CONVENTION.md / LEGEND.md syntax. Keep line breaks as they are unless a line was missing or merged.
- Append one line per file to tr/PASS2_LOG.md: `<stem>: N tokens changed, M lines added/removed; residual garble: <where>`.
Accuracy of numbers matters most. Clear-text braces need no work.
