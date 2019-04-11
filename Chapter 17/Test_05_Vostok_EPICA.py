from Utilities import *

filename = "./Data/Vostok_CDI_Temperature_CO2_Radiation.txt"
Y_Vostok, T_Vostok = Load_Calibration( filename, "BP", "Temp")
CO2_Vostok, Radiation = Load_Calibration( filename, "CO2", "Radiation")
filename2 = "./Data/NOAA_EPICA_Deuterium.txt"
Y_EPICA, D_EPICA = Load_Calibration( filename2, "Age/mean", "deltaD", separator="\t")

Y_Vostok /= 1000
T_Vostok -= 55
Y_EPICA /= 1000
D_EPICA += 391.2
D_EPICA *= 0.16
D_EPICA -= 55

limits = -450, 0

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 1, height_ratios=[1,1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title('Данные ледового керна скважин "Восток" и "EPICA"', fontsize=22)
ax1.errorbar( Y_Vostok, T_Vostok, yerr=1, alpha=0.2, fmt=".", color="r")
ax1.plot( Y_Vostok, T_Vostok, "-", lw=2, color="r", alpha=0.5, label='Температура по дейтерию "Восток"')
ax1.plot( -Y_EPICA, D_EPICA, "-", lw=3, color="b", alpha=0.5, label='Температура по дейтерию "EPICA"')
ax1.plot( [-15,-15], [-65,-52], "--", lw=2, color="k")
ax1.text( -51, -52, "Голоцен", color="k")
ax1.plot( [-132,-132], [-65,-52], "--", lw=2, color="k")
ax1.text( -182, -52, "Микулино", color="k")
ax1.plot( [-243,-243], [-65,-52], "--", lw=2, color="k")
ax1.text( -282, -52, "Уолстон", color="k")
ax1.plot( [-330,-330], [-65,-52], "--", lw=2, color="k")
ax1.text( -392, -52, "Гольдштейн", color="k")
ax1.plot( [-423,-423], [-65,-52], "--", lw=2, color="k")
ax1.text( -449, -52, "Хоксни", color="k")
ax1.set_xlim( limits)
ax1.set_ylim( -70, -50)
ax1.set_yticks( [-65,-60,-55,-50])
ax1.set_ylabel("[ºЦ]")
ax1.legend(loc=3)
ax1.grid(True)

ax2.errorbar( Y_Vostok[81:-24], CO2_Vostok[81:-24], yerr=5, alpha=0.2, fmt=".", color="g")
ax2.plot( Y_Vostok[81:-24], CO2_Vostok[81:-24], "-", lw=2, color="g", alpha=0.5, label="CO₂")
ax2.arrow( -350, 320, -91, 0, width=2, color="k")
ax2.text( -340, 317, "неандертальцы", color="k")
ax2.arrow( -265, 320, 218, 0, width=2, color="k")
ax2.arrow( -420, 310, -91, 0, width=2, color="k")
ax2.text( -400, 307, "хомо эректус", color="k")
ax2.arrow( -330, 310, 63, 0, width=2, color="k")
ax2.arrow( -160, 300, -131, 0, width=2, color="k")
ax2.text( -150, 297, "хомо сапиенс", color="k")
ax2.arrow( -80, 300, 71, 0, width=2, color="k")
ax2.set_xlim( limits)
ax2.set_ylim( 180,330)
ax2.set_ylabel("[ppmv]")
ax2.legend(loc=3)
ax2.grid(True)

ax3.plot( Y_Vostok[21:], Radiation[21:], "-", lw=2, color="m", label="Солнечное излучение на широте 65º (циклы Миланковича)")
ax3.set_xlim( limits)
ax3.set_ylim( 380,500)
ax3.set_ylabel("[Вт/м²]")
ax3.legend(loc=3)
ax3.grid(True)
ax3.set_xlabel("тысяч лет назад")

plt.savefig( ".\\Graphs\\figure_17_05.png")
fig.show()
