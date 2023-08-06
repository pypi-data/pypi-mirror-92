# MakeGeoidGridDH()

Create a global map of the geoid.

# Usage

```python
`geoid` = MakeGeoidGridDH (`cilm`, `r0`, `gm`, `potref`, [`lmax`, `omega`, `r`, `order`, `lmax_calc`, `a`, `f`, `sampling`, `extend`])
```

# Returns

`geoid` : float, dimension (nlat, nlong)
:   A global grid of the height to the potential `potref` above a flattened ellipsoid of equatorial radius `a` and flattening `f`, where the grid conforms to the sampling theorem of Driscoll and Healy (1994). If `sampling` is 1, the grid is equally sampled and is dimensioned as (`n` by `n`), where `n` is `2lmax+2`. If sampling is 2, the grid is equally spaced and is dimensioned as (`n` by 2`n`). The first latitudinal band of the grid corresponds to 90 N, the latitudinal sampling interval is 180/`n` degrees, and the default behavior is to exclude the latitudinal band for 90 S. The first longitudinal band of the grid is 0 E, by default the longitudinal band for 360 E is not included, and the longitudinal sampling interval is 360/`n` for an equally sampled and 180/`n` for an equally spaced grid, respectively. If `extend` is 1, the longitudinal band for 360 E and the latitudinal band for 90 S will be included, which increases each of the dimensions of the grid by 1.

# Parameters

`cilm` : float, dimension (2, `lmaxin`+1, `lmaxin`+1)
:   The real spherical harmonic coefficients (geodesy normalized) of the gravitational potential referenced to a spherical interface of radius `r0`.

`r0` : float
:   The reference radius of the spherical harmonic coefficients.

`gm` : float
:   The product of the gravitational constant and mass of the planet.

`potref` : float
:   The value of the potential on the chosen geoid, in SI units.

`lmax` : optional, integer, default = `lmaxin`
:   The maximum spherical harmonic degree of the gravitational-potential coefficients. This determines the number of latitudinal and longitudinal samples.

`omega` : optional, float, default = 0
:   The angular rotation rate of the planet.

`r` : optional, float, default = `r0`
:   The radius of the reference sphere that the Taylor expansion of the potential is performed on.

`order` : optional, integer, default = 2
:   The order of the Taylor series expansion of the potential about the reference radius `r`. This can be either 1, 2, or 3.

`lmax_calc` : optional, integer, default = `lmax`
:   The maximum degree used in evaluating the spherical harmonic coefficients. This must be less than or equal to `lmax`.

`a` : optional, float, default = `r0`
:   The semi-major axis of the flattened ellipsoid that the output grid `geoid` is referenced to. The optional parameter `f` must also be specified.

`f` : optional, float, default = 0
:   The flattening `(R_equator-R_pole)/R_equator` of the reference ellipsoid. The optional parameter `a` (i.e., `R_equator`) must be specified.

`sampling` : optional, integer, default = 2
:   If 1 (default) the output grids are equally sampled (`n` by `n`). If 2, the grids are equally spaced (`n` by 2`n`).

`extend` : input, optional, bool, default = False
:   If True, compute the longitudinal band corresponding to 360 E for `gridtype` 1, 2 and 3, and compute the latitudinal band for 90 S for `gridtype` 2 and 3.

# Description

`MakeGeoidGrid` will create a global map of the geoid, accurate to either first, second, or third order, using the method described in Wieczorek (2007; equation 19-20). The algorithm expands the potential in a Taylor series on a spherical interface of radius `r`, and computes the height above this interface to the potential `potref` exactly from the linear, quadratic, or cubic equation at each grid point. If the optional parameters `a` and `f` are specified, the geoid height will be referenced to a flattened ellipsoid with semi-major axis `a` and flattening `f`. The pseudo-rotational potential is explicitly accounted for by specifying the angular rotation rate `omega` of the planet.

It should be noted that this geoid calculation is only strictly exact when the radius `r` lies above the maximum radius of the planet. Furthermore, the geoid is only strictly valid when it lies above the surface of the planet (it is necessary to know the density structure of the planet when calculating the potential below the surface).

The default is to use an input grid that is equally sampled (`n` by `n`), but this can be changed to use an equally spaced grid (`n` by 2`n`) by the optional argument `sampling`. The redundant longitudinal band for 360 E and the latitudinal band for 90 S are excluded by default, but these can be computed by specifying the optional argument `extend`.

# References

Driscoll, J.R. and D.M. Healy, Computing Fourier transforms and convolutions on the 2-sphere, Adv. Appl. Math., 15, 202-250, 1994.

Wieczorek, M. A. Gravity and topography of the terrestrial planets, Treatise on Geophysics, 10, 165-206, 2007.
