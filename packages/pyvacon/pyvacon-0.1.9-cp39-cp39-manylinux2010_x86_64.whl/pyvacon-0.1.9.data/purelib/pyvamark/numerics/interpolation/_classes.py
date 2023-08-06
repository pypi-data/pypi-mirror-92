import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter


InterpolationType = _add_converter(_swig.InterpolationType)
InterpolationLinear1D = _add_converter(_swig.InterpolationLinear1D)
InterpolationMonotoneSpline1D = _add_converter(_swig.InterpolationMonotoneSpline1D)
InterpolationNaturalSpline1D = _add_converter(_swig.InterpolationNaturalSpline1D)
InterpolationHagan1D = _add_converter(_swig.InterpolationHagan1D)
InterpolationHagan1D_DF = _add_converter(_swig.InterpolationHagan1D_DF)

