from Predictions import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Y_BP, Coal = Load_Calibration( "./Data/11_BP_Electricity_Generation.csv", "Year", "Coal")
Coal /= 8.766
print( Coal[-1])
Gas, Nuclear = Load_Calibration( "./Data/11_BP_Electricity_Generation.csv", "Gas", "Nuclear")
Gas = Gas/8.766+Coal
print( Gas[-1])
Nuclear = Nuclear/8.766+Gas
print( Nuclear[-1])
Oil, Solar = Load_Calibration( "./Data/11_BP_Electricity_Generation.csv", "Oil", "Solar")
Oil = Oil/8.766+Nuclear
print( Oil[-1])
Solar = Solar/8.766+Oil
print( Solar[-1])
Wind, Hydro = Load_Calibration( "./Data/11_BP_Electricity_Generation.csv", "Wind", "Hydro")
Wind = Wind/8.766+Solar
print( Wind[-1])
Hydro = Hydro/8.766+Wind
print( Hydro[-1])
Other, Unind = Load_Calibration( "./Data/11_BP_Electricity_Generation.csv", "Geo_Biomass_Other", "Unindentified")
Other = (Other+Unind)/8.766+Hydro
print( Other[-1])

Year_Model = np.linspace( 2018, 2050, 33)

Model_4 = np.ones( len(Year_Model)) * 2932
k4a = (3707 / 2932) ** (1/12)
k4b = (5875 / 3707) ** (1/20)
Model_4_Solar = np.ones( len(Year_Model)) * 68
k4a_solar = (342 / 68) ** (1/12)
k4b_solar = (1700 / 342) ** (1/20)
Model_4_Wind = np.ones( len(Year_Model)) * 297
k4a_wind = (662 / 297) ** (1/12)
k4b_wind = (776 / 662) ** (1/20)
for i in range( 1,len(Model_4)):
    if Year_Model[i]<=2030:
        Model_4[i] = Model_4[i-1] * k4a
        Model_4_Solar[i] = Model_4_Solar[i-1] * k4a_solar
        Model_4_Wind[i] = Model_4_Wind[i-1] * k4a_wind
    else:
        Model_4[i] = Model_4[i-1] * k4b
        Model_4_Solar[i] = Model_4_Solar[i-1] * k4b_solar
        Model_4_Wind[i] = Model_4_Wind[i-1] * k4b_wind

Model_2 = np.ones( len(Year_Model)) * 2943
k2a = (3365 / 2943) ** (1/12)
k2b = (4871 / 3365) ** (1/20)
for i in range( 1,len(Model_4)):
    if Year_Model[i]<=2030: Model_2[i] = Model_2[i-1] * k2a
    else: Model_2[i] = Model_2[i-1] * k2b

#Pop = Population().UN_Medium.GetVector(Year)
#Pop_Model = Population().UN_Medium.GetVector(Year_Model)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценки CSIRO по выработке электроэнергии', fontsize=22)
gs = plt.GridSpec(1, 1, height_ratios=[1]) 
ax1 = plt.subplot(gs[0])
x_start, x_end = 1985, 2030

img = imread( cbook.get_sample_data( os.getcwd() + '/2018-2018.png'))
ax1.set_title('Сценарии "СSIRO 4º" и СSIRO 2º" против экономического отдела "ВР"')
ax1.imshow(img, zorder=0, extent=[2017, 2029, -960, 3000],  interpolation='nearest', aspect='auto')
ax1.plot( Y_BP, Other, "-", color="#005500", lw=2, label="Гео и био")
ax1.plot( Y_BP, Hydro, "-", color="b", lw=2, label="Гидро")
ax1.plot( Y_BP, Wind, "-", color="c", lw=2, label="Ветровая")
ax1.plot( Y_BP, Solar, "-", color="y", lw=2, label="Солнечная")
ax1.plot( Y_BP, Oil, "-", color="g", lw=2, label="Из нефти")
ax1.plot( Y_BP, Nuclear, "-", color="m", lw=2, label="Ядерная")
ax1.plot( Y_BP, Gas, "-", color="c", lw=2, label="Из природного газа")
ax1.plot( Y_BP, Coal, "-", color="k", lw=2, label="Уголь")
#ax1.errorbar( [2018,2018,2018,2018,2018,2018,2018,2018], [1270,1660,1992,2095,2164,2450,2863,2943], fmt=".", color="r")
#ax1.errorbar( [2018.2,2018.2,2018.2,2018.2,2018.2,2018.2,2018.2,2018.2], [1328,1706,2015,2141,2221,2439,2840,2943], fmt=".", color="b")
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( -1000,3200)
ax1.set_ylabel("ГВт·лет")
ax1.grid(True)
ax1.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_16_21.png")
fig.show()

