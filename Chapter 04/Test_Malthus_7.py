from Population import *

#
# Описывает популяцию в открытой системе
# Согласно уравнению Мальтуса-Ферхюльста, но с потерями d
# Популяция стремится к кажущемуся оптимуму Q
# Время удвоения T2 используется вместо b
# Убрано ограничение на потребление
#
class Pond_Population_3:
    def __init__( self, P0, Q0, O0, T2, d_rate):
        self.P_Initial = P0
        self.P = P0
        self.Q_Initial = Q0
        self.Q = Q0
        self.O_Initial = O0
        self.O = O0
        self.B = np.log(2)/T2
        self.D = d_rate
        return
    def dP_dt( self, t):
        tmp = max ( self.Q, 0.01)
        tmp = self.B * (1 - self.P / tmp)
        tmp *= self.P
        return tmp
    def dQ_dt( self, t):
        tmp = self.O
        tmp -= self.D * self.Q + self.P
        return tmp
    def dO_dt( self, t):
        tmp = 0
        return tmp
    def _func( self, y, t):
        self.P = max( [y[0], 0])
        self.Q = max( [y[1], 0])
        self.O = max( [y[2], 0])
        f0 = self.dP_dt( t)
        f1 = self.dQ_dt( t)
        f2 = self.dO_dt( t)
        return [f0, f1, f2]
    def Solve( self, t0):
        y0 = [self.P, self.Q, self.O]
        # Не забудем поставить правильную дискретизацию!
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.025)
        self.Solution_Time = t0
        self.Solution_P = soln[:, 0].clip(0)
        self.Solution_Q = soln[:, 1].clip(0)
        self.Solution_O = soln[:, 2].clip(0)
        self.P = self.P_Initial
        self.Q = self.Q_Initial
        self.O = self.O_Initial
        return

#
# Solve numerically
#
T = np.linspace(1944, 1974, 301)
P1 = Pond_Population_3( 29, 35000, 300, 2.35, 0.01)
P1.Solve( T)
b = np.log(2) / 2.35
Exponent = 29 * np.exp( b*(T-1944))
Linear = (T-1957)*950

for i, t in enumerate(T):
    print( "{:7.1f} {:7.1f} {:7.1f} {:7.1f}".format( t, P1.Solution_P[i], P1.Solution_Q[i], P1.Solution_O[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Time, P1.Solution_P, "-", lw=2, label="Популяция оленей")
plt.plot( P1.Solution_Time, P1.Solution_Q/10, "-", lw=1, label="Запасы ягеля (x10)")
plt.plot( P1.Solution_Time, P1.Solution_O, "--", lw=1, label="Прибавка ягеля / год")
plt.plot( P1.Solution_Time, Exponent, "--", lw=1, label="Экспоненциальный рост Т₂ = 2.35 года")
plt.plot( P1.Solution_Time, Linear, "--", lw=1, label="Линейный рост 950/год")
plt.xlabel("Годы")
plt.xlim( 1940, 1980)
plt.ylabel("единиц")
plt.ylim( 0, 7000)
plt.title( "Пруд Мальтуса #3 - Моделирование о Св.Мэтью")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_04_07.png")
if InteractiveModeOn: plt.show(True)
