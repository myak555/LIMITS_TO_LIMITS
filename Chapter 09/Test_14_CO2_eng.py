from Predictions import *

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

#
# Models reagent sequestration
# Q0 - balance concentaration
# q(t), as a control curve - reagent addition (removal)
# q_norm - total system volume to compute concentarations
# d_rate - reaction speed
# uncertainty - sustematic error in q estimate
#
class Reagent_Sequestration:
    def __init__( self, Q0, q, q_norm, d_rate, uncertainty=1.0):
        self.Q_Initial = Q0
        self.Q = Q0
        self.B = q
        self.B_norm = q_norm
        self.D = d_rate
        self.U = uncertainty
        return
    def dQ_dt( self, t):
        tmp = self.U * self.B.Compute( t) / self.B_norm
        tmp += self.D * (1.0-self.Q/self.Q_Initial)
        return tmp
    def _func( self, y, t):
        self.Q = max( [y[0], 0])
        f0 = self.dQ_dt( t)
        return [f0]
    def Solve( self, t0):
        y0 = [self.Q]
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.0025)
        self.Solution_Time = t0
        self.Solution_Q = soln[:, 0].clip(0)
        self.Q = self.Q_Initial
        return

#
# Models reagent sequestration via convolution
# Q0 - balance concentaration
# q(t), as a control curve - reagent addition (removal)
# q_norm - total system volume to compute concentarations
# sigma - 1/characteristic reaction time
# q_corr - array with real measirements for calibrations
# uncertainty - sustematic error in q estimate
#
class Reagent_Sequestration_Analytical:
    def __init__( self, Q0, q, q_norm, sigma, q_corr=[], corr_start=0, corr_end=0, uncertainty=1.0):
        self.Q_Initial = Q0
        self.B = q
        self.B_norm = q_norm
        self.Sigma = sigma
        self.U = uncertainty
        self.Corr = q_corr
        self.Corr0 = corr_start
        self.Corr1 = corr_end
        return
    def Solve( self, t0):
        self.Solution_Time = t0
        l = len(t0)
        tmpTime = np.linspace( 0, t0[ l-1]-t0[0], l)
        tmp = self.B.GetVector( t0)
        for i in range( 1):
            if t0[i] < self.Corr0: continue
            if t0[i] > self.Corr1: continue
            tmp[i] = self.Corr[i]
        tmp = self.U * tmp / self.B_norm - self.Sigma
        Exp = np.exp( -self.Sigma * tmpTime)
        tmp = np.convolve( tmp, Exp) + self.Q_Initial
        self.Solution_Q = np.array(tmp[:l])
        return

#
# Calibration data
#
T_ML, ML_PPM = Load_Calibration( "../Global Data/CO2_Mauna_Loa.csv", ["Year", "Mean"])
T_LD, LD_PPM = Load_Calibration( "../Global Data/Ice_Core_Law_Dome.csv", ["Year", "Total"])
Interpolation = Interpolation_Realistic_2018()

#
# Solve numerically
#
T = np.linspace(1800, 2100, 301)
Interpolation.Solve( T)
Interpolation.Correct_To_Actual(1800, 2016)
Q0 = 284.0                          # pre-industrial CO2 concentration, ppm
M_atmosphere = 5.1480e9             # mln tonn
conversion = 0.658e6                # conversion from mass ppm to ppmv
norm = M_atmosphere / conversion
uncertainty = 1.0
sigma1 = np.log(2) / 38
sigma2 = np.log(2) / 37
sigma3 = np.log(2) / 37
Sequestration_1 = Reagent_Sequestration( Q0, CO2_Scenario_1(), norm, Q0 * sigma1)
Sequestration_1.Solve( T)
Sequestration_2 = Reagent_Sequestration( Q0, CO2_Scenario_2(), norm, Q0 * sigma2)
Sequestration_2.Solve( T)
Sequestration_3 = Reagent_Sequestration( Q0, CO2_Scenario_3(), norm, Q0 * sigma3)
Sequestration_3.Solve( T)
Sequestration_1e = Reagent_Sequestration_Analytical( Q0, CO2_Scenario_1(), norm, sigma1, Interpolation.CO2_Emissions, 1800, 2016)
Sequestration_1e.Solve( T)
Sequestration_2e = Reagent_Sequestration_Analytical( Q0, CO2_Scenario_2(), norm, sigma2, Interpolation.CO2_Emissions, 1800, 2016)
Sequestration_2e.Solve( T)
Sequestration_3e = Reagent_Sequestration_Analytical( Q0, CO2_Scenario_3(), norm, sigma3, Interpolation.CO2_Emissions, 1800, 2016)
Sequestration_3e.Solve( T)

conc = 0
for i in range( len(T_LD)):
    if T_LD[i] == 1896: print( T_LD[i], LD_PPM[i])
    if T_LD[i] != 1956: continue
    print( T_LD[i], LD_PPM[i])
    conc = LD_PPM[i]
    break
for i in range( len(T_ML)):
    if T_ML[i] != 2017: continue
    print( T_ML[i], ML_PPM[i])
    print( "Increase {:.1f}% per 100 years".format( (ML_PPM[i]/conc-1)/(2017-1956)*10000))
    break

fig = plt.figure( figsize=(15,10))
##plt.plot( T, Sequestration_1.Solution_Q, "--", lw=2, color='m', label=Sequestration_1.B.Name)
##plt.plot( T, Sequestration_2.Solution_Q, "-", lw=2, color='m', label=Sequestration_2.B.Name)
##plt.plot( T, Sequestration_3.Solution_Q, "-.", lw=2, color='m', label=Sequestration_3.B.Name)
##plt.plot( T, Sequestration_1e.Solution_Q, "--", lw=2, color='r', label=Sequestration_1.B.Name + " (свёртка)")
##plt.plot( T, Sequestration_2e.Solution_Q, "-", lw=2, color='r', label=Sequestration_2.B.Name + " (свёртка)")
##plt.plot( T, Sequestration_3e.Solution_Q, "-.", lw=2, color='r', label=Sequestration_3.B.Name + " (свёртка)")
plt.errorbar( T_ML, ML_PPM, yerr=ML_PPM*0.005, fmt='.', color="b", label="Direct observations (Mauna Loa, HI)")
plt.errorbar( T_LD, LD_PPM, yerr=LD_PPM*0.020, fmt='.', color="g", label="Ice core content (Law Dome CO₂ station, Antarctica)")
plt.xlabel("Year")
plt.xlim( 1830, 2030)
plt.ylabel("Atmosphere CO₂ Concentration [ppmv]")
#plt.ylim( 300, 410)
plt.title( "Accumulation of Anthropgenic CO₂ in Atmosphere")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_09_14_eng.png")
if InteractiveModeOn: plt.show(True)
