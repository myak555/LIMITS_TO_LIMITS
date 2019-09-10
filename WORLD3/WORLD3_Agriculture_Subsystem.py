from WORLD3_Labor_Subsystem import *

#
# This run checks the subsystems running together: 
#    - population,
#    - industry,
#    - services
#    - labor
#    - agriculture
# the polution and resources usage
# are presumed constant (equations {201}-{207})
#

#
# AGRICULTURE SUBSYSTEM
# (equations {84}-{89},{92},{93},{96}-{105},{108}-{113},{116}-{128})
#
# Loop 1: Food from Investment in Land Development
#
agr084 = AuxVariable(
    84, "landFractionCultivated",
    updatefn = lambda : agr084.Kof("arableLand") / \
    agr084.Kof("potentiallyArableLandTotal"))

agr085 = LevelVariable(
    85, "arableLand", 0.9e9, "hectares",
    updatefn = lambda : agr085.Jof("landDevelopmentRate") - \
    agr085.Jof("landErosionRate") - \
    agr085.Jof("landRemovalForUrbanIndustrialUse"))

agr086 = LevelVariable(
    86, "potentiallyArableLand", 2.3e9, "hectares",
    updatefn = lambda : -agr086.Jof("landDevelopmentRate"))

agr087 = AuxVariable(
    87, "food", "kilograms / year",
    ["landYield"],
    lambda : agr087.Kof("landYield") * agr087.Kof("arableLand") * \
    agr087.Kof("landFractionHarvested") * (1 - agr087.Kof("foodProcessingLoss")))

agr088 = AuxVariable(
    88, "foodPerCapita", "kilograms / person / year",
    ["food", "population"],
    lambda : agr088.Kof("food") / agr088.Kof("population"))

