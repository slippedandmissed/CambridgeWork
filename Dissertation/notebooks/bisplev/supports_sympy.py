#!/usr/bin/python3.11
from tqdm import tqdm
import numpy as np
import sympy


def lazy_array_access(arr, i, verbose=False):
    return sympy.Piecewise(
        *list((
            x,
            sympy.simplify(sympy.Eq(i, idx)),
        ) for idx, x in tqdm(enumerate(arr), total=len(arr), leave=False, disable=not verbose)),
    )


def fpbisp(tx, ty, c, kx, ky, x, y, verbose=False):
    nx = len(tx)
    ny = len(ty)

    arg = sympy.Max(tx[kx], sympy.Min(tx[nx - kx - 1], x))
    l = sympy.Piecewise(
        *list((
            l_,
            arg < tx[l_]
        ) for l_ in range(kx+1, nx-kx-1)),
        (kx+1, True)
    )

    if verbose:
        print("Calculating wx...")
    wx = fpbspl(tx, kx, arg, l, verbose)

    lx = l-kx-1

    arg = sympy.Max(ty[ky], sympy.Min(ty[ny - ky - 1], y))
    l = sympy.Piecewise(
        *list((
            l_,
            arg < ty[l_]
        ) for l_ in range(ky+1, ny-ky-1)),
        (ky+1, True)
    )

    if verbose:
        print("Calculating wy...")
    wy = fpbspl(ty, ky, arg, l, verbose)

    ly = l-ky-1

    l = lx*(ny-ky-1)

    l1 = l+ly - 1
    sp = 0

    if verbose:
        print("Calculating c...")
    c_laz_idx = sympy.Dummy("idx")
    c_laz = lazy_array_access(c, l1+c_laz_idx, verbose)

    if verbose:
        print("Calculating z...")
    with tqdm(total=(kx+1)*(ky+1), leave=False, disable=not verbose) as pbar:
        for i1 in range(kx+1):
            for j1 in range(ky + 1):
                sp += \
                    c_laz.subs(c_laz_idx, (ny-ky-1)*i1 + j1 + 1) * \
                    wx[i1] * \
                    wy[j1]

                pbar.update()

    return sp


def fpbspl(t, k, x, l, verbose=False):
    n = len(t)
    h = np.empty((k+1,), dtype=float if type(x) == float else object)

    h[0] = 1
    t_laz_idx = sympy.Dummy("idx")
    t_laz = lazy_array_access(t, l+t_laz_idx, verbose)
    for j in range(k):
        hh = np.copy(h[:j+1])
        h[0] = 0
        for i in range(j+1):
            tli = t_laz.subs(t_laz_idx, i)
            tlj = t_laz.subs(t_laz_idx, i-j-1)

            h[i+1] = sympy.Piecewise(
                (
                    (hh[i]/(tli-tlj))*(x-tlj),
                    tli != tlj
                ),
                (
                    0,
                    True
                )
            )

            h[i] = sympy.Piecewise(
                (
                    h[i]+(hh[i]/(tli-tlj))*(tli-x),
                    tli != tlj
                ),
                (
                    h[i],
                    True
                )
            )
    return h


if __name__ == "__main__":
    import scipy.interpolate

    tx = np.array([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0])
    ty = np.array([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0])
    c = np.array([0.5441782868946293, 0.6414689432409043, 0.15847770134394368, 0.853485388631803, -0.4558858656867021, 1.8954963147112343, 0.11693246052436726, 0.1498908637442094,
                  1.0678254770798374, 0.07342346504069706, 0.6705066478961692, 0.6185878670979407, 0.45189041094655674, 0.36703444824915105, 0.33578873667447073, 0.522899717923794])
    kx = 3
    ky = 3

    x = 0.1
    y = 0.1

    A = scipy.interpolate.bisplev(x, y, (tx, ty, c, kx, ky))
    B = float(fpbisp(tx, ty, c, kx, ky, x, y))

    print(A)
    print(B)

    assert np.isclose(A, B)

    xsymb, ysymb = sympy.symbols("x y")
    formula = fpbisp(tx, ty, c, kx, ky, xsymb, ysymb, verbose=True)
    func = sympy.lambdify((xsymb, ysymb), formula)
    C = float(func(x,y))


    print(C)
    print(formula)

    assert np.isclose(A, C)
