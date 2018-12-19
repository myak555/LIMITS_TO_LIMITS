from Predictions import *

Year, Production = Load_Calibration( "./Data/Uranium_Production_and_Consumption.csv", "Year", "Production")
Civil, Civil_Naval = Load_Calibration( "./Data/Uranium_Production_and_Consumption.csv", "Civil", "Civil_Naval")
Stock = np.zeros( len(Year))
Stock[0] += Production[0] 
Stock[0] -= Civil_Naval[0] 
for i in range( 1,len(Year)):
    Stock[i] = Stock[i-1] 
    Stock[i] += Production[i] 
    Stock[i] -= Civil_Naval[i] 

x_start, x_end = 1940, 2020

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча, расход и стратегические запасы урана', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Годовая добыча и расход")
ax1.errorbar( Year, Production/1000, yerr=Production*0.05/1000, fmt=".", color="m", label="Реальная добыча")
ax1.plot( Year, Civil/1000, "-", color="m", label="Расход в гражданских реакторах")
ax1.plot( Year, Civil_Naval/1000, "--", color="m", label="+ расход в ЯСУ ВМФ (оценка WNA)")
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,90)
ax1.set_ylabel("тысяч тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Накопленные извлечённые запасы")
ax2.plot( Year, Stock/1000, "-", lw=3, color="m")
ax2.set_xlim(x_start, x_end)
ax2.set_ylim( 0, 850)
ax2.set_ylabel("тысяч тонн")
ax2.grid(True)
#ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_12_08.png")
fig.show()

