from Predictions import *
import scipy.stats as stat

#
# Calibrations
#
# Population
Pop = Population()
Pop.Solve(np.linspace( 1830, 2200, 371))
Pop_UN_Medium = Pop.UN_Medium.GetVector(Pop.Solution_Year)
Pop_UN_Medium5 = []
for i in range(155,len(Pop_UN_Medium)-100, 5): 
    Pop_UN_Medium5 += [Pop_UN_Medium[i]/1000]
    #print( Pop.Solution_Year[i], Pop_UN_Medium5[-1])
Pop_UN_Medium2000 = []
for i in range(170,len(Pop_UN_Medium), 5): 
    Pop_UN_Medium2000 += [Pop_UN_Medium[i]/1000]
    #print( Pop.Solution_Year[i], Pop_UN_Medium2000[-1])

# CO2 emissions
YCO2, ECO2 = Load_Calibration( "../Global Data/CO2_Calibration.csv", ["Year", "Total"])
ECO2 /= 3660
YCO2 = YCO2[30:]
ECO2 = ECO2[30:]
filename = "./Data/IPCC_Emission_Scenarios.txt"
YIPCC, SRES_A1F, SRES_A1B, SRES_B1, SRES_A1T, SRES_B2 = Load_Calibration(
    "./Data/IPCC_Emission_Scenarios.txt",
    ["Year", "SRES_A1F", "SRES_A1B", "SRES_B1","SRES_A1T", "SRES_B2"], separator="\t")
YearRCP, RCP_8_5, RCP_6_0, RCP_4_5, RCP_2_6 = Load_Calibration(
    "./Data/IPCC_Emission_Scenarios_RCP.txt",
    ["Year", "RCP_8_5", "RCP_6", "RCP_4_5", "RCP_2_6"],
    separator="\t")

# Resources extraction
YRes, Res = Load_Calibration( "../Global Data/Resources_Calibration.csv", ["Year", "Total"])
Res_PC = Res / Pop.Calibration_Total[10:-1]
Res /= 1000
Randers2012 = Interpolation_BAU_2012()
Randers2012.Solve( np.linspace( 2000, 2200, 201))
Randers2012_CO2 = Randers2012.Coal+Randers2012.Oil+Randers2012.Gas
(Randers2012.Energy-Randers2012.Nuclear-Randers2012.Renewable) / 1130
Randers2012_PC = Randers2012_CO2 / Pop_UN_Medium[170:] 
Randers2012_CO2 /= 1130
SRES_A1F_PC = SRES_A1F * 1.13 / Pop_UN_Medium5 
SRES_A1B_PC = SRES_A1B * 1.13 / Pop_UN_Medium5 
SRES_B1_PC = SRES_B1 * 1.13 / Pop_UN_Medium5 
SRES_A1T_PC = SRES_A1T * 1.13 / Pop_UN_Medium5 
SRES_B2_PC = SRES_B2 * 1.13 / Pop_UN_Medium5 
RCP_8_5_PC = RCP_8_5 * 1.13 / Pop_UN_Medium2000
RCP_6_0_PC = RCP_6_0 * 1.13 / Pop_UN_Medium2000
RCP_4_5_PC = RCP_4_5 * 1.13 / Pop_UN_Medium2000
RCP_2_6_PC = RCP_2_6 * 1.13 / Pop_UN_Medium2000

limits = 1950, 2200

