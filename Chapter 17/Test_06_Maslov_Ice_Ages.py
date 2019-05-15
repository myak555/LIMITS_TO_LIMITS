from Population import *

#
# Describes modified Lotka-Volterra system
# after Lev A. Maslov
# "Self-organization of the Earth’s climate system versus Milankovitch-Berger astronomical cycles 
# Тc - average air/surface temperature
# T0 - initial temperature
# Ec - system enthropy
# E0 - initiar enthropy
# Bc - buffer
# B0 - initial buffer
# T - current temperature
# aT, bT - constants in equation (1)
# aE, bE - constants in equation (2)
# aB, bB - constants in equation (3)
#
class Ice_Age_Simple:
    def __init__( self, initial=[8,0.00015,150], a=[-4.673,17.9005,-2], b=[0.1827,-0.7,3.5]):
    #def __init__( self, initial=[10,0.00015,20], a=[-4.673,17.9005,-2], b=[0.1827,-0.7,3.5]):
    #def __init__( self, initial=[10,0.45,20], a=[-4, 4, -5], b=[1,-1,5]):
        self.Initial = np.array( initial)
        self.Functions = np.array( initial)
        self.A = np.array( a)
        self.B = np.array( b)
        return
    def dTc_dt( self, t):
        tmp = self.A[0] + self.B[0] * self.Functions[2]
        tmp *= self.Functions[0]
        #tmp += 40*np.sin( 60*t)
        return tmp
    def dEc_dt( self, t):
        tmp = self.A[1] + self.B[1] * self.Functions[2]
        tmp *= self.Functions[1]
        return tmp
    def dBc_dt( self, t):
        tmp = self.A[2] * self.Functions[0] + self.B[2] * self.Functions[1]
        tmp *= self.Functions[2]
        return tmp
    def _func( self, y, t):
        for i in range( len(self.Functions)):
            self.Functions[i] = y[i]
            #self.Functions[i] = max( [y[i], 0.01])
        f0 = self.dTc_dt( t)
        f1 = self.dEc_dt( t)
        f2 = self.dBc_dt( t)
        return [f0, f1, f2]
    def Solve( self, t0):
        y0 = np.array(self.Functions)
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.0025)
        self.Solution_Time = t0*100
        self.Solution_Tc = soln[:, 0].clip(0)
        self.Solution_Ec = soln[:, 1].clip(0)
        self.Solution_Bc = soln[:, 2].clip(0)
        self.Functions = np.array( self.Initial)
        return

#
# Calibrate
#
Age, Tvar = Load_Calibration("./Data/Vostok_T.csv", ["Age", "Tvar"])
Age /= -1000

#
# Solve numerically
#
time = np.linspace(-4.3, 0, 10001)
ia = Ice_Age_Simple()
ia.Solve( time)
limits = -420, 0

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Модель ледниковых периодов Л Маслова (2014 г)", fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.plot( ia.Solution_Time, ia.Solution_Tc*0.66-8, "-", lw=3, color="r", label="Температуры")
ax1.errorbar( Age, Tvar, xerr=5, yerr=0.5, fmt=".", color="k", alpha=.2, label='По дейтерию "Восток"')
ax1.set_xlim( limits)
ax1.set_ylabel("ºЦ")
ax1.set_yticks([-10, -5, 0])
ax1.grid( True)
ax1.legend( loc=0)

ax2.plot( ia.Solution_Time, ia.Solution_Ec, "-", lw=2, color="b", label="Энтропия системы")
ax2.plot( ia.Solution_Time, ia.Solution_Bc/7.5, "-", lw=2, color="m", label="Буферная функция")
ax2.set_xlim( limits)
ax2.set_ylabel("условные единицы")
ax2.grid( True)
ax2.legend( loc=0)
ax2.set_xlabel("Тысячи лет")

plt.savefig( "./Graphs/figure_17_06.png")
fig.show()
