"""Wehrmacht Enigma I model (UKW B/C, wheels I-V) with a reference decrypt and a test
against the Huppenkothen message of 9 April 1945 (Sullivan & Weierud 2005, key published)."""
import numpy as np

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
WHEELS = {
    'I':   ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
    'II':  ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
    'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
    'IV':  ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
    'V':   ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
}
UKW = {'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}


def perm(s):
    return np.array([A.index(c) for c in s], dtype=np.int64)


def inv(p):
    q = np.empty_like(p); q[p] = np.arange(26); return q


class Enigma:
    """Positions and rings are given as letters (window letters)."""

    def __init__(self, ukw, order, rings, plugs):
        self.ukw = perm(UKW[ukw])
        self.rot = [perm(WHEELS[w][0]) for w in order]
        self.rinv = [inv(r) for r in self.rot]
        self.notch = [A.index(WHEELS[w][1]) for w in order]
        self.rings = [A.index(c) for c in rings]
        pb = np.arange(26)
        for pr in plugs.split():
            a, b = A.index(pr[0]), A.index(pr[1]); pb[a], pb[b] = b, a
        self.pb = pb

    def step(self, pos):
        l, m, r = pos
        if m == self.notch[1]:
            m = (m + 1) % 26; l = (l + 1) % 26
        elif r == self.notch[2]:
            m = (m + 1) % 26
        r = (r + 1) % 26
        return [l, m, r]

    def scrambler(self, pos):
        """Return the 26-permutation of rotors+reflector at window positions pos."""
        x = np.arange(26)
        for i in (2, 1, 0):
            off = (pos[i] - self.rings[i]) % 26
            x = (self.rot[i][(x + off) % 26] - off) % 26
        x = self.ukw[x]
        for i in (0, 1, 2):
            off = (pos[i] - self.rings[i]) % 26
            x = (self.rinv[i][(x + off) % 26] - off) % 26
        return x

    def run(self, text, start):
        pos = [A.index(c) for c in start]
        out = []
        for c in text:
            if c not in A: continue
            pos = self.step(pos)
            s = self.scrambler(pos)
            out.append(A[self.pb[s[self.pb[A.index(c)]]]])
        return ''.join(out)


if __name__ == '__main__':
    # Huppenkothen Nr. 69 part 1, 9 Apr 1945: UKW B, W/O 123 (12:00-17:29), rings XJE,
    # stecker AM BF CD EK HQ IO LV NT SY WZ, message key GLB (from UFC KHR)
    ct = ('BUQVG DQYEU AUTCD FJFRG LIDWF WBKMH RBWIK OOBRL UBTSL EKDGK GMKDN GCZJV '
          'AGRGK TUNAH QDJRT GHYTR YEKSP KGWYQ OMEWN DXCWN XKPGJ GNGSG TQEZW WXUKI '
          'DPVCU JWQCH GBPBC SJRFS HFXBF MWPLE JWCAD JCSUO MKGWF QRKXZ KLJBG FHINI '
          'JLMIS WIRMZ JGDDC NQUJK PSMMR SETKH HGFSG YINBB INHPX HGJKT IBPHW HQGTQ UOEDD FPV')
    e = Enigma('B', ['I', 'II', 'III'], 'XJE', 'AM BF CD EK HQ IO LV NT SY WZ')
    print('indicator check: KHR at UFC ->', e.run('KHR', 'UFC'))
    full = ct.replace(' ', '')
    print('from group 1:', e.run(full[:60], 'GLB'))
    print('from group 2:', e.run(full[5:65], 'GLB'))
