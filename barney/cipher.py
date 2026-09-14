"""Barney–Mallory dictionary cipher (19 March 1863), CSS Harriet Lane, Galveston Bay.

STATUS: SOLVED (Aug 2026) by reddit u/offgramercy, r/codes post 1vpq87y.
  Dictionary: Webster's Primary School Dictionary, 1850 printing (HathiTrust hvd.32044086661170).
  Rule: printed page -> column -> nth displayed headword. 17/18 coordinates resolve; 113-3-85 is a
  typesetting error (column has 35 entries; entry 8 = GUN). Only remaining open item: confirm the
  original digit in Barney's manuscript letterbook (NARA RG 45, Entry I-18 644, NAID 1848146, undigitized).

Source: Official Records of the Union and Confederate Navies, Ser. I, vol. 20, p. 805.
Scheme (per Mallory's instructions to Maffitt, OR Navy vol. 1 p. 762, and Barney's N.B.):
    (page)-column-entry   column = 1, 2, or 3 ; entry counted from the top of the column.
Dictionary: "a copy of Webster's Dictionary" sent by Barney to Richmond on 23 Feb 1863
(OR Navy vol. 19 p. 844). Edition unknown.
"""

# Each group: (page, column, entry, context_before, context_after)
GROUPS = [
    (177, 2, 16, "General Magruder proposed to", "the"),
    (216, 1, 15, "proposed to [177-2-16] the", "[113-3-85] in"),
    (113, 3, 85, "the [216-1-15]", "in"),
    (29, 3, 36, "in", "[23-3-29]."),
    (23, 3, 29, "in [29-3-36]", "."),
    (163, 1, 34, "I am officially informed that", "will prevent"),
    (85, 3, 14, "will prevent", "from"),
    (115, 1, 7, "from", "."),
    (262, 3, 22, "I presume the", "will not be kept in"),
    (54, 2, 33, "will not be kept in", ","),
    (215, 2, 26, ",", "being entirely useless."),
    (149, 1, 30, "being so near", "a"),
    (156, 1, 8, "a", "the"),
    (163, 3, 40, "the", "might be"),
    (213, 2, 21, "might be", "[10-1-12]."),
    (10, 1, 12, "might be [213-2-21]", ". / Some might, if practicable, be sent"),
    (150, 3, 12, "What shall be done with the", "sent from Richmond"),
]

LETTER_TEXT = """SIR: In my last of 9th instant by Lieutenant Warley I reported that General Magruder
proposed to (177)-2-16- the (216)-1-15-(113)-3-85- in (29)-3-36-(23)-3-29. I am
officially informed that (163)-1-34- will prevent (85)-3-14- from (115)-1-7-. As my
previous suggestions are thus defeated, I presume the (262)-3-22- will not be kept in
(54)-2-33, (215)-2-26 being entirely useless. I beg leave respectfully to suggest that
being so near (149)-1-30-a (156)-1-8- the (163)-3-40 might be (213)-2-21-(10)-1-12-.
[...]
P. S.--What shall be done with the (150)-3-12- sent from Richmond in case the above
suggestion is carried out? Some might, if practicable, be sent (10)-1-12-.
N. B.--The second or middle figure indicates the column, 1st, 2d, or 3d."""

# Distinct pages we need to inspect in any candidate dictionary
PAGES = sorted({g[0] for g in GROUPS})

# Contextual expectations (hypotheses only, from Barney's 9 March letter, OR Navy vol. 19 p. 848-849):
#   (10)-1-12   'A' word; "sent ___" twice -> likely "abroad"
#   (150)-3-12  'L/M' word; "the ___ sent from Richmond" -> men / marines / officers / lieutenants
#   (262)-3-22  late-alphabet noun; "the ___ will not be kept in (54)-2-33" -> vessel / ship ... in commission
#   (29)(23)    two 'B' words forming a place: Buffalo Bayou? (Houston's waterway) -- 29 > 23 fits bu > ba
#   (213)(10)   "might be ___ ___" -> "sent abroad" (Barney's own phrase on 9 March)

if __name__ == "__main__":
    print("pages needed:", PAGES)
    for g in GROUPS:
        print(f"({g[0]})-{g[1]}-{g[2]:<3} {g[3]!r} ___ {g[4]!r}")
