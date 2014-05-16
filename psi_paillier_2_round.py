import random as pyrandom
from charm.toolbox.integergroup import random, integer
from pkenc_paillier import Paillier
from utils_poly import poly_eval, poly_eval_horner, poly_from_roots


class PSI(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def b_to_a(self, set_b):
        pass

    def a_to_b(self, set_a, pk, coef_cts):
        pass


def test():
    set_len = 50
    set_int_len = 10
    set_a = list(set([pyrandom.randint(1, 200) for i in range(100)]))[:set_len]
    set_b = list(set([pyrandom.randint(201, 400) for i in range(100)]))[:set_len - set_int_len] + set_a[:set_int_len]

    print('a: {0}'.format(sorted(set_a)))
    print('b: {0}'.format(sorted(set_b)))
    print('a & b: {0}'.format(sorted(set(set_a) & set(set_b))))
    print

    psi = PSI()

    out_b = psi.b_to_a(set_b)
    out_a = psi.a_to_b(set_a, **out_b)

    print('output: {0}'.format(sorted(out_a)))


if __name__ == '__main__':
    test()