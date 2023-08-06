# SlepianCoeffs()

Determine the expansion coefficients of a function for a given set of input Slepian functions.

# Usage

```python
`falpha` = SlepianCoeffs(`galpha`, `flm`, `nmax`)
```

# Returns

`falpha` : float, dimension (`nmax`)
:   A vector containing the Slepian coefficients of the input function `flm`.

# Parameters

`galpha` : float, dimension ((`lmax`+1)\*\*2, `nmax`)
:   An array containing the spherical harmonic coefficients of the Slepian functions, where `lmax` is the spherical harmonic bandwidth of the functions. Each column corresponds to a single function of which the spherical harmonic coefficients can be unpacked with `SHVectorToCilm`.

`flm` : float, dimension (2, `lmax`+1, `lmax`+1)
:   The spherical harmonic coefficients of the global function to be expanded in Slepian functions.

`nmax` : integer
:   The number of expansion coefficients to compute. This must be less than or equal to (`lmax`+1)\*\*2.

# Description

`SlepianCoeffs` will compute the Slepian coefficients of a global input function `flm` given the Slepian functions `galpha`. The Slepian functions are determined by a call to either (1) `SHReturnTapers` and then `SHRotateTapers`, or (2) `SHReturnTapersMap`. Each row of `galpha` contains the (`lmax`+1)\*\*2 spherical harmonic coefficients of a Slepian function that can be unpacked using `SHVectorToCilm`. The Slepian functions must be normalized to have unit power (that is the sum of the coefficients squared is 1), and the Slepian coefficients are calculated as

`f_alpha = sum_{lm}^{lmax} f_lm g(alpha)_lm`  
