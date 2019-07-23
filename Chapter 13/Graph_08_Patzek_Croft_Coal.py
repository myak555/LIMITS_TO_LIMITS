from Utilities import *

data_name = "./Data/Coal_Patzek_Croft_EJ.csv"
calibration_name = "../Global Data/Resources_Calibration.csv"
var_names = ["Year", "Coal"]

Coal_Production_Function = Linear_Combo()
Coal_Production_Function.Wavelets +=[Hubbert( x0=2011.000, s0=0.03814, s1=0.04697, peak=158.000)]
Coal_Production_Function.Wavelets += [Hubbert( x0=1994.909, s0=0.05686, s1=0.05491, peak=-43.461)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1916.727, s0=0.12688, s1=0.14711, peak=16.132)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=2010.545, s0=0.47351, s1=0.25361, peak=35.696)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1890.545, s0=0.10567, s1=0.22316, peak=3.681)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1945.091, s0=0.33335, s1=0.52935, peak=4.048)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1934.909, s0=1.00000, s1=1.00000, peak=-2.177)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1989.818, s0=0.42616, s1=0.58743, peak=6.794)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=2055.636, s0=0.16014, s1=0.16069, peak=-2.188)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=2120.000, s0=0.12884, s1=0.07107, peak=2.216)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=2014.545, s0=1.00000, s1=1.00000, peak=-8.623)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=1969.818, s0=0.14966, s1=0.64954, peak=-1.926)]
Coal_Production_Function.Wavelets += [ Hubbert( x0=2132.000, s0=0.16677, s1=0.23344, peak=-0.803)]

Time = np.linspace(1800, 2400, 601)
Year,Total = Load_Calibration( data_name, var_names)
Estimate = Coal_Production_Function.GetVector( Time) / 41 * 1050
Estimate2 = Hubbert(x0=2013, s0=0.2, s1=0.039, peak=4000).GetVector(Time)
Estimate3 = Hubbert(x0=2025, s0=0.045, s1=0.025, peak=4400).GetVector(Time)
Estimate4 = Hubbert(x0=2050, s0=0.020, s1=0.0152, peak=4000).GetVector(Time)

Year_C, Total_C = Load_Calibration( calibration_name, var_names)
for i in range( len(Year_C)):
    if Year_C[i] <= 2010: Estimate[i+30] = Total_C[i]
    if Year_C[i] <= 2010: Estimate2[i+30] = Total_C[i]
    if Year_C[i] <= 2008: Estimate3[i+30] = Total_C[i]
    Estimate4[i+30] = Total_C[i]

for i in range( 30):
    Estimate4[i] = Estimate3[i]

Sum = Cumulative(Estimate2) / np.sum( Estimate2) 
for i in range( 250, 300):
    print( "{:g}\t{:>8.2f}".format(Time[i], Sum[i]))

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча каменного угля - предсказание Т.Пазека и Г.Крофта, 2010", fontsize=22)
gs = plt.GridSpec(1, 1, height_ratios=[1]) 
ax1 = plt.subplot(gs[0])

ax1.errorbar( Year_C, Total_C, yerr=Total_C*0.05, fmt = '.', color='g')
#ax1.errorbar( Year, Total*1000/41, fmt = 'o', color='m')
ax1.plot( Time, Estimate, "-", lw=2, color='k', label="Пазек и Крофт, URR = {:.1f} 10⁹ toe".format(np.sum(Estimate)/1000))
ax1.plot( Time, Estimate2, "-", lw=2, color='b', label="Рутлидж, URR = {:.1f} 10⁹ toe".format(np.sum(Estimate2)/1000))
ax1.plot( Time, Estimate3, "--", lw=1, color='g', label="BP-2008, URR = {:.1f} 10⁹ toe".format(np.sum(Estimate3)/1000))
ax1.plot( Time, Estimate4, "-.", lw=1, color='g', label="BP-2017, URR = {:.1f} 10⁹ toe".format(np.sum(Estimate4)/1000))
ax1.plot( [2070,2070], [0,4500], "--", lw=1, color='b')
ax1.set_ylim( 0, 4500)
ax1.set_ylabel("Млн toe в год")
ax1.set_xlim( 1800, 2200)
ax1.grid(True)
ax1.legend(loc=0)
ax1.set_xlabel("Годы")
ax1.annotate("Пик добычи по энергии в 2011 году", xy=(2011, 4000), xytext=(2050, 4200), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("К 2070 году добыто 90% запасов", xy=(2070, 1400), xytext=(2080, 2000), arrowprops=dict(facecolor='blue', shrink=0.05))

plt.savefig( "./Graphs/figure_13_08.png")
if InteractiveModeOn: plt.show(True)
