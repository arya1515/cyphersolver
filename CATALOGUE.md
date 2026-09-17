# Catalogue of unsolved historical ciphers for future work

Compiled 17 Sept 2026 from (a) the Gallica/BnF catalogue harvest in `gallica_sweep/` (331 SRU records whose
descriptions mention *chiffre*; 225 items described as "avec chiffre" or "en chiffre" **without** a noted
*déchiffrement*), (b) items that S. Tomokiyo's cryptiana articles mark "undeciphered" but which do not appear on his
Unsolved Historical Ciphers list, and (c) this repo's own sweep of BnF fr. 16127. Everything below is **unvalidated
until reviewed**: entries marked ◇ were selected from catalogue descriptions only and the leaf has *not* been viewed;
entries marked ● have been viewed on the image (fr. 16127; fr. 3484 f. 34).

Failure mode first: "avec chiffre" in Omont's inventories means the letter contains cipher, not that it was never
read. The Court's decipherment may sit in another volume, a modern edition (Scheurer's du Bellay, Mousset's Longlée,
Savasse's Maisse) may print a clear text, and Tomokiyo may already have a key that reads the leaf even where he wrote
"undeciphered". Each entry therefore lists what would confirm it is genuinely open. Coverage checks were made against
Tomokiyo's unsolved list and his French pages for Henri III, Henri IV, Nevers, Mayenne, the League and fr. 4715 (copies
in `gallica_sweep/src/`); his François I era article was **not** fetched (*), so 1520s–1550s entries carry that caveat.

## The 25 targets

Difficulty key: **A** siblings with decipherment in the same volume (key recoverable by alignment, as for Feuquières
and Catinat); **B** partial key exists in print (Tomokiyo) or the cipher family is known; **C** no key, no sibling,
attack by statistics only.

