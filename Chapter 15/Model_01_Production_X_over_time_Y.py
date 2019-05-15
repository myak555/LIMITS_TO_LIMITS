from Predictions import *

Res = Resources()
Year = np.linspace( 1800, 2300, 501)
Oil_1P = Bathtub( 1965, s0=0.2, x1 = 2053.30, s1=2, middle=Res.Oil[-1]).GetVector(Year)
Oil_2P = Bathtub( 1965, s0=0.2, x1 = 2059.75, s1=2, middle=Res.Oil[-1]).GetVector(Year)
Oil_3P = Bathtub( 1965, s0=0.2, x1 = 2092.02, s1=2, middle=Res.Oil[-1]).GetVector(Year)
OGL_1P = Bathtub( 1965, s0=0.2, x1 = 2049.07, s1=1.5, middle=Res.Gas_and_Liquids[-1]).GetVector(Year)
OGL_2P = Bathtub( 1965, s0=0.2, x1 = 2063.93, s1=1.5, middle=Res.Gas_and_Liquids[-1]).GetVector(Year)
OGL_3P = Bathtub( 1965, s0=0.2, x1 = 2085.55, s1=1.5, middle=Res.Gas_and_Liquids[-1]).GetVector(Year)
All_1P = Bathtub( 1965, s0=0.2, x1 = 2061.58, s1=1.25, middle=Res.Total[-1]).GetVector(Year)
All_2P = Bathtub( 1965, s0=0.2, x1 = 2096.91, s1=1.25, middle=Res.Total[-1]).GetVector(Year)
All_3P = Bathtub( 1965, s0=0.2, x1 = 2264.75, s1=1.25, middle=Res.Total[-1]).GetVector(Year)

for i in range(len(Year)):
    j = int(Year[i] - Res.Year[0])
    if j < 0: continue
    if j >= len( Res.Year): break
    Oil_1P[i] = Res.Oil[j]
    Oil_2P[i] = Res.Oil[j]
    Oil_3P[i] = Res.Oil[j]
    OGL_1P[i] = Res.Gas_and_Liquids[j]
    OGL_2P[i] = Res.Gas_and_Liquids[j]
    OGL_3P[i] = Res.Gas_and_Liquids[j]
    All_1P[i] = Res.Total[j]
    All_2P[i] = Res.Total[j]
    All_3P[i] = Res.Total[j]

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Модель типа "При добыче Х запасов хватит на Y лет"', fontsize=22)
gs = plt.GridSpec(1, 1) 
ax1 = plt.subplot(gs[0])

ax1.errorbar( Res.Year, Res.Oil, yerr=Res.Oil_Error, fmt=".", color='g')
ax1.errorbar( Res.Year, Res.Gas_and_Liquids, yerr=Res.Gas_and_Liquids_Error, fmt=".", color='r')
ax1.errorbar( Res.Year, Res.Total, yerr=Res.Total_Error, fmt=".", color='k')
ax1.plot( Year, Oil_1P, "-", lw=2, color='g', label="Нефть (1P) URR={:.1f} млрд т".format(np.sum(Oil_1P)/1000))
#ax1.plot( Year, Oil_2P, "--", lw=2, color='g', label="Нефть (2P) URR={:.1f} млрд т".format(np.sum(Oil_2P)/1000))
ax1.plot( Year, Oil_3P, "-.", lw=2, color='g', label="Нефть (3P) URR={:.1f} млрд т".format(np.sum(Oil_3P)/1000))
ax1.plot( Year, OGL_1P, "-", lw=2, color='r', label="Жидкости и газ (1P) URR={:.1f} млрд т".format(np.sum(OGL_1P)/1000))
#ax1.plot( Year, OGL_2P, "--", lw=2, color='r', label="Жидкости и газ (2P) URR={:.1f} млрд т".format(np.sum(OGL_2P)/1000))
ax1.plot( Year, OGL_3P, "-.", lw=2, color='r', label="Жидкости и газ (3P) URR={:.1f} млрд т".format(np.sum(OGL_3P)/1000))
ax1.plot( Year, All_1P, "-", lw=2, color='k', label="Всё ископаемое топливо (1P) URR={:.1f} млрд т".format(np.sum(All_1P)/1000))
#ax1.plot( Year, All_2P, "--", lw=2, color='k', label="Всё ископаемое топливо (2P) URR={:.1f} млрд т".format(np.sum(All_2P)/1000))
ax1.plot( Year, All_3P, "-.", lw=2, color='k', label="Всё ископаемое топливо (3P) URR={:.1f} млрд т".format(np.sum(All_3P)/1000))
ax1.plot( [2048, 2048], [0, 13000], "--", lw=3, color='m')
ax1.set_xlim( 1800, 2300)
ax1.set_ylim( 0, 18000)
ax1.set_xlabel("Годы")
ax1.set_ylabel("Млн toe")
ax1.text(2060, 11800, "2048 год", color='m')
ax1.grid(True)
ax1.legend(loc=2)

plt.savefig( "./Graphs/figure_15_01.png")
fig.show()
