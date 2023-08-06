#!/usr/bin/env python3
"""
This script is a python version of TimingAccuracyDHC. We use numpy functions to
simplify the creation of random coefficients.
"""
import time
import numpy as np

from pyshtools import expand
from pyshtools import spectralanalysis


# ==== MAIN FUNCTION ====

def main():
    TimingAccuracyDHC(2)


# ==== TEST FUNCTIONS ====

def TimingAccuracyDHC(sampling=1):
    # ---- input parameters ----
    maxdeg = 2800
    ls = np.arange(maxdeg + 1)
    beta = 1.5
    print('Driscoll-Healy (complex), sampling =', sampling)

    # ---- create mask to filter out m<=l ----
    mask = np.zeros((2, maxdeg + 1, maxdeg + 1), dtype=np.bool)
    mask[0, 0, 0] = True
    for l in ls:
        mask[:, l, :l + 1] = True
    mask[1, :, 0] = False

    # ---- create Gaussian powerlaw coefficients ----
    print('creating {:d} random coefficients'.format(2 * (maxdeg + 1) *
                                                     (maxdeg + 1)))
    np.random.seed(0)
    cilm = np.zeros((2, (maxdeg + 1), (maxdeg + 1)), dtype=np.complex)
    cilm.imag = np.random.normal(loc=0., scale=1.,
                                 size=(2, maxdeg + 1, maxdeg + 1))
    cilm.real = np.random.normal(loc=0., scale=1.,
                                 size=(2, maxdeg + 1, maxdeg + 1))
    old_power = spectralanalysis.spectrum(cilm)
    new_power = 1. / (1. + ls)**beta  # initialize degrees > 0 to power-law
    cilm[:, :, :] *= np.sqrt(new_power / old_power)[None, :, None]
    cilm[~mask] = 0.

    # ---- time spherical harmonics transform for lmax set to increasing
    # ---- powers of 2
    lmax = 2
    print('lmax    maxerror    rms         tinverse    tforward')
    while lmax <= maxdeg:
        # trim coefficients to lmax
        cilm_trim = cilm[:, :lmax + 1, :lmax + 1]
        mask_trim = mask[:, :lmax + 1, :lmax + 1]

        # synthesis / inverse
        tstart = time.time()
        grid = expand.MakeGridDHC(cilm_trim, sampling=sampling)
        tend = time.time()
        tinverse = tend - tstart

        # analysis / forward
        tstart = time.time()
        cilm2_trim = expand.SHExpandDHC(grid, sampling=sampling)
        tend = time.time()
        tforward = tend - tstart

        # compute error
        err = np.abs(cilm_trim[mask_trim] - cilm2_trim[mask_trim]) / \
            np.abs(cilm_trim[mask_trim])
        maxerr = err.max()
        rmserr = np.mean(err**2)

        print('{:4d}    {:1.2e}    {:1.2e}    {:1.1e}s    {:1.1e}s'.format(
            lmax, maxerr, rmserr, tinverse, tforward))

        if maxerr > 100.:
            raise RuntimeError('Tests Failed. Maximum relative error = ',
                               maxerr)

        lmax = lmax * 2


# ==== EXECUTE SCRIPT ====
if __name__ == "__main__":
    main()
