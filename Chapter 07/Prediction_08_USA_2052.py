from Population import *
from Predictions import Interpolation_BAU_1972 
from Predictions import Interpolation_BAU_2012 

Time, Pop, Workforce, Labor_Prod, GDP, Consumption, Coal, Oil, Gas, Nuclear, Renewable, Food, Land, Yield = Load_Calibration(
    "./Data/Randers_2052_USA.csv",
    ["Year", "Population", "Workforce", "Labor_Prod", "GDP", "Consumption", "Coal", "Oil",
     "Gas", "Nuclear", "Renewable", "Food", "Land", "Yield"])

Labor_Prod /= 365
GDP /= Pop / 1e6 * 365
Consumption /= Pop / 1e6 * 365
Energy = (Coal + Oil + Gas + Nuclear + Renewable) * 1000 / Pop / 365
NonRenewable = (Coal + Oil + Gas + Nuclear) * 1000 / Pop / 365
Food /= Pop / 1000 * 365
Land /= Pop / 100
Yield *= 10

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Соединённые Штаты (предсказание NewWorld 2012 г)', fontsize=22)
gs = plt.GridSpec(2, 2, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot( Time, Pop, "-", lw=3, color="b", label="Всего")
ax1.plot( Time, Workforce, "--", lw=1, color="b", label="Работоспособных")
ax1.set_title( "Население (млн)")
ax1.grid( True)
ax1.set_xlim( 1970, 2050)
ax1.set_ylim( 0, 1500)
ax1.legend(loc=0)

ax2.plot( Time, Consumption, "-", lw=3, color="r", label="Потребление")
ax2.plot( Time, Labor_Prod, "--", lw=1, color="r", label="Производительность труда")
ax2.set_title( "Экономика ($/день/душу)")
ax2.grid( True)
ax2.set_xlim( 1970, 2050)
ax2.set_ylim( 0, 300)
ax2.legend(loc=0)

ax3.plot( Time, Energy * 41e3 / 24/ 3600, "-", lw=3, color="m", label="Потребление")
ax3.plot( Time, NonRenewable * 41e3 / 24/ 3600, "--", lw=1, color="m", label="Невозобновляемой")
ax3.set_title( "Энергетика (кВт/душу)")
ax3.grid( True)
ax3.set_xlim( 1970, 2050)
ax3.set_ylim( 0, 12)
ax3.legend(loc=0)

ax4.plot( Time, Food, "-", lw=3, color="g", label="(кг/день/душу)")
ax4.plot( Time, Land/10, "-", lw=2, color="k", label="Сельхозугодий (га/душу х 10)")
ax4.plot( Time, Yield/10, "--", lw=1, color="k", label="Урожайность [т/га]")
ax4.set_title( "Продовольствие")
ax4.grid( True)
ax4.set_xlim( 1970, 2050)
ax4.set_ylim( 0, 20)
ax4.legend(loc=0)

plt.savefig( "./Graphs/figure_07_08.png")
fig.show()
