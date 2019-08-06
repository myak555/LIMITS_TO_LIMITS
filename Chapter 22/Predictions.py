from Population import *
from Resources import *


class _Interpolation:
    """
    Generic interpolation class for creation of phenomenological models (data fits)
    """
    def __init__( self):
        return
    def Solve( self, t):
        self.Time = t
        return
    def _Interpolate_Function(self, wavelets):
        tmp = wavelets[0].GetVector(self.Time)
        for i in range( 1, len(wavelets)):
            tmp += wavelets[i].GetVector(self.Time)
        return tmp
    def _Calibrate_Function(self, func, filename, timename, varname, start_t, stop_t, baseline=0.0):
        calibrationT, calibrationV = Load_Calibration( filename, [timename, varname]);
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
    def _Correct_To_Actual(self, func, varname):
        norm = 1.0 / func[0]
        print( "Normalized {:s} to first value {:g} in {:g}".format( varname, func[0], self.Time[0]))
        tmp = np.array( func)
        for i in range( len(self.Time)):
            tmp[i] *= norm
        return tmp
    def _Shift_To_Actual( self, func, filename, timename, varname, start_t, stop_t, norm = 1.0):
        calibrationT, calibrationV = Load_Calibration( filename, [timename, varname]);
        diff = int( calibrationT[0] - self.Time[0])
        for i in range( len( self.Time)):
            t = self.Time[i]
            if t < start_t: continue
            if t > stop_t: break
            j = i-diff
            if j < 0: continue
            if j >= len(calibrationV): continue
            func[i] = calibrationV[j] * norm
        return func


class Interpolation_BAU_1972( _Interpolation):
    """
    Phenomenological model BAU 1972
    'Limits to Growth', 1972, Graph 35 Page 124
    """
    def __init__( self):
        self.Name = "Interpolation BAU 1972"
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
        self.Population = self._Calibrate_Function(self.Population_U, "../Global Data/Population_Calibration.csv", "Year", "Population", 1930, 1970)
        self.Resources = self.Resources_U * 1186e3
        self.Energy = -Rate(self.Resources)
        self.Energy = Filter( self.Energy, matrix = [1,2,2,2,3,3,3,2,2,2,1])
        self.Energy_PC = self.Energy / self.Population 
        self.Industrial_PC = self._Calibrate_To_First_Value( self.Industrial_PC_U, "Industrial PC")
        self.Food_PC = self._Calibrate_To_First_Value( self.Food_PC_U, "Food PC")
        self.Services_PC = self._Calibrate_To_First_Value( self.Services_PC_U, "Services PC")
        tmp_Pop = self._Calibrate_To_First_Value( self.Population_U, "Population")
        self.Industrial = self.Industrial_PC * tmp_Pop
        self.Food = self.Food_PC * tmp_Pop
        self.Services = self.Services_PC * tmp_Pop
        self.GDP_PC = (2.0*self.Industrial_PC+self.Services_PC+self.Food_PC)*.8
        self.CO2 = self.Pollution_U*600 + 305
        return


class Interpolation_BAU_2002( _Interpolation):
    """
    Phenomenological model BAU 2002
    'Limits to Growth', 2002, Graph 4-11 Page 169
    """
    def __init__( self):
        self.Name = "Interpolation BAU 2002"
        self._Population_Functions = [Hubbert( x0=2028.000, s0=0.037, s1=0.038, peak=0.500, shift=0.130)]
        self._Population_Functions += [Hubbert( x0=2112.000, s0=0.065, s1=0.065, peak=0.062)]
        self._Resources_Functions = [Sigmoid( x0=2010.000, s0=0.062, left=0.500, right=0.094)]
        self._Resources_Functions += [Hubbert( x0=2028.000, s0=0.183, s1=0.095, peak=-0.024)]
        self._Resources_Functions += [Hubbert( x0=2007.000, s0=0.150, s1=0.150, peak=0.013)]
        self._Industrial_Functions = [Hubbert( x0=2016.000, s0=0.09678, s1=0.12761, peak=0.630)]
        self._Industrial_Functions += [Hubbert( x0=1990.000, s0=0.04084, s1=0.12976, peak=0.230)]
        self._Industrial_Functions += [Hubbert( x0=2042.000, s0=0.13235, s1=0.06880, peak=0.153)]
        self._Industrial_Functions += [Hubbert( x0=2090.000, s0=0.18530, s1=0.06461, peak=0.019)]
        self._Industrial_Functions += [Hubbert( x0=1965.000, s0=0.07977, s1=0.14711, peak=-0.024)]
        self._Industrial_Functions += [Hubbert( x0=1915.000, s0=0.28243, s1=0.20589, peak=0.008)]
        self._Food_Functions = [Hubbert( x0=2015.000, s0=0.05061, s1=0.07521, peak=0.455, shift=0.071)]
        self._Food_Functions += [Hubbert( x0=1970.000, s0=0.05075, s1=0.07107, peak=0.061)]
        self._Food_Functions += [Hubbert( x0=2060.000, s0=0.07322, s1=0.02726, peak=0.087)]
        self._Pollution_Functions = [Hubbert( x0=2035.000, s0=0.08381, s1=0.06993, peak=0.284)]
        self._Pollution_Functions += [Hubbert( x0=1995.000, s0=0.07107, s1=0.13509, peak=0.051)]
        self._Pollution_Functions += [Hubbert( x0=2085.000, s0=0.10807, s1=0.06333, peak=0.026)]
        self._Pollution_Functions += [Hubbert( x0=1945.000, s0=0.03730, s1=0.07249, peak=0.017)]

