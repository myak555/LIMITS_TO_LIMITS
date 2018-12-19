from Population import *

#
# Описывает популяцию в открытой системе
# согласно системе уравнений Мальтуса
# P0 - начальная популяция
# Q0 - начальные запасы
# O0 - начальное производство
# F0 - начальные природные ресурсы
# T2_P - время удвоения популяции
# T2_O - время удвоения призводства
# T2_F - время восстановления ресурсов
# d_Q - процент потери запасов
# j_O - технологический коэффициент урожайности
# Популяция стремится к кажущемуся оптимуму Q
#
class Island_Population_3:
    def __init__( self, P0, Q0, O0, F0, T2_P, T2_O, T2_F, d_Q, j_O):
        self.P_Initial = P0
        self.P = P0
        self.Q_Initial = Q0
        self.Q = Q0
        self.O_Initial = O0
        self.O = O0
        self.F_Initial = F0
        self.F = F0
        self.B_P = np.log(2)/T2_P
        self.B_O = np.log(2)/T2_O
        self.B_F = np.log(2)/T2_F
        self.D = Sigmoid( 150, 0.05, 1, d_Q)
        self.J = Sigmoid( 400, 0.025, j_O, j_O*10)
        return
    def dP_dt( self, t):
        tmp = max ( self.Q, 0.01)
        tmp = self.B_P * (1 - self.P / tmp)
        tmp *= self.P
        return tmp
    def dQ_dt( self, t):
        tmp = -self.D.Compute(t) * self.Q # естественная убыль запасов
        tmp -= self.P          # убыль запасов на потребление
        tmp += self.O          # текущий урожай
        return tmp
    def dO_dt( self, t):
        tmp = max ( self.F * self.J.Compute(t), 0.01)
        tmp = self.B_O * (1 - self.P / tmp)
        tmp *= self.O
        return tmp
    def dF_dt( self, t):
        tmp = self.B_F * (1-self.F/self.F_Initial) * self.F     # естественное восстановление ресурса
        tmp -= self.O                                           # убыль ресурса на пополнение запасов
        return tmp
    def _func( self, y, t):
        self.P = max( [y[0], 0])
        self.Q = max( [y[1], 0])
        self.O = max( [y[2], 0])
        self.F = max( [y[3], 0])
        f0 = self.dP_dt( t)
        f1 = self.dQ_dt( t)
        f2 = self.dO_dt( t)
        f3 = self.dF_dt( t)
        return [f0, f1, f2, f3]
    def Solve( self, t0):
        y0 = [self.P, self.Q, self.O, self.F]
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.025)
        self.Solution_Time = t0
        self.Solution_P = soln[:, 0].clip(0)
        self.Solution_Q = soln[:, 1].clip(0)
        self.Solution_O = soln[:, 2].clip(0)
        self.Solution_F = soln[:, 3].clip(0)
        self.P = self.P_Initial
        self.Q = self.Q_Initial
        self.O = self.O_Initial
        self.F = self.F_Initial
        return

#
# Solve numerically
#
T = np.linspace(0, 1000, 1001)
t2_q = 10 # восстановление ресурсов
productivity = 0.001
P1 = Island_Population_3( 500, 500, 1000, 500000, 25, 5, t2_q, 0.3, productivity)
P1.Solve( T)
b1 = np.log(2) / 25
Exponent1 = 500 * np.exp( b1*(T-0))

for i in range( len(T)):
    print( "{:4g} {:6.1f} {:6.1f} {:6.1f} {:8.1f}".format( T[i], P1.Solution_P[i], P1.Solution_Q[i], P1.Solution_O[i], P1.Solution_F[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Time, P1.Solution_P, "-", lw=2, label="Население")
plt.plot( P1.Solution_Time, P1.Solution_Q, "-", lw=2, label="Запасы")
plt.plot( P1.Solution_Time, P1.Solution_O, "-", lw=1, label="Производство {:5.2f}% от F".format( productivity*100))
plt.plot( P1.Solution_Time, P1.Solution_F/100, "-", lw=1, label="Природные ресурсы (х100)")
plt.plot( T, Exponent1, "--", lw=1, label="Экспоненциальный рост Т₂=25 лет")
plt.xlabel("Годы")
plt.xlim( 0, 1000)
plt.ylabel("единиц")
plt.ylim( 0, 10000)
plt.title( "Остров Мальтуса #3 - Второе технологическое достижение")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_05_08.png")
fig.show()
