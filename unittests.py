__author__ = 'Milinda Perera'

import unittest

from utils_poly import poly_from_roots, poly_eval, poly_eval_horner, poly_mul, poly_print
from pkenc_elgamal_exp import ElGamalExp
from pkenc_paillier import Paillier


class Test_utils_poly(unittest.TestCase):
    def test_1_poly_from_roots(self):
        """Tests the polynomial interpolation function."""

        output = "poly_from_roots failed on {0}.\nNeeded {1}, got {2}."

        # Each test case is (roots, coefs)
        cases = [([2, 3, 4, 5], [120, -154, 71, -14, 1]),
                 ([0], [0, 1]),
                 ([-1], [1, 1])]

        for (roots, coefs) in cases:
            result = poly_from_roots(roots, -1, 1)
            self.assertListEqual(result, coefs, output.format(roots, coefs, result))

    def test_2_poly_eval(self):
        """Tests the regular polynomial evaluation function"""

        output = "poly_eval failed on {0} and {1}.\nNeeded {2}, got {3}."

        # Each test case is (roots, x, eval)
        cases = [([2, 3, 4, 5], 3, 0),
                 ([-1, 2, -10, -111], -10, 0),
                 ([1, 2, -7, -22, 0], 4, 6864)]

        for (roots, x, eval) in cases:
            coefs = poly_from_roots(roots, -1, 1)
            result = poly_eval(coefs, x)
            self.assertEqual(result, eval, output.format(roots, x, eval, result))

    def test_3_poly_eval_horner(self):
        """Tests the Horner's polynomial evaluation function"""

        output = "poly_eval_horner failed on {0} and {1}.\nNeeded {2}, got {3}."

        # Each test case is (roots, x, eval)
        cases = [([2, 3, 4, 5], 3, 0),
                 ([-1, 2, -10, -111], -10, 0),
                 ([1, 2, -7, -22, 0], 4, 6864)]

        for (roots, x, eval) in cases:
            coefs = poly_from_roots(roots, -1, 1)
            result = poly_eval_horner(coefs, x)
            self.assertEqual(result, eval, output.format(roots, x, eval, result))

    def test_4_poly_mul(self):
        """Tests the polynomial multiplication"""

        output = "poly_mul failed on {0} and {1}.\nNeeded {2}, got {3}."

        # Each test case is (coefs_1, coefs_2, coefs_mul)
        cases = [([0], [0], [0]),
                 ([1], [1], [1]),
                 ([2], [-2], [-4]),
                 ([2, 3], [4, 5], [8, 22, 15]),
                 ([0, -2, 5, -6], [0, 2, 0, -4], [0, 0, -4, 10, -4, -20, 24])]

        for (coefs_1, coefs_2, coefs_mul) in cases:
            result = poly_mul(coefs_1, coefs_2, 0)
            self.assertEqual(result, coefs_mul, output.format(coefs_1, coefs_2, coefs_mul, result))

    def test_5_poly_print(self):
        """Tests the polynomial print function"""

        output = "poly_print failed on {0}.\nNeeded {1}, got {2}."

        # Each test case is (coefs, string)
        cases = [([0], '0'),
                 ([1], '1'),
                 ([1, 0], '1'),
                 ([1, 0, 0, 0, -6], '- 6 X^4 + 1'),
                 ([-1], '- 1'),
                 ([-1, 0], '- 1'),
                 ([-1, 9], '9 X - 1'),
                 ([-1, 0, 9], '9 X^2 - 1')]

        for (coefs, string) in cases:
            result = poly_print(coefs)
            self.assertEqual(result, string, output.format(coefs, string, result))


