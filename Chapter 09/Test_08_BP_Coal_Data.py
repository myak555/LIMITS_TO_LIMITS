from Population import *

datafile1 = "./Data/06_BP_Coal.csv"
BP_Year, BP_2008P = Load_Calibration( datafile1, "Year", "2008")
BP_2009P, BP_2010P = Load_Calibration( datafile1, "2009", "2010")
BP_2011P, BP_2012P = Load_Calibration( datafile1, "2011", "2012")
BP_2014P, BP_2015P = Load_Calibration( datafile1, "2014", "2015")
BP_2016P, BP_2017P = Load_Calibration( datafile1, "2016", "2017")
BP_2016P, BP_2018P = Load_Calibration( datafile1, "2016", "2018")

datafile2 = "./Data/07_BP_Coal.csv"
BP_Year, BP_2008C = Load_Calibration( datafile2, "Year", "2008")
BP_2009C, BP_2010C = Load_Calibration( datafile2, "2009", "2010")
BP_2011C, BP_2012C = Load_Calibration( datafile2, "2011", "2012")
BP_2014C, BP_2015C = Load_Calibration( datafile2, "2014", "2015")
BP_2016C, BP_2017C = Load_Calibration( datafile2, "2016", "2017")
BP_2016C, BP_2018C = Load_Calibration( datafile2, "2016", "2018")

diff_2008 = BP_2008P - BP_2008C 
diff_2009 = BP_2009P - BP_2009C 
diff_2010 = BP_2010P - BP_2010C 
diff_2011 = BP_2011P - BP_2011C 
diff_2012 = BP_2012P - BP_2012C 
diff_2014 = BP_2014P - BP_2014C 
diff_2015 = BP_2015P - BP_2015C 
diff_2016 = BP_2016P - BP_2016C 
diff_2017 = BP_2017P - BP_2017C 
diff_2018 = BP_2018P - BP_2018C 

delta_2008 = diff_2008 * 100 / BP_2018P 
delta_2009 = diff_2009 * 100 / BP_2018P 
delta_2010 = diff_2010 * 100 / BP_2018P 
delta_2011 = diff_2011 * 100 / BP_2018P 
delta_2012 = diff_2012 * 100 / BP_2018P 
delta_2014 = diff_2014 * 100 / BP_2018P 
delta_2015 = diff_2015 * 100 / BP_2018P 
delta_2016 = diff_2016 * 100 / BP_2018P 
delta_2017 = diff_2017 * 100 / BP_2018P
delta_2018 = diff_2018 * 100 / BP_2018P

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировoе потребление каменного угля по отчётам "ВР" 2008-2018 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[16:-10], diff_2008[16:-10], "--", lw=1, color='r', label="Отчёт 2008 г")
ax1.plot( BP_Year[16:-9], diff_2009[16:-9], "--", lw=1, color='g', label="Отчёт 2009 г")
ax1.plot( BP_Year[16:-8], diff_2010[16:-8], "--", lw=1, color='b', label="Отчёт 2010 г")
ax1.plot( BP_Year[16:-7], diff_2011[16:-7], "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[16:-6], diff_2012[16:-6], "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[16:-4], diff_2014[16:-4], "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[16:-3], diff_2015[16:-3], "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[16:-2], diff_2016[16:-2], "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year[16:-1], diff_2017[16:-1], "-", lw=1, color='y', label="Отчёт 2017 г")
ax1.plot( BP_Year[16:], diff_2018[16:], "-", lw=1, color='k', label="Отчёт 2018 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.set_ylim( -150, 400)
ax1.grid(True)
ax1.set_title( 'Разница между "добычей" и "потреблением"')
ax1.legend(loc=0)

ax2.plot( BP_Year[16:-10], delta_2008[16:-10], "--", lw=1, color='r')
ax2.plot( BP_Year[16:-9], delta_2009[16:-9], "--", lw=1, color='g')
ax2.plot( BP_Year[16:-8], delta_2010[16:-8], "--", lw=1, color='b')
ax2.plot( BP_Year[16:-7], delta_2011[16:-7], "--", lw=1, color='m')
ax2.plot( BP_Year[16:-6], delta_2012[16:-6], "--", lw=1, color='k')
ax2.plot( BP_Year[16:-4], delta_2014[16:-4], "-", lw=1, color='r')
ax2.plot( BP_Year[16:-3], delta_2015[16:-3], "-", lw=1, color='g')
ax2.plot( BP_Year[16:-2], delta_2016[16:-2], "-", lw=1, color='b')
ax2.plot( BP_Year[16:-1], delta_2017[16:-1], "-", lw=1, color='y')
ax2.plot( BP_Year[16:], delta_2018[16:], "-", lw=1, color='k')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( -5, 5)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к добыче 2018 г")

plt.savefig( ".\\Graphs\\figure_09_08.png")
fig.show()

##dd = 0
##for i in range( len( diff_2017)):
##    dd += diff_2017[i]
##    print( BP_Year[i], dd)
