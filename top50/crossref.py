"""Klaus Schmeh's "Top 50 unsolved encrypted messages", cross-referenced and re-checked.

The Top 50 ran as a post series on Cipherbrain from 8 February 2017 (no. 50) to 12 April 2020
(no. 1), one article per entry. "Solved since publication" therefore means solved since that
entry's own post date, which top50.json records.

Two facts govern how the list has to be read today:

  * Cipherbrain stopped publishing on 31 December 2022 when ScienceBlogs.de closed. Schmeh is
    active at klausschmeh.net, but the Cipherbrain archive is frozen.
  * The Top 50 index page was never retro-annotated. It still describes Rivest's timelock as
    unbroken "18 years later" although Schmeh himself posted the solution in May 2019. The index
    is therefore worthless as a status source, and every entry here was checked independently.

This file holds the classification. NOTES.md holds the findings and the scoring.

Usage: python crossref.py
"""
import json

# Top 50 number -> (how the tracker already covers it, where)
COVERED = {
    49: ('done here: proved constructed rather than enciphered', 'goldbar/'),
    40: ('done here: concluded a fabrication', 'beale/'),
    34: ('the umbrella over the whole cryptiana workstream', 'TARGETS.md main table'),
    27: ('tracker #16 - and the tracker is STALE, see NOTES.md', 'ferdinand3/'),
    26: ('Elonka table: 87 symbols, many readings fit, none provable', 'TARGETS.md Elonka'),
    20: ('Elonka table: GCHQ assesses one-time pad', 'TARGETS.md Elonka'),
    4:  ('Elonka table: K4', 'TARGETS.md Elonka'),
    2:  ('Elonka section notes Z408/Z340 closed', 'TARGETS.md Elonka'),
    1:  ('Elonka table: evidence favours a constructed or glossolalic text', 'TARGETS.md Elonka'),
}

# Solved, or explained away, since its own post date. Kept separate from "still open" because a
# tracker that carries solved items as targets is worse than no tracker.
CLOSED = {
    48: 'SOLVED 2019. Bernard Fabrot finished 15 Apr 2019 by 3.5 years of sequential squaring on '
        'one consumer CPU; Cryptophage (Peffers, Ozturk, Drake, Johnson) finished 10 May 2019 on '
        'FPGAs. Verified by Rivest; capsule opened at MIT 15 May 2019. Successor puzzle CSAIL2019 '
        'is now open',
    42: 'SOLVED 20 Jan 2018 by George Lasry, confirmed by the challenge author Jean-Francois '
        'Bouchaudy. It was the last unsolved one of his 40 M-209 problems; all 40 are now solved',
    35: 'SOLVED Aug 2019 by Richard Bean: a book cipher on Francis Thompson\'s "The Hound of '
        'Heaven", found by sweeping ~37,000 Gutenberg texts. Plaintext: "A number of successful '
        'experiments of this kind would give strong evidence for survival." See NOTES.md for the '
        'residual target this leaves',
    32: 'SOLVED 2023 by Wayne Chan (Cryptologia 48(5), 2024). Not a personal cipher at all but US '
        'Army Signal Service telegraphic weather code; pinned to a single date, 27 May 1888. Why '
        'the sheets were in the dress remains unknown',
    27: 'SOLVED Oct 2017 by Thomas Ernst, in the comment thread of the Top 50 post itself. A '
        'digit-pair code on the Habsburg AEIOU motto, with each non-numeric sign encoding its '
        'count of strokes or semicircles',
    15: 'EXPLAINED Feb 2021 (Schrodel and Schmeh; Foxon, Cryptologia 2022): not a cipher. The '
        'four-letter groups are adjacent keys on a German QWERTZ typewriter, Morse practice',
    14: 'NOT A CIPHER by the author\'s own statement (Serafini, Oxford, 11 May 2009): the script '
        'is asemic. Only the base-21 page numbering was ever decoded',
    39: 'NOT A REAL CASE. An April Fools\' joke posted 1 April 2017: the ciphertext is one '
        'character, the transcription is credited to "George Fabyan", and the first murder is set '
        'in Geneva, Illinois, home of Riverbank Laboratories',
    21: 'CLOSED as a case, never a cipher. Hagen police and prosecutors closed the death in April '
        '2025 as a single-vehicle accident; investigators doubt the slip of paper ever existed',
}

