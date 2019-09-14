from DYNAMO_Prototypes import *

#
# This run checks only the population subsystem,
# presuming the industry, agriculture and services
# outputs per capita to be hard-coded inputs
# (tables instead of equations {049}-{143})
#


#
# POPULATION SUBSYSTEM (equations {1}-{23}, {26}-{48})
#
Population = AuxVariable(
    "_001_Population", "persons",
    fupdate = "_002_Population0To14.K + _006_Population15To44.K"
    "+ _010_Population45To64.K + _014_Population65AndOver.K")

Population0To14 = LevelVariable(
    "_002_Population0To14", "6.5e8", "persons",
    fupdate = "_030_BirthsPerYear.J - _003_DeathsPerYear0To14.J"
    "- _005_MaturationsPerYear14to15.J")

DeathsPerYear0To14 = RateVariable(
    "_003_DeathsPerYear0To14", "persons / year",
    fupdate = "_002_Population0To14.K * _004_Mortality0To14.K")

Mortality0To14 = TableParametrization(
    "_004_Mortality0To14",
    [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")

MaturationsPerYear14to15 = RateVariable(
    "_005_MaturationsPerYear14to15", "persons / year",
    fupdate = "_002_Population0To14.K * (1 - _004_Mortality0To14.K) / 15.0")

Population15To44 = LevelVariable(
    "_006_Population15To44", "7.0e8", "persons",
    fupdate = "_005_MaturationsPerYear14to15.J - _007_DeathsPerYear15To44.J"
    "- _009_MaturationsPerYear44to45.J")

DeathsPerYear15To44 = RateVariable(
    "_007_DeathsPerYear15To44", "persons / year",
    fupdate = "_006_Population15To44.K * _008_Mortality15To44.K")

Mortality15To44 = TableParametrization(
    "_008_Mortality15To44",
    [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")

MaturationsPerYear44to45 = RateVariable(
    "_009_MaturationsPerYear44to45", "persons / year",
    fupdate = "_006_Population15To44.K * (1 - _008_Mortality15To44.K) / 30.0")

Population45To64 = LevelVariable(
    "_010_Population45To64", "1.9e8", "persons",
    fupdate = "_009_MaturationsPerYear44to45.J - _011_DeathsPerYear45To64.J"
    "- _013_MaturationsPerYear64to65.J")

DeathsPerYear45To64 = RateVariable(
    "_011_DeathsPerYear45To64", "persons / year",
    fupdate = "_010_Population45To64.K * _012_Mortality45To64.K")

Mortality45To64 = TableParametrization(
    "_012_Mortality45To64",
    [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")

MaturationsPerYear64to65 = RateVariable(
    "_013_MaturationsPerYear64to65", "persons / year",
    fupdate = "_010_Population45To64.K * (1 - _012_Mortality45To64.K) / 20.0")

Population65AndOver = LevelVariable(
    "_014_Population65AndOver", "6.0e7", "persons",
    fupdate = "_013_MaturationsPerYear64to65.J - _015_DeathsPerYear65AndOver.J")

DeathsPerYear65AndOver = RateVariable(
    "_015_DeathsPerYear65AndOver", "persons / year",
    fupdate = "_014_Population65AndOver.K * _016_Mortality65AndOver.K")

Mortality65AndOver = TableParametrization(
    "_016_Mortality65AndOver",
    [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")

DeathsPerYear = AuxVariable(
    "_017_DeathsPerYear", "persons / year",
    fupdate = "_003_DeathsPerYear0To14.J  + _007_DeathsPerYear15To44.J"
    "+ _011_DeathsPerYear45To64.J + _015_DeathsPerYear65AndOver.J")

CrudeDeathRate = AuxVariable(
    "_018_CrudeDeathRate", "deaths / 1000 persons / year",
    fupdate = "1000 * _017_DeathsPerYear.K / _001_Population.K")

LifeExpectancy = AuxVariable(
    "_019_LifeExpectancy", "years",
    fupdate = "32 * _020_LifetimeMultiplierFromFood.K"
    "* _023_LifetimeMultiplierFromHealthServices.K"
    "* _028_LifetimeMultiplierFromCrowding.K"
    "* _029_LifetimeMultiplierFromPollution.K")

LifetimeMultiplierFromFood = TableParametrization(
    "_020_LifetimeMultiplierFromFood",
    [0, 1, 1.2, 1.3, 1.35, 1.4], 0, 5,
    fupdate = "_088_FoodPerCapita.K / _151_SubsistenceFoodPerCapita.K")

HealthServicesAllocationsPerCapita = TableParametrization(
    "_021_HealthServicesAllocationsPerCapita",
    [0, 20, 50, 95, 140, 175, 200, 220, 230], 0, 2000,
    "dollars / person / year",
    fupdate = "_071_ServiceOutputPerCapita.K")

EffectiveHealthServicesPerCapita = SmoothVariable(
    "_022_EffectiveHealthServicesPerCapita",
    "_152_EffectiveHealthServicesPerCapitaImpactDelay.K",
    "dollars / person / year",
    "_021_HealthServicesAllocationsPerCapita.K")

LifetimeMultiplierFromHealthServices = TableParametrization(
    "_023_LifetimeMultiplierFromHealthServices",
    [1, 1.4, 1.6, 1.8, 1.95, 2.0], 0, 100,
    fpoints_1940 = [1, 1.1, 1.4, 1.6, 1.7, 1.8],
    fupdate = "_022_EffectiveHealthServicesPerCapita.K")

#
# pop024, pop025 - used to be policy tables, now in {pop023}
#

FractionOfPopulationUrban = TableParametrization(
    "_026_FractionOfPopulationUrban",
    [0, 0.2, 0.4, 0.5, 0.58, 0.65, 0.72, 0.78, 0.80], 0, 16e9,
    fupdate = "_001_Population.K")

CrowdingMultiplierFromIndustrialization = TableParametrization(
    "_027_CrowdingMultiplierFromIndustrialization",
    [0.5, 0.05, -0.1, -0.08, -0.02, 0.05, 0.1, 0.15, 0.2], 0, 1600,
    fupdate = "_049_IndustrialOutputPerCapita.K")

LifetimeMultiplierFromCrowding = AuxVariable(
    "_028_LifetimeMultiplierFromCrowding",
    fupdate = "1 - _027_CrowdingMultiplierFromIndustrialization.K"
    "* _026_FractionOfPopulationUrban.K") 

LifetimeMultiplierFromPollution = TableParametrization(
    "_029_LifetimeMultiplierFromPollution",
    [1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.75, 0.65, 0.55, 0.40, 0.20],
    0, 100,
    fupdate = "_143_IndexOfPersistentPollution.K")

BirthsPerYear = RateVariable(
    "_030_BirthsPerYear", "persons / year",
    fupdate = "_032_TotalFertility.K * _006_Population15To44.K * 0.5 / 30.0",
    fequilibrium = "_017_DeathsPerYear.K")

CrudeBirthRate = AuxVariable(
    "_031_CrudeBirthRate", "births / 1000 persons / year",
    fupdate = "1000 * _030_BirthsPerYear.J / _001_Population.K")

TotalFertility = AuxVariable(
    "_032_TotalFertility",
    fupdate = "min( _033_MaxTotalFertility.K,"
    "_033_MaxTotalFertility.K * (1 - _045_FertilityControlEffectiveness.K)"
    "+ _035_DesiredTotalFertility.K * _045_FertilityControlEffectiveness.K)")

MaxTotalFertility = AuxVariable(
    "_033_MaxTotalFertility",
    fupdate = "12 * _034_FecundityMultiplier.K")
    # 12 - max number of births

FecundityMultiplier = TableParametrization(
    "_034_FecundityMultiplier",
    [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.05, 1.1], 0, 80,
    fupdate = "_019_LifeExpectancy.K")

DesiredTotalFertility = AuxVariable(
    "_035_DesiredTotalFertility",
    fupdate = "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy.K"
    "* _038_DesiredCompletedFamilySize.K")

CompensatoryMultiplierFromPerceivedLifeExpectancy = TableParametrization(
     "_036_CompensatoryMultiplierFromPerceivedLifeExpectancy",
    [3.0, 2.1, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0], 0, 80,
    fupdate = "_037_PerceivedLifeExpectancy.K")

PerceivedLifeExpectancy = DelayVariable(
    "_037_PerceivedLifeExpectancy",
    "_153_LifetimePerceptionDelay.K", "years",
    "_019_LifeExpectancy.K")

DesiredCompletedFamilySize = AuxVariable(
    "_038_DesiredCompletedFamilySize", "persons",
    fupdate = "4.0 * _039_SocialFamilySizeNorm.K"
    "* _041_FamilyResponseToSocialNorm.K",
    fequilibrium = "2.0")

SocialFamilySizeNorm = TableParametrization(
    "_039_SocialFamilySizeNorm",
    [1.25, 1, 0.9, 0.8, 0.75], 0, 800,
    fupdate = "_040_DelayedIndustrialOutputPerCapita.K")

DelayedIndustrialOutputPerCapita = DelayVariable(
    "_040_DelayedIndustrialOutputPerCapita",
    "_154_SocialAdjustmentDelay.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

FamilyResponseToSocialNorm = TableParametrization(
    "_041_FamilyResponseToSocialNorm",
    [0.5, 0.6, 0.7, 0.85, 1.0], -0.2, 0.2,
    fupdate = "_042_FamilyIncomeExpectation.K")

FamilyIncomeExpectation = AuxVariable(
    "_042_FamilyIncomeExpectation",
    fupdate = "_049_IndustrialOutputPerCapita.K"
    "/ _043_AverageIndustrialOutputPerCapita.K - 1")

AverageIndustrialOutputPerCapita = SmoothVariable(
    "_043_AverageIndustrialOutputPerCapita",
    "_155_IncomeExpectationAveragingTime.K",
    "dollars / person / year",
    "_049_IndustrialOutputPerCapita.K")

NeedForFertilityControl = AuxVariable(
    "_044_NeedForFertilityControl",
    fupdate = "_033_MaxTotalFertility.K"
    "/ _035_DesiredTotalFertility.K - 1")

FertilityControlEffectiveness = TableParametrization(
    "_045_FertilityControlEffectiveness",
    [0.75, 0.85, 0.90, 0.95, 0.98, 0.99, 1.0], 0, 3,
    fupdate = "_046_FertilityControlFacilitiesPerCapita.K")

FertilityControlFacilitiesPerCapita = DelayVariable(
    "_046_FertilityControlFacilitiesPerCapita",
    "_156_HealthServicesImpactDelay.K",
    "dollars / person / year",
    "_047_FertilityControlAllocationPerCapita.K")

FertilityControlAllocationPerCapita = AuxVariable(
    "_047_FertilityControlAllocationPerCapita",
    "dollars / person / year",
    fupdate = "_048_FractionOfServicesAllocatedToFertilityControl.K"
    "* _071_ServiceOutputPerCapita.K")

FractionOfServicesAllocatedToFertilityControl = TableParametrization(
    "_048_FractionOfServicesAllocatedToFertilityControl",
    [0.0, 0.005, 0.015, 0.025, 0.030, 0.035], 0, 10,
    fupdate = "_044_NeedForFertilityControl.K")

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


    #
    # NUMERICAL CHECKS (this test only)
    #
    IndustrialOutputPerCapita = AuxVariable(
        "_049_IndustrialOutputPerCapita", "dollars / person / year",
        fupdate = "_649_Goods_Digitized.K * 5")

    #IndustrialOutputPerCapita = Parameter(
    #    "_049_IndustrialOutputPerCapita",
    #    200, "dollars / person / year")

    ServiceOutputPerCapita = AuxVariable(
        "_071_ServiceOutputPerCapita", "dollars / person / year",
        fupdate = "_671_Services_Digitized.K * 1e11 / _001_Population.K")

    #ServiceOutputPerCapita = Parameter(
    #    "_071_ServiceOutputPerCapita",
    #    50, "dollars")

    FoodPerCapita = AuxVariable(
        "_088_FoodPerCapita", "kg / person / year",
        fupdate = "_688_FoodPerCapita_Digitized.K * 10")

    #FoodPerCapita = PolicyParametrization(
    #    "_088_FoodPerCapita",
    #    900, 900, "kg / person / year")

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
    PlotTable( DYNAMO_Engine, Mortality0To14, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality15To44, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality45To64, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality65AndOver, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, HealthServicesAllocationsPerCapita, 0, 2200,
               "ServiceOutputPerCapita [dollars / person / year]", show=False)
    PlotTable( DYNAMO_Engine, LifetimeMultiplierFromFood, 0, 6,
               "FoodPerCapita [fraction of subsistence]", show=False)
    PlotTable( DYNAMO_Engine, LifetimeMultiplierFromHealthServices, 0, 120, show=False)
    PlotTable( DYNAMO_Engine, FractionOfPopulationUrban, 0, 18e9, show=False)
    PlotTable( DYNAMO_Engine, CrowdingMultiplierFromIndustrialization, 0, 1800,
              "IndustrialOutputPerCapita [dollars / person / year]", show=False)
    PlotTable( DYNAMO_Engine, LifetimeMultiplierFromPollution, 0, 120,
              "IndexOfPersistentPollution [unitless]", show=False)
    PlotTable( DYNAMO_Engine, FecundityMultiplier, 0, 100, show=False)
    PlotTable( DYNAMO_Engine,
               CompensatoryMultiplierFromPerceivedLifeExpectancy, 0, 100,
               "PerceivedLifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, SocialFamilySizeNorm, 0, 1000,
               "DelayedIndustrialOutputPerCapita [dollars / person / year]", show=False)
    PlotTable( DYNAMO_Engine, FamilyResponseToSocialNorm, -0.25, 0.25,
               "FamilyIncomeExpectation [unitless]", show=False)
    PlotTable( DYNAMO_Engine, FertilityControlEffectiveness, 0, 4,
               "FertilityControlFacilitiesPerCapita [dollars / person / year]", show=False)
    PlotTable( DYNAMO_Engine, FractionOfServicesAllocatedToFertilityControl,
               0, 11, show=False)


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
        dt=0.5, global_policy_year=2050,
        global_stability_year=4000,
        verbose = vrb)
    DYNAMO_Engine.Warmup( verbose = vrb)
    DYNAMO_Engine.Compute( verbose = vrb)
    #PlotVariable( FertilityControlAllocationPerCapita, DYNAMO_Engine.Model_Time,
    #              filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
    #PlotVariable( FertilityControlFacilitiesPerCapita, DYNAMO_Engine.Model_Time,
    #              filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

    Population.Data = np.array(Population.Data)
    Population0To14.Data = np.array(Population0To14.Data)
    Population15To44.Data = np.array(Population15To44.Data)
    Population45To64.Data = np.array(Population45To64.Data)
    Population_Reference.Data = np.array(Population_Reference.Data)
    FoodPerCapita.Data = np.array(FoodPerCapita.Data)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle('WORLD3 Test: Population Only', fontsize=25)
    gs = plt.GridSpec(3, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    ax1.plot( DYNAMO_Engine.Model_Time,
              Population.Data/1e9, "-", lw=6, alpha=0.5, color="b", label="Population total")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Population_Reference.Data/1e9, ".", lw=1, alpha=0.5, color="k", label="Population (check)")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Population0To14.Data/1e9, "-", lw=2, color="g", label="0-14 y.o.")
    ax1.plot( DYNAMO_Engine.Model_Time,
              (Population0To14.Data + Population15To44.Data)/1e9, "-", lw=2, color="r", label="15-14 y.o.")
    ax1.plot( DYNAMO_Engine.Model_Time,
              (Population0To14.Data + Population15To44.Data + Population45To64.Data)/1e9,
              "-", lw=2, color="y", label="45-64 y.o.")
    #ax1.plot( [2020, 2020], [0, 10], "--", lw=2, color="k", label="Global policy")
    #ax1.plot( [2070, 2070], [0, 10], "-.", lw=2, color="k", label="Global stability")
    ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax1.set_ylim( 0, 10)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("billion")

    ax2.plot( DYNAMO_Engine.Model_Time, IndustrialOutputPerCapita.Data,
              "-", lw=2, color="b", label="Goods per capita")
    ax2.plot( DYNAMO_Engine.Model_Time, ServiceOutputPerCapita.Data,
              "-", lw=2, color="r", label="Services per capita")
    ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita.Data,
              "-", lw=2, color="g", label="Food per capita ($1/kg)")
    #ax2.plot( [2020, 2020], [10, 50], "--", lw=2, color="k")
    #ax2.plot( [2070, 2070], [10, 50], "-.", lw=2, color="k")
    ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    #ax2.set_ylim( 0, 500)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_ylabel("$ / person / year")

    ax3.plot( DYNAMO_Engine.Model_Time, CrudeBirthRate.Data,
              "-", lw=2, color="g", label="Crude Birth Rate")
    ax3.plot( DYNAMO_Engine.Model_Time, CrudeDeathRate.Data,
              "-", lw=2, color="r", label="Crude Death Rate")
    ax3.plot( DYNAMO_Engine.Model_Time, LifeExpectancy.Data,
              "--", lw=3, color="m", label="Life Expectancy [years]")
    ax3.plot( DYNAMO_Engine.Model_Time, LifeExpectancy_Reference.Data,
              ".", lw=1, alpha=0.5, color="k", label="Life Expectancy (check)")
    #ax3.plot( [2020, 2020], [10, 50], "--", lw=2, color="k")
    #ax3.plot( [2070, 2070], [10, 50], "-.", lw=2, color="k")
    ax3.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax3.set_ylim( 0, 60)
    ax3.grid(True)
    ax3.legend(loc=0)
    ax3.set_xlabel("Year")
    ax3.set_ylabel("per 1000 per year")
    
    plt.savefig( "./Graphs/Test_001_Population.png")
    plt.show()
