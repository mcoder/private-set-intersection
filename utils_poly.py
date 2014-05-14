from charm.toolbox.integergroup import integer


def poly_eval(coefs, x):
    out = 0
    for i in range(len(coefs)):
        out = coefs[i] * (x ** i) + out
    return out


def poly_eval_horner(coefs, x):
    out = 0
    for c in reversed(coefs):
        out = c + out * x
    return out


def poly_mul(coefs1, coefs2):
    coefs3 = [0] * (len(coefs1) + len(coefs2) - 1)
    for i in range(len(coefs1)):
        for j in range(len(coefs2)):
            coefs3[i + j] += coefs1[i] * coefs2[j]
    return coefs3


def poly_from_roots(roots):
    coefs = [-1 * roots[0], 1]
    for r in roots[1:]:
        coefs = poly_mul(coefs, [-1 * r, 1])
    return coefs


def poly_print(coefs):
    out = [poly_coef_to_str(int(coefs[i]), i) for i in range(len(coefs)) if coefs[i] != 0]
    out.reverse()
    if out[0][0] == '+':
        del out[0][0]
    print(' '.join([' '.join(l) for l in out]))


def poly_coef_to_str(coef, degree):
    out = []
    if coef < 0:
        out.append('-')
    else:
        out.append('+')
    if abs(coef) != 1:
        out.append(str(abs(coef)))
    if degree == 1:
        out.append('X')
    elif degree > 1:
        out.append('X^' + str(degree))
    return out


def test_poly():
    coefs1 = map(integer, [-1, -2])
    coefs2 = [3, 4]
    coefs3 = poly_mul(coefs1, coefs2)
    poly_print(coefs3)

    roots = [2, 3, 4, 5]
    roots = map(integer, roots)
    coefs = poly_from_roots(roots)
    eval1 = poly_eval(coefs, 3)
    eval2 = poly_eval_horner(coefs, 3)
    poly_print(coefs)
    print(eval1)
    print(eval2)


if __name__ == '__main__':
    test_poly()