from Population import *

time = np.linspace(0, 183, 184)
Model = Linear_Combo()
Model.Wavelets += [Sigmoid( x0=124.000, s0=0.27, left=0, right=500000)]

Model1 = Linear_Combo()
Model1.Wavelets += [Sigmoid( x0=105.000, s0=0.10, left=0, right=1e6)]

Model_Exp = np.exp(0.25*(time-73))
Model_Exp_Death = np.exp(0.21*(time-74))

Death_Rate = Weibull(x0=7.0, b=0.1, k=1.5, peak=0.0122).GetVector(time)

Model_WHO_Cases = Model.GetVector(time) 
Model_Total_Cases = Model1.GetVector(time) 
Model_Detection_Rate = Rate( Model_WHO_Cases)
Model_Infection_Rate = Rate( Model_Total_Cases)

#Model_Death_Rate = np.convolve(Death_Rate, Model_Infection_Rate)
#Model_Deaths = Cumulative( Model_Death_Rate)
#print(len(Model_Deaths), len(time))

Model_Deaths = Linear_Combo()
Model_Deaths.Wavelets += [Sigmoid( 143, 0.15, 0, 40000)]
#Model_Deaths.Wavelets += [Hubbert( x0=92.000, s0=0.26, s1=0.26, peak=4)]
Model_Deaths = Model_Deaths.GetVector(time)
Model_Death_Rate = Rate(Model_Deaths)

Day, WHO_Cases, WHO_Deaths = Load_Calibration("./Data/USA.csv", ["day", "cases", "deaths"], separator='\t')
for limit,d in enumerate( WHO_Deaths):
    if d<0: break

xlimits =(0,184)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Эпидемия COVID-19 в США', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

#ax1.plot( Day[0:limit], WHO_Cases[0:limit], 'o', lw=5, color='b', label="Случаи-ВОЗ")
ax1.plot( Day[0:limit], WHO_Deaths[0:limit]*10, 'o', lw=5, color='r', label="Смерти-ВОЗ (х10)")
#ax1.plot( time, Model_Total_Cases, '--', color='g', lw=2, label="Инфицировано (мoдель)")
#ax1.plot( time, Model_WHO_Cases, '-', color='g', lw=3, label="Выявлено (мoдель)")
ax1.plot( time, Model_Deaths[:184]*10, '-', color='k', lw=2, label="Смерти (модель, х10)")
#ax1.plot( time, Model_Exp, '-.', color='g', lw=3, label="Тупая экспонента бледнолисых")
#ax1.plot( time, Model_Exp_Death, '-.', color='k', lw=3, label="Расчёт смертей у бледнолисых (х10)")
ax1.annotate('Ожидаемый IFR={:.1f}%'.format(Model_Deaths[-1]*100/Model_WHO_Cases[-1]),
                xy=(175,102500),xytext=(130,150000),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Первый диагноз 23 января',
                xy=(54,10),xytext=(5,10000),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Первые две смерти 3 марта',
                xy=(94,10),xytext=(5,20000),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 50000)
ax1.set_ylabel("единиц")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( time, Model_Infection_Rate, "--", lw=2, color='g', label="Заразились (модель)")
ax2.plot( time, Model_Detection_Rate, "-", lw=3, color='g', label="Выявлено (модель)")
ax2.plot( time, Model_Death_Rate[:184]*10, "-", lw=3, color='k', label="Смертей (x10)")
ax2.annotate('Первый диагностированный в прилетел в США 20 января',
                xy=(51,19),xytext=(5,40),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 20000)
ax2.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax2.set_ylabel("в сутки")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_06_USA.png")

if InteractiveModeOn: plt.show(True)
