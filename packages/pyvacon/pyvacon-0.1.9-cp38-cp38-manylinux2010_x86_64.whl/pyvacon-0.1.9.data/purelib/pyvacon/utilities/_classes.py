import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

ptime = _add_converter(_swig.ptime)
DataTable = _add_converter(_swig.DataTable)
Logger = _add_converter(_swig.Logger)

