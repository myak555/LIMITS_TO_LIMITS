from Population import *

#
# Описывает популяцию в открытой системе
# Согласно уравнению Мальтуса-Ферхюльста, но с потерями d
# Популяция стремится к кажущемуся оптимуму Q
#
class Pond_Population_2:
    def __init__( self, P0, Q0, O0, b_rate, d_rate):
        self.P_Initial = P0
        self.P = P0
        self.Q_Initial = Q0
        self.Q = Q0
        self.O_Initial = O0
        self.O = O0
        self.B = b_rate
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
# Solve numerically
#
T  = np.linspace(1600, 2000, 401)
P1 = Pond_Population_2( 100, 100, 1000, 0.1, 0)
P1.Solve( T)

for i, t in enumerate(T):
    print( "{:4g} {:6.1f} {:6.1f} {:6.1f}".format( t, P1.Solution_P[i], P1.Solution_Q[i], P1.Solution_O[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Time, P1.Solution_P, "-", lw=1, label="Популяция")
plt.plot( P1.Solution_Time, P1.Solution_Q/10, "-", lw=1, label="Ресурс (x10)")
plt.plot( P1.Solution_Time, P1.Solution_O, "--", lw=1, label="Оптимальный уровень")
plt.errorbar( [1624,1624,1637,1696,1805,1832,1832,1847,1899], [994,1494,2825,1000,71,994,1792,3136,1000], fmt='o', color="k")
plt.text( 1627,1039, 'A')
plt.text( 1627,1539, 'D')
plt.text( 1640,2864, 'B')
plt.text( 1699,1045, 'C')
plt.text( 1797,175, 'E')
plt.text( 1834,1039, 'A')
plt.text( 1834,1831, 'D')
plt.text( 1850,3182, 'B')
plt.text( 1902,1052, 'C')
plt.annotate("Органический рост", xy=(1619,591), xytext=(1650,688), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Мальтузианская ловушка", xy=(1630,1786), xytext=(1660,1980), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Мальтузианская катастрофа", xy=(1640,2513), xytext=(1668,2682), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Стабилизация", xy=(1720,1000), xytext=(1730,1400), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Бутылочное горлышко популяции", xy=(1805,71), xytext=(1865,468), arrowprops=dict(facecolor='black', shrink=0.05))
plt.xlabel("Годы")
plt.xlim( 1600, 2000)
plt.ylabel("единиц")
plt.ylim( 0, 4000)
plt.title( "Пруд Мальтуса #2 - Популяция стремится к кажущемуся оптимуму")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_04_02.png")
if InteractiveModeOn: plt.show(True)
