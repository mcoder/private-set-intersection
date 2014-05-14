from charm.toolbox.integergroup import random, integer

from pkenc_paillier import Paillier

from utils_poly import *


class PSI(object):
    def a_to_b_1(self, set_a):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(1024)

        coefs = poly_from_roots(set_a)
        coef_cts = [enc_scheme.encrypt(pk, c) for c in coefs]

        state_a = {'pk': pk, 'sk': sk, 'set_a': set_a}
        out = {'pk': pk, 'coef_cts': coef_cts}

        return state_a, out

    def b_to_a(self, set_b, pk, coef_cts):
        eval_cts = [poly_eval_horner(coef_cts, e) * random(pk['n']) + e for e in set_b]

        return eval_cts

    def a_to_b_2(self, eval_cts, pk, sk, set_a):
        enc_scheme = Paillier()
        evals = [int(enc_scheme.decrypt(pk, sk, ct)) for ct in eval_cts]
        set_int = sorted(set(evals) & set(set_a))

        return set_int


def test():
    set_a = [1, 2, 3, 5, 6, 10, 11, 12, 13, 16, 18, 19, 20, 22, 23, 24, 25, 26, 28, 30]
    set_b = [3, 4, 16, 17, 21, 22, 24, 27, 29, 32, 38, 39, 42, 44, 47, 50, 51, 55, 59, 60]

    psi = PSI()

    state_a, out_a_1 = psi.a_to_b_1(set_a)
    out_b = psi.b_to_a(set_b, **out_a_1)
    a_out_2 = psi.a_to_b_2(out_b, **state_a)

    print(a_out_2)


if __name__ == '__main__':
    test()