| # | Date | Item | Shelfmark / access | Status & prior art | Why it matters | Diff. | Seen |
|---|------|------|--------------------|--------------------|----------------|-------|------|
| 1 | 13 Jul 1572 | Claude de Mondoucet (Brussels) → Charles IX | BnF fr. 16127 ff. 60–61, ark btv1b90609766 (PDF page = canvas + 2) | Only despatch of the ~20 ciphered ones without the Court's decipherment; not on any list. Key not recovered by four aligners (see `gallica_sweep/NOTES.md`); f. 62r carries interlinear glosses to anchor on | Four days before Genlis's relief column was destroyed at Saint-Ghislain; French covert support of Orange, six weeks before St Bartholomew | A | ● |
| 2 | 4 Jan, 5 Sep 1573 | Mondoucet (Antwerp, Amsterdam) → Charles IX, further leaves whose margin decipherment is abridged or missing (*) | BnF fr. 16127 ff. 126–127, 138–140 | Inventoried in `gallica_sweep/NOTES.md`; margin readings visibly shortened. Confirm on image which passages lack a reading | Siege of Haarlem, Alkmaar; Alva's last year | A | ● |
| 3 | 26 Apr 1573 | Guy de Saint-Gelais de Lanssac (Warsaw) → Charles IX | BnF fr. 4735 no. 51, f. 126, ark btv1b9060724s (614 canvases, microfilm, canvases unlabelled) | Described "avec chiffre" only; no. 52 is the decipherment of a *mémoire*, not of this letter. Siblings nos. 35, 36, 63, 65, 70 have decipherments | The Polish election embassy: Henri of Anjou elected king of Poland 11 May 1573 | A | ◇ |
| 4 | Jun–Oct 1528, Sep–Oct 1529 | Jean du Bellay, bishop of Bayonne (London) → Anne de Montmorency, five letters | BnF fr. 3078 nos. 5 (f. 3), 17, 19 (ark btv1b9060311s); fr. 3077 nos. 18, 23 (ark btv1b90599292) | No decipherment noted. Check Scheurer, *Correspondance du cardinal Jean du Bellay* t. I (1969), which may print clear texts from other copies (*); not in Tomokiyo's fetched pages | Henry VIII's divorce suit, the sweating sickness, Wolsey's fall (Oct 1529) reported by the French ambassador | C (A if any sibling deciphered) | ◇ |
| 5 | May–Dec 1526; Aug 1529 | Nicolas Raince (Rome) → Montmorency and → François I, eight letters | BnF fr. 2984 nos. 6 (f. 29), 7, 8 (f. 39), 10, 11, 24, 28 (ark btv1b90598430); fr. 3091 no. 11 (ark btv1b9060253s) | No decipherment noted; no. 8 is entirely in cipher. Raince not on unsolved.htm; Tomokiyo's François I article not checked (*) | League of Cognac, Colonna raid on Rome (Sept 1526), prelude to the Sack; Aug 1529 = Cambrai/Bologna | C | ◇ |
| 6 | 1529–1537 | Gabriel de Gramont, bishop of Tarbes (Rome) → Montmorency, 11 Oct [1529] and 21 Jul; Cardinal de Mâcon (Rome) 11 Apr 1537; Jean de Langeac (Venice) 14 Jan | BnF fr. 3091 no. 23; fr. 3071 nos. 4, 7 (ark btv1b9060315f); fr. 3083 no. 8 (ark btv1b90601328) | "En chiffre" / "avec chiffre", no decipherment noted (*) | Charles V's coronation at Bologna; Clement VII's marriage diplomacy; Paul III and the 1537 truce | C | ◇ |
| 7 | 27 Sep 1527; 11 Apr 1528 | Marquis del Vasto → Charles V (Spanish); anonymous report to Charles V; Italian memoir from Madrid | BnF fr. 3022 nos. 6, 10, 20, ark btv1b90601558 | Imperial correspondence in French hands, presumably intercepted; no decipherment noted (*) | Five months after the Sack of Rome, Lautrec's campaign in Italy | C | ◇ |
| 8 | 23 & 28 Feb 1529 | Gaspare Sormano and Joachim de Vaulx (Ferrara) → François I, three letters (Italian) | BnF fr. 3096 nos. 63, 65, 66, ark btv1b9060015d; sibling no. 62 (22 Mar 1529) **with** decipherment, no. 67 likewise | Same agents, same month: key almost certainly shared with no. 62 | Ferrara's defection from France before Cambrai | A | ◇ |
| 9 | 1497–1504 | Frederick of Naples → Catholic Monarchs (11 Jan 1497, partly cipher); Lorenzo Suárez (Venice) 24 Feb 1504; viceroy of Sicily (Messina) 27 Apr 1503; anonymous cipher 8 Jan 1497 | BnF Espagnol 318 nos. 5, 93, 94, 95, ark btv1b52503046q | No decipherment noted; the Catholic Monarchs' cipher families are studied (Galende Díaz) and a key may be published (*) | Earliest Spanish diplomatic ciphers online; Naples war (Cerignola, Garigliano) | C/B | ◇ |
| 10 | 1551–1558 | Claude de La Guiche (Rome) → Montmorency 22 Nov 1551; François de Noailles (Venice) → Cardinal de Lorraine 13 Nov 1558; chevalier de Seure (Lisbon) → de Fresne 12 Dec 1558 | BnF fr. 3138 no. 22, ark btv1b90601662; fr. 3151 nos. 33, 39, ark btv1b9059865k | No decipherment noted; the same volumes hold deciphered letters of Tournon, Babou, Morvilliers (other keys) | Parma war; Cateau-Cambrésis negotiations; Portugal after Sebastian's accession | C | ◇ |
| 11 | 31 Jul 1563; 1560s | Catherine de Médicis → Bernardin Bochetel, bishop of Rennes (imperial court); Court → Rennes; Bourdin → Rennes | BnF fr. 3181 f. 55; 500 Colbert 390 pp. 139, 357; 500 Colbert 392 p. 231 | Tomokiyo (Henri III page) marks these undeciphered though he reconstructed sibling keys of the Rennes embassy | Charles IX's majority declared at Rouen 17 Aug 1563; Trent's last session | B | ◇ |
| 12 | Jan–Jul 1586 | Forget, Matignon, Mayenne despatches: fr. 15572 ff. 43 (two pages, "Du xxx janvier 1586"), 110, 123–124, 143, 150, 154, 173, 196, 201; fr. 15571 ff. 218–219 (Matignon) | BnF fr. 15571, 15572 (Gallica) | Tomokiyo: "undeciphered", but gives partial openings with his Mayenne–Forget cipher 1 / Matignon cipher 3, so most are readable once his tables are completed | Guyenne front of the eighth war; Matignon vs Navarre | B | ◇ |
| 13 | "ce xxvj juin" [c. 1586] | Anonymous → Duke of Mercœur | BnF fr. 15564 f. 151 | Tomokiyo: undeciphered; other Mercœur-circle letters in the volume were solved by G. Lasry | League in Brittany | C | ◇ |
| 14 | 28 Oct 1586 | Anonymous figure cipher, sender marked by signs | BnF Clairambault 357 f. 167 | Tomokiyo reconstructed part of the key; two thirds of the first page unread | Autumn 1586 League intrigues | B | ◇ |
| 15 | 18 Jun 1592 | Charles III (II) duke of Lorraine → count of Vaudémont, copy | BnF fr. 3621 no. 97, ark btv1b52524472n; same volume no. 22 is a decipherment of *intercepted* Vaudémont letters (Jan 1592) | No decipherment noted for the June copy; the Jan decipherment shows the Nevers side broke this family | Lorraine's double game between the League and Henri IV | B | ◇ |
| 16 | 13 Sep 1592 | A. Pelissier (Burgos) → Pierre Jeannin, nine pages | BnF fr. 3982 no. 22 (f. 46) | Tomokiyo: "mostly in cipher, only partially deciphered" | League envoy at Philip II's court on the eve of the Estates of 1593 | B | ◇ |
| 17 | Nov 1592 – 1593 | Henri IV → André Hurault de Maisse (Venice), four letters countersigned Revol | BnF fr. 16093 ff. 370, 373, 406, 410 | Tomokiyo: undeciphered (overbars mark abbreviations). Check Savasse's 1997 edition of Maisse's despatches (*) | Henri IV's Italian diplomacy before his conversion | B/C | ◇ |
| 18 | 17 Jan, 10 & 27 Mar 1593 | Lebel, Savoyard ambassador in Paris → Duke of Savoy, three letters | BnF fr. 3983 nos. 11, 62, 100, ark btv1b9059406b | No decipherment noted; Lebel named in Tomokiyo's League page but check whether keyed | Savoy's candidature and the Estates of the League | C | ◇ |
| 19 | Feb–Jul 1593 | Spanish despatches: count of Miranda (Naples) → duke of Feria 25 Feb; duke of Sessa (Rome) → Diego de Ibarra 11 Mar; Sessa → Philip II 30 Jun (copy, decipherment begun); Ibarra (Paris) 10 Jul | BnF fr. 3983 nos. 45, 79; fr. 3984 nos. 47, 68 (ark btv1b9060633d) | No or partial decipherment noted; Ibarra/Sessa/Feria keys partly treated by Tomokiyo | Spanish management of the Estates of 1593 and the Infanta's candidature | B | ◇ |
| 20 | 14–15 May, 22 Jul, 4 Aug 1593 | Italian/French papal-side letters: memoir to Cardinal Sega of Piacenza 14 May; letter "Di Parigi" 15 May; Baudouin-Desportes → Pietro Aldobrandini and → Girolamo Frachetta 22 Jul (ff. 186, 189); Dr Mauclerc → Creil (Rome) 4 Aug | BnF fr. 3984 nos. 6, 8, 88, 90; fr. 3985 no. 7 (ark btv1b90606498) | Baudouin-Desportes' Lisieux letter of the same day is deciphered (f. 184); Mauclerc's 3 Aug letter is deciphered (no. 4): keys likely shared | Written in the week of Henri IV's abjuration (25 Jul 1593) and the Suresnes truce | A | ◇ |
| 21 | 27 Aug – 23 Oct 1593 | Duke of Nevers → Louis de Revol (27 Aug, 2 Sep, 7, 9, 23 Oct) and → marquis de Pisany (8 Sep, 14 Oct), copies with cipher | BnF fr. 3985 nos. 66, 88, 116; fr. 3986 nos. 68, 75, 81, 101 (ark btv1b9060631k, 481 canvases) | Tomokiyo read one passage with Nevers cipher no. 46; the rest unread | Nevers' embassy to Rome to obtain Henri IV's absolution (refused by Clement VIII, Jan 1594) | B | ◇ |
| 22 | 9–22 Nov 1601 | Henri IV → Philippe de Béthune (Rome), 9, 10 and 22 Nov 1601 | BnF fr. 3484 nos. 7 (f. 34, canvas 75), 8, 12 (f. 49), ark btv1b52523722c; ~25 siblings Nov 1601–Oct 1602 **with** decipherment | Key recoverable from siblings; Tomokiyo has a Béthune (Rome) cipher for 1606–08, not this one. Viewed: f. 34 is the sent original signed *Henry*, countersigned de Neufville, about the Este–Aldobrandini debt and Cardinal d'Ossat; c. 12 lines of letter-and-figure cipher with no interlinear or marginal decipherment | Aftermath of the Peace of Lyon, Biron's treason forming, the dauphin's birth | A | ● |
| 23 | 18 Feb & 1 Mar 1603 | Henri IV → François Savary de Brèves (Constantinople), and possibly others in the volume | BnF fr. 3541 ff. 60, 63 | Undeciphered as of Desenclos 2018; Tomokiyo gives a preliminary partial reading from a reconstructed key | Ottoman disorder of 1603, renewal of the Capitulations (1604) | B | ◇ |
| 24 | 12 Jan 1603, 28 Dec 1603, 27 Dec 1604 | Henri IV → Landgrave Maurice of Hesse-Kassel | Printed in Rommel, *Correspondance inédite de Henri IV avec Maurice le Savant* (1840) pp. 12, 148–189, 388–393; originals Hessisches Staatsarchiv Marburg | Undeciphered in Rommel and in *Lettres missives*; Tomokiyo reconstructed a later (1603–10) Henri IV–Hesse cipher: test it first | German Protestant alliance policy leading to the 1610 campaign | B | ◇ |
| 25 | 10 Nov 1610 | Marie de Médicis → Savary de Brèves | BnF fr. 3789 no. 12, ark btv1b9059628m | No decipherment noted; same volume holds deciphered Savoy (1606) and Villeroy (1605) letters | Six months after Henri IV's assassination; the regency's Rome policy | C | ◇ |

