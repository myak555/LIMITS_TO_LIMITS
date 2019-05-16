from Predictions import * 

T = np.linspace( 1800, 2200, 401)
P0 = Population()
UN_Medium = P0.UN_Medium.GetVector( T)
UN_Low = P0.UN_Low.GetVector( T)

Calibration_Time, Calibration_Net = Load_Calibration(
    "Agriculture_Calibration.csv", ["Year", "Net_Food"])
Calibration_Year, Calibration_Pop = Load_Calibration(
    "Population_Calibration.csv", ["Year", "Population"])

BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
BAU_2012.Correct_To_Actual( 1900, 2010)
BAU_2012_Realistic = Interpolation_Realistic_2012()
BAU_2012_Realistic.Solve(T)
BAU_2012_Realistic.Correct_To_Actual( 1900, 2012)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Население NewWorld 2012 г с ограничениями по ВИЭ и урожайности', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title( "Население и продовольствие")
ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.Food, "-", lw=2, color="g")
ax1.plot( BAU_2012_Realistic.Time, BAU_2012_Realistic.Population, "-", lw=2, color="b")
ax1.plot( BAU_2012.Time, BAU_2012.Population, "-.", lw=2, color="k", label="Рандерс - 2012")
ax1.plot( BAU_2012_Realistic.Time, UN_Medium, "--", lw=1, color="b", label="Средняя модель ООН - 2014")
ax1.plot( BAU_2012_Realistic.Time, UN_Low, "--", lw=1, color="m", label="Минимальная модель ООН - 2014")
ax1.errorbar( Calibration_Time, Calibration_Net, yerr=Calibration_Net*0.05, fmt='.', color="g", label="Продовольствие [тонн]")
ax1.errorbar( Calibration_Year, Calibration_Pop, fmt='.', color="b", label="Население реальное (ООН)")
ax1.grid(True)
ax1.set_ylabel("млн единиц")
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 10000)
ax1.legend(loc=0)

ax2.set_title( "Душевое потребление")
ax2.plot( BAU_2012.Time, BAU_2012_Realistic.Food_PC*1000, ".", lw=2, color="y", label="Продовольствие")
ax2.plot( BAU_2012.Time, BAU_2012_Realistic.Energy_PC*1000, "-", lw=2, color="m", label="Энергия")
ax2.set_ylabel("кг/год")
ax2.set_xlabel("Годы")
ax2.set_xlim( 1900, 2100)
#ax2.set_ylim( 0, 1250)
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_07_15.png")
if InteractiveModeOn: plt.show(True)

