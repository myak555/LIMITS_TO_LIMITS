from DYNAMO_Prototypes import *
from Utilities import Load_Calibration as clb

GraphShow = False

#
# Population a function of LEB and TFR calibration
#

#
# POPULATION SUBSYSTEM (equations {1}-{48}, {80}, {142})
# as a function of modelled {49}, {71}, {88}, {143}
#
# Validated
Population = AuxVariable(
    "_001_Population", "persons",
    fupdate = "_002_Population0To14.K + _006_Population15To44.K"
    "+ _010_Population45To64.K + _014_Population65AndOver.K")

# Digitized from http://bit-player.org/extras/limits/ltg.html
Population_Check = TableParametrization(
    "_901_Population_Check",
    [1.67E+09,1.88E+09,2.10E+09,2.31E+09,2.57E+09,	
     3.04E+09,3.59E+09,4.23E+09,4.96E+09,5.86E+09,	
     6.80E+09,7.74E+09,8.60E+09,9.24E+09,9.20E+09,	
     8.56E+09,7.66E+09,6.84E+09,6.16E+09,5.60E+09,5.22E+09],
    1900, 2100, "persons",
    fupdate = "DYNAMO_Engine.time")

#
# Population 0-14
#
# Validated
# Initial value changed from 0.65е9 to 0.67e9
Population0To14 = LevelVariable(
    "_002_Population0To14", "0.67e9", "persons",
    fupdate = "_030_BirthsPerYear.J - _003_DeathsPerYear0To14.J"
    "- _005_MaturationsPerYear14to15.J")

# Validated
DeathsPerYear0To14 = RateVariable(
    "_003_DeathsPerYear0To14", "persons / year",
    fupdate = "_002_Population0To14.K * _004_Mortality0To14.K")

