# Intercepted enemy cipher letters summarised for Nevers — BnF fr. 3977 no. 96

Catalogue no. 31 (priority 4.1, class B). Worked 20 Sept 2026.

Status: closed from the evidence. The question the entry poses is answered: **the September–October 1589
intercepts do not survive in fr. 3977**; only the summary does, and it is in clear French, now read. But the
volume holds **eleven other intercepted ciphered letters, every one with its contemporary decipherment**.

## 1. The question

The catalogue entry says: *"Only the 'Recueil sommaire' of the interpreted letters is described; whether the
intercepts survive in the volume is unknown."* Scores: *"Unknown whether there is any ciphertext to attack."*
Verify first: *"Sweep fr. 3977 around no. 96 for cipher leaves."*

## 2. The volume, and the folio map

BnF fr. 3977 = ark `btv1b9060546p`, 715 canvases, *Collection Mémoires de la Ligue*. Canvas labels are `NP`.
The catalogue notice (archivesetmanuscrits ark `cc504266`, fragment `cd0e4184`, saved to `src/notice_3977.html`)
carries the piece-by-piece *dépouillement*: **138 pieces, nos. 2–143, folios 3–423**.

Folio → canvas is not constant; two anchors read off the leaves:

| folio | canvas | offset |
|---|---|---|
| f. 125 | 229 | +104 |
| f. 127 | 231 | +104 |
| f. 318 | 520 | +202 |
| f. 330 | 540 | +210 |

`fetch.py` takes canvas numbers.

**A parsing trap worth recording.** A naive regex for `Fol. N • M` silently drops the multi-folio entries,
and one of those is the most important cipher entry in the volume:

```
Fol. 126, 128 et 130 • 43 à 45   Trois lettres, avec chiffre et déchiffrement,
                                 de don BERNARDIN DE MENDOÇA au duc de Parme, avril 1589.
```

The corrected pattern accepts `Fol. a, b et c • n à m`.

## 3. No. 96 itself: read

**Folio 318 = canvas 520.** The document is headed, in a large chancery hand:

> *Recueil sommaire des principaux poincts contenuz en plusieurs lettres escriptes en chiffre par les
> ennemis du Roy — **En Septembre et Octobre 1589** — et envoyées à S.A. pour estre interpretées en
> decembre aud. an.*

It is **in clear French**, not cipher: a digest in **fifteen numbered points** running fol. 318r–319r
(canvases 520–522). Read here:

1. The **duc de Mercœur** has asked the King of Spain for help through a captain; Spain has sent powder and
   money — *"xx[m]v et ii[c] quintaulx de poudre"* — by **Diego Maldonado**, despatched to **Nantes**
   *"avec le chiffre g[e]n[er]al d'Espagne"*, arriving 18 October 1589.
2. **Mendoza** has lent the Prévôt des marchands a sum, to his master's satisfaction; the Prévôt has since
   repaid it, and Mendoza is cautioned not to gratify him too promptly *"à cause des envieux et calumniateurs"*.
3. The sieur de **Mauléon** is aggrieved at not being employed by Spain; Mendoza renews the signal agreed
   with him, *"par tant la lettre escripte du chiffre qu'ilz ont ensemble"*.
4. The **master of the posts of Bordeaux** passes Spain's advices, and what **Matignon** orders him for the
   King's service.
5. **Villeroy** has complained to Mendoza that help has not come to the League, which was expecting it.
6. **Mendoza** writes repeatedly from **Bayonne** on what passed at **Arques and Dieppe**, *"jusques a
   dementir les advis et les memoires du Roy"*; the *"sornettes"* Madame de **Montpensier** tells him; and
   the King reproves him for not reporting particularly enough on the **Cardinal de Bourbon**, the **duc de
   Guise**, **d'Elbeuf** and the **archevêque de Lyon**.
7. The commandeur de **Diou** presses his suit at Rome; what the consistory means to allow him.
8. **The King of Spain presses the Pope**, and has his adherents press him, to **renew the excommunication**
   against subjects who obey the King, and beyond that deplores his treasure; the Pope seems willing to
   resolve, but wants ...
