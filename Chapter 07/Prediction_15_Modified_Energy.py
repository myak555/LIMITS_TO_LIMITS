from Population import *
from Predictions import Interpolation_BAU_2012 
from Predictions import Interpolation_Realistic_2012 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Time_Ran, GDP_Ran = Load_Calibration( "Randers_2052.csv", "Year", "GDP")
Prod_Ran, CO2_Ran = Load_Calibration( "Randers_2052.csv", "Labor_Prod", "CO2")

BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
NW_2012 = Interpolation_Realistic_2012()
NW_2012.Solve(T)
NW_2012.Correct_To_Actual( 1900, 2010)
GDP_PP_Randers = NW_2012.GDP / NW_2012.Population * 1000000 / 365
GDP_PP_UN = NW_2012.GDP / UN_Med * 1000000 / 365

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))

plt.plot( BAU_2012.Time, GDP_PP_Randers, ".", lw=3, color="y", label="ВВП на душу (NewWorld) [$/день]")
plt.plot( BAU_2012.Time, GDP_PP_UN, "-", lw=2, color="y", label="ВВП на душу (ООН) [$/день]")
plt.plot( NW_2012.Time, NW_2012.Productivity/1000, "-", lw=1, color="k", label="Производительность труда [тыс $ / работника]")
plt.plot( BAU_2012.Time[200:], BAU_2012.GDP[200:], "--", lw=1, color="g", label="ВВП (Randers-2012) [млрд, $]")
plt.plot( NW_2012.Time, NW_2012.GDP, "-", lw=3, color="g", label="ВВП (NewWorld) [млрд, $]")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("единиц")
#plt.ylim( 0, 175)
plt.title( 'Валовый продукт NewWorld 2012 г с ограничениями')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_15.png")
fig.show()

