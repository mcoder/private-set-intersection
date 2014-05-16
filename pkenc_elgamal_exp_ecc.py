from charm.toolbox.ecgroup import G, ZR, ECGroup
from charm.toolbox.eccurve import prime192v2


class ElGamal(object):
    def keygen(self):
        group = ECGroup(prime192v2)
        g = group.random(G)
        x = group.random(ZR)
        h = g ** x
        pk = {'g': g, 'h': h, 'group': group, 'order': 6277101735386680763835789423078825936192100537584385056049}
        sk = {'x': x}
        return pk, sk

    def encrypt(self, pk, m):
        g, h, group, order = pk['g'], pk['h'], pk['group'], pk['order']
        y = group.random(ZR)
        c1 = g ** y
        c2 = (h ** y) * (g ** (m % order))
        return Cipher(c1, c2, pk)

    def encrypts_zero(self, sk, c):
        x = sk['x']
        return c.c2 == c.c1 ** x


class Cipher(object):
    def __init__(self, c1, c2, pk):
        self.c1 = c1
        self.c2 = c2
        self.pk = pk

    def __add__(self, other):
        g, order = self.pk['g'], self.pk['order']
        if type(other) == Cipher:
            return Cipher(self.c1 * other.c1, self.c2 * other.c2, self.pk)
        else:
            return Cipher(self.c1, self.c2 * (g ** (other % order)), self.pk)

    def __mul__(self, other):
        g, order = self.pk['g'], self.pk['order']
        return Cipher(self.c1 ** (other % order), self.c2 ** (other % order), self.pk)


def test_elgamal():
    enc_scheme = ElGamal()
    pk, sk = enc_scheme.keygen()

    c1 = enc_scheme.encrypt(pk, -2)
    c2 = enc_scheme.encrypt(pk, 1)
    c3 = c1 + c2 + 1
    c4 = enc_scheme.encrypt(pk, 4)
    c5 = c1 * 2 + c4

    print(enc_scheme.encrypts_zero(sk, c1))
    print(enc_scheme.encrypts_zero(sk, c2))
    print(enc_scheme.encrypts_zero(sk, c3))
    print(enc_scheme.encrypts_zero(sk, c5))


if __name__ == '__main__':
    test_elgamal()