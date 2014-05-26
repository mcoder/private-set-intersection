__author__ = 'Milinda Perera'

from charm.toolbox.integergroup import random, integer

from pkenc_elgamal_exp import ElGamalExp
from utils_poly import poly_eval_horner, poly_from_roots


class PSI2RoundElGamal(object):
    """
    Implements the 2-round PSI protocol based on ElGamal cryptosystem
    """

    def client_to_server(self, client_set):
        # Initialize the cryptosystem.
        enc_scheme = ElGamalExp()
        pk, sk = enc_scheme.keygen()

        # Map the client set to the ring of ElGamal exponents, interpolate the unique
        # polynomial representing the set, and encrypt its coefficients.
        set_a_mapped = [integer(a, pk['order']) for a in client_set]
        coefs = poly_from_roots(set_a_mapped, integer(-1, pk['order']), integer(1, pk['order']))
        coef_cts = [enc_scheme.encrypt(pk, int(c)) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        client_state = {'pk': pk, 'sk': sk, 'client_set': client_set}

        return out, client_state

    def server_to_client(self, server_set, pk, coef_cts):
        # Evaluate the polynomial on each element of the server set.
        eval_cts = [poly_eval_horner(coef_cts, e) * int(random(pk['order'])) + e for e in server_set]

        return eval_cts

    def client_output(self, eval_cts, pk, sk, client_set):
        g, order = pk['g'], pk['order']
        x = sk['x']

        eval_exps = [ct.c2 * ((ct.c1 ** x) ** -1) for ct in eval_cts]
        intersection = [e for e in client_set if g ** (e % order) in eval_exps]

        return intersection
