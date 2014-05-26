__author__ = 'Milinda Perera'


def poly_from_roots(roots, neg_one, one):
    """
    Interpolates the unique polynomial that encodes the given roots.
    The function also requires the one and the negative one of the underlying ring.
    """
    zero = one + neg_one
    coefs = [neg_one * roots[0], one]
    for r in roots[1:]:
        coefs = poly_mul(coefs, [neg_one * r, one], zero)
    return coefs


def poly_eval(coefs, x):
    """
    Evaluates the polynomial whose coefficients are given in coefs on the value x.
    Polynomial coefficient are stored in coefs from the lowest power to the highest.
    x is required to be a ring element.
    """
    out = 0
    for i in range(len(coefs)):
        out = coefs[i] * (x ** i) + out
    return out


def poly_eval_horner(coefs, x):
    """
    Evaluates the polynomial whose coefficients are given in coefs on the value x
    using the Horner's method. This function is much faster than regular polynomial evaluation.
    Polynomial coefficient are stored in coefs from the lowest power to the highest.
    x is required to be a ring element.
    """
    out = 0
    for c in reversed(coefs):
        out = c + out * x
    return out


def poly_mul(coefs1, coefs2, zero):
    """
    Multiplies two polynomials whose coefficients are given in coefs1 and coefs2.
    Zero value of the underlying ring is required on the input zero.
    """
    coefs3 = [zero] * (len(coefs1) + len(coefs2) - 1)
    for i in range(len(coefs1)):
        for j in range(len(coefs2)):
            coefs3[i + j] += coefs1[i] * coefs2[j]
    return coefs3


def poly_print(coefs):
    """Prints the polynomial whose coefficients are given in coefs in human readable form."""
    out = [poly_coef_to_str(int(coefs[i]), i) for i in range(len(coefs)) if coefs[i] != 0 or i == 0]
    out.reverse()
    if out[0][0] == '+':
        del out[0][0]
    return ' '.join([' '.join(l) for l in out])


def poly_coef_to_str(coef, degree):
    """A helper function for poly_print."""
    out = []
    if coef < 0:
        out.append('-')
    else:
        out.append('+')
    if abs(coef) != 1 or degree == 0:
        out.append(str(abs(coef)))
    if degree == 1:
        out.append('X')
    elif degree > 1:
        out.append('X^' + str(degree))
    return out
