from DYNAMO_Prototypes import *

#
# Basic ERoEI illustration
#

Population = TableParametrization(
    "_001_Population",
    [1650.4,1778.7,1912.6,2088.6,2311.1,
    2556.0,3033.2,3700.6,4458.4,5330.9,
    6145.0,6958.2,7795.5,8551.2,9210.3,
    9771.8,10222.6,10575.8,10848.7,11050.1,
    11184.4], 1900, 2100,
    fupdate = "DYNAMO_Engine.time")

IndustrialOutputPerCapita = AuxVariable(
    "_049_IndustrialOutputPerCapita", "dollars / year",
    fupdate = "_050_IndustrialOutput.K"
    "/ _001_Population.K / 1000000")

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

IndustrialOutput = AuxVariable(
    "_050_IndustrialOutput", "dollars / year",
    fupdate = "_052_IndustrialCapital.K / 3"
    "* (1 - _134_FractionOfCapitalAllocatedToObtainingResources.K)")

IndustrialCapital = LevelVariable(
    "_052_IndustrialCapital", "210e9", "dollars",
    fupdate = "_050_IndustrialOutput.J * 0.40"
    "- _052_IndustrialCapital.J / 14")

NonrenewableResources = LevelVariable(
    "_129_NonrenewableResources",
    "_168_NonrenewableResourcesInitial.K", "resource units",
    fupdate = "-_130_NonrenewableResourceUsageRate.K")

NonrenewableResourceUsageRate = RateVariable(
    "_130_NonrenewableResourceUsageRate", "resource units / year",
    fupdate = "_050_IndustrialOutput.J / 15")

FractionOfCapitalAllocatedToObtainingResources = TableParametrization(
    "_134_FractionOfCapitalAllocatedToObtainingResources",
    [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05], 0, 1,
    fpoints_after_policy = [1, 0.9, 0.7, 0.5, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05],
    fupdate = "_129_NonrenewableResources.K"
    "/_168_NonrenewableResourcesInitial.K")

NonrenewableResourcesInitial = Parameter(
    "_168_NonrenewableResourcesInitial", 1400e9, "tonn")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.ListEquations()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )

fig = plt.figure( figsize=(15,15))
fig.suptitle('WORLD3 Test: Industry and Resources Illustration', fontsize=25)
gs = plt.GridSpec(2, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( DYNAMO_Engine.Model_Time, IndustrialCapital.Data, "-",
          lw=5, alpha=0.5, color="b", label="Capital")
ax1.plot( DYNAMO_Engine.Model_Time, NonrenewableResources.Data, "-",
          lw=5, alpha=0.5, color="g", label="Resources")
ax1.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
ax1.set_ylim( 0, 1.4e12)
ax1.grid(True)
ax1.legend(loc=0)
#ax1.set_ylabel("billion")

ax2.plot( DYNAMO_Engine.Model_Time, np.array(IndustrialOutputPerCapita.Data),
              "-", lw=3, color="b", label="Industrial Output Per Capita [kg/year]")

#ax2.plot( DYNAMO_Engine.Model_Time, np.array(IndustrialOutput.Data)/10,
#              "-", lw=3, color="b", label="Industrial Output [tonn/year]")
#ax2.plot( DYNAMO_Engine.Model_Time, NonrenewableResourceUsageRate.Data,
#              "-", lw=3, color="g", label="Resource Usage Rate [tonn/year]")
ax2.set_xlim( DYNAMO_Engine.Model_Time[0], DYNAMO_Engine.Model_Time[-1])
#ax2.set_ylim( 0, 15e9)
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_xlabel("Year")
ax2.set_ylabel("Units")
    
#plt.savefig( "./Graphs/Test_002_Capital.png")
plt.show()


##PlotVariable( IndustrialCapital, DYNAMO_Engine.Model_Time,
##    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
##    show=True)
##PlotVariable( NonrenewableResources, DYNAMO_Engine.Model_Time,
##    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
##    show=True)
