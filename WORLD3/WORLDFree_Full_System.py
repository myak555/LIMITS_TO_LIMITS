from DYNAMO_Prototypes import *

#
# This module contains all equations of World3 model,
# modified with parametrizations, based on the UN
# statistics and other data
# Changes from the original World-3 model are in comments
#
GraphShow = False


#
# POPULATION SUBSYSTEM (equations {1}-{23}, {26}-{48})
#
# Validated
# Unchanged
Population = AuxVariable(
    "_001_Population", "persons",
    fupdate = "_002_Population0To14.K"
    "+ _006_Population15To44.K"
    "+ _010_Population45To64.K"
    "+ _014_Population65AndOver.K")

#
# Population 0-14
#
# Validated
# Initial value changed from 0.65е9 to 0.67e9
Population0To14 = LevelVariable(
    "_002_Population0To14", "0.67e9", "persons",
    fupdate = "_030_BirthsPerYear.J"
    "- _003_DeathsPerYear0To14.J"
    "- _005_MaturationsPerYear14to15.J")

# Validated
# Unchanged
DeathsPerYear0To14 = RateVariable(
    "_003_DeathsPerYear0To14", "persons / year",
    fupdate = "_002_Population0To14.K"
    "* _004_Mortality0To14.K")

# Validated
# The original table from World-3 (1972-2013):
# [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010]
# These values have been adjusted to match the UN age distribution stats
Mortality0To14 = TableParametrization(
    "_004_Mortality0To14",
    [0.0850, 0.0575, 0.0355, 0.0157, 0.0065, 0.0018, 0.0008],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality0To14,
#    0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
# Unchanged
MaturationsPerYear14to15 = RateVariable(
    "_005_MaturationsPerYear14to15", "persons / year",
    fupdate = "_002_Population0To14.K"
    "* (1 - _004_Mortality0To14.K) / 15.0")


#
# Population 15-44
#
# Initial value changed from 0.70е9 to 0.72e9
Population15To44 = LevelVariable(
    "_006_Population15To44", "0.72e9", "persons",
    fupdate = "_005_MaturationsPerYear14to15.J"
    "- _007_DeathsPerYear15To44.J"
    "- _009_MaturationsPerYear44to45.J")

# Validated
# Unchanged
DeathsPerYear15To44 = RateVariable(
    "_007_DeathsPerYear15To44", "persons / year",
    fupdate = "_006_Population15To44.K"
    "* _008_Mortality15To44.K")

# Validated
# The original table from World-3 (1972-2013):
# [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008]
# These values have been adjusted to match the UN age distribution stats
Mortality15To44 = TableParametrization(
    "_008_Mortality15To44",
    [0.0213, 0.0137, 0.0088, 0.0046, 0.0010, 0.0001, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality15To44,
#    0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
# Unchanged
MaturationsPerYear44to45 = RateVariable(
    "_009_MaturationsPerYear44to45", "persons / year",
    fupdate = "_006_Population15To44.K"
    "* (1 - _008_Mortality15To44.K) / 30.0")


#
# Population 45-64
#
# Validated
# Initial value changed from 0.19е9 to 0.195e9 (for 1.65e9 total population in 1900)
Population45To64 = LevelVariable(
    "_010_Population45To64", "0.195e9", "persons",
    fupdate = "_009_MaturationsPerYear44to45.J"
    "- _011_DeathsPerYear45To64.J"
    "- _013_MaturationsPerYear64to65.J")

# Validated
# Unchanged
DeathsPerYear45To64 = RateVariable(
    "_011_DeathsPerYear45To64", "persons / year",
    fupdate = "_010_Population45To64.K"
    "* _012_Mortality45To64.K")

# Validated
# The original table from World-3 (1972-2013):
# [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060]
# These values have been adjusted to match the UN age distribution stats
Mortality45To64 = TableParametrization(
    "_012_Mortality45To64",
    [0.0450, 0.0298, 0.0195, 0.0115, 0.0034, 0.0002, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, Mortality45To64,
    0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
# Unchanged
MaturationsPerYear64to65 = RateVariable(
    "_013_MaturationsPerYear64to65", "persons / year",
    fupdate = "_010_Population45To64.K"
    "* (1 - _012_Mortality45To64.K) / 20.0")


#
# Population over 65
#
# Validated
# Unchanged
Population65AndOver = LevelVariable(
    "_014_Population65AndOver", "6.0e7", "persons",
    fupdate = "_013_MaturationsPerYear64to65.J"
    "- _015_DeathsPerYear65AndOver.J")

# Validated
# Unchanged
DeathsPerYear65AndOver = RateVariable(
    "_015_DeathsPerYear65AndOver", "persons / year",
    fupdate = "_014_Population65AndOver.K"
    "* _016_Mortality65AndOver.K")

# Validated
# The original table from World-3 (1972-2013):
# [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04] for the range of [20, 80]
# These values have been adjusted to match the UN age distribution stats
Mortality65AndOver = TableParametrization(
    "_016_Mortality65AndOver",
    [0.129, 0.127, 0.124, 0.120, 0.115, 0.108, 0.098, 0.060, 0.010],
    40, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality65AndOver,
#    0, 100, "LifeExpectancy [years]", show=GraphShow)


#
# Death rate and life expectancy
#
# Validated
# Unchanged
DeathsPerYear = AuxVariable(
    "_017_DeathsPerYear", "persons / year",
    fupdate = "_003_DeathsPerYear0To14.J"
    "+ _007_DeathsPerYear15To44.J"
    "+ _011_DeathsPerYear45To64.J"
    "+ _015_DeathsPerYear65AndOver.J")

# Validated
# Unchanged
CrudeDeathRate = AuxVariable(
    "_018_CrudeDeathRate", "deaths / 1000 persons / year",
    fupdate = "1000 * _017_DeathsPerYear.K"
    "/ _001_Population.K")

# Validated
# Base value changed from 32 to 32.6
# Variable smoothed over 3-year period
##    "_019_LifeExpectancy", "years",
##    fupdate = "32 * _020_LifetimeMultiplierFromFood.K"
##    "* _023_LifetimeMultiplierFromHealthServices.K"
##    "* _028_LifetimeMultiplierFromCrowding.K"
##    "* _029_LifetimeMultiplierFromPollution.K")
LifeExpectancy = SmoothVariable(
    "_019_LifeExpectancy",
    "3.0", "years",
    "32.6 * _020_LifetimeMultiplierFromFood.K"
    "* _023_LifetimeMultiplierFromHealthServices.K"
    "* _028_LifetimeMultiplierFromCrowding.K"
    "* _029_LifetimeMultiplierFromPollution.K")

# Validated
# Unchanged
LifetimeMultiplierFromFood = TableParametrization(
    "_020_LifetimeMultiplierFromFood",
    [0, 1, 1.2, 1.3, 1.35, 1.4], 0, 5,
    fupdate = "_088_FoodPerCapita.K /"
    "_151_SubsistenceFoodPerCapita.K")
#PlotTable( DYNAMO_Engine, LifetimeMultiplierFromFood, 0, 10,
#           "Subsistence levels [unitless]", show=GraphShow)

# Validated
# Unchanged
HealthServicesAllocationsPerCapita = TableParametrization(
    "_021_HealthServicesAllocationsPerCapita",
    [0, 20, 50, 95, 140, 175, 200, 220, 230], 0, 2000,
    "dollars / person / year",
    fupdate = "_071_ServiceOutputPerCapita.K")
#PlotTable( DYNAMO_Engine, HealthServicesAllocationsPerCapita, 0, 2000,
#           "Service Output Per Capita [$/person/year]", show=GraphShow)

# Validated
# Unchanged
EffectiveHealthServicesPerCapita = SmoothVariable(
    "_022_EffectiveHealthServicesPerCapita",
    "_152_EffectiveHealthServicesPerCapitaImpactDelay.K",
    "dollars / person / year",
    "_021_HealthServicesAllocationsPerCapita.K")

#
# Updated to match the UN LEB data
# The original parametrization
#    [1, 1.4, 1.6, 1.8, 1.95, 2.0], 0, 100,
#    fpoints_1940 = [1, 1.1, 1.4, 1.6, 1.7, 1.8],
#
LifetimeMultiplierFromHealthServices = TableParametrization(
    "_023_LifetimeMultiplierFromHealthServices",
    [0.95, # 5
     1.29, # 10
     1.70, # 15
     1.80, # 20
     1.85, # 25
     1.95, # 30
     2.01, # 35
     2.07, # 40
     2.13, # 45
     2.18, # 50
     2.22, # 55
     2.26, # 60
     2.28, # 65
     2.30, # 70
     2.31, # 75
     2.32, # 80
     2.33, # 85
     2.34], 5, 90,
    fupdate = "_022_EffectiveHealthServicesPerCapita.K")
#PlotTable( DYNAMO_Engine, LifetimeMultiplierFromHealthServices, 0, 100,
#           "Effective Health Services Per Capita [$/person/year]", show=GraphShow)


#
# pop024, pop025 - used to be policy tables, depicting
# lower LEB before 1940. With calibrations - no longer needed
#
# slots 24 and 25 are used for adjustments in female population
#
# Gender adjustment based on the UN distribution data
# https://ourworldindata.org/gender-ratio
#
Females20to40Ratio  = TableParametrization(
    "_024_Females20to40Ratio",
    [0.51,0.49],
    1950, 2020,
    fupdate = "DYNAMO_Engine.time")
#PlotTable( DYNAMO_Engine, Females20to40Ratio,
#    1900, 2100, "Time [years]", show=GraphShow)

#
# Adjustment based on fertility period
# Lower TFR usually means the first birth
# later than 15 years of age.
#
AverageFertilityPeriod  = TableParametrization(
    "_025_AverageFertilityPeriod",
    [26.3,28.3],
    2.8, 5.0, "years",
    fupdate = "_032_TotalFertility.K")
#PlotTable( DYNAMO_Engine, AverageFertilityPeriod,
#    0, 6, "TFR [children per woman]", show=GraphShow)


# Validated
# The original parametrization
# [0, 0.2, 0.4, 0.5, 0.58, 0.65, 0.72, 0.78, 0.80]
# it replaced with the statistically computed
# data from https://ourworldindata.org/urbanization
FractionOfPopulationUrban = TableParametrization(
    "_026_FractionOfPopulationUrban",
    [0.000,0.046,0.094,0.151,0.222,
     0.296,0.339,0.363,0.380,0.397,
     0.418,0.443,0.469,0.496,0.523,
     0.549,0.573,0.597,0.618,0.639,
     0.658,0.676,0.692,0.707,0.721,
     0.734,0.746,0.757,0.767,0.776,
     0.784,0.792,0.800], 0, 16e9,
    fupdate = "_001_Population.K")
#PlotTable( DYNAMO_Engine, FractionOfPopulationUrban,
#    0, 16e9, "Total Population [persons]", show=GraphShow)

# Validated
# Unchanged
CrowdingMultiplierFromIndustrialization = TableParametrization(
    "_027_CrowdingMultiplierFromIndustrialization",
    [0.5, 0.05, -0.1, -0.08, -0.02, 0.05, 0.1, 0.15, 0.2],
    0, 1600,
    fupdate = "_049_IndustrialOutputPerCapita.K")
#PlotTable( DYNAMO_Engine, CrowdingMultiplierFromIndustrialization,
#    0, 1700, "Industrial Output Per Capita [kg/person/year]", show=GraphShow)

# Validated
# Unchanged
LifetimeMultiplierFromCrowding = AuxVariable(
    "_028_LifetimeMultiplierFromCrowding",
    fupdate = "1 - _027_CrowdingMultiplierFromIndustrialization.K"
    "* _026_FractionOfPopulationUrban.K") 

# Validated
# Unchanged
LifetimeMultiplierFromPollution = TableParametrization(
    "_029_LifetimeMultiplierFromPollution",
    [1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.75, 0.65, 0.55, 0.40, 0.20],
    0, 100,
    fupdate = "_143_IndexOfPersistentPollution.K")
#PlotTable( DYNAMO_Engine, LifetimeMultiplierFromPollution,
#    0, 110, "Index Of Persistent Pollution [levels of 1970]", show=GraphShow)

#
# Fertility and birth rate
#
# Validated
# Adjustment factor Females20to40Ratio accounts for male-female disbalance
# Fertility period adjusted as a function of LEB to match the UN crude birth rate stats
BirthsPerYear = RateVariable(
    "_030_BirthsPerYear", "persons / year",
    fupdate = "_032_TotalFertility.K"
    "* _006_Population15To44.K"
    "* _024_Females20to40Ratio.K"
    "/ _025_AverageFertilityPeriod.K",
    fequilibrium = "_017_DeathsPerYear.K")

# Validated
# Unchanged
CrudeBirthRate = AuxVariable(
    "_031_CrudeBirthRate", "births / 1000 persons / year",
    fupdate = "1000 * _030_BirthsPerYear.J / _001_Population.K")

# Validated
TotalFertility = AuxVariable(
    "_032_TotalFertility",
    fupdate = "min( _033_MaxTotalFertility.K,"
    "_033_MaxTotalFertility.K"
    "* (1 - _045_FertilityControlEffectiveness.K)"
    "+ _035_DesiredTotalFertility.K"
    "* _045_FertilityControlEffectiveness.K)")

# Validated
# max number of births per woman changed (original value 12)
MaxTotalFertility = AuxVariable(
    "_033_MaxTotalFertility",
    fupdate = "10 * _034_FecundityMultiplier.K")
    # 10 - max number of births

# Validated
# Unchanged
FecundityMultiplier = TableParametrization(
    "_034_FecundityMultiplier",
    [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.05, 1.1], 0, 80,
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, FecundityMultiplier,
    0, 100, "Life Expectancy [years]", show=GraphShow)

# Validated
# Changed to smooth variable
DesiredTotalFertility = SmoothVariable(
    "_035_DesiredTotalFertility", "2.0",
    fupdate = "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy.K"
    "* _038_DesiredCompletedFamilySize.K"
    "* _235_FertilityCorrection_WW2.K")

#
# Added to match the UN fertility data
#
FertilityCorrection_WW2 = TableParametrization(
    "_235_FertilityCorrection_WW2",
    [1.0,0.9,0.9,1.0],
    1939, 1945,
    fupdate = "DYNAMO_Engine.time")
PlotTable( DYNAMO_Engine, FertilityCorrection_WW2,
    1925, 1975, "Year", show=GraphShow)

# Validated
# Updated based on the UN fertlity data
# Original [3.0, 2.1, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0]
CompensatoryMultiplierFromPerceivedLifeExpectancy = TableParametrization(
     "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy",
    [2.45, 1.95, 1.75, 1.45, 1.25, 1.15, 1.1, 1.05, 1], 0, 80,
    fupdate = "_037_PerceivedLifeExpectancy.K")
PlotTable( DYNAMO_Engine, CompensatoryMultiplierFromPerceivedLifeExpectancy,
    0, 100, "PerceivedLifeExpectancy [years]", show=GraphShow)

# Validated
# Unchanged
PerceivedLifeExpectancy = DelayVariable(
    "_037_PerceivedLifeExpectancy",
    "_153_LifetimePerceptionDelay.K", "years",
    "_019_LifeExpectancy.K")

# Validated
# Original coefficient of 4.0 decreased to match the UN fertility data
DesiredCompletedFamilySize = AuxVariable(
    "_038_DesiredCompletedFamilySize", "persons",
    fupdate = "3.33 * _039_SocialFamilySizeNorm.K"
    "* _041_FamilyResponseToSocialNorm.K",
    fequilibrium = "2.0")

# Validated
# Modified from 1972 version: [1.25, 1, 0.9, 0.8, 0.75], 0, 800
SocialFamilySizeNorm = TableParametrization(
    "_039_SocialFamilySizeNorm",
    [1.000, #40, step 12.5
     0.980, 
     0.970, #65
     0.960, 
     0.950, #90
     0.960, 
     0.990, #115
     0.820, 
     0.720, #140
     0.700, 
     0.700, #165
     0.700, 
     0.700, #190
     0.700, 
     0.700, #215
     0.700, 
     0.700  #240
     ], 40, 240,
    fupdate = "_040_DelayedIndustrialOutputPerCapita.K")
PlotTable( DYNAMO_Engine, SocialFamilySizeNorm,
    0, 300, "Delayed Industrial Output Per Capita [$/capita/year]",
    show=GraphShow)

# Validated
# Unchanged
DelayedIndustrialOutputPerCapita = DelayVariable(
    "_040_DelayedIndustrialOutputPerCapita",
    "_154_SocialAdjustmentDelay.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

# Validated
# Modified from values of 1972 model: [0.5, 0.6, 0.7, 0.85, 1.0]
FamilyResponseToSocialNorm = TableParametrization(
    "_041_FamilyResponseToSocialNorm",
    [1.3,
     1.2, 
     1.0,
     1.0,
     1.0],
    -0.2, 0.2,
    fupdate = "_042_FamilyIncomeExpectation.K")
PlotTable( DYNAMO_Engine, FamilyResponseToSocialNorm,
    0, 300, "Family Income Expectation [unitless]",
    show=GraphShow)

# Validated
# Unchanged
FamilyIncomeExpectation = AuxVariable(
    "_042_FamilyIncomeExpectation",
    fupdate = "_049_IndustrialOutputPerCapita.K"
    "/ _043_AverageIndustrialOutputPerCapita.K - 1")

# Validated
# Unchanged
AverageIndustrialOutputPerCapita = SmoothVariable(
    "_043_AverageIndustrialOutputPerCapita",
    "_155_IncomeExpectationAveragingTime.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

# Validated
# Unchanged
NeedForFertilityControl = AuxVariable(
    "_044_NeedForFertilityControl",
    fupdate = "_033_MaxTotalFertility.K"
    "/ _035_DesiredTotalFertility.K - 1")

# Validated
# Unchanged
FertilityControlEffectiveness = TableParametrization(
    "_045_FertilityControlEffectiveness",
    [0.75, 0.85, 0.90, 0.95, 0.98, 0.99, 1.0], 0, 3,
    fupdate = "_046_FertilityControlFacilitiesPerCapita.K")
PlotTable( DYNAMO_Engine, FertilityControlEffectiveness,
    0, 300, "Fertility Control Facilities Per Capita [$/capita/year]",
    show=GraphShow)

# Validated
# Unchanged
FertilityControlFacilitiesPerCapita = DelayVariable(
    "_046_FertilityControlFacilitiesPerCapita",
    "_156_HealthServicesImpactDelay.K",
    "dollars / person / year",
    "_047_FertilityControlAllocationPerCapita.K")

# Validated
# Unchanged
FertilityControlAllocationPerCapita = AuxVariable(
    "_047_FertilityControlAllocationPerCapita",
    "dollars / person / year",
    fupdate = "_048_FractionOfServicesAllocatedToFertilityControl.K"
    "* _071_ServiceOutputPerCapita.K")

# Validated
# Unchanged
FractionOfServicesAllocatedToFertilityControl = TableParametrization(
    "_048_FractionOfServicesAllocatedToFertilityControl",
    [0.0, 0.005, 0.015, 0.025, 0.030, 0.035], 0, 10,
    fupdate = "_044_NeedForFertilityControl.K")
PlotTable( DYNAMO_Engine, FractionOfServicesAllocatedToFertilityControl,
    0, 300, "Need For Fertility Control [unitless]",
    show=GraphShow)

#
# INDUSTRY SUBSYSTEM (equations {49}-{59})
#
# Validated
# Unchanged
IndustrialOutputPerCapita = AuxVariable(
    "_049_IndustrialOutputPerCapita",
    "dollars / person / year",
    fupdate = "_050_IndustrialOutput.K"
    "/ _001_Population.K")

# Validated
# Unchanged
IndustrialOutput = AuxVariable(
    "_050_IndustrialOutput", "dollars / year",
    fupdate = "_052_IndustrialCapital.K"
    "* (1 - _134_FractionOfCapitalAllocatedToObtainingResources.K)"
    "* _083_CapitalUtilizationFraction.K"
    "/ _051_IndustrialCapitalOutputRatio.K")

# Validated
IndustrialCapitalOutputRatio = PolicyParametrization(
    "_051_IndustrialCapitalOutputRatio", 3, 3, "years")

# Validated
# Unchanged
IndustrialCapital = LevelVariable(
    "_052_IndustrialCapital", "2.1e11", "dollars",
    fupdate = "_055_IndustrialCapitalInvestmentRate.J"
    "- _053_IndustrialCapitalDepreciationRate.J")

# Validated
# Unchanged
IndustrialCapitalDepreciationRate = RateVariable(
    "_053_IndustrialCapitalDepreciationRate", "dollars / year",
    fupdate = "_052_IndustrialCapital.K"
    "/ _054_AverageLifetimeOfIndustrialCapital.K")

# Validated
AverageLifetimeOfIndustrialCapital = PolicyParametrization(
    "_054_AverageLifetimeOfIndustrialCapital", 14, 14, "years")

# Validated
# Unchanged
IndustrialCapitalInvestmentRate = RateVariable(
    "_055_IndustrialCapitalInvestmentRate", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _056_FractionOfIndustrialOutputAllocatedToIndustry.K")

# Validated
# Unchanged
FractionOfIndustrialOutputAllocatedToIndustry = AuxVariable(
    "_056_FractionOfIndustrialOutputAllocatedToIndustry",
    fupdate = "1 - _057_FractionOfIndustrialOutputAllocatedToConsumption.K"
    "- _063_FractionOfIndustrialOutputAllocatedToServices.K"
    "- _093_FractionOfIndustrialOutputAllocatedToAgriculture.K")

# Validated
# Unchanged
FractionOfIndustrialOutputAllocatedToConsumption = AuxVariable(
    "_057_FractionOfIndustrialOutputAllocatedToConsumption",
    fupdate = "_058_FractionOfIndustrialOutputAllocatedToConsumptionConstant.K",
    fequilibrium = "_059_FractionOfIndustrialOutputAllocatedToConsumptionVariable.K")

# Validated
FractionOfIndustrialOutputAllocatedToConsumptionConstant = PolicyParametrization(
    "_058_FractionOfIndustrialOutputAllocatedToConsumptionConstant", 0.43, 0.43)

# Validated
FractionOfIndustrialOutputAllocatedToConsumptionVariable = TableParametrization(
    "_059_FractionOfIndustrialOutputAllocatedToConsumptionVariable",
    [0.3, 0.32, 0.34, 0.36, 0.38, 0.43, 0.73, 0.77, 0.81, 0.82, 0.83], 0, 2,
    fupdate = "_049_IndustrialOutputPerCapita.K"
    "/ _157_IndicativeConsumptionValue.K")

#
# SERVICES SUBSYSTEM (equations {60}, {63}, {66}-{72})
#
# Validated
IndicatedServiceOutputPerCapita = TableParametrization(
    "_060_IndicatedServiceOutputPerCapita",
    [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    0, 1600, "dollars / person / year",
    fpoints_after_policy = [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    fupdate = "_049_IndustrialOutputPerCapita.K")

#
# svc_061, svc_062 - used to be policy tables, now in {060}
#

# Validated
FractionOfIndustrialOutputAllocatedToServices = TableParametrization(
    "_063_FractionOfIndustrialOutputAllocatedToServices",
    [0.3, 0.2, 0.1, 0.05, 0], 0, 2,
    fpoints_after_policy = [0.3, 0.2, 0.1, 0.05, 0],
    fupdate = "_071_ServiceOutputPerCapita.K"
    "/ _060_IndicatedServiceOutputPerCapita.K")

#
# svc064, svc065 - used to be policy tables, now in {063}
#

# Validated
ServiceCapitalInvestmentRate = RateVariable(
    "_066_ServiceCapitalInvestmentRate", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _063_FractionOfIndustrialOutputAllocatedToServices.K")

# Validated
ServiceCapital = LevelVariable(
    "_067_ServiceCapital", "1.44e11", "dollars",
    fupdate = "_066_ServiceCapitalInvestmentRate.J"
    "- _068_ServiceCapitalDepreciationRate.J")

# Validated
ServiceCapitalDepreciationRate = RateVariable(
    "_068_ServiceCapitalDepreciationRate", "dollars / year",
    fupdate = "_067_ServiceCapital.K"
    "/ _069_AverageLifetimeOfServiceCapital.K")

# Validated
AverageLifetimeOfServiceCapital = PolicyParametrization(
    "_069_AverageLifetimeOfServiceCapital", 20, 20, "years")

# Validated
ServiceOutput = AuxVariable(
    "_070_ServiceOutput", "dollars / year",
    fupdate = "_067_ServiceCapital.K"
    "* _083_CapitalUtilizationFraction.K"
    "/ _072_ServiceCapitalOutputRatio.K")

# Validated
# Unchanged
ServiceOutputPerCapita = AuxVariable(
    "_071_ServiceOutputPerCapita", "dollars / person / year",
    fupdate = "_070_ServiceOutput.K / _001_Population.K")

# Validated
ServiceCapitalOutputRatio = PolicyParametrization(
    "_072_ServiceCapitalOutputRatio", 1, 1, "years")

#
# LABOR SUBSYSTEM (equations {73}-{83})
#
Jobs = AuxVariable(
    "_073_Jobs", "persons",
    fupdate = "_074_PotentialJobsInIndustrialSector.K"
    "+ _076_PotentialJobsInServiceSector.K"
    "+ _078_PotentialJobsInAgriculturalSector.K")

# Validated
PotentialJobsInIndustrialSector = AuxVariable(
    "_074_PotentialJobsInIndustrialSector", "persons",
    fupdate = "_052_IndustrialCapital.K"
    "* _075_JobsPerIndustrialCapitalUnit.K")

# Validated
JobsPerIndustrialCapitalUnit = TableParametrization(
    "_075_JobsPerIndustrialCapitalUnit",
    [0.00037, 0.00018, 0.00012, 0.00009, 0.00007, 0.00006],
    50, 800, "persons / dollar",
    fupdate = "_049_IndustrialOutputPerCapita.K")

# Validated
PotentialJobsInServiceSector = AuxVariable(
    "_076_PotentialJobsInServiceSector", "persons",
    fupdate = "_067_ServiceCapital.K"
    "* _077_JobsPerServiceCapitalUnit.K")

# Validated
JobsPerServiceCapitalUnit = TableParametrization(
    "_077_JobsPerServiceCapitalUnit",
    [.0011, 0.0006, 0.00035, 0.0002, 0.00015, 0.00015],
    50, 800, "persons / dollar",
    fupdate = "_071_ServiceOutputPerCapita.K")

# Validated
PotentialJobsInAgriculturalSector = AuxVariable(
    "_078_PotentialJobsInAgriculturalSector", "persons",
    fupdate = "_085_ArableLand.K * _079_JobsPerHectare.K")

# Validated
JobsPerHectare = TableParametrization(
    "_079_JobsPerHectare",
    [2, 0.5, 0.4, 0.3, 0.27, 0.24, 0.2, 0.2],
    2, 30, "persons / hectare",
    fupdate = "_101_AgriculturalInputsPerHectare.K")

# Validated
# Unchanged
LaborForce = AuxVariable(
    "_080_LaborForce", "persons",
    fupdate = "0.75 * (_006_Population15To44.K"
    "+ _010_Population45To64.K)")
    # 0.75 - participation fraction

# Validated
LaborUtilizationFraction = AuxVariable(
    "_081_LaborUtilizationFraction",
    fupdate = "_073_Jobs.K / _080_LaborForce.K")

# Validated
LaborUtilizationFractionDelayed = SmoothVariable(
    "_082_LaborUtilizationFractionDelayed",
    "_158_LaborUtilizationFractionDelayTime.K",
    fupdate = "_081_LaborUtilizationFraction.K")

# This is confirmed to be the source of model instability
# for dt>1. The utilization jumps between 1 and 0.2.
# LaborUtilizationFractionDelayTime is set to 2 years
# This prevents it from smoothing if dt>=2 
CapitalUtilizationFraction = TableParametrization(
    "_083_CapitalUtilizationFraction",
    [1.0, 0.9, 0.7, 0.3, 0.1, 0.1], 1, 11,
    fupdate = "_082_LaborUtilizationFractionDelayed.K",
    fignore = ["_082_LaborUtilizationFractionDelayed"], # to break a circular dependency
    initialValue = 1.0)

#
# AGRICULTURE SUBSYSTEM
# (equations {84}-{89},{92},{93},{96}-{105},{108}-{113},{116}-{128})
#
# Loop 1: Food from Investment in Land Development
#
LandFractionCultivated = AuxVariable(
    "_84_LandFractionCultivated",
    fupdate = "_085_ArableLand.K"
    "/ _159_PotentiallyArableLandTotal.K")

ArableLand = LevelVariable(
    "_085_ArableLand", "0.9e9", "hectares",
    fupdate = "_096_LandDevelopmentRate.J"
    "- _119_LandRemovalForUrbanIndustrialUse.J"
    "- _116_LandErosionRate.J")

PotentiallyArableLand = LevelVariable(
    "_086_PotentiallyArableLand", "2.3e9", "hectares",
    fupdate = "- _096_LandDevelopmentRate.J")

# Validated
Food = AuxVariable(
    "_087_Food", "kilograms / year",
    fupdate = "_103_LandYield.K * _085_ArableLand.K"
    "* _160_LandFractionHarvested.K"
    "* (1 - _161_FoodProcessingLoss.K)")

# Validated
# Unchanged
FoodPerCapita = AuxVariable(
    "_088_FoodPerCapita", "kilograms / person / year",
    fupdate = "_087_Food.K / _001_Population.K")

# Validated
IndicatedFoodPerCapita = TableParametrization(
    "_089_IndicatedFoodPerCapita",
    [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    0, 1600, "kilograms / person / year",
    fpoints_after_policy = [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    fupdate = "_049_IndustrialOutputPerCapita.K")

#
# agr_090, agr_091 - used to be policy tables, now in {089}
#

# Validated
TotalAgriculturalInvestment = AuxVariable(
    "_092_TotalAgriculturalInvestment", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _093_FractionOfIndustrialOutputAllocatedToAgriculture.K")

# Validated
FractionOfIndustrialOutputAllocatedToAgriculture = TableParametrization(
    "_093_FractionOfIndustrialOutputAllocatedToAgriculture",
    [0.4, 0.2, 0.1, 0.025, 0, 0], 0, 2.5,
    fpoints_after_policy = [0.4, 0.2, 0.1, 0.025, 0, 0],
    fupdate = "_088_FoodPerCapita.K"
    "/ _089_IndicatedFoodPerCapita.K")

#
# agr_094, agr_095 - used to be policy tables, now in {093}
#

LandDevelopmentRate = RateVariable(
    "_096_LandDevelopmentRate", "hectares / year",
    fupdate = "_092_TotalAgriculturalInvestment.K"
    "/ _097_DevelopmentCostPerHectare.K"
    "* _108_FractionOfInputsAllocatedToLandDevelopment.K")

DevelopmentCostPerHectare = TableParametrization(
    "_097_DevelopmentCostPerHectare",
    [100000, 7400, 5200, 3500, 2400, 1500, 750, 300, 150, 75, 50],
    0, 1.0, "dollars / hectare",
    fupdate = "_086_PotentiallyArableLand.K"
    "/ _159_PotentiallyArableLandTotal.K")

#
# Loop 2: Food from Investment in Agricultural Inputs
#
CurrentAgriculturalInputs = AuxVariable(
    "_098_CurrentAgriculturalInputs", "dollars / year",
    fupdate = "_092_TotalAgriculturalInvestment.K"
    "* (1 - _108_FractionOfInputsAllocatedToLandDevelopment.K)")

AgriculturalInputs = SmoothVariable(
    "_099_AgriculturalInputs",
    "_162_AverageLifetimeOfAgriculturalInputs.K",
    "dollars / year",
    fupdate = "_098_CurrentAgriculturalInputs.K",
    initialValue = 5.0e9)
    #note dependency replaced by the initialValue to break a definition cycle

# this parametrization is unused - replaced with fixed parameter:
# _162_AverageLifetimeOfAgriculturalInputs = 2 years
# AverageLifetimeOfAgriculturalInputs = PolicyParametrization(
#    "_100_AverageLifetimeOfAgriculturalInputs", 2, 2, "years")

AgriculturalInputsPerHectare = AuxVariable(
    "_101_AgriculturalInputsPerHectare", "dollars / hectare / year",
    fupdate = "_099_AgriculturalInputs.K"
    "* (1 - _126_FractionOfInputsAllocatedToLandMaintenance.K)"
    "/ _085_ArableLand.K")

LandYieldMultiplierFromCapital = TableParametrization(
    "_102_LandYieldMultiplierFromCapital",
    [1, 3, 3.8, 4.4, 4.9, 5.4, 5.7, 6, 6.3, 6.6, 6.9, 7.2, 7.4,
    7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 10],
    0, 1000,
    fupdate = "_101_AgriculturalInputsPerHectare.K")

LandYield = AuxVariable(
    "_103_LandYield", "kilograms / hectare / year",
    fupdate = "_104_LandYieldFactor.K"
    "* _121_LandFertility.K"
    "* _102_LandYieldMultiplierFromCapital.K"
    "* _105_LandYieldMultiplierFromAirPollution.K")

LandYieldFactor = PolicyParametrization(
    "_104_LandYieldFactor", 1, 1)

LandYieldMultiplierFromAirPollution = TableParametrization(
    "_105_LandYieldMultiplierFromAirPollution",
    [1, 1, 0.7, 0.4], 0, 30,
    fpoints_after_policy = [1, 1, 0.7, 0.4],
    fupdate = "_050_IndustrialOutput.K"
    "/ _163_IndustrialOutputIn1970.K")

#
# agr106, agr107 - used to be policy tables, now in {agr105}
#

#
# Loops 1 and 2: The Investment Allocation Decision
#
FractionOfInputsAllocatedToLandDevelopment = TableParametrization(
    "_108_FractionOfInputsAllocatedToLandDevelopment",
    [0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.85, 0.95, 1], 0, 2,
    fupdate = "_109_MarginalProductivityOfLandDevelopment.K"
    "/ _110_MarginalProductivityOfAgriculturalInputs.K")

MarginalProductivityOfLandDevelopment = AuxVariable(
    "_109_MarginalProductivityOfLandDevelopment", "kilograms / dollar",
    fupdate = "_103_LandYield.K"
    "/ _097_DevelopmentCostPerHectare.K"
    "/ _164_MarginalProductivityOfLandSocialDiscount.K")

MarginalProductivityOfAgriculturalInputs = AuxVariable(
    "_110_MarginalProductivityOfAgriculturalInputs", "kilograms / dollar",
    fupdate = "_162_AverageLifetimeOfAgriculturalInputs.K"
    "* _103_LandYield.K"
    "* _111_MarginalLandYieldMultiplierFromCapital.K"
    "/ _102_LandYieldMultiplierFromCapital.K")

MarginalLandYieldMultiplierFromCapital = TableParametrization(
    "_111_MarginalLandYieldMultiplierFromCapital",
    [0.075, 0.03, 0.015, 0.011, 0.009, 0.008, 0.007, 0.006,
    0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005],
    0, 600, "hectares / dollar",
    fupdate = "_101_AgriculturalInputsPerHectare.K")

#
# Loop 3: Land Erosion and Urban-Industrial Use
#
AverageLifeOfLand = AuxVariable(
    "_112_AverageLifeOfLand", "years",
    fupdate = "6000 * _113_LandLifeMultiplierFromYield.K") # presumed 6000 years

LandLifeMultiplierFromYield = TableParametrization(
    "_113_LandLifeMultiplierFromYield",
    [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01], 0, 9,
    fpoints_after_policy = [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01],
    fupdate = "_103_LandYield.K / _165_InherentLandFertility.K")

#
# agr114, agr115 - used to be policy tables, now in {113}
#

LandErosionRate = RateVariable(
    "_116_LandErosionRate", "hectares / year",
    fupdate = "_085_ArableLand.K / _112_AverageLifeOfLand.K")

UrbanIndustrialLandPerCapita = TableParametrization(
    "_117_UrbanIndustrialLandPerCapita",
    [0.005, 0.008, 0.015, 0.025, 0.04, 0.055, 0.07, 0.08, 0.09],
    0, 1600, "hectares / person",
    fupdate = "_049_IndustrialOutputPerCapita.K")

UrbanIndustrialLandRequired = AuxVariable(
    "_118_UrbanIndustrialLandRequired", "hectares",
    fupdate = "_117_UrbanIndustrialLandPerCapita.K * _001_Population.K")

LandRemovalForUrbanIndustrialUse = RateVariable(
    "_119_LandRemovalForUrbanIndustrialUse", "hectares / year",
    fupdate = "max(0,"
    "(_118_UrbanIndustrialLandRequired.K"
    "- _120_UrbanIndustrialLand.K)"
    "/ _166_LandRemovalForUrbanIndustrialUseDevelopmentTime.K)")

UrbanIndustrialLand = LevelVariable(
    "_120_UrbanIndustrialLand", "8.2e6", "hectares",
    fupdate = "_119_LandRemovalForUrbanIndustrialUse.J")

#
# Loop 4: Land fertility degradation
#
LandFertility = LevelVariable(
    "_121_LandFertility", "600", "kilograms / hectare / year",
    fupdate = "_124_LandFertilityRegeneration.J"
    "- _123_LandFertilityDegradation.J")

LandFertilityDegradationRate = TableParametrization(
    "_122_LandFertilityDegradationRate",
    [0, 0.1, 0.3, 0.5], 0, 30, "1 / year",
    fupdate = "_143_IndexOfPersistentPollution.K")

LandFertilityDegradation = RateVariable(
    "_123_LandFertilityDegradation", "kilograms / hectare / year^2",
    fupdate = "_121_LandFertility.K * _122_LandFertilityDegradationRate.K")

#
# Loop 5: Land fertility regeneration
#
LandFertilityRegeneration = RateVariable(
    "_124_LandFertilityRegeneration", "kilograms / hectare / year^2",
    fupdate = "(_165_InherentLandFertility.K - _121_LandFertility.K)"
    "/ _125_LandFertilityRegenerationTime.K")

LandFertilityRegenerationTime = TableParametrization(
    "_125_LandFertilityRegenerationTime",
    [20, 13, 8, 4, 2, 2], 0, 0.1, "years",
    fupdate = "_126_FractionOfInputsAllocatedToLandMaintenance.K")

#
# Loop 6: Discontinuing land maintenance
#
FractionOfInputsAllocatedToLandMaintenance = TableParametrization(
    "_126_FractionOfInputsAllocatedToLandMaintenance",
    [0, 0.04, 0.07, 0.09, 0.10], 0, 4,
    fupdate = "_128_PerceivedFoodRatio.K")

FoodRatio = AuxVariable(
    "_127_FoodRatio",
    fupdate = "_088_FoodPerCapita.K"
    "/ _151_SubsistenceFoodPerCapita.K")

PerceivedFoodRatio = SmoothVariable(
    "_128_PerceivedFoodRatio",
    "_167_FoodShortagePerceptionDelay.K",
    fupdate = "_127_FoodRatio.K",   # this will be replaced by value below to break a definition cycle
    initialValue = 1.0)


#
# NONRENEWABLE RESOURCE SUBSYSTEM (equations {129}-{134})
#
# Validated
NonrenewableResources = LevelVariable(
    "_129_NonrenewableResources",
    "_168_NonrenewableResourcesInitial.K", "resource units",
    fupdate = "-_130_NonrenewableResourceUsageRate.J")

# Validated
NonrenewableResourceUsageRate = RateVariable(
    "_130_NonrenewableResourceUsageRate", "resource units / year",
    fupdate = "_001_Population.K"
    "* _132_PerCapitaResourceUsageMultiplier.K"
    "* _131_NonrenewableResourceUsageFactor.K")

# Validated
NonrenewableResourceUsageFactor = PolicyParametrization(
    "_131_NonrenewableResourceUsageFactor", 1, 1)

# Validated
PerCapitaResourceUsageMultiplier = TableParametrization(
    "_132_PerCapitaResourceUsageMultiplier",
    [0, 0.85, 2.6, 4.4, 5.4, 6.2, 6.8, 7, 7],
    0, 1600, "resource units / person / year",
    fupdate = "_049_IndustrialOutputPerCapita.K")

# Validated
NonrenewableResourceFractionRemaining = AuxVariable(
    "_133_NonrenewableResourceFractionRemaining",
    fupdate = "_129_NonrenewableResources.K"
    "/ _168_NonrenewableResourcesInitial.K")

# Validated
FractionOfCapitalAllocatedToObtainingResources = TableParametrization(
    "_134_FractionOfCapitalAllocatedToObtainingResources",
    [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05], 0, 1,
    fpoints_after_policy = [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05],
    fupdate = "_133_NonrenewableResourceFractionRemaining.K")

#
# PERSISTENT POLLUTION SUBSYSTEM  (equations {137}-{146})
#
PersistentPollutionGenerationRate = RateVariable(
    "_137_PersistentPollutionGenerationRate",
    "pollution units / year",
    fupdate = "(_139_PersistentPollutionGeneratedByIndustrialOutput.K"
    "+ _140_PersistentPollutionGeneratedByAgriculturalOutput.K)"
    "* _138_PersistentPollutionGenerationFactor.K")

PersistentPollutionGenerationFactor = PolicyParametrization(
    "_138_PersistentPollutionGenerationFactor", 1, 1)

PersistentPollutionGeneratedByIndustrialOutput = AuxVariable(
    "_139_PersistentPollutionGeneratedByIndustrialOutput",
    "pollution units / year",
    fupdate = "_132_PerCapitaResourceUsageMultiplier.K"
    "* _001_Population.K"
    "* _170_FractionOfResourcesAsPersistentMaterial.K"    
    "* _171_IndustrialMaterialsEmissionFactor.K"
    "* _172_IndustrialMaterialsToxicityIndex.K")

PersistentPollutionGeneratedByAgriculturalOutput = AuxVariable(
    "_140_PersistentPollutionGeneratedByAgriculturalOutput",
    "pollution units / year",
    fupdate =  "_101_AgriculturalInputsPerHectare.K"
    "* _085_ArableLand.K"
    "* _173_AgriculturalOutputAsPersistentMaterial.K"
    "* _174_AgriculturalMaterialsToxicityIndex.K")

PersistenPollutionAppearanceRate = DelayVariable(
    "_141_PersistenPollutionAppearanceRate",
    "_175_PersistentPollutionTransmissionDelay.K",
    "pollution units / year",
    fupdate = "_137_PersistentPollutionGenerationRate.K") 
## persistenPollutionAppearanceRate.Type = "Rate"      # Type change to rate probably not needed

PersistentPollution = LevelVariable(
    "_142_PersistentPollution", "2.5e7", "pollution units",
    fupdate = "_141_PersistenPollutionAppearanceRate.J"
    "- _144_persistenPollutionAssimilationRate.J")

IndexOfPersistentPollution = AuxVariable(
    "_143_IndexOfPersistentPollution",
    fupdate = "_142_PersistentPollution.K"
    "/ _169_PollutionIn1970.K")

PersistenPollutionAssimilationRate = RateVariable(
    "_144_persistenPollutionAssimilationRate",
    "pollution units / year",
    fupdate = "_142_PersistentPollution.K / 1.4"
    "/ _146_AssimilationHalfLife.K")

AssimilationHalfLifeMultiplier = TableParametrization(
    "_145_AssimilationHalfLifeMultiplier",
    [1, 11, 21, 31, 41], 1, 1001,
    fupdate = "_143_IndexOfPersistentPollution.K")

AssimilationHalfLife = AuxVariable(
    "_146_AssimilationHalfLife", "years",
    fupdate =  "1.5 * _145_AssimilationHalfLifeMultiplier.K")
    #AssimilationHalfLife.valueIn1970 = 1.5 # [years]

    
#
# SUPPLEMENTARY EQUATIONS ({147}-{150})
#
# Validated
# Unchanged
GrossProduct = AuxVariable(
    "_147_GrossProduct", "dollars",
    fupdate = "0.22 * _087_Food.K"
    "+ _070_ServiceOutput.K"
    "+ _050_IndustrialOutput.K")

# Validated
# Unchanged
FractionOfOutputInAgriculture = AuxVariable(
    "_148_FractionOfOutputInAgriculture",
    fupdate = "0.22 * _087_Food.K / _147_GrossProduct.K")

# Validated
# Unchanged
FractionOfOutputInIndustry = AuxVariable(
    "_149_FractionOfOutputInIndustry",
    fupdate = "_050_IndustrialOutput.K / _147_GrossProduct.K")

# Validated
# Unchanged
FractionOfOutputInServices = AuxVariable(
    "_150_FractionOfOutputInServices",
    fupdate = "_070_ServiceOutput.K / _147_GrossProduct.K")

#
# PARAMETERS
#
# Validated
# Unchanged
SubsistenceFoodPerCapita = Parameter(
    "_151_SubsistenceFoodPerCapita",
    230, "kilograms / person / year")

# Validated
# Unchanged
EffectiveHealthServicesPerCapitaImpactDelay = Parameter(
    "_152_EffectiveHealthServicesPerCapitaImpactDelay",
    20, "years")

# Validated
# Unchanged
LifetimePerceptionDelay = Parameter(
    "_153_LifetimePerceptionDelay",
    20, "years")

# Validated
# Unchanged
SocialAdjustmentDelay = Parameter(
    "_154_SocialAdjustmentDelay",
    20, "years")

# Validated
# Unchanged
IncomeExpectationAveragingTime = Parameter(
    "_155_IncomeExpectationAveragingTime",
    3, "years")

# Validated
# Unchanged
HealthServicesImpactDelay = Parameter(
    "_156_HealthServicesImpactDelay",
    20, "years")

# Validated
IndicativeConsumptionValue = Parameter(
    "_157_IndicativeConsumptionValue", 400, "dollars / person")

# This is confirmed to be the source of model instability
# for dt>1. The original has it at 2 years; better to put 5 
LaborUtilizationFractionDelayTime = Parameter(
    "_158_LaborUtilizationFractionDelayTime", 5, "years")

PotentiallyArableLandTotal = Parameter(
    "_159_PotentiallyArableLandTotal", 3.2e9, "hectares")

LandFractionHarvested = Parameter(
    "_160_LandFractionHarvested", 0.7)

FoodProcessingLoss = Parameter(
    "_161_FoodProcessingLoss", 0.1)

# This is confirmed to be the source of model instability
# for dt>1. The original has it at 2 years; better to put 3 
AverageLifetimeOfAgriculturalInputs = Parameter(
    "_162_AverageLifetimeOfAgriculturalInputs", 3, "years")

IndustrialOutputIn1970 = Parameter(
    "_163_IndustrialOutputIn1970", 7.9e11, "dollars")

MarginalProductivityOfLandSocialDiscount = Parameter(
    "_164_MarginalProductivityOfLandSocialDiscount", 0.07)

InherentLandFertility = Parameter(
    "_165_InherentLandFertility",
    600, "kilograms / hectare / year")

LandRemovalForUrbanIndustrialUseDevelopmentTime = Parameter(
    "_166_LandRemovalForUrbanIndustrialUseDevelopmentTime",
    10, "years")

FoodShortagePerceptionDelay = Parameter(
    "_167_FoodShortagePerceptionDelay",
    2, "kilograms / hectare / year")

NonrenewableResourcesInitial = Parameter(
    "_168_NonrenewableResourcesInitial", 1.0e12, "resource units")

# Validated
# Unchanged
PollutionIn1970 = Parameter(
    "_169_PollutionIn1970", 1.36e8, "pollution units")

FractionOfResourcesAsPersistentMaterial = Parameter(
    "_170_FractionOfResourcesAsPersistentMaterial", 0.02)

IndustrialMaterialsEmissionFactor = Parameter(
    "_171_IndustrialMaterialsEmissionFactor", 0.1)
    
IndustrialMaterialsToxicityIndex = Parameter(
    "_172_IndustrialMaterialsToxicityIndex", 10,
    "pollution units / dollar")

AgriculturalOutputAsPersistentMaterial = Parameter(
    "_173_AgriculturalOutputAsPersistentMaterial", 0.001)

AgriculturalMaterialsToxicityIndex = Parameter(
    "_174_AgriculturalMaterialsToxicityIndex", 1,
    "pollution units / dollar")

PersistentPollutionTransmissionDelay = Parameter(
    "_175_PersistentPollutionTransmissionDelay", 20,
    "years")