class Test_pkenc_elgamal_exp(unittest.TestCase):
    def setUp(self):
        self.enc_scheme = ElGamalExp()
        self.pk, self.sk = self.enc_scheme.keygen()

    def test_1_enc(self):
        """Tests ElGamal encryption function."""

        output = "ElGamal encryption failed on {0}."

        messages = [0, 1, 55, 535, 29847123948, 1928347123949123764876, 23984761239847612346781234987001234]

        for m in messages:
            c = self.enc_scheme.encrypt(self.pk, m)
            encoded_m = c.c1 ** self.sk['x'] * self.pk['g'] ** (m % self.pk['order'])
            self.assertEqual(c.c2, encoded_m, output.format(m))

    def test_2_homomorphic_addition(self):
        """Tests homomorphic addition of ElGamal ciphertexts."""

        output = "ElGamal homomorphic addition failed on {0} and {1}."

        # Each test case is (num1, num2, sum)
        cases = [(0, 0, 0),
                 (0, 1, 1),
                 (-1, 2, 1),
                 (3, 30, 33),
                 (-22, 22, 0)]

        for (a, b, s) in cases:
            c1 = self.enc_scheme.encrypt(self.pk, a)
            c2 = self.enc_scheme.encrypt(self.pk, b)
            c3 = c1 + c2
            self.assertTrue(self.enc_scheme.does_encrypt(self.pk, self.sk, c3, s), output.format(a, b))

    def test_3_homomorphic_multiplication(self):
        """Tests homomorphic multiplication of ElGamal ciphertexts."""

        output = "ElGamal homomorphic multiplication failed on {0} and {1}."

        # Each test case is (num1, num2, mul)
        cases = [(0, 0, 0),
                 (0, 1, 0),
                 (-2, 4, -8),
                 (-5, 5, -25),
                 (6, 4, 24)]

        for (a, b, m) in cases:
            c1 = self.enc_scheme.encrypt(self.pk, a)
            c3 = c1 * b
            self.assertTrue(self.enc_scheme.does_encrypt(self.pk, self.sk, c3, m), output.format(a, b))


class Test_pkenc_paillier(unittest.TestCase):
    def setUp(self):
        self.enc_scheme = Paillier()
        self.pk, self.sk = self.enc_scheme.keygen(1024)

    def test_1_enc(self):
        """Tests Paillier encryption function."""

        output = "Paillier encryption failed on {0}."

        messages = [1, 2, 55, 535, 29847123948, 1928347123949123764876, 23984761239847612346781234987001234]

        for m in messages:
            c = self.enc_scheme.encrypt(self.pk, m)
            d = self.enc_scheme.decrypt(self.pk, self.sk, c)
            self.assertEqual(d, m, output.format(m))

    def test_2_homomorphic_addition(self):
        """Tests homomorphic addition of Paillier ciphertexts."""

        output = "Paillier homomorphic addition failed on {0} and {1}."

        cases = [(1, 1, 2),
                 (1, 2, 3),
                 (3, 30, 33),
                 (22, 22, 44)]

        # Each test case is (num1, num2, sum)
        for (a, b, s) in cases:
            c1 = self.enc_scheme.encrypt(self.pk, a)
            c2 = self.enc_scheme.encrypt(self.pk, b)
            c3 = c1 + c2
            d = self.enc_scheme.decrypt(self.pk, self.sk, c3)
            self.assertEqual(d, s, output.format(a, b))

    def test_3_homomorphic_multiplication(self):
        """Tests homomorphic multiplication of Paillier ciphertexts."""

        output = "Paillier homomorphic multiplication failed on {0} and {1}."

        # Each test case is (num1, num2, mul)
        cases = [(1, 1, 1),
                 (2, 4, 8),
                 (5, 5, 25),
                 (6, 4, 24)]

        for (a, b, m) in cases:
            c1 = self.enc_scheme.encrypt(self.pk, a)
            c2 = c1 * b
            d = self.enc_scheme.decrypt(self.pk, self.sk, c2)
            self.assertEqual(d, m, output.format(a, b))


if __name__ == '__main__':
    tests = [Test_utils_poly, Test_pkenc_elgamal_exp, Test_pkenc_paillier]
    suites = [unittest.makeSuite(t, 'test') for t in tests]
    all_suites = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(all_suites)