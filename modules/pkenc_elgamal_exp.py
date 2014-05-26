__author__ = 'Milinda Perera'

from charm.toolbox.ecgroup import G, ZR, ECGroup
from charm.toolbox.eccurve import prime192v2


class ElGamalExp(object):
    """
    Implements the ElGamal cryptosystem where messages are encoded in the exponent.
    """

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

    def does_encrypt_zero(self, pk, sk, c):
        x = sk['x']
        return c.c2 == c.c1 ** x

    def does_encrypt_one(self, pk, sk, c):
        g = pk['g']
        x = sk['x']
        return c.c2 == (c.c1 ** x) * g

    def does_encrypt(self, pk, sk, c, m):
        g, order = pk['g'], pk['order']
        x = sk['x']
        return c.c2 == (c.c1 ** x) * (g ** (m % order))


class Cipher(object):
    """
    This class abstracts the homomorphic operations of the Paillier ciphertexts.
    """

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
