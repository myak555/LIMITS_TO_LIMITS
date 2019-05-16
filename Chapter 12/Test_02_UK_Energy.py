from UK_Utilities import *

T0, Pop, C_Coal, C_Oil, C_Gas, P_Coal, P_Oil, P_Gas = Load_Calibrations_UK()

P1 = Population_UK()
P1.Solve( np.linspace( 1800, 2100, 301))
C0 = Coal_UK()
C0.Solve( np.linspace( 1800, 2100, 301))
#C0.Solve( np.linspace( 2015, 2100, 86))
C1 = Oil_UK()
C1.Solve( np.linspace( 1800, 2100, 301))
#C1.Solve( np.linspace( 2015, 2100, 86))
C2 = Gas_UK()
C2.Solve( np.linspace( 1800, 2100, 301))
#C2.Solve( np.linspace( 2015, 2100, 86))

print( "Coal: {:.1f} {:.1f}".format(C0.URR/1000, np.sum(C0.Total[:-83])/1000) )
print( "Oil: {:.1f} {:.1f}".format(C1.URR/1000, np.sum(C1.Total[:-83])/1000) )
print( "Gas: {:.1f} {:.1f}".format(C2.URR/1000, np.sum(C2.Total[:-83])/1000) )

fig = plt.figure( figsize=(15,10))
plt.plot( C0.Time, C0.Total, "-", lw=2, color="k", label="Добыча угля URR={:4.2f} млрд toe".format( C0.URR/1000))
plt.plot( C1.Time, C1.Total, "-", lw=2, color="g", label="Добыча нефти URR={:4.2f} млрд toe".format( C1.URR/1000))
plt.plot( C2.Time, C2.Total, "-", lw=2, color="r", label="Добыча газа URR={:4.2f} млрд toe".format( C2.URR/1000))
plt.errorbar( T0, P_Coal, yerr=5, fmt='.', color="k", label="Добыча угля (BP+Халл)")
plt.errorbar( T0, P_Oil, yerr=5, fmt='.', color="g", label='Добыча нефти и "жидкостей" (BP)')
plt.errorbar( T0, P_Gas, yerr=5, fmt='.', color="r", label="Добыча газа (статистика BP)")
plt.xlabel("Годы")
plt.xlim( 1850, 2100)
plt.ylabel("Миллионов тонн нефтяного эквивалента")
plt.ylim( 0, 250)
plt.title( 'Добыча угля, нефти и газа в Великобритании')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_12_02.png")
if InteractiveModeOn: plt.show(True)
