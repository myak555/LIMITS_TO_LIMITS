from Utilities import *

def Compute_T_from_CO2( t, gc):
    atm_temp_0 = 0
    DT2x = 3
    solar_response = -7.4
    atm_temp = atm_temp_0 + DT2x * np.log(gc/280)/np.log(2)
    atm_temp -= solar_response * (t/570)
    return atm_temp 

mya, gc3 = Load_Calibration( "./Data/GEOCARB_III.csv", "MYA", "GEOCARB3", '\t')
Delta_O18, Polar_Ice = Load_Calibration( "./Data/GEOCARB_III.csv", "Delta_O18", "Polar_Ice", '\t')
Tropical, CO2Corr = Load_Calibration( "./Data/GEOCARB_III.csv", "Tropical", "CO2Corr", '\t')

uncertainty = 6000 / np.exp( (mya+570)*0.005)
gc3_max = gc3 + uncertainty
gc3_min = np.clip( gc3 - uncertainty, 50, np.max(gc3))
atm_temp3 = Compute_T_from_CO2( mya, gc3)
atm_temp3_min = Compute_T_from_CO2( mya, gc3_min)
atm_temp3_max = Compute_T_from_CO2( mya, gc3_max)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Температурная аномалия Земли по Ройер, Бернеру и Вейзеру', fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[2,1,2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title("СО₂ в атмосфере и δ¹⁸О в морских карбонатах")
ax1.plot( mya, gc3/1000, "-", lw=3, color="g", label="GEOCARB III (1000 ppmv)")
ax1.bar( mya, (gc3_max-gc3_min)/1000, 7.5, bottom=gc3_min/1000, alpha=0.1, color="g")
ax1.plot( mya, Delta_O18, "-", lw=3, color="m", label="δ¹⁸О, с удалением тренда")
ax1.bar( mya, np.ones(len(Delta_O18))*2, 7.5, bottom=Delta_O18-1, alpha=0.3, color="m")
ax1.plot( [-547,-547], [-5, 15], "--", lw=2, color="k")
ax1.plot( [-450,-450], [-5, 15], "--", lw=2, color="k")
ax1.plot( [-420,-420], [-5, 15], "--", lw=2, color="k")
ax1.plot( [-360,-360], [-5, 15], "--", lw=2, color="k")
ax1.plot( [-260,-260], [-5, 15], "--", lw=2, color="k")
ax1.set_xlim( -600, 0)
ax1.set_ylim( -2.5, 8.5)
ax1.set_ylabel("[1000 ppmv / ppmv]")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Распространение полярных ледников")
ax2.bar( mya, 90-Polar_Ice, 7.5, bottom=Polar_Ice, alpha=0.5, color="b")
ax2.plot( [-547,-547], [0, 90], "--", lw=2, color="k")
ax2.plot( [-450,-450], [0, 90], "--", lw=2, color="k")
ax2.plot( [-420,-420], [0, 90], "--", lw=2, color="k")
ax2.plot( [-360,-360], [0, 90], "--", lw=2, color="k")
ax2.plot( [-260,-260], [0, 90], "--", lw=2, color="k")
ax2.set_xlim( -600, 0)
ax2.set_ylim( 15, 90)
ax2.yaxis.set_ticks(np.arange(15, 91, 15))
ax2.set_ylabel("[º широты]")
ax2.grid(True)

ax3.set_title("Средняя температура поверхности Земли")
ax3.plot( mya, atm_temp3, "-", lw=2, color="g", label="По модели GEOCARB III")
ax3.plot( mya, CO2Corr, "-", lw=3, color="k", label="По δ¹⁸О с коррекцией за СО₂ в воде")
ax3.plot( mya, Tropical, "--", lw=3, color="k", label="Поверхность моря в тропиках по δ¹⁸О")
ax3.bar( mya, np.ones(len(Delta_O18))*4, 7.5, bottom=CO2Corr-2, alpha=0.5, color="y")
ax3.text( -590, 11.0, "Байконур")
ax3.plot( [-547,-547], [0, 10], "--", lw=2, color="k")
ax3.text( -460, 0.5, "Андо-Сахара")
ax3.plot( [-450,-450], [2, 16], "--", lw=2, color="k")
ax3.plot( [-420,-420], [2, 16], "--", lw=2, color="k")
ax3.text( -320, 10.5, "Кару")
ax3.plot( [-360,-360], [-8, 16], "--", lw=2, color="k")
ax3.plot( [-260,-260], [-8, 16], "--", lw=2, color="k")
ax3.set_xlim( -600, 0)
ax3.set_ylim( -10, 14)
ax3.set_xlabel("миллионов лет")
ax3.set_ylabel("[ºЦ от среднего 1960-1990 гг.]")
ax3.grid(True)
ax3.legend(loc=3)

plt.savefig( ".\\Graphs\\figure_17_02.png")
fig.show()
