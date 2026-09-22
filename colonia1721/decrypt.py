"""R24 (Colonia 5:1, Brussels 9 Oct 1721): Lasry's key ASV-C15 (DECODE DOC_R24_D3446) + context values added here."""
import pathlib
LASRY = {'2':'','22':'','222':'','6':'a','77':'a','58':'c','35':'che','46':'d','47':'de','53':'di','04':'e','40':'e',
 '73':'f','17':'i','71':'i','1':'il','65':'in','15':'l','08':'m','74':'ma','66':'n','81':'ne','16':'o','61':'o',
 '05':'p','50':'p','18':'que','14':'r','41':'r','01':'s','38':'s','86':'se','88':'st','75':'su','03':'t','06':'u','60':'u'}
ADDED = {'18':'qu','55':'gli','67':'g'}   # 18 QUE->QU (qualche, quel, questo); 55 e-gli; 67 g-rat(o), grade M
key = {**LASRY, **ADDED}
toks = pathlib.Path(__file__).with_name('cipher.txt').read_text().split()
out = []
for t in toks:
    out.append('·' if t in ('2','22','222') else key.get(t, f'[{t}]'))
print(' '.join(out))
print(f'{sum(t in key for t in toks)}/{len(toks)} tokens valued')
