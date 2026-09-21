# "Ferenc Rákóczi II to unknown recipient, 4 ciphertexts" — DECODE R483, R852, R912, R922

Status: read in part. Three letters are reports *to* Rákóczi, read in substance with the preserved key DECODE R639.
The fourth (R483) is a Latin letter in Rákóczi's name, deciphered interlinearly when it arrived. Its key was not rebuilt.

Catalogue item 44 (class B, scored by rule). All four records are MNL OL, and the images are not in the public
domain, so none is reproduced here. Worked 21 Sept 2026 from the DECODE text transcriptions, fetched with
`fetch_decode.py` through the project's DECODE account.

## Correction to the catalogue

DECODE gives Ferenc Rákóczi II as the author of all four. That holds only for R483. R852, R912 and R922 address
"Monseigneur" and "Votre Altesse" and report on Rákóczi's affairs at the Polish court, so Rákóczi is their
**recipient**. They are the same kind of document as R902 (see `../rakoczi1707/`), which is addressed in clear to
Rákóczi's alias Pompeio Cesoni. The catalogue's date span "1704–1711" is DECODE's range for the volume. The letters
themselves are from 1707–08 (French) and June 1711 (Latin).

## R852, R912, R922: the Bonac–Groffey key

The three letters use the same one-part numerical nomenclator as R902. It survives as DECODE R639 (MNL OL G15 Caps.
C. Fasc. 44/08, headed *De Monsieur de Bonac et Graffei*). Codes run from 10 to 560. The range 10–120 holds letters
and endings, 121–460 syllables and words, and 461–560 names and places. The twelve odd numbers from 97 to 119 are
nulls. `decode.py` applies the table, parsing groups as `../rakoczi1707/decode.py` does, and the output is in
`R*_key08_read.txt`.

| Record | Shelfmark (G15 Caps. C. Fasc. 39) | Groups | In key | Date in text |
|---|---|---|---|---|
| R922 | pp. 346–347 | 730 | 683 (93.6%) | Dantzig, 28 October [1707?] |
| R852 | pp. 115–117 | 513 | 497 (96.9%) | [Dantzig?], ... December [1707?] |
| R912 | pp. 312–314 | 1,596 | 1,473 (92.3%) | "au quartier ...", 5 November [1707?] |

Groups are counted by the parser. `_check_profile.py --measure` counts single digits because DECODE separates every
digit with a space. Coverage alone proves little, since almost any number from 10 to 560 is in the table. The proof
is that the output reads as French, with the right names in the right places.

Most of the unread residue comes from DECODE's transcription (joined groups, one-digit slips, values above 560).
R852 is the noisiest: *beaucoup* and *serviteur* come up where letters are expected. That points either to digit
misreadings or to a slightly different issue of the table.

### What they say (in substance)

- **R922** (Dantzig, 28 Oct). "Monseigneur, je me suis souvenu depuis quelque temps de l'honneur d'escrire à Vostre
  Altesse …". The writer reports a sale (*vente*) done for Madame la Palatine de Belz (Elżbieta Sieniawska) and
  sends an authentic copy to the sieur Kray. He says he has been kept out of the business "as far as possible" by
  his own caution. He mentions Tököly ("Tekeli"), orders for carbines, and his coming departure "pour joindre le
  Roy de Pologne". He asks that Kray be given the orders that would let him continue his services "à la Cour
  de Pologne". Page 2 turns to money matters and a person who is a prisoner, and closes "je suis avec tout le respect
  possible, Monseigneur".
- **R852** (December). The writer acknowledges letters from Rákóczi. He will pass letters "au sieur Groffey", so
  Groffey is named in the third person and is **not** the writer of this one. There is news of the Diet, the
  marshal, the Germans and the Dutch, the Kingdom and Volhynia, and "vos ennemis". Letters from Monsieur Ráday and
  Count Bercsényi ("Berthoti") are to be forwarded by way of Cracow.
- **R912** (5 Nov). The letter gives news of King Stanisław, the Swedes, the Palatine of Belz and the Grand Hetman
  (Sieniawski), and the Muscovites under the Field Hetman. It mentions the King of Sweden's plans for a
  *pacification* in Poland, a new election, the Cossacks, the Emperor, and the Tsar. Rákóczi's letter to Marshal
  Rehnskiöld is discussed, which is the same affair as R902. The Palatine of Ruthenia is also mentioned. So is a
  regiment Rákóczi was asked to supply, which King Stanisław and the Germans are using against him, and Tököly.
  The letter closes "avec un profond respect et un zèle parfait".

Writer: unsigned. R912 and R922 are consistent with Groffey, the agent at the Swedish and Polish courts whose
name is in the key heading. R852 names Groffey in the third person, so at least that letter is by a colleague,
possibly Bonac's side or Kray. Grade: attribution M.

## R483: Rákóczi, Lwów, 27 June [1711], Latin

P237 Festetics 10. d. 2. 42–44, 6 pp., 2,112 groups by the parser. It is a different cipher: values run to about 800,
and the underlying language is Latin. The whole text carries a contemporary **interlinear decipherment**, which
DECODE transcribed as 166 PLAINTEXT lines, together with clear passages. It was read when it arrived. The opening
reads "Leopoli vigesima septima Junii 17[11]", and the text speaks of Vienna, the allied powers, the Emperor,
Pálffy, a manifesto "in omnibus Hungariae comitatibus … pro Rege promulgasse", and cannon brought up against "arcem
nostram Munkácsiensem". That fits Rákóczi's exile in Poland and the siege of Munkács, which surrendered 24 June 1711.
DECODE's 7 June 1711 is probably a misreading of the date. The R639 table gives nonsense on it, as expected.

Open: the key of R483 has not been rebuilt, although the interlinear would allow it. DECODE's Latin transcription
of the interlinear is heavily queried, so a clean text needs the images.

## Files

- `fetch_decode.py`: fetches the four DOC transcriptions (cookie from `../bordeaux/decode/cookie.txt`).
- `decode.py`: applies R639 (it reads `DOC_R639_D2752_2752.txt`, copied from `../rakoczi1707/`).
- `R922_key08_read.txt`, `R852_key08_read.txt`, `R912_key08_read.txt`: readings. `R483_key08_read.txt` is kept as
  the negative control.
