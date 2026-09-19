# No. 1, Vienna, 3 February 1720, in the first key (R5017): decryption

Autograph R5019 (SOA Plzeň, RA Windischgrätz, inv. 694, karton 5); register copy R5020 (inv. 5, book 5,
pp. 401–404). The numbers are taken from the copy and checked against the autograph. There are 26 cipher passages, A–Z.
Key R5017: numbers 1–400 stand for letters and bigrams (syllabary, key5017_syllabary.tsv) and 401–977 for words and
names (nomenclator, key5017_nomenclator.tsv). Run `python dec.py ct_1720-02-03.txt` for the mechanical output.
Below: the numbers, the key values, and the reading in context.

Notes on the key:
- **31.** The key gives 31 as "el". In all three places it occurs (F, X, Z) the sense needs "zu", which is syllabary no. 3. So
  "31" here is either a homophone for "zu" missing from the surviving key or a writing of 3. Both hands have it.
- **268.** The key reads "em". In G the sense needs "ein-" (*einichen*), so the key cell is probably "ein" or "ei".
- **283 da, 29 ro, 148 qui.** Together these give "Daroqui" in H. This is almost certainly the Portuguese envoy at The Hague, João Gomes da Silva,
  Count of Tarouca, in Charles's own spelling. The next passage (I) names Portugal.

