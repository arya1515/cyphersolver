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
    ("Debosnys cryptograms", "1882–83",
     "https://scienceblogs.de/klausis-krypto-kolumne/2020/01/06/the-top-50-unsolved-encrypted-messages-3-the-debosnys-cryptograms/",
     "top 50", "low", "lo", "high",
     "Four passages written in an Essex County jail before the writer was hanged. <b>Solve attempted September 2026, not solved.</b> The "
     "twenty-line cipher poem and the No. 10 block are now transcribed (378 glyphs). The poem is rhyming couplets by its final glyphs, "
     "and line length and rhyme behaviour both point to a <b>French syllabary</b> — English syllables would match the rhymes with "
     "probability 3&thinsp;×&thinsp;10<sup>−4</sup>. Every crib failed against controls that prove the tests could see a hit: the clear "
     "poem under the No. 10 block, 7,821 couplet windows of French verse, Delille's <i>Aeneid</i>, Moore, and a letter-monogram reading. "
     "What is left needs the other ~800 glyphs transcribed and a wider search of popular French verse."),

    ("Censorship manual steganograms", "1943",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/05/03/the-top-50-unsolved-encrypted-messages-33-the-censorship-manual-steganograms/",
     "top 50", "even", "md", "low",
     "Already half solved: readers recovered Morse hidden in the pen strokes of a map of Amsterdam and matched it to the manual's own published "
     "gloss. The residue is unusually well specified — the Morse in the second drawing, and the exact German wording of the first. Originals are at "
     "the National Archives in KV 2/2424, so the material is obtainable."),

    ("Abwehr agent's messages, New York to Berlin", "1944",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/02/19/the-top-50-unsolved-encrypted-messages-47-encrypted-messages-of-a-nazi-spy/",
     "top 50", "even", "md", "medium",
     "Nine hundred and twenty-one letters over five messages — a decent corpus by this list's standards. The system is unknown and Enigma variants "
     "were exhaustively excluded in the original thread. Published as an image only, so a transcription comes first."),

    ("Telegram from Switzerland, “BLUME SALAMANCA”", "1937",
     CRYPTIANA, "", "low", "lo", "low",
     "Never attempted here and cheap to try. Salamanca was Franco's headquarters, so the Spanish Civil War supplies cribs, and the coincidence "
     "index points at transposition rather than a code. Only two short messages, which caps the odds."),

    ("Copenhagen cryptogram", "c.1835",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/08/17/the-top-50-unsolved-encrypted-messages-23-the-copenhagen-cryptogram/",
     "top 50", "low", "lo", "low",
     "Found behind an 1835 painting of a Danish general and sent to the American Cryptogram Association, which never broke it or even wrote it up. "
     "A hundred and seven characters over twenty-five symbols, almost certainly simple substitution and almost certainly <b>not English</b>. That "
     "makes it a multilingual reading problem rather than a cryptanalytic one, which is the angle nobody has pushed."),

    ("Scorpion letters", "1991",
     "https://scienceblogs.de/klausis-krypto-kolumne/2018/01/30/the-top-50-unsolved-encrypted-messages-12-the-sccorpion-letters/",
     "top 50", "low", "lo", "medium",
     "About two hundred and fifty symbols over two homophonic ciphers in Zodiac style; the remaining letters are withheld by law enforcement. The "
     "Z340 break showed what searching transposition alongside substitution can do, but this is a quarter of that length."),

    ("Japanese telegram decoded by Yardley", "c.1920",
     "https://cryptiana.web.fc2.com/code/yardley.htm", "", "partial", "lo", "low",
     "Yardley printed the plaintext, so the scheme is attackable, but Japanese diplomatic traffic of 1920 ran on codebooks. One message can only "
     "recover the entries it happens to use, so a complete answer is ruled out by construction."),
]

