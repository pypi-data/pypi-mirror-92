# PlSchmidt()

Compute all the Schmidt-normalized Legendre polynomials.

# Usage

```python
`p` = PlSchmidt (`lmax`, `z`)
```

# Returns

`p` : float, dimension (`lmax`+1)
:   An array of Schmidt-normalized Legendre polynomials up to degree `lmax`. Degree `l` corresponds to array index `l`.

# Parameters

`lmax` : integer
:   The maximum degree of the Legendre polynomials to be computed.

`z` : float
:   The argument of the Legendre polynomial.

# Description

`PlSchmidt` will calculate all of the Schmidt-normalized Legendre polynomials up to degree `lmax` for a given argument. These are calculated using a standard three-term recursion formula. The integral of the Schmidt-normalized Legendre polynomials over the interval [-1, 1] is `2/(2l+1)`.
