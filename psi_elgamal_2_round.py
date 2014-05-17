import random as pyrandom
from charm.toolbox.integergroup import random, integer
from pkenc_elgamal_exp_ecc import ElGamal
from utils_poly import poly_eval, poly_eval_horner, poly_from_roots


class PSIElGamal(object):
    def client_to_server(self, client_set):
        enc_scheme = ElGamal()
        pk, sk = enc_scheme.keygen()

        set_a_mapped = [integer(a, pk['order']) for a in client_set]
        coefs = poly_from_roots(set_a_mapped, integer(-1, pk['order']), integer(1, pk['order']))
        coef_cts = [enc_scheme.encrypt(pk, int(c)) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        client_state = {'pk': pk, 'sk': sk, 'client_set': client_set}

        return out, client_state

    def server_to_client(self, server_set, pk, coef_cts):
        #eval_cts = [poly_eval_horner(coef_cts, e) * int(random(pk['order'])) + e for e in server_set]
        eval_cts = [poly_eval_horner(coef_cts, e) + e for e in server_set]

        return eval_cts

    def client_output(self, eval_cts, pk, sk, client_set):
        g = pk['g']
        x = sk['x']
        #el = ElGamal()

        eval_exps = [ct.c2 * ((ct.c1 ** x) ** -1) for ct in eval_cts]
        #print(eval_exps[0] == g ** client_set[0])
        intersection = [e for e in client_set if g ** e in eval_exps]

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

    psi = PSIElGamal()

    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)

    print('client output: {0}'.format(sorted(set(server_set) & set(client_set))))


if __name__ == '__main__':
    test()