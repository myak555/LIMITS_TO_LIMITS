from Utilities import *

data_name = "./Data/Coal_Russian_Empire.csv"

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

Year,Poland,Republics,Russia = Load_Calibration(
    data_name,
    ["Year", "Poland", "Republics", "Russia"])
Finland = np.zeros(len(Year))
Republics += Poland
Russia += Republics
Poland_toe = np.array(Poland)
Poland_Finland_toe = np.array(Poland)
Republics_toe = np.array(Republics)
Russia_toe = np.array(Russia)
for i in range( len( Poland_toe)-1):
    Poland_toe[i+1] += Poland_toe[i]  
    Poland_Finland_toe[i+1] += Poland_Finland_toe[i]  
    Republics_toe[i+1] += Republics_toe[i]  
    Russia_toe[i+1] += Russia_toe[i]  
Poland_toe *= 0.6 / (0.313)
Poland_Finland_toe *= 0.6 / (0.313 + 0.338)
Republics_toe *= 0.6 / (0.313 + 0.338 + 22.402 - 17.098)
Russia_toe *= 0.6 / (0.313 + 0.338 + 22.402)

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча каменного угля в Российской империи", fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.errorbar( Year, Russia, yerr=Russia*0.05, fmt = '.', color='r', label="Российская империя всего, Q = {:.1f} млрд т".format(np.sum(Russia)/1000))
ax1.errorbar( Year, Republics, yerr=Republics*0.05, fmt = '.', color='b', label="Финляндия+Польша+республики СССР, Q = {:.1f} млрд т".format(np.sum(Republics)/1000))
ax1.errorbar( Year, Poland, yerr=Poland*0.05, fmt = '.', color='g', label="Финляндия+Польша, Q = {:.1f} млрд т".format(np.sum(Poland)/1000))
ax1.errorbar( Year, Finland, fmt = '.', color='m', label="Финляндия")
#ax1.plot( Year, Estimate, "-", lw=2, color='k', label="Аппроксимация ({:.2f} 10⁹ toe)".format(np.sum(Estimate)/1000))
#ax1.set_ylim( 0, 60)
ax1.set_ylabel("Млн тонн в год")
ax1.set_xlim( 1850, 2050)
ax1.grid(True)
ax1.legend(loc=2)
ax1.annotate("Пик добычи в 1988 году", xy=(1988, 1088), xytext=(2000, 900), arrowprops=dict(facecolor='black', shrink=0.05))

ax2.plot( Year, Poland_toe, "-", color='g', label = "Польша: {:.0f}".format(Poland_toe[len(Poland_toe)-1]))
ax2.plot( Year, Poland_Finland_toe, "-", color='m', label = "Польша+Финляндия: {:.0f}".format(Poland_Finland_toe[len(Poland_toe)-1]))
ax2.plot( Year, Republics_toe, "-", color='b', label = "Польша+Финляндия+республики СССР: {:.0f}".format(Republics_toe[len(Republics_toe)-1]))
ax2.plot( Year, Russia_toe, "-", color='r', label = "Вся Российская империя: {:.0f}".format(Russia_toe[len(Russia_toe)-1]))
ax2.legend(loc=2)
ax2.set_ylabel("toe/км²")
ax2.set_xlim( 1850, 2050)
ax2.set_ylim( 0, 25000)
ax2.grid(True)
ax2.set_xlabel("Годы")

plt.savefig( "./Graphs/figure_13_04.png")
if InteractiveModeOn: plt.show(True)
