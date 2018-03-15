from Population import *
from Resources import *

#
# Феноменологическая интерполяция кривых модели BAU 1972
# "Limits to Growth", 1972, график 35 на странице 124
#
class Interpolation_BAU_1972:
    def __init__( self):
        self._Population_Functions = [Sigmoid( x0=1986.000, s0=0.03059, left=0.091, right=0.360, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2050.000, s0=0.05345, s1=0.09477, peak=0.360, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1995.000, s0=0.13373, s1=0.11916, peak=0.012, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2030.000, s0=0.17573, s1=0.17659, peak=-0.023, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2075.000, s0=0.18075, s1=0.12037, peak=0.031, shift=0.000)]
        self._Resources_Functions = [Sigmoid( x0=2006.0, s0=0.08077, left=0.999, right=0.145, shift=0.000)]
        self._Resources_Functions += [Hubbert( x0=1973.0, s0=0.05764, s1=0.16380, peak=-0.044, shift=0.000)]
        self._Resources_Functions += [Hubbert( x0=2005.5, s0=0.20335, s1=0.24725, peak=0.042, shift=0.000)]
        self._Resources_Functions += [Hubbert( x0=2025.273, s0=0.32508, s1=0.30757, peak=-0.025, shift=0.000)]
        self._Industrial_Functions = [Sigmoid( x0=2007.000, s0=0.07940, left=0.040, right=0.015, shift=0.000)]
        self._Industrial_Functions += [Hubbert( x0=2013.000, s0=0.04441, s1=0.12795, peak=0.416, shift=0.000)]
        self._Industrial_Functions += [Hubbert( x0=1947.000, s0=0.13342, s1=0.17434, peak=0.017, shift=0.000)]
        self._Industrial_Functions += [Hubbert( x0=1990.000, s0=0.20126, s1=0.16167, peak=-0.035, shift=0.000)]
        self._Industrial_Functions += [Hubbert( x0=2046.000, s0=0.21696, s1=0.21436, peak=0.016, shift=0.000)]
        self._Industrial_Functions += [Hubbert( x0=2025.500, s0=0.28751, s1=0.58459, peak=-0.038, shift=0.000)]
        self._Food_Functions = [Sigmoid( x0=2010.000, s0=0.10795, left=0.200, right=0.100, shift=0.000)]
        self._Food_Functions += [Hubbert( x0=2012.000, s0=0.05698, s1=0.10617, peak=0.315, shift=0.000)]
        self._Food_Functions += [Hubbert( x0=1931.000, s0=0.11859, s1=0.16268, peak=0.022, shift=0.000)]
        self._Food_Functions += [Hubbert( x0=1975.000, s0=0.10673, s1=0.22040, peak=0.016, shift=0.000)]
        self._Food_Functions += [Hubbert( x0=2000.000, s0=0.25105, s1=0.31381, peak=-0.016, shift=0.000)]
        self._Food_Functions += [Hubbert( x0=2062.000, s0=0.13509, s1=0.12683, peak=-0.028, shift=0.000)]
        self._Services_Functions = [Sigmoid( x0=2015.000, s0=0.05504, left=0.083, right=0.032, shift=0.000)]
        self._Services_Functions += [Hubbert( x0=2016.000, s0=0.07358, s1=0.09509, peak=0.600, shift=0.000)]
        self._Services_Functions += [Hubbert( x0=1971.000, s0=0.05663, s1=0.10172, peak=0.144, shift=0.000)]
        self._Services_Functions += [Hubbert( x0=1989.000, s0=0.14234, s1=0.18082, peak=0.034, shift=0.000)]
        self._Services_Functions += [Hubbert( x0=2045.000, s0=0.22315, s1=0.17365, peak=0.035, shift=0.000)]
        self._Services_Functions += [Hubbert( x0=2076.000, s0=0.14173, s1=0.16877, peak=0.028, shift=0.000)]
        self._Pollution_Functions = [Hubbert( x0=2034.000, s0=0.11938, s1=0.13576, peak=0.339, shift=0.000)]
        self._Pollution_Functions += [Hubbert( x0=2005.000, s0=0.07362, s1=0.12681, peak=0.058, shift=0.000)]
        self._Pollution_Functions += [Hubbert( x0=2035.000, s0=0.26795, s1=0.34906, peak=-0.017, shift=0.000)]
        self._Pollution_Functions += [Hubbert( x0=2061.000, s0=0.28971, s1=0.03610, peak=0.012, shift=0.000)]
        self._Pollution_Functions += [Hubbert( x0=1950.000, s0=0.11596, s1=0.08770, peak=0.009, shift=0.000)]
        self._Birth_Rate_Functions = [Sigmoid( x0=2030.0, s0=0.03000, left=0.850, right=1.200, shift=0.000)]
        self._Birth_Rate_Functions += [Hubbert( x0=2040.0, s0=0.03600, s1=0.05400, peak=-0.440, shift=0.000)]
        self._Birth_Rate_Functions += [Hubbert( x0=1950.0, s0=0.07700, s1=0.06300, peak=-0.055, shift=0.000)]
        self._Birth_Rate_Functions += [Hubbert( x0=2065.0, s0=0.15860, s1=0.16799, peak=-0.083, shift=0.000)]
        self._Birth_Rate_Functions += [Hubbert( x0=2000.0, s0=0.17622, s1=0.24547, peak=0.017, shift=0.000)]
        self._Death_Rate_Functions = [Sigmoid( x0=2061.0, s0=0.15144, left=0.656, right=1.300, shift=0.000)]
        self._Death_Rate_Functions += [Hubbert( x0=2038.0, s0=0.03736, s1=0.18551, peak=-0.318, shift=0.000)]
        self._Death_Rate_Functions += [Hubbert( x0=1990.0, s0=0.06712, s1=0.09413, peak=-0.154, shift=0.000)]
        self._Death_Rate_Functions += [Hubbert( x0=1960.5, s0=0.18477, s1=0.15664, peak=-0.038, shift=0.000)]
        self._Death_Rate_Functions += [Hubbert( x0=2015.0, s0=0.24664, s1=0.26527, peak=-0.032, shift=0.000)]
        return
    def Solve( self, t):
        self.Time = t
        self.Population_U = self._Interpolate_Function( self._Population_Functions)
        self.Resources_U = self._Interpolate_Function( self._Resources_Functions)
        self.Industrial_PC_U = self._Interpolate_Function( self._Industrial_Functions)
        self.Food_PC_U = self._Interpolate_Function( self._Food_Functions)
        self.Services_PC_U = self._Interpolate_Function( self._Services_Functions)
        self.Pollution_U = self._Interpolate_Function( self._Pollution_Functions)
        self.Birth_Rate_U = self._Interpolate_Function( self._Birth_Rate_Functions)
        self.Death_Rate_U = self._Interpolate_Function( self._Death_Rate_Functions)
        self.Population = self._Calibrate_Function(self.Population_U, "Population_Calibration.csv", "Year", "Population", 1930, 1970)
        self.Resources = self.Resources_U * 1186e3
        self.Industrial_PC = self._Calibrate_To_First_Value( self.Industrial_PC_U, "Industrial PC")
        self.Food_PC = self._Calibrate_To_First_Value( self.Food_PC_U, "Food PC")
        self.Services_PC = self._Calibrate_To_First_Value( self.Services_PC_U, "Services PC")
        tmp_Pop = self._Calibrate_To_First_Value( self.Population_U, "Population")
        self.Industrial = self.Industrial_PC * tmp_Pop
        self.Food = self.Food_PC * tmp_Pop
        self.Services = self.Services_PC * tmp_Pop
        self.CO2 = self.Pollution_U*600 + 305
        return
    def _Interpolate_Function(self, wavelets):
        tmp = wavelets[0].GetVector(self.Time)
        for i in range( 1, len(wavelets)):
            tmp += wavelets[i].GetVector(self.Time)
        return tmp
    def _Calibrate_Function(self, func, filename, timename, varname, start_t, stop_t, baseline=0.0):
        calibrationT, calibrationV = Load_Calibration( filename, timename, varname);
        calibrationV -= baseline
        norm = 0.0
        count = 0.0
        for i in range( len(self.Time)):
            t = self.Time[i]
            if t < start_t: continue
            if t > stop_t: continue
            v = func[i]
            for j in range(len(calibrationT)):
                if calibrationT[j] != t: continue
                norm += calibrationV[j] / v
                count += 1.0
                break
        if count < 1.0:
            print( "Calibration {:s} is out of range: {:g} to {:g}".format( varname, start_t, stop_t))
            return func
        norm /= count
        print( "Normalized {:s} from {:g} to {:g} = {:.5f}".format( varname, start_t, stop_t, norm))
        tmp = np.array( func)
        for i in range( len(self.Time)):
            tmp[i] *= norm
        return tmp + baseline
    def _Calibrate_To_First_Value(self, func, varname):
        norm = 1.0 / func[0]
        print( "Normalized {:s} to first value {:g} in {:g}".format( varname, func[0], self.Time[0]))
        tmp = np.array( func)
        for i in range( len(self.Time)):
            tmp[i] *= norm
        return tmp

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
