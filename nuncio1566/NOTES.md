# Cardinal Alessandrino to the nuncio in Spain, 1567 — READ

Catalogue item 261 (class B), listed as "Unknown sender (Spain) to unknown recipient, 6 ciphertexts, 1 Jan 1566".
ASV (AAV), Segreteria di Stato, Spagna 1 (DECODE: "i. 1025, Segretario di Stato, doss. I"), DECODE R85–R90.

**Result (21 Sept 2026): read.** All six ciphertexts read end to end with George Lasry's reconstructed key, the
same key that read Alessandrino's 1568–69 letters ([alessandrino1568](../alessandrino1568/NOTES.md)).

## Who, when

- DECODE gives no sender, recipient or date beyond the volume span (1566). The archive description on the records
  lists the volume's units. Folios 146–338 are "Lett. orig. e cifre del card. Alessandrino al nunzio, 2 jan
  1567 – 29 dec 1567". All six ciphers fall in that range (ff. 165, 236, 249–250, 301, 314, 324).
- Sender: Michele Bonelli, Cardinal Alessandrino, nephew and secretary of Pius V. Recipient: the nuncio at Madrid,
  Giovan Battista Castagna. The clear letter on f. 163r opens "Molto Rev.do Mons.r come fratello", the cardinal
  nephew's form of address to a nuncio, and is filed as "Nuntio di Spagna" in the foot margin.
- Dates, from content (M): R87, on the archbishop of Cologne Friedrich von Wied who had not sought confirmation,
  is before his resignation (autumn 1567). R88–R90, on the second French civil war (Condé and the Admiral in arms,
  the Constable alive), fall between the Surprise of Meaux (28 Sept 1567) and the battle of Saint-Denis (10 Nov 1567).

## Key

Lasry's reconstruction, DOC_R85_D3265 etc. (24 Oct 2020), identical on all six records and to the one on
R93–R102. Polyphonic: 1 u|t, 2 i|m, 3 f|g, 4 a|l, 5 o|s, 6 e|n, 7 d|r, 8 b|c, 9 p|z; 0 null; X0Y0 nomenclator and
dotted pairs. `decrypt.py` is alessandrino1568's decoder unchanged (beam search, lang/ it-cinquecento), run on the
DECODE transcriptions (RebAn, 2016): `PYTHONUTF8=1 python decrypt.py > decrypt_raw.txt`. `rNN.digits.txt` are the
digit streams used for the profile counts.

## The letters (gist from decrypt_raw.txt)

- R85 (f. 165r; cipher of the letter beginning on f. 163r, whose clear part is about hurrying the archbishop of
  Toledo, Carranza, to Rome): the Pope wishes to be certain whether the King's journey [to Flanders] will take
  place, because if so he wants an interview (abboccamento) with him at the most convenient place; the nuncio is
  to find out. From words alone nothing can be built; the King should be exhorted, since such a meeting would bring
  great fruit to the Catholic religion; the prudence and experience of the King of Spain; nothing will be lacking
  on the Pope's side in whatever is for the service of God.
- R86 (f. 236r): Milan. Proceedings against the authors of the outrage on the archbishop's (Borromeo's)
  jurisdiction: the Senate with its arms; the Pope will use spiritual arms and a monitorium; the dignity of the Holy
  See requires proceeding at least against the Capitano di giustizia and the fiscal (the worst of all), and some of
  the Senate; the King should deprive his ministers concerned; V. S. to press it at the opportune time.
- R87 (ff. 249r–250r, 3 pp.): the Pope wants the King's journey to Flanders, for the restoration of religion there
  and in Germany and a reform of all Christendom; the King's great desire for it. Then: the archbishop of Cologne
  has been many years in the see without seeking confirmation, and will not make the profession of faith in the
  form of the Council of Trent; he is treating with the Duke of Cleves; the Pope means to proceed to his
  deprivation, but fears the devil will stir many to support him; the King should work in Germany so that the
  Cologne chapter, not all Catholic, does not designate a suspect person dependent on the heretics who could
  attack the ecclesiastical state of the archbishopric.
- R88 (f. 301r–v) and R89 (f. 314r–v): two copies of one letter on the troubles of France. The King of France
  gives too much credit to the Chancellor, Morvilliers and l'Aubespine, his counsellors, and never resolves,
  always medicating the evil with worse; the Queen Mother's ambition to rule, "I believe she is a bad Christian";
  the kingdom kept divided so that she may rule. "I will tell you only this: if His Majesty had the Constable
  Montmorency and his son put in a secure prison, protesting to them that if within three days they did not make
  the Admiral and the Prince lay down their arms he would have their heads cut off, an end would soon be put to so
  many troubles", since the plot is believed to have been laid with the Constable's and his son's knowledge; she
  will find herself deceived one day and repent too late of not having believed the good; the Catholic King should
  be well instructed of that court. The two copies correct each other (R89 is cleaner on 314r).
- R90 (f. 324r): the same closing passage again ("instructed of the nature of that court and of the principal
  persons … it would perhaps be well that the King … the King of France … she thinks she can trust them, who are
  unfaithful"), so a third copy's last page or its continuation.

## Grades and what is open

- Continuous Italian throughout; single letters are model choices (M), words H where context forces them. Names
  read from the letters: Morvilliers ("mortiglieri"), l'Aubespine ("baspina"), Memoransi (Montmorency), Cleves.
- Recurring unread group "colospo"/"a colospo" in R85 and R87 (the King "inviti … a colospo per satisfatione del
  mondo"): not resolved; possibly a word corrupted by a transcription slip.
- Unlisted dotted groups [60.] [70.] [80.] [50.] [30.] [02.] [05.] [85.], as in alessandrino1568; not resolved.
- Not done: Serrano, *Correspondencia diplomática entre España y la Santa Sede durante el pontificado de S. Pío V*
  (1914), which prints Alessandrino–Castagna letters of 1566–68 and may give these in clear (HathiTrust 403; not on
  archive.org). No decifrato was seen on the images fetched (ff. 163r and 299r, the clear openings of the R85 and R88 letters, both "Molto Rev.do Mons.r come fratello").
- Transcriptions are DECODE's (RebAn 2016) and were not re-checked against the images; R88's second page has more
  '?' than R89's.
- In the France passage the nomenclator group reads S. S. where the sense needs the King of France; taken as S. M. (C).
