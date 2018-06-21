from Utilities import *

data_name = "./Data/US_China_India_Compared.csv"

Year,US_Cons = Load_Calibration( data_name, "Year", "US_Cons_toe") 
China_Cons,India_Cons = Load_Calibration( data_name, "China_Cons_toe", "India_Cons_toe") 
US_Prod,US_PT = Load_Calibration( data_name, "US_Prod_toe", "US_Prod_t") 
China_Prod,India_Prod = Load_Calibration( data_name, "China_Prod_toe", "India_Prod_toe") 
China_PT,India_PT = Load_Calibration( data_name, "China_Prod_t", "India_Prod_t") 

US_Import = US_Cons-US_Prod
US_PT = US_Prod/US_PT
China_Import = China_Cons-China_Prod
China_PT = China_Prod/China_PT
India_Import = India_Cons-India_Prod
India_PT = India_Prod/India_PT

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Эффект Парижских соглашений: каменный уголь", fontsize=22)
gs = plt.GridSpec(2, 3, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])
ax5 = plt.subplot(gs[4])
ax6 = plt.subplot(gs[5])

minCons = -100
maxCons = 2000
minQ = 0.35
maxQ = 0.65

ax1.plot( Year, US_Cons, "-", lw=2, color='r')
ax1.plot( Year[16:], US_Prod[16:], "-", lw=2, color='b')
ax1.plot( Year[16:], US_Import[16:], "-", lw=2, color='k')
ax1.plot( [2015.4,2015.4], [minCons,maxCons], "--", lw=1, color='g')
ax1.set_ylim( minCons, maxCons)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.set_xlim( 1965, 2020)
ax1.grid(True)
ax1.set_title( "США")

ax2.plot( Year, China_Cons, "-", lw=2, color='r')
ax2.plot( Year[16:], China_Prod[16:], "-", lw=2, color='b')
ax2.plot( Year[16:], China_Import[16:], "-", lw=2, color='k')
ax2.plot( [2015.4,2015.4], [minCons,maxCons], "--", lw=1, color='g')
ax2.set_ylim( minCons, maxCons)
ax2.set_xlim( 1965, 2020)
ax2.grid(True)
ax2.set_title( "КНР")

ax3.plot( Year, India_Cons, "-", lw=2, color='r', label="Потребление")
ax3.plot( Year[16:], India_Prod[16:], "-", lw=2, color='b', label="Производство")
ax3.plot( Year[16:], India_Import[16:], "-", lw=2, color='k', label="+Импорт/-Экспорт")
ax3.plot( [2015.4,2015.4], [minCons,maxCons], "--", lw=1, color='g')
ax3.set_ylim( minCons, maxCons)
ax3.set_xlim( 1965, 2020)
ax3.grid(True)
ax3.set_title( "Индия")
ax3.legend(loc=2)

ax4.plot( Year[16:], US_PT[16:], "-", lw=2, color='m')
ax4.set_xlim( 1965, 2020)
ax4.set_ylim( minQ, maxQ)
ax4.set_ylabel("toe/т")
ax4.grid(True)

ax5.plot( Year[16:], China_PT[16:], "-", lw=2, color='m')
ax5.set_xlim( 1965, 2020)
ax5.set_ylim( minQ, maxQ)
ax5.grid(True)

ax6.plot( Year[16:], India_PT[16:], "-", lw=2, color='m', label="Качество угля")
ax6.set_xlim( 1965, 2020)
ax6.set_ylim( minQ, maxQ)
ax6.grid(True)
ax6.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_13_05.png")
fig.show()
