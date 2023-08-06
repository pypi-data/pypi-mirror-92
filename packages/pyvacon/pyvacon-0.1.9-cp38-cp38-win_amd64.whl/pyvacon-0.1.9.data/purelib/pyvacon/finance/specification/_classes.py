import pyvacon.pyvacon_swig as _swig
from pyvacon._converter import _add_converter

# helper
BaseSpecification = _add_converter(_swig.BaseSpecification)
FixingTable = _add_converter(_swig.FixingTable)
ComboSpecification = _add_converter(_swig.ComboSpecification)

# equity
PayoffStructure = _add_converter(_swig.PayoffStructure)
BarrierDefinition = _add_converter(_swig.BarrierDefinition)
BarrierSchedule = _add_converter(_swig.BarrierSchedule)
BarrierPayoff = _add_converter(_swig.BarrierPayoff)
ExerciseSchedule = _add_converter(_swig.ExerciseSchedule)
BarrierSpecification = _add_converter(_swig.BarrierSpecification)
EuropeanVanillaSpecification = _add_converter(_swig.EuropeanVanillaSpecification)
AmericanVanillaSpecification = _add_converter(_swig.AmericanVanillaSpecification)

#bond
CouponDescription = _add_converter(_swig.CouponDescription)
BondSpecification = _add_converter(_swig.BondSpecification)
ConvertibleBondSpecification = _add_converter(_swig.ConvertibleBondSpecification)
ConvertibleBondSpecification_Conversion = _add_converter(_swig.ConvertibleBondSpecification_Conversion)
ConvertibleBondSpecification_CallPut = _add_converter(_swig.ConvertibleBondSpecification_CallPut)
InflationLinkedBondSpecification = _add_converter(_swig.InflationLinkedBondSpecification)
CallableBondSpecification = _add_converter(_swig.CallableBondSpecification)
IrSwapLegSpecification = _add_converter(_swig.IrSwapLegSpecification)
IrFixedLegSpecification = _add_converter(_swig.IrFixedLegSpecification)
IrFloatLegSpecification = _add_converter(_swig.IrFloatLegSpecification)
InterestRateSwapSpecification = _add_converter(_swig.InterestRateSwapSpecification)
InterestRateBasisSwapSpecification = _add_converter(_swig.InterestRateBasisSwapSpecification)
DepositSpecification = _add_converter(_swig.DepositSpecification)
InterestRateFutureSpecification = _add_converter(_swig.InterestRateFutureSpecification)

# equity complex
LocalVolMonteCarloSpecification = _add_converter(_swig.LocalVolMonteCarloSpecification)
RainbowSpecification = _add_converter(_swig.RainbowSpecification)
MultiMemoryExpressSpecification = _add_converter(_swig.MultiMemoryExpressSpecification)
MemoryExpressSpecification = _add_converter(_swig.MemoryExpressSpecification)
ExpressPlusSpecification = _add_converter(_swig.ExpressPlusSpecification)
AsianVanillaSpecification = _add_converter(_swig.AsianVanillaSpecification)
RiskControlStrategy = _add_converter(_swig.RiskControlStrategy)
AsianRiskControlSpecification = _add_converter(_swig.AsianRiskControlSpecification)
BarrierPayoff = _add_converter(_swig.BarrierPayoff)
