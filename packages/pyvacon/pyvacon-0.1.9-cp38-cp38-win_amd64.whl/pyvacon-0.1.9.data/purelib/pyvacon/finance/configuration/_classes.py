import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

BaseUnderlying = _add_converter(_swig.BaseUnderlying)
EquityUnderlying = _add_converter(_swig.EquityUnderlying)
FxUnderlying = _add_converter(_swig.FxUnderlying)
IrUnderlying = _add_converter(_swig.IrUnderlying)
IssuerToCreditMapping = _add_converter(_swig.IssuerToCreditMapping)
