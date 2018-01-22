from Utilities import *

#
# Describes population (as a Malthus-Velhurst equation)
# P0 - starting population
# Q0 - starting renewable resource
# O0 - renewable resource recovered per year
# T2 - time for population to double
# d_rate - natural renewable resource depreciation
#
class Population:
    def __init__( self, P0, Q0, O0, T2, d_rate):
        self.P_Initial = P0
        self.P = P0
        self.Q_Initial = Q0
        self.Q = Q0
        self.O_Initial = O0
        self.O = O0
        self.B = np.log(2)/T2
        self.D = d_rate
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Yerr = Load_Calibration( "Population_calibration.csv", "Year", "Delta")
        self.UN_Low = Bathtub( 1997, 0.0380, 2100, 0.0250, 1390, 12000, 1800)
        self.UN_Low.Name = "UN Low Case"
        self.UN_Medium = Sigmoid( 2003, 0.0350, 1390, 11400)
        self.UN_Medium.Name = "UN Medium Case"
        self.UN_High = Sigmoid( 2043, 0.0240, 1000, 20000)
        self.UN_High.Name = "UN High Case"
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
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.025)
        self.Solution_Year = t0
        self.Solution_Total = soln[:, 0].clip(0)
        self.Solution_Q = soln[:, 1].clip(0)
        self.Solution_O = soln[:, 2].clip(0)
        self.P = self.P_Initial
        self.Q = self.Q_Initial
        self.O = self.O_Initial
        return
