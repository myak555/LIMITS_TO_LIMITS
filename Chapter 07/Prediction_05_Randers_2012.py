from Predictions import * 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Resources_Time, Resources_Coal, Resources_Oil, Resources_Gas, Resources_Nuclear, Resources_Renewable = Load_Calibration(
    "../Global Data/Energy_Calibration.csv",
    ["Year", "Coal", "Oil", "Gas", "Nuclear", "Renewable"])

Time_Ran, Coal_Ran, Oil_Ran, Gas_Ran, Nuclear_Ran, Renewable_Ran = Load_Calibration(
    "./Data/Randers_2052_World.csv",
    ["Year", "Coal", "Oil", "Gas", "Nuclear", "Renewable"])

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
URR_Coal = np.sum( BAU_2012.Coal)
URR_Oil = np.sum( BAU_2012.Oil)
URR_Gas = np.sum( BAU_2012.Gas)
URR_Nuclear = np.sum( BAU_2012.Nuclear)
URR_Renewable = np.sum( BAU_2012.Renewable)
Energy_Per_Capita_UN = BAU_2012.Energy * 1000 / UN_Med

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Энергетика NewWorld 2012 г', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BAU_2012.Time, BAU_2012.Coal, "-", lw=1, color="k")
ax1.plot( BAU_2012.Time, BAU_2012.Oil, "-", lw=1, color="g")
ax1.plot( BAU_2012.Time, BAU_2012.Gas, "-", lw=1, color="r")
ax1.plot( BAU_2012.Time, BAU_2012.Nuclear, "-", lw=1, color="m")
ax1.plot( BAU_2012.Time, BAU_2012.Renewable, "-", lw=1, color="b")
ax1.errorbar( Resources_Time, Resources_Coal, yerr=Resources_Coal*0.03, fmt='.', color="k",
              label="Каменный уголь(и торф): {:.0f} млрд toe".format(URR_Coal/1e3))
ax1.errorbar( Resources_Time, Resources_Oil, yerr=Resources_Oil*0.03, fmt='.', color="g",
              label="Нефть (битум и жидкости): {:.0f} млрд toe".format(URR_Oil/1e3))
ax1.errorbar( Resources_Time, Resources_Gas, yerr=Resources_Gas*0.03, fmt='.', color="r",
              label="Природный газ: {:.0f} млрд toe".format(URR_Gas/1e3))
ax1.errorbar( Resources_Time, Resources_Nuclear, yerr=Resources_Nuclear*0.03, fmt='.', color="m",
              label="Ядерная энергия: {:.0f} млрд toe".format(URR_Nuclear/1e3))
ax1.errorbar( Resources_Time, Resources_Renewable, yerr=Resources_Renewable*0.03, fmt='.', color="b",
              label="Возобновляемые и биотопливо: {:.0f} млрд toe".format(URR_Renewable/1e3))
ax1.grid(True)
ax1.set_ylabel("миллионов toe")
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 7000)
ax1.legend(loc=0)

ax2.set_title( "Душевое потребление")
ax2.plot( BAU_2012.Time, BAU_2012.Energy_PC*1000, ".", lw=3, color="y",
          label="Рандерс - 2012")
ax2.plot( BAU_2012.Time, Energy_Per_Capita_UN, "-", lw=1, color="y",
          label="По демографической модели ООН - 2019")
ax2.set_ylabel("кг/год")
ax2.set_xlabel("Годы")
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 2500)
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_07_05.png")
if InteractiveModeOn: plt.show(True)

