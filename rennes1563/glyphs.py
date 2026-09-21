# glyph name -> candidate values ('-' = null), Bishop of Rennes' cipher as seen in the Colbert hands
G = {
 'qq':'que|-', 'lt':'vous', 'gt':'nous', 'plus':'vostre|-', 'Vb':'qui', 'A':'mais', 'at':'par', 'ca':'faire',
 'tu':'faict', 'mn':'la', 'vp':'le', 'sc':'lettre', 'pl':'bien', '8':'luy|b', 'Om':'quant', 'tz':'puis',
 'eq':'-', 'sl':'-', 'dag':'-',
 'z':'a', 'eta':'a|n', 'S':'a|s', 'ff':'a',
 'hb':'b', 'La':'d', 'do':'d|-', 'y':'d', 'gam':'d',
 'd':'e', 'xy':'e', 'xi':'e', 'x1':'e', 'bs':'e',
 '4':'f', 'phi':'f', 'a':'g', 'at~':'g', 'beta':'g|l', 'pi':'h', 'Ch':'h',
 '10':'i', 'io':'i', 'k':'i', 'mi':'i', 'sharp':'i|est', 'lz':'i',
 '6':'l|t', 'sig':'l|o', 'D':'m', 'J':'m', 'mJ':'m|c|i', '9':'n', 'a1':'n|g', 'tt':'n|i|-', 'uh':'n',
 'O':'o', 'Z3':'o', 'Lo':'o|-', 'lf':'o', 'b':'p', 'Zp':'p', 'my':'p', 'ss':'q',
 'r2':'r', 'ee':'r', 'er':'r|t|c', 'rs':'r|s', 's3':'s|r', 'ct':'s|t', 'V':'s',
 'G':'t', 'ec':'t', 'Tb':'t', 'lam':'u', 'mu':'u', 'w':'u', 'star':'x', '7':'y', 'T':'y', 'th':'z',
 '3':'c|o', 'm':'c|i', 'E':'c',
}
def cands(tok):
    if '=' in tok and not tok.startswith('='): return tok.split('=',1)[1].split('|')
    if tok.startswith('"'): return [tok.strip('"')]
    return G.get(tok, '{%s}' % tok).split('|')
G.update({'la':'u|v','5':'r|s','we':'e','xe':'e','o':'o','al':'h','sh':'i','io':'i','th':'z','d':'e','Gb':'t','La':'d','9':'n','z':'a','b':'p','D':'m','ct':'s','m':'c','mu':'u','ee':'r','4':'f','hb':'b','Vb':'qui','at':'par','qq':'que','sl':'-','S':'a','eta':'a','6':'l'})
