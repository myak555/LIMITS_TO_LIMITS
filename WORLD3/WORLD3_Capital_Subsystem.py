from WORLD3_Population_Subsystem import *

#
# This run checks the population subsystem together with
# industry, services and labor parts of the capital subsystem.
# The agriculture outputs per capita
# are presumed constant (equations {83}-{143});
# Resources and pollution are constant
#

#
# INDUSTRY SUBSYSTEM (equations {49}-{59})
#
IndustrialOutputPerCapita = AuxVariable(
    "_049_IndustrialOutputPerCapita",
    "dollars / person / year",
    fupdate = "_050_IndustrialOutput.K / _001_Population.K")

IndustrialOutput = AuxVariable(
    "_050_IndustrialOutput", "dollars / year",
    fupdate = "_052_IndustrialCapital.K"
    "* (1 - _134_FractionOfCapitalAllocatedToObtainingResources.K)"
    "* _083_CapitalUtilizationFraction.K"
    "/ _051_IndustrialCapitalOutputRatio.K")

IndustrialCapitalOutputRatio = PolicyParametrization(
    "_051_IndustrialCapitalOutputRatio", 3, 3, "years")

IndustrialCapital = LevelVariable(
    "_052_IndustrialCapital", "2.1e11", "dollars",
    fupdate = "_055_IndustrialCapitalInvestmentRate.J"
    "- _053_IndustrialCapitalDepreciationRate.J")

IndustrialCapitalDepreciationRate = RateVariable(
    "_053_IndustrialCapitalDepreciationRate", "dollars / year",
    fupdate = "_052_IndustrialCapital.K"
    "/ _054_AverageLifetimeOfIndustrialCapital.K")

AverageLifetimeOfIndustrialCapital = PolicyParametrization(
    "_054_AverageLifetimeOfIndustrialCapital", 14, 14, "years")

