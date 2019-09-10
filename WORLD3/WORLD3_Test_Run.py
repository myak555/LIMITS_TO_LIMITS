#from WORLD3_Boundary_Test import *

class c2:
    def __init__(self):
        self.J = 10.0
        self.K = 3.0

a = c2()
_1b = c2()

print( eval("a.J + _1b.K"))
print( eval("a.J + _1b.K"))

#fun_dict = {}
for f in [a, _1b]:
    print(f.__name__)
    #fun_dict[f.__name__] = f

##
##
##def extractDependencies( line):
##    """
##    class name starts with an underscore, then has 3-digit
##    number, then any combination of letters, numbers and underscores
##    """
##    digits = "0123456789"
##    symbols = digits + "_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
##    tmp = []
##    pos = 0
##    next_name = ""
##    in_name = False
##    for i, c in enumerate(line):
##        in_symbols = c in symbols
##        if not in_name and not in_symbols:
##            continue
##        if in_name and in_symbols:
##            next_name += c
##            continue
##        if not in_name and in_symbols:
##            in_name = True
##            next_name += c
##            continue
##        in_name = False
##        tmp += [next_name]
##        next_name = ""
##        continue
##    ret = []
##    for s in tmp:
##        if s[0] != '_' : continue
##        if not s[1] in digits: continue
##        if not s[2] in digits: continue
##        if not s[3] in digits: continue
##        if s[4] != '_' : continue
##        ret += [s]
##    return ret
##
##Line = "max(_012_population / _025_popNorm*3, 3)"
##print( extractName( Line))
    
