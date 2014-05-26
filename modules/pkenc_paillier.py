__author__ = 'Milinda Perera'

from charm.toolbox.integergroup import random, randomPrime, isPrime, gcd, lcm, integer


class Paillier(object):
    """
    Implements the Paillier cryptosystem.
    """

    def L(self, u, n):
        return integer(int(u) - 1) / n

    def keygen(self, secparam=1024):
        while True:
            p, q = randomPrime(secparam), randomPrime(secparam)
            if isPrime(p) and isPrime(q) and gcd(p * q, (p - 1) * (q - 1)) == 1:
                break
        n = p * q
        g = n + 1
        n2 = n ** 2
        lam = lcm(p - 1, q - 1)
        u = (self.L(((g % n2) ** lam), n) % n) ** -1
        pk = {'n': n, 'g': g, 'n2': n2}
        sk = {'lam': lam, 'u': u}
        return pk, sk

    def encrypt(self, pk, m):
        g, n, n2 = pk['g'], pk['n'], pk['n2']
        r = random(pk['n'])
        c = (((g % n2) ** m) * ((r % n2) ** n)) % n2
        return Cipher(c, pk)

    def decrypt(self, pk, sk, ct):
        n, n2 = pk['n'], pk['n2']
        lam, u = sk['lam'], sk['u']
        m = ((self.L((ct.c ** lam) % n2, n) % n) * u) % n
        return m


class Cipher(object):
    """
    This class abstracts the homomorphic operations of the Paillier ciphertexts.
    """

    def __init__(self, c, pk):
        self.c = c
        self.pk = pk

    def __add__(self, other):
        g, n2 = self.pk['g'], self.pk['n2']
        if type(other) == Cipher:
            return Cipher((self.c * other.c) % n2, self.pk)
        else:
            return Cipher((self.c * ((g ** other) % n2)) % n2, self.pk)

    def __mul__(self, other):
        n2 = self.pk['n2']
        return Cipher((self.c ** other) % n2, self.pk)


def test_paillier():
    enc_scheme = Paillier()
    pk, sk = enc_scheme.keygen(1024)

    m = 2
    c = enc_scheme.encrypt(pk, m)
    c1 = c * (2 ** 2) + 0
    c1 = c1 * (2 ** 2) + c1
    c1.c *= ((c1.pk['n2'] - 1) % c1.pk['n2'])

    d = enc_scheme.decrypt(pk, sk, c)

    print(str(m), str(d))


if __name__ == '__main__':
    test_paillier()