Private Set Intersection Library
================================

Increasing dependence on anytime-anywhere availability of data and the increasing fear of losing privacy
motivate the need for privacy-preserving techniques. One interesting and common problem occurs when two parties,
a server and a client, need to privately compute an intersection of their respective sets of data.
In doing so, one or both parties must obtain the intersection, while neither should learn any information
about the other set.

This library implements three private set intersection (PSI) protocols based on oblivious polynomials evaluations and
interpolations. At the completion of each of these protocols, only the client learns the intersection.
The protocols are,

1. A 3-Round PSI Protocol Based on Paillier Encryption Scheme
2. A 2-Round PSI Protocol Based on Paillier Encryption Scheme
3. A 2-Round PSI Protocol Based on ElGamal Encryption Scheme

The first protocol is initiated by the server, whereas the second and third protocols are initiated by
the client. The Paillier encryption scheme is based on integer groups. Therefore, it requires a security parameter of
at least 1024 to be secure with respect to currently available computing power. On the other hand, ElGamal
encryption scheme is based on elliptic curve groups, which can provide comparable security only with a security
parameter of 160. This makes the third protocol far more efficient than the other two.
Please refer to [this paper](http://link.springer.com/chapter/10.1007/978-3-642-14577-3_13) for more information
regarding the theory behind these protocols.

Some information about the included files are as follows.

**1. simulate_psi.py:**

This script simulates the three PSI protocols. The script first asks the user for the length of the server and
client sets as well as the length of their intersection. Next, it generates those sets by randomly picking
integers. Finally, it runs the three PSI protocols on the two sets and reports the output. It also measures
the time required to execute each protocol and reports that result as well. One can run this script by executing
the following command.

`python simulate_psi.py`

**2. sample_simulation.txt**

This file contains the output of a single run of the simulate_psi.py script.

**3. psi_3_round_paillier.py, 4. psi_2_round_paillier.py, 5. psi_2_round_elgamal.py**

These modules contain the classes that implement the three PSI protocols.

**6. utils_poly.py**

This module consists of polynomial interpolation and evaluation functions. These functions are defined general
enough to work on any type of ring elements such as integer rings, polynomial rings, etc. In other words, the input
type is only required to have addition and multiplication operations implemented, and the designer of the input
type is given complete freedom to build those operations.

**7. pkenc_paillier.py**

This module contains the class that implements the [Paillier cryptosystem](http://en.wikipedia.org/wiki/Paillier_cryptosystem).
Also defined in this module is a class for Paillier ciphertexts that abstract away the homomorphic properties of
the Paillier cryptosystem.

**8. pkenc_elgamal.py**

This module provides the class that implements a variant of the [ElGamal cryptosystem](http://en.wikipedia.org/wiki/ElGamal)
that provides the homorphic properties required for oblivious polynomial evaluations. More specifically, the encryption of
a message `m` maps it to the group element `g^m`. This allows one to perform homomorphic addition and multiplication (by a constant)
in the exponent. Unfortunately, this mapping makes it hard to decrypt ciphertexts efficiently. Nevertheless, it suffices for
our purposes.

**9. unittests.py**

This script consists of the unit tests created for testing purposes. One can run this script by executing the following command.

`python unittests.py`