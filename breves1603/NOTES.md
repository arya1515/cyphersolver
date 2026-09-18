# Henri IV → Savary de Brèves, 1603 (BnF fr. 3541) — catalogue item 23

**Result, 18 Sept 2026:** the "undeciphered" letters were decoded long ago in a contemporary clear copy, and the
original key survives. Three of the twelve ciphered letters are in print in full. The other nine are in print as
summaries. What stays open is the cipher text itself: fr. 3541 is not digitised, so the ciphertext of the nine
summarised letters cannot be read against the key from here.

## 1. The key: BnF fr. 3462 f. 103

- Gallica btv1b9058227h, **canvas 109**. The full-resolution scan (7541 × 4902) is `src/fr3462_c109_full.jpg`, cut
  into tiles in `key/`. My transcription is in `key.md`.
- It is Tomokiyo's "Savary de Breves' Cipher (1602-1603)", which he rebuilt from fr. 16144. On the right of the leaf
  are the alphabet (2 to 4 homophones a letter), a nomenclator (numbers 10–99 for the A–G words, signs for the
  rest), a column of persons (pape, roy, empereur, grand seigneur, sultane, grand bassa, viziers, aga des
  janissaires, beglerbey, nissangi, tesquitar, spahis…), *Doubles* (13 49 57 30 97 38 70 with a caret) and two
  lists of *Nulles*.
- Canvas 110 (f. 104) is **a different key**: the "Chiffre reformé pour Levant", sent to Brèves in April 1604.
  Canvas 111 is another table again. Neither fits the 1603 letters.
- The key checks out against Tomokiyo's partial reading of f. 60: aussi 11, avec 12, faire 92, fault 93, a = 7/3/5.

## 2. The letters (fr. 3541 = anc. Béthune 9021)

The folios come from Berger de Xivrey's source lines, which agree with the order of the BnF notice
(archivesetmanuscrits ark cc49988x, saved as `src/fr3541_notice.txt`).

| date 1603 | place | fol. | text in Berger, *Lettres missives* t. VI (1853) |
|---|---|---|---|
| 18 Feb | Paris | 60 | **full**, pp. 31–32 → `berger/1603-02-18_f60.txt` |
| 31 Mar | Metz | 63 | **full**, pp. 63–65 → `berger/1603-03-31_f63.txt` |
| 17 Apr | Fontainebleau | 66 | **full**, pp. 76–78 → `berger/1603-04-17_f66.txt` (cipher passages in italics) |
| 1 May | Fontainebleau | 69 | summary p. 668 |
| 13 May | Fontainebleau | 72 | summary pp. 669–70 |
| 22 Jun | Paris | 75 | summary pp. 670–71 |
| 22 Jul | Nanteuil | 78 | summary p. 672 |
| 6 Aug | St-Germain | 81 | summary p. 673 |
| 15 Sep | Caen | 84 | summary pp. 676–77 |
| 15 Oct | Fontainebleau | 104 | summary p. 678 ("chiffré à moitié") |
| 9 Nov | Fontainebleau | 87 | summary pp. 678–79 |
| 23/24 Dec | Paris | 90 | summary p. 680 |

Berger printed from a **clear copy**: "Biblioth. de M. Monmerqué, Ms. intitulé *Lettres à l'ambassadeur du
Levant*". It is not known where that copy is now (probably dispersed at the Monmerqué sales). The summaries are in
`berger/table_pp667-682.txt` (Wikisource OCR of t. VI, djvu 683–698).

Also in the volume: a fully ciphered king's letter of 5 Jan 1610 (f. 8), and a Puisieux letter with cipher,
incomplete at the end (f. 39). Both belong to Brèves's later period as ambassador in Rome (1607–1614), so they probably use a different key.
Not checked.

### Tomokiyo's reading corrected against Berger (f. 60)

| Tomokiyo | Berger |
|---|---|
| "mesuois*ns" | mes voisins |
| "fault nau*ra *sitost que vous le ap*e" | ou faire naufrage si tost que vous l'apprehendés |
| "roibuent plus craindre les armes du revolt eul dasie" | doivent plustost craindre les armes du revolteur d'Asie |
| "contestans et catholicques" | protestants et catholiques |
| "ja pripes de *t et daultre" | jà prestes d'une part et d'aultre |
| "quel en sera le congres" | quel en sera le progrés |

He took f. 63 for 1 March, but it is the Metz letter of 31 March ("le dernier jour de mars"). His "lissueduremument
c?omance a la porte" = "l'isseue du remuement commencé à la Porte".

### Content, in brief

- **February:** the "désordres" of the Ottoman empire, with Henri IV refusing to believe it is about to fall. The
  real danger is the *revolteur d'Asie* (the Celali revolt). Bouillon has fled to Germany. The king is leaving for
  Metz; war threatens over the Strasbourg bishopric (Brandenburg vs Lorraine).
- **March:** the palace *remuement* at the Porte. The emperor is recruiting Frenchmen (Nevers, wounded at Buda). The
  king refuses to mediate an imperial–Ottoman peace. English pirates. Elizabeth is ill.
- **April:** the spahi revolt of Mahmud Pasha is put down, and the mufti and his brother are in disgrace. Brèves is
  not to ask for an Ottoman fleet, and to back out of the peace mediation. Spain has designs on Algiers. Elizabeth
  has died and James has succeeded.
- **May–December:** the Hongrie/Transylvania campaign (Mózes Székely vs Basta). Frenchmen are to be withdrawn from
  Ottoman service. The chiaoux arrives at Marseille. Marseille ships are to be armed against Barbary and English
  pirates. The Nevers/Joinville expedition. A Porte coup in December (the execution of the sultan's son, Mahmud,
  is mentioned in August).

## What remains

1. **Images of fr. 3541 ff. 60–104.** They are not on Gallica, and there are none in Desenclos 2018 (her n. 6 only
   notes that the decipherments aren't written on the letters). A BnF reproduction order, or a reading-room visit,
   is the only route. With the key in hand, reading them is table work. The three letters in full text give about
   2 pages of known plaintext for fixing the glyph readings in `key.md` before tackling the nine summarised ones.
2. The Monmerqué clear copy, which would give full texts without any decipherment.

## Access check (18 Sept 2026, after the first write-up)

Checks for images of fr. 3541 anywhere online, all negative:
- Gallica SRU: `dc.source adj "Français 3541"` = 0 records. `dc.title "Breves"` + Français = 11 records,
  none of them fr. 3541. `dc.description "9021"` = no manuscript.
- The BnF notice (cc49988x) has no digitisation link.
- Gallica arks are not assigned in shelfmark order, so they can't be guessed: the arks next to fr. 3540
  (btv1b90605139) belong to fr. 5xxx volumes.
- Desenclos 2018 has no plates.

Tomokiyo does not say where his images came from. They were probably a reproduction ordered from the BnF.
Deciphering the nine summarised letters needs that reproduction.
