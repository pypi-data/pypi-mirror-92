# MakeGradientDH()

Compute the gradient of a scalar function and return grids of the two horizontal components that conform with Driscoll and Healy's (1994) sampling theorem.

# Usage

```python
`theta`, `phi` = MakeGradientDH (`cilm`, [`lmax`, `sampling`, `lmax_calc`, `extend`])
```

# Returns

`theta` : float, dimension (nlat, nlong)
:   A 2D map of the theta component of the horizontal gradient that conforms to the sampling theorem of Driscoll and Healy (1994). If `sampling` is 1, the grid is equally sampled and is dimensioned as (`n` by `n`), where `n` is `2lmax+2`. If sampling is 2, the grid is equally spaced and is dimensioned as (`n` by 2`n`). The first latitudinal band of the grid corresponds to 90 N, the latitudinal sampling interval is 180/`n` degrees, and the default behavior is to exclude the latitudinal band for 90 S. The first longitudinal band of the grid is 0 E, by default the longitudinal band for 360 E is not included, and the longitudinal sampling interval is 360/`n` for an equally sampled and 180/`n` for an equally spaced grid, respectively. If `extend` is 1, the longitudinal band for 360 E and the latitudinal band for 90 S will be included, which increases each of the dimensions of the grid by 1.

`phi` : float, dimension (nlat, nlong)
:   A 2D equally sampled or equally spaced grid of the phi component of the horizontal gradient.

# Parameters

`cilm` : float, dimension (2, `lmaxin`+1, `lmaxin`+1)
:   The real 4-pi normalized spherical harmonic coefficients of a scalar function. The coefficients c1lm and c2lm refer to the cosine and sine coefficients, respectively, with `c1lm=cilm[0,l,m]` and `c2lm=cilm[1,l,m]`.

`lmax` : optional, integer, default = `lmaxin`
:   The maximum spherical harmonic degree of the coefficients `cilm`. This determines the number of samples of the output grids, `n=2lmax+2`, and the latitudinal sampling interval, `90/(lmax+1)`.

`sampling` : optional, integer, default = 2
:   If 1 (default) the output grids are equally sampled (`n` by `n`). If 2, the grids are equally spaced (`n` by 2`n`).

`lmax_calc` : optional, integer, default = `lmax`
:   The maximum spherical harmonic degree used in evaluating the functions. This must be less than or equal to `lmax`.

`extend` : input, optional, bool, default = False
:   If True, compute the longitudinal band for 360 E and the latitudinal band for 90 S. This increases each of the dimensions of `griddh` by 1.

# Description

`MakeGradientDH` will compute the horizontal gradient of a scalar function on a sphere defined by the spherical harmonic coefficients `cilm`. The output grids of the theta and phi components of the gradient are either equally sampled (`n` by `n`) or equally spaced (`n` by 2`n`) in latitude and longitude. The gradient is given by the formula

`Grad F = 1/r dF/theta theta-hat + 1/(r sin theta) dF/dphi phi-hat`.

where theta is colatitude and phi is longitude. The radius r is taken from the degree zero coefficient of the input function.

The default is to use an input grid that is equally sampled (`n` by `n`), but this can be changed to use an equally spaced grid (`n` by 2`n`) by the optional argument `sampling`. The redundant longitudinal band for 360 E and the latitudinal band for 90 S are excluded by default, but these can be computed by specifying the optional argument `extend`.

# Reference

Driscoll, J.R. and D.M. Healy, Computing Fourier transforms and convolutions on the 2-sphere, Adv. Appl. Math., 15, 202-250, 1994.
