__author__ = 'Milinda Perera'

import unittest

from utils_poly import poly_from_roots, poly_eval, poly_eval_horner, poly_mul, poly_print


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
            self.assertListEqual(coefs, result, output.format(roots, coefs, result))

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
            self.assertEqual(eval, result, output.format(roots, x, eval, result))

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
            self.assertEqual(eval, result, output.format(roots, x, eval, result))

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
            self.assertEqual(coefs_mul, result, output.format(coefs_1, coefs_2, coefs_mul, result))

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
            self.assertEqual(string, result, output.format(coefs, string, result))


if __name__ == '__main__':
    tests = [Test_utils_poly]
    suites = [unittest.makeSuite(t, 'test') for t in tests]
    all_suites = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(all_suites)