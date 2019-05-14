from Predictions import * 

T0 = np.linspace( 1900, 2100, 201)
P0 = Population()
R0 = Resources()
BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T0)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Предсказания базового сценария World3 (1972 г)', fontsize=22)
gs = plt.GridSpec(2, 2, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot( T0, BAU_1972.Population/1000, "-", lw=2, color="b", label="World3")
ax1.plot( T0[100:], P0.UN_Medium.GetVector( T0)[100:]/1000, "--", lw=1, color="b", label="Средняя оценка ООН")
ax1.errorbar( P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000, fmt='.', color="k", label="Статистика (ООН)")
ax1.set_title( "Население (млрд)")
ax1.grid( True)
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 12 )
ax1.legend(loc=0)

ax2.plot( T0, BAU_1972.Resources/1e6, "-", lw=2, color="m", label="World3")
ax2.errorbar( R0.Calibration_Year, R0.Calibration_Reserves/1e6, fmt='.', color="k", label="Статистика (EIA/BP)")
ax2.set_title( "Ископаемое топливо (трлн тут)")
ax2.grid( True)
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 1.2)
ax2.legend(loc=0)

FAO_Year, FAO_Net_Food = Load_Calibration("Agriculture_Calibration.csv", ["Year", "Net_Food"])
ax3.plot( T0, BAU_1972.Industrial, "-", lw=2, color="r", label="Промтоваров")
ax3.plot( T0, BAU_1972.Food, "-", lw=2, color="g", label="Продовольствия")
ax3.plot( T0, BAU_1972.Services, "-", lw=2, color="m", label="Услуг")
ax3.plot( [2007,2007], [0,40], "--", lw=1, color="k")
ax3.plot( [2015,2015], [0,40], "-.", lw=1, color="k")
ax3.errorbar( FAO_Year, FAO_Net_Food/1000, fmt='.', color="k", label="Статистика (ФАО)")
ax3.set_title( "Производство (1900 год = 1)")
ax3.grid( True)
ax3.set_xlim( 1900, 2100)
ax3.set_ylim( 0, 50)
ax3.legend(loc=0)

ML_Year, ML_CO2 = Load_Calibration("./Data/CO2_Mauna_Loa.csv", ["Year", "Mean"])
ax4.plot( T0, BAU_1972.CO2/1000, "-", lw=2, color="y", label="World3")
ax4.errorbar( ML_Year, ML_CO2/1e3, fmt='.', color="k", label="Статистика (Мауна Лоа)")
ax4.set_title( "Уровень СО₂ (ppb)")
ax4.grid( True)
ax4.set_xlim( 1900, 2100)
ax4.set_ylim( 0, 0.6)
ax4.legend(loc=3)

plt.savefig( "./Graphs/figure_07_02.png")
fig.show()
