"""
pyshtools Spherical Harmonic Expansion Routines.

This subpackage of pyshtools defines the following functions:

Equally sampled (N by N) and equally spaced (N by 2N) Grids
-----------------------------------------------------
SHExpandDH     Expand an equally sampled or equally spaced map into spherical
               harmonics using Driscoll and Healy's (1994) sampling theorem.
MakeGridDH     Create a 2D map from a set of spherical harmonic coefficients
               that conforms with Driscoll and Healy's (1994) sampling theorem.
SHExpandDHC    Expand an equally sampled or equally spaced complex map into
               complex spherical harmonics using Driscoll and Healy's (1994)
               sampling theorem.
MakeGridDHC    Create a 2D complex map from a set of complex spherical harmonic
               coefficients that conforms with Driscoll and Healy's (1994)
               sampling theorem.
MakeGradientDH Compute the gradient of a scalar function and return grids of
               the two horizontal components that conform with Driscoll and
               Healy's (1994) sampling theorem.

Gauss-Legendre quadrature grids
-------------------------------
SHGLQ          Precompute the weights and nodes used in the GLQ-based spherical
               harmonics routines.
SHExpandGLQ    Expand a 2D map sampled on the Gauss-Legendre quadrature nodes
               into spherical harmonics.
MakeGridGLQ    Create a 2D map from a set of spherical harmonic coefficients
               sampled on a the Gauss-Legendre quadrature nodes.
SHExpandGLQC   Expand a 2D complex map sampled on the Gauss-Legendre quadrature
               nodes into complex spherical harmonics.
MakeGridGLQC   Create a 2D complex map from a set of complex spherical harmonic
               coefficients sampled on a the Gauss-Legendre quadrature nodes.
GLQGridCoord   Compute the latitude and longitude coordinates used in Gauss-
               Legendre quadrature grids.

Other
-----
SHExpandLSQ    Expand a set of irregularly sampled data points into spherical
               harmonics using a least squares inversion.
SHExpandWLSQ   Expand a set of irregularly sampled data points into spherical
               harmonics using a weighted least squares inversion.
MakeGrid2D     Create a 2D cylindrical map with arbitrary grid spacing from a
               set of spherical harmonic coefficients.
MakeGridPoint  Evaluate a real function expressed in real spherical harmonics
               at a single point.
MakeGridPointC Evaluate a complex function expressed in complex spherical
               harmonics at a single point.
SHMultiply     Multiply two functions and determine the spherical harmonic
               coefficients of the resulting function.
spharm         Compute all the spherical harmonic functions up to a maximum
               degree and order.
spharm_lm      Compute the spherical harmonic function for a specific degree l
               and order m.
"""
from ..shtools import SHExpandDH
from ..shtools import MakeGridDH
from ..shtools import SHExpandDHC
from ..shtools import MakeGridDHC
from ..shtools import SHGLQ
from ..shtools import SHExpandGLQ
from ..shtools import MakeGridGLQ
from ..shtools import SHExpandGLQC
from ..shtools import MakeGridGLQC
from ..shtools import GLQGridCoord
from ..shtools import SHExpandLSQ
from ..shtools import SHExpandWLSQ
from ..shtools import MakeGrid2D
from ..shtools import MakeGridPoint
from ..shtools import MakeGridPointC
from ..shtools import SHMultiply
from ..shtools import MakeGradientDH

from .spharm_functions import spharm
from .spharm_functions import spharm_lm

del spharm_functions  # noqa: F821


# ---- Define __all__ for use with: from pyshtools import * ----
__all__ = ['SHExpandDH', 'MakeGridDH', 'SHExpandDHC', 'MakeGridDHC',
           'SHGLQ', 'SHExpandGLQ', 'MakeGridGLQ', 'SHExpandGLQC',
           'MakeGridGLQC', 'GLQGridCoord', 'SHExpandLSQ', 'SHExpandWLSQ',
           'MakeGrid2D', 'MakeGridPoint', 'MakeGridPointC', 'SHMultiply',
           'MakeGradientDH', 'spharm', 'spharm_lm']
