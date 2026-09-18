# fr. 15572 f. 19r — the decipherment, in clear (transcription in progress)

Canvas 21 right of ark `btv1b9061879d`. The office's clear-text reading of the cipher on f. 18.
Ordinary French secretary hand, 33 lines. Read with `mtile.py` at three tiles a line.

Lines 1–8, with `…` where a word is not yet settled:

1. Que sa Ma[jes]té fust advertie … plustost que nous eussions victoire e[t]
2. **Conseil d[e] [a]ssembl[er/ée] de Castillebourg où l'on feist … que je n'avois plus d'instruction**
3. … à nulle cause, il nous … **Mais** considérant que ces so[nt] …   *(not "Ma[jes]té": at six tiles the word is plainly **Mais**, which also reads better — the landmark discrepancy on this line is what prompted the re-reading)*
4. **changera tant par ce que les habitans de la ville qui s'estoient fort estonnez**   *(firm at six tiles; "par ce que" = parce que)*
5. … ou reprim[ent] … pas ce retour de m[onsieu]r le gouverneur de Coul… aut…
6. … noz lieux forces. Que les froidz sont devenuz tres grandz, que pour
7. … tenir les soldatz dans les tranchées sans grande …
8. … [ex]pedie. Qui veulent considérer nostre armée pour plus d'ung effect quel…

Enough is legible to confirm the subject: a winter siege in Guyenne, the cold in the trenches,
the townsmen's morale, the governor's return, and the army's strength — and it is the plaintext of
f. 18's ~1,650 figures.

**Why the transcription is worth finishing.** It is not itself a decipherment (the Court read this
in 1586 and wrote it out here). Its value is that it is the *key*: aligned against f. 18's figures
it labels every homophone with an image, and that labelled set is what the eight undeciphered
leaves need. It is also, incidentally, a Mayenne despatch that has not been transcribed in modern
times.

## State

`hi/f19rflat.png` flattened, `f19r_lines.txt` fitted (33 lines, pitch ~127), all 99 tiles cut at
`hi/P_*`. f. 18r's cipher is set up the same way (`hi/f18rflat.png`, `f18r_lines.txt`, 22 lines)
and segments to ~29 figures a line, 624 in all, which against f. 19's letter count gives the
~0.9 figures per letter a homophonic cipher with code groups should give.


## Line 2 settled at six tiles

Line 2 now reads through: **"Conseil d[e] [a]ssembl[er] de Castillebourg où l'on feist … que je
n'avois plus d'instruction"**. The head word is *Conseil* — a C with its loop, then *onseil* with
the tall l — and the second word is an s-s form, *assembler* or *assemblée*; the place is written
*Castil* + *lebourg*.

With that, f. 18r line 3 — 24 boxes, segmented and rendered at `hi/l3box_*.png` and stored in
`f18r_l3_boxes.json` — has its plaintext and is ready to label. That is the next unit of work, and
it is the same unit repeated: read a plaintext line, lay it across the cipher line's boxes, save
each box as a labelled image.


## Further lines, read at three tiles

12. … bonnes villes … plus importantes que quelque[s] veulen[t] … au M[onsieur] …
13. **Matignon** comme proteste … quel[le] faveur contrari[er] et m[es] … avantures ung …

Line 13 names **Matignon** in the clear — the marshal commanding in Guyenne, and the second party
in this whole catalogue entry. The despatch is therefore not only about the siege but about
Matignon's own position, which is what the ciphered passages of ff. 196/201 also circle around
("Monsieur du Mayne vous a faict une autre despesche…").

A name in the plaintext is worth more than an ordinary word for the mining: proper nouns are spelled
out letter by letter rather than hidden in a code group, so *Matignon* is nine consecutive figures
whose letters are certain — and it carries a **g**, which the exemplar set has only once.


## A fourth correction, and one discrepancy left open

Line 3 re-read at six tiles: the word I had as *Ma[jes]té* is **Mais**. Four corrections now, all
found by going back over the plaintext rather than the cipher — *et* for the phantom "Heut Jo.", a
dropped thirteen-letter phrase, this, and the still-open one below.

**Open:** f. 18r line 6 ends with code `35` (*parce que*), which the figure arithmetic puts inside
this line — and *parce que* is not in it at six tiles either. Two possibilities and no way to choose
yet: the ±4 drift has accumulated far enough by line 6 to put the landmark in the wrong plaintext
line, or Tomokiyo's value for 35 is wrong. The second would be worth knowing; it is the kind of
thing a crib this size exists to settle, and it will settle itself once the plaintext either side is
firm.


## Line 4 firm, and the *parce que* found

At six tiles line 4 reads **"changera tant par ce que les habitans de la ville qui s'estoient fort
estonnez"**. The words I had skated over as *"tant par … l[es] … que"* are **par ce que** — *parce
que* written in three words, which is how the secretary writes it.

That closes the discrepancy left open above. f. 18r line 6 ends with code `35`, Tomokiyo's *parce
que*; the arithmetic had put it in f. 19r line 3, which has no *parce que*; it is in line 4. So:

* **Tomokiyo's 35 = *parce que* is confirmed** against a plaintext — the fourth nomenclature value
  checked this way, after 14, 25 and 52;
* the figure arithmetic was **one line out**, not wrong: accumulated drift of the kind already
  measured (±4 units per 125) is enough to cross a line boundary by the sixth line.

And the line carries what the mining needs: **h** twice (*changera*, *habitans*).
