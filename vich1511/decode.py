"""Decode a transcription of the Ferdinand-Vich cipher (AHN Estado 8715, 1511-12 key).

Values come from aligning N.46 (5 Jul 1511) and N.52BIS (1 Mar 1512) with their contemporary
decipherments. Unknown tokens print in [brackets]."""
import sys, re

LET = {  # single symbols -> letters (homophones)
    '40': 'r', '4h': 'e', '3': 'e', 'ah': 'o', 'T': 'o', 'to': 'a', 'q': 'm', '7': 'a', 'b': 'a',
    'ch': 'c', 'c': 'l', 'oo': 'd', '11': 'n', 'X': 't', 'g': 't', 'P': 'p', 'SS': 'p', 'e': 'i',
    'Z': 'i', '8': 'y', 'B': 'b', 'd': 's', 'eh': 's', 'V': 'v', '3t': 'u', 'gh': 'f', '7o': 'll',
    '9': 't', 'p': 'z', 'W': 'n', 'o': 'g', 'O': 'h', 'E': 'r',
}
CODE = {  # code groups -> words / syllables
    'pef': 'que', 'diz': 'de', 'dih': 'con', 'fak': 'el', 'fem': 'es', 'fan': 'en', 'has': 'lo',
    'hor': 'la', 'raf': 'por', 'rif': 'porque', 'mik': 'no', 'flart': 'me', 'seh': 'se', 'pob': 'si',
    'soy': 'io', 'suy': 'ia', 'pax': 'su', 'mix': 'papa', 'moe': 'mucho', 'mee': 'muy', 'mem': 'nro',
    'fug': 'señor', 'fiq': 'victoria', 'sod': 'sera', 'gik': 'agora', 'go': 'aunque', 'doh': 'contra',
    'fid': 'despues', 'sal': 'todo', 'sel': 'todo', 'sub': 'vras', 'par': 'recebido', 'hap': 'havemos',
    'hag': 'havemos', 'hib': 'guerra', 'hub': 'gente', 'gos': 'ciudad', 'pip': 'razon', 'fub': 'daño',
    'fuj': 'exercito', 'dai': 'como', 'mok': 'nos', 'fol': 'ellas', 'goy': 'cartas', 'fis': 'febrero',
    'fib': 'febrero', 'hat': 'luego', 'fac': 'dichas', 'heh': 'ha', 'hig': 'haver', 'day': 'direys',
    'gak': 'aquella', 'hel': 'ingalaterra', 'hep': 'julio', 'gik': 'agora', 'pag': 'quales',
    'moe': 'mucho', 'die': 'cosa', 'huf': 'he', 'fun': 'esta', 'sus': 'um', 'miq': 'orden',
    'plart': 'mi', 'soy': 'yo', 'mah': 'dezir', 'fim': 'esta', 'fit': 'capitan', 'dee': 'general',
    'gab': 'assi', 'plort': 'mi', 'fef': 'emperador', 'sap': 'venecianos', 'ref': 'para', 'suk': 'tiene',
    'roc': 'parece', 'gor': 'venir', 'seg': 'viene', 'hob': 'largo', 'fir': 'del', 'rof': 'paraque', 'keg': 'pero',
    'huz': 'mas', 'fud': 'dicho', 'hik': 'italia', 'myk': 'no', 'rie': 'pued', 'fat': 'forma', 'dieb': 'cosas', 'fic': 'del',
    'soq': 'verdad', 'daz': 'dize', 'gup': 'batalla', 'fur': 'dela', 'guo': 'bien', 'dij': 'cierto', 'diy': 'cierto',
    'hih': 'ha', 'fue': 'saber', 'far': 'dar', 'pid': 'presa', 'gaf': 'aqui', 'guj': 'esto', 'meq': 'otra',
}

def decode(tokens):
    out = []
    for t in tokens:
        if t in CODE: out.append(' ' + CODE[t] + ' ')
        elif t in LET: out.append(LET[t])
        else: out.append(' [' + t + '] ')
    return re.sub(r' +', ' ', ''.join(out)).strip()

if __name__ == '__main__':
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.startswith('L'): continue
        tag, body = line.split(':', 1)
        print(tag, decode(body.split()))
