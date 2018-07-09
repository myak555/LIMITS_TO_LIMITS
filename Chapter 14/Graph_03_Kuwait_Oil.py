from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", "Year", "Production")

Year = np.linspace( 1946, 2199, 254)
Year_BP = np.linspace( 1965, 2017, 53)
P_Kuwait_BP = np.array( [119.0,125.6,126.4,133.1,140.9,
                         151.8,162.5,167.3,153.8,129.9,
                         106.3,109.9,100.8,108.8,129.6,
                         86.8,58.6,42.7,55.0,60.7,
                         55.5,59.4,52.1,63.0,68.4,
                         46.8,9.2,54.0,96.6,103.4,
                         104.9,105.1,105.1,110.0,102.6,
                         109.9,106.6,98.8,115.6,123.3,
                         130.4,133.7,129.9,136.1,120.9,
                         123.3,140.8,153.9,151.3,150.1,
                         148.2,152.7,146.0])

P_Burgan = Hubbert( 1971, 0.2, 0.07, 167).GetVector( Year)
for i in range( 28): P_Burgan[i+19] = P_Kuwait_BP[i] 
P_Кuwait = P_Burgan + Hubbert( 2014, 0.20, 0.07, 125).GetVector( Year)
for i in range( 53): P_Кuwait[i+19] = P_Kuwait_BP[i] 

Cumulative = np.array( P_Кuwait)
for i in range( 1, len(Cumulative)): Cumulative[i] += Cumulative[i-1]

Per_km2 = np.array( Cumulative) / 0.018

for i in range( len(Year)): print( "{:g},{:.3f},{:.3f},{:.1f}".format( Year[i], P_Кuwait[i], Cumulative[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.errorbar( Year_BP, P_Kuwait_BP, yerr=P_Kuwait_BP*0.05, fmt='.', color="g", label="Добыча в Кувейте по данным ВР UR = {:.1f} млрд т".format(np.sum(P_Kuwait_BP)/1000))
plt.plot( Year, P_Burgan, "--", lw=2, color="g", label="Добыча из месторождения Бурган (оценка) URR = {:.1f} млрд т".format(np.sum(P_Burgan)/1000))
plt.plot( Year[50:], P_Кuwait[50:], "-", lw=2, color="b", label="Добыча из всех месторождений (оценка) URR = {:.1f} млрд т".format(np.sum(P_Кuwait)/1000))
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")
plt.annotate("Эмбарго ОПЕК 1973 года", xy=(1972, 167), xytext=(1945, 175), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Иранский кризис 1979 года", xy=(1979, 130), xytext=(1945, 110), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Вторжение Ирака 1990 года", xy=(1990, 69), xytext=(1945, 60), arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlim( 1940, 2040)
plt.ylim( 0, 220)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Кувейте 1946-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_14_03.png")
fig.show()
