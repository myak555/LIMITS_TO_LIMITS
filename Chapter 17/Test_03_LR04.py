from Utilities import *

filename = "./Data/LR04_bentic_stack.txt"
Y_LR04, d18O_LR04 = Load_Calibration( filename, "Time (ka)", "Benthic d18O (per mil)", separator='\t')
Y_LR04, d18O_std_LR04 = Load_Calibration( filename, "Time (ka)", "Standard error (per mil)", separator='\t')
Y_Vostok_NOAA, T_Vostok_NOAA = Load_Calibration( "./Data/Vostok_NOAA_Temperature.txt", "age egtmod", "temperature", separator='\t')
Y_Vostok_CDI, T_Vostok_CDI = Load_Calibration( "./Data/Vostok_CDI_Temperature.txt", "BP", "Temp", separator=',')
Y_Vostok_CDI /= 1000
Y_Vostok, d18O_Vostok = Load_Calibration( "./Data/Vostok_d18O.txt", "gas age (GT4)", "Atm O18", separator='\t')
Y_Vostok /= 1000
T_LR04 = 11.64-4*d18O_LR04
print( T_LR04[-1] )
T_Vostok = 8.6-2.243*d18O_Vostok
limits = -5350, 0
limits = -500, 0

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Температурная аномалия Земли по Лисеки и Раймо (2005)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Разница концентрации изотопов кислорода, δ¹⁸О")
ax1.errorbar( -Y_LR04, d18O_LR04, yerr=3*d18O_std_LR04, fmt=".", color="g", label="LR04 (океаническое дно)")
ax1.errorbar( -Y_Vostok, d18O_Vostok, yerr=0.15, fmt=".", color="b", label='Ледовый керн "Восток" (атмосфера)')
ax1.set_xlim( limits)
##ax1.set_ylim( 0, 8500)
ax1.set_ylabel("δ¹⁸О [‰]")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Аномалия температур (от уровня 1950 г)")
ax2.errorbar( -Y_LR04, T_LR04, xerr=10, yerr=2, alpha=0.5,fmt=".", color="g")
ax2.errorbar( -Y_Vostok_NOAA, T_Vostok_NOAA, yerr=2, alpha=0.1, fmt=".", color="b", label='Реконструкция NOAA по дейтерию керна "Восток"')
ax2.plot( Y_Vostok_CDI, T_Vostok_CDI, "-", lw=3, alpha=0.5, color="k", label='Данные с сайта www.climatedata.info')
ax2.set_xlim( limits)
##ax2.set_ylim( -8, 14)
ax2.set_xlabel("тысяч лет (шкала EGTMOD)")
ax2.set_ylabel("[ºЦ]")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_17_03.png")
fig.show()
