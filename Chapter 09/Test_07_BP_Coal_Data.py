from Population import *

BP_Year, BP_2008P, BP_2009P, BP_2010P, BP_2011P, BP_2012P, BP_2014P, BP_2015P, BP_2016P, BP_2017P, BP_2018P = Load_Calibration(
    "./Data/06_BP_Coal.csv",
    ["Year", "2008", "2009", "2010", "2011", "2012", "2014", "2015", "2016", "2017", "2018"])

diff_2008 = BP_2008P[16:-10] * 100 / BP_2018P[16:-10] 
diff_2009 = BP_2009P[16:-9] * 100 / BP_2018P[16:-9] 
diff_2010 = BP_2010P[16:-8] * 100 / BP_2018P[16:-8] 
diff_2011 = BP_2011P[16:-7] * 100 / BP_2018P[16:-7] 
diff_2012 = BP_2012P[16:-6] * 100 / BP_2018P[16:-6] 
diff_2014 = BP_2014P[16:-4] * 100 / BP_2018P[16:-4] 
diff_2015 = BP_2015P[16:-3] * 100 / BP_2018P[16:-3] 
diff_2016 = BP_2016P[16:-2] * 100 / BP_2018P[16:-2] 
diff_2017 = BP_2017P[16:-1] * 100 / BP_2018P[16:-1] 

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировая добыча каменного угля по отчётам "ВР" 2008-2018 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[16:-10], BP_2008P[16:-10], "--", lw=1, color='r', label="Отчёт 2008 г")
ax1.plot( BP_Year[16:-9], BP_2009P[16:-9], "--", lw=1, color='g', label="Отчёт 2009 г")
ax1.plot( BP_Year[16:-8], BP_2010P[16:-8], "--", lw=1, color='b', label="Отчёт 2010 г")
ax1.plot( BP_Year[16:-7], BP_2011P[16:-7], "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[16:-6], BP_2012P[16:-6], "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[16:-4], BP_2014P[16:-4], "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[16:-3], BP_2015P[16:-3], "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[16:-2], BP_2016P[16:-2], "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year[16:-1], BP_2017P[16:-1], "-", lw=1, color='y', label="Отчёт 2017 г")
ax1.plot( BP_Year[16:], BP_2018P[16:], "-", lw=1, color='k', label="Отчёт 2018 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=0)

ax2.plot( BP_Year[16:-10], diff_2008, "--", lw=1, color='r')
ax2.plot( BP_Year[16:-9], diff_2009, "--", lw=1, color='g')
ax2.plot( BP_Year[16:-8], diff_2010, "--", lw=1, color='b')
ax2.plot( BP_Year[16:-7], diff_2011, "--", lw=1, color='m')
ax2.plot( BP_Year[16:-6], diff_2012, "--", lw=1, color='k')
ax2.plot( BP_Year[16:-4], diff_2014, "-", lw=1, color='r')
ax2.plot( BP_Year[16:-3], diff_2015, "-", lw=1, color='g')
ax2.plot( BP_Year[16:-2], diff_2016, "-", lw=1, color='b')
ax2.plot( BP_Year[16:-1], diff_2017, "-", lw=1, color='y')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 95, 105)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к отчёту 2018 г")

plt.savefig( "./Graphs/figure_09_07.png")
fig.show()
