from DYNAMO_Prototypes import *


#
# PARAMETERS
#
subsistenceFoodPerCapita = Parameter(
    151, "subsistenceFoodPerCapita", 230,
    [20, 127], "kilograms / person / year")
effectiveHealthServicesPerCapitaImpactDelay = Parameter(
    152, "effectiveHealthServicesPerCapitaImpactDelay", 20,
    [22], "years")
lifetimePerceptionDelay = Parameter(
    153, "lifetimePerceptionDelay", 20,
    [37], "years")
socialAdjustmentDelay = Parameter(
    154, "socialAdjustmentDelay", 20,
    [40], "years")
incomeExpectationAveragingTime = Parameter(
    155, "incomeExpectationAveragingTime", 3,
    [43], "years")
healthServicesImpactDelay = Parameter(
    156, "healthServicesImpactDelay", 20,
    [46], "years")


#
# POPULATION SUBSYSTEM (equations {1}-{23}, {26}-{48})
#
population = AuxVariable(
    1, "population", "persons",
    updatefn = lambda : population0To14.K + population15To44.K + \
    population45To64.K + population65AndOver.K)

population0To14 = LevelVariable(
    2, "population0To14", 6.5e8, "persons",
    updatefn = lambda : birthsPerYear.J - deathsPerYear0To14.J - \
    maturationsPerYear14to15.J)

deathsPerYear0To14 = RateVariable(
    3, "deathsPerYear0To14", "persons / year",
    lambda : population0To14.K * mortality0To14.K)

