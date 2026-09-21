# Robert Fagel to William V, The Hague, 18 June 1804 (DECODE R2238)

Status: in progress — cipher transcribed and contextualized; exact plaintext still requires its missing codebook
nPublic write-up: https://dbourdeau.github.io/cyphersolver/fagel1804.html

Koninklijk Huisarchief, The Hague, A31 Prins Willem V, inv. nr. 337. DECODE R2238 (non-decrypted, nomenclator,
numerical, 3 pp., login). Robert Fagel (1771-1856), William V's adjutant in 1793-94, writes from The Hague to the
exiled Stadholder. Outcome so far: **attempted, open**. The key has not been found.

## The letter

DECODE numbers the pages back to front: P2 is the first page, P3 the second (the cipher), P1 the closing page with
"Je suis avec respect, Monseigneur, de Votre Altesse Sérénissime le très humble et très obéissant serviteur,
R. Fagel", dated "La Haye 18 Juin 1804".

Clear context (P2): a letter from the Hereditary Prince dated the 6th of this month announces V.A.S.'s departure
"as fixed" (destination read as Brunswick or Berlin, uncertain) at the end of next week. Gaebel arrived here on the
9th and could leave only on Monday the 13th. After conferring with Monsieur de Cesar, the Commissaires kept him
so that Monsieur d'Yvoy could be briefed. "Messrs les Commissaires de la maison" sent a note to Monsieur Hubrecht
(name uncertain) on Monday, hoping for a meeting. He replied by word of mouth that he hoped to speak with
Monsieur Damen within a couple of days. P3 opens in clear: "Dès lors il n'a plus fait entendre parler de lui, et
l'on ne tardera pas à connaître la déclaration, sur laquelle les instructions de V. A. S. et celles du ministre du
Roi sont parfaitement d'accord." The cipher follows. The subject is the 1804 settlement of the House of Orange's
property with the Batavian Republic.

## The cipher

`ciphertext.txt`: 128 figure groups (99 distinct), 2 to 4 digits, the highest 2510. Commas separate words. Dots
join groups inside one word, which points to syllable groups. Clear endings are appended to some groups (503t, 788e,
281s, 1241t, 687e, 248e). The words "&", "car" and "que" are in clear, and there is one boxed interlinear insertion.
Small superscript marks (c, 3, 6, 9, fractions) follow some groups, and their reading is uncertain. The arcs over
groups containing 6 or 8 are the looped digit tops, not marks.

## Keys tried (19 Sept 2026), all ruled out

