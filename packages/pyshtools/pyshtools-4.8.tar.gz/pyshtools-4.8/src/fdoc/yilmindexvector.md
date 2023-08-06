# YilmIndexVector

Compute the index of an 1D array of spherical harmonic coefficients corresponding to `i`, `l`, and `m`.

# Usage

`index` = YilmIndexVector (`i`, `l`, `m`)

# Parameters

`index` : output, integer(int32)
:   Index of an 1D array of spherical harmonic coefficients corresponding to `i`, `l`, and `m`.

`i` : input, integer(int32)
:   1 corresponds to the cosine coefficient `cilm(1,:,:)`, and 2 corresponds to the sine coefficient `cilm(2,:,:)`.

`l` : input, integer(int32)
:   The spherical harmonic degree.

`m` : input, integer(int32)
:   The angular order.

# Description

`YilmIndexVector` will calculate the index of a 1D vector of spherical harmonic coefficients corresponding to degree `l`, angular order `m` and `i` (1 = cosine, 2 = sine). The elements of the 1D vector array are packed by successive degrees, where each degree lists the l+1 cosine terms and then the l cosine terms. The index is given explicitly by `l**2+(i-1)*l+m+1`.

# See also

[shcilmtovector](shcilmtovector.html), [shvectortocilm](shvectortocilm.html)