ATTEMPTED = [
    ("William Perwich to Lord Arlington", "1670",
     "https://www.nationalarchives.gov.uk/explore-the-collection/the-collection-blog/secret-diplomatic-message-deciphered-after-350-years/",
     "", "found solved", "md",
     "<b>Solved in October 2025</b> by Matthew Brown, and independently by Lasry, Biermann and Tomokiyo: a 20-column transposition with nulls. "
     "This entry had called it a substitution, and that was wrong — the eight q's, seven of them nulls, add 106 to the in-place chi-squared, and on "
     "the plaintext cells it is an ordinary 28. <b>Reproduced here from the transcription</b>: rows 2–21 are the columns, rows 1 and 22 are null "
     "lines, a keyless quadgram climb recovers the order, and 414 plaintext cells read out <i>“the souldiers grumble much that the king is of late "
     "growne cool towards them…”</i>. Only the nomenclator numbers remain."),

    ("Catokwacopa newspaper advertisements", "1875",
     "https://klausschmeh.net/the-catokwacopa-cryptograms-a-150-year-old-mystery/",
     "top 50", "readings audited", "md",
     "Two <i>Standard</i> advertisements whose lines are two order-preserving halves of one abbreviated phrase. The disputed question was how much "
     "the omission rule lets a reader invent, so it was measured. The pairing is structural (no random re-pairing in 100,000 fits the lengths). "
     "Consonant-initial words always start in the 8 May half. An open-vocabulary search forces DYING DECLARATION, REPEATED and OLD CAP BROKE AT "
     "CORNER LEFT INSTEAD, finds exact CHANGE ADOPTED and HOLIDAYS EXAMINE where published readings needed misprints, and shows MASTER PUPIL and "
     "SIGNED are emendations. Decisively, of 1,645 names only CONINGTON, JOWETT, SHIRLEY and HERTFORD fit their frames: the Oxford reading is right "
     "in outline. Lines 9, 12, 23 and 29 are not decided by the letters."),

    ("ADFGVX residue of the Eastern Front", "1918",
     "https://scienceblogs.de/klausis-krypto-kolumne/unsolved-adfxvx-messages-from-world-war-i/", "top 50",
     "1 of 22 read", "md",
     "Not unbroken ciphers at all — Lasry and colleagues published the keys, and these twenty-two are mutilated transmissions against them. "
     "Built a working decoder, settled the transposition convention the published keys leave ambiguous, and repaired three keys whose squares the "
     "source PDF had collapsed into dashes. <b>Page 100 reproduced from scratch</b> at score 140.7 where nothing else clears 7. Page 132's key "
     "identified — <i>WIEDERHOLE</i> and <i>TELEG</i> emerge unprompted. The other twenty need heavier repair than two insertions."),

    ("Vatican Challenge, Part 5 — Farnese to Poggio", "1542",
     "vatican.html", "", "family identified", "md",
     "Identified as a polyphonic-syllabic cipher of the kind <b>Antonio Elio</b> built for Paul III's chancery — the chancery that sent this letter. "
     "Five independent measurements match that design, including a doubled-digit suppression that recovers the chancery's own written rule against "
     "doubling consonants. Five model classes excluded, two against matched controls the same code solves. Still unread; needs the key or the "
     "manuscript's word division."),

    ("D’Agapeyeff cipher", "1939", ELONKA, "famous", "diagnosed", "lo",
     "196 digit pairs, and the author admitted he had forgotten his own method. Five independent lines — frequency against the author's own worked "
     "control, no transposition signal, no periodicity, repetition far below language, and the book's own null rule swept — all say near-uniform "
     "random. Consistent with a botched encipherment rather than a lost key."),

    ("Maltravers to Ormonde — the last nine codes", "1634–35", "ormonde.html", "", "partial", "md",
     "The alphabet is recovered and every spelled word reads. The nine nomenclator codes still resting on context need either the real key or more "
     "ciphertext, and neither is online."),

    ("Thomas Urquhart’s encrypted poems", "17th c.",
     "https://scienceblogs.de/klausis-krypto-kolumne/2017/06/30/the-top-50-unsolved-encrypted-messages-28-thomas-urquharts-encrypted-poems/",
     "top 50", "provenance", "lo",
     "The structure of the August 2026 claim checks out — Wilcock records thirty-two proquiritations from petitioners hiding behind their initials, "
     "and the distich is two lines of thirty-two. But the provenance objection holds on an independent copy: the 1653 book ends in an errata table "
     "and contains <b>zero</b> runs of eight or more numbers, as does Wilcock 1899. The ciphertext could not be located in the source it is said to "
     "come from."),

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
    ("Voynich manuscript", "c.1420", ELONKA, "famous",
     "~38,000 word-tokens and six centuries of failure. No proposed reading has been independently verified, and the competing hypotheses — natural "
     "language in invented script, constructed language, cipher, hoax — remain unresolved."),
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
        meta += '<span class="eff">%s effort</span>' % eff
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
               '  <button class="qf" data-f="live">Attack now <span>%d</span></button>\n'
               '  <button class="qf" data-f="done">Attempted <span>%d</span></button>\n'
               '  <button class="qf" data-f="no">Not a cipher <span>%d</span></button>\n'
               '</div>\n' % (len(LIVE) + len(ATTEMPTED) + len(NOTCIPHER), len(LIVE), len(ATTEMPTED), len(NOTCIPHER)))

    out.append('<h3 class="tier" data-t="live">Attack now <small>ranked by odds against effort</small></h3>\n')
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
