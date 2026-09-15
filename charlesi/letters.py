"""The Isle of Wight cipher passages of 1648.

Source: https://cryptiana.web.fc2.com/code/charlesii.htm section "4. From the Isle of Wight (1648)"
(saved here as charlesii.htm).

The 22 May text has been checked character by character against the 1795 printing itself - John
Albin, "A new, correct, and much-improved history of the Isle of Wight", p.237, Internet Archive
item bim_eighteenth-century_a-new-correct-and-much_albin-john_1795, leaf 258, saved here as
img/albin_leaf258.jpg. Every group agrees with Tomokiyo. That matters because the strongest
structural result in this directory (nearrepeat.py) turns on three digits.

Albin also prints, on the facing page 236, a letter of 16 May 1648 to the same man which neither
cryptiana nor the Cipherbrain thread uses. It is almost entirely in clear and contains exactly one
cipher group, which the King's own postscript identifies as a person's name. That makes it the only
crib anywhere in this correspondence, so it is included below.

Each letter is a list of (cleartext, codes) chunks in reading order, so the surrounding plaintext -
which is often the most useful crib available - stays attached to the passage it introduces.

Two were solved by Biermann, Bosbach and Brown in 2021 and are kept here as positive controls.
Two remain unread. A fifth and sixth letter (2 September, 6 November) are also solved but Tomokiyo
prints only images of them, not transcriptions, so they are not included.
"""

# ---------------------------------------------------------------- solved (controls)

OCT3 = {
    'date': '1648-10-03',
    'to': 'Prince Charles',
    'status': 'solved 2021 (Biermann, Bosbach, Brown)',
    'source': 'Vindication',
    'chunks': [
        ("Yours by Oudart I received upon Sunday last, and am very well satisfied with your "
         "account, and his relation; only I somewhat wonder that you give me no account of my "
         "last Letter, which was of the 6th of September our Stile, wherein I gave you a "
         "conditional advice concerning", [563, 528, 456]),
        (", of which you was then more able to judge than I; but now being at some more freedom, "
         "I hope shortly to give you a reasonable clear advice: .... And now I must command you "
         "to answer me freely to a Question, (I am confident that you will not dissemble with "
         "me) which is, if",
         [615, 211, 179, 217, 52, 5, 25, 62, 557, 24, 9, 29, 39, 56, 1, 34, 19, 6, 90, 34, 26,
          347, 15, 23, 33, 50, 345, 509, 447, 328, 27, 5, 49, 71, 448, 340, 275, 350, 328, 345]),
        ("(", [36, 563, 29, 1, 39, 5, 51, 37, 15, 7, 72, 61]),
        (")", [10, 9, 285, 404, 277, 615]),
        ("; to this I would have your speedy resolution, for I am told that lost time now in it, "
         "will not be recovered, ....", []),
    ],
}

NOV7 = {
    'date': '1648-11-07',
    'to': 'Prince Charles',
    'status': 'solved 2021 (Biermann, Bosbach, Brown)',
    'source': 'Original Letters',
    'chunks': [
        ("Let none decypher this but your selfe, or my Lord Culpeper. ....I must desyre of you an "
         "account of the receipt of my former Letters, to witt fyve in October, besydes one "
         "yesterday; in some of which I gave you an advice",
         [447, 536, 350, 563, 278, 557, 334, 179, 350, 613, 447, 563, 51, 9, 24, 5, 442]),
        ("as allso",
         [210, 410, 26, 54, 15, 25, 516, 557, 50, 61, 7, 9, 27, 5, 10, 447, 602, 429, 340, 325,
          299, 332]),
        ("For other things I refer you to my former Letters, and to the obedience of your "
         "Mother's commands. So God bless you, and send you perfect healthe and prosperity", []),
    ],
}

# ---------------------------------------------------------------- unread

