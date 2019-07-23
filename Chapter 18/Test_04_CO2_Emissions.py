from Predictions import *
import scipy.stats as stat

#
# Calibrations
#
# Resources extraction (recalculated into mlrd toe)
resources = Resources()
Year = np.linspace(resources.Year[0], 2200, int( 2201-resources.Year[0]))
Res1 = resources.Total/1000
Res2 = np.zeros(len(Year))
for i, r in enumerate(Res1): Res2[i] = r
Year_Decimated = np.linspace(1830, 2200, 75)
Res_Decimated = Decimate( Res1, 5)

# CO2 emissions recalculated into fossil fuel production
# 1 ton of carbon = 3.66 ton of CO2
# 1 ton of carbon = 1.13 ton of oil equivalent (by fuel mix)
YearCO2, CO2 = Load_Calibration( "../Global Data/CO2_Calibration.csv", ["Year", "Total"])
YearCO2 = Year[30:]
CO2 = CO2[30:] / 3660
YearRCP, RCP_8_5, RCP_6_0, RCP_4_5, RCP_2_6 = Load_Calibration(
    "./Data/IPCC_Emission_Scenarios_RCP.txt",
    ["Year", "RCP_8_5", "RCP_6", "RCP_4_5", "RCP_2_6"],
    separator="\t")
RCP_8_5 = ArrayMerge( Res_Decimated, RCP_8_5[4:]*1.13)
RCP_6_0 = ArrayMerge( Res_Decimated, RCP_6_0[4:]*1.13)
RCP_4_5 = ArrayMerge( Res_Decimated, RCP_4_5[4:]*1.13)
RCP_2_6 = ArrayMerge( Res_Decimated, RCP_2_6[4:]*1.13)
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
Res_MY2018 = (MY2018.Coal+MY2018.Oil+MY2018.Gas)/1000
ERoEI_2P = Bathtub( 1965, s0=0.2, x1 = 2085, s1=0.15, middle=12852).GetVector(Year)
ERoEI_2P += Hubbert( 2018, 0.5, 0.1, -1600).GetVector(Year)
ERoEI_2P += Hubbert( 2050, 0.3, 0.14, 3070).GetVector(Year)
ERoEI_2P /= 1000
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
Res_Shark_Fin = SharkFin.GetVector(Year)

# Apply actual
for i, r in enumerate(Res1):
    RCP_8_5[i] = r
    RCP_6_0[i] = r
    RCP_4_5[i] = r
    RCP_2_6[i] = r
    Res_MY2018[i] = r
    ERoEI_2P[i] = r
    Res_Shark_Fin[i] = r

Cum_RCP_8_5 = Cumulative( RCP_8_5)
Cum_RCP_6_0 = Cumulative( RCP_6_0)
Cum_RCP_4_5 = Cumulative( RCP_4_5)
Cum_RCP_2_6 = Cumulative( RCP_2_6)
Cum_Res_MY2018 = Cumulative( Res_MY2018)
Cum_ERoEI_2P = Cumulative( ERoEI_2P)
Cum_Shark_Fin = Cumulative( Res_Shark_Fin)

limits = 1830, 2200

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(2, 1, height_ratios=[1,1])
ax1 = plt.subplot( gs[0])
ax2 = plt.subplot( gs[1])

