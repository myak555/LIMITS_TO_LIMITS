from Population import *

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", ["Year", "Production"])

Year = np.linspace( 1971, 2100, 130)
P_Norway_BP = np.array( [0.3,1.6,1.6,1.7,9.2,
                         13.7,14.0,17.4,19.5,25.0,
                         24.3,25.2,31.4,36.0,39.2,
                         43.0,50.1,57.0,74.9,82.1,
                         93.8,106.9,114.1,128.6,138.4,
                         154.7,156.2,149.6,149.7,160.7,
                         162.5,157.9,153.9,150.3,138.7,
                         129.0,118.6,114.8,108.7,98.8,
                         93.8,87.3,83.2,85.3,88.0,90.4,88.8])

P_Norway_Hub = Hubbert(1998.5,0.2,0.13,165).GetVector( Year)
P_Norway_Hub_2 = np.array( P_Norway_Hub)
P_Norway_Hub_2 += Hubbert(2025,0.18,0.13,70).GetVector( Year)
for i in range( len( P_Norway_BP)): P_Norway_Hub_2[i] = P_Norway_BP[i]

Cumulative_P = Cumulative( P_Norway_Hub_2)
Per_km2 = np.array( Cumulative_P) / 0.450

for i in range( len(Year)): print( "{:g}\t{:.3f}\t{:.3f}\t{:.1f}".format( Year[i], P_Norway_Hub_2[i], Cumulative_P[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.plot( Year, P_Norway_Hub, "--", lw=2, color="r", label="Классическая кривая Хабберта URR={:.1f} млрд т".format(np.sum(P_Norway_Hub)/1000))
plt.plot( Year[45:], P_Norway_Hub_2[45:], "--", lw=2, color="b", label="Оптимистическая модель URR={:.1f} млрд т".format(np.sum(P_Norway_Hub_2)/1000))
plt.plot( np.linspace( 1971,2017, len(P_Norway_BP)), P_Norway_BP, "-", lw=2, color="b", label="Добыча в Норвегии")
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")

plt.xlim( 1950, 2100)
plt.ylim( 0, 220)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Норвегии 1971-2017 гг')
plt.grid(True)
plt.legend(loc=1)
plt.savefig( "./Graphs/figure_14_05.png")
if InteractiveModeOn: plt.show(True)
