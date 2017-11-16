from Population import *

T_CO2, CO2_Total = Load_Calibration( "CO2_Calibration.csv", "Year", "Total")
T = np.linspace( 1800, 2100, 301)
l_real = len( T_CO2)
Scenario1 = Hubbert( 2014,0.1,0.1,47768).GetVector(T)
Scenario2 = Sigmoid( 2009,0.8,40000,47768).GetVector(T)
Scenario3 = Hubbert( 2025,0.065,0.065,55000).GetVector(T)
for i in range(len( T_CO2)-1):
    Scenario1[i] = CO2_Total[i]
    Scenario2[i] = CO2_Total[i]
    Scenario3[i] = CO2_Total[i]
T_ML, ML_PPM = Load_Calibration( "CO2_Mauna_Loa_2016.csv", "Year", "Mean")
T_LD, LD_PPM = Load_Calibration( "Ice_Core_Law_Dome.csv", "Year", "Total")

CO2_1800 = 285
M_atmosphere = 5.1480e9 # миллионов тонн
conversion = 0.658e6    # из массовых ppm в объёмные
sigma = np.log(2) / 21
T0 = np.linspace( 0,200,201)
Exp = np.exp( -sigma * T0)
C02_Level1 = np.convolve( Scenario1, Exp) * conversion / M_atmosphere + CO2_1800  
C02_Level2 = np.convolve( Scenario2, Exp) * conversion / M_atmosphere + CO2_1800  
C02_Level3 = np.convolve( Scenario3, Exp) * conversion / M_atmosphere + CO2_1800  
l1 = len( C02_Level1)
T1 = np.linspace( 1800, 1799+l1, l1)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
plt.plot( T1, C02_Level1, "--", lw=2, color='m', label="Сценарий #1: Обвал в 2014 г")
plt.plot( T1, C02_Level2, "-", lw=2, color='m', label="Сценарий #2: Плато с 2016 г")
plt.plot( T1, C02_Level3, ".", lw=2, color='m', label="Сценарий #3: Рост до 2025 г")
plt.errorbar( T_ML, ML_PPM, yerr=ML_PPM*0.005, fmt='.', color="b", label="Данные обсерватории Мауна Лоа (Гавайи)")
#plt.errorbar( T_LD, LD_PPM, yerr=LD_PPM*0.020, fmt='.', color="g", label="Данные льда станции Купол Ло (Антарктика)")
plt.xlabel("Годы")
plt.xlim( 1990, 2030)
plt.ylabel("Концентрация CO2 в атмосфере[ppmv]")
plt.ylim( 350, 440)
plt.title( "Накопление антропогенного CO2 в атмосфере")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_09_15.png")
fig.show()
