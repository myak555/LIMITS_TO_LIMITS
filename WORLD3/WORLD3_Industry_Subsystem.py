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
    "* _083_CapitalUtilizationFraction.K"
    "/ _051_IndustrialCapitalOutputRatio.K")

IndustrialCapitalOutputRatio = PolicyParametrization(
    "_051_IndustrialCapitalOutputRatio", 3, 3, "years")

IndustrialCapital = LevelVariable(
    "_052_IndustrialCapital", 2.1e11, "dollars",
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
    "_067_ServiceCapital", 1.44e11, "dollars",
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
# PARAMETERS
#
IndicativeConsumptionValue = Parameter(
    "_157_IndicativeConsumptionValue", 400, "dollars / person")

if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    CapitalUtilizationFraction = PolicyParametrization(
        "_083_CapitalUtilizationFraction", 0.9, 0.9,
        "unitless")

    FoodPerCapita = PolicyParametrization(
        "_088_FoodPerCapita",
        800, 800, "kg / person / year")

    FractionOfIndustrialOutputAllocatedToAgriculture = PolicyParametrization(
        "_093_FractionOfIndustrialOutputAllocatedToAgriculture", 0.10, 0.1,
        "unitless")

    FractionOfCapitalAllocatedToObtainingResources = PolicyParametrization(
        "_134_FractionOfCapitalAllocatedToObtainingResources", 0.03, 0.10,
        "unitless")

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

    #
    #Test_Run
    #
    vrb = False
    DYNAMO_Engine.SortByType()
    DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.Produce_Solution_Path( verbose = vrb)
    DYNAMO_Engine.ListSolutionPath()
    DYNAMO_Engine.Reset(
        dt=0.5, global_policy_year=2020,
        global_stability_year=2070,
        verbose = vrb)
    DYNAMO_Engine.Warmup( verbose = vrb)
    DYNAMO_Engine.Compute( verbose = vrb)
    PlotVariable( IndustrialCapital, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
    PlotVariable( FractionOfIndustrialOutputAllocatedToIndustry, DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

    Population.Data = np.array(Population.Data)
    Population0To14.Data = np.array(Population0To14.Data)
    Population15To44.Data = np.array(Population15To44.Data)
    Population45To64.Data = np.array(Population45To64.Data)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle('WORLD3 Test: Population and Industry Only', fontsize=25)
    gs = plt.GridSpec(2, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ax1.plot( DYNAMO_Engine.Model_Time,
              Population.Data/1e9, "-", lw=5, alpha=0.5, color="b")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Population.Data/1e9, "o", lw=1, color="k", label="Population Total")
    ax1.plot( DYNAMO_Engine.Model_Time,
              Population0To14.Data/1e9, "-", lw=2, color="g", label="0-14 y.o.")
    ax1.plot( DYNAMO_Engine.Model_Time,
              (Population0To14.Data + Population15To44.Data)/1e9, "-", lw=2, color="r", label="15-14 y.o.")
    ax1.plot( DYNAMO_Engine.Model_Time,
              (Population0To14.Data + Population15To44.Data + Population45To64.Data)/1e9,
              "-", lw=2, color="y", label="45-64 y.o.")
    ax1.plot( [2020, 2020], [0, 10], "--", lw=2, color="k", label="Global policy")
    ax1.plot( [2070, 2070], [0, 10], "-.", lw=2, color="k", label="Global stability")
    ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax1.set_ylim( 0, 12)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("billion")

    ax2.plot( DYNAMO_Engine.Model_Time, IndustrialOutputPerCapita.Data,
              "-", lw=2, color="b", label="Industrial Output Per Capita [$ / year]")
    ax2.plot( DYNAMO_Engine.Model_Time, ServiceOutputPerCapita.Data,
              "-", lw=2, color="m", label="Service Output Per Capita [$ / year]")
    ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita.Data,
              "--", lw=3, color="g", label="Food Per Capita [kg / year]")
    ax2.plot( [2020, 2020], [0, 10000], "--", lw=2, color="k")
    ax2.plot( [2070, 2070], [0, 10000], "-.", lw=2, color="k")
    ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax2.set_ylim( 0, 1000)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Units")
    
    plt.savefig( "./Graphs/Test_002_Capital.png")
    plt.show()
