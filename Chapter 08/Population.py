from Utilities import *

#
# Describes population (as a Malthus-Velhurst equation solution AKA Shark Fin)
# Peak_Year - peak population year
# Peak_Value - peak population value
# L_Slope - left slope
# R_Slope - right slope
#
class Population:
    def __init__( self, Peak_Year=2057, Peak_Value=8000, L_Slope=0.028, R_Slope=0.080):
        self._Model0 = Bathtub( -650,0.0025,2200,0.004,30,260,4200)
        self._Model1 = Hubbert( Peak_Year, L_Slope, R_Slope, Peak_Value)
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_Calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Delta = Load_Calibration( "Population_Calibration.csv", "Year", "Delta")
        self.Historical_Year, self.Historical_Total = Load_Calibration( "Earth_Historical.csv", "Year", "Population")
        self.Historical_Year, self.Historical_Delta = Load_Calibration( "Earth_Historical.csv", "Year", "Delta")
        self.UN_Low = Bathtub( 1997, 0.0380, 2100, 0.0250, 1390, 12000, 1800)
        self.UN_Low.Name = "UN Low Case"
        self.UN_Medium = Sigmoid( 2003, 0.0350, 1390, 11400)
        self.UN_Medium.Name = "UN Medium Case"
        self.UN_High = Sigmoid( 2043, 0.0240, 1000, 20000)
        self.UN_High.Name = "UN High Case"
        return
    def Solve( self, t0):
        self.Solution_Year = t0
        self.Solution_Total = self._Model0.GetVector( t0) + self._Model1.GetVector( t0)
        return self.Solution_Total
