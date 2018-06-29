from Utilities import *

#
# Provides access to historical resource extraction data
# Q0 - total resource estimate in mln tonn of oil equivalent
#
class Resources:
    def __init__( self, Q0=1200e3):
        self.Name = "PyWorld 2017"
        self.Calibration_Year, self.Calibration_Carbon = Load_Calibration( "Energy_Calibration.csv", "Year", "Total_C")
        self.Calibration_Nuclear, self.Calibration_Renewable = Load_Calibration( "Energy_Calibration.csv", "Nuclear", "Renewable")
        self.Calibration_Total = self.Calibration_Carbon + self.Calibration_Nuclear + self.Calibration_Renewable
        self.Calibration_Yerr = np.ones( len(self.Calibration_Year)) * 0.035 
        self.Calibration_Reserves = np.zeros( len(self.Calibration_Year))
        self.Calibration_Reserves[0] = Q0
        for i in range( 1, len(self.Calibration_Reserves)):
            self.Calibration_Reserves[i] = self.Calibration_Reserves[i-1] - self.Calibration_Total[i-1]
            if self.Calibration_Reserves[i] < 0.0: self.Calibration_Reserves[i] = 0.0
        return
    #
    # Creates the solution vector
    #
    def Solve( self, t0):
        self.Solution_Year = t0
        self.Solution_Total = np.zeros( len(t0))
        self.Solution_Reserves = np.zeros( len(t0))
        if t0[0] <= self.Calibration_Year[0]:
            self.Solution_Reserves[0] = self.Calibration_Reserves[0]
        else:
            for i in range( len( self.Calibration_Year)):
                if self.Calibration_Year[i] < t0[0]: continue
                self.Solution_Reserves[0] = self.Calibration_Reserves[i]
                break
        for i in range( 1, len(self.Solution_Reserves)):
            self.Solution_Reserves[i] = self.Solution_Reserves[i-1] - self.Solution_Total[i-1]
            if self.Solution_Reserves[i] < 0.0: self.Solution_Reserves[i] = 0.0
        return self.Solution_Total
    #
    # Computes the approximation
    #
    def Compute( self, t):
        tmp = 0
        return tmp
