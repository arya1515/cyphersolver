# Milroy cipher telegrams (Cox 3 Dec 1862, Bascom 4 Dec 1861) — found already solved

cryptiana's unsolved list (fetched 2026-09-14) marks this item **Solved**: Richard Bean, with Claude Opus 5, 2026
(https://cryptiana.web.fc2.com/code/civilwar1b_milroy.htm). Stager Cipher No. 7: 6 fixed columns; indicator word
gives the number of lines ("China" = 8, "Turkey" = 12, "Austria" = 9); words entered column-wise in a set sequence,
up or down; plaintext read row-wise. Cox: "If your information as to Imboden is confirmed, let me know by what route
you shall try to reach him, also how far forward in the Moorefield Road…". Bascom: "General Kelley having received
directions from General Halleck to hold himself in readiness to move under orders from army head quarters…".

Spot check here (`route.py`, transcription from the Jasper County Library lesson plan, i.e. Milroy's own copy):
the run "imboden by to forward" is column 6 rows 1–4 read downward, and "what is if" is column 1 rows 3–1 read
upward, consistent with Bean's grid. A blind bigram search over all 6-column routes did not converge because the
lesson-plan transcription is unreliable and the grid contains nulls and code words; not pursued further.
