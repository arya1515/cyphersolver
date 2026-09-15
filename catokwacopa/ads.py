"""The two 'W.' advertisements, The Standard, p.1 col.2, 8 and 20 May 1875.

Text as checked against the British Newspaper Archive originals by Thomas Ernst (klausschmeh blog,
comments #24-#25, 27 July 2018); the circulating 2005/2015 transcriptions have a dozen errors
(Hfsclam for Hrsclam, 139 for 138, Eftdorshpxn for Etfdorshpxn, Tavlysdinlge for Tsvlysdinlge, ...).
"""
import re

AD1 = ("W. Str 53. Catokwacopa. Olcabrokorlested. Coomemega. Sesipyyocashostikr. Rep.– Itedconlec mistrl. "
       "Hrsclam 54. 3 caselcluchozamot. 1. 6. 9. Mopredisco. Contoladsemot. Iadfilisat. Qft. Cagap. "
       "Balmnopsemsov. Ap. 138.–Hodsam 55, 6. Iopotonrogfimsecharsenr. Tolshr. Itedjolec. mistrl.–Ding "
       "Declon.–Ereflodbr.")
AD2 = ("W. –Umem 18. Poayatlgerty. Dpeatcnrftin. Nvtinrdn. Dmlurpinrtrcamnr. Etd. – Atndngtnsurs. Otenpu.–"
       "Etfdorshpxn. 18. Ndtsfindseseo. Cotegr Tsvlysdinlge. Ngtndusdcndo. Edrstneirs. Ui. Ndted. "
       "Iolapstedttoc. A.P. 138.–Yxn. 18. 18. Wtubtrfftrstendinhofsvmnr. Dily.–Atdwtsurs. Oatvpu.–Y Arati. "
       "Rileohmae.–This will be intelligible if read in connection with my communication published in this "
       "column on the 8th inst.")

# Ernst's 29 lines (2018 comment #29), which follow the printed word and punctuation divisions.
PAIRS = [
    ('str', 'umem'), ('53', '18'), ('catokwacopa', 'poayatlgerty'), ('olcabrokorlested', 'dpeatcnrftin'),
    ('coomemega', 'nvtinrdn'), ('sesipyyocashostikr', 'dmlurpinrtrcamnr'), ('rep', 'etd'),
    ('itedconlec', 'atndngtnsurs'), ('mistrl', 'otenpu'), ('hrsclam', 'etfdorshpxn'), ('54.3', '18'),
    ('caselcluchozamot', 'ndtsfindseseo'), ('1.6.9', 'cotegr'), ('mopredisco', 'tsvlysdinlge'),
    ('contoladsemot', 'ngtndusdcndo'), ('iadfilisat', 'edrstneirs'), ('qft', 'ui'), ('cagap', 'ndted'),
    ('balmnopsemsov', 'iolapstedttoc'), ('ap138', 'ap138'), ('hodsam', 'yxn'), ('55.6', '18.18'),
    ('iopotonrogfimsecharsenr', 'wtubtrfftrstendinhofsvmnr'), ('tolshr', 'dily'), ('itedjolec', 'atdwtsurs'),
    ('mistrl', 'oatvpu'), ('ding', 'y'), ('declon', 'arati'), ('ereflodbr', 'rileohmae'),
]

# Letter-only lines (the numeral lines 2, 11, 20, 22 and the mixed line 13 are set aside).
LETTER_LINES = [i + 1 for i, (a, b) in enumerate(PAIRS) if a.isalpha() and b.isalpha() and i + 1 != 20]


def tokens(ad):
    body = ad.split('This will')[0]
    return [t for t in re.split(r'[\s.,–-]+', body[2:]) if t]


if __name__ == '__main__':
    t1, t2 = tokens(AD1), tokens(AD2)
    print(len(t1), t1)
    print(len(t2), t2)
    print('letter lines:', LETTER_LINES)
    a = ''.join(p[0] for p in PAIRS if p[0].isalpha()); b = ''.join(p[1] for p in PAIRS if p[1].isalpha())
    print('letters: ad1 %d, ad2 %d' % (len(a), len(b)))
