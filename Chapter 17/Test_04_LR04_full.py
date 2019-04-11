from Utilities import *

filename = "./Data/LR04_bentic_stack.txt"
Y_LR04, d18O_LR04 = Load_Calibration( filename, "Time (ka)", "Benthic d18O (per mil)", separator='\t')
Y_LR04, d18O_std_LR04 = Load_Calibration( filename, "Time (ka)", "Standard error (per mil)", separator='\t')
Y_Vostok_NOAA, T_Vostok_NOAA = Load_Calibration( "./Data/Vostok_NOAA_Temperature.txt", "age egtmod", "temperature", separator='\t')
T_LR04 = 11.64-4*d18O_LR04
Y_Error_LR04 = np.ones( len(Y_LR04))*60*(np.exp(Y_LR04/5400)-1)
D_Error_LR04 = np.ones( len(Y_LR04))*0.3*(np.exp(Y_LR04/5400)-0.5)
T_Error_LR04 = np.ones( len(Y_LR04))*2*(np.exp(Y_LR04/5400)-1)
limits = -5350, 0

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Температурная аномалия Земли по Лисеки и Раймо (2005)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Разница концентрации изотопов кислорода, δ¹⁸О")
ax1.errorbar( -Y_LR04, d18O_LR04, xerr=Y_Error_LR04, yerr=D_Error_LR04, alpha=0.5, fmt=".", color="g", label="LR04 (океаническое дно)")
ax1.set_xlim( limits)
ax1.set_ylabel("δ¹⁸О [‰]")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Аномалия антарктических температур (от уровня 1950 г)")
ax2.errorbar( -Y_LR04, T_LR04, xerr=Y_Error_LR04, yerr=T_Error_LR04, alpha=0.5,fmt=".", color="g")
ax2.plot( -Y_Vostok_NOAA, T_Vostok_NOAA, "-", lw=2, alpha=0.5, color="b", label='Реконструкция NOAA по дейтерию керна "Восток"')
ax2.arrow( -4550, 7.7, -300, 0, width=.2, color="k")
ax2.text( -4500, 7.2, "KОП", color="k")
ax2.arrow( -4230, 7.7, 200, 0, width=.2, color="k")
ax2.set_xlim( limits)
ax2.set_ylim( -10, 10)
ax2.set_xlabel("тысяч лет (шкала EGTMOD)")
ax2.set_ylabel("[ºЦ]")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_17_04.png")
fig.show()
