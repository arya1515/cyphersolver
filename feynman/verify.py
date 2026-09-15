"""Independent verification of David Vierra's May-2023 solution of Feynman ciphers #2 and #3.
Method: two monoalphabetic substitution alphabets, alternating word by word (first word of each
line uses alphabet 1), even-length words written backwards after substitution. Word boundaries dropped."""
import re, sys
A1 = 'MANYREQUS.HVBCID.OLWGZX.K.'
A2 = 'JHAZTENYXMLOCUFBQVKPSGW.D.'
C2 = ('XUKEXWSLZJUAXUNKIGWFSOZRAWURORKXAOSLHROBXBTKCMUWDVPTFBLMKEFVWMUXTVTWUIDDJVZKBRMC'
      'WOIWYDXMLUFPVSHAGSVWUFWORCWUIDUJCNVTTBERTUNOJUZHVTWKORSVRZSVVFSQXOCMUWPYTRLGBMCY'
      'POJCLRIYTVFCCMUWUFPOXCNMCIWMSKPXEDLYIQKDJWIWCJUMVRCJUMVRKXWURKPSEEIWZVXULEIOETOO'
      'FWKBIUXPXUGOWLFPWUSCH')
C3 = ('WURVFXGJYTHEIZXSQXOBGSVRUDOOJXATBKTARVIXPYTMYABMVUFXPXKUJVPLSDVTGNGOSIGLWURPKFCV'
      'GELLRNNGLPYTFVTPXAJOSCWRODORWNWSICLFKEMOTGJYCRRAOJVNTODVMNSQIVICRBICRUDCSKXYPDMD'
      'ROJUZICRVFWXIFPXIVVIEPYTDOIAVRBOOXWRAKPSSZTZKVROSWCRCFVEESOLWKTOBXAUXVB')
# Housman, A Shropshire Lad LXII, lines 19-32 (line breaks as printed)
P2 = """Why, if 'tis dancing you would be,
There's brisker pipes than poetry.
Say, for what were hop-yards meant,
Or why was Burton built on Trent?
Oh many a peer of England brews
Livelier liquor than the Muse,
And malt does more than Milton can
To justify God's ways to man.
Ale, man, ale's the stuff to drink
For fellows whom it hurts to think:"""
# Feynman, Phys. Rev. 91, 1291 (1953), "Atomic Theory of the λ Transition in Helium", opening sentences
P3 = """The behavior of liquid helium, especially below the lambda transition, is very curious.
The most successful theoretical interpretations so far have been largely phenomenological.
In this paper and one or two to follow, the problem will be studied entirely from first principles."""

def enc_word(w, alpha):
    out = ''.join(alpha[ord(c) - 65] for c in w)
    return out[::-1] if len(w) % 2 == 0 else out

def encrypt(text, alphabets=(A1, A2), reset='line', tokens=r"[A-Za-z']+|-"):
    ct = []; k = 0
    units = text.split('\n') if reset == 'line' else re.split(r'(?<=[.?!:])\s+', text)
    for line in units:
        k = 0
        for tok in re.findall(r"[A-Za-z][A-Za-z']*(?:-[A-Za-z']+)*", line):
            w = re.sub('[^A-Z]', '', tok.upper())
            ct.append(enc_word(w, alphabets[k % 2])); k += 1
    return ''.join(ct)

def compare(name, got, want):
    n = sum(a == b for a, b in zip(got, want))
    print(f"{name}: len got {len(got)} want {len(want)}; matching positions {n}")
    for i in range(0, max(len(got), len(want)), 80):
        g, w = got[i:i+80], want[i:i+80]
        print('  enc ', g); print('  ct  ', w)
        print('       ' + ''.join(' ' if a == b else '^' for a, b in zip(g, w)))
    return got == want

if __name__ == '__main__':
    ok2 = compare('Cipher #2', encrypt(P2), C2)
    ok3 = compare('Cipher #3', encrypt(P3), C3)
    print('EXACT MATCH #2:', ok2, ' #3:', ok3)
