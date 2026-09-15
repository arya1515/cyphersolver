"""Structural analysis of the 24 cipher groups in Stepney -> Manchester, Vienna 23 Mar 1702
(Yale Osborn fc37 Box 8 f.40 = DECODE R2864), and a test against the partial
THE=454 "Duke of Manchester's cypher" (DECODE R2858) as published on cryptiana.

Run:  python analyze.py  > analyze_out.txt   (UTF-8)
"""
from collections import Counter

P1 = [836, 468, 445, 242, 233, 55, 44, 370, 30, 325, 576, 246, 388, 380]
P2 = [418, 847, 398, 370, 360, 731, 102, 271, 632, 413]
ALL = P1 + P2

# ---------------------------------------------------------------------------
# Partial THE=454 key, assembled from the decipherments Tomokiyo prints for
# DECODE R2859/2860/2865/2866 (cryptiana glorious.htm, saved in cryptiana/).
# Null rule (marginal note on R2858): numbers <3, >2343, ending in 5 or 9,
# and 516-617 are blanks.  Printed entries 3-2342.
# ---------------------------------------------------------------------------
KEY454 = {
    # letters (3 - c.160, alphabetical)
    4: 'a', 6: 'a', 7: 'a', 10: 'a', 13: 'c?', 20: 'c?', 21: 'd?', 28: 'd', 33: 'd',
    36: 'e', 37: 'e', 38: 'e', 40: 'e', 42: 'f', 48: 'f/e', 72: 'k', 73: 'l', 74: 'l',
    87: 'n', 88: 'n', 93: 'o', 112: 'r', 116: 'r', 117: 'r',
    120: 's', 121: 's', 122: 's', 123: 's', 126: 's', 127: 's', 128: 's', 130: 't', 146: 'w',
    # syllables, first series (c.164 - c.320)
    164: 'as', 172: 'be', 180: 'ce', 188: 'de', 194: 'ed', 197: 'er', 206: 'fo', 211: 'ge',
    217: 'he', 230: 'ke', 231: 'ki', 233: 'la', 240: 'ma', 241: 'me', 242: 'mi', 254: 'of',
    272: 'ra', 273: 're', 276: 'ro', 281: 'se', 283: 'so', 284: 'su', 286: 'st', 292: 'ti',
    293: 'to', 299: '-', 300: 'ue', 304: 'wa', 307: 'wi', 316: 'ye',
    # syllables / short words, second series (c.320 - 515)
    326: 'an', 327: 'at', 340: 'ch', 347: 'do', 348: 'du', 356: 'en', 372: 'gr', 377: 'his',
    384: 'is', 394: 'ly', 428: 'que', 453: 'th', 454: 'the', 466: 'war', 468: 'way',
    476: 'yet', 483: 'and', 486: 'all', 487: 'are', 500: 'con',
    # words (618 - 2342)
    622: 'for', 631: 'gon', 642: 'in', 656: 'like', 661: 'may', 662: 'men', 667: 'nt',
    670: 'not', 673: 'on', 711: 'the', 716: 'that', 724: 'who', 736: 'you', 751: 'but',
    761: 'court', 790: 'give', 791: 'gain', 797: 'hath', 798: 'him', 804: 'ing', 823: 'move',
    842: 'prize', 870: 'take', 888: 'writ', 908: 'any', 1003: 'Prince', 1024: 'state',
    1034: 'there', 1036: 'thing', 1038: 'ver', 1047: 'what', 1128: 'the King', 1191: 'turn',
    1232: 'brought', 1256: 'expect', 1276: 'have not', 1316: 'other', 1333: 'resolu',
    1340: 'Scot', 1341: 'secur', 1401: 'concern', 1402: 'consider', 1403: 'Captain',
    1454: 'little', 1456: 'letter', 1621: 'Majesty', 1641: 'present', 1724: 'command',
    1854: '-', 1900: 'equal', 2291: '-',
}


def is_null_454(n):
    return n < 3 or n > 2343 or n % 10 in (5, 9) or 516 <= n <= 617


def bracket(n):
    """Nearest known entries below/above n in the THE=454 partial key."""
    lo = max((k for k in KEY454 if k < n), default=None)
    hi = min((k for k in KEY454 if k > n), default=None)
    f = lambda k: f"{k}={KEY454[k]}" if k is not None else '?'
    return f"{f(lo)} .. {f(hi)}"


