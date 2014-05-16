from charm.toolbox.ecgroup import G, ZR, ECGroup
from charm.toolbox.eccurve import prime192v2


class ElGamal(object):
    def keygen(self):
        group = ECGroup(prime192v2)
        g = group.random(G)
        x = group.random(ZR)
        h = g ** x
        pk = {'group': group, 'g': g, 'h': h}
        sk = {'x': x}
        return pk, sk

    def encrypt(self, pk, m):
        group, g, h = pk['group'], pk['g'], pk['h']
        y = group.random(ZR)
        c1 = g ** y
        s = h ** y
        c2 = group.encode(str(m)) * s
        return Cipher(c1, c2, pk)

    def decrypt(self, pk, sk, c):
        group = pk['group']
        x = sk['x']
        s = c.c1 ** x
        m = group.decode(c.c2 * (s ** -1))
        return m


class Cipher(object):
    def __init__(self, c1, c2, pk):
        self.c1 = c1
        self.c2 = c2
        self.pk = pk

    def __add__(self, other):
        g = self.pk['g']
        if type(other) == Cipher:
            return Cipher(self.c1 * other.c1, self.c2 * other.c2, self.pk)
        else:
            return Cipher(self.c1, self.c2 * (g ** other), self.pk)

    def __mul__(self, other):
        pass


def test_elgamal():
    enc_scheme = ElGamal()
    pk, sk = enc_scheme.keygen()

    m = 2
    c = enc_scheme.encrypt(pk, m)
    d = enc_scheme.decrypt(pk, sk, c)

    print(str(m), str(d))


if __name__ == '__main__':
    test_elgamal()