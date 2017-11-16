from Population import *
from Predictions import Interpolation_BAU_1972 
from Predictions import Interpolation_BAU_2012 
from Predictions import Interpolation_Realistic_2012 

T = np.linspace( 1890, 2100, 211)
Time_Ran, Population_Ran = Load_Calibration( "Randers_2052.csv", "Year", "Population")

P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)
UN_Low = P0.UN_Low.GetVector( T)

BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
NW_2012 = Interpolation_Realistic_2012()
NW_2012.Solve(T)
NW_2012.Correct_To_Actual( 1900, 2015)
Difference = UN_Med - NW_2012.Population 

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))

plt.plot( BAU_2012.Time, BAU_2012.Population, "--", lw=1, color="b", label="Население (Рандерс-2012) [млн]")
plt.plot( NW_2012.Time, NW_2012.Population, "-", lw=3, color="b", label="Население (NewWorld) [млн]")
plt.plot( T[125:], UN_Med[125:], "-", lw=2, color="g", label="Население (ООН-2010) [млн]")
plt.plot( T[125:], UN_Low[125:], "--", lw=2, color="g", label="Население - минимум (ООН-2010) [млн]")
plt.plot( T[100:], Difference[100:], "--", lw=3, color="r", label="Разница ООН-NewWorld [млн]")

plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Delta, fmt='.', color="k", label="Население (статистика ООН)")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов единиц")
plt.ylim( 0, 12000)
plt.title( 'NewWorld 2012 г с ограничением возобновляемой энергии и урожайности')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_14.png")
fig.show()

