from Population import *

BP_Year, BP_2008P, BP_2009P, BP_2010P, BP_2011P, BP_2012P, BP_2014P, BP_2015P, BP_2016P, BP_2017P, BP_2018P = Load_Calibration(
    "./Data/01_BP_Oil_Liquids.csv",
    ["Year", "2008", "2009", "2010", "2011", "2012", "2014", "2015", "2016", "2017", "2018"])

BP_Year, BP_2008C, BP_2009C, BP_2010C, BP_2011C, BP_2012C, BP_2014C, BP_2015C, BP_2016C, BP_2017C, BP_2018C = Load_Calibration(
    "./Data/02_BP_Oil_Liquids.csv",
    ["Year", "2008", "2009", "2010", "2011", "2012", "2014", "2015", "2016", "2017", "2018"])

diff_2008 = BP_2008P[:-10] - BP_2008C[:-10] 
diff_2009 = BP_2009P[:-9] - BP_2009C[:-9] 
diff_2010 = BP_2010P[:-8] - BP_2010C[:-8] 
diff_2011 = BP_2011P[:-7] - BP_2011C[:-7] 
diff_2012 = BP_2012P[:-6] - BP_2012C[:-6] 
diff_2014 = BP_2014P[:-4] - BP_2014C[:-4] 
diff_2015 = BP_2015P[:-3] - BP_2015C[:-3] 
diff_2016 = BP_2016P[:-2] - BP_2016C[:-2] 
diff_2017 = BP_2017P[:-1] - BP_2017C[:-1] 
diff_2018 = BP_2018P - BP_2018C

delta_2008 = diff_2008 * 100 / BP_2017P[:-10] 
delta_2009 = diff_2009 * 100 / BP_2017P[:-9] 
delta_2010 = diff_2010 * 100 / BP_2017P[:-8] 
delta_2011 = diff_2011 * 100 / BP_2017P[:-7] 
delta_2012 = diff_2012 * 100 / BP_2017P[:-6] 
delta_2014 = diff_2014 * 100 / BP_2017P[:-4] 
delta_2015 = diff_2015 * 100 / BP_2017P[:-3] 
delta_2016 = diff_2016 * 100 / BP_2017P[:-2] 
delta_2017 = diff_2017 * 100 / BP_2017P[:-1]
delta_2018 = diff_2018 * 100 / BP_2018P

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировoе потребление нефти и жидкостей по отчётам "ВР" 2008-2018 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[:-10], diff_2008, "--", lw=1, color='r', label="Отчёт 2008 г")
ax1.plot( BP_Year[:-9], diff_2009, "--", lw=1, color='g', label="Отчёт 2009 г")
ax1.plot( BP_Year[:-8], diff_2010, "--", lw=1, color='b', label="Отчёт 2010 г")
ax1.plot( BP_Year[:-7], diff_2011, "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[:-6], diff_2012, "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[:-4], diff_2014, "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[:-3], diff_2015, "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[:-2], diff_2016, "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year[:-1], diff_2017, "-", lw=1, color='y', label="Отчёт 2017 г")
ax1.plot( BP_Year, diff_2018, "-", lw=1, color='k', label="Отчёт 2018 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.set_ylim( -150, 400)
ax1.grid(True)
ax1.set_title( 'Разница между "добычей" и "потреблением"')
ax1.legend(loc=0)

ax2.plot( BP_Year[:-10], delta_2008, "--", lw=1, color='r')
ax2.plot( BP_Year[:-9], delta_2009, "--", lw=1, color='g')
ax2.plot( BP_Year[:-8], delta_2010, "--", lw=1, color='b')
ax2.plot( BP_Year[:-7], delta_2011, "--", lw=1, color='m')
ax2.plot( BP_Year[:-6], delta_2012, "--", lw=1, color='k')
ax2.plot( BP_Year[:-4], delta_2014, "-", lw=1, color='r')
ax2.plot( BP_Year[:-3], delta_2015, "-", lw=1, color='g')
ax2.plot( BP_Year[:-2], delta_2016, "-", lw=1, color='b')
ax2.plot( BP_Year[:-1], delta_2017, "-", lw=1, color='y')
ax2.plot( BP_Year, delta_2018, "-", lw=1, color='k')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( -10, 10)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к добыче 2018 г")

plt.savefig( "./Graphs/figure_09_02.png")
fig.show()

dd = 0
for i in range( len( diff_2018)):
    dd += diff_2018[i]
    print( "{:d}\t{:>8.1f}".format( int(BP_Year[i]), dd))
