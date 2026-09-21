# Alonso Sánchez (Venice) to Charles V, May–August 1523 — RAH Salazar 9/28 (A-28)

Status: done — found already calendared (Bergenroth 1866) with contemporary decipherings; the key is the 1522
key; the uncalendared August letter is read in part.

Catalogue entry 147 ("Alonso Sánchez (Venice) to unknown recipient, 10 ciphertexts", DECODE R9670–R9770).
Worked 2026-09-21. The recipient is not unknown: every letter is addressed "Sacra cesarea y catholica
magestad", i.e. Charles V. Sibling target: `../sanchez1522/` (the 1522 despatches, same cipher).

## What the records are

Metadata from `decode/metadata.tsv` (DECODE record pages, no login). All ten are flagged
`Inline Cleartext: Yes`, but that flag means passages written *in the clear* inside the letter. None of the
DECODE images carries an interlinear or facing decipherment. The contemporary decipherings Bergenroth cites
are filed separately in the volume and were not imaged with these records.

| DECODE | DECODE ff. | stamped ff. | date (from the letter) | what | CSP Spain 2 |
|---|---|---|---|---|---|
| R9670 | 18–24 | 35–38 | 8 May 1523 | Doge Grimani's death "de noventa años", Cornaro's illness; mixed clear/cipher | duplicate of no. 549 |
| R9671 | 40–43 | 40–42 | 8 May 1523 | same letter | **no. 549** (A-28 ff. 40–44) |
| R9672 | 78–79 | 78– | c. 20–23 May 1523 | "A xviij y xxiij del presente el duplicado por via de Genova escrevi"; the election of the new Doge (Gritti); facing leaf "A. Claro" | cf. no. 552 |
| R9674 | 81–82 | 81–82 | 20 May 1523 ("a xx de mayo"), "es treslado de otro" | duplicate | duplicate of no. 552 (ff. 83–85) |
| R9677 | 148–152 | 148–150 | early June 1523 ("Despues de los xx del passado no he escrito") | the Infante's powers | probably no. 554 (5 June, f. 157) |
| R9689 | 224–226 | | 13 June 1523 | | **no. 558** (ff. 224–228) |
| R9690 | 226–228 | | 13 June 1523 | | no. 558 |
| R9767 | 563–564 | 563–564 | **16 Aug 1523**, Sánchez alone | mostly clear; ~18 cipher lines on f. 563r | **not calendared** |
| R9769 | 569–571 | 569– | 16 Aug 1523, Caracciolo and Sánchez | clear: the league concluded, Pace left for Ferrara and Milan, the Infante's envoy, prisoners freed | not calendared |
| R9770 | 572–574 | 572–574 | 16 Aug 1523, Caracciolo and Sánchez, "es treslado de otro" | duplicate of R9769; short cipher at the head of the last written page; clear note f. 574 on the "mutua restitucion" instrument | not calendared |

Bergenroth's abstracts for nos. 549, 552, 554, 558 are in `csp/bergenroth_abstracts.txt`. Each says "Autograph
in cipher. Contemporary deciphering." So the content of the May–June despatches has been in print in English
since 1866, from the decipherings made at court. Nos. 566/577/587 (the joint letters of 16 July, 29 July and
18 Aug) are other letters, not these.

## The key

Unchanged from 1522. The code groups on every page examined (R9670, R9671, R9672, R9677, R9767) read
coherently with `../sanchez1522/key_codes.tsv` (Tomokiyo 2025 plus this project's additions): `xig`=de, `vog`=en,
`dom pud`=vuestra magestad, `ho`=que, `nuf`=no, `lal`=publica, `tum`=frances, `gub rac`=señor infante. It is
the same hand, the same three opening nulls and the same run of latin-looking cursive signs. Nothing new
was needed to read these letters, and nothing here contradicts the 1522 key.

## What was read here

`read_r9767.md`: the one letter not in Bergenroth, Sánchez's own despatch of 16 August 1523. The clear text is
transcribed in full. In the two cipher passages every code group is resolved except `pem` and `yol`, but the
spelled runs are only partly read. Gist: he refers the Emperor to the joint letter and answers the imperial
letter of 15 July; something in Venice leans French but "poco podra danyar"; the capitulation says nothing
about the Venetian money payment. The clear postscript says they did not bind the Infante to the defensive
league because the Venetians would not bind themselves against the Turk, and that shipping rights for the
Archduke's subjects could not be obtained.

R9769/R9770 (joint letter of the same day) are nearly all in the clear and were read at sight for the table
above; not edited.

## Why not more

A full edition of the cipher passages is transcription work at about a page per session (see the sanchez1522
notes). For eight of the ten records it would reproduce content already calendared from the contemporary
decipherings. The two records with new content are short and mostly clear. Closed as **found in print, read
in part**.

## Files

- `decode/` — `getrec.py`, `meta.py`, `fetch.py` (copied from sanchez1522; the cookie and rec*.htm are git-ignored), `metadata.tsv`.
- `csp/bergenroth_abstracts.txt` — the four CSP entries.
- `read_r9767.md` — the reading.
- Images (`img/`) are git-ignored; fetch with `python decode/fetch.py 9670 9671 …` and a DECODE cookie.
