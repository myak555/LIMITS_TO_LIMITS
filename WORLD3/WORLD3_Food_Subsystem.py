from WORLD3_Capital_Subsystem import *

#
# This run checks the entire system of WORLD3.
#

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

Food = AuxVariable(
    "_087_Food", "kilograms / year",
    fupdate = "_103_LandYield.K * _085_ArableLand.K"
    "* _160_LandFractionHarvested.K"
    "* (1 - _161_FoodProcessingLoss.K)")

FoodPerCapita = AuxVariable(
    "_088_FoodPerCapita", "kilograms / person / year",
    fupdate = "_087_Food.K / _001_Population.K")

IndicatedFoodPerCapita = TableParametrization(
    "_089_IndicatedFoodPerCapita",
    [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    0, 1600, "kilograms / person / year",
    fpoints_after_policy = [230, 480, 690, 850, 970, 1070, 1150, 1210, 1250],
    fupdate = "_049_IndustrialOutputPerCapita.K")

#
# agr_090, agr_091 - used to be policy tables, now in {089}
#

TotalAgriculturalInvestment = AuxVariable(
    "_092_TotalAgriculturalInvestment", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _093_FractionOfIndustrialOutputAllocatedToAgriculture.K")

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


if __name__ == "__main__":

    #
    # PARAMETERS
    #
    SubsistenceFoodPerCapita = Parameter(
        "_151_SubsistenceFoodPerCapita",
        230, "kilograms / person / year")

    EffectiveHealthServicesPerCapitaImpactDelay = Parameter(
        "_152_EffectiveHealthServicesPerCapitaImpactDelay",
        20, "years")

    LifetimePerceptionDelay = Parameter(
        "_153_LifetimePerceptionDelay",
        20, "years")

    SocialAdjustmentDelay = Parameter(
        "_154_SocialAdjustmentDelay",
        20, "years")

    IncomeExpectationAveragingTime = Parameter(
        "_155_IncomeExpectationAveragingTime",
        3, "years")

    HealthServicesImpactDelay = Parameter(
        "_156_HealthServicesImpactDelay",
        20, "years")

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


    #
    # NUMERICAL CHECKS (this test only)
    #
    #FoodPerCapita = AuxVariable(
    #    "_088_FoodPerCapita", "kg / person / year",
    #    fupdate = "_688_FoodPerCapita_Digitized.K * 10")
    #FoodPerCapita = PolicyParametrization(
    #    "_088_FoodPerCapita",
    #    900, 900, "kg / person / year")
    #ArableLand = Parameter(
    #    "_085_ArableLand", 0.9e9, "hectares")
    #FractionOfIndustrialOutputAllocatedToAgriculture = PolicyParametrization(
    #    "_093_FractionOfIndustrialOutputAllocatedToAgriculture", 0.05, 0.1,
    #    "unitless")
    #AgriculturalInputsPerHectare = PolicyParametrization(
    #    "_101_AgriculturalInputsPerHectare", 200, 200, "dollars / hectare / year")

    IndexOfPersistentPollution = AuxVariable(
        "_143_IndexOfPersistentPollution", "unitless",
        fupdate = "_743_PollutionIndex_Digitized.K * 0.32")

    #IndexOfPersistentPollution = Parameter(
    #    "_143_IndexOfPersistentPollution", 1)


    Population_Reference = AuxVariable(
        "_501_Population_Reference", "persons",
        fupdate = "_601_Population_Digitized.K * 1.6e8")

    LifeExpectancy_Reference = AuxVariable(
        "_519_LifeExpectancy_Reference", "persons",
        fupdate = "_619_LifeExpectancy_Digitized.K * 0.8")

    IndustrialOutputPerCapita_Reference = AuxVariable(
        "_549_IndustrialOutputPerCapita_Reference", "dollars / person / year",
        fupdate = "_649_Goods_Digitized.K * 5")

    ServiceOutputPerCapita_Reference = AuxVariable(
        "_571_ServiceOutputPerCapita", "dollars / person / year",
        fupdate = "_671_Services_Digitized.K * 1e11 / _001_Population.K")

    FoodPerCapita_Reference = AuxVariable(
        "_588_FoodPerCapita", "kg / person / year",
        fupdate = "_688_FoodPerCapita_Digitized.K * 10")

    #IndustrialOutput_Reference = AuxVariable(
    #    "_849_IndustrialOutput_Reference", "dollars / year",
    #    fupdate = "_049_IndustrialOutputPerCapita.K * _001_Population.K")

    #ServiceOutput_Reference = AuxVariable(
    #    "_870_ServiceOutput_Reference", "dollars / year",
    #    fupdate = "_671_Services_Digitized.K * 1e11")

    NonrenewableResources_Reference = AuxVariable(
        "_629_NonrenewableResources_Reference", "resource units",
        fupdate = "_729_Resources_Digitized.K * 1e10")


    Population_Digitized = TableParametrization(
        "_601_Population_Digitized",
        [10.428, 10.963, 11.530, 12.032, 12.834,
        13.636, 14.439, 15.241, 16.364, 17.647,
        18.984, 20.588, 22.460, 24.332, 26.471,
        28.610, 31.016, 33.690, 36.631, 39.305,
        42.246, 45.187, 48.128, 51.070, 53.743,
        55.882, 57.487, 58.021, 57.487, 56.150,
        53.476, 50.267, 47.594, 44.920, 42.513,
        40.107, 38.235, 36.265, 34.492, 33.155, 31.818],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    LifeExpectancy_Digitized = TableParametrization(
        "_619_LifeExpectancy_Digitized",
        [41.176,40.642,40.642,40.909,40.909,
        41.176,41.711,42.246,47.594,49.733,
        50.802,51.872,53.476,55.080,56.952,
        58.824,60.963,62.567,63.904,64.973,
        66.578,67.914,69.251,70.856,71.925,
        71.925,70.321,66.043,59.626,52.674,
        45.989,43.583,43.048,40.107,38.235,
        36.898,35.829,35.027,34.492,34.225,34.225],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    Goods_Digitized = TableParametrization(
        "_649_Goods_Digitized",
        [8.824,10.160,10.963,12.299,13.636,
        15.241,17.112,19.251,21.390,23.262,
        25.134,27.540,29.947,32.353,35.294,
        38.235,40.909,43.316,45.989,48.930,
        51.604,54.545,57.754,60.428,61.230,
        59.358,52.139,39.305,32.353,26.471,
        21.658,17.914,14.973,12.567,10.428,
         8.556, 7.219, 6.150, 5.080, 4.011, 3.209],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    Services_Digitized = TableParametrization(
        "_671_Services_Digitized",
        [1.604,1.604,1.872,2.139,2.406,
        2.674,3.209,3.476,4.011,4.813,
        5.615,6.417,7.487,8.824,10.428,
        12.032,13.904,16.310,18.984,21.925,
        24.866,28.342,32.086,36.631,40.107,
        42.781,43.583,40.107,34.759,29.679,
        24.332,20.856,16.845,13.904,11.497,
        9.358,7.754,6.684,5.615,4.545,3.743],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    FoodPerCapita_Digitized = TableParametrization(
        "_688_FoodPerCapita_Digitized",
        [28.877,27.807,28.075,28.877,29.412,
        30.214,31.283,32.086,33.690,33.957,
        35.294,35.829,37.433,38.503,39.305,
        39.572,39.840,39.840,39.840,40.107,
        40.107,40.107,40.107,39.840,39.037,
        37.701,35.294,29.679,25.668,21.658,
        20.321,20.053,20.588,19.786,19.519,
        18.717,18.984,19.251,19.519,19.786,20.053],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    Resources_Digitized = TableParametrization(
        "_729_Resources_Digitized",
        [100.267,100.267,100.000,99.733,99.465,
        99.198,98.930,98.396,97.861,97.326,
        96.524,95.722,94.652,93.583,92.246,
        90.374,88.503,86.364,83.422,79.947,
        75.936,71.390,65.508,58.824,51.872,
        44.652,37.166,32.086,28.877,26.203,
        23.797,22.193,21.123,20.053,18.717,
        18.182,17.914,17.380,17.112,16.845,15.775],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    PollutionIndex_Digitized = TableParametrization(
        "_743_PollutionIndex_Digitized",
        [0.802,0.802,0.802,0.802,0.802,
        0.802,1.070,1.070,1.337,1.337,
        1.872,1.872,2.406,2.674,3.209,
        3.743,4.545,5.348,6.417,7.754,
        9.358,10.963,13.369,16.310,19.786,
        23.529,28.342,32.888,35.829,36.364,
        34.225,30.214,25.668,21.123,16.845,
        13.102,10.160,8.021,6.417,4.813,3.743],
        1900, 2100,
        fupdate = "DYNAMO_Engine.time")

    #
    # Parametrization plots
    #
    PlotTable( DYNAMO_Engine, IndicatedFoodPerCapita,
        0, 1700, show=False)
    PlotTable( DYNAMO_Engine,
        FractionOfIndustrialOutputAllocatedToAgriculture,
        0, 1700, show=False)
    PlotTable( DYNAMO_Engine,
        DevelopmentCostPerHectare,
        0, 1.1, show=False)
    PlotTable( DYNAMO_Engine,
        LandYieldMultiplierFromCapital,
        0, 1100, show=False)
    PlotTable( DYNAMO_Engine,
        LandYieldMultiplierFromAirPollution,
        0, 40, show=False)
    PlotTable( DYNAMO_Engine,
        FractionOfInputsAllocatedToLandDevelopment,
        0, 2.2, show=False)
    PlotTable( DYNAMO_Engine,
        MarginalLandYieldMultiplierFromCapital,
        0, 700, show=False)
    PlotTable( DYNAMO_Engine,
        LandLifeMultiplierFromYield,
        0, 10, show=False)
    PlotTable( DYNAMO_Engine,
        UrbanIndustrialLandPerCapita,
        0, 40, show=False)
    PlotTable( DYNAMO_Engine,
        LandFertilityDegradationRate,
        0, 1700, show=False)
    PlotTable( DYNAMO_Engine,
        LandFertilityRegenerationTime,
        0, 0.1, show=False)
    PlotTable( DYNAMO_Engine,
        FractionOfInputsAllocatedToLandMaintenance,
        0, 5, show=False)

    #
    #Test_Run
    #
    vrb = False
    DYNAMO_Engine.SortByType()
    DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.ListDictionary( "levels")
    DYNAMO_Engine.Produce_Solution_Path( verbose = vrb)
    DYNAMO_Engine.ListSolutionPath()
    DYNAMO_Engine.Reset(
        dt=2, global_policy_year=2050,
        global_stability_year=4000,
        verbose = vrb)
    DYNAMO_Engine.Warmup( verbose = vrb)
    DYNAMO_Engine.Compute( verbose = vrb)
    PlotVariable( LandFertility, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
    PlotVariable( AverageLifeOfLand, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle('WORLD3 Test: Population, Capital, Land and Resources', fontsize=25)
    gs = plt.GridSpec(3, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    ax1.plot( DYNAMO_Engine.Model_Time,
              np.array(Population.Data)/1e9, "-", lw=6, alpha=0.5, color="b", label="Population total")
    ax1.plot( DYNAMO_Engine.Model_Time,
              np.array(Population_Reference.Data)/1e9, ".", lw=3, alpha=0.5, color="b", label="Population Check")
    ax1.plot( DYNAMO_Engine.Model_Time,
              np.array( LaborForce.Data)/1e9, "-", lw=3, alpha=0.5, color="g", label="Labor force")
    ax1.plot( DYNAMO_Engine.Model_Time,
              np.array( Jobs.Data)/1e9, "-", lw=3, alpha=0.5, color="r", label="Jobs")
    #ax1.plot( [2020, 2020], [0, 10], "--", lw=2, color="k", label="Global policy")
    #ax1.plot( [2070, 2070], [0, 10], "-.", lw=2, color="k", label="Global stability")
    ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax1.set_ylim( 0, 10)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("billion")

    ax2.plot( DYNAMO_Engine.Model_Time, IndustrialOutputPerCapita.Data,
              "-", lw=6, color="b", alpha=0.5, label="Goods per capita")
    ax2.plot( DYNAMO_Engine.Model_Time, IndustrialOutputPerCapita_Reference.Data,
              ".", lw=2, alpha=0.5, color="b")
    ax2.plot( DYNAMO_Engine.Model_Time, ServiceOutputPerCapita.Data,
              "-", lw=6, color="r", alpha=0.5, label="Services per capita")
    ax2.plot( DYNAMO_Engine.Model_Time, ServiceOutputPerCapita_Reference.Data,
              ".", lw=2, color="r", alpha=0.5)
    ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita.Data,
              "-", lw=6, color="g", alpha=0.5, label="Food per capita ($1/kg)")
    ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita_Reference.Data,
              ".", lw=2, color="g", alpha=0.5)
    #ax2.plot( [2020, 2020], [10, 50], "--", lw=2, color="k")
    #ax2.plot( [2070, 2070], [10, 50], "-.", lw=2, color="k")
    ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    #ax2.set_ylim( 0, 500)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_ylabel("$ / person / year")

    ax3.plot( DYNAMO_Engine.Model_Time, np.array( NonrenewableResources_Reference.Data) / 1e9,
              ".", lw=1, color="k", alpha=0.5, label="Nonrenewable Resources(check)")
    ax3.plot( DYNAMO_Engine.Model_Time, np.array( NonrenewableResources.Data) / 1e9,
              "-", lw=6, color="r", alpha=0.5, label="Nonrenewable Resources(check)")
    #ax3.plot( [2020, 2020], [10, 50], "--", lw=2, color="k")
    #ax3.plot( [2070, 2070], [10, 50], "-.", lw=2, color="k")
    ax3.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    #ax3.set_ylim( 0, 60)
    ax3.grid(True)
    ax3.legend(loc=0)
    ax3.set_xlabel("Year")
    ax3.set_ylabel("10^9 tonn")
    
    plt.savefig( "./Graphs/Test_003_Food.png")
    plt.show()

    #OutputCSV(
    #[IndustrialOutput_Reference, ServiceOutput_Reference],
    #DYNAMO_Engine.Model_Time,
    #"./Data/Output_Checks.csv")

