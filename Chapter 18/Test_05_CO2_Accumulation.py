from Predictions import *
import scipy.stats as stat

#
# Models reagent sequestration via convolution
# Q0 - balance concentaration
# q(t) - reagent addition (removal)
# q_norm - total system volume to compute concentarations
# sigma - 1/characteristic reaction time
# uncertainty - sustematic error in q estimate
#
class CO2_Sequestration_Analytical:
    def __init__( self, model_start=1800, model_end=2200):
        self.Interpolation = Interpolation_Realistic_2018()
        self.Interpolation.Solve( np.arange(model_start, 2018, 1))
        self.Interpolation.Correct_To_Actual(1800, 2018)
        self.Q_Initial = 284.0           # pre-industrial CO2 concentration, ppm
        self.M_atmosphere = 5.1480e9     # mln tonn
        self.conversion = 0.658e6        # conversion from mass ppm to ppmv
        self.Sigma = np.log(2) / 37
        self.Uncertainty = 10.0
        return
    def Solve( self, t0, q, forceActual=False):
        l = len(t0)
        self.Solution_Time = t0
        self.Exp = np.exp(-self.Sigma * (t0-t0[0]))
        self.Solution_Total = np.ones( l) * self.Q_Initial
        for i in range(l):
            tmp = q[i] / self.M_atmosphere * self.conversion * self.Exp
            self.Solution_Total[i:] += tmp[:l-i]
        if not forceActual: return np.array( self.Solution_Total)
        k = len(self.Interpolation.CO2)
        self.Solution_Total[:k] = self.Interpolation.CO2
        return np.array( self.Solution_Total)

#
# Central England Temperatures
#
Y_CET, T_CET = Load_Calibration("./Data/Central_England_Temperature_Dataset.txt", "Year", "YEAR_Average", separator='\t')
baseline = np.average(T_CET[:1750-1659])
dT_CET = T_CET - baseline
dT_CET_30 = Filter( dT_CET, matrix=np.ones(31)) 

#
# Calibrations
#
# Resources extraction (recalculated into mlrd toe)
resources = Resources()
Year = np.linspace(resources.Year[0], 2200, int( 2201-resources.Year[0]))
Res1 = resources.Total / 1.13 * 3.66 # Convert to CO2
Res2 = np.zeros(len(Year))
for i, r in enumerate(Res1): Res2[i] = r
Year_Decimated = np.linspace(1830, 2200, 75)
Res_Decimated = Decimate( Res1, 5)

# CO2 emissions and actual concentration
CO2seq = CO2_Sequestration_Analytical( model_start=Year[0])

filename = "./Data/IPCC_Emission_Scenarios_RCP.txt"
YearRCP, RCP_8_5 = Load_Calibration( filename, "Year", "RCP_8_5", separator="\t")
RCP_6_0, RCP_4_5 = Load_Calibration( filename, "RCP_6", "RCP_4_5", separator="\t")
RCP_2_6, RCP_2_6 = Load_Calibration( filename, "RCP_2_6", "RCP_2_6", separator="\t")
RCP_8_5 = ArrayMerge( Res_Decimated, RCP_8_5[4:]*3660)
RCP_6_0 = ArrayMerge( Res_Decimated, RCP_6_0[4:]*3660)
RCP_4_5 = ArrayMerge( Res_Decimated, RCP_4_5[4:]*3660)
RCP_2_6 = ArrayMerge( Res_Decimated, RCP_2_6[4:]*3660)
RCP_8_5 = np.interp(Year, Year_Decimated, RCP_8_5)
RCP_6_0 = np.interp(Year, Year_Decimated, RCP_6_0)
RCP_4_5 = np.interp(Year, Year_Decimated, RCP_4_5)
RCP_2_6 = np.interp(Year, Year_Decimated, RCP_2_6)
Matr = np.ones(11)
RCP_8_5 = Filter(RCP_8_5, matrix=Matr)
RCP_6_0 = Filter(RCP_6_0, matrix=Matr)
RCP_4_5 = Filter(RCP_4_5, matrix=Matr)
RCP_2_6 = Filter(RCP_2_6, matrix=Matr)

