from DYNAMO_Prototypes import *
from Utilities import Load_Calibration as clb

GraphShow = False

#
# Population a function of LEB and TFR calibration
#

#
# POPULATION SUBSYSTEM (equations {1}-{18}, {30}, {31})
# as function of actual UN data {19}, {32}
#
# Validated
Population = AuxVariable(
    "_001_Population", "persons",
    fupdate = "_002_Population0To14.K + _006_Population15To44.K"
    "+ _010_Population45To64.K + _014_Population65AndOver.K")

# Digitized from http://bit-player.org/extras/limits/ltg.html
Population_Check = TableParametrization(
    "_901_Population_Check",
    [1.67E+09,1.88E+09,2.10E+09,2.31E+09,2.57E+09,	
     3.04E+09,3.59E+09,4.23E+09,4.96E+09,5.86E+09,	
     6.80E+09,7.74E+09,8.60E+09,9.24E+09,9.20E+09,	
     8.56E+09,7.66E+09,6.84E+09,6.16E+09,5.60E+09,5.22E+09],
    1900, 2100, "persons",
    fupdate = "DYNAMO_Engine.time")

#
# Population 0-14
#
# Validated
# Initial value changed from 0.65е9 to 0.67e9
Population0To14 = LevelVariable(
    "_002_Population0To14", "0.67e9", "persons",
    fupdate = "_030_BirthsPerYear.J - _003_DeathsPerYear0To14.J"
    "- _005_MaturationsPerYear14to15.J")

# Validated
DeathsPerYear0To14 = RateVariable(
    "_003_DeathsPerYear0To14", "persons / year",
    fupdate = "_002_Population0To14.K * _004_Mortality0To14.K")

