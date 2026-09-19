# Calibration brief: align Pelissier's cipher letters (nos. 45/46) with their clear-text decipherment

Working dir: C:\Users\dbour\cypher\pelissier1592 (use Git Bash + python; PIL available).
Images (full-res, ~4965x6800): img/c230.jpg = f.111r (cipher, no. 45, Madrid 27 Oct 1592, with interlinear glosses),
img/c234.jpg = f.113r (cipher, no. 46), img/c235.jpg = f.113v (cipher block at top, then clear text + signature),
img/c238.jpg = f.115r and img/c239.jpg = f.115v (the CLEAR-TEXT decipherment of these letters, dated 27 octobre 1592).
Crop helper: `python crop.py img/cNNN.jpg X0 Y0 X1 Y1 out.jpg 1900` (Read the jpg to view). Crop ~600-900 px of original
width per view so single signs are legible. Scratch crops go in cal/crops/.

Key: Tomokiyo's reconstruction `league2_key.png` (zoomed: crops/k0.png..k3.png). Token vocabulary: TOKENS.md, and NOTES.md
section "What the key really looks like". The letter being solved (no. 22, ff. 46-50) uses the same key; its transcription
merged look-alike glyphs. YOUR JOB is to use the known plaintext to establish, for EVERY sign shape, which letter it is,
and in particular to split these look-alike families:
- 56 (plain) vs flourished s6 (c vs y?)
- δ family: plain δ with straight ascender (o?), δ with long curling hook (c?), closed-loop ∂ with curled top (r? = Q), ∂ in e column (D)
- T family: flat ⊤ (a?), hooked τ / ፐ (p?), small "Tz" (g?)
- I family: plain Ɨ (l?), bold-footed ⊥ (o?), double-barred Ƒ (o?), Π/⫴ (l?)
- vv (et vs f/ff), ϙ/ϱ (a vs f), 9 (f), 8 (n vs q), 4 (n vs t), 4 with base/ǂ (m vs o), 3 (b or null), small plain r (f?),
  ℋ vs ℋ-with-lead-in (q vs h), oo/∞ (m), ʃ-types (a / u / n), x vs ✗ (a / u / null), the nulls.
Report any sign that the key table lacks (e.g. b, x, z, k, j signs, doubled-letter signs, code numbers like 315/310).

Method:
1. Transcribe the relevant part of f.115 (clear text) into cal/clear_<yourpart>.txt, line by line. Find where your cipher
   letter's text starts/ends in it (the cipher letters also contain clear passages, which anchor the alignment; f.111 also
   has interlinear glosses above the cipher).
2. Transcribe the cipher sign by sign, using TOKENS.md tokens but SPLITTING the families above with new tokens where the
   shapes differ (invent clear names, e.g. `dc` hooked-δ, `Tp` hooked T, `Tz`, `Ib` bold-footed I, `s6` flourished 56, `r0` small
   plain r, `Hh` H with lead-in). Put under each cipher run the aligned plaintext letters. Format in cal/align_<part>.txt:
       R<n>: tok tok tok ...
       P<n>: l   e   t   ...      (one plaintext letter/digraph per token; `_` for a null; `?` if unsure)
   Keep the alignment honest: when the decipherment (f.115) paraphrases or skips, mark it and don't force it.
3. Tabulate token -> letter counts (python) into cal/table_<part>.txt, and list every token whose letter disagrees with
   Tomokiyo's key or TOKENS.md, with row refs.
4. Save exemplar crops: for each (token,letter) pair, cut 2-3 small crops of individual signs (e.g. 120x160 px original) into
   cal/atlas/<letter>_<token>_<n>.png. Record the crop coordinates in cal/atlas/index_<part>.txt. These will be used by the
   people re-reading no. 22, so pick clean, typical examples, especially of the look-alike families.
Report back: the size of what you aligned (signs), the full token->letter table, the disagreements with the key/TOKENS.md
with evidence, and the list of families you could split and how to tell them apart visually (describe the distinguishing
stroke precisely).
