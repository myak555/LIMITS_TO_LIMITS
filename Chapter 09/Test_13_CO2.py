from Population import *

class CO2_Scenario_1 (Control_Curve):
    def __init__( self):
        self.Name = "Сценарий #1: Обвал в 2014 г"
        self.Wavelets = []
        self.Wavelets = [Hubbert( x0=2025.000, s0=0.04000, s1=0.04000, peak=38400.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1913.000, s0=0.08261, s1=0.10550, peak=1653.634, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1973.500, s0=0.41976, s1=0.43597, peak=2525.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=2000.000, s0=0.22813, s1=0.34509, peak=-4810.824, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1950.000, s0=0.44788, s1=0.34174, peak=-615.293, shift=0.000)]
        self.Projection = Hubbert( 2014,0.1,0.1,36400)
        return
    # computation
    def Compute( self, x):
        if x > 2016: return self.Projection.Compute(x) 
        tmp = 0.0
        for w in self.Wavelets:
            tmp += w.Compute( x)
        return tmp

class CO2_Scenario_2 (Control_Curve):
    def __init__( self):
        self.Name = "Сценарий #2: Плато с 2016 г"
        self.Wavelets = []
        self.Wavelets = [Hubbert( x0=2025.000, s0=0.04000, s1=0.04000, peak=38400.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1913.000, s0=0.08261, s1=0.10550, peak=1653.634, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1973.500, s0=0.41976, s1=0.43597, peak=2525.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=2000.000, s0=0.22813, s1=0.34509, peak=-4810.824, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1950.000, s0=0.44788, s1=0.34174, peak=-615.293, shift=0.000)]
        self.Projection = Sigmoid( 2009,0.8,40000,36400)
        return
    # computation
    def Compute( self, x):
        if x > 2016: return self.Projection.Compute(x) 
        tmp = 0.0
        for w in self.Wavelets:
            tmp += w.Compute( x)
        return tmp

class CO2_Scenario_3 (Control_Curve):
    def __init__( self):
        self.Name = "Сценарий #3: Рост до 2025 г"
        self.Wavelets = []
        self.Wavelets = [Hubbert( x0=2025.000, s0=0.04000, s1=0.04000, peak=38400.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1913.000, s0=0.08261, s1=0.10550, peak=1653.634, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1973.500, s0=0.41976, s1=0.43597, peak=2525.000, shift=0.000)]
        self.Wavelets += [Hubbert( x0=2000.000, s0=0.22813, s1=0.34509, peak=-4810.824, shift=0.000)]
        self.Wavelets += [Hubbert( x0=1950.000, s0=0.44788, s1=0.34174, peak=-615.293, shift=0.000)]
        self.Projection = Hubbert( 2025,0.065,0.065,40000)
        return
    # computation
    def Compute( self, x):
        if x > 2016: return self.Projection.Compute(x) 
        tmp = 0.0
        for w in self.Wavelets:
            tmp += w.Compute( x)
        return tmp

T_CO2, CO2_Cement = Load_Calibration( "CO2_Calibration.csv", "Year", "Cement")
CO2_Coal, CO2_Oil = Load_Calibration( "CO2_Calibration.csv", "Coal", "Oil")
CO2_Gas, CO2_Total = Load_Calibration( "CO2_Calibration.csv", "Gas", "Total")
T_CO2, CO2_BP = Load_Calibration( "CO2_Calibration.csv", "Year", "BP_2018")

T = np.linspace( 1800, 2100, 301)
l_real = len( T_CO2)
Scenario1 = CO2_Scenario_1().GetVector(T)
Scenario2 = CO2_Scenario_2().GetVector(T)
Scenario3 = CO2_Scenario_3().GetVector(T)
for i in range(l_real):
    Scenario1[i] = CO2_Total[i]
    Scenario2[i] = CO2_Total[i]
    Scenario3[i] = CO2_Total[i]

S = np.sum( CO2_Total) / 1000
S1 = 0
S2 = 0
for i in range( l_real):
    t = T_CO2[i]
    if 1990<t and t<=2000: S1 += CO2_Total[i] / 1000
    if 2000<t and t<=2010: S2  += CO2_Total[i] / 1000
    
print( "Всего CO2: {:.1f} ± {:.1f} млрд т".format( S, S*0.15))
print( "С 1991 по 2000 гг: {:.1f} ± {:.1f} млрд т".format( S1, S1*0.15))
print( "С 2001 по 2010 гг: {:.1f} ± {:.1f} млрд т".format( S2, S2*0.15))

fig = plt.figure( figsize=(15,10))
plt.plot( T, Scenario1, "--", lw=2, color='m', label="Сценарий #1: Обвал в 2014 г")
plt.plot( T, Scenario2, "-", lw=2, color='m', label="Сценарий #2: Плато с 2016 г")
plt.plot( T, Scenario3, "-.", lw=2, color='m', label="Сценарий #3: Рост до 2025 г")
plt.plot( T_CO2[165:], CO2_BP[165:], "-", lw=3, color='g', label="Собственная оценка BP (1965-2017)")
plt.errorbar( T_CO2, CO2_Cement, yerr=CO2_Cement*0.15, fmt='.', color="b", label="Производство цемента")
plt.errorbar( T_CO2, CO2_Coal, yerr=CO2_Coal*0.15, fmt='.', color="k", label="Каменный уголь")
plt.errorbar( T_CO2, CO2_Oil, yerr=CO2_Oil*0.15, fmt='.', color="g", label="Нефть и жидкости")
plt.errorbar( T_CO2, CO2_Gas, yerr=CO2_Gas*0.15, fmt='.', color="r", label="Природный газ")
plt.errorbar( T_CO2, CO2_Total, yerr=CO2_Total*0.15, fmt='o', color="m", label="ВСЕГО")
plt.xlabel("Годы")
plt.xlim( 1800, 2100)
plt.ylabel("Выбросы CO₂ [млн тонн]")
plt.ylim( 0, 45000)
plt.title( "Проверка отчётов BP по выбросам CO₂")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_09_13.png")
fig.show()
