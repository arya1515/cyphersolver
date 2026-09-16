"""Generate the priority queue section of docs/index.html from structured data.

The queue had drifted into a 31-row table in which items already attempted, items blocked at source,
and things that are not ciphers at all were interleaved with live targets at ranks 1 to 14. The ranks
had stopped meaning anything. This rebuilds it as three honest tiers, and emits a filterable list
rather than a table, because the reasoning column had become prose crammed into a cell.

Run:  python _build_queue.py    (rewrites the section in index.html between the queue and blocked anchors)
"""
import re

CRYPTIANA = 'https://cryptiana.web.fc2.com/code/unsolved.htm'
T50 = 'https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/'
ELONKA = 'https://elonka.com/UnsolvedCodes.html'

# tier, name, date, href, badge, odds, oddsclass, effort, why
LIVE = [
    ("Telegram from Switzerland, “BLUME SALAMANCA”", "1937",
     "https://github.com/dbourdeau/cyphersolver/blob/main/blume/NOTES.md", "", "even", "md", "compute in progress",
     "Zurich to London and on to Spain, 8 January 1937, from the firm of Werner Oswald, who had close ties to Franco's side. <b>In progress, "
     "September 2026.</b> The first telegram is transcribed here from Schmeh's photograph, 123 groups, and checks against the 125 words "
     "on the form. It is a <b>transposition of Spanish</b>: index of coincidence 0.070, and Spanish fits the letter counts far better than "
     "French, English or German. Excluded, with every search first proven on planted Spanish: rail fence, skip and route transpositions "
     "(107,594 readings), single columnar, and now <b>double columnar in the forward direction</b>, same key at widths 2&ndash;30 and two keys "
     "at 2&ndash;16 &times; 2&ndash;16 (best &minus;5.9 per quadgram where Spanish scores &minus;3.9 and shuffled letters &minus;6.3). The reversed "
     "direction and the divide-and-conquer attack for widths 15&ndash;25 are running. The second telegram, which is not public, would help most."),

    ("Charles I to Boswell, and Nicholas to Boswell", "1643",
     "https://cryptiana.blogspot.com/2021/09/charles-i-boswell-cipher-1643.html", "", "even", "md", "medium",
     "Two letters of 2 November 1643 at the National Archives, unread. Tomokiyo's provisional transcription of the King's letter has <b>460 groups, 170 "
     "distinct, 69 hapax</b>, with English words left in clear between the groups (&ldquo;Not doubting but God will shortly enable Us to recompence "
     "soe 8 82 100 46 154&rdquo;), so the running cribs come with the text. A Civil War nomenclator of the same shape as the Ormonde letter read here. "
     "The risk is the transcription itself, which its author marks as uncertain in many places. Next step: separate alphabet groups from nomenclator "
     "groups by frequency, then a constrained climb against the clear words. Added September 2026, not yet attempted."),

    ("Richard Forster, possibly to Henrietta Maria", "1644",
     "https://cryptiana.blogspot.com/2021/09/an-unsolved-letter-of-richard-forster.html", "", "even", "md", "low",
     "A letter of 13 May 1644 in the hand of the Queen's treasurer, published by Karen Britland in 2013 and transcribed by Tomokiyo: <b>134 groups "
     "mixing letters and numbers, 24 distinct</b>, with one clear French phrase inside. Twenty-four symbols is an alphabet, not a code, and the "
     "plaintext is French. Short, so the answer must be checked against a matched control, but the test is cheap. Added September 2026, not yet attempted."),

    ("“Cifer with Spanish spy”, SP53/22 f.52", "1580s",
     CRYPTIANA, "", "partial", "md", "low",
     "A short undeciphered slip among the Mary Queen of Scots cipher keys, transcribed on Tomokiyo's page: <b>87 groups</b> on a digit-plus-b alphabet "
     "of about 26 symbols, so a monoalphabetic cipher of Spanish. Eighty-seven letters sits at the unicity distance for a mixed alphabet, which is why "
     "the odds are only partial: a reading may come out that cannot be confirmed. Worth an hour, with the control run first. Added September 2026, "
     "not yet attempted."),

    ("Lodovico Birago to the Duke of Nevers, the numerical paragraph", "1571",
     "https://gallica.bnf.fr/ark:/12148/btv1b9060248g/f120.item", "", "partial", "md", "medium",
     "BnF fr. 3251 f.119, a letter of 13 November 1571 in Italian. The rest of Birago's letters read with keys Tomokiyo rebuilt from deciphered siblings, "
     "but one paragraph is in a different cipher: a <b>continuous stream of about 530 digits</b> with diacritics over some of them, transcribed on the "
     "page and imaged on Gallica. The problem is segmentation into one-, two- and three-digit units before any substitution can be scored, the same "
     "step that beat the Vatican letter here. The Italian plaintext and the known sibling keys give the vocabulary. Added September 2026, not yet attempted."),

    ("Armstrong to Madison, 20 February 1808: the disputed contest solution", "1808",
     "armstrong.html", "", "adjudication", "md", "medium",
     "A different code from the postscript solved on this site, and the subject of a 2025 contest whose published solution has been disputed. The roll 13 "
     "frames fetched for the postscript cover this letter too, and thirty-nine of them are down and unread. The job is the Urquhart kind: rebuild the "
     "claimed key from the frames, score it against the code groups and against a shuffled control, and say whether it holds. Not yet started."),

    ("Louis XIV to the Duke of Chaulnes in Rome", "1690",
     "http://www.traces-ecrites.com/expositions/louis-xiv-du-soleil-a-leclipse/laffaire-de-la-regale/", "", "low", "lo", "medium",
     "Instructions of 10 July 1690 in a code running to at least 535, partly transcribed on Tomokiyo's page, with a Cipherbrain thread from 2019 that "
     "started and never concluded. A large nomenclator in a single letter is not attackable ciphertext-only; what can be done is to finish the thread's "
     "work, fix which groups the clear text and Louis XIV's other codes of 1690 pin down, and record how much stays open. Not yet started."),

    ("Japanese telegram decoded by Yardley", "c.1920",
     "https://cryptiana.web.fc2.com/code/yardley.htm", "", "partial", "lo", "not started",
     "Yardley printed the plaintext, so the scheme is attackable, but Japanese diplomatic traffic of 1920 ran on codebooks. One message can only "
     "recover the entries it happens to use, so a complete answer is ruled out by construction."),
]

