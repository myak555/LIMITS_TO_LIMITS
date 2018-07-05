from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", "Year", "Production")

Year = np.linspace( 1965, 2117, 153)
P_UK_BP = np.array( [ 0.1,0.1,0.1,0.1,0.1,
                   0.2,0.2,0.3,0.4,0.4,
                   1.6,12.2,38.3,54.0,77.9,
                   80.5,89.5,103.2,115.0,126.1,
                  127.6,127.1,123.4,114.5,91.7,
                   91.6,91.3,94.3,100.2,126.5,
                  129.9,129.7,127.9,132.6,137.0,
                  126.3,116.8,116.1,106.3,95.6,
                   85.1,76.9,76.9,72.0,68.3,
                   63.2,52.1,44.7,40.7,40.0,
                   45.4,47.5,46.6])

P_UK_1 = np.zeros( len(Year))
P_UK_2 = np.zeros( len(Year))
for i in range( len(P_UK_BP)):
    P_UK_1[i] = P_UK_BP[i]
    P_UK_2[i] = P_UK_BP[i]
for i in range( len(P_UK_BP), len(Year)):
    P_UK_1[i] = P_UK_1[i-1] * 0.94
    P_UK_2[i] = P_UK_2[i-1] * 0.89
Cumulative = np.array( P_UK_1)
for i in range( 1, len(Cumulative)): Cumulative[i] += Cumulative[i-1]

Per_km2 = np.array( Cumulative) / 0.24250 / 1.10

for i in range( len(Year)): print( "{:g},{:.3f},{:.3f},{:.1f}".format( Year[i], P_UK_1[i], Cumulative[i], Per_km2[i]))

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))

plt.plot( np.linspace( 1965,2017, len(P_UK_BP)), P_UK_BP, "-", lw=2, color="b", label="Добыча в Великобритании, UR={:.3f} млрд т".format(np.sum(P_UK_BP)/1000))
plt.plot( Year[52:], P_UK_1[52:], "--", lw=2, color="r", label="Прогнозная 2016 года, URR={:.1f} млрд т".format(np.sum(P_UK_1)/1000))
plt.plot( Year[52:], P_UK_2[52:], "--", lw=2, color="m", label="Прогнозная 2018 года, URR={:.1f} млрд т".format(np.sum(P_UK_2)/1000))
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")
plt.xlim( 1930, 2120)
plt.ylim( 0, 170)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Великобритании 1965-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_14_05.png")
fig.show()
