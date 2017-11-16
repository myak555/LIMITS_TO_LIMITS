from Population import *

BP_Year, BP_2008P = Load_Calibration( "01_BP_Oil_Liquids.csv", "Year", "2008")
BP_2009P, BP_2010P = Load_Calibration( "01_BP_Oil_Liquids.csv", "2009", "2010")
BP_2011P, BP_2012P = Load_Calibration( "01_BP_Oil_Liquids.csv", "2011", "2012")
BP_2014P, BP_2015P = Load_Calibration( "01_BP_Oil_Liquids.csv", "2014", "2015")
BP_2016P, BP_2017P = Load_Calibration( "01_BP_Oil_Liquids.csv", "2016", "2017")

diff_2008 = BP_2008P[:-9] * 100 / BP_2017P[:-9] 
diff_2009 = BP_2009P[:-8] * 100 / BP_2017P[:-8] 
diff_2010 = BP_2010P[:-7] * 100 / BP_2017P[:-7] 
diff_2011 = BP_2011P[:-6] * 100 / BP_2017P[:-6] 
diff_2012 = BP_2012P[:-5] * 100 / BP_2017P[:-5] 
diff_2014 = BP_2014P[:-3] * 100 / BP_2017P[:-3] 
diff_2015 = BP_2015P[:-2] * 100 / BP_2017P[:-2] 
diff_2016 = BP_2016P[:-1] * 100 / BP_2017P[:-1] 

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировая добыча нефти и жидкостей по отчётам "ВР" 2008-2017 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[:-9], BP_2008P[:-9], "--", lw=1, color='r', label="Отчёт 2008 г")
ax1.plot( BP_Year[:-8], BP_2009P[:-8], "--", lw=1, color='g', label="Отчёт 2009 г")
ax1.plot( BP_Year[:-7], BP_2010P[:-7], "--", lw=1, color='b', label="Отчёт 2010 г")
ax1.plot( BP_Year[:-6], BP_2011P[:-6], "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[:-5], BP_2012P[:-5], "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[:-3], BP_2014P[:-3], "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[:-2], BP_2015P[:-2], "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[:-1], BP_2016P[:-1], "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year, BP_2017P, "-", lw=1, color='k', label="Отчёт 2017 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=0)

ax2.plot( BP_Year[:-9], diff_2008, "--", lw=1, color='r')
ax2.plot( BP_Year[:-8], diff_2009, "--", lw=1, color='g')
ax2.plot( BP_Year[:-7], diff_2010, "--", lw=1, color='b')
ax2.plot( BP_Year[:-6], diff_2011, "--", lw=1, color='m')
ax2.plot( BP_Year[:-5], diff_2012, "--", lw=1, color='k')
ax2.plot( BP_Year[:-3], diff_2014, "-", lw=1, color='r')
ax2.plot( BP_Year[:-2], diff_2015, "-", lw=1, color='g')
ax2.plot( BP_Year[:-1], diff_2016, "-", lw=1, color='b')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 98, 102)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к отчёту 2017 г")

plt.savefig( ".\\Graphs\\figure_09_01.png")
fig.show()
