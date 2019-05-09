from Population import *

#
# Описывает популяцию в открытой системе
# Согласно уравнению Мальтуса-Ферхюльста, но с потерями d
# Популяция стремится к кажущемуся оптимуму Q
# Время удвоения T2 используется вместо b
#
class Pond_Population_2:
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
        tmp = max ( self.Q, 0.01) # чтобы не было деления на ноль
        tmp = self.B * (1 - self.P / tmp)
        tmp *= self.P
        return tmp
    def dQ_dt( self, t):
        tmp = self.O
        # 5 лет неурожая
        if 1800 <= t and t < 1805: tmp = 0 
        tmp -= self.D * self.Q + min( self.P, self.Q)
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
        tmp = max ( self.Q, 0.01) # чтобы не было деления на ноль
        tmp = self.B * (1 - self.P / tmp)
        tmp *= self.P
        return tmp
    def dQ_dt( self, t):
        tmp = self.O
        # 5 лет неурожая
        if 1800 <= t and t < 1805: tmp = 0 
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
T  = np.linspace(1600, 2000, 401)
P1 = Pond_Population_2( 100, 100, 1000*(1+0.8), 10, 0.8)
P1.Solve( T)
P2 = Pond_Population_2( 100, 100, 1000*(1+0.1), 10, 0.1)
P2.Solve( T)
P3 = Pond_Population_3( 100, 100, 1000*(1+0.1), 10, 0.1)
P3.Solve( T)
P4 = np.ones( len(T)) * 1000

for i, t in enumerate(T):
    print( "{:4g} {:6.1f} {:6.1f} {:6.1f}".format( t, P1.Solution_P[i], P2.Solution_P[i], P3.Solution_P[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Time, P1.Solution_P, "-", color="b", lw=1, label="Сигмоида")
plt.plot( P2.Solution_Time, P2.Solution_P, "-", color="g", lw=1, label="Пик и стабилизация")
plt.plot( P3.Solution_Time, P3.Solution_P, "-", color="r", lw=1, label="Осцилляция")
plt.plot( T, P4, "--", lw=1, label="Оптимальный уровень")
plt.xlabel("Годы")
plt.xlim( 1600, 2000)
plt.ylabel("единиц")
plt.ylim( 0, 2000)
plt.title( "Пруд Мальтуса #3 - Осциллирующая популяция (T₂=10 лет)")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_04_05.png")
fig.show()
