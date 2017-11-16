from Population import *

#
# Феноменологическая интерполяция кривых модели BAU 1972
# "Limits to Growth", 1972, график 35 на странице 124
#
class Interpolation_BAU_1972:
    def __init__( self):
        self.Population_Function_1 = Sigmoid( 1970, 0.055, 1600, 5400) #5100
        self.Population_Function_2 = Hubbert( 2050, 0.065, 0.078, 5200)
        self.Resources_Function_1 = Sigmoid( 2013, 0.052, 1200e3, 180e3)
        self.Resources_Function_2 = Hubbert( 2025, 0.150, 0.060, -180e3)
        self.Food_Function_1 = Bathtub( 1975, 0.08, 2027, 0.12, 540, 1230, 270)
        self.Food_Function_2 = Hubbert( 1932, 0.1, 0.1, 50)
        self.Food_Function_3 = Hubbert( 2012, 0.2, 0.2, 150)
        self.Food_Function_4 = Hubbert( 2065, 0.1, 0.1, -65)
        self.Industrial_Function_1 = Bathtub( 1970, 0.04, 2027, 0.09, 50, 1150, 30)
        self.Industrial_Function_2 = Hubbert( 2015, 0.12, 0.25, 430)
        self.Services_Function_1 = Bathtub( 1995, 0.035, 2035, 0.07, 120, 2600, 120)
        self.Services_Function_2 = Hubbert( 2016, 0.16, 0.2, 500)
        self.Services_Function_3 = Hubbert( 2080, 0.3, 0.3, 100)
        self.Pollution_Function_1 = Bathtub( 2012, 0.06, 2050, 0.15, 5e3, 310e3, 20e3)
        self.Pollution_Function_2 = Hubbert( 2033, 0.2, 0.2, 170e3)
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self.Population_Function_1.GetVector( t)
        self.Population += self.Population_Function_2.GetVector( t)
        self.Resources = self.Resources_Function_1.GetVector( t)
        self.Resources += self.Resources_Function_2.GetVector( t)
        self.Food_PP = self.Food_Function_1.GetVector( t)
        self.Food_PP += self.Food_Function_2.GetVector( t)
        self.Food_PP += self.Food_Function_3.GetVector( t)
        self.Food_PP += self.Food_Function_4.GetVector( t)
        self.Industrial_PP = self.Industrial_Function_1.GetVector( t)
        self.Industrial_PP += self.Industrial_Function_2.GetVector( t)
        self.Services_PP = self.Services_Function_1.GetVector( t)
        self.Services_PP += self.Services_Function_2.GetVector( t)
        self.Services_PP += self.Services_Function_3.GetVector( t)
        self.Pollution = self.Pollution_Function_1.GetVector( t)
        self.Pollution += self.Pollution_Function_2.GetVector( t)
        return

