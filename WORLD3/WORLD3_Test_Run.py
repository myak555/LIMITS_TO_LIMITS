from WORLD3_Boundary_Test import *

#
# PARAMETERS
#
##indicativeConsumptionValue = Parameter(
##    157, "indicativeConsumptionValue", 400,
##    [59], "dollars / person")
##laborUtilizationFractionDelayTime = Parameter(
##    158, "laborUtilizationFractionDelayTime", 2,
##    [82], "years")
##potentiallyArableLandTotal = Parameter(
##    159, "potentiallyArableLandTotal", 3.2e9,
##    [84,97], "hectares")
##landFractionHarvested = Parameter(
##    160, "landFractionHarvested", 0.7,
##    [87])
##foodProcessingLoss = Parameter(
##    161, "foodProcessingLoss", 0.1,
##    [87])
##averageLifetimeOfAgriculturalInputs = Parameter(
##    162, "averageLifetimeOfAgriculturalInputs", 2,
##    [99,100], "years")
##industrialOutputIn1970 = Parameter(
##    163, "industrialOutputIn1970", 7.9e11,
##    [105], "dollars")
##marginalProductivityOfLandSocialDiscount = Parameter(
##    164, "marginalProductivityOfLandSocialDiscount", 0.07,
##    [109])
##inherentLandFertility = Parameter(
##    165, "inherentLandFertility", 600,
##    [113,124], "kilograms / hectare / year")
##landRemovalForUrbanIndustrialUseDevelopmentTime = Parameter(
##    166, "landRemovalForUrbanIndustrialUseDevelopmentTime", 10,
##    [119], "years")
##foodShortagePerceptionDelay = Parameter(
##    167, "foodShortagePerceptionDelay", 2,
##    [128], "kilograms / hectare / year")
##nonrenewableResourcesInitial = Parameter(
##    168, "nonrenewableResourcesInitial", 1.0e12,
##    [129, 133], "resource units")
##persistentPollutionTransmissionDelay = Parameter(
##    169, "persistentPollutionTransmissionDelay", 20,
##    [141], "years")
##persistentPollutionIn1970 = Parameter(
##    170, "persistentPollutionIn1970", 1.36e8,
##    [143], "pollution units")


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
##    [143], "years")
##
#industrialOutputPerCapita = Parameter(
#   174, "industrialOutputPerCapita", 100,
#   [143], "years")

population0To14 = Parameter(
    171, "population0To14", 1e6,
    [143], "persons")
population15To44 = Parameter(
    172, "population15To44", 1e6,
    [143], "persons")
population45To64 = Parameter(
    173, "population45To64", 1e6,
    [143], "persons")
population65AndOver = Parameter(
    174, "population65AndOver", 1e6,
    [143], "persons")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.Reset( dt=5, global_stability_year=2050, verbose = False)
DYNAMO_Engine.Warmup( verbose = False)
DYNAMO_Engine.Compute( verbose = False)

#print(len(DYNAMO_Engine.Model_Time))
#print(len(population.Data))
#print(len(population0To14.Data))
#for i in range(50, len(DYNAMO_Engine.Model_Time)):
#    print( DYNAMO_Engine.Model_Time[i], population.Data[i])

PlotVariable( population, DYNAMO_Engine.Model_Time, show=True)
#PlotVariable( totalFertility, DYNAMO_Engine.Model_Time, show=True)
#PlotVariable( desiredTotalFertility, DYNAMO_Engine.Model_Time, show=True)

