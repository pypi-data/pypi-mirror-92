# SlepianCoeffsToSH()

Convert a function expressed in Slepian coefficients to spherical harmonic coefficients.

# Usage

```python
`flm` = SlepianCoeffsToSH(`falpha`, `galpha`, `nmax`)
```

# Returns

`flm` :float, dimension (2, `lmax`+1, `lmax`+1)
:   The spherical harmonic coefficients of the global function.

# Parameters

`falpha` :float, dimension (`nmax`)
:   A vector containing the Slepian coefficients of the function.

`galpha` : float, dimension ((`lmax`+1)\*\*2, `nmax`)
:   An array containing the spherical harmonic coefficients of the Slepian functions, where `lmax` is the spherical harmonic bandwidth of the functions. Each column corresponds to a single function of which the spherical harmonic coefficients can be unpacked with `SHVectorToCilm`.

`nmax` : input, integer
:   The number of expansion coefficients to compute. This must be less than or equal to (`lmax`+1)\*\*2.

# Description

`SlepianCoeffsToSH` will compute the spherical harmonic coefficients of a global function `flm` given the Slepian functions `galpha` and the corresponding Slepian coefficients `falpha`. The Slepian functions are determined by a call to either (1) `SHReturnTapers` and then `SHRotateTapers`, or (2) `SHReturnTapersMap`. Each row of `galpha` contains the (`lmax`+1)\*\*2 spherical harmonic coefficients of a Slepian function that can be unpacked using `SHVectorToCilm`. The Slepian functions must be normalized to have unit power (that is the sum of the coefficients squared is 1), and the spherical harmonic coefficients are calculated as

`f_lm = sum_{alpha}^{nmax} f_alpha g(alpha)_lm`  