| | clear text before | numbers | key values | reading |
|---|---|---|---|---|
| A | absonderlich | 89 312 251 65 14 312 20 48 96 | de n pe n te n ri de r | **den Pentenrider** (Pentenriedter, the Emperor's envoy in Paris/London) |
| B | oder geringsten | 315 353 129 312 675 927 543 926 495 795 97 | ar g wo n · machen · von · Frankreich · undt · dem · Regent · en | **Argwohn machen von Frankreich und dem Regenten** |
| C | auch wohl | 684 495 458 79 312 301 89 65 88 50 102 17 88 | mit · dem · Cadagan · cu n fi de n t er of ne t | **mit dem Cadogan confident eröffnet** |
| D | aber auf keine weis | 574 495 543 401 634 91 280 65 353 7 312 315 353 129 65 | gegen · dem · Frankreich · auch · kein · ge ri n g st n ar g wo n | **gegen dem Frankreich auch kein geringsten Argwohn** |
| E | absonderlich | 283 706 494 154 21 351 45 403 854 60 91 57 356 88 | da · nun · der · al be ro ni · aus · Spannien · ab ge sch af t | **da nun der Alberoni aus Spanien abgeschafft** |
| F | (bracket) | 31 76 388 14 312 496 543 911 112 388 191 684 513 515 859 545 970 657 | [zu] fi ch te n · das · Frankreich · vielleicht · su ch e · mit · Duc d'Anjou · ein · sonder · Frieden · zum · Mr. Morville | **zu fürchten, dass Frankreich vielleicht suche mit Duc d'Anjou ein Sonderfrieden durch Mr. Morville** |
| G | auf seiner hut, doch | 732 268 25 388 312 91 280 65 7 68 318 353 129 65 | ohne · em[ein] i ch n · ge ri n st en · ar g wo n | **ohne einichen geringsten Argwohn** |
| H | gut vernemen und vertrauen | 684 495 565 283 29 148 | mit · dem · Graf · da ro qui | **mit dem Graf Tarouca** |
| I | finden wir ohne dem schon | 927 768 403 | von · Portugal · aus | **von Portugal aus** (sein gute Neigung) |
| J | das … verdriesst | 849 631 685 494 413 | seyn · König · mir · der · Allianz | **sein König mir [mit] der Allianz** |
| K | und den | 144 103 58 395 634 680 64 26 65 514 | pu b li co · kein · mehr · re re n · darum | **publico kein mehreren darum** |
| L | als seinen | 631 279 40 191 413 | König · in di e · Allianz | **König in die Allianz** (zu bringen) |
| M | auf das obige aber mich | 768 89 65 225 312 | Portugal · de n ke n | **Portugal denken** |
| N | das wird nicht wohl | 849 191 46 112 26 65 45 162 105 926 446 339 88 449 515 927 854 917 257 393 88 | seyn · e me su re n ni m bt · undt · Bey tri t · [446] · ein · von · Spanien · unter · tru ct t | **sein, [eh er] mesuren nimbt und Beytritt … von Spanien unterdrückt** (446 read "Bischoff" in the key; sense unclear) |
| O | werdet ihr | 458 | Cadagan | **Cadogan** (auf all weis suchen beyzuhalten) |
| P | Unbilligkeit so wohl als schaden | 407 96 414 310 519 355 120 103 242 | alle · r · alliirten · ia · Engelländer · se l b st | **aller Alliirten, ja Engelländer selbst** |
| Q | man | 279 636 68 545 | in · künfft · en · Frieden | **in künfftigen Frieden** |
| R | nur das geringste wider | 152 191 967 934 91 202 388 14 890 91 68 89 96 88 954 | di e · zwischen · uns · ge ma ch te · Tractat · ge en de r t · würde | **die zwischen uns gemachte Tractat geändert würde** |
| S | das under wegen | 878 495 586 927 652 | Sardinien · dem · Herzog · von · Lothringen | **Sardinien dem Herzog von Lothringen** (zu geben ist sehr ideal) |
| T | endlich auch | 957 494 495 350 14 65 132 361 231 312 494 890 | wie · der · dem · qu te n · gl au be n · der · Tractat | **wie der dem guten Glauben der Tractaten** |
| U | das sonst | 685 496 417 927 178 65 140 267 88 | mir · das · aequivalent · von · mo n fe ra t | **mir das Aequivalent von Montferrat** |
| V | das in | 636 68 545 | künfft · en · Frieden | **künfftigen Frieden** (dieses onus nicht auf mich fall) |
| W | den | 495 513 | dem · Duc d'Anjou | **dem Duc d'Anjou** |
| X | oder dem so | 573 31 638 495 721 | gross · [zu] · [638] · dem · nutz | **gross zu … dem Nutzen** (638 unsure: Kommen/Kammern) |
| Y | ob (wie wohl endlich zu glauben) | 749 | D. Orleans | **der Duc d'Orléans** |
| Z | denke | 684 495 513 515 761 545 31 675 | mit · dem · Duc d'Anjou · ein · particular · Frieden · [zu] · machen | **mit dem Duc d'Anjou einen Particularfrieden zu machen** |

## What the letter says

Charles VI writes in his own hand to Windischgrätz, his envoy at The Hague, six weeks after Philip V dismissed
Alberoni (5 December 1719) and while Spain was preparing to accede to the Quadruple Alliance. The cipher carries the
substance of the letter:

- Windischgrätz is to report everything precisely to **Pentenriedter**. He should speak confidentially with
  **Cadogan**, the British envoy, and keep Cadogan on side "in every way". Towards **France and the Regent** he must show
  no suspicion at all.
- The Emperor's fear: now that **Alberoni has been expelled from Spain**, **France may seek a separate peace with the
  Duc d'Anjou** (Philip V, whom Vienna did not recognise as King of Spain) **through Morville**, the French envoy at The Hague.
  At the end of the letter Windischgrätz is asked to find out whether (as is after all to be believed) **Orléans intends to make a
  particular peace with d'Anjou**.
- **Portugal**: Count Tarouca's good disposition is to be cultivated, with the aim of bringing **his king into the
  Alliance**.
- **The peace terms**: the Emperor will not see **the treaty made between us altered** in the slightest. Giving
  **Sardinia to the Duke of Lorraine** is "very ideal and hardly feasible". He insists on **the equivalent for Montferrat**
  and wants the burden of the future peace not to fall on him. Any alteration would wrong **all the allies, even the English themselves**.
