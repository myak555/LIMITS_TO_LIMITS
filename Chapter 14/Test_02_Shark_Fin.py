from Resources import *

#
# Describes shark fin equation
# e_min, e_max – part of capital used for material production [unitless]
# C0 – inital capital [mln toe]
# Q0 – initial resource [mln toe]
# i(t) – investment rate [unitless]
# d(t) – depreciation rate [unitless]
#
class Shark_Fin_1:
    def __init__( self, C0, Q0, mp, sigma, e_min, e_max):
        self.C_0 = C0
        self.C = C0
        self.Q_0 = Q0
        self.Q = Q0
        self.Epsilon = Sigmoid( mp, sigma, e_min, e_max)
        self.Epsilon.Plot( 0, 1)
        return
    def investment_function( self, t):
        if t <= 2200: return 1.0/15.0
        return self.C * self.depreciation_function( t) / max( [self.W(t), 1])
    def depreciation_function( self, t):
        return 1.0/25.0
    def W( self, t):
        tmp = self.Q / self.Q_0
        tmp = self.Epsilon.Compute(tmp)
        tmp *= self.C
        return tmp
    def U( self, t):
        tmp = 1-self.investment_function( t)
        tmp *= self.W(t)
        return tmp
    def dQ_dt( self, t):
        tmp = -self.W(t)
        return tmp
    def dC_dt( self, t):
        tmp = self.investment_function( t) * self.W(t)
        tmp -= self.depreciation_function( t) * self.C
        return tmp
    def _func( self, y, t):
        self.Q = max( [y[0], 0])
        self.C = max( [y[1], 0])
        f0 = self.dQ_dt( t)
        f1 = self.dC_dt( t)
        return [f0, f1]
    def Solve( self, t0):
        y0 = [self.Q, self.C]
        self.Solution_Year = t0
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.025)
        self.Solution_Q = soln[:, 0]
        self.Solution_C = soln[:, 1]
        self.Solution_dQ = np.zeros( len(t0))
        self.Solution_W = np.zeros( len(t0))
        self.Solution_U = np.zeros( len(t0))
        for i in range( len(t0)):
            self.C = self.Solution_C[i]
            self.Q = self.Solution_Q[i]
            self.Solution_dQ[i] = -self.dQ_dt(t0[i])
            self.Solution_W[i] = self.W(t0[i])
            self.Solution_U[i] = self.U(t0[i])
        self.C = self.C_0
        self.Q = self.Q_0
        return

R = Resources()
T  = np.linspace(1800, 2200, 401)

#
# Solve numerically
#
Q0_0 = 750
SF0 = Shark_Fin_1( Q0_0/12.5, Q0_0*1000, 0.2, 20, 0, 1.0-0.03)
SF0.Solve( T)
Q0_1 = 1200
SF1 = Shark_Fin_1( Q0_1/20, Q0_1*1000, 0.4, 20, 0, 1.0-0.03)
SF1.Solve( T)
Q0_2 = 2400
T  = np.linspace(1800, 2200, 401)
SF2 = Shark_Fin_1( Q0_2/40, Q0_2*1000, 0.6, 20, 0, 1.0-0.03)
SF2.Solve( T)

fig = plt.figure( figsize=(15,15))
plt.suptitle( "Акулий плавник 1")

gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( SF2.Solution_Year, SF2.Solution_Q/1000, "--", lw=1, color= "r", label="URR = {:.0f} млрд toe".format(Q0_2))
ax1.plot( SF1.Solution_Year, SF1.Solution_Q/1000, "-", lw=2, color= "r", label="URR = {:.0f} млрд toe".format(Q0_1))
ax1.plot( SF0.Solution_Year, SF0.Solution_Q/1000, "-.", lw=1, color= "r", label="URR = {:.0f} млрд toe".format(Q0_0))
ax1.set_xlim( 1800, 2100)
ax1.set_ylim( 0, Q0_2)
ax1.set_ylabel( "млрд toe")
ax1.grid(True)
ax1.legend(loc=0)
ax1.set_title( 'Технически извелекаемые запасы ископаемого топлива')

AR = R.Calibration_Nuclear + R.Calibration_Renewable
ax2.errorbar( R.Calibration_Year, R.Calibration_Carbon, yerr=R.Calibration_Total*0.05, fmt='.', color="r", label="Добыча энергоресурсов")
#ax2.errorbar( R.Calibration_Year, AR, yerr=AR*0.05, fmt='.', color="m", label="Ядерная + ВИЭ")
ax2.plot( SF0.Solution_Year, SF0.Solution_C, "--", lw=1, color= "g")
ax2.plot( SF0.Solution_Year, SF0.Solution_dQ, "--", lw=1, color= "r")
#ax2.plot( SF0.Solution_Year, SF0.Solution_U, "--", lw=1, color= "b")
ax2.plot( SF1.Solution_Year, SF1.Solution_C, "-", lw=2, color= "g", label="Капитал")
ax2.plot( SF1.Solution_Year, SF1.Solution_dQ, "-", lw=2, color= "r", label="Добыча")
#ax2.plot( SF1.Solution_Year, SF1.Solution_U, "-", lw=2, color= "b", label="Реальное потребление")
ax2.plot( SF2.Solution_Year, SF2.Solution_C, "--", lw=1, color= "g")
ax2.plot( SF2.Solution_Year, SF2.Solution_dQ, "--", lw=1, color= "r")
#ax2.plot( SF2.Solution_Year, SF2.Solution_U, "--", lw=1, color= "b")
#ax2.set_ylim( 0, 10)
ax2.set_xlim( 1950, 2050)
ax2.grid(True)
ax2.set_xlabel( "Годы")
ax2.set_ylabel( "млн toe")
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_13_07.png")
fig.show()
