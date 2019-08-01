from Utilities import *

name = "Остальные"
metric = True

Year,AEO2014,AEO2015,AEO2016,Hughes2014,Actual,WP,WA = Load_Calibration(
    "./Data/US20_Others_Oil.csv",
    ["Year", "AEO2014", "AEO2015", "AEO2016", "Hughes2014", "Actual", "Wells_Plan", "Wells_Actual"])
YC,PC1,PC2,PC3,PC4,PC5,PC6,PC7 = Load_Calibration(
    "./Data/US22_US_Tight_Oil_EIA.csv",
    ["Year", "Monterey", "Granite_Wash", "Marcellus", "Haynesville", "Yeso_Glorieta", "Delaware", "Utica"],separator="\t")

PC = PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7

if metric:
    b2t = 0.159 * 0.827 
    bd2ty = b2t * 365 
    AEO2014 *= bd2ty    
    AEO2015 *= bd2ty   
    AEO2016 *= bd2ty   
    Hughes2014 *= bd2ty   
    Actual *= bd2ty   
    PC *= b2t
else:
    PC /= 365
YC = YC[:-2]
PC = PC[:-2]

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча нефти и конденсата на остальных и ещё не открытых месторождениях", fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

if metric:
    ax1.plot( Year, AEO2014, "--", lw=2, color='g', label="AEO2014 ({:.2f} 10⁹ т)".format(np.sum(AEO2014)/1000))
    ax1.plot( Year, AEO2015, "--", lw=2, color='b', label="AEO2015 ({:.2f} 10⁹ т)".format(np.sum(AEO2015)/1000))
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO2016 ({:.2f} 10⁹ т)".format(np.sum(AEO2016)/1000))
    #ax1.plot( Year, Hughes2014, "-", lw=3, color='m', label="Hughes-2014 ({:.2f} 10⁹ т)".format(np.sum(Hughes2014)/1000))
    ax1.errorbar( YC, PC, yerr=PC*.05, fmt='o', color="k", label="Реальная ({:.2f} 10⁹ т)".format(np.sum(PC)/1000))
    ax1.set_ylim( 0, 80)
    ax1.set_ylabel("Млн тонн в год")
    ax1.annotate("Пик добычи в марте 2015", xy=(2015, 16), xytext=(2020, 70), arrowprops=dict(facecolor='black', shrink=0.05))
    ax1.annotate("С 2018 года статистика не публикуется", xy=(2017.3, 12), xytext=(2020, 5), arrowprops=dict(facecolor='black', shrink=0.05))
else:
    ax1.plot( Year, AEO2014, "--", lw=2, color='g', label="AEO2014 ({:.1f} 10⁹ bbl)".format(np.sum(AEO2014[14:])*0.365))
    ax1.plot( Year, AEO2015, "--", lw=2, color='b', label="AEO2015 ({:.1f} 10⁹ bbl)".format(np.sum(AEO2015[14:])*0.365))
    ax1.plot( Year, AEO2016, "--", lw=2, color='r', label="AEO2016 ({:.1f} 10⁹ bbl)".format(np.sum(AEO2016[14:])*0.365))
    #ax1.plot( Year, Hughes2014, "-", lw=3, color='m', label="Hughes-2014 ({:.1f} 10⁹ bbl)".format(np.sum(Hughes2014[14:])*0.365))
    ax1.errorbar( YC, PC, yerr=PC*.05, fmt='o', color="k", label="Реальная")
    ax1.set_ylabel("Млн баррелей в сутки")

ax1.set_xlim( 2000, 2040)
ax1.grid(True)
ax1.set_title( "Добыча нефти и лицензионного конденсата")
ax1.legend(loc=0)

#ax2.plot( Year, WP/1000, "--", lw=3, color='r', label="По плану")
ax2.errorbar( Year[:-24], WA[:-24]/1000, yerr=.1, fmt='o', color="k", label="Реальных")
ax2.set_xlim( 2000, 2040)
ax2.set_ylim( 0, 8)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( "Количество скважин в эксплуатации")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_11_20.png")
if InteractiveModeOn: plt.show(True)
