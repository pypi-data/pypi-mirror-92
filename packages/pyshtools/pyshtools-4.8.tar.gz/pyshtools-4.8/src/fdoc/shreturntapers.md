# SHReturnTapers

Calculate the eigenfunctions of the spherical-cap concentration problem.

# Usage

call SHReturnTapers (`theta0`, `lmax`, `tapers`, `eigenvalues`, `taper_order`, `degrees`, `exitstatus`)

# Parameters

`theta0` : input, real(dp)
:   The angular radius of the spherical cap in radians.

`lmax` : input, integer(int32)
:   The spherical harmonic bandwidth of the localization windows.

`tapers` : output, real(dp), dimension (`lmax`+1, (`lmax`+1)\*\*2)
:   The spherical harmonic coefficients of the `(lmax+1)**2` localization windows. Each column contains the coefficients of a single window that possesses non-zero coefficients for the single angular order specified in `taper_order`. The first and last rows of each column correspond to spherical harmonic degrees 0 and `lmax`, respectively, and the columns are arranged from best to worst concentrated.

`eigenvalues` : output, real(dp), dimension ((`lmax`+1)\*\*2)
:   The concentration factors of the localization windows.

`taper_order` : output, integer(int32), dimension ((`lmax`+1)\*\*2)
:   The angular order of the non-zero spherical harmonic coefficients in each column of `tapers`.

`degrees` : input, integer(int32), optional, dimension (`lmax`+1)
:   List of degrees to use when computing the eigenfunctions. Only those degrees where `degrees(l+1)` is non-zero will be employed.

`exitstatus` : output, optional, integer(int32)
:   If present, instead of executing a STOP when an error is encountered, the variable exitstatus will be returned describing the error. 0 = No errors; 1 = Improper dimensions of input array; 2 = Improper bounds for input variable; 3 = Error allocating memory; 4 = File IO error.

# Description

`SHReturnTapers` will calculate the eigenfunctions of the spherical-cap concentration problem. Each column of the matrix `tapers` contains the spherical harmonic coefficients of a single window and the corresponding concentration factor is given in the array `eigenvalues`. Each window has non-zero coefficients for only a single angular order that is specified in `taper_order`: all other spherical harmonic coefficients for a given window are identically zero. The columns of `tapers` are ordered from best to worst concentrated, and the first and last rows of each column correspond to spherical harmonic degrees 0 and `lmax`, respectively. The localization windows are normalized such that they have unit power. If the optional vector `degrees` is specified, then the eigenfunctions will be computed using only those degrees where `degrees(l+1)` is not zero.

When possible, the eigenfunctions are calculated using the kernel of Grunbaum et al. 1982 and the eigenvalues are then calculated by integration using the definition of the space-concentration problem. Use of the Grunbaum et al. kernel is prefered over the space-concentration kernel as the eigenfunctions of the later are unreliable when there are several eigenvalues identical (within machine precision) to either 1 or zero. If, the optional parameter `degrees` is specified, and at least one element is zero for degrees greater or equal to abs(m), then the eigenfunctions and eigenvalues will instead be computed directly using the space-concentration kernel.

# References

Grunbaum, F. A., L. Longhi, and M. Perlstadt, Differential operators commuting with finite convolution integral operators: Some non-abelian examples, SIAM, J. Appl. Math. 42, 941-955, 1982.

Simons, F. J., F. A. Dahlen, and M. A. Wieczorek, Spatiospectral concentration on a sphere, SIAM Review, 48, 504-536, 2006.

Wieczorek, M. A. and F. J. Simons, Localized spectral analysis on the sphere, 
Geophys. J. Int., 162, 655-675, 2005.

# See also

[shreturntapersm](shreturntapersm.html), [computedg82](computedg82.html), [computedm](computedm.html)
