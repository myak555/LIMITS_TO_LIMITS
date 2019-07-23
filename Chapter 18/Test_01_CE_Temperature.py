from Utilities import *

#
# Calibrations
#
Y_CET, T_CET, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec = Load_Calibration(
    "./Data/Central_England_Temperature_Dataset.txt",
    ["Year", "YEAR_Average", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
    separator='\t')
Y_LD, CO2_LD = Load_Calibration("../Global Data/Ice_Core_Law_Dome.csv", ["Year", "Total"])
Y_ML, CO2_ML = Load_Calibration("../Global Data/CO2_Mauna_Loa.csv", ["Year", "Mean"])

baseline = np.average(T_CET[:1750-1659])
dT_CET = T_CET - baseline
dT_CET_30 = Filter( dT_CET, matrix=np.ones(31)) 
T_LD = np.log( CO2_LD/CO2_LD[0])/np.log(2) * 1.5 
T_ML = np.log( CO2_ML/CO2_LD[0])/np.log(2) * 1.5 

limits = 1600, 2020

fig = plt.figure( figsize=(15,15))
#fig.suptitle( "Климат Центральной Англии (1659-2018 гг)", fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.set_title( "Климат Центральной Англии (1659-2018 гг)", fontsize=22)
ax1.plot( Y_CET, T_CET, "-", lw=4, color="k", label="Сред")
ax1.plot( Y_CET, Jan, ".", color="b", alpha=0.5, label="Зима")
ax1.plot( Y_CET, Feb, ".", color="b", alpha=0.5)
ax1.plot( Y_CET, Mar, ".", color="g", alpha=0.5, label="Весна")
ax1.plot( Y_CET, Apr, ".", color="g", alpha=0.5)
ax1.plot( Y_CET, May, ".", color="g", alpha=0.5)
ax1.plot( Y_CET, Jun, ".", color="r", alpha=0.5, label="Лето")
ax1.plot( Y_CET, Jul, ".", color="r", alpha=0.5)
ax1.plot( Y_CET, Aug, ".", color="r", alpha=0.5)
ax1.plot( Y_CET, Sep, ".", color="y", alpha=0.5, label="Осень")
ax1.plot( Y_CET, Oct, ".", color="y", alpha=0.5)
ax1.plot( Y_CET, Nov, ".", color="y", alpha=0.5)
ax1.plot( Y_CET, Dec, ".", color="b", alpha=0.5)
ax1.plot( [limits[0], limits[1]], [baseline, baseline], "--", lw=2, color="k")
ax1.set_xlim( limits)
ax1.set_ylabel("ºЦ")
ax1.set_yticks([-5, 0, 5, 10, 15, 20])
ax1.grid( True)
ax1.legend( loc=2)

ax2.plot( Y_CET, dT_CET, "-", lw=1, color="k", label="От среднего 1659-1750 гг")
ax2.plot( Y_CET, dT_CET_30, "-", lw=3, color="k", label="Осреднение 31 год")
ax2.plot( Y_LD, T_LD+0.2, "-", lw=3, color="r", label="Эффект Каллендара")
ax2.plot( Y_ML, T_ML+0.2, "-", lw=3, color="r")
ax2.plot( [1936, 1936], [-2, 2], "--", lw=2, color="m")
ax2.text( 1940, -1, "Коллоквиум 1936 г")
ax2.set_yticks([-2, -1, 0, 1, 2])
ax2.set_xlim( limits)
ax2.set_ylim( -2, 2)
ax2.set_ylabel("ºЦ")
ax2.grid( True)
ax2.legend( loc=2)
ax2.set_xlabel("год")

plt.savefig( "./Graphs/figure_18_01.png")
if InteractiveModeOn: plt.show(True)
