from Population import *
from Predictions import Interpolation_BAU_1972 
from Predictions import Interpolation_BAU_2012 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Time_Ran, Land_Ran = Load_Calibration( "Randers_2052.csv", "Year", "Land")
Food_Ran, Yield_Ran = Load_Calibration( "Randers_2052.csv", "Food", "Yield")

Time_Cal, Land_Cal = Load_Calibration( "Agriculture_Calibration.csv", "Year", "Cereal_Land")
Gross_Cal, Net_Cal = Load_Calibration( "Agriculture_Calibration.csv", "Gross_Food", "Net_Food")

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
Food_PP_1972 = BAU_1972.Food_PP * 0.93 * 3

BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
Food_PP_Randers = BAU_2012.Food / BAU_2012.Population * 1000 * 3
Food_PP_UN = BAU_2012.Food / UN_Med * 1000 * 3

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,15))

plt.plot( T, Food_PP_1972, "--", lw=2, color="y", label="Прод. на душу (BAU-1972) [кг/год x 3]")
plt.plot( BAU_2012.Time, Food_PP_Randers, ".", lw=3, color="y", label="Прод. на душу (Randers-2012) [кг/год  x 3]")
plt.plot( BAU_2012.Time, Food_PP_UN, "-", lw=2, color="y", label="Прод. на душу (ООН) [кг/год  x 3]")
plt.plot( BAU_2012.Time, BAU_2012.Land, "-", lw=1, color="k", label="Пашня [га]")
plt.plot( BAU_2012.Time, BAU_2012.Yield*1000, "--", lw=1, color="m", label="Урожайность [кг/га]")
plt.plot( BAU_2012.Time, BAU_2012.Food, "-", lw=3, color="g", label="Продовольствие [tge]")

plt.errorbar( Time_Cal, Land_Cal, yerr=Land_Cal*0.03, fmt='.', color="k", label="Пашня (ООН-2014) [га]")
plt.errorbar( Time_Cal, Net_Cal, yerr=Net_Cal*0.03, fmt='.', color="g", label="Продовольствие-нетто (ООН-2014) [tge]")
#plt.errorbar( Time_Ran, Land_Ran, yerr=Land_Ran*0.05, fmt='o', color="k")
#plt.errorbar( Time_Ran, Food_Ran, yerr=Food_Ran*0.05, fmt='o', color="g")
#plt.errorbar( Time_Ran, Yield_Ran*1000, yerr=Yield_Ran*0.05*1000, fmt='o', color="m")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов")
plt.ylim( 0, 15000)
plt.title( 'Сельское хозяйство NewWorld 2012 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_05.png")
fig.show()

