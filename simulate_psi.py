__author__ = 'Milinda Perera'

import random as pyrandom
from time import time

from lib.psi_3_round_paillier import PSI3RoundPaillier
from lib.psi_2_round_paillier import PSI2RoundPaillier
from lib.psi_2_round_elgamal import PSI2RoundElGamal


def timer(func, *pargs, **kargs):
    """
    Measures the time required to run func with the given parameters.
    Returns the time as well as the result of the computation.
    """
    start = time()
    ret = func(*pargs, **kargs)
    elapsed = time() - start
    return elapsed, ret


def run_psi_3_round_paillier(server_set, client_set):
    """
    Simulates the 3-round PSI protocol based on Paillier encryption scheme
    on the given server and client sets. Returns the final output of the client.
    """
    psi = PSI3RoundPaillier(1024)
    server_out_1, server_state = psi.server_to_client_1(server_set)
    client_out_1 = psi.client_to_server(client_set, **server_out_1)
    server_out_2 = psi.server_to_client_2(client_out_1, **server_state)
    client_out_2 = psi.client_output(server_out_2)
    return client_out_2


def run_psi_2_round_paillier(server_set, client_set):
    """
    Simulates the 2-round PSI protocol based on Paillier encryption scheme
    on the given server and client sets. Returns the final output of the client.
    """
    psi = PSI2RoundPaillier(1024)
    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)
    return client_out_2


def run_psi_2_round_elgamal(server_set, client_set):
    """
    Simulates the 2-round PSI protocol based on ElGamal encryption scheme
    on the given server and client sets. Returns the final output of the client.
    """
    psi = PSI2RoundElGamal()
    client_out_1, client_state = psi.client_to_server(client_set)
    server_out = psi.server_to_client(server_set, **client_out_1)
    client_out_2 = psi.client_output(server_out, **client_state)
    return client_out_2


if __name__ == '__main__':
    # Obtain the server and client set lengths as well as the intersection length from the user.
    set_len = input('Input set length: ')
    intersection_len = input('Input intersection length: ')

    # Generate server and client sets with above parameters.
    server_set = []
    client_set = []
    while not (len(client_set) == len(server_set) == set_len):
        server_set = list(set([pyrandom.randint(1, set_len * 10) for i in range(set_len * 5)]))[:set_len]
        client_set = list(set([pyrandom.randint(set_len * 10, set_len * 20) for i in range(set_len * 5)]))[:set_len - intersection_len] + server_set[:intersection_len]

    # Print generated sets as well as their intersection for comparison purposes.
    print
    print('server set: {0}'.format(sorted(server_set)))
    print('client set: {0}'.format(sorted(client_set)))
    print('intersection: {0}'.format(sorted(set(server_set) & set(client_set))))
    print

    sims = [['PSI3RoundPaillier', run_psi_3_round_paillier],
            ['PSI2RoundPaillier', run_psi_2_round_paillier],
            ['PSI2RoundElGamal', run_psi_2_round_elgamal]]

    # Simulate the protocols and report results.
    for sim in sims:
        time_taken, result = timer(sim[1], server_set, client_set)
        print('{0} output: {1}'.format(sim[0], sorted(result)))
        print('{0} time: {1}'.format(sim[0], time_taken))
        print