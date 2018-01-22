from Utilities import *

#
# Describes population (as a Velhurst equation)
#
class Population:
    def __init__( self, P0, b, o_left, o_right, o_year=0):
        self.Initial = P0
        self.Total = P0
        self.B = b
        self.O_left = o_left
        self.O_right = o_right
        self.Midpoint = o_year
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
            # solve for each half
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