## Also noted, not counted

- **Prince de Conti's ciphered mémoires, 26–27 Mar 1649**, BnF fr. 3854 nos. 41–42, ark btv1b52520094g; no. 43 (for an envoy to
  the Archduke) has its decipherment. Fronde–Spain negotiation at the Peace of Rueil. Diff. A.
- **Phelipeaux d'Herbault → Béthune, 13 Feb 1626**, BnF fr. 3669 no. 25, ark btv1b9060205q: the single letter without
  decipherment among ~30 Louis XIII/Herbault letters of 1625–26. Trivial key recovery; Valtelline settlement.
- **Charles of Egmond, duke of Guelders**, letter entirely in cipher with ciphered address, BnF fr. 3015 no. 8, ark btv1b9060086g.
- **Letter to the abbé d'Orbais** (League council, Paris) and three loose cipher keys, BnF fr. 3413 nos. 62, 53, 61, 69, ark btv1b52510705j: the keys may read the letter.
- **Champagne news-letters to Nevers 1590–91**, BnF fr. 3623 nos. 23, 24, 25, 60, 78, ark btv1b525245007; **Laurière → Nevers 9 Jul
  1593**, BnF fr. 3625 no. 55, ark btv1b52511322v (sibling of 13 Jul, deciphered).
- **"Recueil sommaire" of enemy cipher letters Sept–Oct 1589 sent to Nevers "pour estre interprétées"**, BnF fr. 3977 no. 96, ark btv1b9060546p: check whether the intercepts themselves survive in the volume.
- **Philip II → Mendoza, 7 Sep 1589 (second letter)**, ark btv1b52508089f no. 6: only no. 5 of that date has its
  decipherment. Tomokiyo covers the Mendoza ciphers.

