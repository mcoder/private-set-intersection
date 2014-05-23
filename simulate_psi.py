__author__ = 'Milinda Perera'

import random as pyrandom
from time import time

from psi_3_round_paillier import PSI3RoundPaillier
from psi_2_round_paillier import PSI2RoundPaillier
from psi_2_round_elgamal import PSI2RoundElGamal


def timer(func, *pargs, **kargs):
    start = time()
    ret = func(*pargs, **kargs)
    elapsed = time() - start
    return elapsed, ret


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
    set_len = input('Input set length: ')
    intersection_len = input('Input intersection length: ')

    server_set = []
    client_set = []
    while not (len(client_set) == len(server_set) == set_len):
        server_set = list(set([pyrandom.randint(1, set_len * 10) for i in range(set_len * 5)]))[:set_len]
        client_set = list(set([pyrandom.randint(set_len * 10, set_len * 20) for i in range(set_len * 5)]))[
                     :set_len - intersection_len] + server_set[:intersection_len]

    print
    print('server set: {0}'.format(sorted(server_set)))
    print('client set: {0}'.format(sorted(client_set)))
    print('intersection: {0}'.format(sorted(set(server_set) & set(client_set))))
    print

    tests = [['PSI3RoundPaillier', run_psi_3_round_paillier],
             ['PSI2RoundPaillier', run_psi_2_round_paillier],
             ['PSI2RoundElGamal', run_psi_2_round_elgamal]]

    for test in tests:
        time_taken, result = timer(test[1], server_set, client_set)
        print('{0} output: {1}'.format(test[0], sorted(result)))
        print('{0} time: {1}'.format(test[0], time_taken))
        print