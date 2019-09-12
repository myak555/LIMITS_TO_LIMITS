from WORLD3_Capital_Subsystem import *

#
# This run checks the population subsystem together with
# industry, services and labor parts of the capital subsystem.
# The agriculture outputs per capita
# are presumed constant (equations {83}-{143});
# Resources and polution are constant
#

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
LandFractionCultivated = AuxVariable(
    "_84_LandFractionCultivated",
    updatefn = lambda : _084.Kof("arableLand") / \
    _084.Kof("_159_PotentiallyArableLandTotal.K"))

_085 = LevelVariable(
    85, "arableLand", 0.9e9, "hectares",
    updatefn = lambda : _085.Jof("landDevelopmentRate") - \
    _085.Jof("landErosionRate") - \
    _085.Jof("landRemovalForUrbanIndustrialUse"))

_086 = LevelVariable(
    86, "potentiallyArableLand", 2.3e9, "hectares",
    updatefn = lambda : -_086.Jof("landDevelopmentRate"))

_087 = AuxVariable(
    87, "food", "kilograms / year",
    ["landYield"],
    lambda : _087.Kof("landYield") * _087.Kof("arableLand") * \
    _087.Kof("landFractionHarvested") * (1 - _087.Kof("foodProcessingLoss")))

_088 = AuxVariable(
    88, "foodPerCapita", "kilograms / person / year",
    ["food", "population"],
    lambda : _088.Kof("food") / _088.Kof("population"))

