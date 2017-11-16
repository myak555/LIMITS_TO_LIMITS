from Population import *
from Predictions import Interpolation_BAU_1972 
from Predictions import Interpolation_BAU_2012 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Time_Ran, GDP_Ran = Load_Calibration( "Randers_2052.csv", "Year", "GDP")
Prod_Ran, CO2_Ran = Load_Calibration( "Randers_2052.csv", "Labor_Prod", "CO2")
Time_CO2, CO2_Cal = Load_Calibration( "CO2_Mauna_Loa.csv", "Year", "Mean")

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
GDP_PP_1972 = BAU_1972.Industrial_PP * 7.5 / 365

BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
GDP_PP_Randers = BAU_2012.GDP / BAU_2012.Population * 1000000 / 365
GDP_PP_UN = BAU_2012.GDP / UN_Med * 1000000 / 365

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,15))

plt.plot( T, GDP_PP_1972, "--", lw=2, color="y", label="ВВП на душу (BAU-1972) [$/день]")
plt.plot( BAU_2012.Time, GDP_PP_Randers, ".", lw=3, color="y", label="ВВП на душу (Randers-2012) [$/день]")
plt.plot( BAU_2012.Time, GDP_PP_UN, "-", lw=2, color="y", label="ВВП на душу (ООН) [$/день]")
plt.plot( BAU_2012.Time, BAU_2012.Productivity/1000, "-", lw=1, color="k", label="Производительность труда [тыс $ / работника]")
plt.plot( BAU_2012.Time, BAU_2012.GDP, "-", lw=3, color="g", label="ВВП (Randers-2012) [млрд, $]")
plt.plot( BAU_2012.Time, BAU_2012.CO2/10, "--", lw=1, color="m", label="Уровень CO2 в атмосфере [ppm х 0.1]")

plt.errorbar( Time_CO2, CO2_Cal/10, yerr=CO2_Cal*0.005/10, fmt='.', color="m", label="Уровень CO2 на станции Мауна-Лоа [ppm х 0.1]")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("единиц")
plt.ylim( 0, 175)
plt.title( 'Валовый продукт NewWorld 2012 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_06.png")
fig.show()

