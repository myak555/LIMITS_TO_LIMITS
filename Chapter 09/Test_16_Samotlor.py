from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Year,Production = Load_Calibration( "./Data/Samotlor_Production.csv", ["Year", "Production"])
Cumulative = np.array( Production)
for i in range( 1, len(Cumulative)): Cumulative[i] += Cumulative[i-1]

for i in range( len(Production)): print( "{:g}\t{:>8.1f}\t{:>8.1f}".format(Year[i], Production[i], Cumulative[i]))

fig = plt.figure( figsize=(15,15))

gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.errorbar( Year[0:48], Production[0:48], yerr=Production[0:48]*0.03, fmt='.', color="b", label="Добыча в год [млн т]")
ax1.errorbar( [1969.5,1987.5,2001.5,2014.5], [200,90,75,60], yerr=[200*0.6,90*0.25,75*0.10,60*0.05], fmt='o', color="r", label="Остаточные извлекаемые [млн т х 10]" )
ax1.plot( Year, Cumulative/10, "-", lw=2, color="k", label="Накопленная добыча [млн т х 10]")
ax1.plot( [1965,2038], [320,320], "--", lw=1, color="k")
ax1.plot( Year[48:], Production[48:], "-", lw=2, color="g", label="Добыча до 2038 г [млн т]")
ax1.annotate("Пик добычи: 158.9 млн т в 1980 г", xy=(1980, 159), xytext=(1990, 190), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("TNK-BP инвестирует в КРС $1 млрд, 2003 г", xy=(2003, 26), xytext=(1993, 170), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Вексельберг покупает яйца, 2004 г", xy=(2004, 30), xytext=(2010, 150), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Роснефть покупает TNK-BP, 2013 г", xy=(2013, 24), xytext=(2015, 130), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Уплотнение сетки скважин, 2014 г", xy=(2014, 22), xytext=(2020, 110), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.set_xlim( 1965, 2038)
ax1.set_ylim( 0, 380)
ax1.set_xlabel( "Годы")
ax1.set_ylabel( "Добыча, млн т")
ax1.grid(True)
ax1.legend(loc=2)
ax1.set_title( 'Прогноз запасов Самотлора, 1969-2038 гг')

ax2.errorbar( Cumulative[0:48], 100*Production[0:48]/Cumulative[0:48], fmt='o')
ax2.plot( [1500,2250], [10,0], "--", lw=2, color="r", label="Запасы в залежах БВ7, БВ8(1-2-3), AB6-8")
ax2.plot( [0,3200], [5.5,0], "--", lw=2, color="g", label="Общие запасы, включая ТрИЗ")
ax2.annotate("K 2015 г извлечено 168 тыс т x 16'000 скважин", xy=(2700, 1), xytext=(2030, 6), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.annotate("K 2099 г извлечено 106 тыс т x 30'000 скважин", xy=(3200, 0), xytext=(2100, -2.5), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.set_ylim( 0, 10)
ax2.grid(True)
ax2.set_xlabel( "Q, млн т")
ax2.set_ylabel( "dQ/Q, %")
ax2.legend(loc=2)

plt.savefig( "./Graphs/figure_09_16.png")
if InteractiveModeOn: plt.show(True)
