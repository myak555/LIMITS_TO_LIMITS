from DYNAMO_Prototypes import *

#
# This run checks only the population subsystem,
# presuming the industry, agriculture and services
# outputs per capita to be constant (equations {049}-{143})
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

if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    IndustrialOutputPerCapita = Parameter(
        "_049_IndustrialOutputPerCapita",
        200, "dollars / person / year")

    ServiceOutputPerCapita = Parameter(
        "_071_ServiceOutputPerCapita",
        50, "dollars")

    FoodPerCapita = PolicyParametrization(
        "_088_FoodPerCapita",
        900, 900, "kg / person / year")

    IndexOfPersistentPollution = Parameter(
        "_143_IndexOfPersistentPollution", 1)

    #
    # Parametrization plots
    #
    PlotTable( DYNAMO_Engine, Mortality0To14, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality15To44, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality45To64, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, Mortality65AndOver, 0, 100, "LifeExpectancy [years]", show=False)
    PlotTable( DYNAMO_Engine, HealthServicesAllocationsPerCapita, 0, 2200,
               "ServiceOutputPerCapita [dollars / person / year]", show=False)
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
    fig.suptitle('WORLD3 Test: Population Only', fontsize=25)
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
    ax1.set_ylim( 0, 16)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("billion")

    ax2.plot( DYNAMO_Engine.Model_Time, CrudeBirthRate.Data,
              "-", lw=2, color="g", label="Crude Birth Rate")
    ax2.plot( DYNAMO_Engine.Model_Time, CrudeDeathRate.Data,
              "-", lw=2, color="r", label="Crude Death Rate")
    ax2.plot( DYNAMO_Engine.Model_Time, LifeExpectancy.Data,
              "--", lw=3, color="m", label="Life Expectancy [years]")
    ax2.plot( [2020, 2020], [10, 50], "--", lw=2, color="k")
    ax2.plot( [2070, 2070], [10, 50], "-.", lw=2, color="k")
    ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
    ax2.set_ylim( 15, 55)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("per 1000 per year")
    
    plt.savefig( "./Graphs/Test_001_Population.png")
    plt.show()
