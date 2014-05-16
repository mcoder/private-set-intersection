import random as pyrandom
from charm.toolbox.integergroup import random, integer
from pkenc_paillier import Paillier
from utils_poly import poly_eval, poly_eval_horner, poly_from_roots


class PSI(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def b_to_a(self, set_b):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(self.sec_param)

        set_a_mapped = [integer(a, pk['n']) for a in set_b]
        coefs = poly_from_roots(set_a_mapped, integer(-1, pk['n']), integer(1, pk['n']))
        coef_cts = [enc_scheme.encrypt(pk, c) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        state_b = {'pk': pk, 'sk': sk, 'set_b': set_b}

        return out, state_b

    def a_to_b(self, set_a, pk, coef_cts):
        eval_cts = [poly_eval_horner(coef_cts, e) * random(pk['n']) + e for e in set_a]

        return eval_cts

    def b_to_out(self, eval_cts, pk, sk, set_b):
        enc_scheme = Paillier()
        evals = [int(enc_scheme.decrypt(pk, sk, ct)) for ct in eval_cts]
        set_int = sorted(set(evals) & set(set_b))

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

    out_b_1, state_b = psi.b_to_a(set_b)
    out_a = psi.a_to_b(set_a, **out_b_1)
    out_b_2 = psi.b_to_out(out_a, **state_b)

    print('output: {0}'.format(sorted(out_b_2)))


if __name__ == '__main__':
    test()