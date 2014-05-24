Private Set Intersection Library
================================

Increasing dependence on anytime-anywhere availability of data and the increasing fear of losing privacy
motivate the need for privacy-preserving techniques. One interesting and common problem occurs when two parties,
a server and a client, need to privately compute an intersection of their respective sets of data.
In doing so, one or both parties must obtain the intersection, while neither should learn any information
about the other set.

This library implements three private set intersection protocols based on polynomials. They are

1. A 3-Round PSI Protocol Based on Paillier Encryption Scheme
2. A 2-Round PSI Protocol Based on Paillier Encryption Scheme
3. A 2-Round PSI Protocol Based on ElGamal Encryption Scheme

The first protocol is initiated by the server. On the other hand, the second and third protocols are initiated by
the client.
