# SHCrossPowerL

Compute the cross-power of two real functions for a single spherical harmonic degree.

# Usage

`cpower` = SHCrossPowerL (`cilm1`, `cilm2`, `l`)

# Parameters

`cpower` : output, real(dp)
:   The cross power of the two functions for spherical harmonic degree `l`.

`cilm1` : input, real(dp), dimension (2, `lmaxin1`+1, `lmaxin1`+1)
:   The spherical harmonic coefficients of the first function.

`cilm2` : input, real(dp), dimension (2, `lmaxin2`+1, `lmaxin2`+1)
:   The spherical harmonic coefficients of the second function.

`l` : input, integer(int32)
:   The spherical harmonic degree. This must be less than or equal to the minimum of `lmaxin1` and `lmaxin2`.

# Description

`SHCrossPowerL` will calculate the cross-power of two functions expressed in 4-pi normalized spherical harmonics for a single spherical harmonic degree `l`. This is explicitly calculated as:

`cpower = Sum_{i=1}^2 Sum_{m=0}^l cilm1(i, l+1, m+1) * cilm2(i, l+1, m+1)`.

# See also

[shpowerl](shpowerl.html), [shpowerdensityl](shpowerdensityl.html), [shcrosspowerdensityl](shcrosspowerdensityl.html), [shpowerspectrum](shpowerspectrum.html), [shpowerspectrumdensity](shpowerspectrumdensity.html), [shcrosspowerspectrum](shcrosspowerspectrum.html), [shcrosspowerspectrumdensity](shcrosspowerspectrumdensity.html), [shadmitcorr](shadmitcorr.html)
