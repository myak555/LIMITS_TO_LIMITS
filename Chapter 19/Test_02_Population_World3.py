from Predictions import *

P0 = Population()
BAU_1972 = Interpolation_BAU_1972()
P1 = Population_World3()
tfr = Linear_Combo()
tfr.Wavelets += [Sigmoid( x0=1975.000, s0=0.07740, left=5.400, right=2.350)]
tfr.Wavelets += [Hubbert( x0=1967.000, s0=0.29510, s1=0.24133, peak=0.631)]
tfr.Wavelets += [Hubbert( x0=1987.000, s0=0.43047, s1=0.43047, peak=0.211)]
tfr.Wavelets += [Hubbert( x0=1998.000, s0=0.53144, s1=0.31381, peak=-0.074)]
leb = Linear_Combo()
leb.Wavelets += [Sigmoid( x0=1965.000, s0=0.03183, left=28.000, right=80.5)]
leb.Wavelets += [Hubbert( x0=1960.656, s0=0.04239, s1=0.47351, peak=-1.814)]
leb.Wavelets += [Hubbert( x0=1977.095, s0=0.20179, s1=0.18345, peak=1.174)]
leb.Wavelets += [Hubbert( x0=1999.712, s0=0.34519, s1=0.34519, peak=-0.865)]
leb.Wavelets += [Hubbert( x0=1948, s0=0.05, s1=1, peak=-7)]

Year = []
Total = []
Births = []
Deaths = []
Pops = []
for i in range(1890, 2041):
    Year += [i]
    Total += [P1.Total]
    Births += [P1.nBirth]
    Deaths += [P1.nDeath]
    Pops += [(np.array(P1.Population_Male),np.array(P1.Population_Female))]
    P1.Compute_Next_Year(tfr.Compute(i), leb_male=leb.Compute(i), leb_female=leb.Compute(i)+2)
Year = np.array(Year)
Total = np.array(Total)
Absolute_Growth = np.array(Total)
Absolute_Growth[1:] -= Total[:-1] 
Absolute_Growth[0] = Absolute_Growth[1]
Relative_Growth = Absolute_Growth / Total * 100000
Births = np.array(Births)
Deaths = np.array(Deaths)
BirthRate = Births / Total * 100000
DeathRate = Deaths / Total * 100000
BirthRate[0] = BirthRate[1]
DeathRate[0] = DeathRate[1]
BAU_1972.Solve(Year)
BAU_1972.Birth_Rate = BAU_1972.Birth_Rate_U * 3700 / 0.845
BAU_1972.Absolute_Growth = np.array(BAU_1972.Population)
BAU_1972.Absolute_Growth[1:] -= BAU_1972.Population[:-1] 
BAU_1972.Absolute_Growth[0] = BAU_1972.Absolute_Growth[1]
BAU_1972.Relative_Growth = BAU_1972.Absolute_Growth / BAU_1972.Population * 100000
BAU_1972.Death_Rate = BAU_1972.Birth_Rate - BAU_1972.Relative_Growth

limits = 1890, 2040

fig = plt.figure( figsize=(15,10))
gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Тест демографической системы World3", fontsize=22)
ax1.plot( Year, Total, "-", lw=3, color="b", label="Модель")
ax1.plot( Year, BAU_1972.Population, ".", color="b",label="World3 1972 г")
ax1.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Yerr, fmt=".", color="k", label="Реальная (ООН)")
ax1.plot( [1972, 1972], [2000, 7000], "--", lw=2, color="k")
ax1.text( 1973, 3000, '"Пределы роста", 1972', color="k")
ax1.set_xlim( limits)
ax1.set_ylim( 0, 10000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( Year, Relative_Growth, "-", lw=2, color="b", label="Прирост")
ax2.plot( Year, BirthRate, "-", lw=2, color="g", label="Рождаемость")
ax2.plot( Year, DeathRate, "-", lw=2, color="r", label="Смертность")
ax2.plot( Year, BAU_1972.Birth_Rate, ".", color="g", label="World3 1972 г")
ax2.plot( Year, BAU_1972.Death_Rate, ".", color="r")
ax2.plot( Year, BAU_1972.Relative_Growth, ".", lw=2, color="b")
BAU_1972.Relative_Growth
ax2.set_xlim( limits)
ax2.set_ylim( 0, 4000)
ax2.set_ylabel("LEB")
ax2.set_xlabel("Год")
ax2.set_ylabel("на 100'000 населения")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_19_02.png")
if InteractiveModeOn: plt.show(True)
