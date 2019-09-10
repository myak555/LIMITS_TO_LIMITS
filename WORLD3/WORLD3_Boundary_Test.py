from DYNAMO_Prototypes import *

#
# This run checks only the population subsystem,
# presuming the industry, agriculture and services
# outputs per capita to be constant (equations {171}-{174})
#

#
# POPULATION SUBSYSTEM (equations {1}-{23}, {26}-{48})
#

f001 = AuxVariable(
    1, "population", "persons",
    updatefn = lambda : f001.p("population0To14").K + \
    f001.p("population15To44").K + f001.p("population45To64").K + \
    f001.p("population65AndOver").K)

class c1:
    def __init__(self):
        self.J = 10.0
        self.K = 3.0
        self.D = "Hello" \
                 "World"

a = c1()

##population0To14 = LevelVariable(
##    2, "population0To14", 6.5e8, "persons",
##    updatefn = lambda : birthsPerYear.J - deathsPerYear0To14.J - \
##    maturationsPerYear14to15.J)
##deathsPerYear0To14 = RateVariable(
##    3, "deathsPerYear0To14", "persons / year",
##    lambda : population0To14.K * mortality0To14.K)
##mortality0To14 = TableParametrization(
##    4, "mortality0To14",
##    [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
##    20, 80, "deaths / person / year",
##    dependencies = ["lifeExpectancy"])
##maturationsPerYear14to15 = RateVariable(
##    5, "maturationsPerYear14to15", "persons / year",
##    lambda : population0To14.K * (1 - mortality0To14.K) / 15)
##population15To44 = LevelVariable(
##    6, "population15To44", 7.0e8, "persons",
##    updatefn = lambda : maturationsPerYear14to15.J - deathsPerYear15To44.J - maturationsPerYear44to45.J)
##deathsPerYear15To44 = RateVariable(
##    7, "deathsPerYear15To44", "persons / year",
##    lambda : population15To44.K * mortality15To44.K)
##mortality15To44 = TableParametrization(
##    8, "mortality15To44",
##    [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008],
##    20, 80, "deaths / person / year",
##    dependencies = ["lifeExpectancy"])
##maturationsPerYear44to45 = RateVariable(
##    9, "maturationsPerYear44to45", "persons / year",
##    lambda : population15To44.K * (1 - mortality15To44.K) / 30)
##population45To64 = LevelVariable(
##    10, "population45To64", 1.9e8, "persons",
##    updatefn = lambda : \
##    maturationsPerYear44to45.J - deathsPerYear45To64.J - \
##    maturationsPerYear64to65.J)
##deathsPerYear45To64 = RateVariable(
##    11, "deathsPerYear45To64", "persons / year",
##    lambda : population45To64.K * mortality45To64.K)
##mortality45To64 = TableParametrization(
##    12, "mortality45To64",
##    [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060],
##    20, 80, "deaths / person / year",
##    dependencies = ["lifeExpectancy"])
##maturationsPerYear64to65 = RateVariable(
##    13, "maturationsPerYear64to65", "persons / year",
##    lambda : population45To64.K * (1 - mortality45To64.K) / 20)
##population65AndOver = LevelVariable(
##    14, "population65AndOver", 6.0e7, "persons",
##    updatefn = lambda :  maturationsPerYear64to65.J - \
##    deathsPerYear65AndOver.J)
##deathsPerYear65AndOver = RateVariable(
##    15, "deathsPerYear65AndOver", "persons / year",
##    lambda : population65AndOver.K * mortality65AndOver.K)
##mortality65AndOver = TableParametrization(
##    16, "mortality65AndOver",
##    [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04], 20, 80, "deaths / person / year",
##    dependencies = ["lifeExpectancy"])
##deathsPerYear = AuxVariable(
##    17, "deathsPerYear", "persons / year",
##    updatefn = lambda : deathsPerYear0To14.J + deathsPerYear15To44.J + \
##    deathsPerYear45To64.J + deathsPerYear65AndOver.J)
##crudeDeathRate = AuxVariable(
##    18, "crudeDeathRate", "deaths / 1000 persons / year",
##    ["deathsPerYear", "population"],
##    lambda : 1000 * deathsPerYear.K / population.K)
##lifeExpectancy = AuxVariable(
##    19, "lifeExpectancy", "years",
##    ["lifetimeMultiplierFromFood",
##     "lifetimeMultiplierFromHealthServices",
##     "lifetimeMultiplierFromPollution",
##     "lifetimeMultiplierFromCrowding"],
##    lambda : 32 * lifetimeMultiplierFromFood.K * \
##    lifetimeMultiplierFromHealthServices.K * \
##    lifetimeMultiplierFromPollution.K * \
##    lifetimeMultiplierFromCrowding.K)
##lifetimeMultiplierFromFood = TableParametrization(
##    20, "lifetimeMultiplierFromFood",
##    [0, 1, 1.2, 1.3, 1.35, 1.4], 0, 5,
##    dependencies = ["foodPerCapita"],
##    normfn = lambda: subsistenceFoodPerCapita.K)
##healthServicesAllocationsPerCapita = TableParametrization(
##    21, "healthServicesAllocationsPerCapita",
##    [0, 20, 50, 95, 140, 175, 200, 220, 230], 0, 2000,
##    "dollars / person / year",
##    dependencies = ["serviceOutputPerCapita"])
##effectiveHealthServicesPerCapita = SmoothVariable(
##    22, "effectiveHealthServicesPerCapita",
##    lambda: effectiveHealthServicesPerCapitaImpactDelay.K,
##    "dollars / person / year",
##    ["healthServicesAllocationsPerCapita"])
##lifetimeMultiplierFromHealthServices = TableParametrization(
##    23, "lifetimeMultiplierFromHealthServices",
##    [1, 1.4, 1.6, 1.8, 1.95, 2.0], 0, 100,
##    data_1940 = [1, 1.1, 1.4, 1.6, 1.7, 1.8],
##    dependencies = ["effectiveHealthServicesPerCapita"])
###
### 24, 25 - used to be policy tables, now in {23}
###
##fractionOfPopulationUrban = TableParametrization(
##    26, "fractionOfPopulationUrban",
##    [0, 0.2, 0.4, 0.5, 0.58, 0.65, 0.72, 0.78, 0.80], 0, 1.6e10,
##    dependencies = ["population"])
##crowdingMultiplierFromIndustrialization = TableParametrization(
##    27, "crowdingMultiplierFromIndustrialization",
##    [0.5, 0.05, -0.1, -0.08, -0.02, 0.05, 0.1, 0.15, 0.2], 0, 1600,
##    dependencies = ["industrialOutputPerCapita"])
##lifetimeMultiplierFromCrowding = AuxVariable(
##    28, "lifetimeMultiplierFromCrowding",
##    dependencies = ["crowdingMultiplierFromIndustrialization",
##                    "fractionOfPopulationUrban"], # added dependency   
##    updatefn = lambda : \
##    1 - crowdingMultiplierFromIndustrialization.K * \
##    fractionOfPopulationUrban.K) 
##lifetimeMultiplierFromPollution = TableParametrization(
##    29, "lifetimeMultiplierFromPollution",
##    [1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.75, 0.65, 0.55, 0.40, 0.20],
##    0, 100,
##    dependencies = ["indexOfPersistentPollution"])
##birthsPerYear = RateVariable(
##    30, "birthsPerYear", "persons / year",
##    lambda : totalFertility.K * population15To44.K * 0.5 / 30,
##    lambda : deathsPerYear.K)
##crudeBirthRate = AuxVariable(
##    31, "crudeBirthRate", "births / 1000 persons / year",
##    ["population"],
##    lambda : 1000 * birthsPerYear.J / population.K)
##totalFertility = AuxVariable(
##    32, "totalFertility",
##    dependencies = ["maxTotalFertility",
##    "fertilityControlEffectiveness", "desiredTotalFertility"],
##    updatefn = lambda : min(maxTotalFertility.K,
##    (maxTotalFertility.K * (1 - fertilityControlEffectiveness.K) + 
##    desiredTotalFertility.K * fertilityControlEffectiveness.K)))
##maxTotalFertility = AuxVariable(
##    33, "maxTotalFertility",
##    dependencies = ["fecundityMultiplier"],
##    updatefn = lambda : 12 * fecundityMultiplier.K)
##    # 12 - max number of births
##fecundityMultiplier = TableParametrization(
##    34, "fecundityMultiplier",
##    [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.05, 1.1], 0, 80,
##    dependencies = ["lifeExpectancy"])
##desiredTotalFertility = AuxVariable(
##    35, "desiredTotalFertility",
##    dependencies = [ "desiredCompletedFamilySize",
##    "compensatoryMultiplierFromPerceivedLifeExpectancy" ],
##    updatefn = lambda : desiredCompletedFamilySize.K * \
##    compensatoryMultiplierFromPerceivedLifeExpectancy.K)
##compensatoryMultiplierFromPerceivedLifeExpectancy = TableParametrization(
##    36, "compensatoryMultiplierFromPerceivedLifeExpectancy",
##    [3.0, 2.1, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0], 0, 80,
##    dependencies = ["perceivedLifeExpectancy"])
##perceivedLifeExpectancy = DelayVariable(
##    37, "perceivedLifeExpectancy",
##    lambda: lifetimePerceptionDelay.K, "years",
##    ["lifeExpectancy"])
##desiredCompletedFamilySize = AuxVariable(
##    38, "desiredCompletedFamilySize", "persons",
##    ["familyResponseToSocialNorm", "socialFamilySizeNorm"],
##    updatefn = lambda : \
##        4 * familyResponseToSocialNorm.K * socialFamilySizeNorm.K,
##    equilibriumfn = lambda : 2)
##socialFamilySizeNorm = TableParametrization(
##    39, "socialFamilySizeNorm",
##    [1.25, 1, 0.9, 0.8, 0.75], 0, 800,
##    dependencies = ["delayedIndustrialOutputPerCapita"])
##delayedIndustrialOutputPerCapita = DelayVariable(
##    40, "delayedIndustrialOutputPerCapita",
##    lambda:socialAdjustmentDelay.K,
##    "dollars / person / year",
##    ["industrialOutputPerCapita"])
##familyResponseToSocialNorm = TableParametrization(
##    41, "familyResponseToSocialNorm",
##    [0.5, 0.6, 0.7, 0.85, 1.0], -0.2, 0.2,
##    dependencies = ["familyIncomeExpectation"])
##familyIncomeExpectation = AuxVariable(
##    42, "familyIncomeExpectation",
##    dependencies = ["industrialOutputPerCapita",
##                    "averageIndustrialOutputPerCapita"],
##    updatefn = lambda : \
##    industrialOutputPerCapita.K / averageIndustrialOutputPerCapita.K - 1)
##averageIndustrialOutputPerCapita = SmoothVariable(
##    43, "averageIndustrialOutputPerCapita",
##    lambda: incomeExpectationAveragingTime.K,
##    "dollars / person / year",
##    ["industrialOutputPerCapita"])
##needForFertilityControl = AuxVariable(
##    44, "needForFertilityControl",
##    dependencies = ["maxTotalFertility", "desiredTotalFertility"],
##    updatefn = lambda : maxTotalFertility.K / desiredTotalFertility.K - 1)
##fertilityControlEffectiveness = TableParametrization(
##    45, "fertilityControlEffectiveness",
##    [0.75, 0.85, 0.90, 0.95, 0.98, 0.99, 1.0], 0, 3,
##    dependencies = ["fertilityControlFacilitiesPerCapita"])
##fertilityControlFacilitiesPerCapita = DelayVariable(
##    46, "fertilityControlFacilitiesPerCapita",
##    lambda: healthServicesImpactDelay.K, "dollars / person / year",
##    ["fertilityControlAllocationPerCapita"])
##fertilityControlAllocationPerCapita = AuxVariable(
##    47, "fertilityControlAllocationPerCapita", "dollars / person / year",
##    ["serviceOutputPerCapita", "fractionOfServicesAllocatedToFertilityControl"],
##    lambda : fractionOfServicesAllocatedToFertilityControl.K * \
##    serviceOutputPerCapita.K)
##fractionOfServicesAllocatedToFertilityControl = TableParametrization(
##    48, "fractionOfServicesAllocatedToFertilityControl",
##    [0.0, 0.005, 0.015, 0.025, 0.030, 0.035], 0, 10,
##    dependencies = ["needForFertilityControl"])
##
###
### PARAMETERS
###
##subsistenceFoodPerCapita = Parameter(
##    151, "subsistenceFoodPerCapita", 230,
##    [20, 127], "kilograms / person / year")
##effectiveHealthServicesPerCapitaImpactDelay = Parameter(
##    152, "effectiveHealthServicesPerCapitaImpactDelay", 20,
##    [22], "years")
##lifetimePerceptionDelay = Parameter(
##    153, "lifetimePerceptionDelay", 20,
##    [37], "years")
##socialAdjustmentDelay = Parameter(
##    154, "socialAdjustmentDelay", 20,
##    [40], "years")
##incomeExpectationAveragingTime = Parameter(
##    155, "incomeExpectationAveragingTime", 3,
##    [43], "years")
##healthServicesImpactDelay = Parameter(
##    156, "healthServicesImpactDelay", 20,
##    [46], "years")

#
# FIXED PARAMETERS (this test only)
#
##foodPerCapita = Parameter(
##    171, "foodPerCapita", 800,
##    [143], "kg / person / year")
##
##serviceOutputPerCapita = Parameter(
##    172, "serviceOutputPerCapita", 100,
##    [143], "dollars")
##
##indexOfPersistentPollution = Parameter(
##    173, "indexOfPersistentPollution", 1,
##    [143])
##
##industrialOutputPerCapita = Parameter(
##    174, "industrialOutputPerCapita", 100,
##    [143], "dollars / person / year")

#DYNAMO_Engine.SortByType()
#DYNAMO_Engine.Produce_Solution_Path( verbose = True)
#DYNAMO_Engine.Reset( dt=0.5, global_stability_year=2050, verbose = True)
#DYNAMO_Engine.Warmup( verbose = True)
#DYNAMO_Engine.Compute( verbose = True)
#PlotVariable( population, DYNAMO_Engine.Model_Time, show=True)
