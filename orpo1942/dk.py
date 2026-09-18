"""Doppelkastenschluessel reference implementation, per 'Vorlaeufige Schluesselanleitung zum Doppelkastenschluessel' (Dec 1941).
Boxes are 25-letter strings, row-major. 1st plaintext letter looked up in box A, 2nd in box B.
Plaintext is written in double lines of L letters; the letters standing one under the other form the pairs;
a remainder not filling a double line is split in half (top row, bottom row). Each pair is enciphered twice."""
AL = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

def pos(box):
    return {c: divmod(i, 5) for i, c in enumerate(box)}

def enc_pair(A, B, pa, pb, p1, p2):
    r1, c1 = pa[p1]; r2, c2 = pb[p2]
    if r1 == r2:
        return B[r1 * 5 + (c2 + 1) % 5], A[r1 * 5 + (c1 + 1) % 5]
    return B[r1 * 5 + c2], A[r2 * 5 + c1]

def dec_pair(A, B, pa, pb, x1, x2):
    rb, cb = pb[x1]; ra, ca = pa[x2]
    if rb == ra:
        return A[ra * 5 + (ca - 1) % 5], B[rb * 5 + (cb - 1) % 5]
    return A[rb * 5 + ca], B[ra * 5 + cb]

def layout(n, L):
    """list of (top_index, bottom_index) plaintext positions, in ciphertext pair order; n must be even"""
    out = []; k = 0
    while n - k >= 2 * L:
        out += [(k + i, k + L + i) for i in range(L)]; k += 2 * L
    h = (n - k) // 2
    out += [(k + i, k + h + i) for i in range(h)]
    return out

def encrypt(A, B, P, L, rounds=2):
    pa, pb = pos(A), pos(B)
    C = []
    for i, j in layout(len(P), L):
        a, b = P[i], P[j]
        for _ in range(rounds):
            a, b = enc_pair(A, B, pa, pb, a, b)
        C += [a, b]
    return ''.join(C)

def decrypt(A, B, C, L, rounds=2):
    pa, pb = pos(A), pos(B)
    P = [None] * len(C)
    for k, (i, j) in enumerate(layout(len(C), L)):
        a, b = C[2 * k], C[2 * k + 1]
        for _ in range(rounds):
            a, b = dec_pair(A, B, pa, pb, a, b)
        P[i], P[j] = a, b
    return ''.join(P)

if __name__ == '__main__':
    A = 'HILQETUARSBKXFGPWCOZDVYMN'
    B = 'ZNOCHBXAVIUDTGWMYELSKPQRF'
    P = 'FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENABGEWEHRT'
    C = 'VDLGCTUQZREOMFCIFEALFYLBAPKWCTEIWBTYMFLNMVMQZTYLHUPILF'
    print(len(P), len(C))
    e = encrypt(A, B, P, 17)
    print(e); print(C); print(e == C)
    print(decrypt(A, B, C, 17))
