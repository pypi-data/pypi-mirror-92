import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter

ptime = _add_converter(_swig.ptime)
DataTable = _add_converter(_swig.DataTable)
Logger = _add_converter(_swig.Logger)

