from Population import *

Year, Coal = Load_Calibration( "Resources_Calibration.csv", "Year", "Coal")
Bitumen, Oil = Load_Calibration( "Resources_Calibration.csv", "Bitumen", "Oil")
Condensate, NGPL = Load_Calibration( "Resources_Calibration.csv", "Condensate", "NGPL")
Gas, Total = Load_Calibration( "Resources_Calibration.csv", "Gas", "Total")

Coal_Cum = np.array( Coal)
Bitumen_Cum = np.array( Bitumen)
Oil_Cum = np.array( Oil)
Condensate_Cum = np.array( Condensate)
Gas_Cum = np.array( Gas)
NGPL_Cum = np.array( NGPL)
Total_Cum = np.array( Total)

for i in range( 1, len(Year)):
    Coal_Cum[i] += Coal_Cum[i-1]
    Bitumen_Cum[i] += Bitumen_Cum[i-1]
    Oil_Cum[i] += Oil_Cum[i-1]
    Condensate_Cum[i] += Condensate_Cum[i-1]
    Gas_Cum[i] += Gas_Cum[i-1]
    NGPL_Cum[i] += NGPL_Cum[i-1]
    Total_Cum[i] += Total_Cum[i-1]
    print( Year[i], Total_Cum[i]) 

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценка добытых запасов 1860-2017 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( Year, Coal, "-", lw=2, color='k', label="Каменный уголь и торф")
ax1.plot( Year, Bitumen, "-", lw=2, color=(0.3,0.3,0.3), label="Природный битум")
ax1.plot( Year, Oil, "-", lw=2, color='g', label="Чёрная нефть")
ax1.plot( Year, Condensate, "-", lw=2, color=(0.3,1,0.3), label="Лицензионный конденсат")
ax1.plot( Year, NGPL, "-", lw=2, color='m', label="ШФЛУ и др. жидкости")
ax1.plot( Year, Gas, "-", lw=2, color='r', label="Природный газ")
ax1.plot( Year, Gas+NGPL+Condensate, "--", lw=2, color='r', label="Природный газ+ШФЛУ+конденсат")
ax1.annotate("Нефтяной век, 1963 г", xy=(1963, 1350), xytext=(1950, 3800), arrowprops=dict(facecolor='g', shrink=0.05))
ax1.annotate("Газовый век, 2006 г", xy=(2006, 3200), xytext=(1970, 4200), arrowprops=dict(facecolor='r', shrink=0.05))
ax1.set_xlim( 1860, 2020)
ax1.set_ylim( 0, 5000)
ax1.set_ylabel("Млн тонн нефт. эквивалента в год")
ax1.grid(True)
ax1.set_title( 'Годовая добыча')
ax1.legend(loc=0)

ax2.plot( Year, Coal_Cum/1000, "-", lw=2, color='k', label="Каменный уголь и торф {:.0f} млрд т".format(np.sum(Coal)/1000))
ax2.plot( Year, Bitumen_Cum/1000, "-", lw=2, color=(0.3,0.3,0.3), label="Природный битум {:.0f} млрд т".format(np.sum(Bitumen)/1000))
ax2.plot( Year, Oil_Cum/1000, "-", lw=2, color='g', label="Чёрная нефть {:.0f} млрд т".format(np.sum(Oil)/1000))
ax2.plot( Year, Condensate_Cum/1000, "-", lw=2, color=(0.3,1,0.3), label="Лицензионный конденсат {:.0f} млрд т".format(np.sum(Condensate)/1000))
ax2.plot( Year, NGPL_Cum/1000, "-", lw=2, color='m', label="ШФЛУ и др. жидкости {:.0f} млрд т".format(np.sum(NGPL)/1000))
ax2.plot( Year, Gas_Cum/1000, "-", lw=2, color='r', label="Природный газ {:.0f} млрд т".format(np.sum(Gas)/1000))
ax2.set_xlim( 1860, 2020)
ax2.set_ylim( 1, 1000)
ax2.set_yscale("log", nonposy='clip')
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млрд тонн нефт. эквивалента")
ax2.grid(True)
ax2.set_title( "Накопленная добыча")
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_13_01.png")
fig.show()
