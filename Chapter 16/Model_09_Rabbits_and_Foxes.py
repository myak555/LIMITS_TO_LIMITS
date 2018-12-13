from Population import *

#
# Описывает классическую систему Лотки-Вольтерры для задачи "зайцев и лис"
# Ph0 - начальная популяция зайцев
# Pf0 - начальная популяция лис
# Ph1 - равновесная популяция зайцев
# Pf1 - равновесная популяция лис
# Ph - текущая популяция зайцев
# Pf - текущая популяция лис
# аf - коэффициент смертности лис: 0.1
# bh - коэффициент рождаемости зайцев: 0.5
#
class Prey_and_Predator:
    def __init__( self, Ph0, Pf0, Ph1, Pf1, af=0.1, bh=0.5):
        self.Ph_Initial = Ph0
        self.Ph = Ph0
        self.Ph_Eq = Ph1
        self.Pf_Initial = Pf0
        self.Pf = Pf0
        self.Pf_Eq = Pf1
        self.Af = af
        self.Bh = bh
        return
    def dPh_dt( self, t):
        tmp = 1 - self.Pf/self.Pf_Eq
        tmp *= self.Bh
        tmp *= self.Ph
        return tmp
    def dPf_dt( self, t):
        tmp = self.Ph/self.Ph_Eq - 1
        tmp *= self.Af
        tmp *= self.Pf
        return tmp
    def _func( self, y, t):
        self.Ph = max( [y[0], 0])
        self.Pf = max( [y[1], 0])
        f0 = self.dPh_dt( t)
        f1 = self.dPf_dt( t)
        return [f0, f1]
    def Solve( self, t0):
        y0 = [self.Ph, self.Pf]
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.0025)
        self.Solution_Time = t0
        self.Solution_Ph = soln[:, 0].clip(0)
        self.Solution_Pf = soln[:, 1].clip(0)
        self.Ph = self.Ph_Initial
        self.Pf = self.Pf_Initial
        return

#
# Solve numerically
#
T = np.linspace(0, 1000, 10001)
P1 = Prey_and_Predator( 5000, 2000, 10000, 1000)
P1.Solve( T)

##for i in range( len(T)):
##    print( "{:4g} {:6.1f} {:6.1f}".format( T[i], P1.Solution_Ph[i], P1.Solution_Pf[i]))

fig = plt.figure( figsize=(15,7.5))
plt.plot( P1.Solution_Time, P1.Solution_Ph/10, "-", lw=2, label="Зайцы x10")
plt.plot( P1.Solution_Time, P1.Solution_Pf, "-", lw=2, label="Лисы")
#plt.plot( P1.Solution_Time, 1000*P1.Solution_Pf/P1.Solution_Ph, "--", lw=2, label="Условная цена зайца")
plt.xlabel("Годы")
plt.xlim( 0, 100)
plt.ylabel("единиц")
plt.ylim( 0, 5000)
plt.title( "Задача о зайцах и лисах - колеблющаяся популяция.")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_16_09.png")
fig.show()