MAY22 = {
    'date': '1648-05-22',
    'to': 'Edward Worsley ("Z")',
    'status': 'UNREAD',
    'source': 'History of the Isle of Wight (1795) p.237',
    'chunks': [
        ('Z: / I am verrie well satisfied with the discreete & carefull account that you have '
         'given me of my Business & particularly that you did',
         [208, 343, 294, 74, 9, 45, 86, 18, 96, 1, 40, 82, 395, 380, 2, 20, 3, 230, 388, 45, 36,
          4, 11, 7, 43, 31, 62, 270, 248]),
        ('now it will be', [36, 19, 5, 32, 39, 12, 37, 8, 97]),
        ('I desyre you to enquyre whether or not',
         [396, 213, 355, 204, 28, 21, 363, 257, 64, 36, 46, 9, 32, 395, 42, 35, 14, 53, 38, 23,
          18, 50, 88]),
        ('but for this',
         [236, 308, 267, 356, 282, 96, 62, 86, 205, 17, 356, 66, 50, 97, 206, 231, 248, 38, 1,
          20, 2, 230, 388, 46, 36, 257, 208, 86, 25, 268, 8, 3, 50, 240, 6, 51, 248, 416, 303,
          78, 9, 68, 45]),
        ('in the meane Tyme lett me know', [379, 4, 28, 5, 348, 354]),
        ('the ....', [206, 18]),
        ('So I rest Your asseured Frend, J.', []),
    ],
}

AUG1 = {
    'date': '1648-08-01',
    'to': 'Prince Charles',
    'status': 'UNREAD',
    'source': 'Original Letters',
    'chunks': [
        ('I had written to you sooner had I knowen where you had been; and particularly that '
         'express which, upon Saterday last, I directed to your brother I had sent to you, but '
         'I thought that',
         [379, 361, 185,
          28, 20, 329, 592, 60, 93, 5, 214, 126, 379, 90, 37,
          1, 258, 6, 2, 212, 370, 196, 379, 245, 339, 363,
          329, 165, 246, 16, 50, 212, 196, 444, 149, 13, 44,
          32, 14, 26, 10, 78, 43, 65, 329, 331, 380, 17, 49,
          29, 338, 77, 102, 365, 5, 20, 532, 9, 41, 282, 212,
          202, 379, 371, 182, 339, 337, 212, 140, 30, 74, 5,
          50, 60, 107, 381, 214, 339, 93, 85, 6, 23, 220, 78,
          57, 152, 5, 65]),
        ('I command you to doe nothing, whether it concerns War or Peace, but with the advice of '
         'your Councell; and that you be constant to those grounds of Religion and Honor which '
         '.... [PS] This Cypher which now I write in, is that which was sent you by the noble '
         'frend who conveis this Letter to you from me.', []),
    ],
}

# the manuscript line breaks of the 1 August letter as Tomokiyo prints them, kept because
# line-final code groups are sometimes informative about where a scribe broke a word
AUG1_LINES = [
    [379, 361, 185],
    [28, 20, 329, 592, 60, 93, 5, 214, 126, 379, 90, 37],
    [1, 258, 6, 2, 212, 370, 196, 379, 245, 339, 363],
    [329, 165, 246, 16, 50, 212, 196, 444, 149, 13, 44],
    [32, 14, 26, 10, 78, 43, 65, 329, 331, 380, 17, 49],
    [29, 338, 77, 102, 365, 5, 20, 532, 9, 41, 282, 212],
    [202, 379, 371, 182, 339, 337, 212, 140, 30, 74, 5],
    [50, 60, 107, 381, 214, 339, 93, 85, 6, 23, 220, 78],
    [57, 152, 5, 65],
]

SOLVED = [OCT3, NOV7]
UNREAD = [MAY22, AUG1]
ALL = SOLVED + UNREAD


def codes(letter):
    out = []
    for _, cs in letter['chunks']:
        out.extend(cs)
    return out


def name(letter):
    return '%s to %s' % (letter['date'], letter['to'])