# Validated
# The original table from 1972 book:
# [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010]
# These values have been adjusted to match the UN age distribution stats
Mortality0To14 = TableParametrization(
    "_004_Mortality0To14",
    [0.0850, 0.0575, 0.0355, 0.0157, 0.0065, 0.0018, 0.0008],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality0To14, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear14to15 = RateVariable(
    "_005_MaturationsPerYear14to15", "persons / year",
    fupdate = "_002_Population0To14.K"
    "* (1 - _004_Mortality0To14.K) / 15.0")

#
# Population 15-44
#
# Validated
# Initial value changed from 0.70е9 to 0.72e9
Population15To44 = LevelVariable(
    "_006_Population15To44", "0.72e9", "persons",
    fupdate = "_005_MaturationsPerYear14to15.J - _007_DeathsPerYear15To44.J"
    "- _009_MaturationsPerYear44to45.J")

# Validated
# Calibration 0.8 is applied to match the UN age structure data
DeathsPerYear15To44 = RateVariable(
    "_007_DeathsPerYear15To44", "persons / year",
    fupdate = "_006_Population15To44.K * _008_Mortality15To44.K")

# Validated
# The original table from 1972 book:
# [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008]
# These values have been adjusted to match the UN age distribution stats
Mortality15To44 = TableParametrization(
    "_008_Mortality15To44",
    [0.0213, 0.0137, 0.0088, 0.0046, 0.0010, 0.0001, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality15To44, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear44to45 = RateVariable(
    "_009_MaturationsPerYear44to45", "persons / year",
    fupdate = "_006_Population15To44.K * (1 - _008_Mortality15To44.K) / 30.0")

#
# Population 45-64
#

# Validated
# Initial value changed from 0.19е9 to 0.195e9 (for 1.65e9 total population in 1900)
Population45To64 = LevelVariable(
    "_010_Population45To64", "0.195e9", "persons",
    fupdate = "_009_MaturationsPerYear44to45.J - _011_DeathsPerYear45To64.J"
    "- _013_MaturationsPerYear64to65.J")

# Validated
DeathsPerYear45To64 = RateVariable(
    "_011_DeathsPerYear45To64", "persons / year",
    fupdate = "_010_Population45To64.K * _012_Mortality45To64.K")

# Validated
# The original table from 1972 book:
# [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060]
# These values have been adjusted to match the UN age distribution stats
Mortality45To64 = TableParametrization(
    "_012_Mortality45To64",
    [0.0450, 0.0298, 0.0195, 0.0115, 0.0034, 0.0002, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality45To64, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear64to65 = RateVariable(
    "_013_MaturationsPerYear64to65", "persons / year",
    fupdate = "_010_Population45To64.K * (1 - _012_Mortality45To64.K) / 20.0")


#
# Population over 65
#

# Validated
Population65AndOver = LevelVariable(
    "_014_Population65AndOver", "0.060e9", "persons",
    fupdate = "_013_MaturationsPerYear64to65.J - _015_DeathsPerYear65AndOver.J")

# Validated
DeathsPerYear65AndOver = RateVariable(
    "_015_DeathsPerYear65AndOver", "persons / year",
    fupdate = "_014_Population65AndOver.K * _016_Mortality65AndOver.K")

# Validated
# The original table from 1972 book:
# [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04] for the range of [20, 80]
# These values have been adjusted to match the UN age distribution stats
Mortality65AndOver = TableParametrization(
    "_016_Mortality65AndOver",
    [0.129, 0.127, 0.124, 0.120, 0.115, 0.108, 0.098, 0.060, 0.010],
    40, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
#PlotTable( DYNAMO_Engine, Mortality65AndOver, 0, 100, "LifeExpectancy [years]", show=GraphShow)


#
# Death rate and life expectancy
#

# Validated
DeathsPerYear = AuxVariable(
    "_017_DeathsPerYear", "persons / year",
    fupdate = "_003_DeathsPerYear0To14.J  + _007_DeathsPerYear15To44.J"
    "+ _011_DeathsPerYear45To64.J + _015_DeathsPerYear65AndOver.J")

# Validated
CrudeDeathRate = AuxVariable(
    "_018_CrudeDeathRate", "deaths / 1000 persons / year",
    fupdate = "1000 * _017_DeathsPerYear.K / _001_Population.K")

# Validated
# Changed to smooth variable
##LifeExpectancy = AuxVariable(
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
LifetimeMultiplierFromFood = TableParametrization(
    "_020_LifetimeMultiplierFromFood",
    [0, 1, 1.2, 1.3, 1.35, 1.4], 0, 5,
    fupdate = "_088_FoodPerCapita.K / _151_SubsistenceFoodPerCapita.K")
#PlotTable( DYNAMO_Engine, LifetimeMultiplierFromFood, 0, 10,
#           "Subsistence levels [unitless]", show=GraphShow)

# Validated
HealthServicesAllocationsPerCapita = TableParametrization(
    "_021_HealthServicesAllocationsPerCapita",
    [0, 20, 50, 95, 140, 175, 200, 220, 230], 0, 2000,
    "dollars / person / year",
    fupdate = "_071_ServiceOutputPerCapita.K")
#PlotTable( DYNAMO_Engine, HealthServicesAllocationsPerCapita, 0, 2000,
#           "Service Output Per Capita [$/person/year]", show=GraphShow)

# Validated
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
    [0.95,1.26,1.66,1.81,1.90,
     1.95,2.01,2.07,2.13,2.18,
     2.22,2.26,2.28,2.30,2.31,
     2.32,2.33,2.34], 5, 90,
    fupdate = "_022_EffectiveHealthServicesPerCapita.K")
#PlotTable( DYNAMO_Engine, LifetimeMultiplierFromHealthServices, 0, 100,
#           "Effective Health Services Per Capita [$/person/year]", show=GraphShow)


#
# pop024, pop025 - used to be policy tables, now in {pop023}
#

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
CrowdingMultiplierFromIndustrialization = TableParametrization(
    "_027_CrowdingMultiplierFromIndustrialization",
    [0.5, 0.05, -0.1, -0.08, -0.02, 0.05, 0.1, 0.15, 0.2],
    0, 1600,
    fupdate = "_049_IndustrialOutputPerCapita.K")

# Validated
LifetimeMultiplierFromCrowding = AuxVariable(
    "_028_LifetimeMultiplierFromCrowding",
    fupdate = "1 - _027_CrowdingMultiplierFromIndustrialization.K"
    "* _026_FractionOfPopulationUrban.K") 

# Validated
LifetimeMultiplierFromPollution = TableParametrization(
    "_029_LifetimeMultiplierFromPollution",
    [1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.75, 0.65, 0.55, 0.40, 0.20],
    0, 100,
    fupdate = "_143_IndexOfPersistentPollution.K")

# Validated
# Adjustment factor Females20to40Ratio accounts for male-female disbalance
# Fertility period adjusted as a function of LEB to match the UN crude birth rate stats
BirthsPerYear = RateVariable(
    "_030_BirthsPerYear", "persons / year",
    fupdate = "_432_TotalFertility_Check.K"
    "* _006_Population15To44.K"
    "* _230_Females20to40Ratio.K"
    "/ _330_AverageFertilityPeriod.K",
    fequilibrium = "_017_DeathsPerYear.K")

#
# Adjustment based on the UN gender distribution data
# https://ourworldindata.org/gender-ratio
#
Females20to40Ratio  = TableParametrization(
    "_230_Females20to40Ratio",
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
    "_330_AverageFertilityPeriod",
    [26.3,28.3],
    2.8, 5.0, "years",
    fupdate = "_432_TotalFertility_Check.K")
#PlotTable( DYNAMO_Engine, AverageFertilityPeriod,
#    0, 6, "TFR [children per woman]", show=GraphShow)

# Validated
CrudeBirthRate = AuxVariable(
    "_031_CrudeBirthRate", "births / 1000 persons / year",
    fupdate = "1000 * _030_BirthsPerYear.J / _001_Population.K")

# Validated
TotalFertility = AuxVariable(
    "_032_TotalFertility",
    fupdate = "min( _033_MaxTotalFertility.K,"
    "_033_MaxTotalFertility.K * (1 - _045_FertilityControlEffectiveness.K)"
    "+ _035_DesiredTotalFertility.K * _045_FertilityControlEffectiveness.K)")

# Model fit (assuming minor increase of TFR before 1950)
# Note that the UN estimates assume the number of
# *registered live births* per woman; some births in
# the developing countries may be underreported or some
# children (e.g. girls in China) may be unregistered
TotalFertility_Tabular = TableParametrization(
    "_232_TotalFertility_Tabular",
    [5.05, # 1900
     5.05, # 1905
     5.05, # 1910
     5.07, # 1915
     5.09, # 1920
     5.11, # 1925
     5.13, # 1930
     5.13, # 1935
     5.09, # 1940
     5.07, # 1945
     5.05, # 1950
     4.90, # 1955
     4.96, # 1960
     5.01, # 1965
     4.72, # 1970
     4.16, # 1975
     3.71, # 1980
     3.52, # 1985
     3.23, # 1990
     2.87, # 1995
     2.68, # 2000
     2.60, # 2005
     2.54, # 2010
     2.49, # 2015
     2.44, # 2020
     2.39, # 2025
     2.40, # 2030
     2.40, # 2035
     2.46, # 2040
     2.60, # 2045
     2.72, # 2050
     2.84, # 2055
     2.99, # 2060
     3.19, # 2065
     3.45, # 2070
     3.61, # 2075
     3.81, # 2080
     3.99, # 2085
     4.12, # 2090
     4.21, # 2095
     4.36  # 2100
     ],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

FertilityCorrection_WW2 = TableParametrization(
    "_332_FertilityCorrection_WW2",
    [1.0,0.9,0.9,1.0],
    1939, 1947,
    fupdate = "DYNAMO_Engine.time")

TotalFertility_Check = AuxVariable(
    "_432_TotalFertility_Check",
    fupdate = "_232_TotalFertility_Tabular.K"
    "* _332_FertilityCorrection_WW2.K")

# Validated
# max number of births per woman changed (original value 12)
MaxTotalFertility = AuxVariable(
    "_033_MaxTotalFertility",
    fupdate = "10 * _034_FecundityMultiplier.K")
    # 12 - max number of births

# Validated
FecundityMultiplier = TableParametrization(
    "_034_FecundityMultiplier",
    [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.05, 1.1], 0, 80,
    fupdate = "_019_LifeExpectancy.K")

# Validated
DesiredTotalFertility = AuxVariable(
    "_035_DesiredTotalFertility",
    fupdate = "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy.K"
    "* _038_DesiredCompletedFamilySize.K")

# Validated
CompensatoryMultiplierFromPerceivedLifeExpectancy = TableParametrization(
     "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy",
    [3.0, 2.1, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0], 0, 80,
    fupdate = "_037_PerceivedLifeExpectancy.K")

# Validated
PerceivedLifeExpectancy = DelayVariable(
    "_037_PerceivedLifeExpectancy",
    "_153_LifetimePerceptionDelay.K", "years",
    "_019_LifeExpectancy.K")

# Validated
# Original coefficient of 4.0 decreased to match the UN fertility data
DesiredCompletedFamilySize = AuxVariable(
    "_038_DesiredCompletedFamilySize", "persons",
    fupdate = "3.33 * _039_SocialFamilySizeNorm.K",
    fequilibrium = "2.0")

#    "* _041_FamilyResponseToSocialNorm.K",

# Validated
SocialFamilySizeNorm = TableParametrization(
    "_039_SocialFamilySizeNorm",
    [1.05, # 0
     1.03, # 25
     1.00,# 50
     0.98,# 75
     0.95,# 100
     0.93,# 125
     0.66, # 150
     0.66, # 175
     0.66, # 200
     0.7, # 225
     0.7, # 250
     0.7, # 275
     0.7, # 300
     ], 0, 300,
    fupdate = "_040_DelayedIndustrialOutputPerCapita.K")

# Validated
# modify _154_SocialAdjustmentDelay = 20
DelayedIndustrialOutputPerCapita = DelayVariable(
    "_040_DelayedIndustrialOutputPerCapita",
    "_154_SocialAdjustmentDelay.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

# Validated
FamilyResponseToSocialNorm = TableParametrization(
    "_041_FamilyResponseToSocialNorm",
    [0.5, 0.6, 0.7, 0.85, 1.0], -0.2, 0.2,
    fupdate = "_042_FamilyIncomeExpectation.K")

# Validated
FamilyIncomeExpectation = AuxVariable(
    "_042_FamilyIncomeExpectation",
    fupdate = "_049_IndustrialOutputPerCapita.K"
    "/ _043_AverageIndustrialOutputPerCapita.K - 1")

# Validated
AverageIndustrialOutputPerCapita = SmoothVariable(
    "_043_AverageIndustrialOutputPerCapita",
    "_155_IncomeExpectationAveragingTime.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

# Validated
NeedForFertilityControl = AuxVariable(
    "_044_NeedForFertilityControl",
    fupdate = "_033_MaxTotalFertility.K"
    "/ _035_DesiredTotalFertility.K - 1")

# Validated
FertilityControlEffectiveness = TableParametrization(
    "_045_FertilityControlEffectiveness",
    [0.75, 0.85, 0.90, 0.95, 0.98, 0.99, 1.0], 0, 3,
    fupdate = "_046_FertilityControlFacilitiesPerCapita.K")

# Validated
FertilityControlFacilitiesPerCapita = DelayVariable(
    "_046_FertilityControlFacilitiesPerCapita",
    "_156_HealthServicesImpactDelay.K",
    "dollars / person / year",
    "_047_FertilityControlAllocationPerCapita.K")

# Validated
FertilityControlAllocationPerCapita = AuxVariable(
    "_047_FertilityControlAllocationPerCapita",
    "dollars / person / year",
    fupdate = "_048_FractionOfServicesAllocatedToFertilityControl.K"
    "* _071_ServiceOutputPerCapita.K")

# Validated
FractionOfServicesAllocatedToFertilityControl = TableParametrization(
    "_048_FractionOfServicesAllocatedToFertilityControl",
    [0.0, 0.005, 0.015, 0.025, 0.030, 0.035], 0, 10,
    fupdate = "_044_NeedForFertilityControl.K")

# Check, based on numerical simulation
IndustrialOutputPerCapita = TableParametrization(
    "_049_IndustrialOutputPerCapita",
    [42.0,48.3,53.6,59.4,66.0,
     73.5,82.0,91.7,102.5,111.3,
     120.9,131.3,142.7,155.1,168.1,
     181.3,194.5,207.3,219.8,232.3,
     245.4,259.1,273.2,287.8,295.2,
     294.2,278.9,222.7,174.3,141.8,
     117.1,97.7,81.5,67.5,55.7,
     46.0,37.9,31.2,25.7,21.1,17.3],
    1900,2100, "dollars / person / year",
    fupdate = "DYNAMO_Engine.time")

# Check, based on numerical simulation
ServiceOutputPerCapita = TableParametrization(
    "_071_ServiceOutputPerCapita",
    [87.6,88.7,93.2,100.1,108.5,
     118.2,129.1,141.3,155.0,165.7,
     177.9,191.3,205.8,221.6,238.7,
     256.6,274.7,292.9,312.7,333.6,
     355.6,378.7,402.8,428.0,451.8,
     467.2,470.8,451.7,402.8,351.6,
     310.4,275.7,243.1,211.3,182.6,
     158.2,137.3,119.4,104.1,91.0,79.6],
    1900,2100, "dollars / person / year",
    fupdate = "DYNAMO_Engine.time")

# Validated
LaborForce = AuxVariable(
    "_080_LaborForce", "persons",
    fupdate = "0.75 * (_006_Population15To44.K"
    "+ _010_Population45To64.K)")
    # 0.75 - participation fraction

# Check, based on numerical simulation
FoodPerCapita = TableParametrization(
    "_088_FoodPerCapita",
    [283.4,276.2,278.3,282.5,288.8,
     296.8,306.2,317.0,329.4,335.6,
     344.1,353.7,364.4,376.7,378.9,
     381.6,383.8,385.4,386.2,385.7,
     385.9,386.0,385.2,382.7,378.2,
     368.1,348.3,313.2,264.1,218.7,
     192.6,182.9,188.4,199.0,192.3,
     188.9,187.2,186.9,188.2,190.6,193.8],
    1900,2100, "kilograms / person / year",
    fupdate = "DYNAMO_Engine.time")

# Check, based on numerical simulation
PersistentPollution = TableParametrization(
    "_142_PersistentPollution",
    [2.345e+07,2.184e+07,2.225e+07,2.373e+07,2.640e+07,
     3.022e+07,3.512e+07,4.111e+07,4.826e+07,5.674e+07,
     6.676e+07,7.865e+07,9.272e+07,1.093e+08,1.287e+08,
     1.517e+08,1.801e+08,2.150e+08,2.575e+08,3.094e+08,
     3.727e+08,4.496e+08,5.429e+08,6.561e+08,7.922e+08,
     9.544e+08,1.142e+09,1.345e+09,1.531e+09,1.640e+09,
     1.624e+09,1.493e+09,1.295e+09,1.075e+09,8.644e+08,
     6.791e+08,5.251e+08,4.027e+08,3.079e+08,2.353e+08,1.799e+08],
    1900,2100, "pollution units",
    fupdate = "DYNAMO_Engine.time")

# Validated
IndexOfPersistentPollution = AuxVariable(
    "_143_IndexOfPersistentPollution",
    fupdate = "_142_PersistentPollution.K"
    "/ _169_PollutionIn1970.K")

# Validated
SubsistenceFoodPerCapita = Parameter(
    "_151_SubsistenceFoodPerCapita",
    230, "kilograms / person / year")

# Validated
EffectiveHealthServicesPerCapitaImpactDelay = Parameter(
    "_152_EffectiveHealthServicesPerCapitaImpactDelay",
    20, "years")

# Validated
LifetimePerceptionDelay = Parameter(
    "_153_LifetimePerceptionDelay",
    20, "years")

# Validated
SocialAdjustmentDelay = Parameter(
    "_154_SocialAdjustmentDelay",
    20, "years")

# Validated
IncomeExpectationAveragingTime = Parameter(
    "_155_IncomeExpectationAveragingTime",
    3, "years")

# Validated
HealthServicesImpactDelay = Parameter(
    "_156_HealthServicesImpactDelay",
    20, "years")


# Validated
PollutionIn1970 = Parameter(
    "_169_PollutionIn1970", 1.36e8, "pollution units")


DYNAMO_Engine.SortByType()
DYNAMO_Engine.Produce_Solution_Path( verbose = False)
#DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=0.5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )
DYNAMO_Engine.ListEquations()

limits = (1900, 2100)
fig = plt.figure( figsize=(15,15))
fig.suptitle('Population "World3" as a function of output per capita', fontsize=25)
gs = plt.GridSpec(3, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

yUrban, pTotal, Urban = clb("./Calibrations/Urban_Population_UN.txt",
                     ["Year", "Population", "Urban"], separator="\t")
ax1.set_title("Urbanization", fontsize=18)
ax1.plot( DYNAMO_Engine.Model_Time, np.array(Population.Data)*1e-9, "-",
          lw=2, color="b", label="Total Population")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array(Population.Data)*1e-9*np.array(FractionOfPopulationUrban.Data), "-",
          lw=2, color="r", label="Urban Population")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array(LaborForce.Data)*1e-9, "-",
          lw=2, color="g", label="Labor Force")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array(FertilityControlEffectiveness.Data), "-",
          lw=2, color="m", label="Fertility Control Effectiveness")
ax1.errorbar( yUrban, pTotal*1.e-3, yerr=pTotal*5.e-5, fmt=".",
              color="k", alpha=0.5, label="(UN actual)")
ax1.errorbar( yUrban, Urban*1.e-3, yerr=Urban*5.e-5, fmt=".",
              color="r", alpha=0.5)
ax1.set_ylabel("billion")
ax1.set_xlim( limits)
ax1.set_ylim( 0, 1.5)
ax1.grid(True)
ax1.legend(loc=0)

yLEB, LEB = clb("./Calibrations/Life_Expectancy_OWID.txt", ["Year", "LEB"], separator="\t")
yTFR, TFR = clb("./Calibrations/Fertility_Rate_OWID.txt", ["Year", "TFR"], separator="\t")
#ax2.plot( DYNAMO_Engine.Model_Time, np.array(LifeExpectancy.Data), "-",
#          lw=2, color="m", label="LEB")
#ax2.plot( DYNAMO_Engine.Model_Time, np.array(PerceivedLifeExpectancy.Data), "--",
#          lw=2, color="m", label="LEB Percieved")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(MaxTotalFertility.Data)*10, ".",
          lw=1, color="g", label="TFR Max")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(TotalFertility.Data)*10, "-",
          lw=2, color="g", label="TFR")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(TotalFertility_Check.Data)*10, "-.",
          lw=2, color="g", label="Check TFR")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(DesiredTotalFertility.Data)*10, "--",
          lw=3, color="g", label="Desired TFR")

#ax2.errorbar( yLEB, LEB, yerr=2.5, fmt=".", color="r", alpha=0.5, label="(OWID own estimates)")
ax2.errorbar( yTFR, TFR*10, yerr=3, fmt=".", color="g", alpha=0.5)
ax2.set_xlim( limits)
ax2.set_ylim( 0, 80)
ax2.set_ylabel("LEB[years], TFR[x10]")
ax2.grid(True)
ax2.legend(loc=0)

year_BH, gpc_BH, spc_BH, fpc_BH, pind_BH = clb("./Calibrations/BAU_Output_View_BHayes.txt",
                ["Year", "GoodsPC", "ServicesPC", "FoodPC", "PollutionIndex"], separator="\t")
ax3.plot( DYNAMO_Engine.Model_Time, np.array(IndustrialOutputPerCapita.Data), "-",
          lw=2, color="r", label="Goods [kg/capita/year]")
ax3.plot( DYNAMO_Engine.Model_Time, np.array(DelayedIndustrialOutputPerCapita.Data), "-.",
          lw=2, color="r", label="Goods delayed [kg/capita/year]")
ax3.plot( DYNAMO_Engine.Model_Time, np.array(AverageIndustrialOutputPerCapita.Data), "--",
          lw=2, color="r", label="Goods smooth [kg/capita/year]")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(ServiceOutputPerCapita.Data), "-",
#          lw=2, color="y", label="Services [$/capita/year]")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(FertilityControlFacilitiesPerCapita.Data), "--",
#          lw=2, color="y", label="Fertility Control Facilities [$/capita/year]")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(FoodPerCapita.Data), "-",
#          lw=2, color="g", label="Food [kg/capita/year]")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(IndexOfPersistentPollution.Data)*10, "-",
#          lw=2, color="m", label="Pollution index x 10 [relative to 1970]")
ax3.plot( year_BH, gpc_BH, "--", lw=2, color="r", alpha=0.5)
#ax3.plot( year_BH, spc_BH, "--", lw=2, color="y", alpha=0.5)
ax3.plot( year_BH, fpc_BH, "--", lw=2, color="g", alpha=0.5)
ax3.plot( year_BH, pind_BH*10, "--", lw=2, color="m", alpha=0.5)
ax3.set_xlim( limits)
ax3.set_ylim( 0, 700)
ax3.legend(loc=0)
ax3.grid(True)
ax3.set_xlabel("Year")
ax3.set_ylabel("Units")

plt.savefig( "./Calibrations/Calibration_03.png")
plt.show()

#PlotVariable( _549_IndustrialOutputPerCapita_Reference, DYNAMO_Engine.Model_Time,
#    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
#    show=True)
