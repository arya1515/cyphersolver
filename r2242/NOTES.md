# R2242 — Prince Frederick of Orange to the Hereditary Prince, London, 7 May 1795 (KHA, Koning Willem I, XVIII-3)

Status: read in part

DECODE R2242 ("KHA_A35_KWI_inr.XVIII-3_Prince_Frederick_to_Heredary_Prince_1795-05-07"), Non-decrypted,
4 pp., authentication-required images IMG_R2242_I15891–I15894 (photographs of photocopies, sideways; git-ignored
in `img/`). DECODE's note: not signed; the first lines point to Prince Frederick (Willem George Frederik,
1774–1799) writing to his elder brother; the cipher part "seems to be written by somebody else, originating
from a letter sent under cover to his banker"; the cipher "seems to point to a link with the Rassemblement de
Osnabrück"; the record asks for a pointer to R1892.

## System: the R1892 key, unchanged

Each letter is a vertical pair of digits 1–6 (top over bottom), monoalphabetic, plus graphic word signs. The key
recovered ciphertext-only for R1892 (`../r1892/NOTES.md`) reads this letter as it stands, which confirms that
DECODE's pointer is right: the same cipher, in Dutch here. `apply.py` is R1892's with the circle-with-dot sign
rendered DE, as in R1892.

The key is confirmed independently on page 1, where a contemporary hand wrote the clear Dutch under the four
cipher lines (a decipherment at the time, or the writer's own draft): every digit word agrees with it, and it
gives the values of a dozen word signs (below).

## The pages

- **p1 (cipher + clear under it).** "als deezen brief geleesen hebt, dan [is de zaak] genoomen en gebraaden. Zo
  het niet verandert, moeten wy niet in de Zee. Als de Erfprins iets begeert, zoo zulks maar weet: ben tot zijn
  dienst, dood of zoo te leeven, is het zelfde." The cipher continues on p3.
- **p2 (clear, dated "Den 7 Mey 1795").** "Weest zoo goed en zegt aan mijn Broer dat hij een brief van mij onder
  couvert van mijn Banquier van E… ontfangen moet hebben": money matters with the banker, a "wissel", letters
  from Hamburg that never arrived, "Robespierre"-era news; one word in cipher: 24 43 25 55 15 15 65 = **famille**.
- **p3 (17 cipher lines) and p4 (8 lines + P.S.)**, one continuous text (p3 ends "ra-", p4 begins "-tificatie").

## What the cipher says (p3–p4, Dutch; | = unread word sign)

The alliance and its effect on the Orange émigré troops, and the Dutch/Prussian situation after the Peace of
Basel (5 April 1795):

- … "| onse alliansie met | geeft | ook verandering; men heeft de officier[s] en de trouppes | wel | malkander
  gelegen … staat op veele der gedimitteerde offeciers te maaken … niet veel | stellen; ook is er geen de minste
  saamenhang tussen | [z]elve, zij [zijn] geheel verstrooid, | hooft …" (the troops scattered, no cohesion,
  dismissed officers).
- "de politiken ook | verslappen … men zig | niet te veel op [ver]laten | het point der coalitie … men heeft de
  ratificatie ons met | gepubliceert, of schoon de ratificatie zelver nog niet gekoomen was" — the ratification
  (the Prussian peace of Basel) published before it had arrived.
- "| Parijs | onse ministers … zijn nog | ambassadeurs gesonden om [de] ratificatie van onse | over te brengen"
  — envoys sent to Paris with the ratification.
- "maar blijft persisteeren het tegenwoordig gouvernement niet te erkennen, dan zoo zij geen Robespierismus durven
  te introduceeren … zeer veel dispositie … is mijn respect … het geheele geselschap … groet mijn broeder."
- P.S. fragment: "… is ook | landig … al | met hen."

Decrypts: `decrypt_p1.txt`, `decrypt_p3.txt`, `decrypt_p4.txt`; transcriptions `transcription_p*.txt`
(LLM transcription from the photographs; several pairs doubtful, marked ?).

## Word signs fixed by the page-1 clear text

| sign | value | | sign | value |
|---|---|---|---|---|
| > ⊙ ▱ | als deezen brief | | ÷ | zoo |
| δ-loop | genoomen | | ɣ | zulks |
| H-bar | zo / zoo | | § | maar |
| long S | moeten | | v | tot |
| ⊙ Y | de Zee | | crossed 8 | zijn |
| > ⊙ ♁ | als de Erfprins | | ʃ | zelfde |

⊙ alone = de (R1892). The p3–p4 signs Λ, ∞, Δ, φ, script L, ⊥ and some twenty others are open.

## Open

- About twenty word signs on p3–p4; p3 line 1 ("wat ze id men") and p4 line 8 are poorly read.
- A second, careful transcription pass of p3–p4 at full resolution would firm up the doubtful pairs.

## Prior art

DECODE: Non-decrypted, no transcription or decipherment on the record. The only decipherment is the clear text on
page 1 itself. This is the first reading of pages 3–4; the key came from R1892 (this project, 21 Sept 2026).
