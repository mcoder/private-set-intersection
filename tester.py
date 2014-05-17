__author__ = 'Milinda Perera'

import random as pyrandom

from psi_3_round_paillier import PSI3RoundPaillier
from psi_2_round_paillier import PSI2RoundPaillier
from psi_2_round_elgamal import PSI2RoundElGamal


def run_psi_3_round_paillier(server_set, client_set):
    psi = PSI3RoundPaillier(1024)
    server_out_1, server_state = psi.server_to_client_1(server_set)
    client_out_1 = psi.client_to_server(client_set, **server_out_1)
    server_out_2 = psi.server_to_client_2(client_out_1, **server_state)
    client_out_2 = psi.client_output(server_out_2)
    return client_out_2


def run_psi_2_round_paillier(server_set, client_set):
    psi = PSI2RoundPaillier(1024)
    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)
    return client_out_2


def run_psi_2_round_elgamal(server_set, client_set):
    psi = PSI2RoundElGamal()
    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)
    return client_out_2


if __name__ == '__main__':
    set_len = 20  #input('Input set length: ')
    intersection_len = 5  #input('Input intersection length: ')
    server_set = list(set([pyrandom.randint(1, 200) for i in range(100)]))[:set_len]
    client_set = list(set([pyrandom.randint(201, 400) for i in range(100)]))[:set_len - intersection_len]
    client_set += server_set[:intersection_len]

    print('server set: {0}'.format(sorted(server_set)))
    print('client set: {0}'.format(sorted(client_set)))
    print('intersection: {0}'.format(sorted(set(server_set) & set(client_set))))
    print

    psi_3_round_paillier_result = run_psi_3_round_paillier(server_set, client_set)
    print('PSI3RoundPaillier output: {0}'.format(psi_3_round_paillier_result))
    print

    psi_2_round_paillier_result = run_psi_2_round_paillier(server_set, client_set)
    print('PSI2RoundPaillier output: {0}'.format(psi_2_round_paillier_result))
    print

    psi_2_round_elgamal_result = run_psi_2_round_elgamal(server_set, client_set)
    print('PSI2RoundElGamal output: {0}'.format(psi_2_round_elgamal_result))
    print