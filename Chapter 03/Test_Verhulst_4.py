from Utilities import *

#
# Describes population as an exponent
#
class Population_Exponent:
    def __init__( self, P0, a, b):
        self.Initial = P0
        self.Total = P0
        self.A = a
        self.B = b
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Yerr = Load_Calibration( "Population_calibration.csv", "Year", "Yerror")
        return
    def dP_dt( self, t):
        tmp = self.Total
        tmp *= self.B - self.A
        return tmp
    def _func( self, y, t):
        self.Total = y[0]
        f0 = self.dP_dt( t)
        return [f0]
    def Solve( self, t0):
        y0 = [self.Total]
        soln = odeint(self._func, y0, t0)
        self.Solution_Year = t0
        self.Solution_Total = soln[:, 0]
        self.Total = self.Initial
        return

#
# Describes population as a Velhurst equation
#
class Population_Velhurst:
    def __init__( self, P0, b, o_left, o_right, o_year=0):
        self.Initial = P0
        self.Total = P0
        self.B = b
        self.O_left = o_left
        self.O_right = o_right
        self.Midpoint = o_year
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Yerr = Load_Calibration( "Population_calibration.csv", "Year", "Yerror")
        return
    def dP_dt( self, t):
        tmp = self.Total
        tmp *= self.B
        o = self.O_left
        if t >= self.Midpoint: o = self.O_right 
        tmp *= (1-self.Total/o)
        return tmp
    def _func( self, y, t):
        self.Total = y[0]
        f0 = self.dP_dt( t)
        return [f0]
    def Solve( self, t0):
        self.Solution_Year = t0
        if self.Midpoint < t0[0] or t0[ len(t0)-1] < self.Midpoint:
            y0 = [self.Total]
            soln = odeint(self._func, y0, t0)
            self.Solution_Total = soln[:, 0]
        else:
            # solve for each half - above an below inflexion point
            mp = (self.O_left + self.O_right) * 0.5
            mpi = np.nonzero( t0 >= self.Midpoint)[0][0]
            t2 = t0[mpi:]
            y0 = [mp]
            soln = odeint(self._func, y0, t2)
            p2 = soln[:, 0]
            p1 = mp*2 - p2[mpi:0:-1]
            self.Solution_Total = np.concatenate( (p1, p2))
        print( self.Solution_Year[0], self.Solution_Total[0])
        self.Total = self.Initial
        return


T  = np.linspace(1890, 2200, 311)

#
# Solve numerically
#
P1 = Population_Exponent( 1534.1, 9.5/1000, 22/1000)
P1.Solve( T)
P2 = Population_Velhurst( 1534.1, 35/1000, 1345, 10500, 1997)
P2.Solve( T)
P3 = Sigmoid( 1997, 0.0370, 1390, 10500)

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Year, P1.Solution_Total, "-", lw=2, color="r", label="Экспоненциальный рост")
plt.plot( P2.Solution_Year, P2.Solution_Total, "--", lw=1, color="b", label="Уравнение Ферхюльста (численное)")
plt.plot( T, P3.GetVector(T), "-", lw=2, color="b", label="Sig (средний сценарий ООН)")
plt.errorbar( P1.Calibration_Year, P1.Calibration_Total, yerr=P1.Calibration_Yerr, fmt='.', color="b", label="Население (реальное)")
plt.annotate("Псевдо-линейный рост", xy=(2005, 6555), xytext=(2030, 4900), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Псевдо-экспоненциальный рост", xy=(1964, 3512), xytext=(2000, 3900), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Экспонента плохо описывает промежуточный результат", xy=(1941, 2500), xytext=(1910, 10900), arrowprops=dict(facecolor='black', shrink=0.05))
plt.xlabel("Годы")
plt.xlim( 1900, 2200)
plt.ylabel("миллионов человек")
plt.ylim( 0, 12000)
plt.title( "Население Земли (Уравнение Ферхюльста)")
plt.grid(True)
plt.legend(loc=4)
plt.savefig( ".\\Graphs\\figure_03_04.png")
fig.show()
