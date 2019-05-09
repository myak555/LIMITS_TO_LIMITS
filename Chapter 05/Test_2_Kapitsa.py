from Population import *

#
# Описывает популяцию по методу С.П.Капицы
# "Успехи физических наук" 139(1) 57-71, РАН, 1996
#
class Population_Kapitsa:
    def __init__( self, T0=2007, K=186e3, tau=42):
        self.T0 = T0
        self.K = K
        self.tau = tau
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_P = self.K / self.tau * (np.pi/2 - np.arctan((self.T0 - t)/self.tau))
        return

#
# Описывает популяцию по формуле фон-Fёрстера
# von Foerster, Mora, and Amiot 1960
# Doomsday: Friday, 13 November, A.D. 2026
#
class Population_vonFoerster:
    def __init__( self, T0=2026.87, K=1.79e5, k=0.990, P_max=1000000):
        self.T0 = T0
        self.K = K
        self.k = k
        self.P_max = P_max
        print( "Adam year:", (T0-K**(1/k))*1000)
        print( "Eva year:", (T0-(K/2)**(1/k))*1000)
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_P = np.ones( len(t)) * self.P_max
        for i in range( len(t)):
            if t[i]>=self.T0: continue
            self.Solution_P[i] = self.K / (self.T0 - t[i])**self.k
        return

#
# Описывает популяцию по формуле фон-Хёрнера
# Sebastien von Hoerner
# "Population Explosion and Interstellar Expansion".
# Journal of the British Interplanetary Society (28): 691–712.
#
class Population_vonHoerner:
    def __init__( self, T0=2026.87, K=2e5, P_max=1000000):
        self.T0 = T0
        self.K = K
        self.P_max = P_max
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_P = np.ones( len(t)) * self.P_max
        for i in range( len(t)):
            if t[i]>=self.T0: continue
            self.Solution_P[i] = self.K / (self.T0 - t[i])
        return

#
# Описывает популяцию по полному решению уравнения фон-Fёрстера
#
class Population_vonFoerster_Full:
    def __init__( self, T0=2026.87, a=0.0001, K=21, P_max=1000000):
        self.T0 = T0
        self.A = a
        self.K = K
        self.P_max = P_max
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_P = np.ones( len(t)) * self.P_max
        for i in range( len(t)):
            if t[i]>=self.T0: continue
            self.Solution_P[i] = self.K / (np.exp(self.A*(self.T0 - t[i]))-1)
        return

P0 = Population()
P0.LoadHistorical()
T0 = np.linspace( 1900, 2200, 301)
T_sf  = np.linspace(-3000, 3000, 6001)
P_sf = P0.Solve( T_sf)

P1 = Population_vonFoerster()
P1.Solve( np.linspace(-3000, 3000, 6001))
P2 = Population_vonHoerner()
P2.Solve( np.linspace(-3000, 3000, 6001))
P3 = Population_vonFoerster_Full()
P3.Solve( np.linspace(-3000, 3000, 6001))

P4 = Population_Kapitsa()
P4.Solve( T_sf)

fig = plt.figure( figsize=(15,10))
ax = plt.subplot()
ax.set_yscale("log")
plt.plot( P2.Solution_Time, P2.Solution_P, "--", lw=1, color="r", label="Шутка фон-Хёрнера, 1975 г")
plt.plot( P4.Solution_Time, P4.Solution_P, "-", lw=2, color="r", label="Статья С.П.Капицы, 1996 г")
plt.plot( [2027, 2027], [1,100000], "-.", lw=3, color="r", label="Конец цивилизации: пятница, 13 ноября 2026 г")
plt.errorbar( P0.Historical_Year, P0.Historical_Total, yerr=P0.Historical_Yerr, fmt='o', color="r", label="Население (оценки)")
plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Yerr, fmt='.', color="b", label="Население (статистика ООН)")

plt.xlabel("Годы")
plt.xlim( -3000, 3000)
plt.ylabel("миллионов человек")
plt.ylim( 10, 20000)
plt.title( 'Серьёзная статья С.П. Капицы 1996 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_05_02.png")
fig.show()
