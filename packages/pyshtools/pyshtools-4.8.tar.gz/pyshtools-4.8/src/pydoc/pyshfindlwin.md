# SHFindLWin()

Determine the spherical-harmonic bandwidth that is necessary to achieve a certain concentration factor.

# Usage

```python
`lwin` = SHFindLWin (`theta0`, `m`, `alpha`, [`taper_number`])
```

# Returns

`lwin` : integer
:   The spherical harmonic bandwidth

# Parameters

`theta0` : float
:   The angular radius of the spherical cap in radians.

`m` : integer
:   The angular order of the taper.

`alpha` : float
:   The desired concentration factor of the window. This must lie between 0 and 1.

`taper_number` : optional, integer, default = 1
:   The taper number corresponding to the angular order `m`. The default is to use the first taper.

# Description

`SHFindLWin` will determine the spherical harmonic bandwidth that is required for a window of the spherical-cap concentration problem to achive a certain concentration factor. By default, the first taper corresponding to the angular order `m` will be used, but this can be modified by specifying the optional argument `taper_number`. 

# References

Wieczorek, M. A. and F. J. Simons, Localized spectral analysis on the sphere, 
Geophys. J. Int., 162, 655-675, 2005.