##        self._TFR_Functions += [Hubbert( x0=2015.000, s0=0.05181, s1=0.08227, peak=0.544, shift=0.318)]

        self._LEB_Functions = [Hubbert( x0=2015.000, s0=0.05181, s1=0.08227, peak=0.544, shift=0.318)]
        self._LEB_Functions += [Hubbert( x0=2052.000, s0=0.15083, s1=0.12216, peak=0.085)]
        self._LEB_Functions += [Hubbert( x0=1965.000, s0=0.13208, s1=0.08595, peak=0.104)]
        self._LEB_Functions += [Hubbert( x0=1941.000, s0=1.50000, s1=0.13373, peak=0.081)]
        self._LEB_Functions += [Hubbert( x0=1925.000, s0=0.16671, s1=0.13107, peak=0.016)]
        self._LEB_Functions += [Hubbert( x0=2000.547, s0=0.25419, s1=0.34519, peak=-0.020)]
        self._GoodsPC_Functions = [Hubbert( x0=2016.000, s0=0.05212, s1=0.11756, peak=0.596, shift=0.026)]
        self._GoodsPC_Functions += [Hubbert( x0=1965.000, s0=0.03553, s1=0.09249, peak=0.161)]
        self._GoodsPC_Functions += [Hubbert( x0=2040.000, s0=0.28863, s1=0.06191, peak=0.119)]
        self._GoodsPC_Functions += [Hubbert( x0=1940.073, s0=0.20589, s1=0.16677, peak=0.010)]
        self._GoodsPC_Functions += [Hubbert( x0=1982.696, s0=0.31381, s1=0.25419, peak=0.008)]
        self._GoodsPC_Functions += [Hubbert( x0=2038.433, s0=0.31534, s1=0.67948, peak=-0.010)]
        self._FoodPC_Functions = [Hubbert( x0=2008.000, s0=0.05010, s1=0.06942, peak=0.282, shift=0.170)]
        self._FoodPC_Functions += [Hubbert( x0=2100.000, s0=0.04434, s1=0.05100, peak=0.051)]
        self._FoodPC_Functions += [Hubbert( x0=1965.000, s0=0.02241, s1=0.08077, peak=0.149)]
        self._FoodPC_Functions += [Hubbert( x0=1950.000, s0=0.07662, s1=0.32816, peak=0.019)]
        self._FoodPC_Functions += [Hubbert( x0=1975.000, s0=0.14859, s1=0.58459, peak=-0.007)]
        self._ServicesPC_Functions = [Hubbert( x0=2020.000, s0=0.05646, s1=0.08902, peak=0.505, shift=0.084)]
        self._ServicesPC_Functions += [Hubbert( x0=1975.000, s0=0.09257, s1=0.11650, peak=0.093)]
        self._ServicesPC_Functions += [Hubbert( x0=1950.000, s0=0.05629, s1=0.14711, peak=0.061)]
        self._ServicesPC_Functions += [Hubbert( x0=2057.000, s0=0.11718, s1=0.07754, peak=0.087)]
        self._HDI_Functions = [Hubbert( x0=2018.000, s0=0.03417, s1=0.11852, peak=0.607, shift=0.159)]
        self._HDI_Functions += [Hubbert( x0=2047.723, s0=0.12780, s1=0.08512, peak=0.150)]
        self._HDI_Functions += [Hubbert( x0=1941.000, s0=4.50353, s1=0.10612, peak=0.042)]
        self._HDI_Functions += [Hubbert( x0=2005.282, s0=0.55038, s1=0.28243, peak=0.022)]
        self._HDI_Functions += [Hubbert( x0=1985.246, s0=0.22877, s1=0.27681, peak=-0.018)]
        self._HDI_Functions += [Hubbert( x0=2025.137, s0=0.38931, s1=0.47351, peak=-0.019)]
        self._EcoFootprint_Functions = [Hubbert( x0=2019.000, s0=0.08905, s1=0.12871, peak=0.446, shift=0.121)]
        self._EcoFootprint_Functions += [Hubbert( x0=2045.000, s0=0.17272, s1=0.03265, peak=0.185)]
        self._EcoFootprint_Functions += [Hubbert( x0=2042.000, s0=0.3, s1=0.3, peak=-0.03)]
        self._EcoFootprint_Functions += [Hubbert( x0=1987.000, s0=0.05569, s1=0.11735, peak=0.125)]
        self._EcoFootprint_Functions += [Hubbert( x0=2100.000, s0=0.15000, s1=0.15000, peak=0.034)]
        self._EcoFootprint_Functions += [Hubbert( x0=2035.000, s0=0.22493, s1=1.65925, peak=0.008)]
        self._EcoFootprint_Functions += [Hubbert( x0=1940.000, s0=0.13342, s1=0.20589, peak=0.011)]
        return
    def Solve( self, t):
        self.Time = t
        self.Population_U = self._Interpolate_Function( self._Population_Functions)
        self.Resources_U = self._Interpolate_Function( self._Resources_Functions)
        self.Industrial_U = self._Interpolate_Function( self._Industrial_Functions)
        self.Food_U = self._Interpolate_Function( self._Food_Functions)
        self.Pollution_U = self._Interpolate_Function( self._Pollution_Functions)
        #self.TFR_U = self._Interpolate_Function( self._LEB_Functions)
        self.LEB_U = self._Interpolate_Function( self._LEB_Functions)
        self.GoodsPC_U = self._Interpolate_Function( self._GoodsPC_Functions)
        self.FoodPC_U = self._Interpolate_Function( self._FoodPC_Functions)
        self.ServicesPC_U = self._Interpolate_Function( self._ServicesPC_Functions)
        self.Services_U = self.ServicesPC_U * self.Population_U
        self.HDI = self._Interpolate_Function( self._HDI_Functions)
        self.EcoFootprint = 4.0 * self._Interpolate_Function( self._EcoFootprint_Functions)
        # Model calibrations:
        # Population = 0..12e9 - from Appendix 1, page 288. Best fit to the UN data 2015: 11.75e9
        self.Population = self.Population_U * 12000 # in million 
        # Resources = 0..2e12 - from Appendix 1, page 288. Best fit to energy estimates: 2.4e9 tonn
        # Fossil energy fraction in total production assumed 0.55
        self.Resources = self.Resources_U * 2400e3 # in million tonn
        self.Energy = -Rate(self.Resources) * 0.55 + 800
        # Industrial output = 0..4e9 tonn - from Appendix 1, page 288
        self.Industrial = self.Industrial_U * 4000 # in million tonn 
        # Pollution = 0..40 (index) - from Appendix 1, page 288
        self.Pollution = self.Pollution_U * 40 
        # Food = 0..6e9 tonn - from Appendix 1, page 288
        self.Food = self.Food_U * 6000 # in million tonn
        # Food per capita = 0..1000 kg - from Appendix 1, page 288.
        self.FoodPC = self.FoodPC_U * 1000 
        self.Food_Chk = self.FoodPC * self.Population / 1000 # in million tonn
        # Goods per capita = 0..250 kg - from Appendix 1, page 288.
        self.GoodsPC = self.GoodsPC_U * 250
        self.Goods = np.array(self.GoodsPC) / 1000
        self.Goods *= self.Population # million tonn
        # Services per capita = 0..1000 units(?) - from Appendix 1, page 288.
        self.ServicesPC = self.ServicesPC_U * 1000 
        self.Services = np.array(self.ServicesPC) / 1000
        self.Services *= self.Population # in billion $
        # LEB = 0..90 - from Appendix 1, page 288. Note unexplained jump from 34 in 1938 to 42 in 1941
        self.LEB = self.LEB_U * 90 # in years 
        return


