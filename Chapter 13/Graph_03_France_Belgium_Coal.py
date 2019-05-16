from Utilities import *

data_name = "./Data/France_Belgium_Coal_Reconstructed.csv"

Coal_Production_Functions = [Hubbert( x0=1953.000, s0=0.04277, s1=0.09793, peak=88.000, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1912.000, s0=0.07281, s1=0.51050, peak=21.000, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1872.614, s0=0.12561, s1=0.30377, peak=17.826, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1846.023, s0=0.19684, s1=1.00000, peak=3.919, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1870.159, s0=1.00000, s1=1.00000, peak=-4.004, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1882.636, s0=0.59049, s1=0.52087, peak=13.305, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1889.795, s0=0.83047, s1=0.41669, peak=12.074, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1899.000, s0=0.47830, s1=0.37591, peak=8.360, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1915.159, s0=1.00000, s1=0.52613, peak=-26.258, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1927.636, s0=0.55038, s1=0.89100, peak=13.923, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1944.818, s0=0.43047, s1=0.57874, peak=-25.640, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1965.682, s0=0.72900, s1=0.58459, peak=10.796, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1984.295, s0=0.42190, s1=0.28363, peak=15.158, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1854.409, s0=1.00000, s1=1.00000, peak=3.761, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1944.205, s0=4.70817, s1=5.29670, peak=-20.000, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1987.568, s0=1.33100, s1=1.00000, peak=-5.567, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=2005.773, s0=0.63025, s1=0.24854, peak=-1.749, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1916.386, s0=1.00000, s1=3.08137, peak=6.271, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1946.250, s0=1.00000, s1=1.00000, peak=5.833, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1957.091, s0=1.00000, s1=1.00000, peak=3.638, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1908.409, s0=0.56022, s1=0.65610, peak=2.021, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1895.932, s0=1.00000, s1=1.00000, peak=1.673, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1930.500, s0=1.00000, s1=1.00000, peak=6.064, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1920.886, s0=1.00000, s1=1.00000, peak=-3.504, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1931.523, s0=3.11249, s1=1.36618, peak=-6.336, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1912.705, s0=1.00000, s1=1.00000, peak=2.433, shift=0.000)]
Coal_Production_Functions += [Hubbert( x0=1914.341, s0=1.00000, s1=1.00000, peak=-3.949, shift=0.000)]

Year,Total = Load_Calibration( data_name, ["Year", "Total_toe"]) 
Estimate = np.zeros( len(Year))
for c in Coal_Production_Functions:
    Estimate += c.GetVector( Year)
Estimate *= 0.6

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча каменного угля во Франции и Бельгии", fontsize=22)
gs = plt.GridSpec(1, 1, height_ratios=[1]) 
ax1 = plt.subplot(gs[0])

ax1.errorbar( Year, Total, yerr=Total*0.1, fmt = '.', color='m')
ax1.errorbar( Year, Total, yerr=Total*0.1, fmt = '.', color='m')
ax1.plot( Year, Estimate, "-", lw=2, color='k', label="Аппроксимация ({:.2f} 10⁹ toe)".format(np.sum(Estimate)/1000))
ax1.set_ylim( 0, 60)
ax1.set_ylabel("Млн toe в год")
ax1.set_xlim( 1800, 2030)
ax1.grid(True)
ax1.legend(loc=2)
ax1.set_xlabel("Годы")
ax1.annotate("Пик добычи по энергии в 1956 году", xy=(1956, 53), xytext=(1973, 55), arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig( "./Graphs/figure_13_03.png")
if InteractiveModeOn: plt.show(True)
