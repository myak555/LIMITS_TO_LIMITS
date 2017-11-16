from Population import *
from Predictions import Interpolation_BAU_1972 

Resources_Time, Resources_Total = Load_Calibration( "Resources_Calibration.csv", "Year", "Total")
Resources_Total[0] = 1200e3 - Resources_Total[0]
for i in range( 1,len(Resources_Total)): Resources_Total[i] = Resources_Total[i-1] - Resources_Total[i]

T0 = np.linspace( 1900, 2100, 201)
T1 = np.linspace( 2015, 2100, 86)
P0 = Population()
BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T0)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,15))

plt.plot( BAU_1972.Time, BAU_1972.Population, "-", lw=3, color="b", label="Население (BAU-1972) [млн]")
plt.plot( T1, P0.UN_High.GetVector(T1), ".", lw=1, color="b", label="Население (предсказание ООН) [млн]")
plt.plot( T1, P0.UN_Low.GetVector(T1), ".", lw=1, color="b")
plt.plot( BAU_1972.Time, BAU_1972.Resources/100, "-", lw=3, color="r", label="Ресурсы (BAU-1972) х0.01 [toe]")
plt.plot( BAU_1972.Time, BAU_1972.Pollution/100, "-", lw=3, color="y", label="Загрязнение (BAU-1972) х0.01 [toe]")
plt.plot( BAU_1972.Time, BAU_1972.Food_PP*5, "--", lw=2, color="g", label="Продовольствие (BAU-1972) х5 [1/душу/год]")
plt.plot( BAU_1972.Time, BAU_1972.Industrial_PP*5, "--", lw=2, color="k", label="Промтовары (BAU-1972) х5 [1/душу/год]")
plt.plot( BAU_1972.Time, BAU_1972.Services_PP*5, "--", lw=2, color="m", label="Услуги (BAU-1972) х5 [1/душу/год]")
plt.plot( [2008,2008], [5000,6000], "-", lw=5, color="r", label="Глобальный Финансовый Кризис 2007-2009")
plt.plot( [2015,2015], [9000,10000], "-", lw=5, color="m", label="Великая Рецессия 2015-????")

plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Delta, fmt='.', color="b", label="Население (статистика ООН)")
plt.errorbar( Resources_Time, Resources_Total/100, yerr=Resources_Total*0.0002, fmt='.', color="r", label="Уголь+Нефть+Газ х0.01 [toe]")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов единиц")
plt.ylim( 0, 20000)
plt.title( 'Аппроксимация "Стандартного Сценария" World3 1972 г')
plt.grid(True)
plt.legend(loc=1)
plt.savefig( ".\\Graphs\\figure_07_02.png")
fig.show()
