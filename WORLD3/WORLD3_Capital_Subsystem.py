from WORLD3_Population_Subsystem import *

#
# This run checks the population subsystem together with
# industry, services and labor parts of the capital subsystem.
# The agriculture outputs per capita
# are presumed constant (equations {83}-{143});
# Resources and polution are constant
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
    "* _083_CapitalUtilizationFraction.K / 2.6")
#    "* _051_IndustrialCapitalOutputRatio.K")
#    "/ _051_IndustrialCapitalOutputRatio.K")

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
    fupdate = "_049_IndustrialOutputPerCapita.K"
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


#
# PARAMETERS
#
IndicativeConsumptionValue = Parameter(
    "_157_IndicativeConsumptionValue", 400, "dollars / person")

LaborUtilizationFractionDelayTime = Parameter(
    "_158_LaborUtilizationFractionDelayTime", 2, "years")

NonrenewableResourcesInitial = Parameter(
    "_168_NonrenewableResourcesInitial", 1.0e12, "resource units")

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
