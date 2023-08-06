# SHVectorToCilm()

Convert a 1-dimensional indexed vector of real spherical harmonic coefficients to a three-dimensional array.

# Usage

```python
`cilm` = SHVectorToCilm (`vector`, [`lmax`])
```

# Returns

`cilm` : float, dimension (2, `lmax`+1, `lmax`+1)
:   The 3-D arrary of output real spherical harmonic coefficients.

# Parameters

`vector` : float, dimension ( (`lmaxin`+1)\*\*2 )
:   The input 1-D indexed array of real spherical harmonic coefficients.

`lmax` : optional, optional, default = `lmaxin`
:   The maximum degree of the output coefficients.

# Description

`SHVectorToCilm` will convert a 1-dimensional indexed vector of real spherical harmonic coefficients to a three-dimensional array. The degree `l`, order `m`, and `i` (1 = cosine, 2 = sine) corresponds to the index `l**2+(i-1)*l+m.
