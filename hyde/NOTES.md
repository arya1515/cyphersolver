# Hyde's "undeciphered superscriptions" (Brussels, 1659-1660)

Target: Tomokiyo, *Unsolved Historical Ciphers* -> "Undeciphered Superscription by Hyde (1659-1660)"
(https://cryptiana.web.fc2.com/code/unsolved.htm ; context https://cryptiana.web.fc2.com/code/charlesii.htm).

## Verdict: SOLVED (explained) — the superscriptions are deliberate nulls, not an address

The contemporary editor of the English *Life of Dr. John Barwick* (1724), who worked from the Barwick
family papers, states explicitly (p. 409, footnote to Hyde's letter No. VI of 12 June 1659 that enclosed the cipher):

> "So several of the Letters were superscribed with Numbers signifying nothing, some with two or three
> Lines of them, only to puzzle the Enemy, if they should fall into their Hands, which I the rather mention
> here, because some Persons, for want of examining those Superscriptions, as printed in the Appendix to the
> Latin Life (p. 358, 360, 389, 396, and 417.) with the Cypher also published there, have wondered what was
> the meaning of them: and it was for the same Reason, that several of the Chancellor's Letters, besides the
> Number denoting his Name, were subscribed with other Numbers, that either had nothing in the Cypher to
> answer them, or nothing to the Purpose. As to the Superscriptions, B. or any Name beginning with B. seems
> to have signified Barwick."

The pages he cites (358, 360, 389, 396) are exactly the four ciphered superscriptions in Tomokiyo's list.
Our own test with the full Hyde–Barwick key (THE=370, 1–692, plate facing p. 316 of the Latin edition)
confirms his description: the one superscription whose numbers all fall inside the key decodes to
gibberish, and the other three contain numbers (705, 729, 831, 856, 858, 859) that do not exist in the key.
(His "p. 417" is the letter of 8 March 1660, No. XXIX, about Wallis's decipherments; no cipher superscription
is printed on that page in the archive.org copy, so that reference is probably to its numeric subscription or a slip.)

## Sources (all archive.org)

| Item | archive.org id | Use |
|---|---|---|
| Peter Barwick, *Vita Johannis Barwick* (London 1721), Latin, English appendix of letters + engraved key plate "Tabula Cryptographica" facing p. 316 | `bim_eighteenth-century_vita-johannis-barwick-s_barwick-peter_1721` | image leaves n386/n387 = key plate (files leaf386.jpg, leaf387.jpg, c386_all.jpg, c387_all.jpg); n429 = p.358, n431 = p.360, n460 = p.389, n467 = p.396, n486 = p.415, n488 = p.417 (leaf*.jpg). OCR: vita1721.txt |
| *Life of Dr. John Barwick* (London 1724), unabridged English tr. by Hilkiah Bedford | `lifeofjohnbarwic00barw` | editor's note on the cipher and the superscriptions, pp. 408-409; OCR: life1724.txt |

Image leaf N ≈ Latin page N−71. Scans are IA `page/n<N>_w2000.jpg` (getleaf.py); crops with crop.py.

The letters are **Hyde (Lord Chancellor) → John Barwick**, London. They were carried under cover to
intermediaries (e.g. "inclos'd ... to Mr. Thornton", 17 Oct 1659). Not Clarendon State Papers vol. 3 as
initially assumed: Tomokiyo's page numbers refer to the Latin *Vita* (1721).

## Exact ciphertext (verified against the page scans)

| Date (Brussels) | Latin *Vita* | English *Life* | Superscription as printed |
|---|---|---|---|
| 29 Sept 1659 | No. XVI, p. 358 | No. XIII, p. 449 | `212. 23. 12. 7. 461. 36.` / `108. 49. 498. 14. 21. 410.` |
| 17 Oct 1659 | No. XVII, p. 360 | No. XIV, p. 451 | `729. 549. 705. 99. 856.` / `250. 245. 831. 100. 859.` / `609. 858. 101. 24.` |
| 14 Jan 1660 | No. XXIII, p. 389 | No. XXI, p. 482 | `729. 549. 856.` / `21. 245. 831. 99.` |
| 16 Jan 1660 | No. XXVI, p. 396 | No. XXIII, p. 486 | `729. 549. 856. 8. 245. 831.` |

Group boundaries are unambiguous (every group is followed by a full stop in the print). OCR variants
("170" for 410, "5" after 856, "65" for 831) are OCR errors; the scans read as above and agree with Tomokiyo.

Clear superscriptions printed in the same appendix (all Hyde → Barwick under cover names):
"For Mr. Burden" (4 June 1659), "For Mr. Brookes" (12 June 1659, p. 313), "For Mr. B." (25 July 1659,
p. 335), "For Mr. Burges, these" (p. 339), "For the Lord General Monk" (p. 441), "For General Monk" (p. 442).

## Key examined: Hyde–Barwick cipher (THE=370), from the 1721 plate

Transcribed in barwick_key.py (643 entries). Structure (confirmed by the 1724 editor, p. 408): numbers
1–692 in eleven columns; col. 1 = letters 1–63 (a=1-3, b=4-6, ... k=28-29, ... w=60-61, y=62-63; x, z none);
64–69 skipped; cols 2–11 = 70–131, 132–193, 194–254, 255–317, 318–379, 380–440, 441–503, 504–566, 567–628,
629–692, each column running A..Y down the rows (three rows per letter, two for k/w/y), so syllables and
words are grouped by initial letter rather than being one alphabetical list. Several slots are empty
("stand for nothing"). Relevant entries: for=210, from=211, Mr.=536, Master=475, Barwick=572,
Hyde Lord Chancellor=589, the=370, this=371, that=372, these=none, Sir=none, London=none, Dr=205.

Result of applying it (python barwick_key.py):

* 29 Sept 1659: 212=gh 23=h 12=d 7=c 461=gentle 36=n 108=ob 49=r 498=ven 14=e 21=g 410=little → nonsense.
* 17 Oct 1659: 729 ✗ 549 (empty slot, Q-row of col. 9) 705 ✗ 99=la 856 ✗ 250=us 245=sen 831 ✗ 100=le 859 ✗
  609=Presbyter 858 ✗ 101=li 24=h → six of fourteen groups outside the key.
* 14 Jan 1660: 729 ✗ 549 ∅ 856 ✗ 21=g 245=sen 831 ✗ 99=la.
* 16 Jan 1660: 729 ✗ 549 ∅ 856 ✗ 8=c 245=sen 831 ✗.

Template test "For / Mr / [name] / these / [initials]": 729, 549, 856, 245, 831 would have to be for, Mr,
these, ... — none of them is (for=210, Mr.=536, these absent), and no single additive offset maps 729→210
and 549→536 (differences 519 vs 13), so it is not a shifted use of the same key. The recurring block
`729 549 856 … 245 831` across the three later letters shows Hyde reused a stock dummy formula, but no
key in the Barwick correspondence answers it, and the editor who had the papers says it meant nothing.

Other keys on the charlesii.htm page (Kingston 1658 THE=403, Kingston 1660 THE=363 with names to 925,
Massey 1660 THE=787/806) are ciphers with other correspondents and were not used between Hyde and
Barwick; they are also only partially known, so they cannot be meaningfully applied.

## Where a key would be if one existed

Hyde's own cipher keys: Bodleian, Clarendon MSS (the Calendar of Clarendon State Papers vols 4-5 lists
ciphers among the 1659-60 papers). Digital Bodleian (https://digital.bodleian.ox.ac.uk, searched
"Clarendon cipher") has no Clarendon State Papers volumes digitised. Given the 1724 editor's explicit
statement, an archive visit is not expected to yield anything for these superscriptions.

## Files

* barwick_key.py — full transcription of the 1721 plate key + the four superscriptions; run to reproduce the decode table.
* vita1721.txt, life1724.txt — archive.org OCR of the two editions.
* leaf385-490.jpg, c386_all.jpg, c387_all.jpg, c4xx_*.jpg — page scans / crops (key plate, superscription pages).
* getleaf.py, crop.py, fetch.py, findleaf.py, peek.py — download / crop helpers.
