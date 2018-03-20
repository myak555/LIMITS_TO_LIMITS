from Predictions import * 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Time_Ran, GDP_Ran = Load_Calibration( ".\Data\Randers_2052_World.csv", "Year", "GDP")
CO2_Ran, Prod_Ran = Load_Calibration( ".\Data\Randers_2052_World.csv", "CO2", "Labor_Prod")
Time_GDP, GDP_Cal = Load_Calibration( ".\Data\GDP_World_Bank.csv", "Year", "GDP_2010")
Time_CO2, CO2_Cal = Load_Calibration( ".\Data\CO2_Mauna_Loa.csv", "Year", "Mean")

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
GDP_Per_Capita_UN = BAU_2012.GDP / UN_Med * 1e6 / 365

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Экономика NewWorld 2012 г', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BAU_2012.Time, BAU_2012.GDP, "-", lw=2, color="g")
ax1.plot( BAU_2012.Time, BAU_2012.CO2/10, "-", lw=1, color="k")
ax1.errorbar( Time_GDP, GDP_Cal, yerr=GDP_Cal*0.05, fmt='.', color="g", label="ВВП [трлн $(2010)]")
ax1.errorbar( Time_Ran, GDP_Ran, fmt='o', color="g", label="ВВП Рандерс [трлн $(2012)]")
ax1.errorbar( Time_CO2, CO2_Cal/10, fmt='.', color="y", label="CO₂ Мауна Лоа [ppm*0.1]")
ax1.grid(True)
ax1.set_ylabel("единиц")
ax1.set_xlim( 1900, 2100)
#ax1.set_ylim( 0, 12000)
ax1.legend(loc=0)

ax2.set_title( "Душевое ВВП (в день)")
ax2.plot( BAU_2012.Time, BAU_2012.Productivity, "--", lw=1, color="m", label="Производительность работника (Рандерс)")
ax2.plot( BAU_1972.Time, BAU_1972.GDP_PC, "--", lw=1, color="r", label="ВВП World3 - 1972")
ax2.plot( BAU_2012.Time, BAU_2012.GDP_PC, ".", lw=3, color="y", label="ВВП Рандерс - 2012")
ax2.plot( BAU_2012.Time, GDP_Per_Capita_UN, "-", lw=1, color="y", label="ВВП по демографической модели ООН - 2014")
ax2.set_ylabel("US$ 2012 годa")
ax2.set_xlabel("Годы")
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 100)
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_07_07.png")
fig.show()

