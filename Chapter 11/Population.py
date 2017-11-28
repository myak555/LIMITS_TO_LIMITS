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
        self._Model0 = Bathtub( -650,0.0025,2200,0.004,30,260,4250)
        self._Model1 = Hubbert( Peak_Year, L_Slope, R_Slope, Peak_Value)
        self._Model2 = Hubbert( 1950, 0.2, 0.2, -250)
        self._Model3 = Hubbert( 2000, 0.1, 0.2, 150)
        self._Model4 = Hubbert( 1970, 0.3, 0.3, -50)
        self._Model5 = Hubbert( 1870, 0.1, 0.05, 120)
        self._Model6 = Hubbert( 1930, 0.2, 0.2, -50)
        self.Name = "PyWorld 2017"
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_Calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Delta = Load_Calibration( "Population_Calibration.csv", "Year", "Delta")
        self.Historical_Year, self.Historical_Total = Load_Calibration( "Earth_Historical.csv", "Year", "Population")
        self.Historical_Year, self.Historical_Delta = Load_Calibration( "Earth_Historical.csv", "Year", "Delta")
        self.UN_Low = Bathtub( 1997, 0.0380, 2100, 0.0250, 1390, 12050, 1800)
        self.UN_Low.Name = "UN Low Case"
        self.UN_Medium = Sigmoid( 2003, 0.0350, 1390, 11250)
        self.UN_Medium.Name = "UN Medium Case"
        self.UN_High = Sigmoid( 2043, 0.0240, 1000, 19650)
        self.UN_High.Name = "UN High Case"
        return
    def Solve( self, t0):
        self.Solution_Year = t0
        self.Solution_Total = self._Model0.GetVector( t0)
        self.Solution_Total += self._Model1.GetVector( t0)
        return self.Solution_Total
    def Compute( self, t):
        tmp = self._Model0.Compute( t)
        tmp += self._Model1.Compute( t)
        tmp += self._Model2.Compute( t)
        tmp += self._Model3.Compute( t)
        tmp += self._Model4.Compute( t)
        tmp += self._Model5.Compute( t)
        tmp += self._Model6.Compute( t)
        return tmp
