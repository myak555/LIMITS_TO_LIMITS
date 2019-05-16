from UK_Utilities import *

T0, Pop, C_Coal, C_Oil, C_Gas, P_Coal, P_Oil, P_Gas, C_Nuc, C_Hyd, C_Ren, C_Tot = Load_Calibrations_UK_Full()

P1 = Population_UK()
P1.Solve( np.linspace( 1800, 2100, 301))
C0 = Coal_UK_Cons()
C0.Solve( np.linspace( 1800, 2100, 301))
C1 = Oil_UK_Cons()
C1.Solve( np.linspace( 1800, 2100, 301))
C2 = Gas_UK_Cons()
C2.Solve( np.linspace( 1800, 2100, 301))
C3 = Nuc_UK_Cons()
C3.Solve( np.linspace( 1800, 2100, 301))
C4 = Hydro_UK_Cons()
C4.Solve( np.linspace( 1800, 2100, 301))
C5 = Renewable_UK_Cons()
C5.Solve( np.linspace( 1800, 2100, 301))
C6 = Coal_UK()
C6.Solve( np.linspace( 1800, 2100, 301))
C7 = Oil_UK()
C7.Solve( np.linspace( 1800, 2100, 301))
C8 = Gas_UK()
C8.Solve( np.linspace( 1800, 2100, 301))

Consumption_Carbon = C0.Total + C1.Total + C2.Total
Consumption = Consumption_Carbon + C3.Total + C4.Total + C5.Total
Export_Carbon = C6.Total + C7.Total + C8.Total - Consumption_Carbon 

Consumption_Carbon /= P1.Total
Consumption /= P1.Total
Export_Carbon /= P1.Total

Conversion_Factor = 41e9 / 365.25 / 86164.1

Consumption_Carbon *= Conversion_Factor
Consumption *= Conversion_Factor
Export_Carbon *= Conversion_Factor
Export_Percentage = Sigmoid( 1950, 0.1, 25, -45).GetVector(np.linspace( 1800, 2100, 301)) / 100.0
Export_Goods = Export_Percentage * Consumption_Carbon
Consumption -= Export_Goods
Export_Food = Sigmoid( 2030, 0.5, -250, 0).GetVector(np.linspace( 1800, 2100, 301))
Consumption -= Export_Food
Consumption += 600

fig = plt.figure( figsize=(15,12.5))
plt.plot( C0.Time, Consumption_Carbon, "-", lw=2, color="k", label="Потребление из ископаемых углеводородов")
plt.plot( C0.Time, Consumption, "-", lw=3, color="b", label="Потребление ВСЕГО, включая товары и продовольствие")
plt.plot( C0.Time, Export_Carbon, "-", lw=2, color="y", label="Экспорт(+) или импорт (-) ископаемых углеводородов")
plt.plot( C0.Time, Export_Goods, "-", lw=2, color="r", label="Экспорт(+) или импорт (-) предметов потребления")
plt.plot( C0.Time, Export_Food, "-", lw=2, color="g", label="Экспорт(+) или импорт (-) продовольствия")
plt.plot( [1850,2100], [2000,2000], "--", lw=1, color="r", label="Уровень 1850 года")
plt.plot( [1850,2100], [5850,5850], "-", lw=1, color="r")
plt.plot( [1850,2100], [8150,8150], "-.", lw=1, color="r", label="Уровень 2007 года")
plt.plot( [2017,2017], [-9000,9000], "-", lw=1, color="r")
plt.plot( [1960,1960], [-9000,9000], "-", lw=1, color="r")
plt.xlabel("Годы")
plt.xlim( 1850, 2100)
plt.ylabel("Мгновенная мощность на душу населения [Вт]")
plt.ylim( -9000, 9000)
plt.title( 'Энергобаланс Великобритании на душу населения')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_12_07.png")
if InteractiveModeOn: plt.show(True)
