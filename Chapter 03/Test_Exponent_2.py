from Utilities import *

#
# Describes population as a differential equation
# P0 – initial population [mln]
# a – attrition [unitless]
# b – birth rate [unitless]
#
class Population:
    def __init__( self, P0, a, b):
        self.Initial = P0
        self.Total = P0
        self.A = a
        self.B = b
        self.Calibration_Year, self.Calibration_Total, self.Calibration_Yerr = Load_Calibration(
            "../Global Data/Population_Calibration.csv", ["Year", "Population", "Yerror"])
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

T  = np.linspace(1890, 2200, 311)

#
# Solve numerically
#
P1 = Population( 1534.1, 9.5/1000, 22/1000)
P1.Solve( T)

#
# Solve analytically
#
P2 = []
P0 = 1534.1
b = 22/1000
a = 9.5/1000

print( "P0 = {:.1f}".format(P0))
print( "a  = {:.4f}".format(a))
print( "b  = {:.4f}".format(b))
print( "Year\tNumerical\tAnalytical")
for i, t in enumerate(T):
    p = P0 * np.exp( (b-a)*(t-1890))
    P2 += [p]
    print( "{:4.0f}\t{:7.1f}\t{:7.1f}".format( t, P1.Solution_Total[i], p))

fig = plt.figure( figsize=(15,10))
plt.plot( P1.Solution_Year, P1.Solution_Total, "-", color='r', lw=1, label="Численное решение")
plt.plot( T, P2, "--", lw=1, color='b', label="Аналитическое решение")
plt.errorbar( P1.Calibration_Year, P1.Calibration_Total, yerr=P1.Calibration_Yerr, fmt='.', color='b', label="Население (реальное)")
plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов человек")
plt.ylim( 0, 25000)
plt.title( "Население Земли (численное решение)")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_03_02.png")
if InteractiveModeOn: plt.show(True)
    
