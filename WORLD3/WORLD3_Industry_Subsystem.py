from WORLD3_Population_Subsystem import *

#
# This run checks the population and industry subsystems
# running together. The agriculture and services outputs per capita
# are presumed constant (equations {63}-{143})
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

fractionOfIndustrialOutputAllocatedToIndustry = AuxVariable(
    "_056_FractionOfIndustrialOutputAllocatedToIndustry",
    fupdate = "1 - _093_FractionOfIndustrialOutputAllocatedToAgriculture.K"
    "- _063_FractionOfIndustrialOutputAllocatedToServices.K"
    "- _057_FractionOfIndustrialOutputAllocatedToConsumption.K")

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
# PARAMETERS
#
IndicativeConsumptionValue = Parameter(
    "_157_IndicativeConsumptionValue", 400, "dollars / person")

if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    FractionOfIndustrialOutputAllocatedToServices = PolicyParametrization(
        "_063_FractionOfIndustrialOutputAllocatedToServices", 0.2, 0.2,
        "unitless")

    ServiceOutputPerCapita = Parameter(
        "_071_ServiceOutputPerCapita",
        100, "dollars")

    CapitalUtilizationFraction = PolicyParametrization(
        "_083_CapitalUtilizationFraction", 0.7, 0.7,
        "unitless")

    FoodPerCapita = PolicyParametrization(
        "_088_FoodPerCapita",
        800, 400, "kg / person / year")

    FractionOfIndustrialOutputAllocatedToAgriculture = PolicyParametrization(
        "_093_FractionOfIndustrialOutputAllocatedToAgriculture", 0.2, 0.2,
        "unitless")

    FractionOfCapitalAllocatedToObtainingResources = PolicyParametrization(
        "_134_FractionOfCapitalAllocatedToObtainingResources", 0.10, 0.10,
        "unitless")

    IndexOfPersistentPollution = Parameter(
        "_143_IndexOfPersistentPollution", 1)

    #
    # Parametrization plots
    #
    PlotTable( DYNAMO_Engine,
           FractionOfIndustrialOutputAllocatedToConsumptionVariable,
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
        dt=5, global_policy_year=2020,
        global_stability_year=2070,
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
    
    plt.savefig( "./Graphs/Test_002_Industry.png")
    plt.show()
