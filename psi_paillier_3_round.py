import random as pyrandom
from charm.toolbox.integergroup import random, integer
from pkenc_paillier import Paillier
from utils_poly import poly_eval, poly_eval_horner, poly_from_roots


class PSI(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def a_to_b_1(self, set_a):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(self.sec_param)

        set_a_mapped = [integer(a, pk['n']) for a in set_a]
        coefs = poly_from_roots(set_a_mapped, integer(-1, pk['n']), integer(1, pk['n']))
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
    set_len = 50
    set_int_len = 10
    set_a = list(set([pyrandom.randint(1, 200) for i in range(100)]))[:set_len]
    set_b = list(set([pyrandom.randint(201, 400) for i in range(100)]))[:set_len - set_int_len] + set_a[:set_int_len]

    print('a: {0}'.format(sorted(set_a)))
    print('b: {0}'.format(sorted(set_b)))
    print('a & b: {0}'.format(sorted(set(set_a) & set(set_b))))
    print

    psi = PSI(1024)

    state_a, out_a_1 = psi.a_to_b_1(set_a)
    out_b = psi.b_to_a(set_b, **out_a_1)
    out_a_2 = psi.a_to_b_2(out_b, **state_a)

    print('output: {0}'.format(sorted(out_a_2)))


if __name__ == '__main__':
    test()