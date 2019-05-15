from Population import *

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", ["Year", "Production"])

Year = np.linspace( 1956, 2099, 144)
P_Syria_BP = np.array( [1.0,2.6,4.2,5.3,5.8,
                        5.5,6.4,9.6,10.0,9.1,
                        8.9,8.3,7.9,8.2,7.7,
                        8.0,8.1,7.9,10.0,11.5,
                        13.4,16.9,20.2,23.5,25.6,
                        28.1,28.0,29.6,29.2,28.7,
                        28.6,28.8,28.1,29.9,32.7,
                        31.6,23.5,21.7,20.3,19.5,
                        19.6,19.3,18.5,16.9,8.1,
                        2.7,1.5,1.2,1.1,1.1])

P_Syria = np.ones( len(Year)) * 0.2
for i in range( len(P_Syria_BP)): P_Syria[i+12] += P_Syria_BP[i]
d = Hubbert( 2012, 0.10, 0.066, 9).GetVector( Year[55:])

P_Syria_1 = np.array( P_Syria)
for i in range( 55, len(P_Syria_1)): P_Syria_1[i] = d[i-55]

Cumulative_P = Cumulative( P_Syria_1)
Per_km2 = np.array( Cumulative_P) / 0.185

for i in range( len(Year)): print( "{:g}\t{:.3f}\t{:.3f}\t{:.1f}".format( Year[i], P_Syria_1[i], Cumulative_P[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.plot( Year, P_Syria, "-", lw=2, color="r", label="Добыча в Сирии по данным ВР")
plt.plot( Year[55:], d, "--", lw=2, color="r", label="Вероятная добыча ИГИЛ (URR = {:.1f} млрд т)".format( np.sum(P_Syria_1)/1000))
plt.annotate("Добыто 770 млн т", xy=(2012, 9), xytext=(1990, 10), arrowprops=dict(facecolor='black', shrink=0.05))
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")
plt.plot( [2012,2012], [0,10], "--", lw=2, color="b")

plt.xlim( 1950, 2030)
plt.ylim( 0, 50)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Сирии 1956-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_14_07.png")
fig.show()