ATTEMPTED = [
    ("Feuqui&egrave;res to Catinat, Pignerol, 25 January 1691", "1691",
     "https://github.com/dbourdeau/cyphersolver/tree/main/feuquieres", "", "not solved, design fixed", "lo",
     "<b>Attempted September 2026.</b> The 1819 <i>M&eacute;moires de Catinat</i> print the 418 groups; collated with the Munich page images "
     "(three corrections to Tomokiyo&rsquo;s copy). The editor says what it is: Feuqui&egrave;res concerting the surprise of Veillane fixed for "
     "27 January, and Catinat&rsquo;s own memoir for the operation survives as a crib. The code is a two-part &ldquo;petit chiffre&rdquo; of at "
     "most 366 entries, letters below 100, no column structure. Same size class as Chaulnes and the same wall: on a matched control every "
     "objective prefers fluent nonsense to the true key, and giving the solver 60&nbsp;% of the code completes only 63&nbsp;% of the rest. "
     "Bazeries&rsquo; 1893 book, read in full, confirms he deciphered it and that the petit chiffre of 1691 had 367 groups, but prints "
     "neither the text nor the table. The reading is in his papers at the Service historique de la D&eacute;fense; that, or a second letter in "
     "the code, would open it. <a href=\"https://github.com/dbourdeau/cyphersolver/blob/main/feuquieres/NOTES.md\">Notes &rarr;</a>"),

    ("ADFGVX residue of the Eastern Front", "1918", "adfgvx.html", "top 50",
     "9 solved, 3 partial, 10 open", "md",
     "Not unbroken ciphers: Lasry and colleagues published the keys, and the twenty-two are mutilated transmissions. <b>Second session, "
     "September 2026.</b> The 2017 comment thread, read in full, had already solved nine and partly read three, by Norbert's rule of two block "
     "edits of up to five letters; Lasry's unpublished <b>sixteenth key</b> (CHI, 13 November) is rebuilt here and added to the fifteen. The table "
     "nobody published is now in the notes. Norbert's method, reimplemented with a German quadgram model, re-derives seven of the solved pages "
     "blind. On the ten never read (73, 152, 153 twice, 158, 170, 176b, 189, 198, 217) it finds nothing with any key, the CHI key fails on the two "
     "page-153 messages, and a key-free transposition attack fails its own 224-letter planted control. They need the Childs originals or a key "
     "that was never in the corpus. <a href=\"adfgvx.html\">Full write-up &rarr;</a>"),

    ("Huang Xing telegram, the scheme corrected from the frames", "1916", "huangxing.html", "", "scheme found, corrected", "md",
     "<b>Second session.</b> Frame 0247 read at 500 dpi gives a 46-character plaintext, and one superfluous kana at position 106 turns out to have "
     "hidden the repeats: with it dropped, &#34892; three times, &#36895; twice and &#38651; twice are <b>identical kana triples</b>. So the code is "
     "deterministic and the vowel is not a free homophone, which overturns the first reading; the seven row collisions are different characters. A "
     "row-to-digit permutation test against telegraph-code order is at chance. 42 codebook entries recovered; the kana-to-digit table needs a second "
     "telegram. <a href=\"huangxing.html\">Write-up, corrected &rarr;</a>"),

    ("Regent Moray to John Wood, the Scottish ambassador in London", "1568",
     "https://github.com/dbourdeau/cyphersolver/blob/main/moray/NOTES.md", "", "undetermined", "lo",
     "BL Add MS 32091 f.213, 13 July 1568, <b>134 groups over 32 symbols</b> in Tomokiyo's transcription. The Catalogue of Additions says "
     "what the letter does: refuses Wood's recall and sends Border news. <b>Attempted September 2026.</b> A 5-gram Scots annealer, built from "
     "the <i>Diurnal of Occurrents</i>, the Privy Council register and Pitscottie, reads <b>five of six planted 134-letter controls</b> of the "
     "same symbol profile at 93&ndash;98%; on the letter it returns gibberish, scoring below every solved control, and English, French and "
     "Latin models do no better. No symbol behaves as a null or a word separator, Tomokiyo's variants are distinct symbols, twenty dragged "
     "cribs (the quene, Lethingtoun, Herreis&hellip;) are all rejected, and a word-code mask has no power at this length. Thirteen per cent of "
     "genuine Scots passages score below the solver's false optimum, and Border news is names, so the result is undetermined, not excluded. "
     "Needs the page, offline since the BL cyber-attack, or a second letter in the cipher."),

    ("Two anonymous letters to English Catholics in France, SP53/16 nos. 78 and 79", "1585?",
     "https://github.com/dbourdeau/cyphersolver/blob/main/sp53/NOTES.md", "", "closed: below threshold", "lo",
     "One to Mr Tempest, a priest in Paris, one to Dr Barret, president of the Rheims seminary, both endorsed by Phelippes and never read: "
     "<b>507 and 644 groups, 132 and 102 symbols</b>. <b>Attempted September 2026, two sessions.</b> The numbers in Tomokiyo's transcription are "
     "glyph labels, so these are symbol ciphers of the Mary&ndash;Castelnau class, not figure ciphers. The two letters do share a key: ten of the "
     "twenty commonest symbols are common to both against three expected by chance, and their frequency profiles correlate at 0.35 where unrelated "
     "keys give zero. So the text pools to 1151 groups, and it still does not fall: the homophonic annealer fails planted English and French "
     "controls at 507 groups and again at 1151, scoring at random-text level while the true plaintext scores twice as well. Four groups per "
     "symbol is below what ciphertext-only attacks on this class can do, as it was for Lasry on d'Avaux. The 1585&ndash;86 calendar is paywalled. "
     "Needs the page images and the SP 53/22 keys, f. 53 first."),

    ("Catokwacopa, line 29 in Latin", "1875", "https://github.com/dbourdeau/cyphersolver/blob/main/catokwacopa/NOTES.md", "top 50", "undetermined", "lo",
     "<b>Second session.</b> The exact-interleaving search rerun with a Latin vocabulary from 43 Latin Library texts. Control: line 17 returns QUI FIT "
     "first, ahead of <i>qui fuit</i>. Line 29 (<i>ereflodbr / rileohmae</i>) is junk in Latin as in English, three or four words at best; "
     "RELIGIONEM CONFIRMARE stays at eleven edits. The line is undetermined in both languages, and the Oxford reading is otherwise as audited before."),

    ("Sun Yat-sen telegram, the tail", "1916", "sunyatsen.html", "", "garble confirmed", "lo",
     "<b>Second session.</b> The received-message form re-fetched from JACAR and its second sheet read at 600 dpi: <i>xopavajejo ropezpo / ngobunibai "
     "tanaka</i>, every letter as Tomokiyo transcribed it. The garble after &#36820; is the operator's, not the transcriber's, and the three lost "
     "codes stay lost."),

    ("Armstrong: the roll 13 residue", "1808", "armstrong.html", "", "one group upgraded", "md",
     "<b>Second session.</b> The microfilm frames were re-fetched through the catalogue proxy. Frame 0190, a fully pencilled despatch of 20 July 1806 "
     "(&ldquo;a peace was signed last night between Russia and France&rdquo;), gives <b>1320 = like</b> as a reading from source, so the last clause "
     "of the postscript no longer rests on inference for that group; it also adds <i>last, night, about, look</i>. Thirty-nine more frames are down "
     "and unread; the 20 February 1808 letter is untouched."),

    ("Urquhart octastich", "17th c.", "https://github.com/dbourdeau/cyphersolver/blob/main/urquhart/NOTES.md", "top 50", "book-cipher shape", "lo",
     "<b>Second session.</b> Measured: 272 numbers, 82 distinct, maximum 201, index of coincidence 0.021, forty per cent of values ten or less, "
     "and 31 of the distich's 32 values recur, so the two poems are one system with the shape of a word-index book cipher. Not attackable without "
     "the key text, and nobody has said where the octastich was printed."),

    ("Copenhagen cryptogram", "c.1950s", "copenhagen.html", "top 50", "not a simple substitution", "lo",
     "Three lines found behind an 1835 portrait of a Danish general, 107 characters. <b>Attempted September 2026.</b> Transcribed twice (20 and "
     "25 symbols), attacked in ten languages under six reading conventions and a word-separator hypothesis with a 5-gram annealer and dictionary "
     "re-ranking, then confirmed with 300 restarts. Nothing readable: best &minus;2.7 nats per letter, while matched controls of the same length "
     "in Danish, German, English, Latin and Swedish are recovered at 96&ndash;100% and &minus;1.4 to &minus;2.1. Either not a simple substitution "
     "of those languages, or both readings share an error only the original slip could fix. <a href=\"copenhagen.html\">Full write-up &rarr;</a>"),

    ("Scorpion letters", "1991", "scorpion.html", "top 50", "below unicity distance", "lo",
     "Two Zodiac-style cryptograms, 70 symbols with 53 distinct and 180 with 145 distinct. <b>Attempted September 2026.</b> Every S5 repeat falls "
     "at a multiple of 16; S1 shows a weak period-5 signal (p = 0.04). Both carry more key information than the English text has redundancy "
     "(249 vs 224 bits, 682 vs 576), and matched controls return fluent English at 3&ndash;13% letter accuracy, so no ciphertext-only solution can "
     "be verified. A claimed 2018 solution is consistent with the repeats but scores worse than the controls' false solutions. Needs S2&ndash;S4. "
     "<a href=\"scorpion.html\">Full write-up &rarr;</a>"),

    ("Abwehr agent Koehler's messages, New York to Berlin", "1944",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/02/19/the-top-50-unsolved-encrypted-messages-47-encrypted-messages-of-a-nazi-spy/",
     "top 50", "skipped: intractable", "lo",
     "Five messages, 924 letters, from the Dutch double agent Walter Koehler. <b>Attempted September 2026.</b> Every tractable class is excluded "
     "against controls: substitution and transposition by the index of coincidence; Vigen&egrave;re, Beaufort and autokey at every period in "
     "German, English and Dutch; a running key from book text, which would show in the letter counts (true cases gain at least 7.5 nats, these "
     "score below uniform); and <b>any Enigma</b>, because the counts are too uneven for machine output (&chi;&sup2; 57.9, p = 0.0003). What "
     "survives is a book key through a mixed alphabet table, the documented prayer-book system, or a hand one-time pad. Neither falls without "
     "the book or the FBI's plaintexts. The attempt also corrects one letter of the circulating text."),

    ("Censorship manual steganograms", "WW2",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/05/03/the-top-50-unsolved-encrypted-messages-33-the-censorship-manual-steganograms/",
     "top 50", "image resolution", "lo",
     "A British censorship manual (TNA KV 2/2424) gives the plaintext of a map and a fashion drawing but not the readings. <b>Attempted "
     "September 2026.</b> The one published fragment (AATHUT &rarr; LLESFE, <i>alles fertig</i>) fixes the map's shift direction, and the "
     "exact dot-dash sequence any German wording would leave is now computed, so a reading can be checked mark by mark. The tram bands "
     "themselves are ordinary map fill; the Morse is pen marks beside them, and those are 0.1&ndash;0.3&nbsp;mm &mdash; 2&ndash;5 pixels in "
     "the best public photograph, where dots and dashes merge. Needs a 1,200&nbsp;dpi scan of pp. 14 and 17. The manual's &ldquo;French "
     "shorthand&rdquo; points to Duploy&eacute; for the signature."),

    ("Debosnys cryptograms", "1882–83", "debosnys.html", "top 50", "attempted, not solved", "lo",
     "About 1,200 glyphs in an invented script, left by a man hanged in 1883. Three passages transcribed here, 969 glyphs. The cipher poem is "
     "<b>rhyming couplets</b> &mdash; the last glyph matches within 9 of 10 couplets and across none of the boundaries &mdash; and line length and "
     "rhyme both point to a <b>French syllabary</b>. Every crib that could be tested failed against controls that would have found a hit: the poem "
     "on the same page, 7,821 couplet windows of French verse, Delille's <i>Aeneid</i>, Moore. The corpus sits at its unicity distance and a "
     "planted syllabary of the same length recovers 0%, so it falls only to a crib from his papers. <a href=\"debosnys.html\">Full write-up &rarr;</a>"),

    ("William Perwich to Lord Arlington", "1670",
     "https://www.nationalarchives.gov.uk/explore-the-collection/the-collection-blog/secret-diplomatic-message-deciphered-after-350-years/",
     "", "found solved", "md",
     "<b>Solved in October 2025</b> by Matthew Brown, and independently by Lasry, Biermann and Tomokiyo: a 20-column transposition with nulls. "
     "This entry had called it a substitution, and that was wrong — the eight q's, seven of them nulls, add 106 to the in-place chi-squared, and on "
     "the plaintext cells it is an ordinary 28. <b>Reproduced here from the transcription</b>: rows 2–21 are the columns, rows 1 and 22 are null "
     "lines, a keyless quadgram climb recovers the order, and 414 plaintext cells read out <i>“the souldiers grumble much that the king is of late "
     "growne cool towards them…”</i>. Only the nomenclator numbers remain."),

    ("Vatican Challenge, Part 5 — Farnese to Poggio", "1542",
     "vatican.html", "", "family identified", "md",
     "Identified as a polyphonic-syllabic cipher of the kind <b>Antonio Elio</b> built for Paul III's chancery — the chancery that sent this letter. "
     "Six sessions: the Meister keys verified from the page scans and excluded on structure, the letter dated from its own cleartext (15 April 1542), "
     "the sibling and relative records located in DECODE, and a unit-level attack (segmentation by EM, then annealing) shown by a matched control to "
     "fail on the segmentation step. Still unread; needs the 400 dpi images behind the DECODE login, the key in Chigi M II 49, or the clear register copy."),

    ("D’Agapeyeff cipher", "1939", ELONKA, "famous", "diagnosed", "lo",
     "196 digit pairs, and the author admitted he had forgotten his own method. Five independent lines — frequency against the author's own worked "
     "control, no transposition signal, no periodicity, repetition far below language, and the book's own null rule swept — all say near-uniform "
     "random. Consistent with a botched encipherment rather than a lost key."),

    ("Maltravers to Ormonde — read", "1634–35", "ormonde.html", "", "solved", "hi",
     "The alphabet is recovered and every spelled word reads. <b>Second session:</b> the nomenclator checked against Wentworth's own dispatches in "
     "Knowler's <i>Strafforde's Letters</i> (1739) — the King refusing to see Kildare, and the 22 December 1634 dispatch moving Ormonde for the "
     "Council in exchange for Sir Piers Crosby, with Coke's marginal answer that the warrant is enclosed. Seven of nine codes fixed; the two "
     "parties in &ldquo;what [185] hath written unto [149] concerning Crosby&rdquo; would need the key sheet."),

    ("Kaliningrad bottle post", "found 2015",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/10/17/the-top-50-unsolved-encrypted-messages-19-the-kalinigrad-bottle-post/",
     "top 50", "transcription", "lo",
     "The blocker is transcription, not cryptanalysis: it exists only as two photographs and nobody has ever published the character string. "
     "Attempted and abandoned honestly — cursive n, u, v and w are barely separable and the verso bleeds through. Two observations stand: the "
     "primed consonants are exactly the Russian palatalisation set, and the text carries dotted initialism groups that would be the natural home "
     "for Bible citations under the outstanding Synodal-Bible claim."),

    ("Colbert passages, Thurloe intercepts, D’Estaing, Le Tellier", "1653–1779",
     CRYPTIANA, "", "too short", "lo",
     "Four separate items that fail the same way. Each is a short passage — sixteen to two hundred and seventeen groups — with every known period "
     "key already tested and failing, and hill-climbing yielding fragments only. None is long enough to solve unconstrained, and the originals are "
     "not digitised."),
]

