import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter

BaseModel = _add_converter(_swig.BaseModel)
CalibrationStorage = _add_converter(_swig.CalibrationStorage)