## Method

- Harvest: Gallica SRU `dc.description all "chiffre" and dc.type all "manuscrit"` → `gallica_sweep/sru_chiffre_desc.json`;
  items split on Omont's numbering and kept when they say *chiffre* without *déchiffrement*
  (`gallica_sweep/bnf_candidates.txt`). Shelfmarks resolved from IIIF manifests (`gallica_sweep/ark_shelfmarks.json`).
- Coverage: string search of correspondents against cryptiana `unsolved.htm` and the six French article pages saved
  in `gallica_sweep/src/`.
- Not done: image inspection of ◇ entries; Tomokiyo's François I article; Scheurer, Savasse, Mousset editions;
  DECODE search for each item.

**Checked:** catalogue descriptions and item numbering; shelfmarks from the IIIF manifests; presence/absence of a *déchiffrement* item in the same
volume; fr. 3484 f. 34 on the image (cipher, no decipherment on the leaf); Tomokiyo's status wording for entries 11–14, 16–17, 19–21, 23–24; fr. 16127 on the image.
**Not checked:** the leaves of ◇ entries; printed editions that may contain clear texts; DECODE records.
**User must verify** before attacking any entry: open the ark at the item's folio and confirm no decipherment
follows, then search DECODE and Tomokiyo's site for the correspondent and date.
