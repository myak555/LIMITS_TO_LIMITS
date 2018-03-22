from Predictions import * 

T = np.linspace( 1890, 2100, 211)
Time_Ran, Population_Ran = Load_Calibration( ".\Data\Randers_2052_World.csv", "Year", "Population")

P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
Difference = UN_Med - BAU_2012.Population 

for i in range( len( BAU_2012.Time)):
    print( "{:g}\t{:.1f}".format( BAU_2012.Time[i], BAU_2012.Population[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( BAU_1972.Time, BAU_1972.Population, "--", lw=1, color="b", label="World3 - 1972")
plt.plot( BAU_2012.Time, BAU_2012.Population, "-", lw=3, color="b", label="Рандерс - 2012")
plt.plot( T[125:], UN_Med[125:], "-", lw=2, color="g", label="Средняя оценка ООН - 2014")
plt.plot( T[100:], Difference[100:], "--", lw=2, color="r", label="Разница ООН-Рандерс")
plt.errorbar( Time_Ran, Population_Ran, fmt='o', color="b")
plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Yerr, fmt='.', color="k", label="Статистика ООН - 2014")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов")
plt.ylim( 0, 12000)
plt.title( 'Аппроксимация NewWorld 2012 г: Население')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_03.png")
fig.show()

