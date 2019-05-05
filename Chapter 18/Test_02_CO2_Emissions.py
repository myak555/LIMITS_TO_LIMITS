from Predictions import *
import scipy.stats as stat

#
# Calibrations
#
# Population
Pop = Population()
Pop.Solve(np.linspace( 1830, 2100, 271))
Pop_UN_Medium = Pop.UN_Medium.GetVector(Pop.Solution_Year)
Pop_UN_Medium5 = []
for i in range(155,len(Pop_UN_Medium), 5): 
    Pop_UN_Medium5 += [Pop_UN_Medium[i]/1000]

# CO2 emissions
YCO2, ECO2 = Load_Calibration( "CO2_Calibration.csv", "Year", "Total")
ECO2 /= 3660
YCO2 = YCO2[30:]
ECO2 = ECO2[30:]
filename = "./Data/IPCC_Emission_Scenarios.txt"
YIPCC, BaU = Load_Calibration( filename, "Year", "FAR_BaU", separator="\t")
FAR_B,FAR_C = Load_Calibration( filename, "FAR_B", "FAR_C", separator="\t")
FAR_D,IS92a = Load_Calibration( filename, "FAR_D", "IS92a", separator="\t")
IS92b,IS92c = Load_Calibration( filename, "IS92b", "IS92c", separator="\t")
IS92d,IS92e = Load_Calibration( filename, "IS92d", "IS92e", separator="\t")
IS92f,WRE1000 = Load_Calibration( filename, "IS92f", "WRE1000", separator="\t")

# Resources extraction
YRes, Res = Load_Calibration( "Resources_Calibration.csv", "Year", "Total")
Res_PC = Res / Pop.Calibration_Total[10:]
Res /= 1000
LTG72 = Interpolation_BAU_1972()
LTG72.Solve( np.linspace( 1970, 2100, 131))
LTG72_CO2 = LTG72.Energy / 1130
BaU_PC = BaU * 1.13 / Pop_UN_Medium5 
FAR_B_PC = FAR_B * 1.13 / Pop_UN_Medium5 
FAR_C_PC = FAR_C * 1.13 / Pop_UN_Medium5 
FAR_D_PC = FAR_D * 1.13 / Pop_UN_Medium5 
IS92a_PC = IS92a * 1.13 / Pop_UN_Medium5
IS92b_PC = IS92b * 1.13 / Pop_UN_Medium5
IS92c_PC = IS92c * 1.13 / Pop_UN_Medium5
IS92d_PC = IS92d * 1.13 / Pop_UN_Medium5
IS92e_PC = IS92e * 1.13 / Pop_UN_Medium5
IS92f_PC = IS92f * 1.13 / Pop_UN_Medium5

limits = 1950, 2100

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.set_title( "Сценарии IPCC по выбросам CO₂ (1990-1992 гг)", fontsize=22)
ax1.plot( LTG72.Time, LTG72_CO2, "-", lw=4, color="m", alpha=0.5, label="Пределы роста 1972 (базовый)")
ax1.plot( YIPCC, BaU, "-", lw=4, color="r", alpha=0.5, label="IPCC 1990")
ax1.text( 2101, BaU[-1], "A", color="r")
ax1.plot( YIPCC, FAR_B, "--", lw=3, color="r", alpha=0.2)
ax1.text( 2101, FAR_B[-1], "B", color="r")
ax1.plot( YIPCC, FAR_C, "-.", lw=3, color="r", alpha=0.2)
ax1.text( 2101, FAR_C[-1], "C", color="r")
ax1.plot( YIPCC, FAR_D, "-.", lw=2, color="r", alpha=0.2)
ax1.text( 2101, FAR_D[-1]-0.3, "D", color="r")
ax1.plot( YIPCC[1:], IS92a[1:], "--", lw=4, color="g", alpha=0.5)
ax1.text( 2101, IS92a[-1], "92a", color="g")
ax1.plot( YIPCC[1:], IS92b[1:], "-", lw=4, color="g", alpha=0.5, label="IPCC IS-1992")
ax1.text( 2101, IS92b[-1], "92b", color="g")
ax1.plot( YIPCC[1:], IS92c[1:], "-.", lw=3, color="g", alpha=0.2)
ax1.text( 2101, IS92c[-1], "92c", color="g")
ax1.plot( YIPCC[1:], IS92d[1:], "-", lw=2, color="g", alpha=0.2)
ax1.text( 2101, IS92d[-1]+1, "92d", color="g")
ax1.plot( YIPCC[1:], IS92e[1:], "--", lw=2, color="g", alpha=0.2)
ax1.text( 2085, 28.5, "92e", color="g")
ax1.plot( YIPCC[1:], IS92f[1:], "-.", lw=2, color="g", alpha=0.2)
ax1.text( 2101, IS92f[-1], "92f", color="g")
ax1.plot( [1990, 1990], [3, 15], "-", lw=2, color="y", alpha=0.5)
ax1.text( 1980, 16, "IPCC-1990")
ax1.errorbar( YCO2, ECO2, yerr=ECO2*0.15, fmt="o", color="k", label="Реальные (1830-2018)")
ax1.set_xlim( limits)
ax1.set_ylim( 0, 30)
ax1.set_yticks([5, 10, 15, 20, 25])
ax1.set_ylabel("млрд тонн углерода")
ax1.grid( True)
ax1.legend( loc=2)

