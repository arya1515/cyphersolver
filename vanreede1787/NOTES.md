# Van Reede diplomatic despatches, 1787–1793

Status: read in part (R1026, R1027 read; R1893 not read).

Target: DECODE R1026, R1027 and R1893, seven pages described as numerical
nomenclator ciphertexts sent by Arend Willem van Reede from Berlin to Laurens
Pieter van de Spiegel, Hendrik Fagel Jr and the Secret Committee of the States
General (29 Dec. 1787–24 Mar. 1793). DECODE suggests the code is likely the
“Grand Chiffre” of Stadholder William V.

The repository's existing authorized DECODE cookie is used only as a request
header to de-crypt.org by `fetch_decode.py`; it is never reproduced here.

## Work log

- 2026-09-20: target opened; authenticated acquisition begun. No prior reading
  or key has yet been established.
- 2026-09-21: **R1026 and R1027 read with DECODE key R1024** (the 1782 "Grand Chiffre"
  of William V, KHA A29 inv. 301, French, 1–5000). Control first: the R1028 undated
  Van Reede despatch (DECODE gives its plaintext) decodes word for word with R1024
  (`la reponse à donner au Roi à la communication que S.M. vient de faire...`), so the
  key is the right one. The earlier garble came from the transcription, not the key:
  DECODE's `J+` is a catch-all for a sign the transcriber could not place, and it does
  not stand for one digit (275J = 2750 *dites*, matching the interlinear gloss, but
  JJ8J = 1181 *le Roi*, 375J = 3751 *dix* in "à dix heures"). `resolve_j.py` tries every
  digit for each J+ and picks the reading with a 6-gram French model built on
  hellen1752/corpus_fr.txt (beam 40). 105 J+ groups resolved this way (79 + 26).
  Output: `reading_R1026.txt`, `reading_R1027.txt`, `resolved_R*.txt`.

## Reading (gist)

**R1026, Berlin 29 Dec. 1787, to Van de Spiegel.** The day before yesterday the two
ministers (Finckenstein and Hertzberg) put to the King the project of the alliance as
Van de Spiegel had sent it. There is to be a conference this morning at ten between the
King and his two ministers; Van Reede hopes for no change. "The only point so far is
that the King said he could not guarantee our possessions overseas"; Van Reede did not
press it, only that if they were attacked in Europe the King would furnish help in
money or subsistence. Mentions the Prince of Anhalt-Schaumburg, England, Finckenstein
and Hertzberg, the treaty. After the clear passage (the conference has been held): the
article is kept without the words *possessions outre-mer*, saying simply that if the
Republic were attacked by a European power the King would furnish the aid. (Cf. the
Prusso-Dutch defensive treaty of 15 Apr. 1788.)

**R1027, Berlin 4 Mar. 1788.** News from Russia; the Russian ministers are anxious
about the triple alliance; the Russian envoy has had no answer yet and does not expect
one until the Empress has the one she awaits from Vienna to her demand; the Emperor's
declaration of war on Turkey (Joseph II, Feb. 1788); a courier sent to London, followed
by two others, before (Prussia) explains itself on the proposals.

## What stays open

- Some passages remain garbled where the DECODE transcription misreads plain digits
  (not only J+): e.g. "comme ils mauvais oyent A differer", "Monsieur de L L nr" (the
  Russian envoy, probably Alopeus). A fresh transcription from better images would
  clear them.
- Unread groups (not in R1024 or damaged): R1026 1250, 21423068 (two run-together
  groups), 4 4 3 8 (corrected above to 4433), 331, 308J9, 2637, 2800, 3160; R1027 3660
  (x2), 2800, 3J089, 2637, 1J1021, 50, 3153, 2751. 2637/2800/3660 recur and are
  probably names absent from the 1782 key.
- **R1893 (24 Mar. 1793, to the Secret Committee, Dutch) not read.** It is a different
  system: three-digit groups with per-digit overmarks (~ v = ¨ +), 696 tokens, 513
  distinct marked forms, so several thousand possible values. No key among the DECODE
  records tried (R2846, R2848, R2850, R2851, R2243) and no crib; with this ratio of
  text to code size a ciphertext-only attack is not feasible. Closed until a key or a
  deciphered copy turns up (Staten-Generaal secret files, NA 1.01.02).
- Follow-up: catalogue 217 (DECODE R1057, Van Reede to William V, 4 Feb 1792) is
  also Grand Chiffre but written as unseparated digit runs with an interlinear
  decipherment; not attempted here.

Write-up: [docs/vanreede1787.html](../docs/vanreede1787.html).

## Remaining gaps
- R1893 (24 Mar 1793, 696 tokens) - blocker: no-key-material; different three-digit overmarked code, 513 distinct forms; keys R2846, R2848, R2850, R2851, R2243 tried; no crib
- R1026/R1027 groups 2637, 2800, 3660, 1250, 331, 3160, 3153, 2751, 50 and damaged groups - blocker: open-codes; not in the 1782 R1024 key; 2637/2800/3660 recur, probably names
- R1026/R1027 garbled passages from DECODE digit misreads - blocker: not-attempted; NOTES say a fresh transcription from the images would clear them; not done

## Escalation
- [x] siblings: R1028 and R1029 opened as controls (R1028 decodes word for word); R1057 noted
- [ ] clear-pages: not done — check the R1026/R1027/R1893 images for interlinear glosses beyond the 275J one and for a clear copy
- [x] known-keys: R1024 Grand Chiffre fits R1026/R1027; R2846, R2848, R2850, R2851, R2243 tried on R1893
- [ ] print: not done — Colenbrander Gedenkstukken and Vreede, Van de Spiegel en zijne tijdgenooten, for these despatches
- [ ] key-rebuild: not done — bracket 2637/2800/3660 alphabetically inside the R1024 code order and by LM context
- [ ] retry: not done — re-transcribe the digits from the images and rerun resolve_j.py
