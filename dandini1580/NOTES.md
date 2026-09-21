# Cardinal of Como (papal Secretariat) to Anselmo Dandini, nuncio in France, 1580 — DECODE R72, R73

Status: read (21 Sept 2026). Catalogue item 244 (removed from the open catalogue).

## The documents

ASV (Archivio Apostolico Vaticano), Segreteria di Stato, Francia 283C: "Letter orig. e ciffre della Segretaria al
nunzio, dall'11 gennaio 1580 al 26 dicembre 1580", ff. 1-129: Tolomeo Gallio, Cardinal of Como, to Mgr Anselmo
Dandini, nuncio in Paris. DECODE ("partially decrypted", homophonic + nomenclator, numerical):

- **R72** (ASV_i1025_SdS_France_283C-1): f. 52, the cipher enclosure of Como's letter from the Villa, 16 May 1580
  (clear letter ff. 50-53 in the DOC attachments; endorsed "1580 - 5 [sic] maggio ... del S.r Card.l di Como").
  About 519 cipher groups; the **contemporary decipherment is written out in clear below the figures** on the same
  leaf, as a block that looks like a postscript.
- **R73** (283C-2): ff. 89r-90r, a second cipher enclosure, no date on the images (1580). About 1,082 groups.
  **Decrypted by George Lasry** (DOC_R72_D3191 = DOC_R73_D3193, from KaJo's 2017 transcription, with his
  reconstructed key DOC_R72_D3190, 24 Oct 2020). 32 groups illegible (`?`) in the transcription.

DECODE's catalogue line "the text was read at the time" is right for R72 and, through Lasry's decryption, R73 is read too.

## Two keys in one frame

Lasry's key (D3190): two-digit letter homophones with even second digit, nomenclator = three digits + a mark
(`^`, transcribed `7` or `t/+` in SofPe's R72 transcription). It reads R73 but gives nonsense on R72.

R72 uses **the same frame and the same nomenclator** (966^ tanto, 266^ che, 366^ per, 388^ quello, 288^ questa, 188^
quanto) but **a different letter assignment**. Recovered here (21 Sept 2026) by parsing SofPe's transcription in the
R73 frame (`decrypt_r72.py`, dynamic programming; only code 38 is outside Lasry's table) and swap-annealing the
letter values against an Italian 4-gram model with the nomenclator words as fixed plaintext (`r72_anneal2.py`,
6 restarts; five agree apart from one or two codes). The result was then aligned with the clear text on the leaf and three codes corrected.

R72 letter key (C = confirmed in the alignment with the decipherment, M = from the anneal only):

    a 14 52 81   b 16 (C, "publica")   c 18 83   d 20   e 12 62   f 41   g 01 26   h 42
    i 30 72 24(M)   l 22   m 34 96   n 36   o 38 82   p 40 00(M)   q 90   r 44   s 46   t 28 48
    u/v 50 92   z 11(M; at the head it is a stray "1")   32 (M, rare)

Unread nomenclator groups in R72: 766^, 866^, 030^, 448^ (the clear text gives them as words in context:
766^ ≈ "come vien detto a V.S.", 866^ ≈ "presuppone"; not pinned). In R73 (Lasry): 866^, 466^, 766^, 324^, 300^ open.

## The reading

R72, f. 52 (contemporary decipherment, transcribed here; the decryption agrees word for word except that the cipher
has "commercio" where the clerk wrote "concetto"):

> La voce et l'opinione della pratica del Re Chr.mo con la monaca è uscita tanto publica che se ne ragiona hormai
> per tutto, et da ogniuno è tenuta per vera: onde quando bene non fusse vero il fatto come vien detto a V.S. da chi
> presuppone di saperne l'intiero, è pure sì grande il scandalo che nasce dal concetto di S. M.tà in quel luogo, che
> per levarsi la infamia che gli ne viene, dovrebbe astenersi in tutto dall'andar più a quel monasterio: et V.S.
> doverà ricordar questo punto, et incaricarlo gagliardamente, già che si ha voluto persuaderle che il fatto non è
> vero. Quanto alla pratica scoperta per conto del credito et sforzo del denaro per la spesa, N. S.re persevera nella
> sua deliberatione persuaso a ciò da molte ragioni che non occorre scrivere.

"The talk of the Most Christian King's affair with the nun has become so public that it is discussed everywhere and
held true by all: so even if it were not true, as someone who claims to know the whole told Your Lordship, the
scandal is so great that to rid himself of the infamy he should stop going to that monastery altogether. Press this
on him hard, since they have tried to persuade you it is not true. As to the scheme uncovered over the credit and
the raising of money for the expense, His Holiness persists in his decision, for many reasons not worth writing."

R73, ff. 89-90 (Lasry's decryption, gaps as in his file): the same affair. The ordinary princes' marriage (S.S. would
be brought in) ... "N.S. è certificato che il gentilhuomo ... ha parlato" ... "la M.S. si movere a abbracciar la
pratica" ... "sarebbe S.S. intieramente certa di muoversi con buon fondamento a trattare la pratica"; then the nun:
"non lauda M.S. che V.S. tenghi proposito alcuno con la Regina nel particolare della monaca per non pigliare occasione
di far con tal coperta qualche rumore non conforme alla mente di S.S." ... "quanto si può con l'officio che N.S. ne
fece con il confessore ... dalla parte della monaca N.S. ha visto commodità di mezzo tale spirituale" ... "S.M.tà
potrebbe far il medesimo con officio simile a quello, ma è ben bisogno di procedere tanto circonspettamente che non ne
nasca rumore né disordine alcuno" ... "la riprensione sia mossa e spinta da N.S. con il re" ... "in consideratione a
S.M.tà parte del molto che si potrebbe ragionevolmente dire in quello proposito". Read as far as Lasry's file goes.

## What is open

- R72: four nomenclator groups (above) and the M-grade letter codes; the contemporary decipherment covers the text.
- R73: 32 illegible groups in the transcription, five nomenclator groups; no contemporary decipherment on ff. 89-90.
- Date of R73; identity of the monastery (Henri III's devotions of 1580 are well documented; not researched here).

## Files

- `decode/DOC_R72_D1824_1824.txt` SofPe's R72 transcription (2019); `decode/DOC_R72_D3190_3190.txt` Lasry's key;
  `decode/DOC_R72_D3191_3191.txt` Lasry's R73 decryption; `decode/DOC_R73_D1789_1789.txt` KaJo's R73 transcription.
- `decrypt_r72.py` (parse + Lasry key; writes `r72_parsed.json`), `r72_tokens.py`, `r72_anneal2.py` (needs the
  it-renaissance corpus from the lang-assets worktree `../cypher-lang`). Images are not committed (ASV).
