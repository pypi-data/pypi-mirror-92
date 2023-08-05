# Necessary modules are imported
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class Rootfinding:

    # Bisection method
    @staticmethod
    def bisection(eps, func, a, b, Nmax, verbose=True):
        """
        The script takes in an absolute error tolerance eps, a defined function func,
        interval extremes a and b, and a maximum number of iterations Nmax,
        and returns an array pn of approximations to the root.
        """
        pn = np.zeros(Nmax)
        pn.fill(np.nan)
        sfa = np.sign(func(a))
        for ii in range(0, Nmax):
            pn[ii] = a + (b-a)/2.0
            if (b - a) < (2.0 * eps):
                if verbose:
                    print("The convergence tolerance has been met")
                    print("after {0:d} iterations".format(ii+1))
                pn = pn[~np.isnan(pn)]
                return pn
            sfp = np.sign(func(pn[ii]))
            if (sfa * sfp) < 0.0:
                b = pn[ii]
            else:
                a = pn[ii]
                sfa = np.sign(func(a))
        if verbose:
            print("The convergence tolerance has not been met")
            print("after Nmax = {0:d} iterations".format(Nmax))
        return pn

    # Newton's Method
    @staticmethod
    def newton(f, fp, po, Nmax, eps, verbose=True):
        """
        The script takes in a defined function f, the derivative of that function fp,
        an initial estimate po of the root, a maximum number of iterations Nmax,
        and an absolute error tolerance eps, and returns an array pn of approximations to the root.
        """
        def g(x, f, fp):
            gx = x - f(x)/fp(x)
            return gx
        pn = np.zeros(Nmax+1)
        pn.fill(np.nan)
        pn[0] = po
        for ii in range(1,Nmax+1):
            pn[ii] = g(pn[ii-1],f,fp)
            if abs(pn[ii] - pn[ii - 1]) < eps:
                if verbose:
                    print("The convergence tolerance has been met")
                    print("after {0:d} iterations".format(ii))
                    pn = pn[~np.isnan(pn)]
                    return pn
        if verbose:
            print("The convergence tolerance has not been met")
            print("after Nmax = {0:d} iterations".format(Nmax))
        return pn
