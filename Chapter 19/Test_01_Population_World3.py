from W3_Population_Test import *

P0 = Population()
P1 = Population_World3()

tfr = Linear_Combo()
tfr.Wavelets += [Sigmoid( x0=1975.000, s0=0.07740, left=5.400, right=2.350)]
tfr.Wavelets += [Hubbert( x0=1967.000, s0=0.29510, s1=0.24133, peak=0.631)]
tfr.Wavelets += [Hubbert( x0=1987.000, s0=0.43047, s1=0.43047, peak=0.211)]
tfr.Wavelets += [Hubbert( x0=1998.000, s0=0.53144, s1=0.31381, peak=-0.074)]
tfr.Wavelets += [Hubbert( x0=1955.000, s0=1.00000, s1=1.00000, peak=-0.057)]
tfr.Wavelets += [Hubbert( x0=1962.000, s0=1.00000, s1=1.00000, peak=0.048)]
tfr.Wavelets += [Hubbert( x0=1978.000, s0=1.00000, s1=1.00000, peak=-0.030)]
tfr.Wavelets += [Hubbert( x0=2014.000, s0=0.59049, s1=0.59049, peak=0.017)]
tfr.Wavelets += [Hubbert( x0=1955, s0=0.2, s1=0.09, peak=0.5)]

leb = Linear_Combo()
leb.Wavelets  = [Sigmoid( x0=1965.000, s0=0.03183, left=26.500, right=80.400)]
leb.Wavelets += [Hubbert( x0=1975.000, s0=0.18500, s1=0.13500, peak=1.632)]
leb.Wavelets += [Hubbert( x0=2000.000, s0=0.28000, s1=0.31000, peak=-1.000)]
leb.Wavelets += [Hubbert( x0=1961.000, s0=0.15009, s1=0.47500, peak=-1.700)]
leb.Wavelets += [Hubbert( x0=1948, s0=0.1, s1=1, peak=-7)]

Year = []
Total = []
TFR_Actual = []
LEB_Actual_Male = []
LEB_Actual_Female = []
LEB_Apparent_Male = []
LEB_Apparent_Female = []
Pops = []
Male_Female_Ratio = []
for i in range(1890, 2041):
    Year += [i]
    Total += [P1.Total]
    LEB_Actual_Male += [P1.LEB_True_Male]
    LEB_Actual_Female += [P1.LEB_True_Female]
    LEB_Apparent_Male += [P1.LEB_Apparent_Male]
    LEB_Apparent_Female += [P1.LEB_Apparent_Female]
    TFR_Actual += [P1.TFR]
    Male_Female_Ratio += [np.sum(P1.Population_Male)*100/np.sum(P1.Population_Female)]
    Pops += [(np.array(P1.Population_Male),np.array(P1.Population_Female))]
    P1.Compute_Next_Year(tfr.Compute(i), leb_male=leb.Compute(i)-2, leb_female=leb.Compute(i)+2)
Year = np.array(Year)
Total = np.array(Total)
LEB_Actual_Male[0] = LEB_Actual_Male[1]
LEB_Actual_Female[0] += LEB_Actual_Female[1]
Absolute_Growth = np.array(Total)
Absolute_Growth[1:] -= Total[:-1] 
Absolute_Growth[0] = Absolute_Growth[1]

limits = 1890, 2040

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 1, height_ratios=[2,1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title("Тест демографической системы World3", fontsize=22)
ax1.plot( Year, Total, "-", lw=3, color="b", label="Модель")
ax1.plot( Year, Absolute_Growth*100, "--", lw=2, color="g", label="Абсолютный прирост x 100")
ax1.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Yerr, fmt=".", color="k", label="Реальная (ООН)")
ax1.plot( [1914, 1918], [2150,2150], "-", lw=3, color="k")
ax1.text( 1913, 2200, 'ПМВ')
ax1.plot( [1939, 1945], [2700,2700], "-", lw=3, color="k")
ax1.text( 1939, 2750, 'ВМВ')
ax1.set_xlim( limits)
ax1.set_ylim( 0, 10000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

#ax2.plot( Year, Male_Female_Ratio, "-", lw=2, color="m", label="Отношение мужч.:женщ.")
ax2.plot( Year, LEB_Actual_Male, "-", lw=2, color="b", label="LEB, мужч.")
ax2.plot( Year, LEB_Apparent_Male, "--", lw=2, color="b")
ax2.plot( Year, LEB_Actual_Female, "-", lw=2, color="r", label="LEB, женщ.")
ax2.plot( Year, LEB_Apparent_Female, "--", lw=2, color="r", label="Кажущиеся")
ax2.plot( [1948, 1948], [20,60], "--", lw=1, color="k")
ax2.text( 1949, 19, '1948 - создание ВОЗ')
ax2.plot( [1945, 1969], [60,60], "-", lw=3, color="k")
ax2.text( 1940, 65, 'DDT против малярии')
ax2.plot( [1977, 1977], [30,70], "--", lw=1, color="k")
ax2.text( 1978, 29, '1977 - победа над оспой')
ax2.set_xlim( limits)
ax2.set_ylim( 0, 80)
ax2.set_ylabel("LEB")
ax2.grid(True)
ax2.legend(loc=0)

ax3.plot( Year, TFR_Actual, "-", lw=2, color="g", label="TFR")
ax3.plot( [1969, 1969], [1,5.5], "--", lw=1, color="k")
ax3.text( 1970, 0.8, '"Одна семья - два ребёнка" в КНР')
ax3.plot( [1979, 1979], [2,4.5], "--", lw=1, color="k")
ax3.text( 1980, 1.8, '"Одна семья - один ребёнок" в КНР')
ax3.plot( [2016, 2016], [2.5,3.5], "--", lw=1, color="k")
ax3.text( 1980, 4.0, 'Возврат к "Одна семья - два ребёнка"')
ax3.set_xlim( limits)
ax3.set_ylim( 0, 6)
ax3.set_xlabel("Год")
ax3.set_ylabel("TFR")
ax3.grid(True)

plt.savefig( "./Graphs/figure_19_01.png")
if InteractiveModeOn: plt.show(True)
