from Population import *

BP_Year, BP_2008P, BP_2009P, BP_2010P, BP_2011P, BP_2012P, BP_2014P, BP_2015P, BP_2016P, BP_2017P, BP_2018P = Load_Calibration(
    "./Data/10_BP_Renewable.csv",
    ["Year", "2008", "2009", "2010", "2011", "2012", "2014", "2015", "2016", "2017", "2018"])

diff_2011 = BP_2011P * 100 / BP_2018P 
diff_2012 = BP_2012P * 100 / BP_2018P 
diff_2014 = BP_2014P * 100 / BP_2018P 
diff_2015 = BP_2015P * 100 / BP_2018P 
diff_2016 = BP_2016P * 100 / BP_2018P 
diff_2017 = BP_2017P * 100 / BP_2018P 

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировое производство возобновляемой энергии по отчётам "ВР" 2008-2018 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[26:-7], BP_2011P[26:-7], "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[26:-6], BP_2012P[26:-6], "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[:-4], BP_2014P[:-4], "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[:-3], BP_2015P[:-3], "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[:-2], BP_2016P[:-2], "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year[:-1], BP_2017P[:-1], "-", lw=1, color='y', label="Отчёт 2017 г")
ax1.plot( BP_Year, BP_2018P, "-", lw=1, color='k', label="Отчёт 2018 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.grid(True)
ax1.set_title( "Абсолютные значения (кроме гидро)")
ax1.legend(loc=0)

ax2.plot( BP_Year[26:-7], diff_2011[26:-7], "--", lw=1, color='m')
ax2.plot( BP_Year[26:-6], diff_2012[26:-6], "--", lw=1, color='k')
ax2.plot( BP_Year[:-4], diff_2014[:-4], "-", lw=1, color='r')
ax2.plot( BP_Year[:-3], diff_2015[:-3], "-", lw=1, color='g')
ax2.plot( BP_Year[:-2], diff_2016[:-2], "-", lw=1, color='b')
ax2.plot( BP_Year[:-1], diff_2017[:-1], "-", lw=1, color='y')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 50, 110)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к отчёту 2018 г")

plt.savefig( "./Graphs/figure_09_11.png")
if InteractiveModeOn: plt.show(True)