def main():
    print("=== Stepney -> Manchester, Vienna 23 March 1702: 24 cipher groups ===")
    print("P1 (after 'Ratification of our article agst ye P.P. of W.'):", P1)
    print("P2 (after 'of what Consequence it would be to have'):        ", P2)
    print()
    lens = Counter(len(str(n)) for n in ALL)
    print(f"group lengths: {dict(lens)}  (2-digit: {[n for n in ALL if n < 100]})")
    print(f"range {min(ALL)}-{max(ALL)}; distinct {len(set(ALL))}/{len(ALL)}; "
          f"repeated: {[n for n, c in Counter(ALL).items() if c > 1]}")
    print("last-digit distribution:", dict(sorted(Counter(n % 10 for n in ALL).items())))
    print("first-digit distribution:", dict(sorted(Counter(int(str(n)[0]) for n in ALL).items())))
    print("Ranges: 0-160 (letters?)  :", sorted(n for n in ALL if n < 160))
    print("        160-515 (syllables):", sorted(n for n in ALL if 160 <= n < 516))
    print("        516-617            :", sorted(n for n in ALL if 516 <= n <= 617))
    print("        618+ (words?)      :", sorted(n for n in ALL if n > 617))
    print()
    print("Observations:")
    print(" * No group above 847, although THE=454-type keys run to 2342 and Vernon's 1700 letter")
    print("   in THE=454 uses 1003..1900 freely -> either a smaller nomenclator (<~900 entries)")
    print("   or the passage happens to use only letters/syllables/low words.")
    print(" * Three 2-digit groups (55 44 30) + 102 cluster as 'letters'; 233-500 as 'syllables';")
    print("   632-847 as 'words' -- same three-tier architecture as the printed templates")
    print("   (letters / syllables / words) used by the Secretaries' office c.1690-1710.")
    print(" * 370 recurs in both passages (only repeat) -> common syllable/word.")
    print(" * Sequence '55 44 370 30' = letter letter syl letter: probably a spelled-out word/name.")
    print()

    print("=== Test: apply THE=454 (R2858) null rule and partial key ===")
    for name, P in (("P1", P1), ("P2", P2)):
        nulls = [n for n in P if is_null_454(n)]
        print(f"{name}: nulls under THE=454 rule = {nulls}  ({len(nulls)}/{len(P)})")
        out = []
        for n in P:
            if is_null_454(n):
                out.append(f"{n}[NULL]")
            elif n in KEY454:
                out.append(f"{n}({KEY454[n]})")
            else:
                out.append(f"{n}<{bracket(n)}>")
        print("   ", ' '.join(out))
    print()
    print("Reading of P1 under THE=454: '[836: move..prize] way [null] mi la [null] f [370: en..gr] d")
    print("  [null] [null] [246: mi..of] [388: is..ly] [380: his..is]' -> 'way ... mi la f ... d' is not")
    print("  English; 44 falls in the e/f block so 'Mila-n' is impossible. P2: 'to have [418] [847]")
    print("  [398] [370] [360] [731: the..you] p [271: of..ra] [632: gon..in] [413]' -> no anchor word.")
    print("  4/14 nulls in P1 vs 0/10 in P2 also looks unlike genuine null sprinkling.")
    print("  => THE=454 is NOT the key of this letter (agrees with Tomokiyo, who lists R2864 as the")
    print("     only Manchester letter he could not read with THE=454).")
    print()
    print("=== Cribs from context (cannot be verified without the key) ===")
    cribs = [
        ("P1", "follows 'the Emperor's Ratification of our article against the pretended Prince of Wales'",
         ["which comes very late / after much delay", "which ought to have been done long ago",
          "with an alteration / in a form which will not be approved",
          "but not that of the States / the Dutch"]),
        ("P2", "follows 'of what Consequence it would be to have' and precedes 'Our project may lye by ... "
               "expedition of Naples is layd aside'",
         ["it (the ratification) dispatched / exchanged in time", "a squadron in the Mediterranean early",
          "the (English/Dutch) fleet in Italy", "the Emperor's troops in Italy before the French"]),
    ]
    for tag, ctx, cands in cribs:
        print(f"{tag}: {ctx}")
        for c in cands:
            print("    -", c)
    print()
    print("Verdict: 24 groups, one repeat, unknown two-part nomenclator with nulls: not breakable")
    print("statistically. Needs the key (Stepney's cipher with the Secretary's office, copy asked")
    print("for by Manchester Aug 1701) or Stepney's letter-book plaintext.")


if __name__ == '__main__':
    main()
