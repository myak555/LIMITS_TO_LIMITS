from Population import *

Year_US, Gas_US = Load_Calibration("../Global Data/US_Fossil_Fuel_Reconstructed.csv", ["Year", "Gas"])
Gas_US *= 1.1

Year_US2 = np.linspace( 1970, 2017, 48)
Gas_US2 = np.array([
    571.5,587.7,585.8,585.2,559.4,
    518.0,513.8,516.1,513.9,529.5,
    525.1,519.6,483.2,437.7,475.0,
    447.9,436.3,452.0,464.2,470.7,
    483.4,480.8,484.7,490.2,510.3,
    503.3,510.2,511.5,517.3,510.1,
    518.6,531.9,511.2,517.9,503.1,
    489.4,501.7,521.9,546.1,557.6,
    575.2,617.4,649.1,655.7,704.7,
    740.3,729.3,734.5])

# Correction from BP report of 2018 0.90
# Correction from BP report of 2017 0.95
# in 2018 BP systematically decreased all US volumes by 5% 

US_Conventional_Func = [Hubbert( x0=1972.000, s0=0.16677, s1=0.22197, peak=625.000, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1953.000, s0=0.29007, s1=0.37774, peak=170.000, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1998.000, s0=0.27681, s1=0.13407, peak=450.000, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1988.500, s0=0.36475, s1=0.42396, peak=287.353, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1980.505, s0=0.65610, s1=0.49916, peak=174.574, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=2021.046, s0=0.27961, s1=0.08666, peak=83.381, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1938.088, s0=0.28243, s1=0.36088, peak=71.220, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1929.143, s0=0.27130, s1=1.08900, peak=41.936, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1960.018, s0=0.59049, s1=0.63025, peak=75.787, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1944.869, s0=0.65610, s1=0.81000, peak=37.358, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1916.447, s0=0.18530, s1=0.42190, peak=20.594, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1984.112, s0=1.92923, s1=2.59374, peak=33.329, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=2015.131, s0=0.42616, s1=0.70735, peak=19.199, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1998.251, s0=0.59049, s1=0.51443, peak=-20.353, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1974.878, s0=1.00000, s1=1.00000, peak=-29.291, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1953.526, s0=1.00000, s1=1.00000, peak=-14.193, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=1988.729, s0=1.00000, s1=1.00000, peak=-15.759, shift=0.000)]
US_Conventional_Func += [Hubbert( x0=2008.061, s0=1.00000, s1=1.00000, peak=15.748, shift=0.000)]

US_Unconventional_Func = [Hubbert( x0=2021.000, s0=0.14418, s1=0.11651, peak=621.499, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=1993.966, s0=0.38355, s1=0.64954, peak=73.382, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=2012.241, s0=0.80190, s1=0.64954, peak=69.827, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=2000.058, s0=0.65610, s1=0.79388, peak=30.272, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=1983.488, s0=0.20589, s1=0.34519, peak=31.181, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=1991.854, s0=1.00000, s1=1.00000, peak=-9.563, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=2041.806, s0=1.00000, s1=1.00000, peak=11.528, shift=0.000)]
US_Unconventional_Func += [Hubbert( x0=0.000, s0=1.00000, s1=1.00000, peak=1.000, shift=0.000)]

Year = np.linspace(1800,2200,401)
#Year = np.linspace(1970, 2017, 48)
Conventional = np.zeros(len(Year))
Unconventional = np.zeros(len(Year))

for f in US_Conventional_Func: Conventional += f.GetVector(Year)
for f in US_Unconventional_Func: Unconventional += f.GetVector(Year)
Conventional *= 0.95
Unconventional *= 0.95

Total = Conventional + Unconventional
for i in range( len(Year_US)-4):
    Total[i] = Gas_US[i]

Prediction_T = np.linspace( 2018, 2200, 183)
Prediction_Conventional = Hubbert( 1998, 1, .085, 600, 100).GetVector( Prediction_T)
Prediction_TG_Hughes = Hubbert( 2016, 1, .07, 428).GetVector( Prediction_T)
Prediction_Total_Hughes = (Prediction_Conventional + Prediction_TG_Hughes) * 0.88 

Cum_Conventional = np.array(Conventional)
for i in range( 1, len(Cum_Conventional)): Cum_Conventional[i] += Cum_Conventional[i-1]

Cum_Total = np.array(Total)
for i in range( 1, len(Cum_Total)): Cum_Total[i] += Cum_Total[i-1]

fig = plt.figure( figsize=(15,10))
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title( 'Добыча природного газа в США 1900-2017 гг')
ax1.plot( Year[170:], Conventional[170:], "-", lw=2, color="g", label="Газ из проницаемых пород")
ax1.plot( Year[150:], Unconventional[150:], "--", lw=2, color="r", label="Газ из ТрИЗ, URR={:.1f} трлн м³".format(np.sum(Unconventional)/1000))
ax1.plot( Prediction_T, Prediction_Total_Hughes, ".", lw=1, color="r", label="Хьюз (2016), URR={:.1f} трлн м³".format(np.sum(Prediction_Total_Hughes)/1000+34.2))
ax1.errorbar( Year_US2, Gas_US2, yerr=Gas_US2*0.05, fmt='.', color="m", label="BP с 1970 по 2017, UR={:.1f} трлн м³".format(np.sum(Gas_US2)/1000))
ax1.plot( Year, Total, "-", lw=2, color="r", label="Лагеррер (2014)")
ax1.annotate("Добыто с 1821 года: {:.1f} трлн м³".format( np.sum(Total[0:217])/1000), xy=(2017, 763), xytext=(2030, 800), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate('Конец "сланцевой революции"', xy=(2021, 594), xytext=(2030, 650), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 1000)
ax1.set_ylabel("миллиардов м³ в год")
ax1.grid(True)
ax1.legend(loc=0)

ax2.errorbar( [1956], [30], fmt="o", color='g', label="Оценка Хабберта 1956 г: URR=30 трлн м³")
ax2.plot( [1900,2100], [30,30], "--", lw=1, color='g')
ax2.plot( Year, Cum_Conventional/1000, "-", lw=2, color="g", label="Газ из проницаемых пород, URR={:.1f} трлн м³".format(np.sum(Conventional)/1000))
ax2.plot( Year, Cum_Total/1000, "-", lw=2, color="r", label="Весь газ, Лагеррер (2014), URR={:.1f} трлн м³".format(np.sum(Total)/1000))
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 60)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Трлн м³")
ax2.grid(True)
ax2.set_title( "Накопленная добыча")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_14_10.png")
if InteractiveModeOn: plt.show(True)
