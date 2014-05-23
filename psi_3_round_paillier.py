__author__ = 'Milinda Perera'

from charm.toolbox.integergroup import random, integer

from pkenc_paillier import Paillier
from utils_poly import poly_eval_horner, poly_from_roots


class PSI3RoundPaillier(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def server_to_client_1(self, server_set):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(self.sec_param)

        server_set_mapped = [integer(a, pk['n']) for a in server_set]
        coefs = poly_from_roots(server_set_mapped, integer(-1, pk['n']), integer(1, pk['n']))
        coef_cts = [enc_scheme.encrypt(pk, c) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        server_state = {'pk': pk, 'sk': sk, 'server_set': server_set}

        return out, server_state

    def client_to_server(self, client_set, pk, coef_cts):
        eval_cts = [poly_eval_horner(coef_cts, e) * random(pk['n']) + e for e in client_set]

        return eval_cts

    def server_to_client_2(self, eval_cts, pk, sk, server_set):
        enc_scheme = Paillier()
        evals = [int(enc_scheme.decrypt(pk, sk, ct)) for ct in eval_cts]
        intersection = sorted(set(evals) & set(server_set))

        return intersection

    def client_output(self, intersect):
        return intersect
