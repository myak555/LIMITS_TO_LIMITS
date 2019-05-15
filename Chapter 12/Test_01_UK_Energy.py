from UK_Utilities import *

T0, Pop, C_Coal, C_Oil, C_Gas, P_Coal, P_Oil, P_Gas = Load_Calibrations_UK()

P1 = Population_UK()
P1.Solve( np.linspace( 1800, 2100, 301))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Time, P1.Total, "-", lw=2, color="g", label="Феноменологическая модель")
plt.errorbar( T0, Pop, yerr=0.5, fmt='.', color="b", label="Население (статистика)")
plt.xlabel("Годы")
plt.xlim( 1800, 2100)
plt.ylabel("Миллионов человек")
plt.ylim( 20, 80)
plt.title( 'Население Великобритании')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_12_01.png")
fig.show()
