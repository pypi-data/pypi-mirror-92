import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

SpotInterface = _add_converter(_swig.SpotInterface)
InMemoryInterface = _add_converter(_swig.InMemoryInterface)


