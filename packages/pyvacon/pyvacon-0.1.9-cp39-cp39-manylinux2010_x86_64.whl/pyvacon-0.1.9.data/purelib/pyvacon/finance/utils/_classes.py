import pyvacon.pyvacon_swig as _swig
#from pyvacon._converter import _add_converter
from pyvacon._converter import  converter as _converter

computeXStrike = _converter(_swig.computeXStrike)
computeRealStrike = _converter(_swig.computeRealStrike)
calcEuropeanPutPrice = _converter(_swig.calcEuropeanPutPrice)
calcEuropeanCallPrice = _converter(_swig.calcEuropeanCallPrice)

