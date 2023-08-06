# ComputeDM()

Compute the space-concentration kernel of a spherical cap.

# Usage

```python
`dm` = ComputeDM (`lmax`, `m`, `theta0`, [`degrees`])
```

# Returns

`dm` : float, dimension (`lmax`+1, `lmax`+1)
:   The space-concentration kernel or angular order `m`.

# Parameters

`lmax` : integer
:   The spherical harmonic bandwidth of the windows.

`m` : integer
:   The angular order of the concentration problem.

`theta0` : float
:   The angular radius of the spherical cap in radians.

`degrees` : integer, optional, dimension (`lmax`+1), default = 1
:   List of degrees to use when computing the space-concentration kernel. Only those degrees where `degrees[l]` is non-zero will be employed.

# Description

`ComputeDM` will calculate the space-concentration kernel of angular order `m` for the spherical-cap concentration problem. The eigenfunctions of this matrix correspond to a family of orthogonal windowing functions, and the eigenvalues correspond to the window's concentration factor (i.e., the power of the window within `theta0` divided by the total power of the function). It is assumed that the employed spherical harmonic functions are normalized to the same value for all degrees and angular orders, which is the case for both the geodesy 4-pi and orthonormalized harmonics. This kernel is symmetric and is computed exactly by Gauss-Legendre quadrature. If the optional vector `degrees` is specified, then the matrix will be computed only for elements where `degrees(l)` is not zero.

# References

Simons, F.J., F.A. Dahlen, and M.A. Wieczorek, Spatiospectral concentration on a sphere, SIAM Review, 48, 504-536, 2006.
