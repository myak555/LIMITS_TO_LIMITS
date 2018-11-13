from Utilities import *

#
# Provides access to historical resource extraction data
# Q0 - total resource estimate in mln tonn of oil equivalent
#
class Resources:
    def __init__( self, Q0=1200e3):
        self.Name = "PyWorld 2017"
        self.Year, self.Oil = Load_Calibration( "Resources_Calibration.csv", "Year", "Oil")
        self.Coal, self.Bitumen = Load_Calibration( "Resources_Calibration.csv", "Coal", "Bitumen")
        self.Condensate, self.NGPL = Load_Calibration( "Resources_Calibration.csv", "Condensate", "NGPL")
        self.Gas, self.Total = Load_Calibration( "Resources_Calibration.csv", "Gas", "Total")
        self.Oil_Error = self.Oil * 0.05
        self.Coal_Error = self.Coal * 0.10
        self.Bitumen_Error = self.Bitumen * 0.05
        self.Condensate_Error = self.Condensate * 0.05
        self.NGPL_Error = self.NGPL * 0.05
        self.Gas_Error = self.Gas * 0.07
        self.Total_Error = self.Total * 0.06
        self.Gas_and_Liquids = self.Oil + self.Condensate + self.NGPL + self.Gas
        self.Gas_and_Liquids_Error = self.Oil_Error + self.Condensate_Error + self.NGPL_Error + self.Gas_Error

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