# Validated
# The original table from 1972 book:
# [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010]
# These values have been adjusted to match the UN age distribution stats
Mortality0To14 = TableParametrization(
    "_004_Mortality0To14",
    [0.0850, 0.0575, 0.0355, 0.0157, 0.0065, 0.0018, 0.0008],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, Mortality0To14, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear14to15 = RateVariable(
    "_005_MaturationsPerYear14to15", "persons / year",
    fupdate = "_002_Population0To14.K"
    "* (1 - _004_Mortality0To14.K) / 15.0")

#
# Population 15-44
#
# Validated
# Initial value changed from 0.70е9 to 0.72e9
Population15To44 = LevelVariable(
    "_006_Population15To44", "0.72e9", "persons",
    fupdate = "_005_MaturationsPerYear14to15.J - _007_DeathsPerYear15To44.J"
    "- _009_MaturationsPerYear44to45.J")

# Validated
# Calibration 0.8 is applied to match the UN age structure data
DeathsPerYear15To44 = RateVariable(
    "_007_DeathsPerYear15To44", "persons / year",
    fupdate = "_006_Population15To44.K * _008_Mortality15To44.K")

# Validated
# The original table from 1972 book:
# [0.0266, 0.0171, 0.0110, 0.0065, 0.0040, 0.0016, 0.0008]
# These values have been adjusted to match the UN age distribution stats
Mortality15To44 = TableParametrization(
    "_008_Mortality15To44",
    [0.0213, 0.0137, 0.0088, 0.0046, 0.0010, 0.0001, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, Mortality15To44, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear44to45 = RateVariable(
    "_009_MaturationsPerYear44to45", "persons / year",
    fupdate = "_006_Population15To44.K * (1 - _008_Mortality15To44.K) / 30.0")

#
# Population 45-64
#

# Validated
# Initial value changed from 0.19е9 to 0.195e9 (for 1.65e9 total population in 1900)
Population45To64 = LevelVariable(
    "_010_Population45To64", "0.195e9", "persons",
    fupdate = "_009_MaturationsPerYear44to45.J - _011_DeathsPerYear45To64.J"
    "- _013_MaturationsPerYear64to65.J")

# Validated
DeathsPerYear45To64 = RateVariable(
    "_011_DeathsPerYear45To64", "persons / year",
    fupdate = "_010_Population45To64.K * _012_Mortality45To64.K")

# Validated
# The original table from 1972 book:
# [0.0562, 0.0373, 0.0252, 0.0171, 0.0118, 0.0083, 0.0060]
# These values have been adjusted to match the UN age distribution stats
Mortality45To64 = TableParametrization(
    "_012_Mortality45To64",
    [0.0450, 0.0298, 0.0195, 0.0115, 0.0034, 0.0002, 0.0001],
    20, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, Mortality45To64, 0, 100, "LifeExpectancy [years]", show=GraphShow)

# Validated
MaturationsPerYear64to65 = RateVariable(
    "_013_MaturationsPerYear64to65", "persons / year",
    fupdate = "_010_Population45To64.K * (1 - _012_Mortality45To64.K) / 20.0")


#
# Population over 65
#

# Validated
Population65AndOver = LevelVariable(
    "_014_Population65AndOver", "0.060e9", "persons",
    fupdate = "_013_MaturationsPerYear64to65.J - _015_DeathsPerYear65AndOver.J")

# Validated
DeathsPerYear65AndOver = RateVariable(
    "_015_DeathsPerYear65AndOver", "persons / year",
    fupdate = "_014_Population65AndOver.K * _016_Mortality65AndOver.K")

# Validated
# The original table from 1972 book:
# [0.13, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04] for the range of [20, 80]
# These values have been adjusted to match the UN age distribution stats
Mortality65AndOver = TableParametrization(
    "_016_Mortality65AndOver",
    [0.129, 0.127, 0.124, 0.120, 0.115, 0.108, 0.098, 0.060, 0.010],
    40, 80, "deaths / person / year",
    fupdate = "_019_LifeExpectancy.K")
PlotTable( DYNAMO_Engine, Mortality65AndOver, 0, 100, "LifeExpectancy [years]", show=GraphShow)

#
# Death rate and life expectancy
#

# Validated
DeathsPerYear = AuxVariable(
    "_017_DeathsPerYear", "persons / year",
    fupdate = "_003_DeathsPerYear0To14.J  + _007_DeathsPerYear15To44.J"
    "+ _011_DeathsPerYear45To64.J + _015_DeathsPerYear65AndOver.J")

# Validated
CrudeDeathRate = AuxVariable(
    "_018_CrudeDeathRate", "deaths / 1000 persons / year",
    fupdate = "1000 * _017_DeathsPerYear.K / _001_Population.K")

# Digitized from http://bit-player.org/extras/limits/ltg.html
CrudeDeathRate_Check = TableParametrization(
    "_918_CrudeDeathRate_Check",
    [28.6,29.8,30.1,29.8,24.6,
     23.0,21.7,19.8,17.6,16.2,
     15.5,14.7,14.2,15.5,21.4,
     30.3,32.2,36.0,37.8,39.2,39.2],
    1900, 2100,"deaths / 1000 persons / year",
    fupdate = "DYNAMO_Engine.time")

LifeExpectancy = AuxVariable(
    "_019_LifeExpectancy", "years",
    fupdate = "_219_LifeExpectancy_Tabular.K"
    "* _319_LEBCorrection_WW2.K"
    "* _419_LEBCorrection_GreatLeapForward.K")

#
# Numerical data from
# https://ourworldindata.org/life-expectancy
#
LifeExpectancy_Tabular = TableParametrization(
    "_219_LifeExpectancy_Tabular",
    [29.7, # 1870 (estimates)
     30.0, # 1875
     30.3, # 1880
     30.7, # 1885
     31.1, # 1890
     31.5, # 1895
     32.0, # 1900
     33.0, # 1905
     34.1, # 1910
     34.2, # 1915
     34.4, # 1920
     34.7, # 1925
     35.0, # 1930
     38.0, # 1935
     41.0, # 1940
     44.0, # 1945
     45.7, # 1950 (relatively reliable data)
     48.2, # 1955
     50.2, # 1960
     53.3, # 1965
     56.8, # 1970
     59.2, # 1975
     61.2, # 1980
     62.9, # 1985
     64.2, # 1990
     65.1, # 1995
     66.3, # 2000
     68.0, # 2005
     69.9, # 2010
     71.6, # 2015
     72.6  # 2020 (prediction)
     ],
    1870, 2020, "years",
    fupdate = "DYNAMO_Engine.time")

# Corrections for actual known events
LEBCorrection_WW2 = TableParametrization(
    "_319_LEBCorrection_WW2",
    [1.0,0.95,0.95,1.0],
    1939, 1947,
    fupdate = "DYNAMO_Engine.time")

LEBCorrection_GreatLeapForward = TableParametrization(
    "_419_LEBCorrection_GreatLeapForward",
    [1.0,0.9,0.9,1.0],
    1957.5, 1961.5,
    fupdate = "DYNAMO_Engine.time")

# Digitized from http://bit-player.org/extras/limits/ltg.html
LifeExpectancy_Check = TableParametrization(
    "_919_LifeExpectancy_Check",
    [40.909,40.642,41.176,41.979,48.663,
     50.802,53.476,56.952,60.963,63.904,
     66.578,69.786,71.925,70.053,59.358,
     46.791,43.583,38.770,36.096,34.492,33.957],
    1900, 2100, "years",
    fupdate = "DYNAMO_Engine.time")

# Validated
# Adjustment factor Females20to40Ratio accounts for male-female disbalance
# Fertility period adjusted from 30.0 to 28.3 years to match the UN crude birth rate stats
BirthsPerYear = RateVariable(
    "_030_BirthsPerYear", "persons / year",
    fupdate = "_032_TotalFertility.K * _006_Population15To44.K"
    "* _232_FertilityCorrection_WW2.K"
    "* _230_Females20to40Ratio.K / _330_AverageFertilityPeriod.K",
    fequilibrium = "_017_DeathsPerYear.K")

#
# Adjustment based on the UN gender distribution data
# https://ourworldindata.org/gender-ratio
#
Females20to40Ratio  = TableParametrization(
    "_230_Females20to40Ratio",
    [0.51,0.49],
    1950, 2020,
    fupdate = "DYNAMO_Engine.time")
PlotTable( DYNAMO_Engine, Females20to40Ratio, 1900, 2100, "Time [years]", show=GraphShow)

#
# Adjustment based on fertility period
# Lower TFR usually means the first birth
# later than 15 years of age.
#
AverageFertilityPeriod  = TableParametrization(
    "_330_AverageFertilityPeriod",
    [26.3,28.3],
    2.8, 5.0, "years",
    fupdate = "_032_TotalFertility.K")
PlotTable( DYNAMO_Engine, AverageFertilityPeriod, 0, 6, "TFR [children per woman]", show=GraphShow)

# Validated
CrudeBirthRate = AuxVariable(
    "_031_CrudeBirthRate", "births / 1000 persons / year",
    fupdate = "1000 * _030_BirthsPerYear.J / _001_Population.K")

# Digitized from http://bit-player.org/extras/limits/ltg.html
CrudeBirthRate_Check = TableParametrization(
    "_931_CrudeBirthRate_Check",
    [39.0,41.4,40.9,40.6,41.8,	
     40.0,38.4,36.5,34.5,32.4,
     29.5,27.0,23.7,19.0,17.9,
     19.5,22.2,25.0,28.1,30.3,32.4],
    1900, 2100,"births / 1000 persons / year",
    fupdate = "DYNAMO_Engine.time")

# Model fit (assuming minor increase of TFR before 1950)
# Note that the UN estimates assume the number of
# *registered live births* per woman; some births in
# the developing countries may be underreported or some
# children (e.g. girls in China) may be unregistered
TotalFertility = TableParametrization(
    "_032_TotalFertility",
    [5.05,5.05,5.05,5.07,5.09,5.11,5.13,5.13,5.09,5.07,
     5.05,4.90,4.96,5.01,4.72,4.16,3.71,3.52,3.23,2.87,2.68,2.60,2.54,2.49],
    1900, 2015,
    fupdate = "DYNAMO_Engine.time")

FertilityCorrection_WW2 = TableParametrization(
    "_232_FertilityCorrection_WW2",
    [1.0,0.9,0.9,1.0],
    1939, 1947,
    fupdate = "DYNAMO_Engine.time")

#
# Numerical data (1950-2015) from
# https://ourworldindata.org/fertility-rate
#
TotalFertility_OWID = TableParametrization(
    "_932_TotalFertility_OWID",
    [5.048,5.018,4.966,4.926,4.899,
     4.884,4.882,4.890,4.909,4.934,
     4.963,4.993,5.017,5.033,5.037,
     5.025,4.996,4.951,4.891,4.818,
     4.731,4.630,4.517,4.397,4.273,
     4.151,4.036,3.931,3.839,3.762,
     3.700,3.653,3.618,3.588,3.561,
     3.532,3.494,3.446,3.387,3.318,
     3.240,3.156,3.073,2.994,2.923,
     2.861,2.810,2.766,2.729,2.698,
     2.672,2.651,2.634,2.620,2.607,
     2.595,2.583,2.572,2.562,2.551,
     2.541,2.531,2.521,2.512,2.503,2.494],
    1950, 2015,
    fupdate = "DYNAMO_Engine.time")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.Produce_Solution_Path( verbose = False)
#DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=0.5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )
DYNAMO_Engine.ListEquations()

PlotTable( DYNAMO_Engine, AverageFertilityPeriod, 0, 10, "TFR [unitless]", show=GraphShow)

limits = (1900, 2100)
fig = plt.figure( figsize=(15,15))
fig.suptitle('Population "World3" as a function of LEB and TFR', fontsize=25)
gs = plt.GridSpec(3, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

yrCal, pCal, errCal = clb("../Global Data/Population_Calibration.csv",
                          ["Year", "Population", "Yerror"])
y, p0, p12, p3 = clb("./Calibrations/Age_Structure_UN.txt",
                     ["Year", "0_14", "15_64", "65_over"], separator="\t")
p0m = np.array(Population0To14.Data) * 1e-6
p1m = np.array(Population15To44.Data) * 1e-6
p2m = np.array(Population45To64.Data) * 1e-6
p3m = np.array(Population65AndOver.Data) * 1e-6
ax1.set_title("Population age structure", fontsize=18)
a = (p0m+p1m+p2m)*1e-3
ax1.plot( DYNAMO_Engine.Model_Time, a, "-", lw=2, color="m")
ax1.text( 2101, a[-1], "0-64")
a = (p0m+p1m)*1e-3
ax1.plot( DYNAMO_Engine.Model_Time, a, "-", lw=2, color="r")
ax1.text( 2101, a[-1], "0-44")
a = p0m*1e-3
ax1.plot( DYNAMO_Engine.Model_Time, a, "-", lw=2, color="g")
ax1.text( 2101, a[-1], "0-14")
ax1.errorbar( y, p0*1e-3, yerr=p0*5e-5, fmt=".", color="g", alpha=0.5, label="(UN actual)")
ax1.errorbar( y, (p0+p12)*1e-3, yerr=(p0+p12)*5e-5, fmt=".", color="m", alpha=0.5)
ax1.errorbar( yrCal, pCal*1e-3, yerr=errCal*1e-3, fmt=".", color="k", alpha=0.5)
ax1.plot( DYNAMO_Engine.Model_Time, np.array(Population.Data)/1e9, "-",
          lw=2, color="b", label="Population total (Calibrated)")
year_BH, LEB_BH, CBR_BH, CDR_BH, Pop_BH = clb("./Calibrations/BAU_Population_View_BHayes.txt",
        ["Year", "LEB", "BR_Crude", "DR_Crude", "Population"], separator="\t")
#ax1.plot( DYNAMO_Engine.Model_Time, np.array(Population_Check.Data)/1e9, "--",
#          lw=2, color="b", alpha=0.5, label='"World-3" 2003 in JS by Brian Hayes')
ax1.plot( year_BH, Pop_BH/1e3, "--",
          lw=2, color="b", alpha=0.5, label='"World-3" 2003 in JS by Brian Hayes')
ax1.set_ylabel("billion")
#ax1.set_xlim( 1895, 2025)
#ax1.set_ylim( 0, 8)
ax1.set_xlim( limits)
ax1.set_ylim( 0, 12)
ax1.grid(True)
ax1.legend(loc=0)

yLEB, LEB = clb("./Calibrations/Life_Expectancy_OWID.txt", ["Year", "LEB"], separator="\t")
yTFR, TFR = clb("./Calibrations/Fertility_Rate_OWID.txt", ["Year", "TFR"], separator="\t")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(LifeExpectancy.Data), "-",
          lw=2, color="m", label="LEB")
ax2.plot( DYNAMO_Engine.Model_Time, np.array(TotalFertility.Data)*10, "-",
          lw=2, color="g", label="TFR")
#ax2.plot( DYNAMO_Engine.Model_Time, np.array(LifeExpectancy_Check.Data)*0.8, "--",
#          lw=2, alpha=0.5, color="m")
ax2.plot( year_BH, LEB_BH, "--", lw=2, color="m", alpha=0.5)
ax2.errorbar( yLEB, LEB, yerr=2.5, fmt=".", color="r", alpha=0.5, label="(OWID own estimates)")
ax2.errorbar( yTFR, TFR*10, yerr=3, fmt=".", color="g", alpha=0.5)
ax2.set_xlim( limits)
ax2.set_ylim( 20, 80)
ax2.set_ylabel("LEB[years], TFR[x10]")
ax2.grid(True)
ax2.legend(loc=0)

y, br, ar = clb("./Calibrations/Attrition_Rate_UN.txt", ["Year", "BR_Crude", "AR_Crude"], separator="\t")
ax3.plot( DYNAMO_Engine.Model_Time, np.array(CrudeBirthRate.Data), "-",
          lw=2, color="g", label="Crude Birth Rate")
ax3.plot( DYNAMO_Engine.Model_Time, np.array(CrudeDeathRate.Data), "-",
          lw=2, color="r", label="Crude Death Rate")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(CrudeBirthRate_Check.Data), "--",
#          lw=2, alpha=0.5, color="g")
#ax3.plot( DYNAMO_Engine.Model_Time, np.array(CrudeDeathRate_Check.Data), "--",
#          lw=2, alpha=0.5, color="r")
ax3.plot( year_BH, CDR_BH, "--", lw=2, color="r", alpha=0.5)
ax3.plot( year_BH, CBR_BH, "--", lw=2, color="g", alpha=0.5)
ax3.errorbar( y, br, yerr=2, fmt=".", color="g", alpha=0.5, label="(Computed from OWID)")
ax3.errorbar( y, ar, yerr=2, fmt=".", color="r", alpha=0.5)
ax3.set_xlim( limits)
ax3.set_ylim( 0, 60)
ax3.grid(True)
ax3.legend(loc=0)
ax3.set_xlabel("Year")
ax3.set_ylabel("per 1000 population")
plt.savefig( "./Calibrations/Calibration_01.png")
plt.show()

#PlotVariable( _549_IndustrialOutputPerCapita_Reference, DYNAMO_Engine.Model_Time,
#    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
#    show=True)