- **Grand Chiffre du Stadhouder** (DECODE R1024, KHA A29 PWIV 301 B, 1782, J. F. Euler; de Leeuw, Cryptologia 25,
  2001). The DECODE key transcription (DOC_R1024_D2881, 4,732 entries, 51-5000; the 1-50 and 1201-1250 blocks are
  not transcribed) gives nonsense on direct lookup ("presque, dio, savoir, presenter, accession.?.cla.cahos ...").
  The optional additive Tableau (rows T-Dd, 17 values each, from de Leeuw's DOC_R1024_D1785) was tried from all
  187 row starts and 187 column starts. None gives French. The letter also carries no start letter at its head,
  which the Grand Chiffre instructions require when the Tableau is used.
- **R2240** (KHA PWV inv. 339, "cipherkey 1793 or later"). This key has letter homophones 1-100 and names and
  places 100-6006. Our dot-joined words are not runs of small numbers, so it does not fit.
- **R1035** (1803 Russia legation codebook) and **R1891** (1798 Schimmelpenninck codebook) are Dutch-language
  codes. The letter's plaintext is French.
- **Siblings in inv. 337**: R2236, R2237 (decrypted) and R2239 (the Hereditary Prince to William V, 1795-96). These
  use a small-number system with fraction marks, a different system from Fagel's.

The Grand Chiffre instructions make the negative result stronger than it first appeared: use of Euler's additive
table had to be signalled by a starting letter written at the head of the message. R2238 has no such letter, so it
must not be processed through that table. The direct R1024 lookup is nonsense and therefore rules that key out.

As a final check against a merely *renumbered* Euler key, `try_key_transforms.py` tests all 5,000 cyclic shifts,
small coprime affine maps modulo 5,000, number complements, and every four-digit position permutation against the
R1024 transcription. Candidates are ranked with a four-character language model trained on three public-domain
French memoir/correspondence corpora. The best candidate scores -10.167 per character and is plainly word salad
(`officier commencer quatrecent ...`); the genuine clear sentence adjoining the cipher scores -8.524. No tested
renumbering produces connected French. This eliminates the remaining simple-key-transform shortcut without
pretending that it excludes an arbitrary new code assignment.

The DECODE key R2233 (Wolff/Wilhelmina, 1801) is also incompatible: it is a small homophonic system based on
consecutive numbers through 45 with index figures, whereas R2238 uses code groups as high as 2510.

## Modern archive concordance and historical context (20 Sept 2026)

The current online KHA A31 inventory does **not** agree with the old shelfmark in DECODE. Modern A31-337 is a
file about William V's English securities (1795-1799), and A31-339 is correspondence with the London banking
house Van Notten (1796-1806). The target instead belongs contextually in modern **A31-2306–2308**, “Stukken
betreffende de onderhandelingen met de Bataafse Republiek over schadevergoeding voor het verlies van bezittingen
en inkomsten,” 1802-1804; files 2307 and 2308 are both dated 1804. The adjacent A31-2292–2293 dossier contains
letters involving William V, D'Yvoy, Van Olden and Prussian authorities, and its catalogue note explicitly mentions
three Fagel letters of April 1804 about fl. 500,000 intended for the French with Van der Goes's knowledge. None of
these modern files has online scans.

This fixes the subject and sequence. Contemporary reporting says the talks were a final liquidation of House of
Orange claims under the Franco-Prussian convention of 23 May 1802. The Batavian plenipotentiaries were J.C.
Hultman and De Vos van Steenwijk; the Orange side was represented by R. van Olden, J.P. Ferrand and P. Damen.
The proposed settlement was five million guilders in ten instalments. The Legislative Body later rejected it by
17 votes to 8. The Delft newspaper reported on 4 July 1804 that Baron d'Yvoy and Fagel had returned to The Hague
from a short journey to Germany. This fits the clear sentence in the cipher passage, “j'attends la réponse pour
partir,” and places the encrypted section immediately before that journey.

Relevant modern KHA catalogue nodes:

- A31-2292–2293: compensation dossier from Princess Wilhelmina, with William V, D'Yvoy, Van Olden, and Prussian correspondence.
- A31-2299: instructions for and correspondence with M.L. baron d'Yvoy (1801-1802).
- A31-2306–2308: Batavian compensation negotiations (1802-1804); 2307 and 2308 are the two 1804 files.
- A31-2309: treaty of 1/9 August 1804, not ratified by the Batavian government.

The only modern A31 catalogue hits explicitly described as cipher keys are A31-903–904 (ca. 1775-1780), far too
early. There is no catalogued 1804 codebook and no scan in the modern compensation files, so the decisive key is
probably an uncatalogued enclosure within A31-2307/2308 or the matching copy/draft in the Fagel archive.

## Authenticated DECODE verification (20 Sept 2026)

The logged-in DECODE image and transcription views were checked directly. R2238 has no contributed
transcription, and neither does the closest cipher companion R2236. A database search for Robert Fagel returns
only R2238 among correspondence records. R2237 is marked decrypted and preserves plaintext plus cipher, but its
cipher uses small numbers (roughly 1–180) with index/fraction marks; it is visibly a different system and cannot
provide the R2238 key.

The DECODE advanced search for numerical French keys found no key whose metadata combines a large (100+)
nomenclature with the other target characteristics. A period search did identify British Library Add MS 32264,
especially R8963/R8964 ("French Cypher 1798–1799") and R8984 (1805). The first is a random two-part code numbered
only 1–750, and the latter only about 1–250 plus additions. Direct and modulo-1000 comparisons with R2238 are
nonsense. The intervening Add MS 32264 records R8965–R8983 are mostly one- or two-page royalist correspondence
specimens, not large codebooks.

High-resolution comparison confirms that 1531, 1731 and 2510 are genuine four-digit groups rather than
three-digit numbers followed by clear letters. The required nomenclator therefore really does extend to at least
2510. Euler's original instructions were also re-read from DOC_R1024_D1785: superencipherment adds one value from
the 17-column table to each code group, and the chosen starting row or column must be written at the head of the
letter. R2238 has no such marker. Exhaustive row/column-start subtraction and direct lookup both remain nonsense.

The Nationaal Archief catalogue now exposes a stable deep link for the Robert Fagel series, but the relevant
material is explicitly marked PHYSICAL. No digital object or IIIF scan is attached to inv. nr. 1909.

## Printed sources and a newly identified key file (20 Sept 2026)

The full OCR and page images of Colenbrander, *Gedenkstukken*, vol. IV, bands 1-2 (1908), are available in the
Huygens retrobooks reader. This is the documentary edition later historians cite for the compensation negotiations.
It does not print Fagel's letter of 18 June 1804. It does, however, fix the immediate context unusually closely:

- no. 790 (d'Yvoy to Talleyrand, 18 February 1804) asks for French intervention in settling the Orange claims;
- no. 793 and its note record that Talleyrand forwarded the memoranda to Sémonville, and that d'Yvoy promised
  500,000 Dutch guilders for payments and gratuities at Paris, Berlin and The Hague;
- a letter of Princess Wilhelmina dated 14 June 1804 says the arrangement was already decided and complains about
  the promised payments; this is only four days before R2238;
- no. 794 says Robert Fagel and d'Yvoy returned from The Hague with the signed convention on 7 August;
- nos. 803-804 print Robert Fagel's reports from Paris of 28 January, 2 February and 15 February 1805. They concern
  renewed negotiations after the 1804 convention failed, not the target letter.

The current Royal Collections catalogue also reveals a substantially better key target than the two older key
books: **A31-902, “Stukken betreffende de aan het hof gebruikte geheimschriften,” one packet, broadly dated to the
late eighteenth and early nineteenth centuries**. It is in William V's own archive and has no online scans or child
description. A31-903/904 are specifically the older ca. 1775-1780 *Chiffre chiffrant/déchiffrant* already known;
A31-902 is a separate packet and is therefore the first physical file to request for the missing 1804 key.

An authenticated DECODE advanced search for every record typed as a **Key** at the Koninklijk Huisarchief returns
only four records: R1024, R2233, R2235 and R2240. All four are now ruled out. R1024 is Euler's 1782 large code
already tested directly and with its optional addition table; R2235 and R2240 are exile-era keys already compared
with the target; R2233 is Wolff's 8 September 1801 homophonic key, but DECODE's own description and image show that
it uses consecutive values no higher than 45 with index numbers 1-4. A broader DECODE search for French keys dated
1799-1805 finds only R2233. Thus the database does not contain an overlooked contemporaneous large KHA key.

The fully digitized Royal Collections file A32-630 (387 scans, “Anciens déchiffrements ...”, 1795-1797) was also
sampled throughout and compared at high resolution with R2238. It and DECODE R2237 use the small Euler/Boyer book
cipher described by de Leeuw: reference groups run only from 10 to about 334 and separate one-digit positions select
letters from the reference words. R2238 instead clearly writes 1531 and 2510 as full baseline four-digit groups;
its occasional small superscripts are separate marks. The superficial similarity is therefore not a usable key.
Royal Collections A35-488-1, the two-scan family cipher key made by H.W. van Aylva on 19 January 1795, is likewise
a word-grid/transposition key rather than R2238's numbered nomenclator.

The Royal Collections CMS was then checked below the public catalogue interface. A31-902 is page 7354 and its
archive-detail JSON explicitly returns empty `scans`, `scans_thumbnails`, `children`, `related_items`, `content`,
and `finding_aids` fields. Its generated ZIP endpoint resolves to a valid but empty 22-byte archive named
`A31-902 images 0.zip`; the single-image endpoint is a 404. The Wagtail image index contains only eight images
whose title begins with A31 (A31-216, A31-1007-1, and derivatives), and a direct audit of the surrounding A31
ingest batch likewise finds no A31-902 asset. This rules out an unlinked public scan: the packet is genuinely
undigitized.

The archive's current public instructions confirm that pre-7 September 1948 holdings are open for scholarly
research by application. General archive questions go to `info@koninklijkeverzamelingen.nl`; requests for images
not yet online can often be supplied for a fee through `beeld@koninklijkeverzamelingen.nl`. The web permission
form is for arranging personal consultation and requires identity and research-role details, so the least
burdensome next step is the prepared, narrowly scoped email asking staff first to identify the key or parallel
decipherment and to quote any reproduction cost.

A DECODE search for French correspondence received by William V in 1795-1806 returns only R2239, R2238, R2234,
and R1892. R2239 is the already-ruled-out small book cipher. The authenticated scans show that R2234 is a
continuous non-numerical cipher alphabet and R1892 is a dense two-digit/symbol system; neither resembles R2238.
Thus DECODE contains no second message in the target large-number system from which a crib or parallel
decipherment can be derived.

The authenticated DECODE key search was finally broadened beyond the KHA. The `100+` French-nomenclature filter
returns eleven records, all from Lille (1670-1689) or Saxon files (1700-1728); no eighteenth-century or Napoleonic
candidate appears in that metadata class. An unrestricted French-key search for 1750-1810 returns 28 records.
Only four families overlap the target period: KHA R2233/R2240 (already ruled out), British Library R8987 (1809),
and Uppsala R5160 (catalogued 1772-1809). The R8987 image is a simple 48-value homophonic alphabet. Both pages of
R5160 were downloaded and rendered: it is an alphabetically arranged French nomenclator numbered only 210-841,
with letters and punctuation through 841, titled `Chiffre François, de M. de Lacy Avec`; its reverse is blank.
Neither can emit R2238's genuine groups 1087, 1531, 1731, and 2510. The remaining results end before 1800 and are
geographically unrelated. The global DECODE key audit therefore adds no viable shared codebook.

## Next

The code has about 2,500 groups, and a 128-group text cannot yield a unique exact plaintext without a key. The key
is most likely among the KHA papers of William V's exile or the Fagel family papers (NA 1.10.29, which DECODE indexes for keys of
1680-1793: R2792-R2852). The eleven undated sets R2842-R2852 were initially sampled on 19 Sept. A complete
13-image check of R2846 corrects the earlier shorthand description: it is a bilingual Dutch-French court
nomenclator, with instructions and parallel vocabulary/political-name sections rather than a purely Dutch key.
Its continuous numerical sequence ends at 999, however, and the small pasted annexes on the final leaves add no
four-digit range. It therefore cannot directly encode R2238's genuine groups 1087, 1200+, 1531, 1731, and 2510.

A deeper authenticated pass through R2842-R2852 on 20 Sept also corrected a DECODE ordering trap: the generated
`P` numbers are not consistently in the same order as the original `NL-HaNA_..._NNNN.jpg` filenames. Pages were
therefore re-sorted by the archival filenames before identifying their tails. The final tail audit is now complete:
R2842 P71-P72 and R2844 P20 are blank; R2845's last written leaves P20 and P18 cover 518-546 and 740-755, followed
by blank P21; R2847 P22 and P20 are blank after the previously observed 838-978 range; R2848 P10, R2850 P9, and
R2851 P11 are blank after their previously observed terminal ranges (about 455, 971, and three digits respectively).
R2849 terminates in a 1-200 syllable grid. R2852 P121 and P119 are paired Dutch/French word lists without numerical
code groups. R2843 P61 is blank, confirming that its preceding W-Z leaf (P62) is the last substantive one and reaches
only approximately 1055. Thus the sole four-digit exception is still below R2238's genuine 1087 and far below 1531,
1731, and 2510. The complete range audit rules out every DECODE Fagel-family key R2842-R2852 as R2238's direct
nomenclator; the KHA remains the strongest lead.

The most targeted physical checks are now: **KHA A31-902 first** (the packet of court cipher material), then
A31-2307 and A31-2308 (including loose enclosures and any parallel fair copy), A31-2292–2293 for the same negotiation
and cipher, and Nationaal Archief 1.10.29 no. 1909 (Robert Fagel's 1802-1803 compensation-negotiation file). A
request should ask specifically for a numerical French syllabic/nomenclator key with values extending to at least
2510 and for any duplicate or deciphered copy of the 18 June 1804 letter.

DECODE images are git-ignored (`img/`, `key*/`, `decode/`, `lines/`). Only derived text is committed.