NOTCIPHER = [
    ("Voynich manuscript", "c.1420", "voynich.html", "famous",
     "<b>Adjudicated September 2026</b>, not deciphered. Six computational tests on the transliteration against eleven languages and implemented hoax "
     "generators, each re-run adversarially, plus five literature sweeps. A plain or simply enciphered European language is excluded on transliteration-"
     "robust entropy (h2 2.2&ndash;2.9 bits against a 3.3 floor); Rugg's grille and free-edit self-citation are disfavoured; a verbose or slot-template "
     "encoding and a structured meaningless text are left roughly even, with the tests that would separate them. <a href=\"voynich.html\">Full write-up &rarr;</a>"),
    ("Kryptos, passage K4", "1990", ELONKA, "famous",
     "97 characters. The plaintext was recovered from Sanborn's own papers in 2025 — explicitly not a cryptographic solve — and the archive sold at "
     "auction for $962,500. The method remains unbroken and the plaintext unpublished."),
    ("Zodiac Z13 and Z32", "1970", ELONKA, "famous",
     "Z408 fell in 1969 and Z340 in December 2020. What is left is thirteen and thirty-two symbols, far too short for any answer to be verifiable."),
    ("Dorabella cipher", "1897", ELONKA, "famous",
     "Eighty-seven characters. Wase's 2023 statistical study finds it unlikely to be monoalphabetic English or Latin at all, which undercuts most of "
     "the century of proposed solutions at the root."),
    ("WWII pigeon cipher, Bletchingley", "1942?", ELONKA, "famous",
     "135 letters. GCHQ's position is that without the codebook the message cannot be decrypted, nor any claimed solution verified."),
    ("Enigma message of 10 January 1945", "1945", CRYPTIANA, "",
     "A single message, and compute-bound. The comparable unsolved M4 messages fell only to distributed computing."),
    ("Lüderitz consular telegram", "1911", CRYPTIANA, "",
     "A five-figure codebook. One message recovers nothing without the book."),
    ("Phaistos disc, Linear A, Indus script, Rongorongo and the rest", "c.2600 BC – c.1800 BC", ELONKA, "famous",
     "Undeciphered writing systems, not concealed messages. These are problems for linguistics, and several may not encode language at all. "
     "Meroitic can be read aloud without being understood, which is the clearest illustration of the difference."),
]


