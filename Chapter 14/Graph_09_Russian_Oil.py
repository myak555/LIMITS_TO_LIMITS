from Population import *

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", ["Year", "Production"])
Year_Samotlor = Year_Samotlor[:-82]
P_Samotlor = P_Samotlor[:-82]

Year = np.linspace( 1860, 2017, 158)
P_RussianEmpire = np.array( [4,4,4,6,9,
                    9,13,17,29,42,
                    33,26,27,68,86,
                   132,191,253,334,403,
                   352,663,827,991,1479,
                  1905,1896,2360,3013,3281,
                  3778,4527,4690,5530,4916,
                  6745,6795,7275,8331,8958,
                 10378,11562,11080,10415,10888,
                  7556,8171,8655,8739,9296,
                  9626,9176,9292,9234,9176,
                  9442,9970,8800,4146,4448,
                  3851,3781,4658,5277,6064,
                  7061,8318,10285,11625,13684,
                 18451,22329,21414,21489,24218,
                 25218,27427,28501,30186,30259,
                 31121,18000,18000,18000,18000,
                 19436,21746,26022,29249,33444,
                 37878,42253,47311,52777,59281,
                 70793,83806,98346,113216,129557,
                147859,168000,188000,208000,228000,
                242888,265100,288100,309200,328300,
                353039,377000,400400,429000,458900,
                490801,519677,545799,571531,585600,
                603180,608820,612551,616343,612710,
                598244,617655,627306,626060,609282,
                572638,518442,453691,405203,365961,
                360485,354790,363007,363538,370717,
                397311,428519,469486,516792,561443,
                580084,604093,627799,630294,648664,
                662535,664691,668936,677314,677953,
                683553,695367,700577])

P_RussianEmpire = P_RussianEmpire/1000

Year_Poland = np.linspace( 1980,2017,38)
P_Poland = np.array( [8,8,5.5,5,5,
                      5,5,4,4,3.3,
                      2.2,3.1,3.2,5,5.1,
                      4.7,5.1,6.1,7.4,11,
                      14.4,16.6,16.3,16.1,27.7,
                      31.1,33.4,27.6,28.1,25.3,
                      20.0,19.7,19.1,25.2,30.3,
                      30.4,32.1,32.3])
P_Poland = P_Poland*365/1000*0.159*0.85

Year_Republics = np.linspace( 1985,2017,33)
P_Republics = np.array( [55.9,56.5,57.8,57.3,57.1,
                      56.7,56.5,54.9,50.3,48.4,
                      49.7,51.9,55.6,59.2,65.9,
                      70.6,76.8,85.8,91.1,98.1,
                     105.3,118.4,131.0,136.6,147.8,
                     150.7,145.8,142.8,146.2,143.8,
                     142.8,141.0,146.2])
for i in range( len(Year_Republics)): P_Republics[i] += P_Poland[i+5] 
for i in range( len(Year_Poland)): P_RussianEmpire[i+120] += P_Poland[i] 

P_WithoutSamotlor = np.array( P_RussianEmpire)
for i in range( len(Year_Samotlor)): P_WithoutSamotlor[i+109] -= P_Samotlor[i] 

Cumulative_P = Cumulative( P_RussianEmpire)
Per_km2 = np.array( Cumulative_P) / 23.0533

for i in range( len(Year)): print( "{:g}\t{:.3f}\t{:.3f}\t{:.1f}".format( Year[i], P_RussianEmpire[i], Cumulative_P[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.plot( Year, P_RussianEmpire, "-", lw=2, color="r", label="Добыча в странах бывш. Российской Империи, UR={:.3f} млрд т".format(np.sum(P_RussianEmpire)/1000))
plt.plot( Year, P_WithoutSamotlor, "--", lw=2, color="r", label="Без Самотлорского месторождения")
plt.plot( Year_Republics, P_Republics, "-", lw=2, color="g", label="Страны бывш. Российской Империи, кроме РФ")
plt.annotate("Добыто за пределами РФ с 1988 по 2017: {:.0f} млн т".format( np.sum(P_Republics[3:])), xy=(2000, 70), xytext=(1870, 200), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Добыто на Самотлоре с 1969 по 2017: {:.0f} млн т".format( np.sum(P_Samotlor)), xy=(1980, 500), xytext=(1870, 300), arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlim( 1860, 2020)
plt.ylim( 0, 750)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в странах бывшей Российской Империи 1860-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_14_09.png")
if InteractiveModeOn: plt.show(True)