mortality0To14 = TableParametrization(
    4, "mortality0To14",
    [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
    20, 80, "deaths / person / year",
    dependencies = ["lifeExpectancy"])

maturationsPerYear14to15 = RateVariable(
    5, "maturationsPerYear14to15", "persons / year",
    lambda : population0To14.K * (1 - mortality0To14.K) / 15)

population15To44 = LevelVariable(
    6, "population15To44", 7.0e8, "persons",
    updatefn = lambda : maturationsPerYear14to15.J - deathsPerYear15To44.J - maturationsPerYear44to45.J)

deathsPerYear15To44 = RateVariable(
    7, "deathsPerYear15To44", "persons / year",
    lambda : population15To44.K * mortality15To44.K)

mortality15To44 = TableParametrization(
    8, "mortality15To44",
    [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008],
    20, 80, "deaths / person / year",
    dependencies = ["lifeExpectancy"])

maturationsPerYear44to45 = RateVariable(
    9, "maturationsPerYear44to45", "persons / year",
    lambda : population15To44.K * (1 - mortality15To44.K) / 30)

population45To64 = LevelVariable(
    10, "population45To64", 1.9e8, "persons",
    updatefn = lambda : \
    maturationsPerYear44to45.J - deathsPerYear45To64.J - maturationsPerYear64to65.J)

deathsPerYear45To64 = RateVariable(
    11, "deathsPerYear45To64", "persons / year",
    lambda : population45To64.K * mortality45To64.K)

mortality45To64 = TableParametrization(
    12, "mortality45To64",
    [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060],
    20, 80, "deaths / person / year",
    dependencies = ["lifeExpectancy"])

maturationsPerYear64to65 = RateVariable(
    13, "maturationsPerYear64to65", "persons / year",
    lambda : population45To64.K * (1 - mortality45To64.K) / 20)

population65AndOver = LevelVariable(
    14, "population65AndOver", 6.0e7, "persons",
    updatefn = lambda :  maturationsPerYear64to65.J - deathsPerYear65AndOver.J)

deathsPerYear65AndOver = RateVariable(
    15, "deathsPerYear65AndOver", "persons / year",
    lambda : population65AndOver.K * mortality65AndOver.K)

mortality65AndOver = TableParametrization(
    16, "mortality65AndOver",
    [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04], 20, 80, "deaths / person / year",
    dependencies = ["lifeExpectancy"])

deathsPerYear = AuxVariable(
    17, "deathsPerYear", "persons / year",
    updatefn = lambda : deathsPerYear0To14.J + deathsPerYear15To44.J + \
    deathsPerYear45To64.J + deathsPerYear65AndOver.J)

crudeDeathRate = AuxVariable(
    18, "crudeDeathRate", "deaths / 1000 persons / year",
    ["deathsPerYear", "population"],
    lambda : 1000 * deathsPerYear.K / population.K)

lifeExpectancy = AuxVariable(
    19, "lifeExpectancy", "years",
    ["lifetimeMultiplierFromFood",
     "lifetimeMultiplierFromHealthServices",
     "lifetimeMultiplierFromPollution",
     "lifetimeMultiplierFromCrowding"],
    lambda : 32 * lifetimeMultiplierFromFood.K * \
    lifetimeMultiplierFromHealthServices.K * \
    lifetimeMultiplierFromPollution.K * \
    lifetimeMultiplierFromCrowding.K)

lifetimeMultiplierFromFood = TableParametrization(
    20, "lifetimeMultiplierFromFood",
    [0, 1, 1.2, 1.3, 1.35, 1.4], 0, 5,
    dependencies = ["foodPerCapita"],
    norm = subsistenceFoodPerCapita.K)

healthServicesAllocationsPerCapita = TableParametrization(
    21, "healthServicesAllocationsPerCapita",
    [0, 20, 50, 95, 140, 175, 200, 220, 230], 0, 2000,
    "dollars / person / year",
    dependencies = ["serviceOutputPerCapita"])

effectiveHealthServicesPerCapita = SmoothVariable(
    22, "effectiveHealthServicesPerCapita",
    effectiveHealthServicesPerCapitaImpactDelay.K,
    "dollars / person / year",
    ["healthServicesAllocationsPerCapita"])

lifetimeMultiplierFromHealthServices = TableParametrization(
    23, "lifetimeMultiplierFromHealthServices",
    [1, 1.4, 1.6, 1.8, 1.95, 2.0], 0, 100,
    data_1940 = [1, 1.1, 1.4, 1.6, 1.7, 1.8],
    dependencies = ["effectiveHealthServicesPerCapita"])

#
# 24, 25 - used to be policy tables
#

fractionOfPopulationUrban = TableParametrization(
    26, "fractionOfPopulationUrban",
    [0, 0.2, 0.4, 0.5, 0.58, 0.65, 0.72, 0.78, 0.80], 0, 1.6e10,
    dependencies = ["population"])

crowdingMultiplierFromIndustrialization = TableParametrization(
    27, "crowdingMultiplierFromIndustrialization",
    [0.5, 0.05, -0.1, -0.08, -0.02, 0.05, 0.1, 0.15, 0.2], 0, 1600,
    dependencies = ["industrialOutputPerCapita"])

lifetimeMultiplierFromCrowding = AuxVariable(
    28, "lifetimeMultiplierFromCrowding",
    dependencies = ["crowdingMultiplierFromIndustrialization",
                    "fractionOfPopulationUrban"], # added dependency   
    updatefn = lambda : \
    1 - crowdingMultiplierFromIndustrialization.K * fractionOfPopulationUrban.K) 

lifetimeMultiplierFromPollution = TableParametrization(
    29, "lifetimeMultiplierFromPollution",
    [1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.75, 0.65, 0.55, 0.40, 0.20], 0, 100,
    dependencies = ["indexOfPersistentPollution"])

birthsPerYear = RateVariable(
    30, "birthsPerYear", "persons / year",
    lambda : totalFertility.K * population15To44.K * 0.5 / 30,
    lambda : deathsPerYear.K)

crudeBirthRate = AuxVariable(
    31, "crudeBirthRate", "births / 1000 persons / year",
    ["population"],
    lambda : 1000 * birthsPerYear.J / population.K)

totalFertility = AuxVariable(
    32, "totalFertility",
    dependencies = ["maxTotalFertility",
    "fertilityControlEffectiveness", "desiredTotalFertility"],
    updatefn = lambda : min(maxTotalFertility.K,
    (maxTotalFertility.K * (1 - fertilityControlEffectiveness.K) + 
    desiredTotalFertility.K * fertilityControlEffectiveness.K)))

maxTotalFertility = AuxVariable(
    33, "maxTotalFertility",
    dependencies = ["fecundityMultiplier"],
    updatefn = lambda : 12 * fecundityMultiplier.K)   # 12 - max number of births

fecundityMultiplier = TableParametrization(
    34, "fecundityMultiplier",
    [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.05, 1.1], 0, 80,
    dependencies = ["lifeExpectancy"])

desiredTotalFertility = AuxVariable(
    35, "desiredTotalFertility",
    dependencies = [ "desiredCompletedFamilySize",
    "compensatoryMultiplierFromPerceivedLifeExpectancy" ],
    updatefn = lambda : desiredCompletedFamilySize.K * \
    compensatoryMultiplierFromPerceivedLifeExpectancy.K)

compensatoryMultiplierFromPerceivedLifeExpectancy = TableParametrization(
    36, "compensatoryMultiplierFromPerceivedLifeExpectancy",
    [3.0, 2.1, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0], 0, 80,
    dependencies = ["perceivedLifeExpectancy"])

perceivedLifeExpectancy = DelayVariable(
    37, "perceivedLifeExpectancy",
    lifetimePerceptionDelay.K, "years",
    ["lifeExpectancy"])

desiredCompletedFamilySize = AuxVariable(
    38, "desiredCompletedFamilySize", "persons",
    ["familyResponseToSocialNorm", "socialFamilySizeNorm"],
    updatefn = lambda : \
        4 * familyResponseToSocialNorm.K * socialFamilySizeNorm.K,
    equilibriumfn = lambda : 2)

socialFamilySizeNorm = TableParametrization(
    39, "socialFamilySizeNorm",
    [1.25, 1, 0.9, 0.8, 0.75], 0, 800,
    dependencies = ["delayedIndustrialOutputPerCapita"])

delayedIndustrialOutputPerCapita = DelayVariable(
    40, "delayedIndustrialOutputPerCapita",
    socialAdjustmentDelay.K,
    "dollars / person / year",
    ["industrialOutputPerCapita"])

familyResponseToSocialNorm = TableParametrization(
    41, "familyResponseToSocialNorm",
    [0.5, 0.6, 0.7, 0.85, 1.0], -0.2, 0.2,
    dependencies = ["familyIncomeExpectation"])

familyIncomeExpectation = AuxVariable(
    42, "familyIncomeExpectation",
    dependencies = ["industrialOutputPerCapita",
                    "averageIndustrialOutputPerCapita"],
    updatefn = lambda : \
    industrialOutputPerCapita.K / averageIndustrialOutputPerCapita.K - 1)

averageIndustrialOutputPerCapita = SmoothVariable(
    43, "averageIndustrialOutputPerCapita",
    incomeExpectationAveragingTime.K,
    "dollars / person / year",
    ["industrialOutputPerCapita"])

needForFertilityControl = AuxVariable(
    44, "needForFertilityControl",
    dependencies = ["maxTotalFertility", "desiredTotalFertility"],
    updatefn = lambda : maxTotalFertility.K / desiredTotalFertility.K - 1)

fertilityControlEffectiveness = TableParametrization(
    45, "fertilityControlEffectiveness",
    [0.75, 0.85, 0.90, 0.95, 0.98, 0.99, 1.0], 0, 3,
    dependencies = ["fertilityControlFacilitiesPerCapita"])

fertilityControlFacilitiesPerCapita = DelayVariable(
    46, "fertilityControlFacilitiesPerCapita",
    healthServicesImpactDelay.K, "dollars / person / year",
    ["fertilityControlAllocationPerCapita"])

fertilityControlAllocationPerCapita = AuxVariable(
    47, "fertilityControlAllocationPerCapita", "dollars / person / year",
    ["serviceOutputPerCapita", "fractionOfServicesAllocatedToFertilityControl"],
    lambda : fractionOfServicesAllocatedToFertilityControl.K * \
    serviceOutputPerCapita.K)

fractionOfServicesAllocatedToFertilityControl = TableParametrization(
    48, "fractionOfServicesAllocatedToFertilityControl",
    [0.0, 0.005, 0.015, 0.025, 0.030, 0.035], 0, 10,
    dependencies = ["needForFertilityControl"])

foodPerCapita = Parameter(
    171, "foodPerCapita", 800,
    [143], "kg / person / year")

serviceOutputPerCapita = Parameter(
    172, "serviceOutputPerCapita", 100,
    [143], "dollars")

indexOfPersistentPollution = Parameter(
    173, "indexOfPersistentPollution", 1,
    [143])

industrialOutputPerCapita = Parameter(
    174, "industrialOutputPerCapita", 100,
    [143], "dollars / person / year")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.Reset( dt=0.5, global_stability_year=2050, verbose = True)
DYNAMO_Engine.Warmup( verbose = True)
DYNAMO_Engine.Compute( verbose = True)
PlotVariable( population, DYNAMO_Engine.Model_Time, show=True)

##
###
### INDUSTRY SUBSYSTEM (equations {49}-{59})
###
##industrialOutputPerCapita = AuxVariable(
##    49, "industrialOutputPerCapita", "dollars / person / year",
##    ["industrialOutput", "population"],
##    lambda : max( 0.01, industrialOutput.K / population.K))
##
##industrialOutput = AuxVariable(
##    50, "industrialOutput", "dollars / year",
##    ["fractionOfCapitalAllocatedToObtainingResources",
##    "capitalUtilizationFraction",
##    "industrialCapitalOutputRatio"],
##    lambda : industrialCapital.K * (1 - fractionOfCapitalAllocatedToObtainingResources.K) * \
##    capitalUtilizationFraction.K / industrialCapitalOutputRatio.K)
##
##industrialCapitalOutputRatio = PolicyParametrization(
##    51, "industrialCapitalOutputRatio", 3, 3, units="years")
##
##industrialCapital = LevelVariable(
##    52, "industrialCapital", 2.1e11, "dollars",
##    updatefn = lambda : industrialCapitalInvestmentRate.J - industrialCapitalDepreciationRate.J)
##
##industrialCapitalDepreciationRate = RateVariable(
##    53, "industrialCapitalDepreciationRate", "dollars / year",
##    lambda : industrialCapital.K / averageLifetimeOfIndustrialCapital.K)
##
##averageLifetimeOfIndustrialCapital = PolicyParametrization(
##    54, "averageLifetimeOfIndustrialCapital", 14, 14, units="years")
##
##industrialCapitalInvestmentRate = RateVariable(
##    55, "industrialCapitalInvestmentRate", "dollars / year",
##    lambda : industrialOutput.K * fractionOfIndustrialOutputAllocatedToIndustry.K)
##
##fractionOfIndustrialOutputAllocatedToIndustry = AuxVariable(
##    56, "fractionOfIndustrialOutputAllocatedToIndustry",
##    dependencies = ["fractionOfIndustrialOutputAllocatedToAgriculture",
##    "fractionOfIndustrialOutputAllocatedToServices",
##    "fractionOfIndustrialOutputAllocatedToConsumption"],
##    updatefn = lambda : \
##    1 - fractionOfIndustrialOutputAllocatedToAgriculture.K - \
##    fractionOfIndustrialOutputAllocatedToServices.K - \
##    fractionOfIndustrialOutputAllocatedToConsumption.K)
##
##fractionOfIndustrialOutputAllocatedToConsumption = AuxVariable(
##    57, "fractionOfIndustrialOutputAllocatedToConsumption",
##    dependencies = ["fractionOfIndustrialOutputAllocatedToConsumptionVariable"],
##    updatefn = lambda : fractionOfIndustrialOutputAllocatedToConsumptionConstant.K,
##    equilibriumfn = lambda : fractionOfIndustrialOutputAllocatedToConsumptionVariable.K)
##
##fractionOfIndustrialOutputAllocatedToConsumptionConstant = PolicyParametrization(
##    58, "fractionOfIndustrialOutputAllocatedToConsumptionConstant", 0.43, 0.43)
##
##fractionOfIndustrialOutputAllocatedToConsumptionVariable = TableParametrization(
##    59, "fractionOfIndustrialOutputAllocatedToConsumptionVariable",
##    [0.3, 0.32, 0.34, 0.36, 0.38, 0.43, 0.73, 0.77, 0.81, 0.82, 0.83], 0, 2,
##    dependencies = ["industrialOutputPerCapita"],
##    norm = indicativeConsumptionValue.K)
##
##
###
### SERVICES SUBSYSTEM (equations {60}, {63}, {66}-{72})
###
##indicatedServiceOutputPerCapita = TableParametrization(
##    60, "indicatedServiceOutputPerCapita",
##    [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
##    0, 1600, "dollars / person / year",
##    data_after_policy = [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
##    dependencies = ["industrialOutputPerCapita"])
##
###
### 61, 62 - used to be policy tables
###
##
##fractionOfIndustrialOutputAllocatedToServices = TableParametrization(
##    63, "fractionOfIndustrialOutputAllocatedToServices",
##    [0.3, 0.2, 0.1, 0.05, 0], 0, 2,
##    data_after_policy = [0.3, 0.2, 0.1, 0.05, 0],
##    dependencies = ["serviceOutputPerCapita", "indicatedServiceOutputPerCapita"],
##    updatefn = lambda : serviceOutputPerCapita.K / indicatedServiceOutputPerCapita.K)
##
###
### 64, 65 - used to be policy tables
###
##
##serviceCapitalInvestmentRate = RateVariable(
##    66, "serviceCapitalInvestmentRate", "dollars / year",
##    lambda : industrialOutput.K * fractionOfIndustrialOutputAllocatedToServices.K)
##
##serviceCapital = LevelVariable(
##    67, "serviceCapital", 1.44e11, "dollars",
##    updatefn = lambda : serviceCapitalInvestmentRate.J - serviceCapitalDepreciationRate.J)
##
##serviceCapitalDepreciationRate = RateVariable(
##    68, "serviceCapitalDepreciationRate", "dollars / year",
##    lambda : serviceCapital.K / averageLifetimeOfServiceCapital.K)
##
##averageLifetimeOfServiceCapital = PolicyParametrization(
##    69, "averageLifetimeOfServiceCapital", 20, 20, "years")
##
##serviceOutput = AuxVariable(
##    70, "serviceOutput", "dollars / year",
##    ["capitalUtilizationFraction", "serviceCapitalOutputRatio"],
##    lambda : serviceCapital.K * \
##    capitalUtilizationFraction.K / serviceCapitalOutputRatio.K)
##
##serviceOutputPerCapita = AuxVariable(
##    71, "serviceOutputPerCapita", "dollars / person / year",
##    ["serviceOutput", "population"],
##    lambda : serviceOutput.K / population.K)
##
##serviceCapitalOutputRatio = PolicyParametrization(
##    72, "serviceCapitalOutputRatio", 1, 1, "years")
##
###
### LABOR SUBSYSTEM (equations {73}-{83})
###
##jobs = AuxVariable(
##    73, "jobs", "persons",
##    ["potentialJobsInIndustrialSector",
##    "potentialJobsInAgriculturalSector",
##    "potentialJobsInServiceSector"],
##    lambda : \
##    potentialJobsInIndustrialSector.K + \
##    potentialJobsInAgriculturalSector.K + \
##    potentialJobsInServiceSector.K)
##
##potentialJobsInIndustrialSector = AuxVariable(
##    74, "potentialJobsInIndustrialSector", "persons",
##    ["jobsPerIndustrialCapitalUnit"],
##    lambda : \
##    industrialCapital.K * jobsPerIndustrialCapitalUnit.K)
##
##jobsPerIndustrialCapitalUnit = TableParametrization(
##    75, "jobsPerIndustrialCapitalUnit",
##    [0.00037, 0.00018, 0.00012, 0.00009, 0.00007, 0.00006],
##    50, 800, "persons / dollar",
##    dependencies = ["industrialOutputPerCapita"])
##
##potentialJobsInServiceSector = AuxVariable(
##    76, "potentialJobsInServiceSector", "persons",
##    ["jobsPerServiceCapitalUnit"],
##    lambda : \
##    serviceCapital.K * jobsPerServiceCapitalUnit.K)
##
##jobsPerServiceCapitalUnit = TableParametrization(
##    77, "jobsPerServiceCapitalUnit",
##    [.0011, 0.0006, 0.00035, 0.0002, 0.00015, 0.00015],
##    50, 800, "persons / dollar",
##    dependencies = ["serviceOutputPerCapita"])
##
##potentialJobsInAgriculturalSector = AuxVariable(
##    78, "potentialJobsInAgriculturalSector", "persons",
##    ["jobsPerHectare"],
##    lambda : arableLand.K * jobsPerHectare.K)
##
##jobsPerHectare = TableParametrization(
##    79, "jobsPerHectare",
##    [2, 0.5, 0.4, 0.3, 0.27, 0.24, 0.2, 0.2],
##    2, 30, "persons / hectare",
##    dependencies = ["agriculturalInputsPerHectare"])
##
##laborForce = AuxVariable(
##    80, "laborForce", "persons",
##    updatefn = lambda : \
##    0.75 * (population15To44.K + population45To64.K)) # 0.75 - participation fraction
##
##laborUtilizationFraction = AuxVariable(
##    81, "laborUtilizationFraction",
##    dependencies = ["jobs", "laborForce"],
##    updatefn = lambda : jobs.K / laborForce.K)
##
##laborUtilizationFractionDelayed = SmoothVariable(
##    82, "laborUtilizationFractionDelayed",
##    laborUtilizationFractionDelayTime.K,
##    dependencies = ["laborUtilizationFraction"])
##
##capitalUtilizationFraction = TableParametrization(
##    83, "capitalUtilizationFraction",
##    [1.0, 0.9, 0.7, 0.3, 0.1, 0.1], 1, 11,
##    dependencies = ["laborUtilizationFractionDelayed"], # will be taken over by initialValue 
##    updatefn = lambda : laborUtilizationFractionDelayed.K,
##    initialValue = 1.0)
##
###
### AGRICULTURE SUBSYSTEM
### (equations {84}-{89},{92},{93},{96}-{105},{108}-{113},{116}-{128})
###
### Loop 1: Food from Investment in Land Development
###
##landFractionCultivated = AuxVariable(
##    84, "landFractionCultivated",
##    updatefn = lambda : arableLand.K / potentiallyArableLandTotal.K)
##
##arableLand = LevelVariable(
##    85, "arableLand", 0.9e9, "hectares",
##    updatefn = lambda : landDevelopmentRate.J - \
##    landErosionRate.J - landRemovalForUrbanIndustrialUse.J)
##
##potentiallyArableLand = LevelVariable(
##    86, "potentiallyArableLand", 2.3e9, "hectares",
##    updatefn = lambda : -landDevelopmentRate.J)
##
##food = AuxVariable(
##    87, "food", "kilograms / year",
##    ["landYield"],
##    lambda : landYield.K * arableLand.K * \
##    landFractionHarvested.K * (1 - foodProcessingLoss.K))
##
##foodPerCapita = AuxVariable(
##    88, "foodPerCapita", "kilograms / person / year",
##    ["food", "population"],
##    lambda : food.K / population.K)
##
##indicatedFoodPerCapita = TableParametrization(
##    89, "indicatedFoodPerCapita",
##    [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
##    0, 1600, "kilograms / person / year",
##    data_after_policy = [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
##    dependencies = ["industrialOutputPerCapita"])
##
###
### 90, 91 - used to be policy tables
###
##
##totalAgriculturalInvestment = AuxVariable(
##    92, "totalAgriculturalInvestment", "dollars / year",
##    ["industrialOutput", "fractionOfIndustrialOutputAllocatedToAgriculture"],
##    lambda : industrialOutput.K * fractionOfIndustrialOutputAllocatedToAgriculture.K)
##
##fractionOfIndustrialOutputAllocatedToAgriculture = TableParametrization(
##    93, "fractionOfIndustrialOutputAllocatedToAgriculture",
##    [0.4, 0.2, 0.1, 0.025, 0, 0], 0, 2.5,
##    data_after_policy = [0.4, 0.2, 0.1, 0.025, 0, 0],
##    dependencies = ["foodPerCapita", "indicatedFoodPerCapita"],
##    updatefn = lambda : foodPerCapita.K / indicatedFoodPerCapita.K)
##
###
### 94, 95 - used to be policy tables
###
##
##landDevelopmentRate = RateVariable(
##    96, "landDevelopmentRate", "hectares / year",
##    lambda : totalAgriculturalInvestment.K * \
##    fractionOfInputsAllocatedToLandDevelopment.K / \
##    developmentCostPerHectare.K)
##
##developmentCostPerHectare = TableParametrization(
##    97, "developmentCostPerHectare",
##    [100000, 7400, 5200, 3500, 2400, 1500, 750, 300, 150, 75, 50],
##    0, 1.0, "dollars / hectare",
##    dependencies = ["potentiallyArableLand"],
##    norm = potentiallyArableLandTotal.K)
##
###
### Loop 2: Food from Investment in Agricultural Inputs
###
##currentAgriculturalInputs = AuxVariable(
##    98, "currentAgriculturalInputs", "dollars / year",
##    ["totalAgriculturalInvestment",
##     "fractionOfInputsAllocatedToLandDevelopment"],
##    lambda : totalAgriculturalInvestment.K * \
##    (1 - fractionOfInputsAllocatedToLandDevelopment.K))
##
##agriculturalInputs = SmoothVariable(
##    99, "agriculturalInputs",
##    averageLifetimeOfAgriculturalInputs.K,
##    "dollars / year",
##    ["currentAgriculturalInputs"],   # this will be replaced by value below to break a definition cycle
##    initialValue = 5.0e9)
##
###
### output of this equation is unused (replaced with a constant 2)
###
##averageLifetimeOfAgriculturalInputs = PolicyParametrization(
##    100, "averageLifetimeOfAgriculturalInputs", 2, 2, "years")
##
##agriculturalInputsPerHectare = AuxVariable(
##    101, "agriculturalInputsPerHectare", "dollars / hectare / year",
##    ["agriculturalInputs", "fractionOfInputsAllocatedToLandMaintenance"],
##    lambda : agriculturalInputs.K * \
##    (1 - fractionOfInputsAllocatedToLandMaintenance.K) / arableLand.K)
##
##landYieldMultiplierFromCapital = TableParametrization(
##    102, "landYieldMultiplierFromCapital",
##    [1, 3, 3.8, 4.4, 4.9, 5.4, 5.7, 6, 6.3, 6.6, 6.9, 7.2, 7.4,
##     7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 10],
##    0, 1000, dependencies = ["agriculturalInputsPerHectare"])
##
##landYield = AuxVariable(
##    103, "landYield", "kilograms / hectare / year",
##    ["landYieldFactor", "landYieldMultiplierFromCapital",
##     "landYieldMultiplierFromAirPollution"],
##    lambda : landYieldFactor.K * landFertility.K * \
##    landYieldMultiplierFromCapital.K * landYieldMultiplierFromAirPollution.K)
##
##landYieldFactor = PolicyParametrization(
##    104, "landYieldFactor", 1, 1)
##
##landYieldMultiplierFromAirPollution = TableParametrization(
##    105, "landYieldMultiplierFromAirPollution",
##    [1, 1, 0.7, 0.4], 0, 30,
##    data_after_policy = [1, 1, 0.7, 0.4],
##    dependencies = ["industrialOutput"],
##    norm = industrialOutputIn1970.K)
###
### 106, 107 - used to be policy tables
###
##
###
### Loops 1 and 2: The Investment Allocation Decision
###
##fractionOfInputsAllocatedToLandDevelopment = TableParametrization(
##    108, "fractionOfInputsAllocatedToLandDevelopment",
##    [0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.85, 0.95, 1], 0, 2,
##    dependencies = ["marginalProductivityOfLandDevelopment",
##                    "marginalProductivityOfAgriculturalInputs"],
##    updatefn = lambda : \
##        marginalProductivityOfLandDevelopment.K / marginalProductivityOfAgriculturalInputs.K)
##
##marginalProductivityOfLandDevelopment = AuxVariable(
##    109, "marginalProductivityOfLandDevelopment", "kilograms / dollar",
##    ["landYield", "developmentCostPerHectare"],
##    lambda : landYield.K / developmentCostPerHectare.K /\
##    marginalProductivityOfLandSocialDiscount.K)
##
##marginalProductivityOfAgriculturalInputs = AuxVariable(
##    110, "marginalProductivityOfAgriculturalInputs", "kilograms / dollar",
##    ["averageLifetimeOfAgriculturalInputs", "landYield",
##     "marginalLandYieldMultiplierFromCapital",
##     "landYieldMultiplierFromCapital"],
##    lambda : averageLifetimeOfAgriculturalInputs.K * landYield.K * \
##    marginalLandYieldMultiplierFromCapital.K / landYieldMultiplierFromCapital.K)
##
##marginalLandYieldMultiplierFromCapital = TableParametrization(
##    111, "marginalLandYieldMultiplierFromCapital",
##    [0.075, 0.03, 0.015, 0.011, 0.009, 0.008, 0.007, 0.006,
##     0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005],
##    0, 600, "hectares / dollar",
##    dependencies = ["agriculturalInputsPerHectare"])
##
###
### Loop 3: Land Erosion and Urban-Industrial Use
###
##averageLifeOfLand = AuxVariable(
##    112, "averageLifeOfLand", "years",
##    ["landLifeMultiplierFromYield"],
##    lambda : 6000 * landLifeMultiplierFromYield.K) # presumed 6000 years
##
##landLifeMultiplierFromYield = TableParametrization(
##    113, "landLifeMultiplierFromYield",
##    [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01], 0, 9,
##    data_after_policy = [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01],
##    dependencies = ["landYield"], norm = inherentLandFertility.K)
##
###
### 114, 115 - used to be policy tables
###
##
##landErosionRate = RateVariable(
##    116, "landErosionRate", "hectares / year",
##    lambda : arableLand.K / averageLifeOfLand.K)
##
##urbanIndustrialLandPerCapita = TableParametrization(
##    117, "urbanIndustrialLandPerCapita",
##    [0.005, 0.008, 0.015, 0.025, 0.04, 0.055, 0.07, 0.08, 0.09],
##    0, 1600, "hectares / person",
##    dependencies = ["industrialOutputPerCapita"])
##
##urbanIndustrialLandRequired = AuxVariable(
##    118, "urbanIndustrialLandRequired", "hectares",
##    ["urbanIndustrialLandPerCapita", "population"],
##    lambda : urbanIndustrialLandPerCapita.K * population.K)
##
##landRemovalForUrbanIndustrialUse = RateVariable(
##    119, "landRemovalForUrbanIndustrialUse", "hectares / year",
##    lambda : max(0, (urbanIndustrialLandRequired.K - \
##    urbanIndustrialLand.K) / landRemovalForUrbanIndustrialUseDevelopmentTime.K))
##
##urbanIndustrialLand = LevelVariable(
##    120, "urbanIndustrialLand", 8.2e6, "hectares",
##    updatefn = lambda : landRemovalForUrbanIndustrialUse.J)
##
###
### Loop 4: Land fertility degradation
###
##landFertility = LevelVariable(
##    121, "landFertility", 600, "kilograms / hectare / year",
##    updatefn = lambda : landFertilityRegeneration.J - landFertilityDegradation.J)
##
##landFertilityDegradationRate = TableParametrization(
##    122, "landFertilityDegradationRate",
##    [0, 0.1, 0.3, 0.5], 0, 30, "1 / year",
##    dependencies = ["indexOfPersistentPollution"])
##
##landFertilityDegradation = RateVariable(
##    123, "landFertilityDegradation", "kilograms / hectare / year^2",
##    lambda : landFertility.K * landFertilityDegradationRate.K)
##
###
### Loop 5: Land fertility regeneration
###
##landFertilityRegeneration = RateVariable(
##    124, "landFertilityRegeneration", "kilograms / hectare / year^2",
##    lambda : (inherentLandFertility.K - landFertility.K)\
##    / landFertilityRegenerationTime.K)
##
##landFertilityRegenerationTime = TableParametrization(
##    125, "landFertilityRegenerationTime",
##    [20, 13, 8, 4, 2, 2], 0, 0.1, "years",
##    dependencies = ["fractionOfInputsAllocatedToLandMaintenance"])
##
###
### Loop 6: Discontinuing land maintenance
###
##fractionOfInputsAllocatedToLandMaintenance = TableParametrization(
##    126, "fractionOfInputsAllocatedToLandMaintenance",
##    [0, 0.04, 0.07, 0.09, 0.10], 0, 4,
##    dependencies = ["perceivedFoodRatio"])
##
##foodRatio = AuxVariable(
##    127, "foodRatio",
##    dependencies = ["foodPerCapita"],
##    updatefn = lambda : foodPerCapita.K / subsistenceFoodPerCapita.K)
##
##perceivedFoodRatio = SmoothVariable(
##    128, "perceivedFoodRatio",
##    foodShortagePerceptionDelay.K,
##    dependencies = ["foodRatio"],   # this will be replaced by value below to break a definition cycle
##    initialValue = 1.0)
##
###
### NONRENEWABLE RESOURCE SECTOR (equations {129}-{134})
###
##nonrenewableResources = LevelVariable(
##    129, "nonrenewableResources",
##    nonrenewableResourcesInitial.K, "resource units",
##    updatefn = lambda : -nonrenewableResourceUsageRate.J)
##
##nonrenewableResourceUsageRate = RateVariable(
##    130, "nonrenewableResourceUsageRate", "resource units / year",
##    lambda : population.K * perCapitaResourceUsageMultiplier.K \
##    * nonrenewableResourceUsageFactor.K)
##
##nonrenewableResourceUsageFactor = PolicyParametrization(
##    131, "nonrenewableResourceUsageFactor", 1, 1)
##
##perCapitaResourceUsageMultiplier = TableParametrization(
##    132, "perCapitaResourceUsageMultiplier",
##    [0, 0.85, 2.6, 4.4, 5.4, 6.2, 6.8, 7, 7],
##    0, 1600, "resource units / person / year",
##    dependencies = ["industrialOutputPerCapita"])
##
##nonrenewableResourceFractionRemaining = AuxVariable(
##    133, "nonrenewableResourceFractionRemaining",
##    updatefn = lambda : \
##    nonrenewableResources.K / nonrenewableResourcesInitial.K)
##
##fractionOfCapitalAllocatedToObtainingResources = TableParametrization(
##    134, "fractionOfCapitalAllocatedToObtainingResources",
##    [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05], 0, 1,
##    data_after_policy = [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05],
##    dependencies = ["nonrenewableResourceFractionRemaining"])
##
###
### 135, 136 - used to be policy tables
###
##
###
### PERSISTENT POLLUTION SUBSYSTEM  (equations {137}-{146})
###
##persistentPollutionGenerationRate = RateVariable(
##    137, "persistentPollutionGenerationRate", "pollution units / year",
##    lambda : (persistentPollutionGeneratedByIndustrialOutput.K + \
##    persistentPollutionGeneratedByAgriculturalOutput.K) * \
##    persistentPollutionGenerationFactor.K)
##
##persistentPollutionGenerationFactor = PolicyParametrization(
##    138, "persistentPollutionGenerationFactor", 1, 1)
##
##persistentPollutionGeneratedByIndustrialOutput = AuxVariable(
##    139, "persistentPollutionGeneratedByIndustrialOutput",
##    "pollution units / year",
##    ["perCapitaResourceUsageMultiplier", "population"],
##    lambda : perCapitaResourceUsageMultiplier.K * \
##    population.K,
##    norm = 50) # 50 = 1/0.02 - industrial toxisity index
##
##persistentPollutionGeneratedByAgriculturalOutput = AuxVariable(
##    140, "persistentPollutionGeneratedByAgriculturalOutput",
##    "pollution units / year",
##    ["agriculturalInputsPerHectare"],
##    lambda : \
##    agriculturalInputsPerHectare.K * arableLand.K,
##    norm = 1000) # 1000 = 1/0.001 unitless toxicity index
##
##persistenPollutionAppearanceRate = DelayVariable(
##    141, "persistenPollutionAppearanceRate",
##    persistentPollutionTransmissionDelay.K,
##    "pollution units / year",
##    ["persistentPollutionGenerationRate"]) 
##persistenPollutionAppearanceRate.Type = "Rate"      # Type change to rate
##
##persistentPollution = LevelVariable(
##    142, "persistentPollution", 2.5e7, "pollution units",
##    updatefn = lambda : persistenPollutionAppearanceRate.J - persistenPollutionAssimilationRate.J)
##
##indexOfPersistentPollution = AuxVariable(
##    143, "indexOfPersistentPollution",
##    updatefn = lambda : persistentPollution.K,
##    norm = persistentPollutionIn1970.K)
##
##persistenPollutionAssimilationRate = RateVariable(
##    144, "persistenPollutionAssimilationRate", "pollution units / year",
##    lambda : persistentPollution.K / 1.4 / assimilationHalfLife.K)
##
##assimilationHalfLife = TableParametrization(
##    145, "assimilationHalfLife",
##    [1, 11, 21, 31, 41], 1, 1001,
##    dependencies = ["indexOfPersistentPollution"],
##    norm = 2/3)
##
###
### 146 - redundant equation for table multiplication
###
##
###
### SUPPLEMENTARY EQUATIONS ({147}-{150})
###
##grossProduct = AuxVariable(
##    147, "grossProduct", "dollars",
##    ["food", "serviceOutput", "industrialOutput"],
##    lambda : 0.22 * food.K + serviceOutput.K + industrialOutput.K)
##
##fractionOfOutputInAgriculture = AuxVariable(
##    148, "fractionOfOutputInAgriculture",
##    dependencies = ["grossProduct"],
##    updatefn = lambda : 0.22 * food.K / grossProduct.K)
##
##fractionOfOutputInIndustry = AuxVariable(
##    149, "fractionOfOutputInIndustry",
##    dependencies = ["grossProduct"],
##    updatefn = lambda : industrialOutput.K / grossProduct.K)
##
##fractionOfOutputInServices = AuxVariable(
##    150, "fractionOfOutputInServices",
##    dependencies = ["grossProduct"],
##    updatefn = lambda : serviceOutput.K / grossProduct.K)
##
##DYNAMO_Engine.SortByType()