#
# Феноменологическая интерполяция кривых модели BAU 2012
# Веб-страница http://www.2052.info/
# Версия 7 ноября 2014 г
#
class Interpolation_BAU_2012:
    def __init__( self):
        self.Population_Function_1 = Sigmoid( 1950, 0.030, 1150, 3600)
        self.Population_Function_2 = Hubbert( 2038, 0.036, 0.028, 4620)
        self.Population_Function_3 = Hubbert( 1955, 0.065, 0.080, -520)
        
        self.Coal_Function_1 = Hubbert( 2032, 0.058, 0.054, 5000)
        self.Coal_Function_2 = Hubbert( 1925, 0.06, 0.05, 850)
        self.Oil_Function_1 = Hubbert( 2024, 0.050, 0.053, 4060)
        self.Oil_Function_2 = Hubbert( 1975, 0.2, 0.20, 1700)
        self.Oil_Function_3 = Hubbert( 2007, 0.070, 0.35, 500)
        self.Gas_Function_1 = Hubbert( 2036, 0.061, 0.065, 4700)
        self.Gas_Function_2 = Hubbert( 1995, 0.1, 0.2, 600)
        self.Gas_Function_3 = Hubbert( 1975, 0.15, 0.2, 400)
        self.Nuclear_Function_1 = Weibull( 1968, 0.015, 2.2, 50e3)
        self.Renewable_Function_1 = Sigmoid( 2043, 0.072, 35, 10200)
        self.Renewable_Function_2 = Hubbert( 1965, 0.05, 0.01, 110)

        self.Land_Function_1 = Sigmoid( 1920, 0.06, 800, 1300)
        self.Land_Function_2 = Hubbert( 2037.5, 0.08, 0.085, 400)
        self.Yield_Function_1 = Sigmoid( 2000, 0.042, 0.8, 6.8)
        self.Yield_Function_2 = Hubbert( 2010, 0.2, 0.06, 0.5)
        self.Yield_Function_3 = Hubbert( 2013, 1, 1, 0.2)

        self.GDP_Function_1 = Sigmoid( 2010, 0.06, 0, 130)
        self.GDP_Function_2 = Hubbert( 2050, 0.08, 0.2, 26)
        self.GDP_Function_3 = Hubbert( 1970, 0.05, 0.1, 6)
        self.Prod_Function_1 = Sigmoid( 2025, 0.042, 5000, 35000)
        self.CO2_Function_1 = Hubbert( 2062, 0.031, 0.02, 200, 280)
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self.Population_Function_1.GetVector( t)
        self.Population += self.Population_Function_2.GetVector( t)
        self.Population += self.Population_Function_3.GetVector( t)

        self.Coal = self.Coal_Function_1.GetVector( t)
        self.Coal += self.Coal_Function_2.GetVector( t)
        self.Oil = self.Oil_Function_1.GetVector( t)
        self.Oil += self.Oil_Function_2.GetVector( t)
        self.Oil += self.Oil_Function_3.GetVector( t)
        self.Gas = self.Gas_Function_1.GetVector( t)
        self.Gas += self.Gas_Function_2.GetVector( t)
        self.Gas += self.Gas_Function_3.GetVector( t)
        self.Nuclear = self.Nuclear_Function_1.GetVector( t)
        self.Renewable = self.Renewable_Function_1.GetVector( t)
        self.Renewable += self.Renewable_Function_2.GetVector( t)
        self.Total_Energy = self.Coal + self.Oil + self.Gas + self.Nuclear + self.Renewable
        
        self.Land = self.Land_Function_1.GetVector( t)
        self.Land += self.Land_Function_2.GetVector( t)
        self.Yield = self.Yield_Function_1.GetVector( t)
        self.Yield += self.Yield_Function_2.GetVector( t)
        self.Yield += self.Yield_Function_3.GetVector( t)
        self.Food = self.Yield * self.Land

        self.GDP = self.GDP_Function_1.GetVector( t)
        self.GDP += self.GDP_Function_2.GetVector( t)
        self.GDP += self.GDP_Function_3.GetVector( t)
        self.Productivity = self.Prod_Function_1.GetVector( t)
        self.CO2 = self.CO2_Function_1.GetVector( t)
        return
    def Correct_To_Actual( self, t0, t1):
        R_Time, R_Coal = Load_Calibration( "Resources_Calibration.csv", "Year", "Coal")
        R_Oil, R_Gas = Load_Calibration( "Resources_Calibration.csv", "Oil", "Gas")
        R_Nuclear, R_Renewable = Load_Calibration( "Resources_Calibration.csv", "Nuclear", "Renewable")
        diff = int( R_Time[0] - self.Time[0])
        for i in range( len( self.Time)):
            t = self.Time[i]
            if t < t0: continue
            if t > t1: break
            j = i-diff
            if j < 0: continue
            self.Coal[i] = R_Coal[j]
            self.Oil[i] = R_Oil[j]
            self.Gas[i] = R_Gas[j]
            self.Nuclear[i] = R_Nuclear[j]
            self.Renewable[i] = R_Renewable[j]
        A_Time, A_Land = Load_Calibration( "Agriculture_Calibration.csv", "Year", "Cereal_Land")
        A_Gross, A_Net = Load_Calibration( "Agriculture_Calibration.csv", "Gross_Food", "Net_Food")
        diff = int( A_Time[0] - self.Time[0])
        for i in range( len( self.Time)):
            t = self.Time[i]
            if t < t0: continue
            if t > t1: break
            j = i-diff
            if j < 0: continue
            self.Land[i] = A_Land[j]
            self.Food[i] = A_Net[j]
            self.Yield[i] = A_Net[j] / A_Land[j]
        return

