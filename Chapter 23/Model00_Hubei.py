from Population import *

strName = "провинции Хубей" 
dataName = "./Data/Hubei.csv"
nRight = 150000
detection = 1.4/10.7

Day, Onset, WHO_Cases, WHO_Cases2, WHO_Deaths = Load_Calibration(
    dataName, ["day", "onset", "cases", "cases_corr", "deaths"], separator='\t')
for limit,d in enumerate( Onset):
    if d>0: break
Onset_start = limit
for limit,d in enumerate( Onset[Onset_start:]):
    if d<0: break
Onset_end = limit
for limit,d in enumerate( WHO_Cases):
    if d>0: break
WHO_start = limit
WHO_end = len(WHO_Cases)
Onset_cum = Cumulative(Onset[Onset_start:Onset_end])

time = np.linspace(0, 183, 184)

Onset_Model = Linear_Combo()
Onset_Model.Wavelets += [Hubbert( x0=57.000, s0=0.30, s1=0.16, peak=3100)]
Onset_Model = Onset_Model.GetVector(time)
Onset_Model_cum = Cumulative(Onset_Model)

Death_Model = Linear_Combo()
Death_Model.Wavelets += [Sigmoid( x0=78.000, s0=0.16, right=3100)]
Death_Model = Death_Model.GetVector(time)
Death_Model_rate = Rate(Death_Model)

Report_Model = Linear_Combo()
Report_Model.Wavelets += [Sigmoid( x0=70.000, s0=0.21, right=48000)]
Report_Model = Report_Model.GetVector(time)
Report_Model_rate = Rate(Report_Model)

Infection_Model = Linear_Combo()
Infection_Model.Wavelets += [Hubbert( x0=52.000, s0=0.30, s1=0.16, peak=6200)]
Infection_Model = Infection_Model.GetVector(time)
Infection_Model_cum = Cumulative(Infection_Model)

xlimits =(0,106)
norm = 1e-3

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Эпидемия COVID-19 в {:s}'.format(strName), fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Day[Onset_start:Onset_end], Onset[Onset_start:Onset_end], 'o', lw=5, color='m', label="Начало симптомов (ВОЗ)")
ax1.plot( time, Onset_Model, '-', lw=3, color='m', label="Начало симптомов (модель)")
ax1.plot( time, Death_Model_rate*10, '-', lw=3, color='k', label="Смерти (модель) х 10")
ax1.plot( time, Report_Model_rate, '--', lw=3, color='g', label="Подача данных в ВОЗ до 17 февраля")
#ax1.plot( time, Infection_Model, '-.', lw=3, color='g', label="Вероятно инфицированных (модель)")
ax1.annotate('Первый официальный случай (он же первая смерть) 30 декабря',
                xy=(30,0),xytext=(5,-550),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Задержка результатов тестов 13 дней',
                xy=(70,2530),xytext=(40,4800),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Смерти через 21 день после первых симптомов',
                xy=(78,1250),xytext=(50,4300),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
#ax1.annotate('О заболевании доложено ВОЗ 3 января',
#                xy=(34,Onset[33]),xytext=(10,1200),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax1.annotate('Первый отчёт ВОЗ 20 января',
##                xy=(51,Onset[50]),xytext=(15,900),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 4000)
ax1.set_ylabel("в сутки")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( Day[Onset_start:Onset_end], Onset_cum*norm, 'o', lw=5, color='m', label="По началу симптомов (ВОЗ)")
ax2.plot( Day[WHO_start:WHO_end], WHO_Cases[WHO_start:WHO_end]*norm, 'o', lw=5, color='g', label="Подтверждённые случаи (ВОЗ)")
ax2.plot( time, Onset_Model_cum*norm, '-', lw=3, color='m', label="По началу симптомов (модель)")
ax2.plot( time, Report_Model*norm, '--', lw=3, color='g', label="Подача данных в ВОЗ до 17 февраля")
#ax2.plot( time, Infection_Model_cum*norm, '-.', lw=3, color='g', label="Вероятно инфицированных (модель)")
ax2.annotate('Маленький скачок симптомов 1 февраля',
                xy=(62,38),xytext=(5,30),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.annotate('Начало работы комиссии ВОЗ 16 февраля',
                xy=(78,39),xytext=(60,9),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.annotate('Большой скачок случаев 17 февраля',
                xy=(79,58),xytext=(50,80),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 90000*norm)
ax2.set_ylabel("всего (тысяч)")
ax2.grid(True)
ax2.legend(loc=0)

ax3.plot( Day[WHO_start:WHO_end], WHO_Deaths[WHO_start:WHO_end], 'o', lw=5, color='k', label="Подтверждённые смерти (ВОЗ)")
ax3.plot( time, Death_Model, '-', lw=3, color='k', label="Смерти (модель)")
#ax3.plot( time, Infection_Model_cum/100, '-.', lw=3, color='g', label="Вероятно инфицированных (модель) / 200")
ax3.annotate('Первый отчёт ВОЗ 20 января',
                xy=(51,4),xytext=(5,1000),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.set_xlim( xlimits)
ax3.set_ylim( 0, 4000)
ax3.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax3.set_ylabel("всего")
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_00_Hubei.png")

if InteractiveModeOn: plt.show(True)
