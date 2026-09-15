"""The Biermann / Bosbach / Brown nomenclator for Charles I's Isle of Wight letters (2021).

Transcribed from the published reconstruction
https://scienceblogs.de/klausis-krypto-kolumne/files/2021/05/Nomenclator-Charles-I.png
(saved here as img/Nomenclator-Charles-I.png).

Structure, which is worth stating because it is what makes the reconstruction trustworthy:

  * 2-9   run h g f e d c b a  (descending)
  * 12-19 run h g f e d c b a  (descending, second homophone set)
  * 20    third homophone for h
  * 21-30 run i k l m n o p q r s  (ascending)
  * 31-40 run i k l m n o p q r s  (second set)
  * 41-49 run i k l m n o p q r    (third set), with s displaced to 51 because 50 is taken
  * 50-57 e t u w x y z            (50 = third e; 52-57 = t u w x y z)
  * 60-67 d t u w x y z            (60 = third d; 62-67 = second t u w x y z)
  * 70-77 c t u w x y z            (70 = third c; 72-77 = third t u w x y z)
  * 61, 71 extra homophones for s
  * 80 = b, 90 = a
  * nulls 1, 10, 58, 68, 69, 78, 9x, 100-107
  * words 142-615, roughly alphabetical

The period alphabet has 24 letters: i/j and u/v are each one letter, so there is no j and no v.
Entries the solvers printed in grey were never observed in the four letters; they are reconstructed
from the pattern. GREY records which those are, so a decode can be told how much it is leaning on
inference.
"""

LETTERS = {
    9: 'a', 19: 'a', 90: 'a',
    8: 'b', 18: 'b', 80: 'b',
    7: 'c', 17: 'c', 70: 'c',
    6: 'd', 16: 'd', 60: 'd',
    5: 'e', 15: 'e', 50: 'e',
    4: 'f', 14: 'f',
    3: 'g', 13: 'g',
    2: 'h', 12: 'h', 20: 'h',
    21: 'i', 31: 'i', 41: 'i',
    22: 'k', 32: 'k', 42: 'k',
    23: 'l', 33: 'l', 43: 'l',
    24: 'm', 34: 'm', 44: 'm',
    25: 'n', 35: 'n', 45: 'n',
    26: 'o', 36: 'o', 46: 'o',
    27: 'p', 37: 'p', 47: 'p',
    28: 'q', 38: 'q', 48: 'q',
    29: 'r', 39: 'r', 49: 'r',
    30: 's', 40: 's', 51: 's', 61: 's', 71: 's',
    52: 't', 62: 't', 72: 't',
    53: 'u', 63: 'u', 73: 'u',
    54: 'w', 64: 'w', 74: 'w',
    55: 'x', 65: 'x', 75: 'x',
    56: 'y', 66: 'y', 76: 'y',
    57: 'z', 67: 'z', 77: 'z',
}

# printed in grey by the solvers: inferred from the pattern, never seen in the four letters
GREY = {18, 80, 13, 32, 41, 42, 28, 38, 48, 40, 47, 64, 73, 74, 75, 57, 67, 77}

NULLS = {1, 10, 58, 68, 69, 78, 100, 101, 102, 103, 104, 105, 106, 107}
# "9x": one line of the 2 September letter ends with a truncated 9-something, taken as a null.

WORDS = {
    142: 'Argyll?', 149: 'aid', 155: 'and', 156: 'at', 157: 'as', 158: 'all',
    160: 'agreement', 164: 'are', 165: 'any',
    178: 'but', 179: 'be',
    189: 'Culpeper?', 199: 'consider', 203: 'Councell', 210: 'concerning', 211: 'could',
    216: 'cause', 217: 'con',
    236: 'defeat', 238: 'did',
    255: 'enter', 263: 'endeavour',
    275: 'find', 277: 'for', 278: 'fleet?',
    285: 'good', 299: 'great', 300: 'go',
    325: 'have', 328: 'her', 330: 'had', 332: 'hope', 334: 'help?',
    339: 'im', 340: 'I', 345: 'in', 346: 'if', 347: 'is', 350: 'ing', 351: 'ion', 352: 'ill',
    362: 'know', 364: 'kingdom',
    373: 'London', 378: 'lyke',
    404: 'match', 405: 'may', 406: 'me', 410: 'my', 411: 'made', 412: 'more',
    428: 'not', 429: 'now', 430: 'near', 432: 'no', 434: 'none',
    442: 'opinion', 447: 'of', 448: 'on', 451: 'one', 453: 'or', 455: 'order', 456: 'offer',
    471: 'pro', 475: 'Parliamentarians', 485: 'party',
    508: 'reason', 509: 'regard', 516: 'request',
    528: 'Scots', 530: 'Scotland', 536: 'send', 543: 'shall',
    554: 'treat', 557: 'to', 558: 'these', 559: 'them', 560: 'this', 561: 'that',
    562: 'thought', 563: 'the', 564: 'thing',
    572: 'unto',
    583: 'Newport', 593: 'wai', 595: 'would', 598: 'was', 600: 'with',
    602: 'which', 603: 'why', 609: 'will', 613: 'yet', 614: 'your', 615: 'you',
}

# highest letter code, lowest word code: the boundary of the two halves
LETTER_MAX = 107
WORD_MIN = 142


def decode_token(n):
    """Return (text, kind). kind is 'letter', 'null', 'word' or 'unknown'."""
    if n in NULLS:
        return ('', 'null')
    if n in LETTERS:
        return (LETTERS[n], 'letter')
    if n in WORDS:
        return (WORDS[n], 'word')
    return ('[%d]' % n, 'unknown')


def decode(seq, sep='-'):
    out, kinds = [], []
    for n in seq:
        t, k = decode_token(n)
        kinds.append(k)
        if k != 'null':
            out.append(t)
    return sep.join(out), kinds


def letters_only(seq):
    """The sub-sequence of codes in the single-letter range, mapped to letters.

    This is the part of a nomenclator that can be scored against a language model: word codes
    expand to variable-length strings and would swamp the statistics, whereas letter codes give
    one plaintext letter each.
    """
    return ''.join(LETTERS[n] for n in seq if n in LETTERS)
