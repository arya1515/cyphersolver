# Brief: transcribing the Sormano/de Vaulx letters (BnF fr. 3096)

## Task
Transcribe the cipher passages of your assigned letter at glyph level, decode
with Lasry's key, and produce a continuous reading. The letters are in Italian
(1529, Ferrara), partly in clear, partly in cipher; cipher and clear alternate
mid-sentence.

## Images
Fetch crops from Gallica IIIF (needs browser UA):
curl -s -A "Mozilla/5.0" "https://gallica.bnf.fr/iiif/ark:/12148/btv1b9060015d/f{VIEW}/{X},{Y},{W},{H}/{SCALE}/0/native.jpg" -o out.jpg
Full page is ~8660x5876 (two-page spread; left page x≈900-4400, right page x≈4400-8300).
Work in bands ~1800px wide x ~330px tall (one line), fetched at /full/ or 2x
(e.g. /3600,/ for a 1800-wide crop). Overlap crops 100px to avoid losing glyphs.
Wait 1-2 s between fetches (Gallica throttles; on 429/error back off 30 s).

## Key (Lasry 2023) — cipher glyph -> plaintext
See key_lasry3.png (and kA.png..kD.png 3x crops) in this directory. Summary:
- a: open "v"; round "υ"; square-top "п" (no overhanging bar); "3"
- b: small "τ" (plain tau, light)
- c: triangle "Δ" (point up)
- cc: double-crossed slash "≠"
- d: "e"-shape with tail curling left/down ("ꜿ")
- e: "n" with inward final tail ("ϰ"); "k"; "Γ" with tick; "7" with foot
- f: "ff/ſſ" double-loop ligature
- g: "S"
- h: seriffed capital "E"
- i: forked "Y"; circle with centre dot "⊙"; "p"; "4"
- l: ring with straight descender "ϙ/9"
- ll: lozenge/square with centre dot "⊡"
- m: "B" with lead-in stroke (looks like "93" or "ꞵ")
- n: "π" (top bar overhangs both legs)
- o: "Ц" (u with descender on right); "1"; "δ" with small ring at foot
- p: "6"
- q: triangle point-DOWN "▽"
- r: "Q"-like ring with tail to lower right
- s: double-crossed "z" ("ƶ"); open square left with centre dot "⊐·"
- t: plain light "x"
- v/u: heavy-top-bar "T"; "α"; "γ" with tick; "H"
- x: bold saltire "✗"
Distinguish: п(a) vs π(n) by overhanging bar; τ(b) vs T(v) by size/serif;
x(t) vs ✗(x) by weight; ⊙(i) vs ⊡(ll) vs ⊐(s) by shape; Q(r) tail direction.
There is no z/k/w in the key; z is written with the s signs or in clear.

## Method
1. Fetch the assigned pages band by band. Transcribe EVERY cipher glyph in
   order using the ASCII aliases of decode.py in this directory
   (v u w 3=a, b=b, c=c, d=d, e k g 7=e, f=f, S=g, h=h, y o p 4=i, 9=l, L=ll,
   m=m, n=n, U 1 5=o, 6=p, q=q, r=r, z s=s, t=t, T a Y H=v, X=x).
   Interleave clear text in [brackets].
2. Decode with: python decode.py "..." (or pipe). Read the result as Italian
   (16th-c. Northern forms: et, ch', havemo, anchora, epso, Mta = Maestà,
   Excel.a = Excellentia, sr = signor; names: duca (Alfonso d'Este), Ferrara,
   Sormano, Joachin, Monsr d'Isarnai/de Sarnay = M. de Sarnay?, Triulzo
   (marshal Teodoro Trivulzio), don Hercole (Ercole d'Este), Madama Rainea
   (Renée de France), capitaneo Leonardo, Barletta, Puglia, Abruzzo, l'Aquila,
   Lautrech, Urbino, papa, imperatore, venetiani, Napoli).
3. Where a glyph is ambiguous, try both readings and keep the one that yields
   Italian; mark residual uncertainty with (?) in the reading.
4. Deliverables — write TWO files in this directory:
   - nNN_transcription.md: per line, the ASCII glyph string + decoded text.
   - nNN_reading.md: continuous mixed clear+deciphered text, cipher parts in
     *italics*, then a 10-line English summary.
Do not fabricate: if a band is illegible, say so and move on. Accuracy over
completeness; but aim to cover every cipher line of your letter.

No n63/n65/n66 deliverables have yet been completed; this directory currently
contains the key and transcription protocol only.
