"""Decrypt ASV Segr. Stato Portogallo 8 cipher passages with Lasry's reconstructed key (DECODE DOC_R190_D3258).
Usage: python decrypt.py "4703775700 9 ..."   (spaces ignored; 9 = word separator/null)"""
import sys
KEY = {'82':'Hunt','28':'M.ta','00':'a','81':'a','44':'ancora','71':'b','61':'c','78':'che','51':'d','68':'dura',
       '07':'e','83':'e','73':'f','63':'g','53':'h','05':'i','85':'i','25':'l','75':'l','65':'m','55':'n','03':'o',
       '87':'o','77':'p','84':'per','67':'q','24':'quell','14':'quest','57':'r','47':'s','37':'t','01':'u','27':'u',
       '17':'z'}
def dec(s):
    s = ''.join(c for c in s if c.isdigit() or c == '?')
    out, i = [], 0
    while i < len(s):
        if s[i] == '9': out.append(' '); i += 1; continue
        g = s[i:i+2]
        out.append(KEY.get(g, '[%s]' % g) if len(g) == 2 else '[%s]' % g); i += 2
    return ''.join(out)
if __name__ == '__main__':
    for a in sys.argv[1:] or sys.stdin.read().splitlines():
        if a.strip(): print(dec(a))
