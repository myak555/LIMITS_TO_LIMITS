from Predictions import * 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Time_Ran, GDP_Ran = Load_Calibration(
    "./Data/Randers_2052_World.csv", ["Year", "GDP"])
Time_GDP, GDP_Cal, Pop_GDP, GDPPC_Cal = Load_Calibration(
    "../Global Data/GDP_World_Bank.csv",
    ["Year", "GDP_IA", "Population", "GDP_per_capita"])

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
BAU_2012_Realistic = Interpolation_Realistic_2012()
BAU_2012_Realistic.Solve(T)
BAU_2012_Realistic.Correct_To_Actual( 1900, 2018)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Экономика NewWorld 2012 г с ограничениями по ВИЭ и урожайности', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title( "Абсолютные значения")
ax1.plot( BAU_2012.Time, BAU_2012.GDP, "--", lw=1, color="r", label="Рандерс - 2012")
ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.GDP, "-", lw=2, color="r", label="С ограничениями по ВИЭ/Урожайности")
ax1.errorbar( Time_GDP, GDP_Cal, yerr=GDP_Cal*0.05, fmt='.', color="g", label="Реальный (World Bank)")
ax1.grid(True)
ax1.set_ylabel("трлн $(2010)")
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 150)
ax1.legend(loc=0)

ax2.set_title( "ВВП на душу населения в день")
ax2.plot( BAU_1972.Time, BAU_1972.GDP_PC, "--", lw=1, color="b", label="World3 - 1972")
ax2.plot( BAU_2012.Time, BAU_2012.GDP_PC, "-.", lw=1, color="y", label="Рандерс - 2012")
ax2.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.GDP_PC, "-", lw=3, color="r", label="С ограничениями по ВИЭ/Урожайности")
ax2.errorbar( Time_GDP, GDPPC_Cal, yerr=GDPPC_Cal*0.1, fmt='.', color="g", label="Реальный")
ax2.set_ylabel("US$ 2010 годa")
ax2.set_xlabel("Годы")
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 50)
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_07_16.png")
if InteractiveModeOn: plt.show(True)