fig = plt.figure( figsize=(15,15))
#fig.suptitle( "Test 02", fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.set_title( "Сценарии IPCC по выбросам CO₂ (2000-2013 гг)", fontsize=22)
ax1.plot( Randers2012.Time, Randers2012_CO2, "-", lw=4, color="m", alpha=0.5, label="Й.Рандерс 2012 (базовый)")
ax1.plot( YIPCC[3:], SRES_A1F[3:], "--", lw=3, color="r", alpha=0.2)
ax1.text( 2101, 29, "A1F", color="r")
ax1.plot( YIPCC[3:], SRES_A1B[3:], "-.", lw=3, color="r", alpha=0.2)
ax1.text( 2101, SRES_A1B[-1], "A1B", color="r")
ax1.plot( YIPCC[3:], SRES_B1[3:], "--", lw=3, color="r", alpha=0.5)
ax1.text( 2101, SRES_B1[-1], "B1", color="r")
ax1.plot( YIPCC[3:], SRES_A1T[3:], "-", lw=4, color="r", alpha=0.5, label="IPCC SRES 2000-2005")
ax1.text( 2101, SRES_A1T[-1]-1, "A1T", color="r")
ax1.plot( YearRCP, RCP_8_5, "-.", lw=3, color="g", alpha=0.2)
ax1.text( 2201, RCP_8_5[-1], "8.5", color="g")
ax1.plot( YearRCP, RCP_6_0, "--", lw=3, color="g", alpha=0.2)
ax1.text( 2201, RCP_6_0[-1], "6", color="g")
ax1.plot( YearRCP, RCP_4_5, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax1.text( 2201, RCP_4_5[-1]-1, "4.5", color="g")
ax1.plot( YearRCP, RCP_2_6, "--", lw=4, color="g", alpha=0.2)
ax1.text( 2075, 1, "2.6", color="g")
ax1.plot( [2013, 2013], [5, 15], "-", lw=2, color="y", alpha=0.5)
ax1.text( 2007, 16, "IPCC-2013")
ax1.errorbar( YCO2, ECO2, yerr=ECO2*0.15, fmt="o", color="k", label="Реальные (1830-2018)")
ax1.set_xlim( limits)
ax1.set_ylim( 0, 30)
ax1.set_yticks([5, 10, 15, 20, 25])
ax1.set_ylabel("млрд тонн углерода")
ax1.grid( True)
ax1.legend( loc=2)

ax2.set_title( "Потребление ископаемого топлива на душу населения", fontsize=22)
ax2.plot( Randers2012.Time, Randers2012_PC, "-", lw=4, color="m", alpha=0.5, label="Й.Рандерс 2012 (базовый)")
ax2.plot( YIPCC[3:], SRES_A1F_PC[3:], "--", lw=3, color="r", alpha=0.5)
ax2.text( 2101, SRES_A1F_PC[-1], "A1F", color="r")
ax2.plot( YIPCC[3:], SRES_A1B_PC[3:], "-.", lw=3, color="r", alpha=0.2)
ax2.text( 2101, SRES_A1B_PC[-1], "A1B", color="r")
ax2.plot( YIPCC[3:], SRES_B1_PC[3:], "--", lw=3, color="r", alpha=0.5)
ax2.text( 2101, SRES_B1_PC[-1], "B1", color="r")
ax2.plot( YIPCC[3:], SRES_A1T_PC[3:], "-", lw=4, color="r", alpha=0.5, label="IPCC SRES 2000-2005")
ax2.text( 2101, SRES_A1T_PC[-1]-0.1, "A1T", color="r")
ax2.plot( YearRCP, RCP_8_5_PC, "-.", lw=3, color="g", alpha=0.2)
ax2.text( 2201, RCP_8_5_PC[-1], "8.5", color="g")
ax2.plot( YearRCP, RCP_6_0_PC, "--", lw=3, color="g", alpha=0.2)
ax2.text( 2201, RCP_6_0_PC[-1], "6", color="g")
ax2.plot( YearRCP, RCP_4_5_PC, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax2.text( 2201, RCP_4_5_PC[-1]-0.1, "4.5", color="g")
ax2.plot( YearRCP, RCP_2_6_PC, "--", lw=4, color="g", alpha=0.2)
ax2.text( 2075, 0.1, "2.6", color="g")
ax2.errorbar( YRes, Res_PC, yerr=Res_PC*0.25, fmt="o", color="k", label="Реальное (1830-2018)")
ax2.set_xlim( limits)
ax2.set_ylim( 0, 3.5)
ax2.set_ylabel("тонн нефтяного экв. в год")
ax2.set_yticks([1, 2, 3])
ax2.grid( True)
#ax2.legend( loc=0)
ax2.set_xlabel("год")

plt.savefig( "./Graphs/figure_18_03.png")
if InteractiveModeOn: plt.show(True)
