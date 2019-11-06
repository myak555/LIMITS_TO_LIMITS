from WORLDFree_Full_System import *
from Utilities import Load_Calibration as clb

    
#
#Test_Run
#
vrb = False
DYNAMO_Engine.SortByType()
#DYNAMO_Engine.ListEquations()
DYNAMO_Engine.ListDictionary( "levels")
DYNAMO_Engine.Produce_Solution_Path( verbose = vrb)
#DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset(
    dt=1, global_policy_year=2150,
    global_stability_year=4000,
    verbose = vrb)
DYNAMO_Engine.Warmup( verbose = vrb)
DYNAMO_Engine.Compute( verbose = vrb)

yUrban, pTotal, Urban = clb("./Calibrations/Urban_Population_UN.txt",
                     ["Year", "Population", "Urban"], separator="\t")

##    PlotVariable( IndustrialOutputPerCapita, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##    PlotVariable( FractionOfIndustrialOutputAllocatedToIndustry, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##    PlotVariable( FractionOfIndustrialOutputAllocatedToServices, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##    PlotVariable( FractionOfIndustrialOutputAllocatedToAgriculture, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
##    PlotVariable( FractionOfIndustrialOutputAllocatedToConsumption, DYNAMO_Engine.Model_Time,
##                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)

fig = plt.figure( figsize=(15,15))
fig.suptitle('WORLD3 Test: BAU Model', fontsize=25)
gs = plt.GridSpec(3, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( DYNAMO_Engine.Model_Time,
          np.array(Population.Data)/1e9, "-", lw=6, alpha=0.5, color="b", label="Total Population")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array(Population.Data)*1e-9*np.array(FractionOfPopulationUrban.Data), "-",
          lw=2, color="m", label="Urban Population")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array( LaborForce.Data)/1e9, "-", lw=3, alpha=0.5, color="g", label="Labor force")
ax1.plot( DYNAMO_Engine.Model_Time,
          np.array( Jobs.Data)/1e9, "-", lw=3, alpha=0.5, color="r", label="Jobs")
ax1.errorbar( yUrban, pTotal*1.e-3, yerr=pTotal*5.e-5, fmt=".",
              color="k", alpha=0.5, label="(UN actual)")
ax1.errorbar( yUrban, Urban*1.e-3, yerr=Urban*5.e-5, fmt=".",
              color="m", alpha=0.5)
ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
ax1.set_ylim( 0, 10)
ax1.grid(True)
ax1.legend(loc=0)
ax1.set_ylabel("billion")

ax2.plot( DYNAMO_Engine.Model_Time, IndustrialOutputPerCapita.Data,
          "-", lw=6, color="b", alpha=0.5, label="Goods per capita")
ax2.plot( DYNAMO_Engine.Model_Time, ServiceOutputPerCapita.Data,
          "-", lw=6, color="r", alpha=0.5, label="Services per capita")
ax2.plot( DYNAMO_Engine.Model_Time, FoodPerCapita.Data,
          "-", lw=6, color="g", alpha=0.5, label="Food per capita ($1/kg)")
ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
#ax2.set_ylim( 0, 500)
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_ylabel("$ / person / year")

ax3.plot( DYNAMO_Engine.Model_Time, np.array( NonrenewableResources.Data) / 1e9,
          "-", lw=6, color="b", alpha=0.5, label="Nonrenewable Resources")
ax3.plot( DYNAMO_Engine.Model_Time, np.array( PersistentPollution.Data) / 1e7,
          "-", lw=6, color="m", alpha=0.5, label="Persistent Pollution x 100")
ax3.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
#ax3.set_ylim( 0, 60)
ax3.grid(True)
ax3.legend(loc=0)
ax3.set_xlabel("Year")
ax3.set_ylabel("10^9 tonn")

plt.savefig( "./Calibrations/Test_001_BAU.png")
plt.show()

##    FractionOfCapitalAllocatedToObtainingResources.GetPoints(
##        "./Data/FractionOfCapitalAllocatedToObtainingResources.csv",
##        x=np.linspace(0, 1.1, 111))
##    PerCapitaResourceUsageMultiplier.GetPoints(
##        "./Data/PerCapitaResourceUsageMultiplier.dgt.csv",
##        x=np.linspace(0, 1700, 111))
##    IndicatedFoodPerCapita.GetPoints(
##        "./Data/IndicatedFoodPerCapita.dgt.csv",
##        x=np.linspace(0, 1700, 111))
##    IndicatedServiceOutputPerCapita.GetPoints(
##        "./Data/IndicatedServiceOutputPerCapita.dgt.csv",
##        x=np.linspace(0, 1800, 111))
##    FractionOfIndustrialOutputAllocatedToAgriculture.GetPoints(
##        "./Data/FractionOfIndustrialOutputAllocatedToAgriculture.dgt.csv",
##        x=np.linspace(0, 4, 111))
##    FractionOfIndustrialOutputAllocatedToServices.GetPoints(
##        "./Data/FractionOfIndustrialOutputAllocatedToServices.dgt.csv",
##        x=np.linspace(0, 2.2, 111))
#OutputCSV(
#[Population, Population0To14, Population15To44, Population45To64, Population65AndOver,
#LifeExpectancy, TotalFertility, CrudeDeathRate, CrudeBirthRate],
#DYNAMO_Engine.Model_Time,
#"./Data/Demographics_Checks.csv")

#OutputCSV(
#[Population, Population0To14,
#LifeExpectancy, TotalFertility,
#IndustrialOutputPerCapita, ServiceOutputPerCapita, FoodPerCapita],
#DYNAMO_Engine.Model_Time,
#"./Data/Life_Quality_Checks.csv")
#OutputCSV(
#[IndustrialOutputPerCapita, ServiceOutputPerCapita, FoodPerCapita],
#DYNAMO_Engine.Model_Time,
#"./Data/Per_Capita_Output_Checks.csv")
#OutputCSV(
#[PersistentPollution],
#DYNAMO_Engine.Model_Time,
#"./Data/Pollution_Checks.csv")
#OutputCSV(
#[IndustrialCapital, ServiceCapital, IndustrialOutput, ServiceOutput, Food],
#DYNAMO_Engine.Model_Time,
#"./Data/Capital_Checks.csv")
