from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Year,Production = Load_Calibration( "./Data/Samotlor_Production.csv", ["Year", "Production"])
Intense = Hubbert( 2017, 0.6, 2, 20).GetVector( Year)
for i in range( 48, len(Production)): Production[i] = Intense[i]
Cumulative = np.array( Production)
for i in range( 1, len(Cumulative)): Cumulative[i] += Cumulative[i-1]

for i in range( len(Production)): print( "{:g}\t{:>8.1f}\t{:>8.1f}".format(Year[i], Production[i], Cumulative[i]))
print( "Total cumulative:{:.1f} mln t".format( np.sum( Production)))

fig = plt.figure( figsize=(15,15))

gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.errorbar( Year[0:48], Production[0:48], yerr=Production[0:48]*0.03, fmt='.', color="b", label="Добыча в год [млн т]")
ax1.plot( Year, Cumulative/10, "-", lw=2, color="k", label="Накопленная добыча [млн т х 10]")
ax1.plot( [1965,2038], [320,320], "--", lw=1, color="k")
ax1.plot( Year[48:], Production[48:], "-", lw=2, color="g", label="Добыча до 2020 г [млн т]")
ax1.annotate("Прекращение добычи в 2020 г", xy=(2020, 0), xytext=(2010, 100), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.set_xlim( 1965, 2038)
ax1.set_ylim( 0, 380)
ax1.set_xlabel( "Годы")
ax1.set_ylabel( "Добыча, млн т")
ax1.grid(True)
ax1.legend(loc=2)
ax1.set_title( 'Прогноз запасов Самотлора, гипотетическое прекращение добычи')

ax2.errorbar( Cumulative, 100*Production/Cumulative, fmt='o')
ax2.plot( [0,3200], [5.5,0], "--", lw=2, color="g", label="Общие запасы, включая ТрИЗ")
ax2.plot( [2650,2770], [10,0], "--", lw=2, color="r", label="Фиктивное снижение запасов")
ax2.annotate("K 2015 г извлечено 168 тыс т x 16'000 скважин", xy=(2700, 1), xytext=(2030, 6), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.annotate("K 2020 г извлечено 172 тыс т x 16'000 скважин", xy=(2750, 0), xytext=(2000, -2.5), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.set_ylim( 0, 10)
ax2.grid(True)
ax2.set_xlabel( "Q, млн т")
ax2.set_ylabel( "dQ x 1000")
ax2.legend(loc=2)

plt.savefig( "./Graphs/figure_09_18.png")
fig.show()