9. Spain **resolves to maintain the war in France**, to continue the Leaguers' agreed annual payments, and
   wants them paid in full; **Parma** to send his forces into France; **Moro**, captain of light horse;
   **Balagny**.

Points 10–15 follow on fol. 318v–319r and are not transcribed here.

## 4. The answer: no ciphertext under no. 96

Every piece in fr. 3977 dated September or October 1589 — nos. 81, 84, 85, 89, 90, 91, 92, 94, 95, 96, 97 —
is **in clear**. Not one is ciphered. The intercepts that lie behind the summary were sent to Nevers *to be
interpreted* and are not bound in this volume; what was kept is the digest.

So for catalogue no. 31 **there is no ciphertext to attack**. That is the result, and it is a negative one.

## 5. What is there instead: eleven deciphered intercepts

The same volume holds **eleven intercepted ciphered letters, every one with a contemporary decipherment**,
running February to August 1589 — the working papers of the same royalist codebreaking effort, three months
earlier:

| piece | folio | letter |
|---|---|---|
| no. 29 | 79 | Governor of Milan → Bernardino de Mendoza, Milan, 16 Feb 1589 (Spanish) |
| no. 31 | 83 | P. de Acuña → Mendoza, Turin, 28 Feb 1589 (Spanish) |
| no. 38 | 115 | Governor of Milan → Mendoza, Milan, 4 Mar 1589 (Spanish) |
| no. 39 | 117 | Bernardino de Yssunça → Martin de Yssunça, Brussels, 18 Mar 1589 (Spanish) |
| **nos. 43–45** | **126, 128, 130** | **three letters, Mendoza → the duke of Parma, April 1589 (Spanish)** |
| no. 47 | 135 | news of the duc de Mayenne → Claude Maumarché, for Pierre Letelier, 21 Apr 1589 |
| no. 48 | 137 | a Leaguer to a royalist he is trying to win for the Union, Paris, 21 Apr 1589 |
| no. 49 | 139 | Mendoza → Juan de Moreo, Paris, 21 Apr 1589 (Spanish) |
| no. 71 | 191 | Robert, marquis de La Vieuville → the duc de Nevers, 13 Aug 1589 |

**Folio 125/126 (canvas 229) photographed**: headed *"Copia de la carta escrita al Duque de Parma por Don
Bernardino [de Mendoza] … a los xv de Abril"*, the cipher runs in continuous strings mixing figures and
letters (`83 b2b9b792 43 b0399932 b11792 96 b7 138 45592 b2505797 b0925592 …`) and the French decipherer has
written **his plaintext word by word above every group**:

> *El Vizeseneschal de Montelimart, que V.A. conoce … aqui me escriva … un billete de Monsieur de Vienna en
> su creancia … y lo que por [Ma…] me ha dicho es el yr a dar intelligencia a V.A. de los abisos que tienen
> del Coronal Fifer … la leva que el haze por los de la Liga, y la que el Rey levanta de los 12.000 que los
> Cantones hereies le han acordado … puntos en que no me alargare, pues ellos … ha de referir a V.A.*

That is eleven complete cipher-and-plaintext pairs for Spanish ciphers of 1589 — the material from which the
keys themselves could be rebuilt. It is an unexploited seam, and it is the useful thing this target turned up.

## 6. Not done

- Points 10–15 of the summary are not transcribed.
- The eleven deciphered intercepts are catalogued and one is photographed; none has been transcribed, and no
  key has been reconstructed from them. That is a separate piece of work, and a promising one.
- Whether the Sept–Oct 1589 originals survive **elsewhere** (another Mémoires de la Ligue volume, or the
  Nevers papers in fr. 3985–4000) was not pursued.

## 7. Files

`fetch.py` — canvases and regions of fr. 3977 (ark btv1b9060546p) ·
`src/notice_3977.html` — the BnF *dépouillement* · `src/pieces_3977.json` — the parsed piece list
