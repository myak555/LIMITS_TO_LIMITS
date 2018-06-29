from Utilities import *

#
# Describes population (as a Malthus-Velhurst equation solution AKA Shark Fin)
# Peak_Year - peak population year
# Peak_Value - peak population value
# L_Slope - left slope
# R_Slope - right slope
# Additionaly creates three approximate UN solutions using linear combinations of Sigmoid and Hubbert functions 
#
class Population:
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
        self.Calibration_Year, self.Calibration_Total = Load_Calibration( "Population_Calibration.csv", "Year", "Population")
        self.Calibration_Year, self.Calibration_Yerr = Load_Calibration( "Population_Calibration.csv", "Year", "Yerror")
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
        self.Historical_Year, self.Historical_Total = Load_Calibration( "Earth_Historical.csv", "Year", "Population")
        self.Historical_Year, self.Historical_Yerr = Load_Calibration( "Earth_Historical.csv", "Year", "Yerror")
    #
    # Creates the solution vector
    #
    def Solve( self, t0):
        self.Solution_Year = t0
        self.Solution_Total = self._Model0.GetVector( t0)
        return self.Solution_Total
    #
    # Computes the approximation
    #
    def Compute( self, t):
        tmp = self._Model0.Compute( t)
        return tmp

#
# Рrovides a programmatic interface to the UN country statistical data and future estimates
# The current statistics is from 1950 to 2017.
# The future estimates are from 2018 till 2100.
#
class Entity_UN:
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
        acc = self.GetAccuracy()
        for i in range( 2,len(estimate_S)):
            self.Population[148+i] = float(estimate_S[i])/1000.0
            self.Population_Low[148+i] = self.Population[148+i] * (1.0-acc)
            self.Population_High[148+i] = self.Population[148+i] * (1.0+acc)
            self.YError[148+i] = self.Population[148+i] * acc
        for i in range( 3,len(med_S)):
            self.Population[213+i] = float(med_S[i])/1000.0
            self.Population_Low[213+i] = float(low_S[i])/1000.0 * (1.0-acc)
            self.Population_High[213+i] = float(high_S[i])/1000.0 * (1.0+acc)
            self.YError[213+i] = (self.Population_High[213+i]-self.Population_Low[213+i])/2.0
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
        for i in range( len(self.Population)):
            f_out1.write( "{:4d},{:.3f}\n".format(int(self.Time[i]), self.Population[i]))
            f_out2.write( "{:4d},{:.3f}\n".format(int(self.Time[i]), self.Population_Low[i]))
            f_out3.write( "{:4d},{:.3f}\n".format(int(self.Time[i]), self.Population_High[i]))
        f_out1.close()
        f_out2.close()
        f_out3.close()
        return
    def SmoothTail( self):
        self.Population = Filter( self.Population, 0, 150, [1,1,1,2,2,2,1,1,1])
        return
    def AppendPre1950( self, data, smoothing, cal=1.0):
        print( "In year {:d} UN = {:.1f} OWID = {:.1f}".format( int(self.Time[150]), self.Population[150], data[150]))
        Calibration = 0.0
        for i in range( 20):
            d = self.Population[i+150] / data[i+150]
            Calibration += d
        Calibration /= 20
        print( self.Name + " calibration: " + str(Calibration))
        acc = 3.0 * self.GetAccuracy()
        for i in range( 150):
            self.Population[i] = data[i] * cal
        for i in range(smoothing): self.SmoothTail()
        for i in range( 150):
            self.Population_Low[i] = self.Population[i] * (1.0-acc)
            self.Population_High[i] = self.Population[i] * (1.0+acc)
            self.YError[i] = self.Population[i] * acc
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

#
# Reads UN data bases, extracts entries
#
class Population_UN:
    def __init__( self):
        f0 = open(".\\Data\\UN_RAW_1950_2015.txt", encoding="cp1251")
        f1 = open(".\\Data\\UN_LOW_2015_2100.txt", encoding="cp1251")
        f2 = open(".\\Data\\UN_MED_2015_2100.txt", encoding="cp1251")
        f3 = open(".\\Data\\UN_HIG_2015_2100.txt", encoding="cp1251")
        f0.readline()
        f1.readline()
        f2.readline()
        f3.readline()
        self.Time = np.linspace(1800,2100,301)
        self.Entities = []
        for i in range( 1000):
            s0 = f0.readline()    
            s1 = f1.readline()    
            s2 = f2.readline()    
            s3 = f3.readline()
            if len(s0) <= 0:
                print( "Read: " + str(i))
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
        return
    def GetEntity( self, name):
        for e in self.Entities:
            if e.Name == name: return e
        return Entity_UN(self.Time, "0\t" + name + " not found","0\tnull","0\tnull","0\tnull")
