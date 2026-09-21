# Cardinal Alessandrino to the nuncio in Spain, 1568–69 — READ

Catalogue items 253 (class B) and 254. ASV (AAV), Segreteria di Stato, Spagna 6/I, items 1–10 ("Lettere orig. e
cifre del cardinale Alessandrino dal 16 gennaio 1568 …"), DECODE R93–R102; and Spagna 6/II item 13 (1569), DECODE R115.
Sender: Michele Bonelli, Cardinal Alessandrino, nephew and secretary of Pius V. Recipient: the nuncio at Madrid,
Giovan Battista Castagna. The letters are undated on DECODE; folio order puts 6/I in 1568.

**Result (21 Sept 2026): read.** All eleven ciphertexts read end to end with George Lasry's reconstructed key.

## Key

Lasry's reconstruction (DOC_R9x_D32xx.txt, 24 Oct 2020), attached to every record; DECODE lists the records as
"partially decrypted" because the key is there, but no plaintext was posted.

- Polyphonic: each digit stands for two letters — 1 u|t, 2 i|m, 3 f|g, 4 a|l, 5 o|s, 6 e|n, 7 d|r, 8 b|c, 9 p|z.
  0 is a null. No h, q.
- Nomenclator: four digits X0Y0 (1010 Nostro Signore, 1090 V. S., 2090 che, 3010 Re, 4030 S. M.tà, 5020 per,
  6090 quel, 7090 quello, 8010 Re di Francia …) and dotted pairs (0^.0 comma, 30^.9 qua). Full list in decrypt.py.

Because each digit has two readings and the zeros make X0Y0 codes ambiguous with letter+null pairs, the text is
chosen by a beam search scored by the shared Italian model (`lang/`, it-cinquecento, no spaces):
`python decrypt.py > decrypt_raw.txt`. Output is unspaced; `[WORD]` = nomenclator, `[NN.]` = dotted group not in
Lasry's list. Each page ends in a run of padding (strings like `fcpfbrpf`), which is the cipher clerk's filler.

## The letters (gist from decrypt_raw.txt)

- R93 (6/I/1, f. 6r): friends of the crown of France have asked here that the Pope promote a marriage of one of the
  French King's daughters to His Catholic Majesty; the Pope would not move without knowing the King's mind; the
  nuncio is to sound it in the way he thinks best, assuring him no word will be said before his intention is known.
- R94 (6/I/2, f. 42r): jurisdiction. The Pope does not mean to revoke the King's privileges but to remove abuses grown
  through his ministers; the ministers try to strip the Holy See of its authority; the King should hear this freely.
- R95 (6/I/3, f. 55r): reply on the ministers' claims, the crusade alms ("elemosina … indulgentia"), the Pope's
  offer of a pension; the King must not be thought alienated from the Holy See.
- R96 (6/I/4, f. 81r): awaiting the nuncio's answer on the marriage; union of the three principal princes of
  Christendom; a heretic prosecuted by the Holy Office; the Hermits of St Jerome (Jeronimites).
- R97 (6/I/5, ff. 88r–89v, 4 pp.): Bolognese exiles (fuorusciti) sheltered in the King's lands, the Cavaliere
  Gualengo; the King as the Holy See's feudatory for Naples must hand back exiles under the investiture; the Turk in
  Adrianople, a French ambassador there, the German Protestants promising the Sultan help; danger to Christendom.
- R98 (6/I/6, f. 136r): the King's orders to his ministers about the clergy are delayed by waiting for commissions.
- R99 (6/I/7, f. 169r–v): the Order of St John and its Grand Master; Don John of Austria; the Milan senate against
  the archbishop (Borromeo) over the Corpus Domini procession; the Pope will use spiritual arms.
- R100 (6/I/8): the King's ministers' proceedings; a brief to be executed.
- R101 (6/I/9, f. 291r–v): Naples census (the hackney and the feudal dues of St Peter's day), the investiture, the
  schism threatened by the ministers; the King's realms will be troubled if he does not remedy it.
- R102 (6/I/10, f. 306r): a prelate "deputato in regno" failing in his office; the Pope might have made him cardinal.
- R115 (6/II/13, f. 641r, 1569): pensions on a see, the King's nomination, a commission; the Council.

## Grades and what is open

- Reading is continuous Italian throughout; individual letters are model choices (M), words H where the context
  forces them. Lasry's tentative glosses kept: 1040 Regina di Francia?, 3040 Fiandra?, 8090 sauere?, 2020 con?.
- Unlisted dotted groups met: [01.] [02.] [03.] [04.] [08.] [09.] [1.] [40.] [43.] [44.] [51.] [60.] [70.] [80.] [90.]
  — mostly punctuation-like (04. and 60. recur where a comma or "et" fits); not resolved.
- Not done: comparison with the contemporary decifrati and with Serrano, *Correspondencia diplomática entre España y
  la Santa Sede durante el pontificado de S. Pío V* (1914), which prints Alessandrino–Castagna letters of 1566–68 and
  may give some of these in clear. HathiTrust full-text search returned 403 from here.
- Transcriptions are DECODE's (TimB 2016, RebAn, Midas) and were not re-checked against the images.
