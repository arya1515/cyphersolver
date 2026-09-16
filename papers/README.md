# Papers — getting the solved findings into a publishable format

Status 2026-09-15: drafts, unvalidated, not submitted. Everything below is for Daniel to review.

## Where the results already are

| Channel | State |
|---|---|
| S. Tomokiyo, *Unsolved Historical Ciphers* (cryptiana) | Richelieu, Armstrong postscript and the Sun Yat-sen telegram are marked **Solved** with the note "Daniel Bourdeau notified me of his solution on 15 September 2026" and a link to each write-up (checked 2026-09-15) |
| DECODE database (de-crypt.org), R9461/R9462 Richelieu | Still "Non-decrypted". Editing needs a registered account; registration is Daniel's step (organisation policy on account creation). Point them at Avenel 1858, t. III pp. 368–369, 381–383 and `docs/richelieu.html` |
| This repository and the GitHub Pages site | Full informal write-ups, code and data |

What is missing is a peer-reviewed record. The two venues in this field are HistoCrypt (annual conference,
proceedings in Linköping Electronic Conference Proceedings / NEALT) and *Cryptologia* (Taylor & Francis).

## Recommended venue: HistoCrypt 2027

10th International Conference on Historical Cryptology, Stockholm, 21–23 June 2027 (histocrypt.org).
The 2026 cycle opened submissions on 5 December 2025 with a deadline of 31 January 2026 (extended to 6 February);
expect the 2027 call in autumn 2026 with a deadline around **end of January 2027**.\*

Reasons: the proceedings regularly publish single-cipher decipherments (e.g. Lasry, *Armand de Bourbon's
Poly-Homophonic Cipher – 1649*; Pierrot et al., *Deciphering Charles Quint*, both HistoCrypt 2023), the short-paper
track takes negative results and surveys, and the format is fixed by a template, so the drafts can be made
submission-ready now. *Cryptologia* remains the right home for a longer version of the Armstrong paper (the
580-group code table, and the other coded Armstrong despatches) after the conference.

### Format requirements (verified against the official template, `histocrypt/template-instructions.pdf`, and histocrypt.org/cfp and /instructions on 2026-09-15)

- **Regular paper:** up to 10 pages of content, references excluded. Substantial, original, unpublished research.
- **Short paper:** up to 4 pages, references excluded. Smaller contributions, work in progress, negative results, surveys.
- **A4, two columns**, 11 pt Times Roman body, abstract 10 pt and at most 200 words, footnotes 9 pt, captions 11 pt
  below the figure/table in the form "Figure 1. …" / "Table 1. …".
- **LaTeX template** (`histocrypt.sty`, `histocrypt.bst`, copied here from histocrypt.org/assets/files/histocrypt.zip);
  a Word template exists too. Citations are author–year: `\cite{key}` gives "(Author, Year)", `\shortcite{key}` gives
  "(Year)" after the name in the text, `\newcite{key}` gives "Author (Year)".
- **Anonymous submission**, double-blind, at least two reviews. No author names or affiliations on the title page
  and no self-revealing references. Acknowledgements only in the camera-ready version.
- **PDF only**, uploaded through EasyChair (2026: easychair.org/conferences/?conf=histocrypt2026; the 2027 link will differ).
- Papers presenting content that has already been published are rejected.

### Format requirements for *Cryptologia* (not verified: tandfonline.com blocks scripted access; confirm on the journal's "Instructions for authors" page before submitting)

- Submission through ScholarOne Manuscripts; double-anonymised peer review.\*
- Taylor & Francis journals generally: unstructured abstract, five or six keywords, Chicago author–date references
  for this journal, figures as separate high-resolution files.\* No fixed word limit is published for Cryptologia
  as far as I could establish.\*
- Preprint policy: T&F allows author's original manuscript on a personal site or preprint server.\*

## The drafts

| File | Track | Subject | Draft length |
|---|---|---|---|
| `histocrypt/armstrong1808.tex` | regular | Reconstruction of the "972" code from the State Department's pencil decodes; the 30 Aug 1808 postscript read in full | ~5 pages |
| `histocrypt/telegrams1916.tex` | regular | Two intercepted telegrams of the 1916 anti-Yuan campaign: the Swatow telegram to Sun Yat-sen (brute-forced systematic condenser) and the Huang Xing telegram (three-kana private code, transmission error located) | ~5 pages |
| `histocrypt/already-solved.tex` | short | Six "unsolved" historical ciphers that were already solved: Richelieu 1629 (Avenel 1858), Hyde 1659–60 (the 1724 editor), Perwich 1670, Ferdinand III, the Confederate dictionary code, Milroy; how catalogues go stale and a checklist | ~4 pages |
| `histocrypt/refs.bib` | shared bibliography | | |

Compile any of them with (Overleaf works; no LaTeX is installed on this machine, so the drafts are **uncompiled**):

```bash
cd papers/histocrypt
pdflatex armstrong1808 && bibtex armstrong1808 && pdflatex armstrong1808 && pdflatex armstrong1808
# telegrams1916.tex contains Chinese and Japanese: compile it with xelatex instead of pdflatex
```

## Before submission (Daniel)

1. **Anonymity vs. the public site.** The reviewers can find dbourdeau.github.io by searching a quoted phrase. The
   ACL-derived rules HistoCrypt uses do not normally count a personal website as prior publication, but the drafts
   must not link to it, and the phrase-level overlap should be kept low. Safest: e-mail the programme chairs
   (2026 address: histocrypt2026@inria.fr) and ask whether web write-ups posted before submission are acceptable.
   Their answer decides whether the repository stays public during review.
2. **Armstrong notes reconciled (2026-09-15):** `armstrong/NOTES.md` now matches the site and the paper: 48 of 49 groups
   determined, the 49th a probable slip (555 for 1555 *man*); 1394 is *ru*, not a null.
3. **Fill the marked gaps.** Every `\todo{…}` in the drafts is a fact to supply or verify from the notes or the
   frames: exact frame numbers, the character-by-character Huang Xing alignment table, figure files.
4. **Figures.** Reuse `docs/armstrong_roll13_0200.jpg`, `docs/sunyatsen_telegram.png`, `docs/huangxing_annotated.png`
   (check the LoC, NARA and JACAR terms for reproduction in proceedings; JACAR requires a credit line).
5. **Author block.** Uncomment the real `\author{}` only in the camera-ready version.
6. **Register with DECODE** and ask that R9461/R9462 be marked deciphered, citing Avenel.

\* Asterisked statements are inferences or unverified; the cfp/instructions pages for 2027 were not yet published on
2026-09-15 and the Cryptologia page could not be fetched.

Checked: HistoCrypt 2026 cfp and instructions pages, the official template zip and its PDF, Tomokiyo's list page,
the LiU E-Press HistoCrypt 2023 volume listing. Not checked: Cryptologia's author instructions, HistoCrypt 2027
dates beyond the conference itself, whether the drafts compile. User must verify all of it before acting.