agr089 = TableParametrization(
    89, "indicatedFoodPerCapita",
    [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    0, 1600, "kilograms / person / year",
    data_after_policy = [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    dependencies = ["industrialOutputPerCapita"])

#
# agr090, agr091 - used to be policy tables, now in {agr089}
#

agr092 = AuxVariable(
    92, "totalAgriculturalInvestment", "dollars / year",
    ["industrialOutput", "fractionOfIndustrialOutputAllocatedToAgriculture"],
    lambda : agr092.Kof("industrialOutput") * agr092.Kof("fractionOfIndustrialOutputAllocatedToAgriculture"))

agr093 = TableParametrization(
    93, "fractionOfIndustrialOutputAllocatedToAgriculture",
    [0.4, 0.2, 0.1, 0.025, 0, 0], 0, 2.5,
    data_after_policy = [0.4, 0.2, 0.1, 0.025, 0, 0],
    dependencies = ["foodPerCapita", "indicatedFoodPerCapita"],
    updatefn = lambda : agr093.Kof("foodPerCapita") / agr093.Kof("indicatedFoodPerCapita"))

#
# agr094, agr095 - used to be policy tables, now in {agr093}
#

agr096 = RateVariable(
    96, "landDevelopmentRate", "hectares / year",
    lambda : agr086.Kof("totalAgriculturalInvestment") * \
    agr096.Kof("fractionOfInputsAllocatedToLandDevelopment") / \
    agr096.Kof("developmentCostPerHectare"))

agr097 = TableParametrization(
    97, "developmentCostPerHectare",
    [100000, 7400, 5200, 3500, 2400, 1500, 750, 300, 150, 75, 50],
    0, 1.0, "dollars / hectare",
    dependencies = ["potentiallyArableLand"],
    normfn = lambda: agr097.Kof("potentiallyArableLandTotal"))

#
# Loop 2: Food from Investment in Agricultural Inputs
#
agr098 = AuxVariable(
    98, "currentAgriculturalInputs", "dollars / year",
    ["totalAgriculturalInvestment",
     "fractionOfInputsAllocatedToLandDevelopment"],
    lambda : agr098.Kof("totalAgriculturalInvestment") * \
    (1 - agr098.Kof("fractionOfInputsAllocatedToLandDevelopment")))

agr099 = SmoothVariable(
    99, "agriculturalInputs",
    lambda: agr099.Kof("averageLifetimeOfAgriculturalInputs"),
    "dollars / year",
    ["currentAgriculturalInputs"],   # this will be replaced by value below to break a definition cycle
    initialValue = 5.0e9)

#
# output of this equation is unused (replaced with a constant 2)
#
agr100 = PolicyParametrization(
    100, "averageLifetimeOfAgriculturalInputs", 2, 2, "years")

agr101 = AuxVariable(
    101, "agriculturalInputsPerHectare", "dollars / hectare / year",
    ["agriculturalInputs", "fractionOfInputsAllocatedToLandMaintenance"],
    lambda : agr101.Kof("agriculturalInputs") * \
    (1 - agr101.Kof("fractionOfInputsAllocatedToLandMaintenance")) / agr101.Kof("arableLand"))

agr102 = TableParametrization(
    102, "landYieldMultiplierFromCapital",
    [1, 3, 3.8, 4.4, 4.9, 5.4, 5.7, 6, 6.3, 6.6, 6.9, 7.2, 7.4,
     7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 10],
    0, 1000, dependencies = ["agriculturalInputsPerHectare"])

agr103 = AuxVariable(
    103, "landYield", "kilograms / hectare / year",
    ["landYieldFactor", "landYieldMultiplierFromCapital",
     "landYieldMultiplierFromAirPollution"],
    lambda : agr103.Kof("landYieldFactor") * agr103.Kof("landFertility") * \
    agr103.Kof("landYieldMultiplierFromCapital") * agr103.Kof("landYieldMultiplierFromAirPollution"))

agr104 = PolicyParametrization(
    104, "landYieldFactor", 1, 1)

agr105 = TableParametrization(
    105, "landYieldMultiplierFromAirPollution",
    [1, 1, 0.7, 0.4], 0, 30,
    data_after_policy = [1, 1, 0.7, 0.4],
    dependencies = ["industrialOutput"],
    norm = agr105.Kof("industrialOutputIn1970"))
#
# agr106, agr107 - used to be policy tables, now in {agr105}
#

#
# Loops 1 and 2: The Investment Allocation Decision
#
agr108 = TableParametrization(
    108, "fractionOfInputsAllocatedToLandDevelopment",
    [0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.85, 0.95, 1], 0, 2,
    dependencies = ["marginalProductivityOfLandDevelopment",
                    "marginalProductivityOfAgriculturalInputs"],
    updatefn = lambda : \
        agr108.Kof("marginalProductivityOfLandDevelopment") / agr108.Kof("marginalProductivityOfAgriculturalInputs"))

agr109 = AuxVariable(
    109, "marginalProductivityOfLandDevelopment", "kilograms / dollar",
    ["landYield", "developmentCostPerHectare"],
    lambda : agr109.Kof("landYield") / agr109.Kof("developmentCostPerHectare") /\
    agr109.Kof("marginalProductivityOfLandSocialDiscount"))

agr110 = AuxVariable(
    110, "marginalProductivityOfAgriculturalInputs", "kilograms / dollar",
    ["averageLifetimeOfAgriculturalInputs", "landYield",
     "marginalLandYieldMultiplierFromCapital",
     "landYieldMultiplierFromCapital"],
    lambda : agr110.Kof("averageLifetimeOfAgriculturalInputs") * agr110.Kof("landYield") * \
    agr110.Kof("marginalLandYieldMultiplierFromCapital") / agr110.Kof("landYieldMultiplierFromCapital"))

agr111 = TableParametrization(
    111, "marginalLandYieldMultiplierFromCapital",
    [0.075, 0.03, 0.015, 0.011, 0.009, 0.008, 0.007, 0.006,
     0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005],
    0, 600, "hectares / dollar",
    dependencies = ["agriculturalInputsPerHectare"])

#
# Loop 3: Land Erosion and Urban-Industrial Use
#
agr112 = AuxVariable(
    112, "averageLifeOfLand", "years",
    ["landLifeMultiplierFromYield"],
    lambda : 6000 * agr112.Kof("landLifeMultiplierFromYield")) # presumed 6000 years

agr113 = TableParametrization(
    113, "landLifeMultiplierFromYield",
    [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01], 0, 9,
    data_after_policy = [1.2, 1, 0.63, 0.36, 0.16, 0.055, 0.04, 0.025, 0.015, 0.01],
    dependencies = ["landYield"],
    normfn = lambda: agr113.Kof("inherentLandFertility"))

#
# agr114, agr115 - used to be policy tables, now in {agr113}
#

agr116 = RateVariable(
    116, "landErosionRate", "hectares / year",
    lambda : agr116.Kof("arableLand") / agr116.Kof("averageLifeOfLand"))

agr117 = TableParametrization(
    117, "urbanIndustrialLandPerCapita",
    [0.005, 0.008, 0.015, 0.025, 0.04, 0.055, 0.07, 0.08, 0.09],
    0, 1600, "hectares / person",
    dependencies = ["industrialOutputPerCapita"])

agr118 = AuxVariable(
    118, "urbanIndustrialLandRequired", "hectares",
    ["urbanIndustrialLandPerCapita", "population"],
    lambda : agr118.Kof("urbanIndustrialLandPerCapita") * agr118.Kof("population"))

agr119 = RateVariable(
    119, "landRemovalForUrbanIndustrialUse", "hectares / year",
    lambda : max(0, 1))

#                 agr119.Kof("urbanIndustrialLandRequired") - \
#    agr119.Kof("urbanIndustrialLand")) / agr119.Kof("landRemovalForUrbanIndustrialUseDevelopmentTime")))

agr120 = LevelVariable(
    120, "urbanIndustrialLand", 8.2e6, "hectares",
    updatefn = lambda : agr120.Jof("landRemovalForUrbanIndustrialUse"))

#
# Loop 4: Land fertility degradation
#
agr121 = LevelVariable(
    121, "landFertility", 600, "kilograms / hectare / year",
    updatefn = lambda : agr121.Jof("landFertilityRegeneration") - agr121.Jof("landFertilityDegradation"))

agr122 = TableParametrization(
    122, "landFertilityDegradationRate",
    [0, 0.1, 0.3, 0.5], 0, 30, "1 / year",
    dependencies = ["indexOfPersistentPollution"])

agr123 = RateVariable(
    123, "landFertilityDegradation", "kilograms / hectare / year^2",
    lambda : agr123.Kof("landFertility") * agr123.Kof("landFertilityDegradationRate"))

#
# Loop 5: Land fertility regeneration
#
agr124 = RateVariable(
    124, "landFertilityRegeneration", "kilograms / hectare / year^2",
    lambda : (agr124.Kof("inherentLandFertility") - agr124.Kof("landFertility"))\
    / agr124.Kof("landFertilityRegenerationTime"))

agr125 = TableParametrization(
    125, "landFertilityRegenerationTime",
    [20, 13, 8, 4, 2, 2], 0, 0.1, "years",
    dependencies = ["fractionOfInputsAllocatedToLandMaintenance"])

#
# Loop 6: Discontinuing land maintenance
#
agr126 = TableParametrization(
    126, "fractionOfInputsAllocatedToLandMaintenance",
    [0, 0.04, 0.07, 0.09, 0.10], 0, 4,
    dependencies = ["perceivedFoodRatio"])

agr127 = AuxVariable(
    127, "foodRatio",
    dependencies = ["foodPerCapita"],
    updatefn = lambda : agr127.Kof("foodPerCapita") / agr127.Kof("subsistenceFoodPerCapita"))

agr128 = SmoothVariable(
    128, "perceivedFoodRatio",
    agr128.Kof("foodShortagePerceptionDelay"),
    dependencies = ["foodRatio"],   # this will be replaced by value below to break a definition cycle
    initialValue = 1.0)

#
# PARAMETERS
#
par159 = Parameter(
    159, "potentiallyArableLandTotal", 3.2e9,
    [84,97], "hectares")
par160 = Parameter(
    160, "landFractionHarvested", 0.7,
    [87])
par161 = Parameter(
    161, "foodProcessingLoss", 0.1,
    [87])
par162 = Parameter(
    162, "averageLifetimeOfAgriculturalInputs", 2,
    [99,100], "years")
par163 = Parameter(
    163, "industrialOutputIn1970", 7.9e11,
    [105], "dollars")
par164 = Parameter(
    164, "marginalProductivityOfLandSocialDiscount", 0.07,
    [109])
par165 = Parameter(
    165, "inherentLandFertility", 600,
    [113,124], "kilograms / hectare / year")
par166 = Parameter(
    166, "landRemovalForUrbanIndustrialUseDevelopmentTime", 10,
    [119], "years")
par167 = Parameter(
    167, "foodShortagePerceptionDelay", 2,
    [128], "kilograms / hectare / year")


if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    par203 = Parameter(
        203, "indexOfPersistentPollution", 1,
        [])

    par204 = PolicyParametrization(
        204, "fractionOfCapitalAllocatedToObtainingResources", 0.10, 0.10,
        "unitless")

    #
    #Test_Run
    #
    DYNAMO_Engine.SortByType()
    DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.Produce_Solution_Path( verbose = True)
    DYNAMO_Engine.ListSolutionPath()
#    DYNAMO_Engine.Reset(
#        dt=5, global_policy_year=2020,
#        global_stability_year=2050,
#        verbose = True)
#    DYNAMO_Engine.Warmup( verbose = True)
#    DYNAMO_Engine.Compute( verbose = True)
#    PlotVariable( "population", DYNAMO_Engine.Model_Time,
#                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

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
