from Utilities import *

Year,Nwells_P, Nwells_A, UTUR2011, AEO2014, AEO2015, AEO2016, Hughes_2014, Year,Actual = Load_Calibration(
    "./Data/US00_Barnett_Production_Data.csv",
    ["Year", "Nwells_Plan", "Nwells_Actual", "UTUR2011", "AEO2014", "AEO2015", "AEO2016", "Hughes_2014", "Year", "Actual"]) 

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Предсказания добычи месторождения Барнетт', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( Year[:-10], UTUR2011[:-10]/1000, "-", lw=2, color='k', label="UTUR-2011")
ax1.plot( Year, AEO2014/1000, "--", lw=2, color='g', label="AEO-2014")
ax1.plot( Year, AEO2015/1000, "--", lw=2, color='b', label="AEO-2015")
ax1.plot( Year, AEO2016/1000, "--", lw=2, color='r', label="AEO-2016")
ax1.plot( Year, Hughes_2014/1000, "-", lw=3, color='m', label="Hughes-2014")
ax1.errorbar( Year, Actual/1000, yerr=0.2, fmt='o', color="k", label="Реальная")
ax1.set_xlim( 1995, 2040)
ax1.set_ylim( 0, 6)
ax1.set_ylabel("Млрд кубических футов в сутки")
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=0)

ax2.plot( Year, Nwells_P/1000, "--", lw=3, color='r', label="По плану")
ax2.errorbar( Year[7:-24], Nwells_A[7:-24]/1000, yerr=2, fmt='o', color="k", label="Реальных")
ax2.annotate("Вывод скважин превысил ввод новых", xy=(2013, 16), xytext=(2015, 10), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.set_xlim( 1995, 2040)
ax2.set_ylim( 0, 30)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( "Количество газовых скважин в эксплуатации")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_10_03.png")
if InteractiveModeOn: plt.show(True)