# Real cryptograms, still open, but outside what cryptanalysis can settle.
NOT_TRACTABLE = {
    50: 'an artist book, 20 pages of block symbols, one copy known; may not be a cipher',
    45: 'a brute-force key-search record attempt, not a cryptanalysis problem. Verified 0 solves',
    36: 'marked letters in film credits; even the transcription is disputed',
    37: 'ten letters carved on a monument; no unique solution can be provable',
    22: '32 letter-triplets in a novel dedication, widely read as dedicatees\' initials',
    11: 'survives only in one c.1530 chronicle manuscript; the cave inscription is unverified',
    41: 'only 8 page scans released, the rest in private hands; authenticity unresolved',
    6:  'a writing system, not a concealed message. Kiraly and Tokai (Cryptologia 2018) claim a '
        'reading, endorsed by Lang, disputed by Pelling; not settled',
    5:  'the code is ~45 letters of probable initials; the man was identified as Carl Webb in 2022 '
        'but that did nothing for the text',
    10: 'a few hundred characters; FBI CRRU and the ACA both failed, and Pelling judges it private '
        'shorthand rather than a cipher',
    13: 'a modern transposition challenge; pure compute, and Parts 1-2 show 0 solves',
    4:  'K4 is 97 characters. The plaintext was recovered from Sanborn\'s papers in 2025 and sold '
        'at auction; the method remains unbroken and the plaintext is not public',
    1:  '~38,000 word-tokens and six centuries of failure; no proposed reading independently '
        'verified',
    2:  'Z13 and Z32 are 13 and 32 symbols, too short for a verifiable solution',
    20: 'GCHQ: without the codebook the message cannot be decrypted or any claim verified',
    26: '87 characters; Wase (2023) shows it is unlikely to be monoalphabetic English or Latin',
}


def main():
    rows = json.load(open('top50.json', encoding='utf-8'))
    print('Schmeh Top 50: %d entries, posted %s to %s' % (len(rows), rows[0]['posted'], rows[-1]['posted']))
    print('Cipherbrain closed 31 Dec 2022; the index page was never retro-annotated.\n')

    closed = [r for r in rows if r['n'] in CLOSED]
    nt = [r for r in rows if r['n'] in NOT_TRACTABLE]
    cov = [r for r in rows if r['n'] in COVERED]
    open_ = [r for r in rows if r['n'] not in CLOSED and r['n'] not in NOT_TRACTABLE]

    print('=== CLOSED SINCE THE LIST WAS WRITTEN (%d)' % len(closed))
    for r in closed:
        print('  %2d %-40s %s' % (r['n'], r['title'][:40], CLOSED[r['n']][:120]))

    print('\n=== OPEN BUT NOT SETTLEABLE BY CRYPTANALYSIS (%d)' % len(nt))
    for r in nt:
        print('  %2d %-40s %s' % (r['n'], r['title'][:40], NOT_TRACTABLE[r['n']][:110]))

    print('\n=== ALREADY REFERENCED IN THE TRACKER (%d)' % len(cov))
    for r in cov:
        how, where = COVERED[r['n']]
        print('  %2d %-40s %s  [%s]' % (r['n'], r['title'][:40], how, where))

    real = [r for r in open_ if r['n'] not in COVERED]
    print('\n=== OPEN, TRACTABLE, NEW TO THE TRACKER (%d)' % len(real))
    for r in real:
        print('  %2d %-44s posted %s' % (r['n'], r['title'][:44], r['posted']))


if __name__ == '__main__':
    main()
