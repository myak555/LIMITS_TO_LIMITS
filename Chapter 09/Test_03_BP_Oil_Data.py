from Population import *

BP_Year, BP_2008P, BP_2009P, BP_2010P, BP_2011P, BP_2012P, BP_2014P, BP_2015P, BP_2016P, BP_2017P, BP_2018P, BP_2019P = Load_Calibration(
    "./Data/03_BP_Oil_Density.csv",
    ["Year", "2008", "2009", "2010", "2011", "2012", "2014", "2015", "2016", "2017", "2018", "2019"])

P2 = Hubbert( 2022, .15, .1, 3.0).GetVector( BP_Year)
P2 += Hubbert( 1980, 1.2, 1.2, 0.1).GetVector( BP_Year)
P2 += Hubbert( 1984.5, 1, 1, 0.15).GetVector( BP_Year)
P2 += Hubbert( 1988, 1, .5, 0.20).GetVector( BP_Year)
P2 += Hubbert( 1998, .3, .8, 0.25).GetVector( BP_Year)
P2 += Hubbert( 2004, 1, 1, 0.25).GetVector( BP_Year)
P2 += Hubbert( 2007, 1, 1, 0.10).GetVector( BP_Year)
P2 *= 365 * 0.159

Y_NGPL = np.linspace(2000, 2018, 19)
NGPL_Percent_By_Volume = [9.2,9.4,9.7,9.2,9.2,9.3,9.3,9.4,9.5,10.2,10.7,11.3,11.5,11.6,12.1,12.3,12.9,13.3,13.9]
NGPL_Tonn = [236.39,241.70,247.66,244.12,256.76,262.13,265.91,268.28,272.80,
             284.47,302.88,321.06,336.36,339.49,361.54,377.92,396.08,409.76,435.97]
NGPL = [363.67,371.85,381.01,375.57,395.02,403.28,409.09,412.74,419.70,437.65,
        465.97,493.93,517.47,522.29,556.21,581.42,609.35,630.40,670.73]

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Средняя плотность нефти и жидкостей по отчётам "ВР" 2008-2019 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2.5, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[:-11], BP_2008P[:-11], "--", lw=2, color='r')
ax1.plot( BP_Year[:-10], BP_2009P[:-10], "--", lw=2, color='g')
ax1.plot( BP_Year[:-9], BP_2010P[:-9], "--", lw=2, color='b')
ax1.plot( BP_Year[:-8], BP_2011P[:-8], "--", lw=2, color='m')
ax1.plot( BP_Year[:-7], BP_2012P[:-7], "--", lw=2, color='k')
ax1.plot( BP_Year[:-5], BP_2014P[:-5], "-", lw=2, color='r')
ax1.plot( BP_Year[:-4], BP_2015P[:-4], "-", lw=2, color='g')
ax1.plot( BP_Year[:-3], BP_2016P[:-3], "-", lw=2, color='b')
ax1.plot( BP_Year[:-2], BP_2017P[:-2], "-", lw=2, color='m')
ax1.plot( BP_Year[:-1], BP_2018P[:-1], "-", lw=2, color='k')
ax1.plot( BP_Year, BP_2019P, "-", lw=5, color='y', alpha=0.5, label="Отчёт 2019 г")
ax1.plot( [1965, 2020], [0.827,0.827], "-.", lw=1, color='k', label="WTI 0.827 г/см³")
ax1.plot( [1965, 2020], [0.835,0.835], "-.", lw=1, color='m', label="Brent 0.835 г/см³")
ax1.plot( [1965, 2020], [0.780,0.780], "-.", lw=1, color='r', label="Конденсат API 0.780 г/см³")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Средняя плотность добытой нефти")
ax1.set_ylim( 0.77, 0.87)
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=3)

ax2.plot( BP_Year, P2, "-", lw=2, color='k', label="Добыча битума в Канаде")
ax2.plot( Y_NGPL, NGPL, "-", lw=2, color='r', label="Мировая добыча ШФЛУ")
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 0, 700)
ax2.set_xlabel("Годы")
ax2.set_ylabel("млн м³")
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_title( "Добыча битума и ШФЛУ")

plt.savefig( "./Graphs/figure_09_03.png")
if InteractiveModeOn: plt.show(True)
