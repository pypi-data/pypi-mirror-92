# SHSCouplingMatrixCap()

This routine returns the spherical harmonic coupling matrix for a given set of spherical-cap Slepian basis functions. This matrix relates the power spectrum expectation of the function expressed in a subset of the best-localized Slepian functions to the expectation of the global power spectrum.

# Usage

```python
`kij` = SHSCouplingMatrixCap (`galpha`, `galpha_order`, `nmax`)
```

# Returns

`kij` : float, dimension (`lmax`+1, `lmax`+1`)
:   The coupling matrix that relates the power spectrum expectation of the function expressed in a subset of the best-localized spherical-cap Slepian functions to the expectation of the global power spectrum.

# Parameters

`galpha` : float, dimension (`lmax`+1, `nmax`)
:   An array of spherical-cap Slepian functions, arranged in columns from best to worst localized.

`galpha_order` : integer, dimension (`kmaxin`)
:   The angular order of the spherical-cap Slepian functions in `galpha`.

`nmax` : input, integer
:   The number of Slepian functions used in reconstructing the function.

# Description

`SHSCouplingMatrixCap` returns the spherical harmonic coupling matrix that relates the power spectrum expectation of the function expressed in a subset of the best-localized spherical-cap Slepian functions to the expectation of the global power spectrum (assumed to be stationary). The Slepian functions are determined by a call to `SHReturnTapers` and each row of `galpha` contains the (`lmax`+1) spherical harmonic coefficients for the single angular order as given in `galpha_order`.

The relationship between the global and localized power spectra is given by:

`< S_{\tilde{f}}(l) > = \sum_{l'=0}^lmax K_{ll'} S_{f}(l')`

where `S_{\tilde{f}}` is the expectation of the power spectrum at degree l of the function expressed in Slepian functions, `S_{f}(l')` is the expectation of the global power spectrum, and `< ... >` is the expectation operator. The coupling matrix is given explicitly by

`K_{ll'} = \frac{1}{2l'+1} Sum_{m=-mmax}^mmax ( Sum_{alpha=1}^nmax g_{l'm}(alpha) g_{lm}(alpha) )**2`

where `mmax` is min(l, l').
