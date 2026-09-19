# Balbases (Nijmegen) to Fuenmayor (Copenhagen), 1677–78 — DECODE R985–R998

Status: read

Fourteen ciphered despatches of Pablo Spínola Doria, 3rd marqués de los Balbases, Spanish plenipotentiary at the
Nijmegen peace congress, to Baltasar de Fuenmayor, Spanish envoy in Denmark. They are dated 29 June 1677 to 22 March 1678.
Archives générales du Royaume, Brussels, Secrétairerie d'État et de Guerre, inv. nr. 2559. The images and DECODE's
transcriptions were fetched on 19 Sept 2026 with the cookie in `bordeaux/decode/cookie.txt`. They are in `decode/`
and are git-ignored.

**Result.** No key survives. None of the eight Brussels keys in the series fits (R958–R965, "chiffres 1647-98",
checked). The key was therefore rebuilt from the ten letters that carry a contemporary decipherment in the left
margin. It then reads the other four, which **nobody had deciphered: R992 (19 Sept 1677), R996 (1 Mar 1678),
R997 (8 Mar 1678) and R998 (22 Mar 1678)**. Across all 14 letters, 97% of the 8,150 cipher groups are covered by
the key.

## Method

1. Two agents transcribed every cipher line and every margin line from the images into `tx/R*.txt`. DECODE's own
   transcriptions leave out cipher lines, and its margin readings are poor.
2. Anchors came from n-grams that repeat across letters, checked against the margin text:
   - `58 28 10 65 y uf 22 16` = lo·s b·ru·n·su·i·c ("los Brunsuic")
   - `26 67 y di ed 28` = pr·i·n·ci·pe·s
   - `xo y no 23 ic 45 e` = co·n·fo·r·mi·da·d
   - `63 41 45 e` = no·ve·da·d
3. A hard-EM monotone aligner (`align2.py`) was seeded with these anchors. Each token emits a substring of the
   margin plaintext. The table converged in two rounds. `dec.py` builds the key and `key.json` is the frozen table.
   The decryptions are in `read/R*.txt`, each with its margin text for comparison.

## The key

This is a syllabic nomenclator with homophones. Groups are separated by spaces.

- **Single letters (numbers and a few signs):** a 21, 3+; b 10, n; c 9; d e; e 2+; g 16; i 22, 67; j u+; l 8, 19;
  n y, 24, 20; o 18; p 26; r 23, 31; s 28, B; t 27; y 25; z h; f x.
- **Consonant-vowel syllables in numbers:**
  - de 46; la 55; en 76; ra 65; re 66, 153; te 71; do 48
  - ta 70; lo 58; no 63; to 73; da 45; ti 72; di 47
  - le 56; ni 62; vi 42; ne 61; in 77; ve 41; va 40
  - na 60; on 78; an 75; li 57; ga 50; go 53; tu 74
  - vo 43; ar 80; gu 54; un 79; er 81; du 49; nu 64
  - ro 68; tr 188
- **Letter-pair syllables, consonant disguised, vowel kept:**
  - c is written x, d or l: xo/do/lo = co, xi/di/li = ci, xa/da/la = ca, xe/de/le = ce, xu/du = cu
  - f is written n: no fo, ni fi, ne fe, na fa, nu fu
  - y is written r: ro yo, ra ya
  - `=` = ui
- **Vowel-first pairs, read as reversed syllables with the consonant disguised:**
  - f for s: ef se, if si, af sa, of so, uf su; also ye es, ya as, yo os
  - d for p: ad pa, ed pe, id pi, od po, ud pu
  - c for m: ac ma, ec me, ic mi, oc mo, uc mu
  - q or g for h: aq/ag ha, eq/eg he, og ho
  - others: en em, ot ch, at cha, as za
- **Word codes:**
  - que: d+ (struck d), b+
  - de: p+, q+/g+
  - V.S.: H
  - para 05; por 15, is; sobre 184; quando 148; alguno 100; congreso 120; tam(bién) 185
  - ministro `des`; materia `dus`; duque `ep`; embax(ador) `§`; -mente `dan`; nue(stro) `fe`
  - Flandes `ban`; francia `bef`; franceses `bin`; Suecia 163; Dinamarca `or`; -bourg 105
- **Nulls and start/end markers:** 13+ and 13 (mostly), 300, 200, 700, 07, 01, 18+, 16+, 35.

Open: about 3% of groups are unassigned, mostly rare 3-digit name codes (82, 83, 150, 161, 182, 187, 189…). Some
homophones are also shaky: 41 reads di and ve, 77 reads in and ot, 61 reads ne and ri. These come from 4/9 and
similar slips in the transcription.

## What the four unread letters say (read from the key; gist)

- **R992, 19 Sept 1677.** On the protest the Imperial ministers published about the dissolution of the Bremen
  assembly. He has nothing to add: "de nuestra parte no nos queda que hacer sino es … temer" what the confederates
  will do. After Charleroi (the failed siege of August 1677) they may insist at the union that the conquests be
  shared out before anything positive is settled. A rumour here about the Danish chancellor, a brother of the
  duke, and the Duke of Celle. He gives it no credit, since V.S. has not reported it. The claim that the Duke would
  take his share of the father's conquests, the duchies of Bremen and Verden.
- **R996, 1 Mar 1678.** Sweden could not undo the distrust they feel towards the allies. What causes it is the
  miserable state of their own affairs and the allies' impatience. The proceedings of the Brunswicks rest on solid
  suspicions. He comments on the ministers of the northern princes, and on the thought of writing to them with a
  protest about treaties of peace that would leave out their participation. He praises V.S.'s diligence in
  avoiding that step. Strasbourg's lack of constancy. A French gentleman has returned from France "satisfied" with
  the Most Christian King. "We need the clarity of the [court] to set down the doubts we suffer from."
- **R997, 8 Mar 1678.** In the business of the Brunswicks' claim with the Danes to the treatment of ambassadors,
  nothing has been conceded. Nor was any formal act in writing made at the first step the other days. He comments on
  the discourse V.S. reports of the Duke of Hanover and his brothers. It all seems to him very heavy, "pero yo creo
  que nada de estas intrigas llegará a fin". He writes of "the incessant dangers in which we are placed" and his
  growing melancholy.
- **R998, 22 Mar 1678.** On the dependencies between the northern princes, who are of enough calibre to keep us
  embarrassed. He writes of the evils "que nosotros estamos padeciendo", worse than anything. He comments on V.S.'s
  prudence. On the loss of Flanders: "con la pérdida de Gante estamos temiendo la de otras importantes plazas".
  Ghent fell to Louis XIV on 9 March 1678. They are still waiting on the long delays of the others while the
  illness advances.

The ten margined letters (985–991, 993–995) are read at the time. The key reproduces their margins, and the
margins in `tx/` are the fuller text.

Dates (from the clear parts): R985 3 Aug 1677; R986 28 Aug; R987 18 (or 28) June; R988 29 June (docket 24 July);
R989 21 Dec; R990 19 Oct; R991 5 Oct(?); R992 19 Sept; R993 28 Dec 1677; R994 15 Feb 1678; R995 26 Jan; R996 1 Mar;
R997 8 Mar; R998 22 Mar 1678.
