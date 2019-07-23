from Population import *

data = './Data/Campbell_Laherrere_Backdated.csv'

Year, Oil = Load_Calibration( "../Global Data/Resources_Calibration.csv", ["Year", "Oil"])
Cumulative = np.array( Oil)
for i in range(1, len(Oil)):
    Cumulative[i] += Cumulative[i-1]
Cumulative /= 1000

Y1, R1998B, R1998R, R2014B, R2014R = Load_Calibration(
    data,
    ["Year", "R1998_Backdated", "R1998_Reported", "R2014_Backdated", "R2014_Reported"])

Year_1 = np.linspace( 1940, 1998, 59)
R1998_Backdated = np.zeros( len(Year_1))
R1998_Reported = np.zeros( len(Year_1))
for i in range( len(Year_1)):
    j = int(Year_1[i] - Y1[0])
    k = int(Year_1[i] - Year[0])
    R1998_Backdated[i] = R1998B[j] + Cumulative[k]
    R1998_Reported[i] = R1998R[j] + Cumulative[k]
Year_2 = np.linspace( 1920, 2010 , 91)
Year_3 = np.linspace( 1920, 2017, 98)
R2014_Backdated = np.zeros( len(Year_2))
R2014_Reported = np.zeros( len(Year_3))
for i in range( len(Year_2)):
    j = int(Year_2[i] - Y1[0])
    k = int(Year_2[i] - Year[0])
    R2014_Backdated[i] = R2014B[j] + Cumulative[k]
for i in range( len(Year_3)):
    j = int(Year_3[i] - Y1[0])
    k = int(Year_3[i] - Year[0])
    R2014_Reported[i] = R2014R[j] + Cumulative[k]

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценка начальных извлекаемых запасов сырой нефти', fontsize=22)
gs = plt.GridSpec(1, 1) 
ax1 = plt.subplot(gs[0])

ax1.errorbar( Year, Cumulative, yerr=Cumulative*0.05, fmt=".", color='g', label="Накопленная добыча")
ax1.plot( Year_1, R1998_Backdated, "--", lw=2, color='g', label="Campbell & Laherrere, 1998 (2P)")
ax1.plot( Year_1, R1998_Reported, "--", lw=2, color='r', label="British Petroleum, 1998 (1P)")
ax1.plot( Year_2, R2014_Backdated, "-", lw=2, color='g', label="Laherrere, 2014 (2P)")
ax1.plot( Year_3, R2014_Reported, "-", lw=2, color='r', label="EIA/OGJ, 2018 (1P)")
ax1.set_xlim( 1920, 2020)
ax1.set_ylim( 0, 400)
ax1.set_xlabel("Годы")
ax1.set_ylabel("Млрд тонн")
ax1.annotate("Венесуэла, 27 млрд т сверхтяжёлой", xy=(2010, 355), xytext=(1965, 380), arrowprops=dict(facecolor='r', shrink=0.05))
ax1.annotate("Канада, 24 млрд т битума", xy=(2001, 280), xytext=(1965, 330), arrowprops=dict(facecolor='r', shrink=0.05))
ax1.annotate("ОПЕК, 30 млрд т", xy=(1987, 193), xytext=(1960, 260), arrowprops=dict(facecolor='r', shrink=0.05))
ax1.annotate("Открытие Гавара", xy=(1947, 58), xytext=(1925, 125), arrowprops=dict(facecolor='r', shrink=0.05))
ax1.grid(True)
ax1.legend(loc=2)

plt.savefig( "./Graphs/figure_14_02.png")
if InteractiveModeOn: plt.show(True)
