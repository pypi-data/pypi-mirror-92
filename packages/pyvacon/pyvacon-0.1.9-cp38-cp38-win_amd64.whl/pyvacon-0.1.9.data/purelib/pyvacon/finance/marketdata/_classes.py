import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

MarketDataObject = _add_converter(_swig.MarketDataObject)

BaseDatedCurve = _add_converter(_swig.BaseDatedCurve)
DatedCurve = _add_converter(_swig.DatedCurve)
DiscountCurve = _add_converter(_swig.DiscountCurve)
SurvivalCurve = _add_converter(_swig.SurvivalCurve)
DividendTable = _add_converter(_swig.DividendTable)
ForwardCurve = _add_converter(_swig.ForwardCurve)
EquityForwardCurve = _add_converter(_swig.EquityForwardCurve)
FxForwardCurve = _add_converter(_swig.FxForwardCurve)
InflationIndexForwardCurve = _add_converter(_swig.InflationIndexForwardCurve)
LiborCurve = _add_converter(_swig.LiborCurve)
SwapCurve = _add_converter(_swig.SwapCurve)


VolatilityParametrization = _add_converter(_swig.VolatilityParametrization)
VolatilityParametrizationFlat = _add_converter(_swig.VolatilityParametrizationFlat)
VolatilityParametrizationTerm = _add_converter(_swig.VolatilityParametrizationTerm)
VolatilityParametrizationSSVI = _add_converter(_swig.VolatilityParametrizationSSVI)
VolatilityParametrizationTimeSlice = _add_converter(_swig.VolatilityParametrizationTimeSlice)
VolatilitySurface = _add_converter(_swig.VolatilitySurface)
VolatilitySurfaceBucketShifted = _add_converter(_swig.VolatilitySurfaceBucketShifted)

QuoteTable = _add_converter(_swig.QuoteTable)
FxForwardQuoteTable = _add_converter(_swig.FxForwardQuoteTable)
FxOptionQuoteTable = _add_converter(_swig.FxOptionQuoteTable)
EquityOptionQuoteTable = _add_converter(_swig.EquityOptionQuoteTable)
BondQuoteTable = _add_converter(_swig.BondQuoteTable)
