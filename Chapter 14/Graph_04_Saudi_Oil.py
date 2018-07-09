from Population import *

Year_Samotlor, P_Samotlor = Load_Calibration("./Data/Samotlor_Production.csv", "Year", "Production")

Year = np.linspace( 1938, 2017, 80)
P_Saudi_BP = np.array( [111.0,130.8,141.3,154.2,162.7,
                     192.2,240.8,304.2,384.0,429.7,
                     359.3,437.3,468.4,424.4,488.0,
                     509.8,506.3,340.2,240.3,219.0,
                     172.1,252.6,221.1,276.5,271.1,
                     342.6,428.4,442.4,432.8,437.2,
                     437.2,445.4,453.2,454.4,422.4,
                     456.0,440.4,425.2,486.2,500.4,
                     521.3,508.9,488.9,509.9,456.7,
                     473.8,525.9,549.8,538.4,543.4,
                     567.8,585.7,561.7])

P_Saudi = Hubbert( 1969,0.15,0.1,130).GetVector( Year)
for i in range( 27, len(P_Saudi)): P_Saudi[i] = P_Saudi_BP[i-27]

Cumulative = np.array( P_Saudi)
for i in range( 1, len(Cumulative)): Cumulative[i] += Cumulative[i-1]

Per_km2 = np.array( Cumulative) / 2.1497 / 1.05

for i in range( len(Year)): print( "{:g},{:.3f},{:.3f},{:.1f}".format( Year[i], P_Saudi[i], Cumulative[i], Per_km2[i]))

fig = plt.figure( figsize=(15,10))

plt.plot( Year, P_Saudi, "-", lw=2, color="r", label="Добыча в Саудовской Аравии, UR = {:.1f} млрд т".format(np.sum(P_Saudi)/1000))
plt.plot( Year_Samotlor, P_Samotlor, "--", lw=1, color="g", label="Добыча на Самотлоре (для сравнения)")
plt.annotate("Эмбарго ОПЕК 1973 года", xy=(1973, 398), xytext=(1945, 450), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Иранский кризис 1979 года", xy=(1979, 498), xytext=(1945, 550), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Вторжение Ирака в Кувейт 1990 года", xy=(1990, 355), xytext=(1945, 250), arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlim( 1930, 2020)
plt.ylim( 0, 750)
plt.xlabel( "Год")
plt.ylabel( "миллионов тонн в год")
plt.title( 'Добыча нефти в Саудовской Аравии 1938-2017 гг')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_14_04.png")
fig.show()