ax1.set_title( "Сценарии IPCC 2013 г и добыча ископаемых энергоресурсов", fontsize=22)
ax1.plot( Year, RCP_8_5, "-.", lw=3, color="g", alpha=0.2)
ax1.text( 2201, RCP_8_5[-1], "8.5", color="g")
ax1.plot( Year, RCP_6_0, "--", lw=4, color="g", alpha=0.5)
ax1.text( 2201, RCP_6_0[-1], "6.0", color="g")
ax1.plot( Year, RCP_4_5, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax1.text( 2201, RCP_4_5[-1]-1, "4.5", color="g")
ax1.plot( Year, RCP_2_6, "--", lw=3, color="g", alpha=0.2)
ax1.text( 2075, 1, "2.6", color="g")
#ax1.plot( Year, Res_MY2018, ".", lw=4, color="m", alpha=0.5, label="Хаббертиана, URR=1200 млрд toe")
ax1.plot( Year, ERoEI_2P, "--", lw=4, color="m", alpha=0.5, label="Метод ERoEI, URR=1400 млрд toe")
ax1.plot( Year, Res_Shark_Fin, "-", lw=4, color="m", alpha=0.5, label="Акулий плавник, URR=1400 млрд toe")
ax1.plot( [2013, 2013], [5, 15], "-", lw=2, color="y", alpha=0.5)
ax1.text( 2007, 16, "IPCC-2013")
ax1.errorbar( resources.Year, Res1, yerr=Res1*0.1, fmt=".", color="k", label="Реальные (1830-2017)")
ax1.set_xlim( limits)
ax1.set_ylim( 0, 33)
ax1.set_yticks([5, 10, 15, 20, 25, 30])
ax1.set_ylabel("млрд toe")
ax1.grid( True)
ax1.legend( loc=0)

ax2.set_title( "Накопленная добыча", fontsize=22)
ax2.plot( Year, Cum_RCP_8_5, "-.", lw=3, color="g", alpha=0.2)
ax2.text( 2125, 3100, "8.5", color="g")
ax2.plot( Year, Cum_RCP_6_0, "--", lw=4, color="g", alpha=0.5)
ax2.text( 2201, Cum_RCP_6_0[-1], "6.0", color="g")
ax2.plot( Year, Cum_RCP_4_5, "-", lw=4, color="g", alpha=0.5, label="IPCC RCP 2013")
ax2.text( 2201, Cum_RCP_4_5[-1], "4.5", color="g")
ax2.plot( Year, Cum_RCP_2_6, "--", lw=3, color="g", alpha=0.2)
ax2.text( 2201, Cum_RCP_2_6[-1], "2.6", color="g")
#ax2.plot( Year, Cum_Res_MY2018, ".", lw=4, color="m", alpha=0.5, label="Хаббертиана, URR=1200 млрд toe")
ax2.plot( Year, Cum_ERoEI_2P, "--", lw=4, color="m", alpha=0.5, label="Метод ERoEI, URR=1400 млрд toe")
ax2.plot( Year, Cum_Shark_Fin, "-", lw=4, color="m", alpha=0.5, label="Акулий плавник, URR=1400 млрд toe")
ax2.plot( [limits[0], limits[1]], [1000, 1000], "--", lw=2, color="b", alpha=0.5)
ax2.text( 1831, 1020, "1P (наша оценка)", color="b", fontsize=12)
ax2.plot( [limits[0], limits[1]], [1300, 1300], "--", lw=2, color="k", alpha=0.5)
ax2.text( 1901, 1150, "1P (GEA)", color="k", fontsize=12)
ax2.plot( [limits[0], limits[1]], [1400, 1400], "-", lw=2, color="b", alpha=0.5)
ax2.text( 1831, 1420, "2P (наша оценка)", color="b", fontsize=12)
ax2.plot( [limits[0], limits[1]], [2400, 2400], "-.", lw=2, color="k", alpha=0.5)
ax2.text( 1901, 2420, "3P (GEA)", color="k", fontsize=12)
ax2.plot( [limits[0], limits[1]], [3300, 3300], "-.", lw=2, color="b", alpha=0.5)
ax2.text( 1831, 3320, "3P (наша оценка)", color="b", fontsize=12)
ax2.set_xlim( limits)
ax2.set_ylabel("млрд toe")
ax2.set_ylim( 0, 3500)
ax2.set_yticks([1000, 2000, 3000])
ax2.grid( True)
#ax2.legend( loc=0)
ax2.set_xlabel("год")

plt.savefig( "./Graphs/figure_18_04.png")
if InteractiveModeOn: plt.show(True)
