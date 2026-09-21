# R1892 — an Orange prince on the émigré "rassemblement", c. 1795 (KHA, Prins Willem V, inv. 339)

Status: read in part

DECODE R1892 ("unkmown (Germany) to Prince William V", dated 1 Jan 1795, Non-decrypted, 2 pp.). KHA The Hague,
Prins Willem V, bundel A18 nr. 339. The archivist's pencil note on page 1: "brief uit KHA bundel A18 nr 339 —
Onderdaad geen nomenclatuur" (no nomenclator found). Images: DECODE IMG_R1892_I9358_P1, IMG_R1892_I9359_P2
(photocopies, photographed sideways; login images, git-ignored in `img/`).

## System

A 6×6 digit square. Each letter is written as a vertical pair of digits 1–6, the top digit over the bottom one
(read here as a token TOP+BOTTOM). Monoalphabetic, one sign per letter, with a few extra graphic signs (circle
with a dot, Λ, Δ, γ, ⊣H, cross, etc.) that stand for frequent words or names and are not in the square. Clear
words are mixed in on page 2.

Key recovered (ciphertext-only, quadgram annealing on page 2's Dutch; page 1 then read straight off in French):

| token | 11 | 12 | 13 | 14 | 15 | 21 | 22 | 23 | 24 | 25 | 31 | 32 | 33 | 34 | 35 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| letter | t | w (Dutch) / z (French -ez) | y, ij | x | l | z | o | k | f | m | d | n | v | h | b |

| token | 41 | 42 | 43 | 44 | 45 | 51 | 52 | 54 | 55 | 65 |
|---|---|---|---|---|---|---|---|---|---|---|
| letter | g | u | a | s | p | c | r | q | i | e |

Rare tokens 53, 61, 62, 63, 64 occur 1–3 times and are probably misreadings of the photocopy.
The square is not in alphabetical order; no key sheet is known.

## What it says

**Page 1 (French, all cipher).** The writer's father ("mon père") is sending Nagel (A. W. C. van Nagell, the
Orange envoy in London) back to the ministers to press for an answer on the representations made about the
*rassemblement*. In case General Dundas ("le général Vundas" in the cipher) declares that the pay will stop or
that the troops must embark, "il faudroit y souscrire et vous borner uniquement à tâcher d'obtenir de pouvoir
donner une gratification à ceux qui ne voudroient se soumettre". The recipient is to tell the troops on what
footing they will enter the service of S.M.B. (His Britannic Majesty), using an adapted copy of the paper meant
for them "dans le premier moment où il étoit question de leur embarquement", which is among the writer's papers.
Finally: do not charge the expense of my lodging to the account; pay it from the money of mine you hold.

**Page 2 (Dutch postscript, "het volgende schrift ... in het hollandsch met cijffer").** If the troops stay
together, the rassemblement is to be kept together; volunteers and officers are to be named and employed; the
officers who will not serve are to be given a set number of days to choose; it is hardly possible that the
French have not offered them service; "ieder [1000?] man kunnen plaatsen". The writer has had no answer for
weeks to his first letter and would rather have stayed at "Nam..nburg"; the writer hopes the recipient can
engage no one further. Closing in French: "le prince [sign] me marque en outre ... vous aurez la bonté de
communiquer le contenu de ce chiffre à mon frère" (the last word is ciphered, `63 25 22 32 44? 54? 65 52 65`,
read as "à mon frère" with two uncertain pairs).

Decrypts: `decrypt_p1.txt`, `decrypt_p2.txt`; transcriptions `transcription_p1.txt`, `transcription_p2.txt`;
`solve.py` (annealer), `apply.py` (key).

## Who and when

A son of William V (the Hereditary Prince or Prince Frederick; "mon frère" is the other) writing to an officer
in charge of the Dutch émigré troops gathered in Germany under British pay, after the flight of January 1795.
Page 1 cites a letter "en date du ... décembre". DECODE's 1 Jan 1795 is probably an archival date; the content
fits winter 1795/96, when the rassemblement's transfer to British service and embarkation were being negotiated.
The attribution "to William V" is the file's provenance, not the addressee.

## Open

- About 30 graphic word signs (circle-with-dot is the most frequent, likely "de/te/het"), not reconstructed.
- Page 2 line 1 and line 24 are poorly legible in the photocopy.
- Exact writer and addressee.

## Prior art

DECODE status Non-decrypted; no decipherment on the record or images. Searched project notes: fagel1804/NOTES.md
mentions R1892 only as "a dense two-digit/symbol system" unrelated to R2238. Key records R2240 (Orange name key,
four-digit) and R2233 do not apply.
