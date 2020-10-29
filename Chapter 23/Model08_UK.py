from Population import *
import datetime as dti

strName = "Великобритании" 
dataName = "./Data/UK.csv"
nRight = 180
detection = 1.4/10.7

Day, WHO_Cases, WHO_Deaths = Load_Calibration(dataName, ["day","cases","deaths"], separator='\t')
for limit,d in enumerate( WHO_Deaths):
    if d<0: break
Day = Day[0:limit]
WHO_Cases = WHO_Cases[0:limit]
WHO_Deaths = WHO_Deaths[0:limit]
WHO_Cases_Rate = np.roll(Filter( Rate(WHO_Cases), matrix=[1,1,2,1,1]), 0)
WHO_Cases_Rate[0] = 0

dta = dti.date(2020, 1, 20)
f = open("./Data/UK_Boats.csv", "w")
f.write("Date\tWHO_Cases\tdelta\n")
for d,r in enumerate(WHO_Cases_Rate):
    f.write("{:s}\t{:.1f}\t{:.1f}\n".format(str(dta), WHO_Cases[d], r))
    dta += dti.timedelta(days=1)
f.close()

#for d,r in enumerate(WHO_Cases_Rate):
#    print("{:d}\t{:.1f}".format(d, r))
    
time = np.linspace(0, 183, 184)

Exp_Model = np.exp(0.23*(time-82))

Detected_Model = Linear_Combo()
Detected_Model.Wavelets += [Hubbert( x0=120.5, s0=0.390, s1=0.200, peak=2545)]
Detected_Model.Wavelets += [Hubbert( x0=110.5, s0=0.80, s1=0.60, peak=380)]
Detected_Model.Wavelets += [Hubbert( x0=105.5, s0=0.45, s1=0.30, peak=110)]
Detected_Model_Rate = Detected_Model.GetVector(time)
Detected_Model_Cum = Cumulative( Detected_Model_Rate)

Infected_Model = Linear_Combo()
#Infected_Model.Wavelets += [Hubbert( x0=114, s0=0.255, s1=0.150, peak=100000)]
Infected_Model.Wavelets += [Hubbert( x0=120, s0=0.255, s1=0.150, peak=100000)]
#Infected_Model.Wavelets += [Hubbert( x0=112, s0=0.45, s1=0.150, peak=500)]
Infected_Model_Rate = Infected_Model.GetVector(time)
Infected_Model_Cum = Cumulative( Infected_Model_Rate)

#for d,r in enumerate(Infected_Model_Rate):
#    print("{:d}\t{:.1f}".format(d, r))

