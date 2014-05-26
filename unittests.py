__author__ = 'Milinda Perera'

import unittest

from utils_poly import poly_from_roots, poly_eval, poly_eval_horner


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
                 ([-1, 2, -10, -111], -10, 3),
                 ([1, 2, -7, -22, 0], 4, 6864)]

        for (roots, x, eval) in cases:
            coefs = poly_from_roots(roots, -1, 1)
            result = poly_eval(coefs, x)
            self.assertEqual(eval, result, output.format(roots, x, eval, result))


if __name__ == '__main__':
    tests = [Test_utils_poly]
    suites = [unittest.makeSuite(t, 'test') for t in tests]
    all_suites = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(all_suites)