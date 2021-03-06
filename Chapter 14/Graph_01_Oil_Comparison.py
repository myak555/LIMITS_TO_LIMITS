from Population import *

Year_Model = np.linspace(1830,2200,371)
Production_Hubbert = Hubbert( 2000, .041, .0345, 1700).GetVector(Year_Model)
Production_Campbell = Hubbert( 2005, .080, .059, 3300).GetVector(Year_Model)

Year, Oil, Condensate, NGPL = Load_Calibration(
    "../Global Data/Resources_Calibration.csv",
    ["Year", "Oil", "Condensate", "NGPL"])
Liquids = Oil + Condensate + NGPL
for i in range(1830,1956):
    j = i-1830
    Production_Hubbert[j] = Oil[j]
for i in range(1830,1999):
    j = i-1830
    Production_Campbell[j] = Oil[j]

Oil_Cum = Cumulative( Oil)
Hubbert_Cum = Cumulative( Production_Hubbert)
Campbell_Cum = Cumulative( Production_Campbell)

for i, y in enumerate(Year):
    print( "{:g}\t{:.1f}".format(y, Oil_Cum[i]))

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценка добытых запасов сырой нефти 1860-2017 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.errorbar( Year, Oil, yerr=Oil*0.05, fmt=".", color='g', label="Реальная")
ax1.plot( Year_Model, Production_Hubbert, "-", lw=1, color='r', label="Hubbert, 1956: URR={:.0f} млрд т".format(np.sum(Production_Hubbert)/1000))
ax1.plot( Year_Model, Production_Campbell, "-", lw=1, color='b', label="Campbell/Laherrere, 1998: URR={:.0f} млрд т".format(np.sum(Production_Campbell)/1000))
ax1.set_xlim( 1850, 2100)
ax1.set_ylim( 0, 5000)
ax1.set_ylabel("Млн тонн в год")
ax1.grid(True)
ax1.set_title( 'Годовая добыча')
ax1.legend(loc=2)

ax2.errorbar( Year, Oil_Cum/1000, yerr=Oil_Cum/1000*0.05, fmt=".", color='g', label="Реальная по 2017 г: {:.0f} млрд т".format(np.sum(Oil)/1000))
ax2.plot( Year_Model, Hubbert_Cum/1000, "-", lw=1, color='r')
ax2.plot( Year_Model, Campbell_Cum/1000, "-", lw=1, color='b')
ax2.annotate("К 1955 году, {:.0f} млрд т".format(Oil_Cum[1956-1830]/1000), xy=(1955, 11), xytext=(1870, 80), arrowprops=dict(facecolor='b', shrink=0.05))
ax2.annotate("К 1997 году, {:.0f} млрд т".format(Oil_Cum[1998-1830]/1000), xy=(1997, 107), xytext=(1870, 110), arrowprops=dict(facecolor='r', shrink=0.05))
ax2.set_xlim( 1850, 2100)
ax2.set_ylim( 1, 250)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млрд тонн")
ax2.grid(True)
ax2.set_title( "Накопленная добыча")
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_14_01.png")
if InteractiveModeOn: plt.show(True)