def badge(b):
    return ' <span class="fam">%s</span>' % b if b else ''


def target(rank, name, date, href, b, odds, oc, eff, why, cls=''):
    r = '<span class="tg-rank">%s</span>' % rank if rank else '<span class="tg-rank tg-dash">·</span>'
    link = '<a href="%s">%s</a>' % (href, name) if href else name
    meta = '<span class="odds %s">%s</span>' % (oc, odds)
    if eff:
        meta += '<span class="eff">%s</span>' % (eff + ' effort' if eff in ('low', 'medium', 'high') else eff)
    return ('<article class="tg %s">\n  <div class="tg-l">%s</div>\n  <div class="tg-b">\n'
            '    <h3>%s<span class="tg-date">%s</span>%s</h3>\n'
            '    <div class="tg-meta">%s</div>\n    <p>%s</p>\n  </div>\n</article>\n'
            % (cls, r, link, date, badge(b), meta, why))


def build():
    out = []
    out.append('<h2 id="queue"><span class="num">02</span> Priority queue</h2>\n')
    out.append('<p>Everything open, from all three source lists, on one scale. <b>Odds</b> is the estimated chance of a full reading; '
               '<b>effort</b> is the work needed to find out. A cheap decisive test outranks an expensive long shot, so a coin-flip that '
               'resolves in an hour sits above a one-in-four that costs a week. Badged entries come from '
               '<a href="%s">Elonka Dunin\'s famous unsolved codes</a> and <a href="%s">Schmeh\'s Top 50</a>.</p>\n' % (ELONKA, T50))
    out.append('<div class="qfilter" role="group" aria-label="Filter the queue">\n'
               '  <button class="qf on" data-f="all">All <span>%d</span></button>\n'
               '  <button class="qf" data-f="live">Worth continuing <span>%d</span></button>\n'
               '  <button class="qf" data-f="done">Attempted <span>%d</span></button>\n'
               '  <button class="qf" data-f="no">Not a cipher <span>%d</span></button>\n'
               '</div>\n' % (len(LIVE) + len(ATTEMPTED) + len(NOTCIPHER), len(LIVE), len(ATTEMPTED), len(NOTCIPHER)))

    out.append('<h3 class="tier" data-t="live">Worth continuing <small>no archive access needed; ranked by odds against effort, the next step named in each</small></h3>\n')
    for i, t in enumerate(LIVE, 1):
        name, date, href, b, odds, oc, eff, why = t
        out.append(target(i, name, date, href, b, odds, oc, eff, why, 'live'))

    out.append('<h3 class="tier" data-t="done">Attempted &mdash; findings recorded <small>what was established, and what is left</small></h3>\n')
    for name, date, href, b, odds, oc, why in ATTEMPTED:
        out.append(target(None, name, date, href, b, odds, oc, '', why, 'done'))

    out.append('<h3 class="tier" data-t="no">Open, but not settleable by cryptanalysis <small>listed, not ranked</small></h3>\n')
    for name, date, href, b, why in NOTCIPHER:
        out.append(target(None, name, date, href, b, 'not tractable', 'no', '', why, 'no'))
    return ''.join(out)


def main():
    p = 'index.html'
    s = open(p, encoding='utf-8').read()
    i = s.index('<h2 id="queue">')
    j = s.index('<h2 id="blocked">')
    s = s[:i] + build() + '\n' + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('queue rebuilt: %d live, %d attempted, %d not-a-cipher' % (len(LIVE), len(ATTEMPTED), len(NOTCIPHER)))


if __name__ == '__main__':
    main()