#
# Феноменологическая интерполяция кривых модели BAU 2012
# с ограничением возобновляемых ресурсов технологическим максимумом 4.6 ГВт = 3530 mln toe
# Веб-страница http://www.2052.info/
# Версия 7 ноября 2014 г
#
class Interpolation_Realistic_2012:
    def __init__( self):
        self.Population_Function_1 = Sigmoid( 1950, 0.030, 1150, 3600)
        self.Population_Function_2 = Hubbert( 2038, 0.036, 0.054, 4620)
        self.Population_Function_3 = Hubbert( 1955, 0.065, 0.080, -520)
        self.Population_Function_4 = Hubbert( 2060, 0.07, 0.1, 700)
        
        self.Coal_Function_1 = Hubbert( 2032, 0.058, 0.054, 5000)
        self.Coal_Function_2 = Hubbert( 1925, 0.06, 0.05, 850)
        self.Oil_Function_1 = Hubbert( 2024, 0.050, 0.053, 4060)
        self.Oil_Function_2 = Hubbert( 1975, 0.2, 0.20, 1700)
        self.Oil_Function_3 = Hubbert( 2007, 0.070, 0.35, 500)
        self.Gas_Function_1 = Hubbert( 2036, 0.061, 0.065, 4700)
        self.Gas_Function_2 = Hubbert( 1995, 0.1, 0.2, 600)
        self.Gas_Function_3 = Hubbert( 1975, 0.15, 0.2, 400)
        self.Nuclear_Function_1 = Weibull( 1968, 0.015, 2.2, 50e3)
        self.Renewable_Function_1 = Sigmoid( 2023.5, 0.072, 35, 3530)

        self.Land_Function_1 = Sigmoid( 1920, 0.03, 800, 1400)
        self.Land_Function_2 = Hubbert( 1975, 0.3, 0.3, 100)
        self.Yield_Function_1 = Hubbert( 2018, 0.075, 0.04, 4.1, 1.2)
        self.Yield_Function_2 = Hubbert( 1975, 0.1, 0.001, 0.5)

        self.GDP_Function_1 = Sigmoid( 2010, 0.06, 0, 130)
        self.GDP_Function_2 = Hubbert( 2050, 0.08, 0.2, 26)
        self.GDP_Function_3 = Hubbert( 1970, 0.05, 0.1, 6)
        self.Prod_Function_1 = Hubbert( 2031, 0.055, 0.1, 16000, 5000)
        self.CO2_Function_1 = Hubbert( 2062, 0.031, 0.02, 200, 280)
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self.Population_Function_1.GetVector( t)
        self.Population += self.Population_Function_2.GetVector( t)
        self.Population += self.Population_Function_3.GetVector( t)
        self.Population += self.Population_Function_4.GetVector( t)

        self.Coal = self.Coal_Function_1.GetVector( t)
        self.Coal += self.Coal_Function_2.GetVector( t)
        self.Oil = self.Oil_Function_1.GetVector( t)
        self.Oil += self.Oil_Function_2.GetVector( t)
        self.Oil += self.Oil_Function_3.GetVector( t)
        self.Gas = self.Gas_Function_1.GetVector( t)
        self.Gas += self.Gas_Function_2.GetVector( t)
        self.Gas += self.Gas_Function_3.GetVector( t)
        self.Nuclear = self.Nuclear_Function_1.GetVector( t)
        self.Renewable = self.Renewable_Function_1.GetVector( t)
        self.Total_Energy = self.Coal + self.Oil + self.Gas + self.Nuclear + self.Renewable
        
        self.Land = self.Land_Function_1.GetVector( t)
        self.Land += self.Land_Function_2.GetVector( t)
        self.Yield = self.Yield_Function_1.GetVector( t)
        self.Yield += self.Yield_Function_2.GetVector( t)
        self.Food = self.Yield * self.Land

##        self.GDP = self.GDP_Function_1.GetVector( t)
##        self.GDP += self.GDP_Function_2.GetVector( t)
##        self.GDP += self.GDP_Function_3.GetVector( t)
        self.Productivity = self.Prod_Function_1.GetVector( t)
        self.GDP = self.Productivity * self.Population * 0.6e-6
        self.CO2 = self.CO2_Function_1.GetVector( t)
        return
    def Correct_To_Actual( self, t0, t1):
        R_Time, R_Coal = Load_Calibration( "Resources_Calibration.csv", "Year", "Coal")
        R_Oil, R_Gas = Load_Calibration( "Resources_Calibration.csv", "Oil", "Gas")
        R_Nuclear, R_Renewable = Load_Calibration( "Resources_Calibration.csv", "Nuclear", "Renewable")
        diff = int( R_Time[0] - self.Time[0])
        for i in range( len( self.Time)):
            t = self.Time[i]
            if t < t0: continue
            if t > t1: break
            j = i-diff
            if j < 0: continue
            if j >= len( R_Time): break
            self.Coal[i] = R_Coal[j]
            self.Oil[i] = R_Oil[j]
            self.Gas[i] = R_Gas[j]
            self.Nuclear[i] = R_Nuclear[j]
            self.Renewable[i] = R_Renewable[j]
        A_Time, A_Land = Load_Calibration( "Agriculture_Calibration.csv", "Year", "Cereal_Land")
        A_Gross, A_Net = Load_Calibration( "Agriculture_Calibration.csv", "Gross_Food", "Net_Food")
        diff = int( A_Time[0] - self.Time[0])
        for i in range( len( self.Time)):
            t = self.Time[i]
            if t < t0: continue
            if t > t1: break
            j = i-diff
            if j < 0: continue
            if j >= len( A_Time): break
            self.Land[i] = A_Land[j]
            self.Food[i] = A_Net[j]
            self.Yield[i] = A_Net[j] / A_Land[j]
        return
