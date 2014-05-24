Private Set Intersection Library
================================

Increasing dependence on anytime-anywhere availability of data and the increasing fear of losing privacy
motivate the need for privacy-preserving techniques. One interesting and common problem occurs when two parties,
a server and a client, need to privately compute an intersection of their respective sets of data.
In doing so, one or both parties must obtain the intersection, while neither should learn any information
about the other set.

This library implements three private set intersection protocols based on polynomials evaluations and interpolations.
They are,

1. A 3-Round PSI Protocol Based on Paillier Encryption Scheme
2. A 2-Round PSI Protocol Based on Paillier Encryption Scheme
3. A 2-Round PSI Protocol Based on ElGamal Encryption Scheme

The first protocol is initiated by the server, whereas the second and third protocols are initiated by
the client. The Paillier encryption scheme is based on integer groups. Therefore, it requires a security parameter of
at least 1024 to be secure with respect to currently available computing power. On the other hand, ElGamal
encryption scheme is based on elliptic curve groups, which can provide comparable security only with a security
parameter of 160. This makes the third protocol above far more efficient than the other two.
Please refer to [this paper](http://link.springer.com/chapter/10.1007/978-3-642-14577-3_13) for more information
regarding the theory behind these protocols.