##
###
### FIXED PARAMETERS (this test only)
###
##par201 = PolicyParametrization(
##    201, "foodPerCapita", 800, 400,
##    "kg / person / year")
##
##par202 = Parameter(
##    202, "serviceOutputPerCapita", 100,
##    [], "dollars")
##
##par203 = Parameter(
##    203, "indexOfPersistentPollution", 1,
##    [])
##
##par204 = Parameter(
##    204, "industrialOutputPerCapita", 100,
##    [], "dollars / person / year")
##
###
###Test_Run
###
##DYNAMO_Engine.SortByType()
##DYNAMO_Engine.ListEquations()
##DYNAMO_Engine.Produce_Solution_Path( verbose = True)
##DYNAMO_Engine.ListSolutionPath()
##DYNAMO_Engine.Reset(
##    dt=5, global_policy_year=2020,
##    global_stability_year=2050,
##    verbose = True)
##DYNAMO_Engine.Warmup( verbose = True)
##DYNAMO_Engine.Compute( verbose = True)
##PlotVariable( "population", DYNAMO_Engine.Model_Time,
##              filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##
##
###
### PARAMETERS
###
####indicativeConsumptionValue = Parameter(
####    157, "indicativeConsumptionValue", 400,
####    [59], "dollars / person")
####laborUtilizationFractionDelayTime = Parameter(
####    158, "laborUtilizationFractionDelayTime", 2,
####    [82], "years")
####potentiallyArableLandTotal = Parameter(
####    159, "potentiallyArableLandTotal", 3.2e9,
####    [84,97], "hectares")
####landFractionHarvested = Parameter(
####    160, "landFractionHarvested", 0.7,
####    [87])
####foodProcessingLoss = Parameter(
####    161, "foodProcessingLoss", 0.1,
####    [87])
####averageLifetimeOfAgriculturalInputs = Parameter(
####    162, "averageLifetimeOfAgriculturalInputs", 2,
####    [99,100], "years")
####industrialOutputIn1970 = Parameter(
####    163, "industrialOutputIn1970", 7.9e11,
####    [105], "dollars")
####marginalProductivityOfLandSocialDiscount = Parameter(
####    164, "marginalProductivityOfLandSocialDiscount", 0.07,
####    [109])
####inherentLandFertility = Parameter(
####    165, "inherentLandFertility", 600,
####    [113,124], "kilograms / hectare / year")
####landRemovalForUrbanIndustrialUseDevelopmentTime = Parameter(
####    166, "landRemovalForUrbanIndustrialUseDevelopmentTime", 10,
####    [119], "years")
####foodShortagePerceptionDelay = Parameter(
####    167, "foodShortagePerceptionDelay", 2,
####    [128], "kilograms / hectare / year")
####nonrenewableResourcesInitial = Parameter(
####    168, "nonrenewableResourcesInitial", 1.0e12,
####    [129, 133], "resource units")
####persistentPollutionTransmissionDelay = Parameter(
####    169, "persistentPollutionTransmissionDelay", 20,
####    [141], "years")
####persistentPollutionIn1970 = Parameter(
####    170, "persistentPollutionIn1970", 1.36e8,
####    [143], "pollution units")
##
##
####foodPerCapita = Parameter(
####    171, "foodPerCapita", 800,
####    [143], "kg / person / year")
####
####serviceOutputPerCapita = Parameter(
####    172, "serviceOutputPerCapita", 100,
####    [143], "dollars")
####
####indexOfPersistentPollution = Parameter(
####    173, "indexOfPersistentPollution", 1,
####    [143], "years")
####
###industrialOutputPerCapita = Parameter(
###   174, "industrialOutputPerCapita", 100,
###   [143], "years")
##
####f171 = Parameter(
####    171, "population0To14", 1e6,
####    [143], "persons")
####f172 = Parameter(
####    172, "population15To44", 1e6,
####    [143], "persons")
####f173 = Parameter(
####    173, "population45To64", 1e6,
####    [143], "persons")
####f174 = Parameter(
####    174, "population65AndOver", 1e6,
####    [143], "persons")
####
####DYNAMO_Engine.SortByType()
####DYNAMO_Engine.Produce_Solution_Path( verbose = True)
####DYNAMO_Engine.Reset( dt=5, global_stability_year=2050, verbose = False)
####DYNAMO_Engine.Warmup( verbose = False)
####DYNAMO_Engine.Compute( verbose = False)
##
###print(len(DYNAMO_Engine.Model_Time))
###print(len(population.Data))
###print(len(population0To14.Data))
###for i in range(50, len(DYNAMO_Engine.Model_Time)):
###    print( DYNAMO_Engine.Model_Time[i], population.Data[i])
##
###PlotVariable( f001, DYNAMO_Engine.Model_Time, show=True)
###PlotVariable( totalFertility, DYNAMO_Engine.Model_Time, show=True)
###PlotVariable( desiredTotalFertility, DYNAMO_Engine.Model_Time, show=True)
##
####computationSequence = [
####    "population",
####    "deathsPerYear",
####    "lifetimeMultiplierFromCrowding",
####    "industrialCapitalOutputRatio",
####    "averageLifetimeOfIndustrialCapital",
####    "averageLifetimeOfServiceCapital",
####    "serviceCapitalOutputRatio",
####    "laborForce",
####    "landFractionCultivated",
####    "developmentCostPerHectare",
####    "landYieldFactor",
####    "nonrenewableResourceUsageFactor",
####    "nonrenewableResourceFractionRemaining",
####    "persistentPollutionGenerationFactor",
####    "indexOfPersistentPollution",
####    "fractionOfIndustrialOutputAllocatedToConsumptionConstant",
####    "averageLifetimeOfAgriculturalInputs",
####    "laborUtilizationFractionDelayed",
####    "agriculturalInputs",
####    "perceivedFoodRatio",
####    "fractionOfPopulationUrban",
####    "crudeDeathRate",
####    "crudeBirthRate",
####    "fractionOfCapitalAllocatedToObtainingResources",
####    "lifetimeMultiplierFromPollution",
####    "landFertilityDegradationRate",
####    "capitalUtilizationFraction",
####    "industrialOutput",
####    "industrialOutputPerCapita",
####    "delayedIndustrialOutputPerCapita",
####    "socialFamilySizeNorm",
####    "averageIndustrialOutputPerCapita",
####    "familyIncomeExpectation",
####    "familyResponseToSocialNorm",
####    "desiredCompletedFamilySize",
####    "crowdingMultiplierFromIndustrialization",
####    "indicatedServiceOutputPerCapita",
####    "fractionOfIndustrialOutputAllocatedToConsumptionVariable",
####    "fractionOfIndustrialOutputAllocatedToConsumption",
####    "jobsPerIndustrialCapitalUnit",
####    "potentialJobsInIndustrialSector",
####    "serviceOutput",
####    "serviceOutputPerCapita",
####    "fractionOfIndustrialOutputAllocatedToServices",
####    "jobsPerServiceCapitalUnit",
####    "potentialJobsInServiceSector",
####    "healthServicesAllocationsPerCapita",
####    "effectiveHealthServicesPerCapita",
####    "lifetimeMultiplierFromHealthServices",
####    "fractionOfInputsAllocatedToLandMaintenance",
####    "agriculturalInputsPerHectare",
####    "jobsPerHectare",
####    "potentialJobsInAgriculturalSector",
####    "jobs",
####    "laborUtilizationFraction",
####    "landYieldMultiplierFromCapital",
####    "landYieldMultiplierFromAirPollution",
####    "landYield",
####    "marginalProductivityOfLandDevelopment",
####    "marginalLandYieldMultiplierFromCapital",
####    "marginalProductivityOfAgriculturalInputs",
####    "fractionOfInputsAllocatedToLandDevelopment",
####    "food",
####    "foodPerCapita",
####    "indicatedFoodPerCapita",
####    "fractionOfIndustrialOutputAllocatedToAgriculture",
####    "totalAgriculturalInvestment",
####    "currentAgriculturalInputs",
####    "foodRatio",
####    "landFertilityRegenerationTime",
####    "lifetimeMultiplierFromFood",
####    "lifeExpectancy",
####    "mortality0To14",
####    "mortality15To44",
####    "mortality45To64",
####    "mortality65AndOver",
####    "fecundityMultiplier",
####    "perceivedLifeExpectancy",
####    "compensatoryMultiplierFromPerceivedLifeExpectancy",
####    "maxTotalFertility",
####    "desiredTotalFertility",
####    "needForFertilityControl",
####    "fractionOfServicesAllocatedToFertilityControl",
####    "fertilityControlAllocationPerCapita",
####    "fertilityControlFacilitiesPerCapita",
####    "fertilityControlEffectiveness",
####    "totalFertility",
####    "landLifeMultiplierFromYield",
####    "averageLifeOfLand",
####    "urbanIndustrialLandPerCapita",
####    "urbanIndustrialLandRequired",
####    "perCapitaResourceUsageMultiplier",
####    "persistentPollutionGeneratedByIndustrialOutput",
####    "persistentPollutionGeneratedByAgriculturalOutput",
####    "assimilationHalfLife",
####    "fractionOfIndustrialOutputAllocatedToIndustry",
####    "fractionOfOutputInAgriculture",
####    "fractionOfOutputInIndustry",
####    "fractionOfOutputInServices"]
####
####
####Not_Found = []
####for s in computationSequence:
####    if DYNAMO_Engine.byName(s) is not None: continue
####    Not_Found += [s]
####if len(Not_Found) > 0:
####    print()
####    print( "Not found:")
####for s in Not_Found: print( s)
##