#IDR = 0.008
IDR = 0.025
survival_rate = 1-IDR
symptomatic = 0.5
Contageous_function = Bathtub( x0=5.0, s0=1.6, x1 = 14.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(time)
Symptom_function = Bathtub( x0=7.0, s0=1.5, x1 = 23.0, s1=0.6, left=0.0, middle=symptomatic, right=0.0).GetVector(time)
Severe_function = Bathtub( x0=12.0, s0=1.0, x1 = 23.0, s1=0.6, left=0.0, middle=0.075, right=0.0).GetVector(time)
Death_function = Sigmoid( x0=30.0, s0=0.13, left=0, right=IDR).GetVector(time)
Immune_function = Sigmoid( x0=12.0, s0=0.5, left=0, right=survival_rate).GetVector(time)
Recovery_function = np.ones(len(time))*(symptomatic)
Recovery_function -= Death_function 
Recovery_function = np.clip( Recovery_function - Symptom_function, 0, symptomatic)  
a = np.argmax(Symptom_function)
Recovery_function[0:a] = 0.0

Contageous_Model_Cum = np.convolve( Infected_Model_Rate, Contageous_function)[:len(time)]
Symptomatic_Model_Cum = np.convolve( Infected_Model_Rate, Symptom_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Recovery_Model_Cum = np.convolve( Infected_Model_Rate, Recovery_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Death_Model_Cum = np.convolve( Infected_Model_Rate, Death_function)[:len(time)]

xlimits =(0,184)
norm = 1e-3

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Эпидемия COVID-19 в {:s}'.format(strName), fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Day, WHO_Cases*norm, 'o', lw=5, color='g', label="Случаи-ВОЗ")
ax1.plot( time, Infected_Model_Cum*norm, '--', color='g', lw=3, label="Инфицировано (мoдель)")
ax1.plot( time, Contageous_Model_Cum*norm, '-.', color='g', lw=3, label="Заразных (мoдель)")
ax1.plot( time, Symptomatic_Model_Cum*norm, '-', color='m', lw=3, label="Больных (мoдель)")
ax1.plot( time, Recovery_Model_Cum*norm, '-', color='y', lw=3, label="Выздоровевших (мoдель)")
ax1.plot( time, Detected_Model_Cum*norm, '-', color='g', lw=3, label="Выявлено (мoдель)")
#ax1.plot( time, Exp_Model*norm, '-.', color='g', lw=2, label="Экспонента бледнолисых")
ax1.annotate('2 подтверждённыx случая 1 февраля',
                xy=(63,10*norm),xytext=(5,3000*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Около 12 тыс инфицировано',
                xy=(120,Infected_Model_Cum[120]*norm),xytext=(50,16500*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Не более 2 тыс имели симптомы',
                xy=(120,Recovery_Model_Cum[120]*norm),xytext=(100,38000*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 45000*norm)
ax1.set_ylabel("тысяч инфицированных")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( Day, WHO_Deaths, 'o', lw=5, color='k', label="Смерти-ВОЗ")
ax2.plot( time, Severe_Model_Cum, '-', color='r', lw=3, label="Тяжёлых и критических пациентов (мoдель)")
ax2.plot( time, Death_Model_Cum, '-', color='k', lw=2, label="Смерти (модель)")
#ax2.annotate('Ожидаемый cIFR={:.1f}%'.format(Model_Deaths[-1]*100/Model_WHO_Cases[-1]),
#                xy=(175,Model_Deaths[-1]),xytext=(130,Model_Deaths[-1]*0.5),
#                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
#                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.annotate('Первая смерть 7 марта',
                xy=(98,10),xytext=(5,50),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 50000)
ax2.set_ylabel("пациентов")
ax2.grid(True)
ax2.legend(loc=0)

ax3.plot( Day+0.5, WHO_Cases_Rate, "o", lw=2, color='g', label="Подтверждённые случаи (ВОЗ)")
ax3.plot( time, Detected_Model_Rate, "-", lw=2, color='g', label="Подтверждённые случаи (модель)")
ax3.plot( time, Infected_Model_Rate, "--", lw=3, color='g', label="Заразились (модель)")
ax3.plot( [41,51], [50,50], "-", lw=5, color='k')

ax3.annotate('Первый случай завезён с 15 по 25 января',
                xy=(46,50),xytext=(-10,-500),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Ruby Princess 8 марта (158 вероятных, 2 положительных)',
                xy=(99,10),xytext=(5,-100),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Ruby Princess 19 марта (2700 вероятных, 133 положительных)',
                xy=(110,10),xytext=(30,-200),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Выборы в Квинследе 28 марта',
                xy=(119,10),xytext=(65,-300),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.set_xlim( xlimits)
ax3.set_ylim( 0, 3000)
ax3.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax3.set_ylabel("в сутки")
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_07_Australia.png")

if False:
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Параметры заразности, симптомов и летальности', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.plot( time, Contageous_function, "-", lw=2, color='g',
              label="Заразность")
    ax1.plot( time, Symptom_function, "-", lw=2 , color='m',
              label="Симптомы")
    ax1.plot( time, Severe_function, "-", lw=2, color='r',
              label="В том числе, тяжёлых")
    ax1.plot( time, Recovery_function, "-", lw=2 , color='y',
              label="Выздоровление")
    ax1.set_xlim( 0, 75)
    ax1.set_ylim( 0, 1.0)
    ax1.set_ylabel("Часть заразившихся")
    ax1.grid(True)
    ax1.legend(loc=0)
    ax2.plot( time, Severe_function, "-", lw=3, color='r',
              label="Тяжёлых и критических пациентов")
    ax2.plot( time, Death_function, "-", lw=3 , color='k',
          label="Умерших")
    ax2.set_xlim( 0, 75)
    ax2.set_ylim( 0, 0.08)
    ax2.set_xlabel("День после заражения")
    ax2.set_ylabel("Часть заразившихся")
    ax2.grid(True)
    ax2.legend(loc=0)
    plt.savefig( "./Graphs/Model_Parameters.png")

if InteractiveModeOn: plt.show(True)