class Interpolation_BAU_2012( _Interpolation):
    """
    Phenomenological model BAU 2012
    http://www.2052.info/, 07-Nov-2014
    """
    def __init__( self):
        self.Name = "Interpolation Randers 2012"
        self._Population_Functions = [Sigmoid( 1950, 0.030, 1150, 3600)]
        self._Population_Functions += [Hubbert( 2038, 0.036, 0.028, 4620)]
        self._Population_Functions += [Hubbert( 1955, 0.065, 0.080, -520)]

        self._Coal_Functions = [Hubbert( 2032, 0.058, 0.054, 5000)]
        self._Coal_Functions += [Hubbert( 1925, 0.06, 0.05, 850)]
        self._Oil_Functions = [Hubbert( 2024, 0.050, 0.053, 4060)]
        self._Oil_Functions += [Hubbert( 1975, 0.2, 0.20, 1700)]
        self._Oil_Functions += [Hubbert( 2007, 0.070, 0.35, 500)]
        self._Gas_Functions = [Hubbert( 2036, 0.061, 0.065, 4700)]
        self._Gas_Functions += [Hubbert( 1995, 0.1, 0.2, 600)]
        self._Gas_Functions += [Hubbert( 1975, 0.15, 0.2, 400)]
        self._Nuclear_Functions = [Weibull( 1968, .015, 2.2, 50000)]
        self._Renewable_Functions = [Sigmoid( 2043, 0.072, 35, 10200)]
        self._Renewable_Functions += [Hubbert( 1965, 0.05, 0.01, 110)]

        self._Land_Functions = [Sigmoid( 1920, 0.06, 800, 1300)]
        self._Land_Functions += [Hubbert( 2037.5, 0.08, 0.085, 400)]
        self._Yield_Functions = [Sigmoid( 2000, 0.042, 0.8, 6.8)]
        self._Yield_Functions += [Hubbert( 2010, 0.2, 0.06, 0.5)]
        self._Yield_Functions += [Hubbert( 2013, 1, 1, 0.2)]

        self._GDP_Functions = [Sigmoid( 2010, 0.06, 0, 130)]
        self._GDP_Functions += [Hubbert( 2050, 0.08, 0.2, 26)]
        self._GDP_Functions += [Hubbert( 1970, 0.12, 0.1, 6)]

        self._Prod_Functions = [Sigmoid( 2025, 0.042, 5000, 35000)]
        self._CO2_Functions = [Hubbert( 2062, 0.031, 0.02, 200, 280)]
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self._Interpolate_Function( self._Population_Functions)

        self.Coal = self._Interpolate_Function( self._Coal_Functions)
        self.Oil = self._Interpolate_Function( self._Oil_Functions)
        self.Gas = self._Interpolate_Function( self._Gas_Functions)
        self.Nuclear = self._Interpolate_Function( self._Nuclear_Functions)
        self.Renewable = self._Interpolate_Function( self._Renewable_Functions)
        self.Energy_Carbon = self.Coal + self.Oil + self.Gas
        self.Resources = 1200e3 - Cumulative(self.Energy_Carbon)
        self.Energy = self.Energy_Carbon + self.Nuclear + self.Renewable
        self.Energy_PC = self.Energy / self.Population
        self.Land = self._Interpolate_Function( self._Land_Functions)
        self.Yield = self._Interpolate_Function( self._Yield_Functions)
        self.Food = self.Yield * self.Land
        self.Food_PC = self.Food / self.Population
        self.GDP = self._Interpolate_Function( self._GDP_Functions)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        self.Productivity = self._Interpolate_Function( self._Prod_Functions) / 365
        self.CO2 = self._Interpolate_Function( self._CO2_Functions)
        return
    def Correct_To_Actual( self, t0, t1):
        self.Coal = self._Shift_To_Actual( self.Coal, "../Global Data/Energy_Calibration.csv", "Year", "Coal", t0, t1)
        self.Oil = self._Shift_To_Actual( self.Oil, "../Global Data/Energy_Calibration.csv", "Year", "Oil", t0, t1)
        self.Gas = self._Shift_To_Actual( self.Gas, "../Global Data/Energy_Calibration.csv", "Year", "Gas", t0, t1)
        self.Nuclear = self._Shift_To_Actual( self.Nuclear, "../Global Data/Energy_Calibration.csv", "Year", "Nuclear", t0, t1)
        self.Renewable = self._Shift_To_Actual( self.Renewable, "../Global Data/Energy_Calibration.csv", "Year", "Renewable", t0, t1)
        self.Energy = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total", t0, t1)
        self.Energy_Carbon = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total_C", t0, t1)
        self.Energy_PC = self.Energy / self.Population

        self.Land = self._Shift_To_Actual( self.Land, "../Global Data/Agriculture_Calibration.csv", "Year", "Cereal_Land", t0, t1)
        self.Food = self._Shift_To_Actual( self.Food, "../Global Data/Agriculture_Calibration.csv", "Year", "Net_Food", t0, t1)
        self.Yield = self.Food / self.Land
        self.Food_PC = self.Food / self.Population

        self.GDP = self._Shift_To_Actual( self.GDP, "../Global Data/GDP_World_Bank.csv", "Year", "GDP_IA", t0, t1)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        return


