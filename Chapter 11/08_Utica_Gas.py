from Utilities import *

name = "Ютика"
metric = True

Year, AEO2016, Yakimov2017, Actual, WP, WA = Load_Calibration(
    "./Data/US08_Utica_Gas.csv",
    ["Year", "AEO2016", "Yakimov2017", "Actual", "Wells_Plan", "Wells_Actual"])
YC,PC = Load_Calibration( "./Data/US12_US_Tight_Gas_EIA.csv", ["Year", "Utica"])

if metric:
    ft2m = 0.3048**3
    AEO2016 *= ft2m   
    Yakimov2017 *= ft2m   
    Actual *= ft2m   
    AEO2016 *= 365   
    Yakimov2017 *= 365   
    Actual *= 365   

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча газа на месторождении " + name, fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

if metric:
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO2016 ({:.2f} 10¹² м³)".format(np.sum(AEO2016)/1000))
    ax1.plot( Year, Yakimov2017, "-", lw=3, color='m', label="Yakimov-2017 ({:.2f} 10¹² м³)".format(np.sum(Yakimov2017)/1000))
    ax1.errorbar( YC, PC, yerr=PC*.05, fmt='o', color="k", label="Реальная EIA ({:.2f} 10¹² м³)".format(np.sum(PC)/1000))
    #ax1.set_ylim( 0, 80)
    ax1.set_ylabel("Млрд м³ в год")
    ax1.annotate("Пик добычи после 2020", xy=(2020, 55), xytext=(2005, 90), arrowprops=dict(facecolor='black', shrink=0.05))
else:
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO-2016 ({:.1f} tcf)".format(np.sum(AEO2016[21:])*0.365))
    ax1.plot( Year, Yakimov2017, "-", lw=3, color='m', label="Yakimov-2017 ({:.0f} tcf)".format(np.sum(Yakimov2017[14:])*0.365))
    ax1.errorbar( Year[:-24], Actual[:-24], yerr=Actual[:-24]*.05, fmt='o', color="k", label="Реальная")
    ax1.set_ylabel("Млрд кубических футов в сутки")

ax1.set_xlim( 2000, 2040)
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=2)

ax2.plot( Year, WP/1000, "--", lw=3, color='r', label="По плану")
ax2.errorbar( Year[:-24], WA[:-24]/1000, yerr=.1, fmt='o', color="k", label="Реальных")
ax2.set_xlim( 2000, 2040)
ax2.set_ylim( 0, 15)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( "Количество газовых скважин в эксплуатации")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_11_08.png")
if InteractiveModeOn: plt.show(True)
