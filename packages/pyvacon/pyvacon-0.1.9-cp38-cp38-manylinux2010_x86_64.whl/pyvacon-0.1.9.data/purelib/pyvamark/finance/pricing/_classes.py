import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter

# storages
MarketDataManager = _add_converter(_swig.MarketDataManager)
ParameterManager = _add_converter(_swig.ParameterManager)
SpecificationManager = _add_converter(_swig.SpecificationManager)

#results & requests
CashflowSlices = _add_converter(_swig.CashflowSlices)
PricingResults = _add_converter(_swig.PricingResults)
PricingRequest = _add_converter(_swig.PricingRequest)

# pricing parameter
PricingParameter = _add_converter(_swig.PricingParameter)
PathGeneratorParameter = _add_converter(_swig.PathGeneratorParameter)
BondPricingParameter = _add_converter(_swig.BondPricingParameter)
CallableBondPdePricingParameter = _add_converter(_swig.CallableBondPdePricingParameter)
PdePricingParameter = _add_converter(_swig.PdePricingParameter)
MonteCarloPricingParameter = _add_converter(_swig.MonteCarloPricingParameter)
InterestRateSwapPricingParameter = _add_converter(_swig.InterestRateSwapPricingParameter)

# pricing data
BasePricingData = _add_converter(_swig.BasePricingData)
LocalVolPdePricingData = _add_converter(_swig.LocalVolPdePricingData)
ComboPricingData = _add_converter(_swig.ComboPricingData)
AsianRiskControlPricingData = _add_converter(_swig.AsianRiskControlPricingData)
InterestRateSwapLegPricingData = _add_converter(_swig.InterestRateSwapLegPricingData)
InterestRateSwapFloatLegPricingData = _add_converter(_swig.InterestRateSwapFloatLegPricingData)
InterestRateSwapPricingData = _add_converter(_swig.InterestRateSwapPricingData)
BondPricingData = _add_converter(_swig.BondPricingData)
PathGeneratorParameter = _add_converter(_swig.PathGeneratorParameter)
BondPricingParameter = _add_converter(_swig.BondPricingParameter)
InflationLinkedBondPricingData = _add_converter(_swig.InflationLinkedBondPricingData)
CallableBondPdePricingData = _add_converter(_swig.CallableBondPdePricingData)
Black76PricingData = _add_converter(_swig.Black76PricingData)
LocalVolMonteCarloPricingData = _add_converter(_swig.LocalVolMonteCarloPricingData)
StochasticVolMonteCarloPricingData = _add_converter(_swig.StochasticVolMonteCarloPricingData)


# pricer
BasePricer = _add_converter(_swig.BasePricer)
LocalVolPdePricer = _add_converter(_swig.LocalVolPdePricer)
BondPricer = _add_converter(_swig.BondPricer)
InflationLinkedBondPricer = _add_converter(_swig.InflationLinkedBondPricer)
CallableBondPdePricer = _add_converter(_swig.CallableBondPdePricer)
InterestRateSwapPricingParameter = _add_converter(_swig.InterestRateSwapPricingParameter)



