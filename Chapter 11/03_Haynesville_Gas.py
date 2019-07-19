from US_Utilities import *

name = "Хайнесвилль"
metric = True
Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual, WP, WA, YC, PC = GetGas(
    "Haynesville", "./Data/US03_Haynesville_Gas.csv", metric)

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча газа на месторождении " + name, fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

if metric:
    ax1.plot( Year, AEO2014, "--", lw=2, color='g', label="AEO2014 ({:.2f} 10¹² м³)".format(np.sum(AEO2014)/1000))
    ax1.plot( Year, AEO2015, "--", lw=2, color='b', label="AEO2015 ({:.2f} 10¹² м³)".format(np.sum(AEO2015)/1000))
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO2016 ({:.2f} 10¹² м³)".format(np.sum(AEO2016)/1000))
    ax1.plot( Year, Hughes2014, "-", lw=3, color='m', label="Hughes-2014 ({:.2f} 10¹² м³)".format(np.sum(Hughes2014)/1000))
    ax1.errorbar( YC, PC, yerr=PC*.05, fmt='o', color="k", label="Реальная EIA ({:.2f} 10¹² м³)".format(np.sum(PC)/1000))
    ax1.set_ylim( 0, 170)
    ax1.set_ylabel("Млрд м³ в год")
    #ax1.annotate("Пик добычи в январе 2012", xy=(2012, 72), xytext=(2025, 60), arrowprops=dict(facecolor='black', shrink=0.05))
else:
    ax1.plot( Year, AEO2014, "--", lw=2, color='g', label="AEO-2014 ({:.1f} tcf)".format(np.sum(AEO2014[21:])*0.365))
    ax1.plot( Year, AEO2015, "--", lw=2, color='b', label="AEO-2015 ({:.1f} tcf)".format(np.sum(AEO2015[21:])*0.365))
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO-2016 ({:.1f} tcf)".format(np.sum(AEO2016[21:])*0.365))
    ax1.plot( Year, Hughes2014, "-", lw=3, color='m', label="Hughes2014 ({:.1f} tcf)".format(np.sum(Hughes2014[21:])*0.365))
    ax1.errorbar( Year[:-24], Actual[:-24], yerr=Actual[:-24]*.05, fmt='o', color="k", label="Реальная")
    ax1.set_ylabel("Млрд кубических футов в сутки")

ax1.set_xlim( 2000, 2040)
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=0)

ax2.plot( Year, WP/1000, "--", lw=3, color='r', label="По плану")
ax2.errorbar( Year[:-24], WA[:-24]/1000, yerr=.1, fmt='o', color="k", label="Реальных")
ax2.set_xlim( 2000, 2040)
ax2.set_ylim( 0, 12)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( "Количество газовых скважин в эксплуатации")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_11_03.png")
if InteractiveModeOn: plt.show(True)
