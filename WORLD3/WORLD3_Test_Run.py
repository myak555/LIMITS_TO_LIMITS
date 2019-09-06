from WORLD3_Equations import *

computationSequence = [
    "population",
    "deathsPerYear",
    "lifetimeMultiplierFromCrowding",
    "industrialCapitalOutputRatio",
    "averageLifetimeOfIndustrialCapital",
    "averageLifetimeOfServiceCapital",
    "serviceCapitalOutputRatio",
    "laborForce",
    "landFractionCultivated",
    "developmentCostPerHectare",
    "landYieldFactor",
    "nonrenewableResourceUsageFactor",
    "nonrenewableResourceFractionRemaining",
    "persistentPollutionGenerationFactor",
    "indexOfPersistentPollution",
    "fractionOfIndustrialOutputAllocatedToConsumptionConstant",
    "averageLifetimeOfAgriculturalInputs",
    "laborUtilizationFractionDelayed",
    "agriculturalInputs",
    "perceivedFoodRatio",
    "fractionOfPopulationUrban",
    "crudeDeathRate",
    "crudeBirthRate",
    "fractionOfCapitalAllocatedToObtainingResources",
    "lifetimeMultiplierFromPollution",
    "landFertilityDegradationRate",
    "capitalUtilizationFraction",
    "industrialOutput",
    "industrialOutputPerCapita",
    "delayedIndustrialOutputPerCapita",
    "socialFamilySizeNorm",
    "averageIndustrialOutputPerCapita",
    "familyIncomeExpectation",
    "familyResponseToSocialNorm",
    "desiredCompletedFamilySize",
    "crowdingMultiplierFromIndustrialization",
    "indicatedServiceOutputPerCapita",
    "fractionOfIndustrialOutputAllocatedToConsumptionVariable",
    "fractionOfIndustrialOutputAllocatedToConsumption",
    "jobsPerIndustrialCapitalUnit",
    "potentialJobsInIndustrialSector",
    "serviceOutput",
    "serviceOutputPerCapita",
    "fractionOfIndustrialOutputAllocatedToServices",
    "jobsPerServiceCapitalUnit",
    "potentialJobsInServiceSector",
    "healthServicesAllocationsPerCapita",
    "effectiveHealthServicesPerCapita",
    "lifetimeMultiplierFromHealthServices",
    "fractionOfInputsAllocatedToLandMaintenance",
    "agriculturalInputsPerHectare",
    "jobsPerHectare",
    "potentialJobsInAgriculturalSector",
    "jobs",
    "laborUtilizationFraction",
    "landYieldMultiplierFromCapital",
    "landYieldMultiplierFromAirPollution",
    "landYield",
    "marginalProductivityOfLandDevelopment",
    "marginalLandYieldMultiplierFromCapital",
    "marginalProductivityOfAgriculturalInputs",
    "fractionOfInputsAllocatedToLandDevelopment",
    "food",
    "foodPerCapita",
    "indicatedFoodPerCapita",
    "fractionOfIndustrialOutputAllocatedToAgriculture",
    "totalAgriculturalInvestment",
    "currentAgriculturalInputs",
    "foodRatio",
    "landFertilityRegenerationTime",
    "lifetimeMultiplierFromFood",
    "lifeExpectancy",
    "mortality0To14",
    "mortality15To44",
    "mortality45To64",
    "mortality65AndOver",
    "fecundityMultiplier",
    "perceivedLifeExpectancy",
    "compensatoryMultiplierFromPerceivedLifeExpectancy",
    "maxTotalFertility",
    "desiredTotalFertility",
    "needForFertilityControl",
    "fractionOfServicesAllocatedToFertilityControl",
    "fertilityControlAllocationPerCapita",
    "fertilityControlFacilitiesPerCapita",
    "fertilityControlEffectiveness",
    "totalFertility",
    "landLifeMultiplierFromYield",
    "averageLifeOfLand",
    "urbanIndustrialLandPerCapita",
    "urbanIndustrialLandRequired",
    "perCapitaResourceUsageMultiplier",
    "persistentPollutionGeneratedByIndustrialOutput",
    "persistentPollutionGeneratedByAgriculturalOutput",
    "assimilationHalfLife",
    "fractionOfIndustrialOutputAllocatedToIndustry",
    "fractionOfOutputInAgriculture",
    "fractionOfOutputInIndustry",
    "fractionOfOutputInServices"]


Not_Found = []
for s in computationSequence:
    if s in DYNAMO_Function_Name_Dictionary: continue
    Not_Found += [s]
if len(Not_Found) > 0:
    print()
    print( "Not found:")
for s in Not_Found: print( s)

solved = []
for i, number in enumerate( DYNAMO_Level_Dictionary):
    eq = DYNAMO_Level_Dictionary[number]
    solved += [eq.Name]
print( "Levels: ", len(solved))

to_solve = len(DYNAMO_Aux_Name_Dictionary)
nsolved_prev = 0
for npass in range( 1, 101):
    print()
    print( "Pass: {:d}".format(npass))
    for i, name in enumerate( DYNAMO_Aux_Name_Dictionary):
        if name in solved: continue 
        eq = DYNAMO_Aux_Name_Dictionary[name]
        dependencies_resolved = True
        for dependence in eq.Dependencies:
            if dependence in solved: continue
            dependencies_resolved = False
            break
        if not dependencies_resolved: continue
        print( "   " + name )
        solved += [name]
    nsolved = len(solved)
    remains = to_solve - nsolved
    if remains <= 0:
        print( "   All {:d} solved".format(nsolved))
        break
    if nsolved == nsolved_prev:
        print( "Got stuck at {:d} equations".format( remains))
        break        
    print( "Solved {:d}, remains {:d}".format( nsolved, remains))
    nsolved_prev = nsolved 

if remains > 0:
    print( "Unresolved dependencies: ")
    for i, name in enumerate( DYNAMO_Aux_Name_Dictionary):
        if name in solved: continue 
        eq = DYNAMO_Aux_Name_Dictionary[name]
        print( eq.Number, eq.Name, eq.Dependencies)

print("Done!")
