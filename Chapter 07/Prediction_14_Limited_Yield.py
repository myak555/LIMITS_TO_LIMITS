from Predictions import * 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

Calibration_Time, Calibration_Land, Calibration_Gross, Calibration_Net = Load_Calibration(
    "Agriculture_Calibration.csv",
    ["Year", "Cereal_Land", "Gross_Food", "Net_Food"])

Time_Ran, Land_Ran, Food_Ran, Yield_Ran = Load_Calibration(
    ".\Data\Randers_2052_World.csv",
    ["Year", "Land", "Food", "Yield"])

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_1972.Food_PC *= 508.0 / 1034.0
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
BAU_2012_Realistic = Interpolation_Realistic_2012()
BAU_2012_Realistic.Solve(T)
BAU_2012_Realistic.Correct_To_Actual( 1900, 2012)
Food_Per_Capita_UN = BAU_2012_Realistic.Food * 1000 / UN_Med

##for i in range( 2050, 2101):
##    print( BAU_2012_Realistic.Food[i-1800]/.5)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Сельское хозяйство NewWorld 2012 г с ограничением по урожайности', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.Food, "-", lw=2, color="g")
ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.Yield*1000, "-", lw=1, color="m")
ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.Land, "-", lw=1, color="k")
ax1.errorbar( Calibration_Time, Calibration_Net, yerr=Calibration_Net*0.05, fmt='.', color="g", label="Продовольствие [млн тонн]")
ax1.errorbar( Calibration_Time, Calibration_Net/Calibration_Land*1000, fmt='.', color="m", label="Урожайность [кг/га]")
ax1.errorbar( Calibration_Time, Calibration_Land, yerr=Calibration_Land*0.03, fmt='.', color="k", label="Пашня [млн га]")
ax1.grid(True)
ax1.set_ylabel("единиц")
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 10000)
ax1.legend(loc=0)

ax2.set_title( "Душевое потребление")
ax2.plot( BAU_1972.Time, BAU_1972.Food_PC*1000, "--", lw=1, color="r", label="World3 - 1972")
ax2.plot( BAU_2012.Time, BAU_2012_Realistic.Food / BAU_2012.Population*1000, ".", lw=3, color="y", label="По демографической модели Рандерса - 2012")
ax2.plot( BAU_2012.Time, Food_Per_Capita_UN, "-", lw=1, color="y", label="По демографической модели ООН - 2014")
ax2.set_ylabel("кг/год")
ax2.set_xlabel("Годы")
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 1250)
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_07_14.png")
fig.show()