ax2.set_title( "Потребление ископаемого топлива на душу населения", fontsize=22)
ax2.plot( LTG72.Time, LTG72.Energy_PC, "-", lw=4, color="m", alpha=0.5, label="Пределы роста 1972 (базовый)")
ax2.plot( YIPCC, BaU_PC, "-", lw=4, color="r", alpha=0.5, label="IPCC 1990")
ax2.text( 2101, BaU_PC[-1], "A", color="r")
ax2.plot( YIPCC, FAR_B_PC, "--", lw=3, color="r", alpha=0.2)
ax2.text( 2101, FAR_B_PC[-1], "B", color="r")
ax2.plot( YIPCC, FAR_C_PC, "-.", lw=3, color="r", alpha=0.2)
ax2.text( 2101, FAR_C_PC[-1], "C", color="r")
ax2.plot( YIPCC, FAR_D_PC, "-.", lw=2, color="r", alpha=0.2)
ax2.text( 2101, FAR_D_PC[-1]-0.05, "D", color="r")
ax2.plot( YIPCC[1:], IS92a_PC[1:], "--", lw=4, color="g", alpha=0.5)
ax2.text( 2101, IS92a_PC[-1], "92a", color="g")
ax2.plot( YIPCC[1:], IS92b_PC[1:], "-", lw=4, color="g", alpha=0.5, label="IPCC IS-1992")
ax2.text( 2101, IS92b_PC[-1], "92b", color="g")
ax2.plot( YIPCC[1:], IS92c_PC[1:], "-.", lw=3, color="g", alpha=0.2)
ax2.text( 2101, IS92c_PC[-1], "92c", color="g")
ax2.plot( YIPCC[1:], IS92d_PC[1:], "-", lw=2, color="g", alpha=0.2)
ax2.text( 2101, IS92d_PC[-1]+0.1, "92d", color="g")
ax2.plot( YIPCC[1:], IS92e_PC[1:], "--", lw=2, color="g", alpha=0.2)
ax2.text( 2085, 3.15, "92e", color="g")
ax2.plot( YIPCC[1:], IS92f_PC[1:], "-.", lw=2, color="g", alpha=0.2)
ax2.text( 2101, IS92f_PC[-1], "92f", color="g")

ax2.errorbar( YRes, Res_PC, yerr=Res_PC*0.25, fmt="o", color="k", label="Реальное (1830-2018)")
ax2.set_xlim( limits)
ax2.set_ylim( 0, 3.5)
ax2.set_ylabel("тонн нефтяного эквивалента в год")
ax2.set_yticks([1, 2, 3])
ax2.grid( True)
#ax2.legend( loc=0)
ax2.set_xlabel("год")

plt.savefig( ".\\Graphs\\figure_18_02.png")
fig.show()
