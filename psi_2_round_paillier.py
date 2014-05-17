__author__ = 'Milinda Perera'

import random as pyrandom

from charm.toolbox.integergroup import random, integer

from pkenc_paillier import Paillier
from utils_poly import poly_eval_horner, poly_from_roots


class PSI2RoundPaillier(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def client_to_server(self, client_set):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(self.sec_param)

        slient_set_mapped = [integer(a, pk['n']) for a in client_set]
        coefs = poly_from_roots(slient_set_mapped, integer(-1, pk['n']), integer(1, pk['n']))
        coef_cts = [enc_scheme.encrypt(pk, c) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        client_state = {'pk': pk, 'sk': sk, 'client_set': client_set}

        return out, client_state

    def server_to_client(self, server_set, pk, coef_cts):
        eval_cts = [poly_eval_horner(coef_cts, e) * random(pk['n']) + e for e in server_set]

        return eval_cts

    def client_output(self, eval_cts, pk, sk, client_set):
        enc_scheme = Paillier()
        evals = [int(enc_scheme.decrypt(pk, sk, ct)) for ct in eval_cts]
        intersection = sorted(set(evals) & set(client_set))

        return intersection


def test():
    set_len = 50
    set_int_len = 10
    server_set = list(set([pyrandom.randint(1, 200) for i in range(100)]))[:set_len]
    client_set = list(set([pyrandom.randint(201, 400) for i in range(100)]))[:set_len - set_int_len] + server_set[
                                                                                                       :set_int_len]

    print('server set: {0}'.format(sorted(server_set)))
    print('client set: {0}'.format(sorted(client_set)))
    print('intersection: {0}'.format(sorted(set(server_set) & set(client_set))))
    print

    psi = PSI2RoundPaillier(1024)

    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)

    print('client output: {0}'.format(sorted(client_out_2)))


if __name__ == '__main__':
    test()