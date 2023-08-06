#!/usr/bin/env python3
"""
This script tests the SHMTCouplingMatrix routine
"""
import numpy as np

import pyshtools
from pyshtools import shtools

pyshtools.utils.figstyle()


def main():
    test_CouplingMatrix()


def test_CouplingMatrix():
    print('\n---- testing SHMTCouplingMatrix ----')
    lmax = 30
    lwin = 10
    nwins = 1

    sqrt_taper_power = np.zeros((lwin+1, nwins))
    sqrt_taper_power[:, 0] = np.hanning(lwin+1)
    Mmt = shtools.SHMTCouplingMatrix(lmax, sqrt_taper_power)
    print(Mmt)


# ==== EXECUTE SCRIPT ====
if __name__ == "__main__":
    main()