# Production models
MY2018 = Interpolation_Realistic_2018()
MY2018.Solve(Year)
MY2018.Correct_To_Actual( 1830, 2017)
ERoEI_2P = Bathtub( 1965, s0=0.2, x1 = 2085, s1=0.15, middle=12852).GetVector(Year)
ERoEI_2P += Hubbert( 2018, 0.5, 0.1, -1600).GetVector(Year)
ERoEI_2P += Hubbert( 2050, 0.3, 0.14, 3070).GetVector(Year)
ERoEI_2P /= 1.13
ERoEI_2P *= 3.66
SharkFin = Linear_Combo() 
SharkFin.Wavelets += [Hubbert( x0=2059.000, s0=0.03471, s1=0.10632, peak=16.100, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=1973.000, s0=0.20589, s1=0.54487, peak=2.143, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=1979.000, s0=0.65610, s1=0.31381, peak=2.252, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=1989.730, s0=0.43047, s1=0.28243, peak=1.885, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=2012.973, s0=0.15009, s1=0.12036, peak=2.157, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=2091.892, s0=0.28243, s1=0.20589, peak=0.357, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=2068.108, s0=0.34868, s1=0.31067, peak=-0.660, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=2048.108, s0=0.28243, s1=0.34868, peak=-0.353, shift=0.000)]
SharkFin.Wavelets += [Hubbert( x0=1917.297, s0=0.09135, s1=0.05686, peak=0.385, shift=0.000)]
Res_Shark_Fin = SharkFin.GetVector(Year) / 1.13
Res_Shark_Fin *= 3660

# Apply actual
for i, r in enumerate(Res1):
    RCP_8_5[i] = r
    RCP_6_0[i] = r
    RCP_4_5[i] = r
    ERoEI_2P[i] = r
    Res_Shark_Fin[i] = r

CO2_RCP_8_5 = CO2seq.Solve( Year, RCP_8_5, True)
CO2_RCP_6_0 = CO2seq.Solve( Year, RCP_6_0, True)
CO2_RCP_4_5 = CO2seq.Solve( Year, RCP_4_5, True)
CO2_RCP_2_6 = CO2seq.Solve( Year, RCP_2_6, True)
CO2_ERoEI_2P = CO2seq.Solve( Year, ERoEI_2P, True)
CO2_Shark_Fin = CO2seq.Solve( Year, Res_Shark_Fin, True)

ln2 = np.log(2)
shift = 0.2
TCR_ECS = Sigmoid( 2000, 0.05, 1.33, 1.66).GetVector(Year)
TCR_ECS_err = Sigmoid( 2000, 0.05, 1.90, 2.70).GetVector(Year) - TCR_ECS 
#TCR_ECS = Sigmoid( 2100, 0.05, 2.5, 2.5).GetVector(Year)
#TCR_ECS_err = Sigmoid( 2100, 0.05, 4.5, 4.5).GetVector(Year) - TCR_ECS 
#TCR_ECS = Sigmoid( 2100, 0.05, 1.66, 1.66).GetVector(Year)
#TCR_ECS_err = Sigmoid( 2100, 0.05, 2.70, 2.70).GetVector(Year) - TCR_ECS 
log_RCP_8_5 = np.log( CO2_RCP_8_5 / CO2seq.Q_Initial) / ln2
T_RCP_8_5 = log_RCP_8_5 * TCR_ECS + shift
T_RCP_8_5_err = log_RCP_8_5 * TCR_ECS_err
log_RCP_6_0 = np.log( CO2_RCP_6_0 / CO2seq.Q_Initial) / ln2
T_RCP_6_0 = log_RCP_6_0 * TCR_ECS + shift
T_RCP_6_0_err = log_RCP_6_0 * TCR_ECS_err
log_RCP_4_5 = np.log( CO2_RCP_4_5 / CO2seq.Q_Initial) / ln2
T_RCP_4_5 = log_RCP_4_5 * TCR_ECS + shift
T_RCP_4_5_err = log_RCP_4_5 * TCR_ECS_err
log_RCP_2_6 = np.log( CO2_RCP_2_6 / CO2seq.Q_Initial) / ln2
T_RCP_2_6 = log_RCP_2_6 * TCR_ECS + shift
T_RCP_2_6_err = log_RCP_2_6 * TCR_ECS_err
T_ERoEI_2P = np.log( CO2_ERoEI_2P / CO2seq.Q_Initial) / ln2 * TCR_ECS + shift
T_MY2018 = np.log( MY2018.CO2 / CO2seq.Q_Initial) / ln2 * TCR_ECS + shift
T_ERoEI_2P = np.log( CO2_ERoEI_2P / CO2seq.Q_Initial) / ln2 * TCR_ECS + shift
T_Shark_Fin = np.log( CO2_Shark_Fin / CO2seq.Q_Initial) / ln2 * TCR_ECS + shift