##computationSequence = [
##    "population",
##    "deathsPerYear",
##    "lifetimeMultiplierFromCrowding",
##    "industrialCapitalOutputRatio",
##    "averageLifetimeOfIndustrialCapital",
##    "averageLifetimeOfServiceCapital",
##    "serviceCapitalOutputRatio",
##    "laborForce",
##    "landFractionCultivated",
##    "developmentCostPerHectare",
##    "landYieldFactor",
##    "nonrenewableResourceUsageFactor",
##    "nonrenewableResourceFractionRemaining",
##    "persistentPollutionGenerationFactor",
##    "indexOfPersistentPollution",
##    "fractionOfIndustrialOutputAllocatedToConsumptionConstant",
##    "averageLifetimeOfAgriculturalInputs",
##    "laborUtilizationFractionDelayed",
##    "agriculturalInputs",
##    "perceivedFoodRatio",
##    "fractionOfPopulationUrban",
##    "crudeDeathRate",
##    "crudeBirthRate",
##    "fractionOfCapitalAllocatedToObtainingResources",
##    "lifetimeMultiplierFromPollution",
##    "landFertilityDegradationRate",
##    "capitalUtilizationFraction",
##    "industrialOutput",
##    "industrialOutputPerCapita",
##    "delayedIndustrialOutputPerCapita",
##    "socialFamilySizeNorm",
##    "averageIndustrialOutputPerCapita",
##    "familyIncomeExpectation",
##    "familyResponseToSocialNorm",
##    "desiredCompletedFamilySize",
##    "crowdingMultiplierFromIndustrialization",
##    "indicatedServiceOutputPerCapita",
##    "fractionOfIndustrialOutputAllocatedToConsumptionVariable",
##    "fractionOfIndustrialOutputAllocatedToConsumption",
##    "jobsPerIndustrialCapitalUnit",
##    "potentialJobsInIndustrialSector",
##    "serviceOutput",
##    "serviceOutputPerCapita",
##    "fractionOfIndustrialOutputAllocatedToServices",
##    "jobsPerServiceCapitalUnit",
##    "potentialJobsInServiceSector",
##    "healthServicesAllocationsPerCapita",
##    "effectiveHealthServicesPerCapita",
##    "lifetimeMultiplierFromHealthServices",
##    "fractionOfInputsAllocatedToLandMaintenance",
##    "agriculturalInputsPerHectare",
##    "jobsPerHectare",
##    "potentialJobsInAgriculturalSector",
##    "jobs",
##    "laborUtilizationFraction",
##    "landYieldMultiplierFromCapital",
##    "landYieldMultiplierFromAirPollution",
##    "landYield",
##    "marginalProductivityOfLandDevelopment",
##    "marginalLandYieldMultiplierFromCapital",
##    "marginalProductivityOfAgriculturalInputs",
##    "fractionOfInputsAllocatedToLandDevelopment",
##    "food",
##    "foodPerCapita",
##    "indicatedFoodPerCapita",
##    "fractionOfIndustrialOutputAllocatedToAgriculture",
##    "totalAgriculturalInvestment",
##    "currentAgriculturalInputs",
##    "foodRatio",
##    "landFertilityRegenerationTime",
##    "lifetimeMultiplierFromFood",
##    "lifeExpectancy",
##    "mortality0To14",
##    "mortality15To44",
##    "mortality45To64",
##    "mortality65AndOver",
##    "fecundityMultiplier",
##    "perceivedLifeExpectancy",
##    "compensatoryMultiplierFromPerceivedLifeExpectancy",
##    "maxTotalFertility",
##    "desiredTotalFertility",
##    "needForFertilityControl",
##    "fractionOfServicesAllocatedToFertilityControl",
##    "fertilityControlAllocationPerCapita",
##    "fertilityControlFacilitiesPerCapita",
##    "fertilityControlEffectiveness",
##    "totalFertility",
##    "landLifeMultiplierFromYield",
##    "averageLifeOfLand",
##    "urbanIndustrialLandPerCapita",
##    "urbanIndustrialLandRequired",
##    "perCapitaResourceUsageMultiplier",
##    "persistentPollutionGeneratedByIndustrialOutput",
##    "persistentPollutionGeneratedByAgriculturalOutput",
##    "assimilationHalfLife",
##    "fractionOfIndustrialOutputAllocatedToIndustry",
##    "fractionOfOutputInAgriculture",
##    "fractionOfOutputInIndustry",
##    "fractionOfOutputInServices"]
##
##
##Not_Found = []
##for s in computationSequence:
##    if DYNAMO_Engine.byName(s) is not None: continue
##    Not_Found += [s]
##if len(Not_Found) > 0:
##    print()
##    print( "Not found:")
##for s in Not_Found: print( s)

