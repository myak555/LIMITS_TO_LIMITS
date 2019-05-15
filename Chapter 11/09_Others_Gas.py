from Utilities import *

name = "Остальные и Антрим"
metric = True

Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual = Load_Calibration(
    "./Data/US09_Others_Gas.csv",
    ["Year", "AEO2014", "AEO2015", "AEO2016", "Hughes2014", "Actual"])
YC,PC,PA,PP = Load_Calibration(
    "./Data/US12_US_Tight_Gas_EIA.csv",
    ["Year", "RestUS", "Antrim", "Permian"])
PC += PA
PC += PP

AntrimY = np.linspace(2000, 2015, 16)
AntrimP = np.array([
    5.021,4.812,4.583,4.222,4.089,3.899,3.842,3.747,
    3.518,3.385,3.176,3.024,2.796,2.587,2.472,2.396])

if metric:
    ft2m = 0.3048**3
    AEO2014 *= ft2m   
    AEO2015 *= ft2m   
    AEO2016 *= ft2m   
    Hughes2014 *= ft2m   
    Actual *= ft2m   
    AEO2014 *= 365   
    AEO2015 *= 365   
    AEO2016 *= 365   
    Hughes2014 *= 365   
    Actual *= 365   

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча газа на месторождении Антрим и "прочих"', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

if metric:
    ax1.plot( Year, AEO2014, "--", lw=2, color='g', label="AEO2014 ({:.2f} 10¹² м³)".format(np.sum(AEO2014)/1000))
    ax1.plot( Year, AEO2015, "--", lw=2, color='b', label="AEO2015 ({:.2f} 10¹² м³)".format(np.sum(AEO2015)/1000))
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO2016 ({:.2f} 10¹² м³)".format(np.sum(AEO2016)/1000))
    ax1.plot( Year, Hughes2014, "-", lw=3, color='m', label="Hughes-2014 ({:.2f} 10¹² м³)".format(np.sum(Hughes2014)/1000))
    ax1.errorbar( Year[:-24], Actual[:-24], yerr=Actual[:-24]*.05, fmt='o', color="k", label="Реальная EIA ({:.2f} 10¹² м³)".format(np.sum(Actual[:-24])/1000))
    ax1.errorbar( YC, PC, yerr=PC*.05, fmt='o', color="r", label="После коррекции 2017 года")
    ax1.set_ylim( 0, 150)
    ax1.set_ylabel("Млрд м³ в год")
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
ax1.legend(loc=2)

ax2.errorbar( AntrimY, AntrimP, yerr=.1, fmt='o', color="k", label="Данные Э.Мартина")
ax2.errorbar( YC, PA, yerr=.1, fmt='o', color="r", label="Данные EIA")
ax2.set_xlim( 2000, 2040)
ax2.set_ylim( 0, 6)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млрд м³ в год")
ax2.grid(True)
ax2.set_title( "Реальная добыча на месторождении Антрим")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_11_09.png")
fig.show()
