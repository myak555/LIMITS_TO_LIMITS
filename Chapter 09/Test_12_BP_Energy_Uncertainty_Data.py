from Population import *

BP_Year, BP_Coal = Load_Calibration( "07_BP_Coal.csv", "Year", "2017")
BP_Year, BP_Oil = Load_Calibration( "01_BP_Oil_Liquids.csv", "Year", "2017")
BP_Year, BP_Gas = Load_Calibration( "05_BP_Gas.csv", "Year", "2017")
BP_Year, BP_Nuclear = Load_Calibration( "08_BP_Nuclear.csv", "Year", "2017")
BP_Year, BP_Hydro = Load_Calibration( "09_BP_Hydro.csv", "Year", "2017")
BP_Year, BP_Renewable = Load_Calibration( "10_BP_Renewable.csv", "Year", "2017")

Pop_Year, Population = Load_Calibration( "Population_Calibration.csv", "Year", "Population")

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировое производство энергии по отчёту "ВР" 2017 г', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.bar( BP_Year, BP_Coal, width=0.35, color='#CDCDCD', label='Каменный уголь и торф')
btm = BP_Coal
ax1.bar( BP_Year, BP_Oil, width=0.35, bottom=btm, color='#B1FFBE', label="Нефть и жидкости")
btm += BP_Oil
ax1.bar( BP_Year, BP_Gas, width=0.35, bottom=btm, yerr=(btm+BP_Gas)*0.03, color='#FFD1D2', label="Природный газ")
btm += BP_Gas
btm_hc = np.array(btm)
ax1.bar( BP_Year, BP_Nuclear, width=0.35, bottom=btm, color='#FFAFE3', label="Ядерная энергия")
btm += BP_Nuclear
btm_hc_nuc = np.array(btm)
ax1.bar( BP_Year, BP_Hydro, width=0.35, bottom=btm, color='#B5E4FE', label="Гидроэнергия")
btm += BP_Hydro
ax1.bar( BP_Year, BP_Renewable, width=0.35, bottom=btm, yerr=(btm+BP_Renewable)*0.05, color='#005F00', label="Остальные возобновляемые")
btm += BP_Renewable

tonn_per_year = btm / Population[75:]
tonn_per_second = tonn_per_year / 365 / 24 /3600
watt = tonn_per_second * 41e9
tonn_per_year_hc = btm_hc / Population[75:]
tonn_per_second_hc = tonn_per_year_hc / 365 / 24 /3600
watt_hc = tonn_per_second_hc * 41e9
tonn_per_year_hc_nuc = btm_hc_nuc / Population[75:]
tonn_per_second_hc_nuc = tonn_per_year_hc_nuc / 365 / 24 /3600
watt_hc_nuc = tonn_per_second_hc_nuc * 41e9

##print( watt)
##print( watt_hc)
##print( watt_hc_nuc)
##print( watt_hc_nuc/watt)

ax1.set_xlim( 1965, 2020)
ax1.set_ylim( 0, 15000)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=0)

ax2.bar( BP_Year, watt_hc_nuc, width=0.35, yerr=watt_hc_nuc*0.05, color='m', label="НВИЭ")
ax2.bar( BP_Year, watt-watt_hc_nuc, width=0.35, bottom=watt_hc_nuc, yerr=watt*0.05, color='y', label="ВИЭ")
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 1000, 2500)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Вт")
ax2.grid(True)
ax2.set_title( "Эквивалент мощности на душу населения")
ax2.legend(loc=4)

plt.savefig( ".\\Graphs\\figure_09_12.png")
fig.show()
