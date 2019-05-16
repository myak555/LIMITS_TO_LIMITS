from Population import *

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", ["Year", "Production"])

Year = np.linspace( 1953, 2017, 65)
P_Australia_BP = np.array( [0.3,0.4,1.0,1.9,2.2,
                         8.7,15.3,16.3,20.4,20.2,
                        21.6,22.1,23.4,23.2,23.3,
                        21.8,21.3,21.0,20.4,26.5,
                        30.7,27.4,29.1,27.7,26.1,
                        30.3,28.6,28.2,26.3,28.3,
                        26.7,28.1,29.8,28.2,27.5,
                        37.1,34.3,34.1,29.5,25.8,
                        25.3,23.5,24.5,24.1,22.4,
                        24.5,21.5,21.4,17.8,19.1,
                        17.4,15.5,14.8])

P_Australia = Hubbert( 1976,0.4,0.1,23.5).GetVector( Year)
for i in range( 12, len(P_Australia)): P_Australia[i] = P_Australia_BP[i-12]
    
Cumulative_P = Cumulative( P_Australia)
Per_km2 = np.array( Cumulative_P) / 7.6920 / 1.10

for i in range( len(Year)): print( "{:g}\t{:.3f}\t{:.3f}\t{:.1f}".format( Year[i], P_Australia[i], Cumulative_P[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.plot( Year, P_Australia, "-", lw=2, color="r", label="Добыча в Австралии, UR={:.3f} млрд т".format(np.sum(P_Australia)/1000))
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")

plt.xlim( 1950, 2020)
plt.ylim( 0, 50)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Австралии 1953-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_14_08.png")
if InteractiveModeOn: plt.show(True)
