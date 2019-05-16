from Population import * 

Time = np.linspace( 1960, 2060, 21)
T_Report =   [1965, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040]
URR_Proven = [   5,  550, 1120, 1120, 1120, 1190, 1200, 1250, 1250]
UR_P10 = Sigmoid( 1985, 0.1, 16000, 2200).GetVector( Time)
UR_P50 = Sigmoid( 1975, 0.5, 3000, 2200).GetVector( Time)
UR_P90 = Sigmoid( 1973, 0.25, 0, 2200).GetVector( Time)
TRF_P10 = Sigmoid( 1980, 1.0, 0.65, 0.57).GetVector( Time)
TRF_P50 = Sigmoid( 1960, 1.0, 0.3,  0.57).GetVector( Time)
TRF_P90 = Sigmoid( 1965, 1.0, 0.2,  0.57).GetVector( Time)
URR_P10 = UR_P10 * TRF_P10
URR_P50 = UR_P50 * TRF_P50
URR_P90 = UR_P90 * TRF_P90
ERF_P10 = Sigmoid( 2015, 0.1, 0.65, 0.95).GetVector( Time)
ERF_P50 = Sigmoid( 2005, 0.5, 0.50,  0.95).GetVector( Time)
ERF_P90 = Sigmoid( 2010, 0.2, 0.25,  0.95).GetVector( Time)
ERR_P10 = URR_P10 * ERF_P10
ERR_P50 = URR_P50 * ERF_P50
ERR_P90 = URR_P90 * ERF_P90

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Вероятностные оценки запасов месторождения Весёлое', fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title( "Начальные геологические запасы")
ax1.plot( Time, UR_P10, "--", lw=2, color="g", label="P-10/3P (возможные)")
ax1.plot( Time[1:], UR_P50[1:], "-", lw=3, color="g", label="P-50/2P (вероятные)")
ax1.plot( Time, UR_P90, "-.", lw=2, color="g", label="P-90/1P (подтверждённые)")
ax1.grid(True)
ax1.set_ylabel("млн баррелей")
ax1.set_xlim( 1960, 2060)
ax1.set_ylim( 0, 15000)
ax1.legend(loc=0)

ax2.set_title( "Начальные технически - извлекаемые запасы")
ax2.plot( Time, URR_P10, "--", lw=2, color="b", label="P-10/3P (возможные)")
ax2.plot( Time[1:], URR_P50[1:], "-", lw=3, color="b", label="P-50/2P (вероятные)")
ax2.plot( Time, URR_P90, "-.", lw=2, color="b", label="P-90/1P (подтверждённые)")
ax2.errorbar( T_Report, URR_Proven, fmt="o", color="m", label="Отчёты SEC/USGS")
ax2.set_ylabel("млн баррелей")
ax2.set_xlim( 1960, 2060)
ax2.set_ylim( 0, 10000)
ax2.grid(True)
ax2.legend(loc=0)

ax3.set_title( "Начальные экономически - извлекаемые запасы")
ax3.plot( Time, ERR_P10, "--", lw=2, color="r", label="P-10/3P (возможные)")
ax3.plot( Time[1:], ERR_P50[1:], "-", lw=3, color="r", label="P-50/2P (вероятные)")
ax3.plot( Time, ERR_P90, "-.", lw=2, color="r", label="P-90/1P (подтверждённые)")
ax3.set_ylabel("млн баррелей")
ax3.set_xlabel("Годы")
ax3.set_xlim( 1960, 2060)
ax3.set_ylim( 0, 7000)
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_08_11.png")
if InteractiveModeOn: plt.show(True)

