from Population import *

#
# Феноменологическая модель населения Великобритании
#
class Population_UK:
    def __init__( self):
        self.Functions = []
        self.Functions += [Sigmoid( 1945, 0.021, 20, 70.5)]
        self.Functions += [Hubbert( 2020, 0.20, 0.10, 5)]
        self.Functions += [Hubbert( 1972, 0.05, 0.17, 3.3)]
        self.Functions += [Hubbert( 1940, 0.4, 0.3, 5)]
        self.Functions += [Hubbert( 1911, 0.15, 0.10, 5)]
        self.Functions += [Hubbert( 1890, 0.10, 0.25, 4.5)]
        self.Functions += [Hubbert( 1841, 0.60, 0.10, 1.5)]
        #self.Functions += [Sigmoid( 2050, 0.15, 0, 20)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        return self.Total

T0, Pop = Load_Calibration( "UK_Population_and_Energy.csv", "Year", "population")
P1 = Population_UK()
P1.Solve( np.linspace( 1800, 2100, 301))

Prepare_Russian_Font()
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
plt.savefig( ".\\Graphs\\figure_12_01.png")
fig.show()
