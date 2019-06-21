from Utilities import *

class Population:
    """
    Describes population (as a Malthus-Velhurst equation solution AKA Shark Fin)
    Peak_Year - peak population year
    Peak_Value - peak population value
    L_Slope - left slope
    R_Slope - right slope
    Additionaly creates three approximate UN solutions using linear combinations of Sigmoid and Hubbert functions 
    """
    def __init__( self, Peak_Year=2057, Peak_Value=8000, L_Slope=0.028, R_Slope=0.080):
        self._Model0 = Linear_Combo()
        self._Model0.Wavelets += [Bathtub( -650,0.0025,2200,0.004,30,260,4250)]
        self._Model0.Wavelets += [Hubbert( Peak_Year, L_Slope, R_Slope, Peak_Value)]
        self._Model0.Wavelets += [Hubbert( 1950, 0.2, 0.2, -250)]
        self._Model0.Wavelets += [Hubbert( 2000, 0.1, 0.2, 150)]
        self._Model0.Wavelets += [Hubbert( 1970, 0.3, 0.3, -50)]
        self._Model0.Wavelets += [Hubbert( 1870, 0.1, 0.05, 120)]
        self._Model0.Wavelets += [Hubbert( 1930, 0.2, 0.2, -50)]
        self.Name = "PyWorld 2017"
        self.Calibration_Year, self.Calibration_Total, self.Calibration_Yerr = Load_Calibration(
            "Population_Calibration.csv", ["Year", "Population", "Yerror"])
        self.UN_Low = Linear_Combo()
        self.UN_Low.Name = "UN Low Case"
        self.UN_Low.Wavelets += [ Sigmoid( x0=2002.0, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1855.5, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1903.0, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1951.0, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1964.0, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1992.0, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2010.0, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2037.8, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_Low.Wavelets += [ Sigmoid( x0=2085.0, s0=0.04452, left=0.000, right=-6116.317, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2017.0, s0=0.16677, s1=0.20335, peak=155.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2062.0, s0=0.11881, s1=0.12884, peak=-128.000, shift=0.000)]
        self.UN_Medium = Linear_Combo()
        self.UN_Medium.Name = "UN Medium Case"
        self.UN_Medium.Wavelets += [ Sigmoid( x0=2002.0, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1855.5, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1903.0, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1951.0, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1964.0, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1992.0, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=2010.0, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=2037.8, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_High = Linear_Combo()
        self.UN_High.Name = "UN High Case"
        self.UN_High.Wavelets += [ Sigmoid( x0=2002.000, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1855.500, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1903.000, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1951.000, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1964.000, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1992.000, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2010.000, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2037.800, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_High.Wavelets += [ Sigmoid( x0=2085.000, s0=0.05121, left=0.000, right=8218.938, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2017.000, s0=0.22877, s1=0.27615, peak=-116.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2056.000, s0=0.13014, s1=0.20680, peak=80.975, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2088.000, s0=0.14967, s1=0.20132, peak=-171.671, shift=0.000)]
        self.Velhurst_Analytical = Sigmoid( 1997, 0.0370, 1390, 10500)
        self.Velhurst_Analytical.Name = "Velhurst Analytical"
        self.Kapitsa_Analytical = KapitsaIntegral( 2003, 176e3, 44)
        self.Kapitsa_Analytical.Name = "Kapitsa Analytical"
        return
    #
    # Loads historical data
    #
    def LoadHistorical(self):
        self.Historical_Year, self.Historical_Total, self.Historical_Yerr = Load_Calibration(
            "Earth_Historical.csv", ["Year", "Population", "Yerror"])
    #
    # Creates the solution vector
    #
    def Solve( self, t0):
        self.Solution_Year = t0
        self.Solution_Total = self._Model0.GetVector( t0)
        self.Solution_UN_Low = self.UN_Low.GetVector( t0)
        self.Solution_UN_Medium = self.UN_Medium.GetVector( t0)
        self.Solution_UN_High = self.UN_High.GetVector( t0)
        return self.Solution_Total
    #
    # Computes the approximation
    #
    def Compute( self, t):
        tmp = self._Model0.Compute( t)
        return tmp

class Population_World3:
    """
    Описывает популяцию матрицей Лесли с шагом 1 год
    year0 - начальный год модели
    population0 - общее население в начальном году
    tfr - количество живых родов в среднем у женщщны
    leb - ожидаемая продолжительность жизни при рождении
    m2f - отношение мальчики:девочки при рождении
    """
    def __init__( self, year0=1890, population0=1530.880, tfr=5.4, leb=30, m2f=1.05):
        self.Year = year0
        self.Ages = np.linspace( 0,199, 200)
        self.Population_Male = np.ones( 200)
        self.Population_Female = np.ones( 200)
        self.Attrition_Model_Male = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Attrition_Model_Female = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Fertility_Model = Bathtub( x0=18.0, s0=1.0, x1=35, s1=0.4, left=0.0, middle=1, right=0)
        self.TFR = tfr
        self.LEB_Male = leb-2
        self.LEB_Female = leb+2
        self.M2F = m2f
        self.__expectancy__ = Linear_Combo()
        self.__expectancy__.Wavelets += [Hubbert( x0=-10.0, s0=0.064, s1=0.064, peak= 0.370)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 45.0, s0=0.095, s1=0.092, peak= 0.024)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 14.0, s0=0.349, s1=0.214, peak=-0.018)]
        self.__expectancy__.Wavelets += [Hubbert( x0=  6.0, s0=1.162, s1=1.162, peak= 0.017)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 82.0, s0=0.240, s1=0.240, peak=-0.009)]

        # create initial population
        for i in range( 300): self.Compute_Next_Year()
        self.Normalize( population0)
        self.Compute_Next_Year()
        self.Normalize( population0)
        self.Year = year0
        return
    def Set_Attrition_Model( self, attr=None):
        if not attr is None:
            self.Attrition_Model_Male.Left = attr
            self.Attrition_Model_Male.Middle = attr * 0.1
            self.Attrition_Model_Female.Left = attr
            self.Attrition_Model_Female.Middle = attr * 0.1
            return
        self.Attrition_Model_Male.Left = self.__expectancy__.Compute_Cropped(
            Limit( self.LEB_Male, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Male.Middle = self.Attrition_Model_Male.Left * 0.1
        self.Attrition_Model_Female.Left = self.__expectancy__.Compute_Cropped(
            Limit( self.LEB_Female, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Female.Middle = self.Attrition_Model_Female.Left * 0.1
        return
    def Compute_LEB(self, attrition, population):
        """
        Computes true and apparent LEB
        """
        leb_true = 0
        counter = 1
        for i in range(199):
            counter *= 1-attrition[i]
            leb_true += counter
        pSum = np.sum( population)
        if pSum <= 0: return leb_true, 0.0
        tmpLEB = attrition * population
        tmpLEB[-1] = population[-1]
        leb_apparent = np.sum( tmpLEB * self.Ages) / np.sum(tmpLEB)
        return leb_true, leb_apparent
    def Compute_Next_Year( self, tfr=None, leb_male=None, leb_female=None, m2f=None,):
        self.Year += 1
        if not tfr is None: self.TFR = tfr
        if not leb_male is None: self.LEB_Male = leb_male
        if not leb_female is None: self.LEB_Female = leb_female
        if not m2f is None: self.M2F = m2f
        self.Set_Attrition_Model()
        attrition_male = self.Attrition_Model_Male.GetVector( self.Ages)
        attrition_female = self.Attrition_Model_Female.GetVector( self.Ages)
        self.LEB_True_Male, self.LEB_Apparent_Male = self.Compute_LEB(
            attrition_male, self.Population_Male )
        self.LEB_True_Female, self.LEB_Apparent_Female = self.Compute_LEB(
            attrition_female, self.Population_Female )
        self.nDeath = np.sum( self.Population_Male * attrition_male)
        self.nDeath += np.sum( self.Population_Female * attrition_female)
        self.Population_Male = np.roll( self.Population_Male * (1-attrition_male), 1)
        self.Population_Female = np.roll( self.Population_Female * (1-attrition_female), 1)
        fertility = self.Fertility_Model.GetVector(self.Ages)
        nFertile = np.dot( self.Population_Female, fertility)
        self.nBirth = nFertile * self.TFR / np.sum( fertility)
        self.Population_Male[0] = self.nBirth * 0.5 * self.M2F
        self.Population_Female[0] = self.nBirth  - self.Population_Male[0]
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        return
    def Normalize( self, norm):
        n = np.sum( self.Population_Male) + np.sum( self.Population_Female)
        if n <= 0.0: return
        n = norm/n
        self.Population_Male *= n
        self.Population_Female *= n
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        return

class Entity_UN:
    """
    Рrovides a programmatic interface to the UN country statistical data and future estimates
    The current statistics is from 1950 to 2017.
    The future estimates are from 2018 till 2100.
    """
    def __init__( self, time, estimate, low, med, high):
        estimate = estimate.strip()
        low = low.strip()
        med = med.strip()
        high = high.strip()
        estimate_S = estimate.split("\t")
        low_S = low.split("\t")
        med_S = med.split("\t")
        high_S = high.split("\t")
        self.Population = np.zeros(len(time))
        self.Population_Low = np.zeros(len(time))
        self.Population_High = np.zeros(len(time))
        self.YError = np.zeros(len(time))
        self.Name = estimate_S[1]
        self.Time = time
        self.Land_Area = -999.25
        self.Total_Area = -999.25
        self.Short_Name = self.Name 
        self.Code = "NONAME"
        acc = self.GetAccuracy()
        for i in range( 2,len(estimate_S)):
            j = 148 + i
            self.Population[j] = float(estimate_S[i])/1000.0
            self.Population_Low[j] = self.Population[j] * (1.0-acc)
            self.Population_High[j] = self.Population[j] * (1.0+acc)
            self.YError[j] = self.Population[j] * acc
        for i in range( 3,len(med_S)):
            j = 213 + i
            self.Population[j] = float(med_S[i])/1000.0
            self.Population_Low[j] = float(low_S[i])/1000.0 * (1.0-acc)
            self.Population_High[j] = float(high_S[i])/1000.0 * (1.0+acc)
            self.YError[j] = (self.Population_High[j]-self.Population_Low[j])/2.0
        return
    #
    # Returns the estimated data accuracy
    #
    def GetAccuracy( self):
        if self.Name == "WORLD": return 0.015
        if self.Name == "Less developed regions": return 0.015
        if self.Name == "Least developed countries": return 0.015
        if self.Name == "Less developed regions, excluding least developed countries": return 0.015
        if self.Name == "Less developed regions, excluding China": return 0.015
        if self.Name == "Low-income countries": return 0.015
        if self.Name == "Sub-Saharan Africa": return 0.015
        if self.Name == "AFRICA": return 0.015
        if self.Name == "Eastern Africa": return 0.015
        if self.Name == "Burundi": return 0.015
        if self.Name == "Comoros": return 0.015
        if self.Name == "Djibouti": return 0.015
        if self.Name == "Eritrea": return 0.015
        if self.Name == "Ethiopia": return 0.015
        if self.Name == "Kenya": return 0.015
        if self.Name == "Madagascar": return 0.015
        if self.Name == "Malawi": return 0.015
        if self.Name == "Mauritius": return 0.015
        if self.Name == "Mayotte": return 0.015
        if self.Name == "Mozambique": return 0.015
        if self.Name == "Rwanda": return 0.015
        if self.Name == "Seychelles": return 0.015
        if self.Name == "Somalia": return 0.015
        if self.Name == "South Sudan": return 0.015
        if self.Name == "Uganda": return 0.015
        if self.Name == "United Republic of Tanzania": return 0.015
        if self.Name == "Zambia": return 0.015
        if self.Name == "Zimbabwe": return 0.015
        if self.Name == "Middle Africa": return 0.015
        if self.Name == "Angola": return 0.015
        if self.Name == "Cameroon": return 0.015
        if self.Name == "Central African Republic": return 0.015
        if self.Name == "Chad": return 0.015
        if self.Name == "Congo": return 0.015
        if self.Name == "Democratic Republic of the Congo": return 0.015
        if self.Name == "Equatorial Guinea": return 0.015
        if self.Name == "Gabon": return 0.015
        if self.Name == "Sao Tome and Principe": return 0.015
        if self.Name == "Northern Africa": return 0.015
        if self.Name == "Algeria": return 0.015
        if self.Name == "Egypt": return 0.015
        if self.Name == "Libya": return 0.015
        if self.Name == "Morocco": return 0.015
        if self.Name == "Sudan": return 0.015
        if self.Name == "Tunisia": return 0.015
        if self.Name == "Western Sahara": return 0.015
        if self.Name == "Southern Africa": return 0.015
        if self.Name == "Botswana": return 0.015
        if self.Name == "Lesotho": return 0.015
        if self.Name == "Namibia": return 0.015
        if self.Name == "South Africa": return 0.015
        if self.Name == "Swaziland": return 0.015
        if self.Name == "Western Africa": return 0.015
        if self.Name == "Benin": return 0.015
        if self.Name == "Burkina Faso": return 0.015
        if self.Name == "Cabo Verde": return 0.015
        if self.Name == "Cote d'Ivoire": return 0.015
        if self.Name == "Gambia": return 0.015
        if self.Name == "Ghana": return 0.015
        if self.Name == "Guinea": return 0.015
        if self.Name == "Guinea-Bissau": return 0.015
        if self.Name == "Liberia": return 0.015
        if self.Name == "Mali": return 0.015
        if self.Name == "Mauritania": return 0.015
        if self.Name == "Niger": return 0.015
        if self.Name == "Nigeria": return 0.015
        if self.Name == "Saint Helena": return 0.015
        if self.Name == "Senegal": return 0.015
        if self.Name == "Sierra Leone": return 0.015
        if self.Name == "Togo": return 0.015
        if self.Name == "ASIA": return 0.015
        if self.Name == "Eastern Asia": return 0.015
        if self.Name == "Mongolia": return 0.015
        if self.Name == "South-Central Asia": return 0.015
        if self.Name == "Central Asia": return 0.015
        if self.Name == "Kyrgyzstan": return 0.015
        if self.Name == "Tajikistan": return 0.015
        if self.Name == "Turkmenistan": return 0.015
        if self.Name == "Uzbekistan": return 0.015
        if self.Name == "Southern Asia": return 0.015
        if self.Name == "Afghanistan": return 0.015
        if self.Name == "Bangladesh": return 0.015
        if self.Name == "Bhutan": return 0.015
        if self.Name == "India": return 0.015
        if self.Name == "Iran (Islamic Republic of)": return 0.015
        if self.Name == "Nepal": return 0.015
        if self.Name == "Pakistan": return 0.015
        if self.Name == "Sri Lanka": return 0.015
        if self.Name == "South-Eastern Asia": return 0.015
        if self.Name == "Cambodia": return 0.015
        if self.Name == "Indonesia": return 0.015
        if self.Name == "Lao People's Democratic Republic": return 0.015
        if self.Name == "Myanmar": return 0.015
        if self.Name == "Philippines": return 0.015
        if self.Name == "Timor-Leste": return 0.015
        if self.Name == "Western Asia": return 0.015
        if self.Name == "Iraq": return 0.015
        if self.Name == "Jordan": return 0.015
        if self.Name == "Lebanon": return 0.015
        if self.Name == "State of Palestine": return 0.015
        if self.Name == "Syrian Arab Republic": return 0.015
        if self.Name == "Yemen": return 0.015
        if self.Name == "LATIN AMERICA AND THE CARIBBEAN": return 0.015
        if self.Name == "Haiti": return 0.015
        return 0.005
    #
    # Returns true for entity in Africa
    #
    def isAFR( self):
        if self.Name == "AFRICA": return True
        if self.Name == "Eastern Africa": return True
        if self.Name == "Burundi": return True
        if self.Name == "Comoros": return True
        if self.Name == "Djibouti": return True
        if self.Name == "Eritrea": return True
        if self.Name == "Ethiopia": return True
        if self.Name == "Kenya": return True
        if self.Name == "Madagascar": return True
        if self.Name == "Malawi": return True
        if self.Name == "Mauritius": return True
        if self.Name == "Mayotte": return True
        if self.Name == "Mozambique": return True
        if self.Name == "Reunion": return True
        if self.Name == "Rwanda": return True
        if self.Name == "Seychelles": return True
        if self.Name == "Somalia": return True
        if self.Name == "South Sudan": return True
        if self.Name == "Uganda": return True
        if self.Name == "United Republic of Tanzania": return True
        if self.Name == "Zambia": return True
        if self.Name == "Zimbabwe": return True
        if self.Name == "Middle Africa": return True
        if self.Name == "Angola": return True
        if self.Name == "Cameroon": return True
        if self.Name == "Central African Republic": return True
        if self.Name == "Chad": return True
        if self.Name == "Congo": return True
        if self.Name == "Democratic Republic of the Congo": return True
        if self.Name == "Equatorial Guinea": return True
        if self.Name == "Gabon": return True
        if self.Name == "Sao Tome and Principe": return True
        if self.Name == "Northern Africa": return True
        if self.Name == "Algeria": return True
        if self.Name == "Egypt": return True
        if self.Name == "Libya": return True
        if self.Name == "Morocco": return True
        if self.Name == "Sudan": return True
        if self.Name == "Tunisia": return True
        if self.Name == "Western Sahara": return True
        if self.Name == "Southern Africa": return True
        if self.Name == "Botswana": return True
        if self.Name == "Lesotho": return True
        if self.Name == "Namibia": return True
        if self.Name == "South Africa": return True
        if self.Name == "Swaziland": return True
        if self.Name == "Western Africa": return True
        if self.Name == "Benin": return True
        if self.Name == "Burkina Faso": return True
        if self.Name == "Cabo Verde": return True
        if self.Name == "Cote d'Ivoire": return True
        if self.Name == "Gambia": return True
        if self.Name == "Ghana": return True
        if self.Name == "Guinea": return True
        if self.Name == "Guinea-Bissau": return True
        if self.Name == "Liberia": return True
        if self.Name == "Mali": return True
        if self.Name == "Mauritania": return True
        if self.Name == "Niger": return True
        if self.Name == "Nigeria": return True
        if self.Name == "Saint Helena": return True
        if self.Name == "Senegal": return True
        if self.Name == "Sierra Leone": return True
        if self.Name == "Togo": return True
        return False
    #
    # Returns true for entity in Asia
    #
    def isASIA( self):
        if self.Name == "ASIA": return True
        if self.Name == "Eastern Asia": return True
        if self.Name == "China": return True
        if self.Name == "China, Hong Kong SAR": return True
        if self.Name == "China, Macao SAR": return True
        if self.Name == "China, Taiwan Province of China": return True
        if self.Name == "Dem. People's Republic of Korea": return True
        if self.Name == "Japan": return True
        if self.Name == "Mongolia": return True
        if self.Name == "Republic of Korea": return True
        if self.Name == "South-Central Asia": return True
        if self.Name == "Central Asia": return True
        if self.Name == "Kazakhstan": return True
        if self.Name == "Kyrgyzstan": return True
        if self.Name == "Tajikistan": return True
        if self.Name == "Turkmenistan": return True
        if self.Name == "Uzbekistan": return True
        if self.Name == "Southern Asia": return True
        if self.Name == "Afghanistan": return True
        if self.Name == "Bangladesh": return True
        if self.Name == "Bhutan": return True
        if self.Name == "India": return True
        if self.Name == "Iran (Islamic Republic of)": return True
        if self.Name == "Maldives": return True
        if self.Name == "Nepal": return True
        if self.Name == "Pakistan": return True
        if self.Name == "Sri Lanka": return True
        if self.Name == "South-Eastern Asia": return True
        if self.Name == "Brunei Darussalam": return True
        if self.Name == "Cambodia": return True
        if self.Name == "Indonesia": return True
        if self.Name == "Lao People's Democratic Republic": return True
        if self.Name == "Malaysia": return True
        if self.Name == "Myanmar": return True
        if self.Name == "Philippines": return True
        if self.Name == "Singapore": return True
        if self.Name == "Thailand": return True
        if self.Name == "Timor-Leste": return True
        if self.Name == "Viet Nam": return True
        if self.Name == "Western Asia": return True
        if self.Name == "Armenia": return True
        if self.Name == "Azerbaijan": return True
        if self.Name == "Bahrain": return True
        if self.Name == "Cyprus": return True
        if self.Name == "Georgia": return True
        if self.Name == "Iraq": return True
        if self.Name == "Israel": return True
        if self.Name == "Jordan": return True
        if self.Name == "Kuwait": return True
        if self.Name == "Lebanon": return True
        if self.Name == "Oman": return True
        if self.Name == "Qatar": return True
        if self.Name == "Saudi Arabia": return True
        if self.Name == "State of Palestine": return True
        if self.Name == "Syrian Arab Republic": return True
        if self.Name == "Turkey": return True
        if self.Name == "United Arab Emirates": return True
        if self.Name == "Yemen": return True
        return False
    #
    # Returns true for entity in Oceania
    #
    def isOCEANIA( self):
        if self.Name == "OCEANIA": return True
        if self.Name == "Australia/New Zealand": return True
        if self.Name == "Australia": return True
        if self.Name == "New Zealand": return True
        if self.Name == "Melanesia": return True
        if self.Name == "Fiji": return True
        if self.Name == "New Caledonia": return True
        if self.Name == "Papua New Guinea": return True
        if self.Name == "Solomon Islands": return True
        if self.Name == "Vanuatu": return True
        if self.Name == "Micronesia": return True
        if self.Name == "Guam": return True
        if self.Name == "Kiribati": return True
        if self.Name == "Marshall Islands": return True
        if self.Name == "Micronesia (Fed. States of)": return True
        if self.Name == "Nauru": return True
        if self.Name == "Northern Mariana Islands": return True
        if self.Name == "Palau": return True
        if self.Name == "Polynesia": return True
        if self.Name == "American Samoa": return True
        if self.Name == "Cook Islands": return True
        if self.Name == "French Polynesia": return True
        if self.Name == "Niue": return True
        if self.Name == "Samoa": return True
        if self.Name == "Tokelau": return True
        if self.Name == "Tonga": return True
        if self.Name == "Tuvalu": return True
        if self.Name == "Wallis and Futuna Islands": return True
        return False
    #
    # Returns true for entity in North America
    #
    def isNAM( self):
        if self.Name == "NORTHERN AMERICA": return True
        if self.Name == "Bermuda": return True
        if self.Name == "Canada": return True
        if self.Name == "Greenland": return True
        if self.Name == "Saint Pierre and Miquelon": return True
        if self.Name == "United States of America": return True
        return False
    #
    # Returns true for entity in Europe
    #
    def isEUR( self):
        if self.Name == "EUROPE": return True
        if self.Name == "Eastern Europe": return True
        if self.Name == "Belarus": return True
        if self.Name == "Bulgaria": return True
        if self.Name == "Czechia": return True
        if self.Name == "Hungary": return True
        if self.Name == "Poland": return True
        if self.Name == "Republic of Moldova": return True
        if self.Name == "Romania": return True
        if self.Name == "Russian Federation": return True
        if self.Name == "Slovakia": return True
        if self.Name == "Ukraine": return True
        if self.Name == "Northern Europe": return True
        if self.Name == "Channel Islands": return True
        if self.Name == "Denmark": return True
        if self.Name == "Estonia": return True
        if self.Name == "Faeroe Islands": return True
        if self.Name == "Finland": return True
        if self.Name == "Iceland": return True
        if self.Name == "Ireland": return True
        if self.Name == "Isle of Man": return True
        if self.Name == "Latvia": return True
        if self.Name == "Lithuania": return True
        if self.Name == "Norway": return True
        if self.Name == "Sweden": return True
        if self.Name == "United Kingdom": return True
        if self.Name == "Southern Europe": return True
        if self.Name == "Albania": return True
        if self.Name == "Andorra": return True
        if self.Name == "Bosnia and Herzegovina": return True
        if self.Name == "Croatia": return True
        if self.Name == "Gibraltar": return True
        if self.Name == "Greece": return True
        if self.Name == "Holy See": return True
        if self.Name == "Italy": return True
        if self.Name == "Malta": return True
        if self.Name == "Montenegro": return True
        if self.Name == "Portugal": return True
        if self.Name == "San Marino": return True
        if self.Name == "Serbia": return True
        if self.Name == "Slovenia": return True
        if self.Name == "Spain": return True
        if self.Name == "TFYR Macedonia": return True
        if self.Name == "Western Europe": return True
        if self.Name == "Austria": return True
        if self.Name == "Belgium": return True
        if self.Name == "France": return True
        if self.Name == "Germany": return True
        if self.Name == "Liechtenstein": return True
        if self.Name == "Luxembourg": return True
        if self.Name == "Monaco": return True
        if self.Name == "Netherlands": return True
        if self.Name == "Switzerland": return True
        return False
    #
    # Returns true for entity in South America
    #
    def isSAM( self):
        if self.Name == "LATIN AMERICA AND THE CARIBBEAN": return True
        if self.Name == "Caribbean": return True
        if self.Name == "Anguilla": return True
        if self.Name == "Antigua and Barbuda": return True
        if self.Name == "Aruba": return True
        if self.Name == "Bahamas": return True
        if self.Name == "Barbados": return True
        if self.Name == "British Virgin Islands": return True
        if self.Name == "Caribbean Netherlands": return True
        if self.Name == "Cayman Islands": return True
        if self.Name == "Cuba": return True
        if self.Name == "Curacao": return True
        if self.Name == "Dominica": return True
        if self.Name == "Dominican Republic": return True
        if self.Name == "Grenada": return True
        if self.Name == "Guadeloupe": return True
        if self.Name == "Haiti": return True
        if self.Name == "Jamaica": return True
        if self.Name == "Martinique": return True
        if self.Name == "Montserrat": return True
        if self.Name == "Puerto Rico": return True
        if self.Name == "Saint Kitts and Nevis": return True
        if self.Name == "Saint Lucia": return True
        if self.Name == "Saint Vincent and the Grenadines": return True
        if self.Name == "Sint Maarten (Dutch part)": return True
        if self.Name == "Trinidad and Tobago": return True
        if self.Name == "Turks and Caicos Islands": return True
        if self.Name == "United States Virgin Islands": return True
        if self.Name == "Central America": return True
        if self.Name == "Belize": return True
        if self.Name == "Costa Rica": return True
        if self.Name == "El Salvador": return True
        if self.Name == "Guatemala": return True
        if self.Name == "Honduras": return True
        if self.Name == "Mexico": return True
        if self.Name == "Nicaragua": return True
        if self.Name == "Panama": return True
        if self.Name == "South America": return True
        if self.Name == "Argentina": return True
        if self.Name == "Bolivia (Plurinational State of)": return True
        if self.Name == "Brazil": return True
        if self.Name == "Chile": return True
        if self.Name == "Colombia": return True
        if self.Name == "Ecuador": return True
        if self.Name == "Falkland Islands (Malvinas)": return True
        if self.Name == "French Guiana": return True
        if self.Name == "Guyana": return True
        if self.Name == "Paraguay": return True
        if self.Name == "Peru": return True
        if self.Name == "Suriname": return True
        if self.Name == "Uruguay": return True
        if self.Name == "Venezuela (Bolivarian Republic of)": return True
        return False
    #
    # Returns true for entity is an aggregate
    #
    def isAggregate( self):
        if self.Name == "WORLD": return True
        if self.Name == "More developed regions": return True
        if self.Name == "Less developed regions": return True
        if self.Name == "Least developed countries": return True
        if self.Name == "Less developed regions, excluding least developed countries": return True
        if self.Name == "Less developed regions, excluding China": return True
        if self.Name == "High-income countries": return True
        if self.Name == "Middle-income countries": return True
        if self.Name == "Upper-middle-income countries": return True
        if self.Name == "Lower-middle-income countries": return True
        if self.Name == "Low-income countries": return True
        if self.Name == "Sub-Saharan Africa": return True
        return False
    #
    # Saves the entity as a CSV file
    #
    def Save( self, name):
        name1 = name + "_UN_Mid.csv"
        name2 = name + "_UN_Low.csv"
        name3 = name + "_UN_Hig.csv"
        f_out1 = self.__openFile__( name1, "Medium estimate")
        f_out2 = self.__openFile__( name2, "Low estimate")
        f_out3 = self.__openFile__( name3, "High estimate")
        for i, t in enumerate(self.Time):
            t = "{:4d}".format( int(t))
            f_out1.write( "{:s},{:.3f}\n".format(t, self.Population[i]))
            f_out2.write( "{:s},{:.3f}\n".format(t, self.Population_Low[i]))
            f_out3.write( "{:s},{:.3f}\n".format(t, self.Population_High[i]))
        f_out1.close()
        f_out2.close()
        f_out3.close()
        return
    def SmoothTail( self):
        self.Population = Filter( self.Population, 0, 150, [1,1,1,2,2,2,1,1,1])
        return
    def AppendPre1950( self, data, smoothing, cal=1.0):
        print( "In year {:d} UN = {:.1f} OWID = {:.1f}".format( int(self.Time[150]), self.Population[150], data[150]))
        Calibration = np.sum( self.Population[150:170] / data[150:170]) / 20.0
        print( self.Name + " calibration: " + str(Calibration))
        acc = 3.0 * self.GetAccuracy()
        self.Population[:150] = data[:150] * cal
        for i in range(smoothing): self.SmoothTail()
        self.Population_Low[:150] = self.Population[:150] * (1.0-acc)
        self.Population_High[:150] = self.Population[:150] * (1.0+acc)
        self.YError[:150] = self.Population[:150] * acc
        return
    def __openFile__( self, name, description):
        f_out = open( name, "w", encoding="cp1251")
        f_out.write( "#\n")
        f_out.write( "# " + description + "\n")
        f_out.write( "#\n")
        f_out.write( "# Horizontal conversion = 150,1080,1800,2100,year\n")
        f_out.write( "# Vertical conversion = 713,97,0,7000,mln\n")
        f_out.write( "#\n")
        f_out.write( "Year,Population\n")
        return f_out
    def GetLandUsage(self):
        lu1 = self.Land_Area / (self.Population + 1e-6) / 100
        lu2 = self.Land_Area / (self.Population_Low + 1e-6) / 100
        lu3 = self.Land_Area / (self.Population_High + 1e-6) / 100
        return lu1, lu2, lu3

#
# Reads UN data bases, extracts entries
#
class Population_UN:
    def __init__( self):
        f0 = open("./Data/UN_RAW_1950_2015.txt", encoding="cp1251")
        f1 = open("./Data/UN_LOW_2015_2100.txt", encoding="cp1251")
        f2 = open("./Data/UN_MED_2015_2100.txt", encoding="cp1251")
        f3 = open("./Data/UN_HIG_2015_2100.txt", encoding="cp1251")
        f0.readline()
        f1.readline()
        f2.readline()
        f3.readline()
        self.Time = np.linspace(1800,2100,301)
        self.Entities = []
        for i in range(1000):
            s0 = f0.readline()    
            s1 = f1.readline()    
            s2 = f2.readline()    
            s3 = f3.readline()
            if len(s0) <= 0:
                print( "Read lines: " + str(i))
                break
            e = Entity_UN( self.Time,s0,s1,s2,s3)
            self.Entities += [e]
        f0.close()
        f1.close()
        f2.close()
        f3.close()
        print( "Processed: " + str(len(self.Entities)))
        for e in self.Entities:
            if e.isAFR(): continue
            if e.isASIA(): continue
            if e.isOCEANIA(): continue
            if e.isNAM(): continue
            if e.isSAM(): continue
            if e.isEUR(): continue
            if e.isAggregate(): continue
            print( e.Name)
        self.Country_Codes, self.Short_Names, self.Long_Names, Area_Land_Sea, Area_Land = Load_Calibration_Text(
            "./Data/Country_Area.txt", ["Code", "Short_Name", "Country_Name", "Land_and_Sea", "Land"], "\t")
        Area_Land_Sea = Strings_To_Array(Area_Land_Sea)
        Area_Land = Strings_To_Array(Area_Land)
        for i, longName in enumerate( self.Long_Names):
            ent = self.GetEntity( longName)
            if " not found" in ent.Name: continue
            ent.Land_Area = Area_Land[i]
            ent.Total_Area = Area_Land_Sea[i]
            ent.Short_Name = self.Short_Names[i]
            ent.Code = self.Country_Codes[i] 
        return
    def GetEntity( self, name):
        for e in self.Entities:
            n = name.lower()
            if e.Name.lower() == n: return e
            if e.Short_Name.lower() == n: return e
            if e.Code != "NONAME" and e.Code.lower == n: return e
        return Entity_UN(self.Time, "0\t" + name + " not found","0\tnull","0\tnull","0\tnull")

class Country_Fertility():
    def __init__( self, name, year, tfr, leb):
        self.Name = name
        self.Data = {year: (float(year), float(tfr), float(leb))}
        #print("{:s} created".format( self.Name))
        return
    def Add_TFR( self, year, tfr):
        if year in self.Data:
            d = self.Data[year]
            self.Data[year] = (float(year), float(tfr), d[2])
            return
        self.Data[year] = (float(year), float(tfr), -999.0)        
        return
    def Add_LEB( self, year, leb):
        if year in self.Data:
            d = self.Data[year]
            self.Data[year] = (float(year), d[1], float(leb))
            return
        self.Data[year] = (float(year), -999.0, float(leb))        
        return
    def Get_TFR_vs_Year( self):
        tmp_y = []
        tmp_t = []
        for i, v in self.Data.items():
            if v[1] < 0: continue
            tmp_y += [v[0]]
            tmp_t += [v[1]]
        return np.array(tmp_y), np.array(tmp_t)
    def Get_LEB_vs_Year( self, lim=1950):
        tmp_y = []
        tmp_l = []
        for i, v in self.Data.items():
            if v[2] < 0: continue
            if v[0] < lim: continue
            tmp_y += [v[0]]
            tmp_l += [v[2]]
        return np.array(tmp_y), np.array(tmp_l)
    def Get_TFR_vs_LEB( self):
        tmp_t = []
        tmp_l = []
        for i, v in self.Data.items():
            if v[1] < 0: continue
            if v[2] < 0: continue
            tmp_t += [v[1]]
            tmp_l += [v[2]]
        return np.array(tmp_l), np.array(tmp_t)

class UN_Fertility():
    def __init__( self):
        self.Countries = {}
        country, year, leb = Load_Calibration_Text("./Data/UN_LEB_Estimates.csv", ["Entity","Year","LEB"], "\t")
        for i, c in enumerate(country):
            if not c in self.Countries:
                self.Countries[c] = Country_Fertility( c, year[i], -999.0, leb[i])
                continue
            self.Countries[c].Add_LEB( year[i], leb[i])
        country, year, tfr = Load_Calibration_Text("./Data/UN_TFR_Estimates.csv", ["Entity","Year","TFR"], "\t")
        for i, c in enumerate(country):
            if not c in self.Countries:
                self.Countries[c] = Country_Fertility( c, year[i], tfr[i], -999.0)
                continue
            self.Countries[c].Add_TFR( year[i], tfr[i])
        self.Exceptions = ["French Guiana"]
        self.Exceptions += ["Israel"]
        self.Exceptions += ["Kazakhstan"]
        self.Exceptions += ["Kyrgyzstan"]
        self.Exceptions += ["Mongolia"]
        self.Exceptions += ["Niger"]
        self.Exceptions += ["Nigeria"]
        self.Exceptions += ["Syria"]
        self.Exceptions += ["Tajikistan"]
        self.Exceptions += ["Timor-Leste"]
        self.Exceptions += ["Turkmenistan"]
        self.Exceptions += ["Zimbabwe"]

        self.Group_2a = ["Afghanistan"]
        self.Group_2a += ["Angola"]
        self.Group_2a += ["Bangladesh"]
        self.Group_2a += ["Benin"]
        self.Group_2a += ["Bhutan"]
        self.Group_2a += ["Burkina Faso"]
        self.Group_2a += ["Burundi"]
        self.Group_2a += ["Cameroon"]
        self.Group_2a += ["Central African Republic"]
        self.Group_2a += ["Chad"]
        self.Group_2a += ["Comoros"]
        self.Group_2a += ["Congo"]
        self.Group_2a += ["Cote d'Ivoire"]
        self.Group_2a += ["Democratic Republic of the Congo"]
        self.Group_2a += ["Djibouti"]
        self.Group_2a += ["Egypt"]
        self.Group_2a += ["Equatorial Guinea"]
        self.Group_2a += ["Eritrea"]
        self.Group_2a += ["Ethiopia"]
        self.Group_2a += ["Gabon"]
        self.Group_2a += ["Gambia"]
        self.Group_2a += ["Ghana"]
        self.Group_2a += ["Guinea-Bissau"]
        self.Group_2a += ["Guinea"]
        self.Group_2a += ["Haiti"]
        self.Group_2a += ["Iraq"]
        self.Group_2a += ["Jordan"]
        self.Group_2a += ["Kenya"]
        self.Group_2a += ["Kiribati"]
        self.Group_2a += ["Laos"]
        self.Group_2a += ["Lesotho"]
        self.Group_2a += ["Liberia"]
        self.Group_2a += ["Madagascar"]
        self.Group_2a += ["Malawi"]
        self.Group_2a += ["Mali"]
        self.Group_2a += ["Mauritania"]
        self.Group_2a += ["Mayotte"]
        self.Group_2a += ["Melanesia"]
        self.Group_2a += ["Micronesia (Fed. States of)"]
        self.Group_2a += ["Micronesia"]
        self.Group_2a += ["Mozambique"]
        self.Group_2a += ["Namibia"]
        self.Group_2a += ["Pakistan"]
        self.Group_2a += ["Palestine"]
        self.Group_2a += ["Papua New Guinea"]
        self.Group_2a += ["Philippines"]
        self.Group_2a += ["Rwanda"]
        self.Group_2a += ["Samoa"]
        self.Group_2a += ["Sao Tome and Principe"]
        self.Group_2a += ["Senegal"]
        self.Group_2a += ["Sierra Leone"]
        self.Group_2a += ["Solomon Islands"]
        self.Group_2a += ["Somalia"]
        self.Group_2a += ["South Sudan"]
        self.Group_2a += ["Sudan"]
        self.Group_2a += ["Swaziland"]
        self.Group_2a += ["Tanzania"]
        self.Group_2a += ["Togo"]
        self.Group_2a += ["Tonga"]
        self.Group_2a += ["Uganda"]
        self.Group_2a += ["Vanuatu"]
        self.Group_2a += ["Yemen"]
        self.Group_2a += ["Zambia"]

        self.Group_2b = ["Algeria"]
        self.Group_2b += ["Bahrain"]
        self.Group_2b += ["Belize"]
        self.Group_2b += ["Bolivia"]
        self.Group_2b += ["Botswana"]
        self.Group_2b += ["Cabo Verde"]
        self.Group_2b += ["Cambodia"]
        self.Group_2b += ["Colombia"]
        self.Group_2b += ["Dominican Republic"]
        self.Group_2b += ["Ecuador"]
        self.Group_2b += ["El Salvador"]
        self.Group_2b += ["Fiji"]
        self.Group_2b += ["French Polynesia"]
        self.Group_2b += ["Guatemala"]
        self.Group_2b += ["Honduras"]
        self.Group_2b += ["India"]
        self.Group_2b += ["Indonesia"]
        self.Group_2b += ["Iran"]
        self.Group_2b += ["Libya"]
        self.Group_2b += ["Maldives"]
        self.Group_2b += ["Mauritius"]
        self.Group_2b += ["Mexico"]
        self.Group_2b += ["Morocco"]
        self.Group_2b += ["Myanmar"]
        self.Group_2b += ["Nepal"]
        self.Group_2b += ["New Caledonia"]
        self.Group_2b += ["Nicaragua"]
        self.Group_2b += ["Oman"]
        self.Group_2b += ["Panama"]
        self.Group_2b += ["Paraguay"]
        self.Group_2b += ["Peru"]
        self.Group_2b += ["Polynesia"]
        self.Group_2b += ["Reunion"]
        self.Group_2b += ["Saint Vincent and the Grenadines"]
        self.Group_2b += ["Saudi Arabia"]
        self.Group_2b += ["South Africa"]
        self.Group_2b += ["Suriname"]
        self.Group_2b += ["Thailand"]
        self.Group_2b += ["Tunisia"]
        self.Group_2b += ["Turkey"]
        self.Group_2b += ["United Arab Emirates"]
        self.Group_2b += ["Western Sahara"]

        self.Group_3 = ["Albania"]
        self.Group_3 += ["Antigua and Barbuda"]
        self.Group_3 += ["Argentina"]
        self.Group_3 += ["Armenia"]
        self.Group_3 += ["Aruba"]
        self.Group_3 += ["Australia"]
        self.Group_3 += ["Azerbaijan"]
        self.Group_3 += ["Bahamas"]
        self.Group_3 += ["Barbados"]
        self.Group_3 += ["Bosnia and Herzegovina"]
        self.Group_3 += ["Brazil"]
        self.Group_3 += ["Brunei"]
        self.Group_3 += ["Canada"]
        self.Group_3 += ["Chile"]
        self.Group_3 += ["China, Hong Kong SAR"]
        self.Group_3 += ["China, Macao SAR"]
        self.Group_3 += ["China"]
        self.Group_3 += ["Costa Rica"]
        self.Group_3 += ["Cuba"]
        self.Group_3 += ["Curacao"]
        self.Group_3 += ["Cyprus"]
        self.Group_3 += ["Dem. People's Republic of Korea"]
        self.Group_3 += ["Finland"]
        self.Group_3 += ["Grenada"]
        self.Group_3 += ["Guadeloupe"]
        self.Group_3 += ["Guam"]
        self.Group_3 += ["Guyana"]
        self.Group_3 += ["Iceland"]
        self.Group_3 += ["Ireland"]
        self.Group_3 += ["Jamaica"]
        self.Group_3 += ["Japan"]
        self.Group_3 += ["Kuwait"]
        self.Group_3 += ["Lebanon"]
        self.Group_3 += ["Macedonia"]
        self.Group_3 += ["Malaysia"]
        self.Group_3 += ["Malta"]
        self.Group_3 += ["Martinique"]
        self.Group_3 += ["Moldova"]
        self.Group_3 += ["Montenegro"]
        self.Group_3 += ["Netherlands"]
        self.Group_3 += ["New Zealand"]
        self.Group_3 += ["Norway"]
        self.Group_3 += ["Poland"]
        self.Group_3 += ["Portugal"]
        self.Group_3 += ["Puerto Rico"]
        self.Group_3 += ["Qatar"]
        self.Group_3 += ["Republic of Korea"]
        self.Group_3 += ["Romania"]
        self.Group_3 += ["Saint Lucia"]
        self.Group_3 += ["Serbia"]
        self.Group_3 += ["Seychelles"]
        self.Group_3 += ["Singapore"]
        self.Group_3 += ["Slovakia"]
        self.Group_3 += ["Slovenia"]
        self.Group_3 += ["Sri Lanka"]
        self.Group_3 += ["Taiwan"]
        self.Group_3 += ["Trinidad and Tobago"]
        self.Group_3 += ["United States of America"]
        self.Group_3 += ["United States Virgin Islands"]
        self.Group_3 += ["Uruguay"]
        self.Group_3 += ["Uzbekistan"]
        self.Group_3 += ["Venezuela"]
        self.Group_3 += ["Vietnam"]

        self.Group_4 = ["Austria"]
        self.Group_4 += ["Belarus"]
        self.Group_4 += ["Belgium"]
        self.Group_4 += ["Bulgaria"]
        self.Group_4 += ["Channel Islands"]
        self.Group_4 += ["Croatia"]
        self.Group_4 += ["Czechia"]
        self.Group_4 += ["Denmark"]
        self.Group_4 += ["Estonia"]
        self.Group_4 += ["France"]
        self.Group_4 += ["Georgia"]
        self.Group_4 += ["Germany"]
        self.Group_4 += ["Greece"]
        self.Group_4 += ["Hungary"]
        self.Group_4 += ["Italy"]
        self.Group_4 += ["Latvia"]
        self.Group_4 += ["Lithuania"]
        self.Group_4 += ["Luxembourg"]
        self.Group_4 += ["Russia"]
        self.Group_4 += ["Spain"]
        self.Group_4 += ["Sweden"]
        self.Group_4 += ["Switzerland"]
        self.Group_4 += ["Ukraine"]
        self.Group_4 += ["United Kingdom"]

        self.Regions = ["Africa"]
        self.Regions += ["Asia"]
        self.Regions += ["Caribbean"]
        self.Regions += ["Central America"]
        self.Regions += ["Central Asia"]
        self.Regions += ["Eastern Africa"]
        self.Regions += ["Eastern Asia"]
        self.Regions += ["Eastern Europe"]
        self.Regions += ["Europe"]
        self.Regions += ["High-income countries"]
        self.Regions += ["Latin America and the Caribbean"]
        self.Regions += ["Least developed countries"]
        self.Regions += ["Less developed regions, excluding China"]
        self.Regions += ["Less developed regions, excluding least developed countries"]
        self.Regions += ["Less developed regions"]
        self.Regions += ["Low-income countries"]
        self.Regions += ["Lower-middle-income countries"]
        self.Regions += ["Middle Africa"]
        self.Regions += ["Middle-income countries"]
        self.Regions += ["More developed regions"]
        self.Regions += ["Northern Africa"]
        self.Regions += ["Northern America"]
        self.Regions += ["Northern Europe"]
        self.Regions += ["Oceania"]
        self.Regions += ["South America"]
        self.Regions += ["South-Central Asia"]
        self.Regions += ["South-Eastern Asia"]
        self.Regions += ["Southern Africa"]
        self.Regions += ["Southern Asia"]
        self.Regions += ["Southern Europe"]
        self.Regions += ["Sub-Saharan Africa"]
        self.Regions += ["Upper-middle-income countries"]
        self.Regions += ["Western Africa"]
        self.Regions += ["Western Asia"]
        self.Regions += ["Western Europe"]
        self.Regions += ["World"]

        self.Areas = ["Africa"]
        self.Areas += ["Asia"]
        self.Areas += ["Europe"]
        self.Areas += ["Latin America and the Caribbean"]
        self.Areas += ["Northern America"]
        self.Areas += ["Oceania"]
        self.Areas += ["World"]
        return