IndustrialCapitalInvestmentRate = RateVariable(
    "_055_IndustrialCapitalInvestmentRate", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _056_FractionOfIndustrialOutputAllocatedToIndustry.K")

FractionOfIndustrialOutputAllocatedToIndustry = AuxVariable(
    "_056_FractionOfIndustrialOutputAllocatedToIndustry",
    fupdate = "1 - _057_FractionOfIndustrialOutputAllocatedToConsumption.K"
    "- _063_FractionOfIndustrialOutputAllocatedToServices.K"
    "- _093_FractionOfIndustrialOutputAllocatedToAgriculture.K")

FractionOfIndustrialOutputAllocatedToConsumption = AuxVariable(
    "_057_FractionOfIndustrialOutputAllocatedToConsumption",
    fupdate = "_058_FractionOfIndustrialOutputAllocatedToConsumptionConstant.K",
    fequilibrium = "_059_FractionOfIndustrialOutputAllocatedToConsumptionVariable.K")

FractionOfIndustrialOutputAllocatedToConsumptionConstant = PolicyParametrization(
    "_058_FractionOfIndustrialOutputAllocatedToConsumptionConstant", 0.43, 0.43)

FractionOfIndustrialOutputAllocatedToConsumptionVariable = TableParametrization(
    "_059_FractionOfIndustrialOutputAllocatedToConsumptionVariable",
    [0.3, 0.32, 0.34, 0.36, 0.38, 0.43, 0.73, 0.77, 0.81, 0.82, 0.83], 0, 2,
    fupdate = "_049_IndustrialOutputPerCapita.K"
    "/ _157_IndicativeConsumptionValue.K")

#
# SERVICES SUBSYSTEM (equations {60}, {63}, {66}-{72})
#
IndicatedServiceOutputPerCapita = TableParametrization(
    "_060_IndicatedServiceOutputPerCapita",
    [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    0, 1600, "dollars / person / year",
    fpoints_after_policy = [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    fupdate = "_049_IndustrialOutputPerCapita.K")

#
# svc_061, svc_062 - used to be policy tables, now in {060}
#

FractionOfIndustrialOutputAllocatedToServices = TableParametrization(
    "_063_FractionOfIndustrialOutputAllocatedToServices",
    [0.3, 0.2, 0.1, 0.05, 0], 0, 2,
    fpoints_after_policy = [0.3, 0.2, 0.1, 0.05, 0],
    fupdate = "_071_ServiceOutputPerCapita.K"
    "/ _060_IndicatedServiceOutputPerCapita.K")

#
# svc064, svc065 - used to be policy tables, now in {063}
#

ServiceCapitalInvestmentRate = RateVariable(
    "_066_ServiceCapitalInvestmentRate", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "* _063_FractionOfIndustrialOutputAllocatedToServices.K")

ServiceCapital = LevelVariable(
    "_067_ServiceCapital", "1.44e11", "dollars",
    fupdate = "_066_ServiceCapitalInvestmentRate.J"
    "- _068_ServiceCapitalDepreciationRate.J")

ServiceCapitalDepreciationRate = RateVariable(
    "_068_ServiceCapitalDepreciationRate", "dollars / year",
    fupdate = "_067_ServiceCapital.K"
    "/ _069_AverageLifetimeOfServiceCapital.K")

AverageLifetimeOfServiceCapital = PolicyParametrization(
    "_069_AverageLifetimeOfServiceCapital", 20, 20, "years")

ServiceOutput = AuxVariable(
    "_070_ServiceOutput", "dollars / year",
    fupdate = "_067_ServiceCapital.K"
    "* _083_CapitalUtilizationFraction.K"
    "/ _072_ServiceCapitalOutputRatio.K")

ServiceOutputPerCapita = AuxVariable(
    "_071_ServiceOutputPerCapita", "dollars / person / year",
    fupdate = "_070_ServiceOutput.K / _001_Population.K")

ServiceCapitalOutputRatio = PolicyParametrization(
    "_072_ServiceCapitalOutputRatio", 1, 1, "years")

#
# LABOR SUBSYSTEM (equations {73}-{83})
#
Jobs = AuxVariable(
    "_073_Jobs", "persons",
    fupdate = "_074_PotentialJobsInIndustrialSector.K"
    "+ _076_PotentialJobsInServiceSector.K"
    "+ _078_PotentialJobsInAgriculturalSector.K")

PotentialJobsInIndustrialSector = AuxVariable(
    "_074_PotentialJobsInIndustrialSector", "persons",
    fupdate = "_052_IndustrialCapital.K"
    "* _075_JobsPerIndustrialCapitalUnit.K")

JobsPerIndustrialCapitalUnit = TableParametrization(
    "_075_JobsPerIndustrialCapitalUnit",
    [0.00037, 0.00018, 0.00012, 0.00009, 0.00007, 0.00006],
    50, 800, "persons / dollar",
    fupdate = "_049_IndustrialOutputPerCapita.K")

PotentialJobsInServiceSector = AuxVariable(
    "_076_PotentialJobsInServiceSector", "persons",
    fupdate = "_067_ServiceCapital.K"
    "* _077_JobsPerServiceCapitalUnit.K")

JobsPerServiceCapitalUnit = TableParametrization(
    "_077_JobsPerServiceCapitalUnit",
    [.0011, 0.0006, 0.00035, 0.0002, 0.00015, 0.00015],
    50, 800, "persons / dollar",
    fupdate = "_071_ServiceOutputPerCapita.K")

PotentialJobsInAgriculturalSector = AuxVariable(
    "_078_PotentialJobsInAgriculturalSector", "persons",
    fupdate = "_085_ArableLand.K * _079_JobsPerHectare.K")

JobsPerHectare = TableParametrization(
    "_079_JobsPerHectare",
    [2, 0.5, 0.4, 0.3, 0.27, 0.24, 0.2, 0.2],
    2, 30, "persons / hectare",
    fupdate = "_101_AgriculturalInputsPerHectare.K")

LaborForce = AuxVariable(
    "_080_LaborForce", "persons",
    fupdate = "0.75 * (_006_Population15To44.K"
    "+ _010_Population45To64.K)")
    # 0.75 - participation fraction

LaborUtilizationFraction = AuxVariable(
    "_081_LaborUtilizationFraction",
    fupdate = "_073_Jobs.K / _080_LaborForce.K")

LaborUtilizationFractionDelayed = SmoothVariable(
    "_082_LaborUtilizationFractionDelayed",
    "_158_LaborUtilizationFractionDelayTime.K",
    fupdate = "_081_LaborUtilizationFraction.K")


#CapitalUtilizationFraction = Parameter(
#    "_083_CapitalUtilizationFraction", 0.8)

# This is confirmed to be the source of model instability
# for dt>1. The utilization jumps between 1 and 0.2.
# LaborUtilizationFractionDelayTime is set to 2 years
# This prevents it from smoothing if dt>=2 
CapitalUtilizationFraction = TableParametrization(
    "_083_CapitalUtilizationFraction",
    [1.0, 0.9, 0.7, 0.3, 0.1, 0.1], 1, 11,
    fupdate = "_082_LaborUtilizationFractionDelayed.K",
    fignore = ["_082_LaborUtilizationFractionDelayed"], # to break a circular dependency
    initialValue = 1.0)

#
# NONRENEWABLE RESOURCE SECTOR (equations {129}-{134})
#
NonrenewableResources = LevelVariable(
    "_129_NonrenewableResources",
    "_168_NonrenewableResourcesInitial.K", "resource units",
    fupdate = "-_130_NonrenewableResourceUsageRate.J")

NonrenewableResourceUsageRate = RateVariable(
    "_130_NonrenewableResourceUsageRate", "resource units / year",
    fupdate = "_001_Population.K"
    "* _132_PerCapitaResourceUsageMultiplier.K"
    "* _131_NonrenewableResourceUsageFactor.K")

NonrenewableResourceUsageFactor = PolicyParametrization(
    "_131_NonrenewableResourceUsageFactor", 1, 1)

PerCapitaResourceUsageMultiplier = TableParametrization(
    "_132_PerCapitaResourceUsageMultiplier",
    [0, 0.85, 2.6, 4.4, 5.4, 6.2, 6.8, 7, 7],
    0, 1600, "resource units / person / year",
    fupdate = "_049_IndustrialOutputPerCapita.K")

NonrenewableResourceFractionRemaining = AuxVariable(
    "_133_NonrenewableResourceFractionRemaining",
    fupdate = "_129_NonrenewableResources.K"
    "/ _168_NonrenewableResourcesInitial.K")

FractionOfCapitalAllocatedToObtainingResources = TableParametrization(
    "_134_FractionOfCapitalAllocatedToObtainingResources",
    [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05], 0, 1,
    fpoints_after_policy = [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05],
    fupdate = "_133_NonrenewableResourceFractionRemaining.K")


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

    NonrenewableResourcesInitial = Parameter(
        "_168_NonrenewableResourcesInitial", 1.0e12, "resource units")


    #
    # NUMERICAL CHECKS (this test only)
    #

    #IndustrialOutputPerCapita = AuxVariable(
    #    "_049_IndustrialOutputPerCapita", "dollars / person / year",
    #    fupdate = "_649_Goods_Digitized.K * 5")
    #IndustrialOutputPerCapita = Parameter(
    #    "_049_IndustrialOutputPerCapita",
    #    200, "dollars / person / year")

    #ServiceOutputPerCapita = AuxVariable(
    #    "_071_ServiceOutputPerCapita", "dollars / person / year",
    #    fupdate = "_671_Services_Digitized.K * 1e11 / _001_Population.K")
    #ServiceOutputPerCapita = Parameter(
    #    "_071_ServiceOutputPerCapita",
    #    50, "dollars")

    FoodPerCapita = AuxVariable(
        "_088_FoodPerCapita", "kg / person / year",
        fupdate = "_688_FoodPerCapita_Digitized.K * 10")

    #FoodPerCapita = PolicyParametrization(
    #    "_088_FoodPerCapita",
    #    900, 900, "kg / person / year")

    ArableLand = Parameter(
        "_085_ArableLand", 0.9e9, "hectares")

    FractionOfIndustrialOutputAllocatedToAgriculture = PolicyParametrization(
        "_093_FractionOfIndustrialOutputAllocatedToAgriculture", 0.05, 0.1,
        "unitless")

    AgriculturalInputsPerHectare = PolicyParametrization(
        "_101_AgriculturalInputsPerHectare", 20, 20, "dollars / hectare / year")

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
    PlotVariable( IndustrialCapital, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
    PlotVariable( CapitalUtilizationFraction, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle('WORLD3 Test: Population and Capital', fontsize=25)
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
              ".", lw=2, color="r", alpha=0.5,)
    ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita.Data,
              "-", lw=2, color="g", label="Food per capita ($1/kg)")
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
    
    plt.savefig( "./Graphs/Test_002_Capital.png")
    plt.show()

    #OutputCSV(
    #[IndustrialOutput_Reference, ServiceOutput_Reference],
    #DYNAMO_Engine.Model_Time,
    #"./Data/Output_Checks.csv")

