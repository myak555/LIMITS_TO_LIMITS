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
Consumption_Renewable = Consumption_Carbon + C3.Total + C4.Total + C5.Total
Export_Carbon = C6.Total + C7.Total + C8.Total - Consumption_Carbon 

fig = plt.figure( figsize=(15,10))
plt.plot( C0.Time, Consumption_Carbon, "-", lw=2, color="k", label="Потребление ископаемых углеводородов")
plt.plot( C0.Time, Consumption_Renewable, "-", lw=3, color="b", label="Потребление ВСЕГО (возобновляемые и ядерная энергия)")
plt.plot( C0.Time, Export_Carbon, "-", lw=2, color="y", label="Экспорт(+) или импорт (-) ископаемых углеводородов")
plt.xlabel("Годы")
plt.xlim( 1850, 2100)
plt.ylabel("Миллионов тонн нефтяного эквивалента")
plt.ylim( -250, 250)
plt.title( 'Энергобаланс Великобритании')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_12_05.png")
if InteractiveModeOn: plt.show(True)
