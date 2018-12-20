from Predictions import *

Year,Renewable = Load_Calibration("Energy_Calibration.csv", "Year", "Renewable")
Pop = Population().UN_Medium.GetVector(Year)
Renewable /= Pop
Renewable *= 1000 # Convert from toe to kg
Renewable *= 42 # Convert from to kg to MJ
Renewable /= 31.6 # Convert from MJ to W momentary
Renewable *= 0.38 # BP assumed conversion efficiency

x_start, x_end = 1965, 2020

fig = plt.figure( figsize=(15,8))
gs = plt.GridSpec(1, 1, height_ratios=[1]) 
ax1 = plt.subplot(gs[0])

ax1.set_title("Выработка энергии из ВИЭ (включая гидро и биомассу)")
ax1.bar( Year, Renewable, 0.35, alpha=0.4, color="g")
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,100)
ax1.set_xlabel("Год")
ax1.set_ylabel("Вт на душу населения")
ax1.grid(True)

plt.savefig( ".\\Graphs\\figure_12_12.png")
fig.show()

