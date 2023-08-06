# SHReturnTapersM()

Calculate the eigenfunctions of the spherical-cap concentration problem for a single angular order.

# Usage

```python
`tapers`, `eigenvalues` = SHReturnTapersM (`theta0`, `lmax`, `m`, [`degrees`])
```

# Returns

`tapers` : float, dimension (`lmax`+1, `lmax`+1)
:   The spherical harmonic coefficients of the `lmax+1` localization windows, arranged in columns. The first and last rows of each column correspond to spherical harmonic degrees 0 and `lmax`, respectively, and the columns are arranged from best to worst concentrated. 

`eigenvalues` : float, dimension (`lmax`+1)
:   The concentration factors of the localization windows.

# Parameters

`theta0` : float
:   The angular radius of the spherical cap in radians.

`lmax` : integer
:   The spherical harmonic bandwidth of the localization windows.

`m` : integer
:   The angular order of the localization windows.

`degrees` : integer, optional, dimension (`lmax`+1), default = 1
:   List of degrees to use when computing the eigenfunctions. Only those degrees where `degrees[l]` is non-zero will be employed.

# Description

`SHReturnTapersM` will calculate the eigenfunctions of the spherical-cap concentration problem for a singule angular order. The 4pi normalized spherical harmonic coefficients of each window are given in the columns of `tapers`, and the corresponding concentration factors are given in `eigenvaules`. The columns of `tapers` are ordered from best to worst concentrated, and the first and last rows of each column correspond to spherical harmonic degrees 0 and `lmax`, respectively. The localization windows are normalized such that they have unit power. If the optional vector `degrees` is specified, then the eigenfunctions will be computed using only those degrees `l` where `degrees(l)` is not zero.

When possible, the eigenfunctions are calculated using the kernel of Grunbaum et al. 1982 and the eigenvalues are then calculated by integration using the definition of the space-concentration problem. Use of the Grunbaum et al. kernel is prefered over the space-concentration kernel as the eigenfunctions of the later are unreliable when there are several eigenvalues identical (within machine precision) to either 1 or zero. If, the optional parameter `degrees` is specified, and at least one element is zero for degrees greater or equal to abs(m), then the eigenfunctions and eigenvalues will instead be computed directly using the space-concentration kernel.

# References

Grunbaum, F. A., L. Longhi, and M. Perlstadt, Differential operators commuting with finite convolution integral operators: Some non-abelian examples, SIAM, J. Appl. Math. 42, 941-955, 1982.

Simons, F. J., F. A. Dahlen, and M. A. Wieczorek, Spatiospectral concentration on a sphere, `SIAM Review`, 48, 504-536, 2006.

Wieczorek, M. A. and F. J. Simons, Localized spectral analysis on the sphere, 
`Geophys. J. Int.`, 162, 655-675, 2005.