limits = 1650, 2200

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.set_title( "Концентрация CO₂ в атмосфере", fontsize=22)
unc = np.ones(len(CO2seq.Interpolation.Time)) * 0.5
for i in range(126,-1,-1): unc[i] = 10  
ax1.errorbar( CO2seq.Interpolation.Time, CO2seq.Interpolation.CO2,
              yerr=unc, fmt=".", color="k", alpha=0.2, label="Реальная (1830-2018)")
ax1.plot( Year, CO2_RCP_8_5, "-.", lw=3, color="g", alpha=0.2)
ax1.text( 2201, CO2_RCP_8_5[-1], "8.5", color="g")
ax1.plot( Year, CO2_RCP_6_0, "--", lw=3, color="g", alpha=0.5)
ax1.text( 2201, CO2_RCP_6_0[-1], "6.0", color="g")
ax1.plot( Year, CO2_RCP_4_5, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax1.text( 2201, CO2_RCP_4_5[-1], "4.5", color="g")
ax1.plot( Year, CO2_RCP_2_6, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax1.text( 2201, CO2_RCP_2_6[-1], "2.6", color="g")
ax1.plot( Year, MY2018.CO2, ".", lw=2, color="r", alpha=0.5, label="Хаббертиана, URR=1200 млрд toe")
ax1.plot( Year, CO2_ERoEI_2P, "--", lw=4, color="m", alpha=0.5, label="Метод ERoEI, URR=1400 млрд toe")
ax1.plot( Year, CO2_Shark_Fin, "-", lw=4, color="m", alpha=0.5, label="Акулий плавник, URR=1400 млрд toe")
ax1.set_xlim( limits)
ax1.set_ylabel("ppmv")
ax1.set_ylim( 0, 1000)
ax1.grid( True)
ax1.legend( loc=0)

ax2.set_title( "Эффект Аррениуса", fontsize=22)
ax2.plot( Year, T_RCP_8_5, "-.", lw=2, color="g", alpha=0.5)
#ax2.bar( Year,  T_RCP_8_5_err, bottom=T_RCP_8_5, width=1, color="r", alpha=0.05)
ax2.text( 2201, T_RCP_8_5[-1], "8.5", color="g")
ax2.plot( Year, T_RCP_6_0, "--", lw=3, color="g", alpha=0.5)
ax2.bar( Year,  T_RCP_6_0_err, bottom=T_RCP_6_0, width=1, color="y", alpha=0.2)
ax2.text( 2201, T_RCP_6_0[-1], "6.0", color="g")
ax2.plot( Year, T_RCP_4_5, "-", lw=3, color="g", alpha=0.5, label="IPCC RCP 2013")
ax2.bar( Year,  T_RCP_4_5_err, bottom=T_RCP_4_5-T_RCP_4_5_err, width=1, color="y", alpha=0.2)
ax2.bar( Year,  T_RCP_6_0-T_RCP_4_5, bottom=T_RCP_4_5, width=1, color="y", alpha=0.2)
ax2.text( 2201, T_RCP_4_5[-1], "4.5", color="g")
ax2.plot( Year, T_RCP_2_6, "-.", lw=2, color="g", alpha=0.5)
ax2.text( 2201, T_RCP_2_6[-1], "2.6", color="g")
ax2.plot( Year, T_MY2018, ".", lw=2, color="r", alpha=0.5, label="Хаббертиана, URR=1200 млрд toe")
ax2.plot( Year, T_ERoEI_2P, "--", lw=4, color="m", alpha=0.5, label="Метод ERoEI, URR=1400 млрд toe")
ax2.plot( Year, T_Shark_Fin, "-", lw=4, color="m", alpha=0.5, label="Акулий плавник, URR=1400 млрд toe")
ax2.errorbar( Y_CET, dT_CET_30,yerr=0.46, fmt="o", color="k", alpha=0.2, label="Среднегодовые Центральной Англии (30-летний фильтр)")
ax2.set_xlim( limits)
ax2.set_ylabel("°Ц от среднего до 1750 года")
ax2.set_ylim( -1, 3.5)
ax2.grid( True)
ax2.legend( loc=0)
ax2.set_xlabel("год")

plt.savefig( ".\\Graphs\\figure_18_05.png")
fig.show()