_089 = TableParametrization(
    89, "indicatedFoodPerCapita",
    [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    0, 1600, "kilograms / person / year",
    data_after_policy = [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    dependencies = ["industrialOutputPerCapita"])

#
# _090, _091 - used to be policy tables, now in {_089}
#

_092 = AuxVariable(
    92, "totalAgriculturalInvestment", "dollars / year",
    ["industrialOutput", "fractionOfIndustrialOutputAllocatedToAgriculture"],
    lambda : _092.Kof("industrialOutput") * _092.Kof("fractionOfIndustrialOutputAllocatedToAgriculture"))

_093 = TableParametrization(
    93, "fractionOfIndustrialOutputAllocatedToAgriculture",
    [0.4, 0.2, 0.1, 0.025, 0, 0], 0, 2.5,
    data_after_policy = [0.4, 0.2, 0.1, 0.025, 0, 0],
    dependencies = ["foodPerCapita", "indicatedFoodPerCapita"],
    updatefn = lambda : _093.Kof("foodPerCapita") / _093.Kof("indicatedFoodPerCapita"))

#
# _094, _095 - used to be policy tables, now in {_093}
#

_096 = RateVariable(
    96, "landDevelopmentRate", "hectares / year",
    lambda : _086.Kof("totalAgriculturalInvestment") * \
    _096.Kof("fractionOfInputsAllocatedToLandDevelopment") / \
    _096.Kof("developmentCostPerHectare"))

_097 = TableParametrization(
    97, "developmentCostPerHectare",
    [100000, 7400, 5200, 3500, 2400, 1500, 750, 300, 150, 75, 50],
    0, 1.0, "dollars / hectare",
    dependencies = ["potentiallyArableLand"]/
    normfn = lambda: _097.Kof("_159_PotentiallyArableLandTotal.K"))

#
# Loop 2: Food from Investment in Agricultural Inputs
#
_098 = AuxVariable(
    98, "currentAgriculturalInputs", "dollars / year",
    ["totalAgriculturalInvestment",
     "fractionOfInputsAllocatedToLandDevelopment"],
    lambda : _098.Kof("totalAgriculturalInvestment") * \
    (1 - _098.Kof("fractionOfInputsAllocatedToLandDevelopment")))

_099 = SmoothVariable(
    99, "agriculturalInputs",
    lambda: _099.Kof("averageLifetimeOfAgriculturalInputs"),
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
PotentiallyArableLandTotal = Parameter(
    "_159_PotentiallyArableLandTotal", 3.2e9, "hectares")
LandFractionHarvested = Parameter(
    "_160_LandFractionHarvested", 0.7)
FoodProcessingLoss = Parameter(
    "_161_FoodProcessingLoss", 0.1)
AverageLifetimeOfAgriculturalInputs = Parameter(
    "_162_AverageLifetimeOfAgriculturalInputs", 2, "years")
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

if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    ArableLand = Parameter(
        "_085_ArableLand", 0.9e9, "hectares")

    FoodPerCapita = PolicyParametrization(
        "_088_FoodPerCapita",
        800, 800, "kg / person / year")

    FractionOfIndustrialOutputAllocatedToAgriculture = PolicyParametrization(
        "_093_FractionOfIndustrialOutputAllocatedToAgriculture", 0.05, 0.1,
        "unitless")

    AgriculturalInputsPerHectare = PolicyParametrization(
        "_101_AgriculturalInputsPerHectare", 20, 20, "dollars / hectare / year")

    IndexOfPersistentPollution = Parameter(
        "_143_IndexOfPersistentPollution", 0.1)


    #
    # Parametrization plots
    #
    PlotTable( DYNAMO_Engine,
        FractionOfIndustrialOutputAllocatedToConsumptionVariable,
        0, 2.2, show=False)
    PlotTable( DYNAMO_Engine, IndicatedServiceOutputPerCapita,
        0, 1800, show=False)
    PlotTable( DYNAMO_Engine, FractionOfIndustrialOutputAllocatedToServices,
        0, 2.2, show=False)
    PlotTable( DYNAMO_Engine, JobsPerIndustrialCapitalUnit,
        0, 1000, show=False)
    PlotTable( DYNAMO_Engine, JobsPerServiceCapitalUnit,
        0, 1000, show=False)
    PlotTable( DYNAMO_Engine, JobsPerHectare,
        0, 40, show=False)
    PlotTable( DYNAMO_Engine, CapitalUtilizationFraction,               
        0, 12,
        "LaborUtilizationFractionDelayed [unitless]",
        show=False)
    PlotTable( DYNAMO_Engine, PerCapitaResourceUsageMultiplier,               
        0, 1700, show=False)
    PlotTable( DYNAMO_Engine, FractionOfCapitalAllocatedToObtainingResources,               
        0, 1.1, show=False)

    #
    #Test_Run
    #
    vrb = False
    DYNAMO_Engine.SortByType()
    if vrb: DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.Produce_Solution_Path( verbose = vrb)
    if vrb: DYNAMO_Engine.ListSolutionPath()
    DYNAMO_Engine.Reset(
        dt=2, global_policy_year=2020,
        global_stability_year=2070,
        verbose = vrb)
    DYNAMO_Engine.Warmup( verbose = vrb)
    DYNAMO_Engine.Compute( verbose = vrb)
#    PlotVariable( NonrenewableResources, DYNAMO_Engine.Model_Time,
#                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##    PlotVariable( CapitalUtilizationFraction, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

    Population.Data = np.array(Population.Data)
    Jobs.Data = np.array(Jobs.Data)
    LaborForce.Data = np.array(LaborForce.Data)
    IndustrialCapital.Data = np.array(IndustrialCapital.Data)
    ServiceCapital.Data = np.array(ServiceCapital.Data)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle('WORLD3 Test: Population and Capital Only', fontsize=25)
    gs = plt.GridSpec(2, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ax1.plot( DYNAMO_Engine.Model_Time,
              Population.Data/1e9, "-", lw=5, alpha=0.5, color="b")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Population.Data/1e9, "o", lw=1, color="k", label="Population Total")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Jobs.Data/1e9, "-", lw=2, color="g", label="Jobs")
    ax1.plot( DYNAMO_Engine.Model_Time,
              LaborForce.Data/1e9, "--", lw=2, color="r", label="Labor Force")
    ax1.plot( [2020, 2020], [0, 10], "--", lw=2, color="k", label="Global policy")
    ax1.plot( [2070, 2070], [0, 10], "-.", lw=2, color="k", label="Global stability")
    ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax1.set_ylim( 0, 12)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("billion")

    ax2.plot( DYNAMO_Engine.Model_Time, FractionOfCapitalAllocatedToObtainingResources.Data,
              "-", lw=3, color="r", label="For resources")
    ax2.plot( DYNAMO_Engine.Model_Time, FractionOfIndustrialOutputAllocatedToConsumption.Data,
              "-", lw=3, color="m", label="For consumption")
    ax2.plot( DYNAMO_Engine.Model_Time, FractionOfIndustrialOutputAllocatedToIndustry.Data,
              "--", lw=2, color="b", label="For industry")
    ax2.plot( DYNAMO_Engine.Model_Time, FractionOfIndustrialOutputAllocatedToServices.Data,
              "--", lw=2, color="y", label="For services")
    ax2.plot( DYNAMO_Engine.Model_Time, FractionOfIndustrialOutputAllocatedToAgriculture.Data,
              "--", lw=2, color="g", label="For agriculture")

#    ax2.plot( DYNAMO_Engine.Model_Time, IndustrialCapital.Data / 1e12,
#              "-", lw=2, color="b", label="Industrial Capital [$ x 1e12]")
#    ax2.plot( DYNAMO_Engine.Model_Time, ServiceCapital.Data / 1e12,
#              "-", lw=2, color="y", label="Service Capital [$ x 1e12]")
##    #ax2.plot( [2020, 2020], [0, 10000], "--", lw=2, color="k")
##    #ax2.plot( [2070, 2070], [0, 10000], "-.", lw=2, color="k")
    ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
##    #ax2.set_ylim( 0, 1000)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Units")
    
    plt.savefig( "./Graphs/Test_002_Capital.png")
    plt.show()
