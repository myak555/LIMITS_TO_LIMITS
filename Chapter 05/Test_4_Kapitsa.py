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
        return self.Solution_P

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

P0 = Population(2061.9005, 8400, 0.027)
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

Magic_Year = np.pi/2 - 10e3/176e3*44
Magic_Year = 2003 - 44 * np.tan( Magic_Year)
print( Magic_Year)

fig = plt.figure( figsize=(15,10))
plt.plot( T0, P0.UN_Medium.GetVector(T0), "-", lw=2, color="g", label="Средняя оценка ООН, 2010 г")
plt.plot( T_sf, P_sf, "--", lw=1, color="g", label="Модель Акулий Плавник")
plt.plot( P4.Solution_Time, P4.Solution_P, "--", lw=1, color="r", label="Статья С.П.Капицы, 1996 г")
plt.plot( T0, P0.Kapitsa_Analytical.GetVector(T0), "-", lw=2, color="r", label="T₀=2003, K=176·10⁹, τ=44")
plt.plot( [Magic_Year, Magic_Year], [1,100000], "-.", lw=3, color="r", label="Магическая дата: пятница, 25 ноября 2061 г")
plt.plot( [1900, 2200], [10000,10000], "-.", lw=3, color="r", label="Великий демографический переход Капицы 10 млрд.")
plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Yerr, fmt='.', color="b", label="Население (статистика ООН)")
plt.xlabel("Годы")
plt.xlim( 1900, 2200)
plt.ylabel("миллионов человек")
plt.ylim( 0, 20000)
plt.title( 'Подбор С, τ, To в формуле С.П.Капицы по данным 2016 года')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_05_04.png")
if InteractiveModeOn: plt.show(True)
