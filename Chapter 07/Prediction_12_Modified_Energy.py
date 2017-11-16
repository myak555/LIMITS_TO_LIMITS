from Population import *
from Predictions import Interpolation_BAU_2012 
from Predictions import Interpolation_Realistic_2012 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Resources_Time, Resources_Coal = Load_Calibration( "Resources_Calibration.csv", "Year", "Coal")
Resources_Oil, Resources_Gas = Load_Calibration( "Resources_Calibration.csv", "Oil", "Gas")
Resources_Nuclear, Resources_Renewable = Load_Calibration( "Resources_Calibration.csv", "Nuclear", "Renewable")

Time_Ran, Coal_Ran = Load_Calibration( "Randers_2052.csv", "Year", "Coal")
Oil_Ran, Gas_Ran = Load_Calibration( "Randers_2052.csv", "Oil", "Gas")
Nuclear_Ran, Renewable_Ran = Load_Calibration( "Randers_2052.csv", "Nuclear", "Renewable")

BAU_2012 = Interpolation_Realistic_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2015)
URR_Coal = np.sum( BAU_2012.Coal)
URR_Oil = np.sum( BAU_2012.Oil)
URR_Gas = np.sum( BAU_2012.Gas)
URR_Nuclear = np.sum( BAU_2012.Nuclear)
Energy_Per_Capita_Randers = BAU_2012.Total_Energy * 1000 / BAU_2012.Population
Energy_Per_Capita_UN = BAU_2012.Total_Energy * 1000 / UN_Med

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))

plt.plot( BAU_2012.Time, BAU_2012.Coal, "-", lw=1, color="k")
plt.plot( BAU_2012.Time, BAU_2012.Oil, "-", lw=1, color="g")
plt.plot( BAU_2012.Time, BAU_2012.Gas, "-", lw=1, color="r")
plt.plot( BAU_2012.Time, BAU_2012.Nuclear, "-", lw=1, color="m")
plt.plot( BAU_2012.Time, BAU_2012.Renewable, "-", lw=1, color="b")
plt.plot( BAU_2012.Time, Energy_Per_Capita_Randers, ".", lw=3, color="y", label="Энергия на душу населения (NewWorld) [кг/год]")
plt.plot( BAU_2012.Time, Energy_Per_Capita_UN, "-", lw=1, color="y", label="Энергия на душу населения (ООН) [кг/год]")

plt.errorbar( Resources_Time, Resources_Coal, yerr=Resources_Coal*0.03, fmt='.', color="k", label="Каменный уголь(и торф): {:5.1f} млрд toe".format(URR_Coal/1e3))
plt.errorbar( Resources_Time, Resources_Oil, yerr=Resources_Oil*0.03, fmt='.', color="g", label="Нефть (битум и жидкости): {:5.1f} млрд toe".format(URR_Oil/1e3))
plt.errorbar( Resources_Time, Resources_Gas, yerr=Resources_Gas*0.03, fmt='.', color="r", label="Природный газ: {:5.1f} млрд toe".format(URR_Gas/1e3))
plt.errorbar( Resources_Time, Resources_Nuclear, yerr=Resources_Nuclear*0.03, fmt='.', color="m", label="Ядерная энергия: {:5.1f} млрд toe".format(URR_Nuclear/1e3))
plt.errorbar( Resources_Time, Resources_Renewable, yerr=Resources_Renewable*0.03, fmt='.', color="b", label="Возобновляемые (и биотопливо)")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов toe")
plt.ylim( 0, 8000)
plt.title( 'NewWorld 2012 г с ограничением возобновляемых источников')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_12.png")
fig.show()

