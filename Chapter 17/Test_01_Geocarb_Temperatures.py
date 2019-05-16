from Utilities import *

def Compute_T_from_CO2( t, gc):
    atm_temp_0 = 0
    DT2x = 3
    solar_response = -7.4
    atm_temp = atm_temp_0 + DT2x * np.log(gc/280)/np.log(2)
    atm_temp -= solar_response * (t/570)
    return atm_temp 

mya, gc2, gc3 = Load_Calibration(
    "./Data/GEOCARB_III.csv",
    ["MYA", "GEOCARB2","GEOCARB3"], '\t')
uncertainty = 6000 / np.exp( (mya+570)*0.005)
gc3_max = gc3 + uncertainty
gc3_min = np.clip( gc3 - uncertainty, 50, np.max(gc3))
atm_temp2 = Compute_T_from_CO2( mya, gc2)
atm_temp3 = Compute_T_from_CO2( mya, gc3)
atm_temp3_min = Compute_T_from_CO2( mya, gc3_min)
atm_temp3_max = Compute_T_from_CO2( mya, gc3_max)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Температурная аномалия Земли по Ройер и Бернеру', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Концентрация СО₂ в атмосфере")
ax1.plot( mya, gc2, "--", lw=2, color="g", label="GEOCARB II")
ax1.plot( mya, gc3, "-", lw=3, color="g", label="GEOCARB III")
ax1.bar( mya, gc3_max-gc3_min, 7.5, bottom=gc3_min, alpha=0.4, color="g", label="Неопределённость")
ax1.plot( [-547,-547], [0, 8000], "--", lw=3, color="k")
ax1.plot( [-450,-450], [0, 8000], "--", lw=3, color="k")
ax1.plot( [-420,-420], [0, 8000], "--", lw=3, color="k")
ax1.plot( [-360,-360], [0, 8000], "--", lw=3, color="k")
ax1.plot( [-260,-260], [0, 8000], "--", lw=3, color="k")
ax1.set_xlim( -600, 0)
ax1.set_ylim( 0, 8500)
ax1.set_ylabel("[ppmv]")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Средняя температура поверхности Земли")
ax2.plot( mya, atm_temp2, "--", lw=2, color="k", label="GEOCARB II")
ax2.plot( mya, atm_temp3, "-", lw=3, color="k", label="GEOCARB III")
ax2.bar( mya, atm_temp3_max-atm_temp3_min, 7.5, bottom=atm_temp3_min, alpha=0.4, color="y", label="Неопределённость")
ax2.text( -590, 11.0, "Байконур")
ax2.plot( [-547,-547], [0, 10], "--", lw=3, color="k")
ax2.text( -460, 0.5, "Андо-Сахара")
ax2.plot( [-450,-450], [2, 16], "--", lw=3, color="k")
ax2.plot( [-420,-420], [2, 16], "--", lw=3, color="k")
ax2.text( -320, 10.5, "Кару")
ax2.plot( [-360,-360], [-8, 16], "--", lw=3, color="k")
ax2.plot( [-260,-260], [-8, 16], "--", lw=3, color="k")
ax2.set_xlim( -600, 0)
ax2.set_ylim( -8, 14)
ax2.set_xlabel("миллионов лет")
ax2.set_ylabel("[ºЦ от среднего 1960-1990 гг.]")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_17_01.png")
if InteractiveModeOn: plt.show(True)
