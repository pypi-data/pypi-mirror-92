import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

Currency = _add_converter(_swig.Currency)
DayCounter = _add_converter(_swig.DayCounter)
Issuer = _add_converter(_swig.Issuer)
HolidayCalendar = _add_converter(_swig.HolidayCalendar)
SimpleHolidayCalendar = _add_converter(_swig.SimpleHolidayCalendar)
CombinedHolidayCalendar = _add_converter(_swig.CombinedHolidayCalendar)
RollConvention = _add_converter(_swig.RollConvention)