class Interpolation_Realistic_2012( _Interpolation):
    """
    Phenomenological model BAU 2012
    with tecnological limit 4.6 GW = 3530 mln toe
    """
    def __init__( self):
        self.Name = "Interpolation BAU 2012"
        self._Population_Functions = [Sigmoid( x0=2002.000, s0=0.03300, left=958.000, right=11600.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1855.500, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1903.000, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1951.000, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1964.000, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1992.000, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2010.000, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2037.800, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self._Population_Functions += [Sigmoid( x0=2079.000, s0=0.10212, left=0.000, right=-6912.095, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1942.000, s0=0.13107, s1=0.06064, peak=67.606, shift=0.000)]

        self._Coal_Functions = [Hubbert( 2032, 0.058, 0.054, 5000)]
        self._Coal_Functions += [Hubbert( 1925, 0.06, 0.05, 850)]
        self._Oil_Functions = [Hubbert( 2024, 0.050, 0.053, 4060)]
        self._Oil_Functions += [Hubbert( 1975, 0.2, 0.20, 1700)]
        self._Oil_Functions += [Hubbert( 2007, 0.070, 0.35, 500)]
        self._Gas_Functions = [Hubbert( 2036, 0.061, 0.065, 4700)]
        self._Gas_Functions += [Hubbert( 1995, 0.1, 0.2, 600)]
        self._Gas_Functions += [Hubbert( 1975, 0.15, 0.2, 400)]

        self._Nuclear_Functions = [Weibull( 1968, .018, 2.2, 40000)]
        self._Nuclear_Functions += [Hubbert( 2013, 0.3, 0.3, -100)]
        self._Nuclear_Functions += [Hubbert( 2028, 0.4, 0.29, 70)]
        self._Nuclear_Functions += [Hubbert( 2038, 0.4, 0.4, -70)]
        self._Nuclear_Functions += [Hubbert( 2052, 0.4, 0.4, 40)]
        self._Nuclear_Functions += [Sigmoid( 2063, .08, 0, 1550)]

        self._Renewable_Functions = [Sigmoid( x0=2022.500, s0=0.07600, left=49.000, right=3550.000, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1985.000, s0=0.08724, s1=0.19580, peak=215.000, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1948.000, s0=0.07937, s1=0.14622, peak=55.132, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1996.000, s0=0.54621, s1=0.62879, peak=69.368, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=2010.000, s0=0.27615, s1=0.37971, peak=-84.426, shift=0.000)]

        self._Land_Functions = [Sigmoid( 1920, 0.03, 800, 1400)]
        self._Land_Functions += [Hubbert( 1975, 0.3, 0.3, 100)]
        self._Yield_Functions = [Hubbert( x0=2025.000, s0=0.05802, s1=0.04271, peak=5.200, shift=1.000)]
        self._Yield_Functions += [Hubbert( x0=1974.000, s0=0.09749, s1=0.12311, peak=0.483, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=1983.000, s0=0.97990, s1=0.97010, peak=0.093, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=2003.000, s0=0.43013, s1=0.59049, peak=-0.172, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=2015.000, s0=0.55593, s1=0.47351, peak=0.200, shift=0.000)]

        self._GDP_Functions = [Hubbert( x0=2012.000, s0=0.16000, s1=0.03800, peak=72.000, shift=0.800)]
        self._GDP_Functions += [Hubbert( x0=1979.000, s0=0.13438, s1=0.24664, peak=28.244, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1993.000, s0=0.42148, s1=0.40122, peak=29.443, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1954.000, s0=0.16268, s1=0.31071, peak=2.300, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1970.000, s0=0.53144, s1=0.34093, peak=-4.744, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2032.000, s0=0.16345, s1=0.16673, peak=-5.645, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2100, s0=0.203, s1=0.203, peak=4.571, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2020, s0=0.60541, s1=0.60515, peak=-3.391, shift=0.000)]

        self._Prod_Functions = [Sigmoid( 2025, 0.042, 5000, 35000)]
        self._CO2_Functions = [Hubbert( 2062, 0.031, 0.02, 200, 280)]
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self._Interpolate_Function( self._Population_Functions)
        self.Coal = self._Interpolate_Function( self._Coal_Functions)
        self.Oil = self._Interpolate_Function( self._Oil_Functions)
        self.Gas = self._Interpolate_Function( self._Gas_Functions)
        self.Nuclear = self._Interpolate_Function( self._Nuclear_Functions)
        self.Renewable = self._Interpolate_Function( self._Renewable_Functions)
        self.Energy_Carbon = self.Coal + self.Oil + self.Gas
        self.Resources = 1200e3 - Cumulative(self.Energy_Carbon)
        self.Energy = self.Energy_Carbon + self.Nuclear + self.Renewable
        self.Energy_PC = self.Energy / self.Population
        self.Land = self._Interpolate_Function( self._Land_Functions)
        self.Yield = self._Interpolate_Function( self._Yield_Functions)
        self.Food = self.Yield * self.Land
        self.Food_PC = self.Food / self.Population
        self.GDP = self._Interpolate_Function( self._GDP_Functions)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        self.Productivity = self._Interpolate_Function( self._Prod_Functions) / 365
        self.CO2 = self._Interpolate_Function( self._CO2_Functions)
        return
    def Correct_To_Actual( self, t0, t1):
        self.Coal = self._Shift_To_Actual( self.Coal, "../Global Data/Energy_Calibration.csv", "Year", "Coal", t0, t1)
        self.Oil = self._Shift_To_Actual( self.Oil, "../Global Data/Energy_Calibration.csv", "Year", "Oil", t0, t1)
        self.Gas = self._Shift_To_Actual( self.Gas, "../Global Data/Energy_Calibration.csv", "Year", "Gas", t0, t1)
        self.Nuclear = self._Shift_To_Actual( self.Nuclear, "../Global Data/Energy_Calibration.csv", "Year", "Nuclear", t0, t1)
        self.Renewable = self._Shift_To_Actual( self.Renewable, "../Global Data/Energy_Calibration.csv", "Year", "Renewable", t0, t1)
        self.Energy_Carbon = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total_C", t0, t1)
        self.Energy = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total", t0, t1)
        self.Energy_PC = self.Energy / self.Population

        self.Land = self._Shift_To_Actual( self.Land, "../Global Data/Agriculture_Calibration.csv", "Year", "Cereal_Land", t0, t1)
        self.Food = self._Shift_To_Actual( self.Food, "../Global Data/Agriculture_Calibration.csv", "Year", "Net_Food", t0, t1)
        self.Yield = self.Food / self.Land
        self.Food_PC = self.Food / self.Population

        self.GDP = self._Shift_To_Actual( self.GDP, "../Global Data/GDP_World_Bank.csv", "Year", "GDP_IA", t0, t1)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        return


class Interpolation_Realistic_2018( _Interpolation):
    """
    Phenomenological model BAU 2012
    with tecnological limit 4.6 GW = 3530 mln toe
    and carbon fuel URR = 1200 bln toe
    """
    def __init__( self):
        self.Name = "Interpolation BAU 2018"
        self._Population_Functions = [Sigmoid( x0=2002.000, s0=0.03300, left=958.000, right=11600.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1855.500, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1903.000, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1951.000, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1964.000, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1992.000, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2010.000, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=2037.800, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self._Population_Functions += [Sigmoid( x0=2079.000, s0=0.10212, left=0.000, right=-6912.095, shift=0.000)]
        self._Population_Functions += [Hubbert( x0=1942.000, s0=0.13107, s1=0.06064, peak=67.606, shift=0.000)]

        self._Coal_Functions = [Hubbert( 2032, 0.058, 0.054, 5000)]
        self._Coal_Functions += [Hubbert( 1925, 0.06, 0.05, 850)]
        self._Oil_Functions = [Hubbert( 2024, 0.050, 0.053, 4060)]
        self._Oil_Functions += [Hubbert( 1975, 0.2, 0.20, 1700)]
        self._Oil_Functions += [Hubbert( 2007, 0.070, 0.35, 500)]
        self._Gas_Functions = [Hubbert( 2036, 0.061, 0.065, 4700)]
        self._Gas_Functions += [Hubbert( 1995, 0.1, 0.2, 600)]
        self._Gas_Functions += [Hubbert( 1975, 0.15, 0.2, 400)]

        self._Nuclear_Functions = [Weibull( 1968, .018, 2.2, 40000)]
        self._Nuclear_Functions += [Hubbert( 2013, 0.3, 0.3, -100)]
        self._Nuclear_Functions += [Hubbert( 2028, 0.4, 0.29, 70)]
        self._Nuclear_Functions += [Hubbert( 2038, 0.4, 0.4, -70)]
        self._Nuclear_Functions += [Hubbert( 2052, 0.4, 0.4, 40)]
        self._Nuclear_Functions += [Sigmoid( 2063, .08, 0, 1550)]

        self._Renewable_Functions = [Sigmoid( x0=2022.500, s0=0.07600, left=49.000, right=3550.000, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1985.000, s0=0.08724, s1=0.19580, peak=215.000, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1948.000, s0=0.07937, s1=0.14622, peak=55.132, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=1996.000, s0=0.54621, s1=0.62879, peak=69.368, shift=0.000)]
        self._Renewable_Functions += [Hubbert( x0=2010.000, s0=0.27615, s1=0.37971, peak=-84.426, shift=0.000)]

        self._Land_Functions = [Sigmoid( 1920, 0.03, 800, 1400)]
        self._Land_Functions += [Hubbert( 1975, 0.3, 0.3, 100)]
        self._Yield_Functions = [Hubbert( x0=2025.000, s0=0.05802, s1=0.04271, peak=5.200, shift=1.000)]
        self._Yield_Functions += [Hubbert( x0=1974.000, s0=0.09749, s1=0.12311, peak=0.483, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=1983.000, s0=0.97990, s1=0.97010, peak=0.093, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=2003.000, s0=0.43013, s1=0.59049, peak=-0.172, shift=0.000)]
        self._Yield_Functions += [Hubbert( x0=2015.000, s0=0.55593, s1=0.47351, peak=0.200, shift=0.000)]

        self._GDP_Functions = [Hubbert( x0=2012.000, s0=0.16000, s1=0.03800, peak=72.000, shift=0.800)]
        self._GDP_Functions += [Hubbert( x0=1979.000, s0=0.13438, s1=0.24664, peak=28.244, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1993.000, s0=0.42148, s1=0.40122, peak=29.443, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1954.000, s0=0.16268, s1=0.31071, peak=2.300, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=1970.000, s0=0.53144, s1=0.34093, peak=-4.744, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2032.000, s0=0.16345, s1=0.16673, peak=-5.645, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2100, s0=0.203, s1=0.203, peak=4.571, shift=0.000)]
        self._GDP_Functions += [Hubbert( x0=2020, s0=0.60541, s1=0.60515, peak=-3.391, shift=0.000)]

        self._Prod_Functions = [Sigmoid( 2025, 0.042, 5000, 35000)]
        self._CO2_Emission_Functions = [Hubbert( x0=2025.000, s0=0.04000, s1=0.04000, peak=38400.000, shift=0.000)]
        self._CO2_Emission_Functions += [Hubbert( x0=1913.000, s0=0.08261, s1=0.10550, peak=1653.634, shift=0.000)]
        self._CO2_Emission_Functions += [Hubbert( x0=1973.500, s0=0.41976, s1=0.43597, peak=2525.000, shift=0.000)]
        self._CO2_Emission_Functions += [Hubbert( x0=2000.000, s0=0.22813, s1=0.34509, peak=-4810.824, shift=0.000)]
        self._CO2_Emission_Functions += [Hubbert( x0=1950.000, s0=0.44788, s1=0.34174, peak=-615.293, shift=0.000)]
        self._CO2_Functions = [Hubbert( 2062, 0.031, 0.02, 192, 284)]
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self._Interpolate_Function( self._Population_Functions)
        self.Coal = self._Interpolate_Function( self._Coal_Functions)
        self.Oil = self._Interpolate_Function( self._Oil_Functions)
        self.Gas = self._Interpolate_Function( self._Gas_Functions)
        self.Nuclear = self._Interpolate_Function( self._Nuclear_Functions)
        self.Renewable = self._Interpolate_Function( self._Renewable_Functions)
        self.Energy_Carbon = self.Coal + self.Oil + self.Gas
        self.Resources = 1400e3 - Cumulative(self.Energy_Carbon)
        self.Energy = self.Energy_Carbon + self.Nuclear + self.Renewable
        self.Energy_PC = self.Energy / self.Population
        self.Land = self._Interpolate_Function( self._Land_Functions)
        self.Yield = self._Interpolate_Function( self._Yield_Functions)
        self.Food = self.Yield * self.Land
        self.Food_PC = self.Food / self.Population
        self.GDP = self._Interpolate_Function( self._GDP_Functions)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        self.Productivity = self._Interpolate_Function( self._Prod_Functions) / 365
        self.CO2_Emissions = self._Interpolate_Function( self._CO2_Emission_Functions)
        self.CO2 = self._Interpolate_Function( self._CO2_Functions)
        return
    def Correct_To_Actual( self, t0, t1):
        self.Coal = self._Shift_To_Actual( self.Coal, "../Global Data/Energy_Calibration.csv", "Year", "Coal", t0, t1)
        self.Oil = self._Shift_To_Actual( self.Oil, "../Global Data/Energy_Calibration.csv", "Year", "Oil", t0, t1)
        self.Gas = self._Shift_To_Actual( self.Gas, "../Global Data/Energy_Calibration.csv", "Year", "Gas", t0, t1)
        self.Nuclear = self._Shift_To_Actual( self.Nuclear, "../Global Data/Energy_Calibration.csv", "Year", "Nuclear", t0, t1)
        self.Renewable = self._Shift_To_Actual( self.Renewable, "../Global Data/Energy_Calibration.csv", "Year", "Renewable", t0, t1)
        self.Energy_Carbon = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total_C", t0, t1)
        self.Energy = self._Shift_To_Actual( self.Energy, "../Global Data/Energy_Calibration.csv", "Year", "Total", t0, t1)
        self.Energy_PC = self.Energy / self.Population

        self.Land = self._Shift_To_Actual( self.Land, "../Global Data/Agriculture_Calibration.csv", "Year", "Cereal_Land", t0, t1)
        self.Food = self._Shift_To_Actual( self.Food, "../Global Data/Agriculture_Calibration.csv", "Year", "Net_Food", t0, t1)
        self.Yield = self.Food / self.Land
        self.Food_PC = self.Food / self.Population

        self.GDP = self._Shift_To_Actual( self.GDP, "../Global Data/GDP_World_Bank.csv", "Year", "GDP_IA", t0, t1)
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365
        self.GDP_PC = self.GDP / self.Population * 1000000 / 365

        self.CO2 = self._Shift_To_Actual( self.CO2, "../Global Data/Ice_Core_Law_Dome.csv", "Year", "Total", t0, t1)
        self.CO2 = self._Shift_To_Actual( self.CO2, "../Global Data/CO2_Mauna_Loa.csv", "Year", "Mean", t0, t1)
        self.CO2_Emissions = self._Shift_To_Actual( self.CO2_Emissions, "../Global Data/CO2_Calibration.csv", "Year", "Total", t0, t1)
        return


#
# Test code
#
if __name__ == "__main__":
    help( _Interpolation)
    help( Interpolation_BAU_1972)
    help( Interpolation_BAU_2002)
    help( Interpolation_BAU_2012)
    help( Interpolation_Realistic_2012)
    help( Interpolation_Realistic_2018)

    model = Interpolation_BAU_2002()
    model.Solve( np.linspace(1900, 2100, 201))

    FPC30 = 0
    GPC30 = 0
    SPC30 = 0
    HDI30 = 0
    FPC60 = 0
    GPC60 = 0
    SPC60 = 0
    HDI60 = 0
    for i,y in enumerate( model.Time):
        if y == 1930:
            FPC30 = model.FoodPC[i]
            GPC30 = model.GoodsPC[i]
            SPC30 = model.ServicesPC[i]
            HDI30 = model.HDI[i]
        if y == 1960:
            FPC60 = model.FoodPC[i]
            GPC60 = model.GoodsPC[i]
            SPC60 = model.ServicesPC[i]
            HDI60 = model.HDI[i]
        if model.FoodPC[i] > FPC30: yFPC30 = y
        if model.GoodsPC[i] > GPC30: yGPC30 = y
        if model.ServicesPC[i] > SPC30: ySPC30 = y
        if model.HDI[i] > HDI30: yHDI30 = y
        if model.FoodPC[i] > FPC60: yFPC60 = y
        if model.GoodsPC[i] > GPC60: yGPC60 = y
        if model.ServicesPC[i] > SPC60: ySPC60 = y
        if model.HDI[i] > HDI60: yHDI60 = y
    print( "Back to the level of 1960:")
    print( "   Food per capita    : {:.0f} kg in {:.0f}".format( FPC60, yFPC60))
    print( "   Goods per capita   : {:.0f} kg in {:.0f}".format( GPC60, yGPC60))
    print( "   Services per capita: {:.0f} eq.$ in {:.0f}".format( SPC60, ySPC60))
    print( "   HDI                : {:.2f} in {:.0f}".format( HDI60, yHDI60))
    print( "Back to the level of 1930:")
    print( "   Food per capita    : {:.0f} kg in {:.0f}".format( FPC30, yFPC30))
    print( "   Goods per capita   : {:.0f} kg in {:.0f}".format( GPC30, yGPC30))
    print( "   Services per capita: {:.0f} eq.$ in {:.0f}".format( SPC30, ySPC30))
    print( "   HDI                : {:.2f} in {:.0f}".format( HDI30, yHDI30))
    
    limits = 1900, 2100
    fig = plt.figure( figsize=(15,20))
    fig.suptitle( "WORLD3 (версия 2002 г)", fontsize=28)
    gs = plt.GridSpec(3, 1, height_ratios=[1,1,1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    ax1.set_title("Состояние мира", fontsize=18)
    ax1.plot( model.Time, model.Population/1000, "-", lw=3, color="b", label="Население (10^9)")
    ax1.plot( model.Time, model.Resources/100, "-", lw=2, color="k", label="Природные ресурсы (10^11 т)")
    ax1.plot( model.Time, model.Industrial/1000, "-", lw=2, color="r", label="Промышленость (10^9 т)")
    ax1.plot( model.Time, model.Goods/1000, "--", lw=2, color="r", label="Потребтовары (10^9 т)")
    ax1.plot( model.Time, model.Food/1000, "-", lw=2, color="g", label="Сельское хоз-во (10^9 т)")
    ax1.plot( model.Time, model.Food_Chk/1000, ".", lw=2, color="g")
    ax1.plot( model.Time, model.Services/1000, "-", lw=2, color="y", label="Услуги (10^15 усл.$)")
    ax1.plot( model.Time, model.Pollution, "-", lw=2, color="m", label="Загрязнения")
    ax1.plot( [2002, 2002], [0,10], "--", lw=2, color="k")
    ax1.set_xlim( limits)
    #ax1.set_ylim( 0, 1)
    ax1.set_ylabel("Единиц")
    ax1.grid(True)
    ax1.legend(loc=2)

    ax2.set_title("Стандарт жизни", fontsize=18)
    ax2.plot( model.Time, model.LEB_U, "-", lw=2, color="b", label="LEB")
    ax2.plot( model.Time, model.GoodsPC_U, "--", lw=2, color="r", label="Промтовары/душу")
    #ax2.plot( model.Time, model.GoodsPC_Chk, "-.", lw=2, color="r")
    ax2.plot( model.Time, model.FoodPC_U, "--", lw=2, color="g", label="Продовольствие/душу")
    #ax2.plot( model.Time, model.FoodPC_Chk, "-.", lw=2, color="g")
    ax2.plot( model.Time, model.ServicesPC_U, "--", lw=2, color="y", label="Услуги/душу")
    ax2.set_xlim( limits)
    ax2.set_ylim( 0, 1)
    ax2.set_ylabel("Единиц")
    ax2.grid(True)
    ax2.legend(loc=2)

    ax3.set_title("Благосостояние", fontsize=18)
    ax3.plot( model.Time, model.HDI, "-", lw=2, color="b", label="HDI")
    ax3.plot( model.Time, model.EcoFootprint, "-", lw=2, color="m", label="Экологическое давление")
    ax3.set_xlim( limits)
    ax3.set_ylim( 0, 2.5)
    ax3.legend(loc=2)
    ax3.set_xlabel("Год")
    ax3.set_ylabel("Единиц")
    ax3.grid(True)
    if InteractiveModeOn: plt.show(True)
