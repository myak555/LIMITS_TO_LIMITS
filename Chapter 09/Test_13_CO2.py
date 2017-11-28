from Population import *

T_CO2, CO2_Cement = Load_Calibration( "CO2_Calibration.csv", "Year", "Cement")
CO2_Coal, CO2_Oil = Load_Calibration( "CO2_Calibration.csv", "Coal", "Oil")
CO2_Gas, CO2_Total = Load_Calibration( "CO2_Calibration.csv", "Gas", "Total")

T = np.linspace( 1800, 2100, 301)
l_real = len( T_CO2)
Scenario1 = Hubbert( 2014,0.1,0.1,36400).GetVector(T)
Scenario2 = Sigmoid( 2009,0.8,40000,36400).GetVector(T)
Scenario3 = Hubbert( 2025,0.065,0.065,40000).GetVector(T)
for i in range(len( T_CO2)):
    Scenario1[i] = CO2_Total[i]
    Scenario2[i] = CO2_Total[i]
    Scenario3[i] = CO2_Total[i]

S = np.sum( CO2_Total)
print( S)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
plt.plot( T, Scenario1, "--", lw=2, color='m', label="Сценарий #1: Обвал в 2014 г")
plt.plot( T, Scenario2, "-", lw=2, color='m', label="Сценарий #2: Плато с 2016 г")
plt.plot( T, Scenario3, ".", lw=2, color='m', label="Сценарий #3: Рост до 2025 г")
plt.errorbar( T_CO2, CO2_Cement, yerr=CO2_Cement*0.1, fmt='.', color="b", label="Производство цемента")
plt.errorbar( T_CO2, CO2_Coal, yerr=CO2_Coal*0.1, fmt='.', color="k", label="Каменный уголь")
plt.errorbar( T_CO2, CO2_Oil, yerr=CO2_Oil*0.1, fmt='.', color="g", label="Нефть и жидкости")
plt.errorbar( T_CO2, CO2_Gas, yerr=CO2_Gas*0.1, fmt='.', color="r", label="Природный газ")
plt.errorbar( T_CO2, CO2_Total, yerr=CO2_Total*0.1, fmt='o', color="m", label="ВСЕГО")
plt.xlabel("Годы")
plt.xlim( 1800, 2100)
plt.ylabel("Выбросы CO₂ [млн тонн]")
plt.ylim( 0, 45000)
plt.title( "Проверка отчётов BP по выбросам CO₂")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_09_13.png")
fig.show()
