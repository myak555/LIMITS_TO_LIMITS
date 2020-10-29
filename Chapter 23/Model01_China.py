from Population import *

time = np.linspace(0, 183, 184)
China_Model_Infected = Hubbert( x0=57, s0=0.31, s1=0.167, peak=3050).GetVector(time)
China_Model_Cum = Cumulative( China_Model_Infected)

China_Actual = np.array( [
   278,  310,  390,  571,  835, 1297, 1985, 2761, 4537, 5997,
  7736, 9720,11821,14411,17238,20471,24363,28060,31211,34598,
 37251,40235,42708,44730,46550,48548,50054,51174,70635,72528,
 74280,74675,75569,76392,77042,77262,77780,78191,78630,78961,
 79394,79968,80174,80304,80422,80565,80711,80817,80859,80904,
 80924,80955,80981,80991,81021,81048,81077,81116,81116,81174,
 81416,81498,81550,81601])
atime = np.linspace(51, 51+len(China_Actual), len(China_Actual))


xlimits =(0,184)
norm = 1e-3

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Эпидемия COVID-19 в КНР', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( atime, China_Actual*norm, '.', color='r', label="Случаи ВОЗ")
ax1.plot( time+10, China_Model_Cum*norm*1.1, '-', color='g', label="Moдель")
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 100)
ax1.set_ylabel("тысяч")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( time, China_Model_Infected*norm, "-", lw=2, color='g', label="Лабораторные (нач.симптомов)")
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 4)
ax2.set_xlabel("День эпидемии (0 - 30 ноября 2019)")
ax2.set_ylabel("тысяч в сутки")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_00_China.png")

if InteractiveModeOn: plt.show(True)
